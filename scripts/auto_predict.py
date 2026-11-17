import os
import re
import time
import json
import glob
import requests
from datetime import datetime, timedelta, timezone
from bs4 import BeautifulSoup
from google import genai
from google.genai import types

JST = timezone(timedelta(hours=9))
API_KEY = os.environ.get("GEMINI_API_KEY", "").strip()
client = genai.Client(api_key=API_KEY) if API_KEY else None

os.makedirs("data", exist_ok=True)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
}

VENUE_MAP = {
    "01": "札幌", "02": "函館", "03": "福島", "04": "新潟", "05": "東京",
    "06": "中山", "07": "中京", "08": "京都", "09": "阪神", "10": "小倉"
}

def decode_html(res: requests.Response) -> str:
    """UTF-8とEUC-JPを自動判別して文字化けを防ぐ"""
    content = res.content
    if b"charset=utf-8" in content.lower() or b"charset=\"utf-8\"" in content.lower():
        return content.decode("utf-8", errors="ignore")
    try:
        return content.decode("utf-8")
    except UnicodeDecodeError:
        return content.decode("euc_jp", errors="ignore")

def fetch_race_list_by_date(ymd: str) -> list:
    """指定日(YYYYMMDD)のJRA全会場・全レース一覧を自動取得する"""
    url = f"https://race.netkeiba.com/top/race_list_sub.html?kaisai_date={ymd}"
    try:
        res = requests.get(url, headers=HEADERS, timeout=15)
        html = decode_html(res)
        soup = BeautifulSoup(html, "html.parser")
        races = []
        for li in soup.select("li.RaceList_DataItem"):
            a_tag = li.select_one("a[href*='race_id=']")
            if not a_tag:
                continue
            m = re.search(r"race_id=(\d{12})", a_tag.get("href", ""))
            if not m:
                continue
            race_id = m.group(1)
            venue_code = race_id[4:6]
            venue_name = VENUE_MAP.get(venue_code, "JRA")
            race_num = int(race_id[10:12])

            title_el = li.select_one(".ItemTitle")
            name = title_el.get_text(strip=True) if title_el else f"{race_num}R"
            time_el = li.select_one(".RaceList_Itemtime")
            post_time = time_el.get_text(strip=True) if time_el else "15:00"
            long_el = li.select_one(".RaceList_ItemLong")
            surf_dist = long_el.get_text(strip=True) if long_el else ""

            races.append({
                "raceId": race_id,
                "venue": venue_name,
                "raceNumber": race_num,
                "venueLabel": f"{venue_name}{race_num}R",
                "name": name,
                "surfaceDist": surf_dist,
                "postTime": post_time,
                "rank": "New" if ("新馬" in name or "メイクデビュー" in name) else "B",
                "skill": "app-bayesian-make-debut" if ("新馬" in name or "メイクデビュー" in name) else "app-bayesian-horse-racing-text",
                "predicted": False
            })
        return races
    except Exception as e:
        print(f"[Warn] fetch_race_list_by_date failed ({ymd}): {e}")
        return []

def find_target_kaisai_date(now: datetime) -> tuple[str, list]:
    """当日開催があれば当日、平日テスト時は直近または次回のJRA開催日を自動検出"""
    candidates = [0, 1, 2, 3, 4, 5, -1, -2, -3, -4, -5, -6]
    for offset in candidates:
        dt = now + timedelta(days=offset)
        ymd = dt.strftime("%Y%m%d")
        date_str = dt.strftime("%Y-%m-%d")
        races = fetch_race_list_by_date(ymd)
        if len(races) >= 6:
            print(f"[Auto-Detect] 開催日 {date_str} ({len(races)}レース) を自動取得しました。")
            return date_str, races
    return now.strftime("%Y-%m-%d"), []

def fetch_race_detail_and_odds(race_id: str) -> str:
    """出馬表・過去走馬柱・オッズ・結果をWebから自動取得してテキスト化する"""
    lines = []
    # 1. 出馬表＋過去5走馬柱の取得
    try:
        url = f"https://race.netkeiba.com/race/shutuba_past.html?race_id={race_id}"
        res = requests.get(url, headers=HEADERS, timeout=15)
        soup = BeautifulSoup(decode_html(res), "html.parser")

        r_data = soup.select_one(".RaceData01")
        r_data2 = soup.select_one(".RaceData02")
        if r_data:
            lines.append("【レース条件】" + " ".join(r_data.get_text(" ", strip=True).split()))
        if r_data2:
            lines.append("【開催情報】" + " ".join(r_data2.get_text(" ", strip=True).split()))

        # オッズAPIから単勝オッズを取得
        odds_map = {}
        try:
            o_url = f"https://race.netkeiba.com/api/api_get_jra_odds.html?race_id={race_id}&type=1&action=init"
            o_res = requests.get(o_url, headers=HEADERS, timeout=10).json()
            o_data = o_res.get("data", {}).get("official_datetime") and o_res["data"].get("odds", {}).get("1", {})
            if isinstance(o_data, dict):
                for h_num, vals in o_data.items():
                    if isinstance(vals, list) and len(vals) > 0:
                        odds_map[int(h_num)] = vals[0]
        except Exception:
            pass

        lines.append("【出走馬・過去走要約】")
        for tr in soup.select("tr.HorseList"):
            waku = tr.select_one("td[class^='Waku']")
            umaban = tr.select_one("td[class^='Umaban']")
            name_el = tr.select_one(".Horse02 a, .HorseName a")
            jockey_el = tr.select_one(".Jockey a, td.Jockey")
            weight_el = tr.select_one("td.Weight")
            pasts = [ " ".join(td.get_text(" ", strip=True).split())[:90] for td in tr.select("td.Past")[:3] ]

            num_str = umaban.get_text(strip=True) if umaban else ""
            num_int = int(num_str) if num_str.isdigit() else 0
            w_str = waku.get_text(strip=True) if waku else ""
            h_name = name_el.get_text(strip=True) if name_el else ""
            j_info = " ".join(jockey_el.get_text(" ", strip=True).split()) if jockey_el else ""
            w_info = weight_el.get_text(strip=True) if weight_el else ""
            odd_str = odds_map.get(num_int, "")

            lines.append(f"{w_str}枠 {num_str}番 {h_name} ({j_info} 馬体重:{w_info} オッズ:{odd_str}) | 近走: {' / '.join(pasts)}")
    except Exception as e:
        print(f"[Warn] fetch_race_detail failed ({race_id}): {e}")

    # 2. 確定結果・単勝オッズ補完（終了済みレースの場合）
    try:
        r_url = f"https://race.netkeiba.com/race/result.html?race_id={race_id}"
        r_res = requests.get(r_url, headers=HEADERS, timeout=10)
        r_soup = BeautifulSoup(decode_html(r_res), "html.parser")
        top_rows = r_soup.select("#All_Result_Table tbody tr")[:5]
        if top_rows:
            res_summary = []
            for tr in top_rows:
                tds = [td.get_text(strip=True) for td in tr.select("td")]
                if len(tds) >= 11:
                    res_summary.append(f"{tds[0]}着:{tds[2]}番{tds[3]}(単{tds[10]}倍/上り{tds[11] if len(tds)>11 else ''})")
            lines.append("【参考確定着順・オッズ】" + " / ".join(res_summary))
    except Exception:
        pass

    return "\n".join(lines)

