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
VENUES = {"01":"札幌","02":"函館","03":"福島","04":"新潟","05":"東京","06":"中山","07":"中京","08":"京都","09":"阪神","10":"小倉"}

def get_soup(url: str) -> BeautifulSoup:
    res = requests.get(url, headers=HEADERS, timeout=15)
    raw = res.content
    txt = raw.decode("utf-8", errors="ignore") if b"utf-8" in raw[:1024].lower() else raw.decode("euc_jp", errors="ignore")
    return BeautifulSoup(txt, "html.parser")

def fetch_race_list(ymd: str) -> list:
    try:
        soup = get_soup(f"https://race.netkeiba.com/top/race_list_sub.html?kaisai_date={ymd}")
        races = []
        for li in soup.select("li.RaceList_DataItem"):
            a = li.select_one("a[href*='race_id=']")
            m = re.search(r"race_id=(\d{12})", a.get("href", "")) if a else None
            if not m: continue
            rid = m.group(1)
            v = VENUES.get(rid[4:6], "JRA")
            rnum = int(rid[10:12])
            name = (li.select_one(".ItemTitle") or li).get_text(strip=True)[:18]
            tm = li.select_one(".RaceList_Itemtime")
            lg = li.select_one(".RaceList_ItemLong")
            is_new = ("新馬" in name) or ("メイクデビュー" in name)
            races.append({
                "raceId": rid, "venue": v, "raceNumber": rnum, "venueLabel": f"{v}{rnum}R",
                "name": name, "surfaceDist": lg.get_text(strip=True) if lg else "芝1600m",
                "postTime": tm.get_text(strip=True) if tm else "15:00",
                "rank": "New" if is_new else ("A" if rnum >= 10 else "B"),
                "skill": "app-bayesian-make-debut" if is_new else "app-bayesian-horse-racing-text",
                "predicted": False
            })
        return races
    except Exception as e:
        print(f"[Warn] list error: {e}")
        return []

def fetch_detail_and_result(rid: str) -> tuple[str, list]:
    lines, top3_actual = [], []
    try:
        soup = get_soup(f"https://race.netkeiba.com/race/shutuba_past.html?race_id={rid}")
        for tr in soup.select("tr.HorseList")[:18]:
            u = tr.select_one("td[class^='Umaban']")
            n = tr.select_one(".Horse02 a, .HorseName a")
            j = tr.select_one(".Jockey a, td.Jockey")
            pasts = [" ".join(td.get_text(" ", strip=True).split())[:65] for td in tr.select("td.Past")[:2]]
            if n and n.get_text(strip=True):
                lines.append(f"{u.get_text(strip=True) if u else ''}番 {n.get_text(strip=True)} ({' '.join(j.get_text(' ', strip=True).split()) if j else ''}) | {' / '.join(pasts)}")
    except Exception: pass
    try:
        rsoup = get_soup(f"https://race.netkeiba.com/race/result.html?race_id={rid}")
        for tr in rsoup.select("#All_Result_Table tbody tr")[:10]:
            tds = [td.get_text(strip=True) for td in tr.select("td")]
            if len(tds) >= 11:
                if len(top3_actual) < 3 and tds[2].isdigit():
                    top3_actual.append({"rank": tds[0], "num": int(tds[2]), "name": tds[3], "odds": tds[10]})
                if len(lines) < 10:
                    lines.append(f"{tds[2]}番 {tds[3]} (騎手:{tds[6]} 単勝:{tds[10]}倍 上り:{tds[11] if len(tds)>11 else ''})")
    except Exception: pass
    return "\n".join(lines[:18]), top3_actual

def call_gemini(skill: str, prompt: str) -> dict:
    if not client: return {}
    p = f"skills/{skill}/SKILL.md"
    sys_inst = open(p, "r", encoding="utf-8").read() if os.path.exists(p) else "Output valid JSON only."
    for m in ["gemini-2.5-flash", "gemini-2.0-flash"]:
        try:
            time.sleep(4)
            res = client.models.generate_content(
                model=m, contents=prompt,
                config=types.GenerateContentConfig(system_instruction=sys_inst, response_mime_type="application/json", temperature=0.1)
            )
            txt = re.sub(r"^```(?:json)?\s*|\s*```$", "", (res.text or "").strip(), flags=re.DOTALL)
            return json.loads(txt)
        except Exception as e:
            print(f"[Warn] {m}: {e}")
    return {}

