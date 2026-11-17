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
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/124.0.0.0"}
VENUE_MAP = {
    "01": "札幌", "02": "函館", "03": "福島", "04": "新潟", "05": "東京",
    "06": "中山", "07": "中京", "08": "京都", "09": "阪神", "10": "小倉"
}

def decode_html(res: requests.Response) -> str:
    raw = res.content
    if b"utf-8" in raw[:1024].lower():
        return raw.decode("utf-8", errors="ignore")
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:
        return raw.decode("euc_jp", errors="ignore")

def fetch_race_list_by_date(ymd: str) -> list:
    url = f"https://race.netkeiba.com/top/race_list_sub.html?kaisai_date={ymd}"
    try:
        res = requests.get(url, headers=HEADERS, timeout=15)
        soup = BeautifulSoup(decode_html(res), "html.parser")
        races = []
        for li in soup.select("li.RaceList_DataItem"):
            a_tag = li.select_one("a[href*='race_id=']")
            if not a_tag:
                continue
            m = re.search(r"race_id=(\d{12})", a_tag.get("href", ""))
            if not m:
                continue
            rid = m.group(1)
            venue = VENUE_MAP.get(rid[4:6], "JRA")
            r_num = int(rid[10:12])
            t_el = li.select_one(".ItemTitle")
            name = t_el.get_text(strip=True) if t_el else f"{r_num}R"
            tm_el = li.select_one(".RaceList_Itemtime")
            ptime = tm_el.get_text(strip=True) if tm_el else "15:00"
            lg_el = li.select_one(".RaceList_ItemLong")
            sdist = lg_el.get_text(strip=True) if lg_el else "芝1600m"
            is_new = ("新馬" in name) or ("メイクデビュー" in name)
            races.append({
                "raceId": rid,
                "venue": venue,
                "raceNumber": r_num,
                "venueLabel": f"{venue}{r_num}R",
                "name": name,
                "surfaceDist": sdist,
                "postTime": ptime,
                "rank": "New" if is_new else ("A" if r_num >= 10 else "B"),
                "skill": "app-bayesian-make-debut" if is_new else "app-bayesian-horse-racing-text",
                "predicted": False
            })
        return races
    except Exception as e:
        print(f"[Warn] fetch_race_list failed: {e}")
        return []

def find_target_kaisai(now: datetime):
    for offset in [0, 1, 2, 3, 4, 5, -1, -2, -3, -4]:
        dt = now + timedelta(days=offset)
        races = fetch_race_list_by_date(dt.strftime("%Y%m%d"))
        if len(races) >= 6:
            return dt.strftime("%Y-%m-%d"), races
    return now.strftime("%Y-%m-%d"), []

def fetch_race_detail(race_id: str) -> str:
    lines = []
    try:
        url = f"https://race.netkeiba.com/race/shutuba_past.html?race_id={race_id}"
        soup = BeautifulSoup(decode_html(requests.get(url, headers=HEADERS, timeout=15)), "html.parser")
        for tr in soup.select("tr.HorseList")[:18]:
            u = tr.select_one("td[class^='Umaban']")
            n = tr.select_one(".Horse02 a, .HorseName a")
            j = tr.select_one(".Jockey a, td.Jockey")
            pasts = [" ".join(td.get_text(" ", strip=True).split())[:70] for td in tr.select("td.Past")[:2]]
            u_txt = u.get_text(strip=True) if u else ""
            n_txt = n.get_text(strip=True) if n else ""
            j_txt = " ".join(j.get_text(" ", strip=True).split()) if j else ""
            lines.append(f"{u_txt}番 {n_txt} ({j_txt}) | {' / '.join(pasts)}")
    except Exception as e:
        print(f"[Warn] detail fetch failed: {e}")
    return "\n".join(lines)

def call_gemini_json(skill_name: str, prompt_text: str) -> dict:
    if not client:
        return {}
    path = f"skills/{skill_name}/SKILL.md"
    sys_inst = open(path, "r", encoding="utf-8").read() if os.path.exists(path) else "Output valid JSON."
    for model_id in ["gemini-2.5-flash", "gemini-2.0-flash"]:
        try:
            time.sleep(4)
            res = client.models.generate_content(
                model=model_id,
                contents=prompt_text,
                config=types.GenerateContentConfig(
                    system_instruction=sys_inst,
                    response_mime_type="application/json",
                    temperature=0.1,
                ),
            )
            txt = (res.text or "").strip()
            if txt.startswith("```"):
                txt = re.sub(r"^```(?:json)?\s*|\s*```$", "", txt, flags=re.DOTALL)
            return json.loads(txt)
        except Exception as e:
            print(f"[Warn] {model_id} error: {e}")
    return {}

def run_pipeline():
    now = datetime.now(JST)
    date_str, scraped = find_target_kaisai(now)
    db_path = f"data/{date_str}.json"

    if os.path.exists(db_path):
        day_db = json.load(open(db_path, "r", encoding="utf-8"))
    else:
        day_db = {"date": date_str, "screened": False, "races": scraped}

    if not day_db.get("races") and scraped:
        day_db["races"] = scraped

    targets = [r for r in day_db.get("races", []) if not r.get("predicted") and r.get("raceNumber") in (11, 10, 5)][:2]
    for race in targets:
        detail = fetch_race_detail(race["raceId"])
        if not detail:
            continue
        prompt = f"【モード: 標準】日付:{date_str} {race['venueLabel']} {race['name']} ({race['surfaceDist']})\n{detail}"
        pred = call_gemini_json(race["skill"], prompt)
        if isinstance(pred, dict) and "horses" in pred:
            race["horses"] = pred["horses"]
            race["scenario"] = pred.get("scenario", "AI推論完了")
            race["rank"] = pred.get("rank", race["rank"])
            race["predicted"] = True

    day_db["updatedAt"] = now.strftime("%Y-%m-%d %H:%M JST")
    with open(db_path, "w", encoding="utf-8") as f:
        json.dump(day_db, f, ensure_ascii=False, indent=2)

    files = sorted([os.path.basename(p).replace(".json", "") for p in glob.glob("data/20*.json")])
    with open("data/index.json", "w", encoding="utf-8") as f:
        json.dump({"availableDates": files, "lastSync": day_db["updatedAt"]}, f, ensure_ascii=False, indent=2)
    print(f"Done: {db_path}")

if __name__ == "__main__":
    run_pipeline()
# === END OF FILE ===