def load_skill_prompt(skill_name: str) -> str:
    path = f"skills/{skill_name}/SKILL.md"
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return "Output valid JSON only."

def call_gemini_json(skill_name: str, prompt_text: str, prefer_pro: bool = False) -> dict:
    if not client:
        return {"error": "GEMINI_API_KEY is not set"}

    system_instruction = load_skill_prompt(skill_name)
    models_to_try = ["gemini-2.5-pro", "gemini-2.5-flash"] if prefer_pro else ["gemini-2.5-flash"]

    for model_id in models_to_try:
        try:
            time.sleep(4)
            response = client.models.generate_content(
                model=model_id,
                contents=prompt_text,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    response_mime_type="application/json",
                    temperature=0.1,
                ),
            )
            text = (response.text or "").strip()
            if text.startswith("```"):
                text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text, flags=re.DOTALL)
            return json.loads(text)
        except Exception as e:
            print(f"[Warn] {model_id} failed: {e}")
            continue
    return {"error": "API limit or error"}

def run_pipeline():
    now = datetime.now(JST)
    date_str, scraped_races = find_target_kaisai_date(now)
    db_path = f"data/{date_str}.json"

    if os.path.exists(db_path):
        with open(db_path, "r", encoding="utf-8") as f:
            day_db = json.load(f)
    else:
        day_db = {
            "date": date_str,
            "updatedAt": now.strftime("%Y-%m-%d %H:%M JST"),
            "screened": False,
            "races": scraped_races,
            "win5": {}
        }

    if not day_db.get("races") and scraped_races:
        day_db["races"] = scraped_races

    # 1. 会場ごとの自動スクリーニング（未実行時のみ・1会場1リクエスト）
    if day_db.get("races") and not day_db.get("screened"):
        venues = sorted(list({r["venue"] for r in day_db["races"]}))
        for v in venues:
            v_races = [r for r in day_db["races"] if r["venue"] == v]
            # メイン10R・11Rの馬柱詳細をサンプル取得して馬場傾向・スクリーニング精度を高める
            sample_details = []
            for r in v_races:
                if r["raceNumber"] in (10, 11) or "新馬" in r["name"]:
                    sample_details.append(f"■{r['venueLabel']} {r['name']} ({r['surfaceDist']})\n" + fetch_race_detail_and_odds(r["raceId"])[:2500])

            prompt = (
                f"【モード: スクリーニング】日付:{date_str} 会場:{v}\n"
                f"レース一覧:{json.dumps(v_races, ensure_ascii=False)}\n"
                f"主要レース出馬表詳細:\n" + "\n".join(sample_details)
            )
            res = call_gemini_json("app-bayesian-horse-racing-text", prompt, prefer_pro=False)
            if isinstance(res, dict) and "races" in res:
                rank_map = {int(item.get("raceNumber", 0)): item for item in res["races"] if isinstance(item, dict)}
                for r in day_db["races"]:
                    if r["venue"] == v and r["raceNumber"] in rank_map:
                        sc = rank_map[r["raceNumber"]]
                        if "新馬" not in r["name"]:
                            r["rank"] = sc.get("rank", r["rank"])
                        r["pivotType"] = sc.get("pivotType", "Dual-Pivot")
                        r["nLead"] = sc.get("nLead", 3)
                        r["expectedRoi"] = sc.get("expectedRoi", 110.0)
                        r["hitRate"] = sc.get("hitRate", 42.0)
                        r["summary"] = sc.get("summary", "")
        day_db["screened"] = True

    # 2. 発走1時間前レース（または手動テスト時は未予想の主要勝負レース最大2鞍）の本予想を自動実行
    target_queue = []
    for race in day_db.get("races", []):
        if race.get("predicted") or race.get("rank") == "Pass":
            continue
        post_time = race.get("postTime", "
