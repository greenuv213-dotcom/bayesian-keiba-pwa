import os, re, time, json, glob, requests
from datetime import datetime, timedelta, timezone
from bs4 import BeautifulSoup
from google import genai
from google.genai import types

JST = timezone(timedelta(hours=9))
API_KEY = os.environ.get("GEMINI_API_KEY", "").strip()
client = genai.Client(api_key=API_KEY) if API_KEY else None
os.makedirs("data", exist_ok=True)

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/124.0.0.0"}
JRA_VENUES = {"01":"札幌","02":"函館","03":"福島","04":"新潟","05":"東京","06":"中山","07":"中京","08":"京都","09":"阪神","10":"小倉"}
NAR_VENUES = {"42":"浦和","43":"船橋","44":"大井","45":"川崎","30":"門別","35":"盛岡","36":"水沢","46":"金沢","47":"笠松","48":"名古屋","50":"園田","51":"姫路","54":"高知","55":"佐賀"}
NANKAN_CODES = {"42", "43", "44", "45"}
MODELS = ["gemini-4-argon", "gemini-4-hydrogen", "gemini-3.8-flash", "gemini-2.5-flash"]

def get_soup(url: str) -> BeautifulSoup:
    res = requests.get(url, headers=HEADERS, timeout=15)
    raw = res.content
    txt = raw.decode("utf-8", errors="ignore") if b"utf-8" in raw[:1024].lower() else raw.decode("euc_jp", errors="ignore")
    return BeautifulSoup(txt, "html.parser")

def fetch_race_list(ymd: str, mode: str = "jra") -> list:
    base = "https://race.netkeiba.com" if mode == "jra" else "https://nar.netkeiba.com"
    vmap = JRA_VENUES if mode == "jra" else NAR_VENUES
    try:
        soup = get_soup(f"{base}/top/race_list_sub.html?kaisai_date={ymd}")
        races = []
        for li in soup.select("li.RaceList_DataItem"):
            a = li.select_one("a[href*='race_id=']")
            m = re.search(r"race_id=(\d{12})", a.get("href", "")) if a else None
            if not m: continue
            rid = m.group(1)
            vcode = rid[4:6]
            v = vmap.get(vcode, "地方" if mode == "nar" else "JRA")
            rnum = int(rid[10:12])
            name = (li.select_one(".ItemTitle") or li).get_text(strip=True)[:18]
            # 地方モードは南関4場またはダートグレード(Jpn/重賞)の後半レースを優先対象にする
            if mode == "nar" and (vcode not in NANKAN_CODES) and ("Jpn" not in name and rnum < 10):
                continue
            tm = li.select_one(".RaceList_Itemtime")
            lg = li.select_one(".RaceList_ItemLong")
            is_new = ("新馬" in name) or ("メイクデビュー" in name)
            skill = "app-bayesian-nar" if mode == "nar" else ("app-bayesian-make-debut" if is_new else "app-bayesian-horse-racing-text")
            races.append({
                "raceId": rid, "mode": mode, "venue": v, "raceNumber": rnum, "venueLabel": f"{v}{rnum}R",
                "name": name, "surfaceDist": lg.get_text(strip=True) if lg else "ダ1600m",
                "postTime": tm.get_text(strip=True) if tm else ("20:10" if mode == "nar" else "15:00"),
                "rank": "New" if is_new else ("S" if "Jpn" in name else ("A" if rnum >= 10 else "B")),
                "skill": skill, "predicted": False
            })
        return races
    except Exception as e:
        print(f"[Warn] {mode} list error: {e}")
        return []