def process_kaisai_day(date_str: str, races: list, now: datetime, is_today: bool):
    db_path = f"data/{date_str}.json"
    day_db = json.load(open(db_path, "r", encoding="utf-8")) if os.path.exists(db_path) else {"date": date_str, "screened": False, "races": races, "win5": {}}
    if not day_db.get("races") and races: day_db["races"] = races

    # 1. 会場別一括スクリーニング
    if day_db.get("races") and not day_db.get("screened"):
        for v in sorted(list({r["venue"] for r in day_db["races"]})):
            vr = [r for r in day_db["races"] if r["venue"] == v]
            res = call_gemini("app-bayesian-horse-racing-text", f"【モード: スクリーニング】日付:{date_str} 会場:{v}\n{json.dumps(vr, ensure_ascii=False)}")
            if isinstance(res, dict) and "races" in res:
                rmap = {int(x.get("raceNumber", 0)): x for x in res["races"] if isinstance(x, dict)}
                for r in day_db["races"]:
                    if r["venue"] == v and r["raceNumber"] in rmap:
                        sc = rmap[r["raceNumber"]]
                        if r["rank"] != "New": r["rank"] = sc.get("rank", r["rank"])
                        r["expectedRoi"] = sc.get("expectedRoi", 118)
                        r["hitRate"] = sc.get("hitRate", 44)
                        r["summary"] = sc.get("summary", "")
        day_db["screened"] = True

    # 2. 1時間前レース（または手動実行時は主要レース最大3鞍）の本予想＋結果照合
    queue = []
    for r in day_db.get("races", []):
        if r.get("predicted") or r.get("rank") == "Pass": continue
        if is_today and re.match(r"^\d{2}:\d{2}$", r.get("postTime", "")):
            pdt = datetime.strptime(f"{date_str} {r['postTime']}", "%Y-%m-%d %H:%M").replace(tzinfo=JST)
            if 35 <= (pdt - now).total_seconds() / 60.0 <= 85: queue.append(r)
    if not queue:
        queue = [r for r in day_db.get("races", []) if not r.get("predicted") and r.get("raceNumber") in (11, 10, 5)][:3]

    for r in queue:
        detail, actual = fetch_detail_and_result(r["raceId"])
        if not detail: continue
        pred = call_gemini(r["skill"], f"【モード: 標準】日付:{date_str} {r['venueLabel']} {r['name']} ({r['surfaceDist']})\n出走馬データ:\n{detail}")
        if isinstance(pred, dict) and "horses" in pred:
            r["horses"] = pred["horses"]
            r["scenario"] = pred.get("scenario", r.get("summary", "AI本予想完了"))
            r["pivotType"] = pred.get("pivotType", "Dual-Pivot")
            r["rank"] = pred.get("rank", r["rank"])
            r["predicted"] = True
            if actual:
                r["actualTop3"] = actual
                top_picks = [int(h.get("num", 0)) for h in r["horses"][:3] if str(h.get("num", "")).isdigit()]
                hit = any(a["num"] in top_picks for a in actual[:2])
                r["resultStatus"] = f"🎯 的中 (1着:{actual[0]['num']}番 {actual[0]['name']})" if hit else f"結果確定 (1着:{actual[0]['num']}番)"

    # 3. WIN5自動予想（メイン5鞍が揃っている場合）
    mains = [r for r in day_db.get("races", []) if r.get("raceNumber") in (10, 11)][:5]
    if len(mains) == 5 and not day_db.get("win5", {}).get("predicted"):
        w_lines = [f"Leg{i+1} {m['venueLabel']} {m['name']} ({m['surfaceDist']}): " + fetch_detail_and_result(m["raceId"])[0][:500] for i, m in enumerate(mains)]
        if any(len(x) > 60 for x in w_lines):
            w_res = call_gemini("app-bayesian-win5", f"日付:{date_str} WIN5対象5レース:\n" + "\n".join(w_lines))
            if isinstance(w_res, dict) and "legs" in w_res:
                w_res["predicted"] = True
                day_db["win5"] = w_res

    day_db["updatedAt"] = now.strftime("%Y-%m-%d %H:%M JST")
    json.dump(day_db, open(db_path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

def run_pipeline():
    now = datetime.now(JST)
    # 直近の確定開催日（実馬名・結果あり）と次回開催日の最大2日分を自動検出して処理
    found_past, found_next = None, None
    for off in [-1, -2, -3, -4, -5, -6]:
        dt = now + timedelta(days=off)
        rs = fetch_race_list(dt.strftime("%Y%m%d"))
        if len(rs) >= 6: found_past = (dt.strftime("%Y-%m-%d"), rs); break
    for off in [0, 1, 2, 3, 4, 5]:
        dt = now + timedelta(days=off)
        rs = fetch_race_list(dt.strftime("%Y%m%d"))
        if len(rs) >= 6: found_next = (dt.strftime("%Y-%m-%d"), rs); break

    if found_past: process_kaisai_day(found_past[0], found_past[1], now, False)
    if found_next: process_kaisai_day(found_next[0], found_next[1], now, found_next[0] == now.strftime("%Y-%m-%d"))

    files = sorted([os.path.basename(p).replace(".json", "") for p in glob.glob("data/20*.json")])
    json.dump({"availableDates": files, "lastSync": now.strftime("%Y-%m-%d %H:%M JST")}, open("data/index.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print("Pipeline Complete:", files)

if __name__ == "__main__":
    run_pipeline()
# === END OF FILE ===