def fetch_full_shutuba(rid: str, mode: str = "jra") -> tuple[str, list]:
    base = "https://race.netkeiba.com" if mode == "jra" else "https://nar.netkeiba.com"
    lines, top3_actual, odds_map = [], [], {}
    if mode == "jra":
        try:
            o_json = requests.get(f"{base}/api/api_get_jra_odds.html?race_id={rid}&type=1&action=init", headers=HEADERS, timeout=10).json()
            o_dict = (o_json.get("data") or {}).get("odds", {}).get("1", {})
            if isinstance(o_dict, dict):
                for k, val in o_dict.items():
                    if isinstance(val, list) and val: odds_map[int(k)] = val[0]
        except Exception: pass

    try:
        soup = get_soup(f"{base}/race/shutuba_past.html?race_id={rid}")
        r1, r2 = soup.select_one(".RaceData01"), soup.select_one(".RaceData02")
        if r1: lines.append("【条件・馬場】" + " ".join(r1.get_text(" ", strip=True).split()))
        if r2: lines.append("【コース詳細】" + " ".join(r2.get_text(" ", strip=True).split()))
        for tr in soup.select("tr.HorseList")[:18]:
            w = tr.select_one("td[class^='Waku']")
            u = tr.select_one("td[class^='Umaban']")
            n = tr.select_one(".Horse02 a, .HorseName a")
            j = tr.select_one(".Jockey a, td.Jockey")
            wt = tr.select_one("td.Weight")
            odd_el = tr.select_one("td.Popular span, span[id^='odds-']")
            pasts = [" ".join(td.get_text(" ", strip=True).split())[:90] for td in tr.select("td.Past")[:4]]
            if n and n.get_text(strip=True):
                u_str = u.get_text(strip=True) if u else "0"
                u_int = int(u_str) if u_str.isdigit() else 0
                odd = odds_map.get(u_int, odd_el.get_text(strip=True) if odd_el else "")
                lines.append(f"{w.get_text(strip=True) if w else ''}枠 {u_str}番 {n.get_text(strip=True)} ({' '.join(j.get_text(' ', strip=True).split()) if j else ''} 馬体重:{wt.get_text(strip=True) if wt else ''} 単勝:{odd}倍) | 近4走: {' / '.join(pasts)}")
    except Exception: pass

    try:
        rsoup = get_soup(f"{base}/race/result.html?race_id={rid}")
        for tr in rsoup.select("#All_Result_Table tbody tr")[:10]:
            tds = [td.get_text(strip=True) for td in tr.select("td")]
            if len(tds) >= 11:
                if len(top3_actual) < 3 and tds[2].isdigit():
                    top3_actual.append({"rank": tds[0], "num": int(tds[2]), "name": tds[3], "odds": tds[10]})
                if len(lines) < 6:
                    lines.append(f"{tds[1]}枠 {tds[2]}番 {tds[3]} (性齢:{tds[4]} 斤量:{tds[5]} 騎手:{tds[6]} 単勝:{tds[10]}倍 上り:{tds[11] if len(tds)>11 else ''})")
    except Exception: pass
    return "\n".join(lines[:20]), top3_actual

def call_gemini(skill: str, prompt: str) -> dict:
    if not client: return {}
    p = f"skills/{skill}/SKILL.md"
    sys_inst = open(p, "r", encoding="utf-8").read() if os.path.exists(p) else "Output valid JSON only."
    ticket_rule = (
        "\n【重要追加指示】標準モードのJSON出力時は、元のスキルのPhase 6（Single-Pivot / Dual-Pivot Triangle / 3連複F 3M+1点検算 / Core 55%・Alpha 45%配分）"
        "に完全準拠した買い目配列 `tickets` を必ず含めること。形式: "
        "\"tickets\": [{\"zone\":\"Core|Alpha\",\"type\":\"馬連|ワイド|単勝|3連複F|馬単\",\"comb\":\"組番表記\",\"points\":点数(整数),\"share\":配分比率(合計1.0),\"odds\":\"想定オッズ\",\"desc\":\"根拠(25字以内)\"}]"
    )
    for m in MODELS:
        try:
            time.sleep(4)
            res = client.models.generate_content(
                model=m, contents=prompt,
                config=types.GenerateContentConfig(system_instruction=sys_inst + ticket_rule, response_mime_type="application/json", temperature=0.1)
            )
            txt = re.sub(r"^```(?:json)?\s*|\s*```$", "", (res.text or "").strip(), flags=re.DOTALL)
            data = json.loads(txt)
            data["usedModel"] = m
            return data
        except Exception as e:
            print(f"[Fallback] {m}: {e}")
    return {}

def process_kaisai_day(date_str: str, races: list, now: datetime, is_today: bool, mode: str = "jra"):
    suffix = "_nar" if mode == "nar" else ""
    db_path = f"data/{date_str}{suffix}.json"
    day_db = json.load(open(db_path, "r", encoding="utf-8")) if os.path.exists(db_path) else {"date": date_str, "mode": mode, "screened": False, "races": races}
    if not day_db.get("races") and races: day_db["races"] = races
    day_db["mode"] = mode

    if day_db.get("races") and not day_db.get("screened"):
        sc_skill = "app-bayesian-nar" if mode == "nar" else "app-bayesian-horse-racing-text"
        for v in sorted(list({r["venue"] for r in day_db["races"]})):
            vr = [r for r in day_db["races"] if r["venue"] == v]
            res = call_gemini(sc_skill, f"【モード: スクリーニング】日付:{date_str} 会場:{v}\n{json.dumps(vr, ensure_ascii=False)}")
            if isinstance(res, dict) and "races" in res:
                rmap = {int(x.get("raceNumber", 0)): x for x in res["races"] if isinstance(x, dict)}
                for r in day_db["races"]:
                    if r["venue"] == v and r["raceNumber"] in rmap:
                        sc = rmap[r["raceNumber"]]
                        if r["rank"] != "New": r["rank"] = sc.get("rank", r["rank"])
                        r["expectedRoi"] = sc.get("expectedRoi", 120)
                        r["hitRate"] = sc.get("hitRate", 45)
                        r["summary"] = sc.get("summary", "")
        day_db["screened"] = True

    queue = []
    for r in day_db.get("races", []):
        if (r.get("predicted") and r.get("tickets")) or r.get("rank") == "Pass": continue
        if is_today and re.match(r"^\d{2}:\d{2}$", r.get("postTime", "")):
            pdt = datetime.strptime(f"{date_str} {r['postTime']}", "%Y-%m-%d %H:%M").replace(tzinfo=JST)
            if 30 <= (pdt - now).total_seconds() / 60.0 <= 90: queue.append(r)
    if not queue:
        queue = [r for r in day_db.get("races", []) if not r.get("tickets") and r.get("raceNumber") in (12, 11, 10, 5)][:3]

    for r in queue:
        detail, actual = fetch_full_shutuba(r["raceId"], mode=mode)
        if not detail: continue
        pred = call_gemini(r["skill"], f"【モード: 標準】日付:{date_str} {r['venueLabel']} {r['name']} ({r['surfaceDist']})\n詳細出馬表・馬柱:\n{detail}")
        if isinstance(pred, dict) and "horses" in pred:
            r.update({k: pred[k] for k in ("horses","tickets","scenario","pivotType","rank","nLead","usedModel") if k in pred})
            r["predicted"] = True
            if actual:
                r["actualTop3"] = actual
                top_picks = [int(h.get("num", 0)) for h in r["horses"][:3] if str(h.get("num", "")).isdigit()]
                hit = any(a["num"] in top_picks for a in actual[:2])
                r["resultStatus"] = f"🎯 的中 (1着:{actual[0]['num']}番 {actual[0]['name']})" if hit else f"結果確定 (1着:{actual[0]['num']}番)"

    day_db["updatedAt"] = now.strftime("%Y-%m-%d %H:%M JST")
    json.dump(day_db, open(db_path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

def run_pipeline():
    now = datetime.now(JST)
    is_weekend_jra_hours = (now.weekday() in (5, 6)) and (8 <= now.hour < 17)

    # 1. JRAパイプライン（土日または手動実行時の直近・次回JRA開催）
    for off in [-1, -2, -3, -4, -5]:
        dt = now + timedelta(days=off)
        rs = fetch_race_list(dt.strftime("%Y%m%d"), "jra")
        if len(rs) >= 6: process_kaisai_day(dt.strftime("%Y-%m-%d"), rs, now, False, "jra"); break
    for off in [0, 1, 2, 3, 4, 5]:
        dt = now + timedelta(days=off)
        rs = fetch_race_list(dt.strftime("%Y%m%d"), "jra")
        if len(rs) >= 6: process_kaisai_day(dt.strftime("%Y-%m-%d"), rs, now, off == 0, "jra"); break

    # 2. NAR地方パイプライン（土日昼のJRA開催時間帯はJRA保護のため自動スキップ）
    if not is_weekend_jra_hours:
        for off in [0, -1, 1, -2]:
            dt = now + timedelta(days=off)
            n_races = fetch_race_list(dt.strftime("%Y%m%d"), "nar")
            if len(n_races) >= 3:
                process_kaisai_day(dt.strftime("%Y-%m-%d"), n_races, now, off == 0, "nar")
                break

    jra_files = sorted([os.path.basename(p).replace(".json", "") for p in glob.glob("data/20*.json") if not p.endswith("_nar.json")])
    nar_files = sorted([os.path.basename(p).replace(".json", "") for p in glob.glob("data/20*_nar.json")])
    json.dump({"availableDates": jra_files, "narDates": nar_files, "lastSync": now.strftime("%Y-%m-%d %H:%M JST")}, open("data/index.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)

if __name__ == "__main__":
    run_pipeline()
# === END OF FILE ===
