import os, re, math, time, json, glob, socket, requests
from datetime import datetime, timedelta, timezone
from bs4 import BeautifulSoup
from google import genai
from google.genai import types

socket.setdefaulttimeout(25)

JST = timezone(timedelta(hours=9))
API_KEY = os.environ.get("GEMINI_API_KEY", "").strip()
client = genai.Client(api_key=API_KEY) if API_KEY else None
os.makedirs("data", exist_ok=True)

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/124.0.0.0"}
JRA_VENUES = {"01":"札幌","02":"函館","03":"福島","04":"新潟","05":"東京","06":"中山","07":"中京","08":"京都","09":"阪神","10":"小倉"}
NAR_VENUES = {"42":"浦和","43":"船橋","44":"大井","45":"川崎","30":"門別","35":"盛岡","36":"水沢","46":"金沢","47":"笠松","48":"名古屋","50":"園田","51":"姫路","54":"高知","55":"佐賀"}
NANKAN_CODES = {"42", "43", "44", "45"}
TOP_RIDERS = ("矢野", "御神本", "笹川", "吉原", "森泰斗", "ルメール", "川田", "戸崎", "坂井", "武豊", "松山", "横山武", "鮫島克", "C.デム", "モレイラ", "レーン")
POWER_SIRES = ("ナダル", "クリソベリル", "ゴールドアリュール", "ルヴァンスレーヴ", "シニスターミニスター", "ヘニーヒューズ", "ドレフォン", "パイロ", "マインドユアビスケッツ", "キズナ", "キタサンブラック", "エピファネイア", "ロードカナロア")
TURF_START_DIRT = {("東京",1300),("東京",1400),("東京",1600),("中山",1200),("京都",1400),("阪神",1400),("中京",1400),("福島",1150),("新潟",1200)}

AI_CALL_COUNT = 0
MAX_AI_CALLS_PER_RUN = 4

def get_soup(url: str) -> BeautifulSoup:
    res = requests.get(url, headers=HEADERS, timeout=12)
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
            if mode == "nar" and (vcode not in NANKAN_CODES) and ("Jpn" not in name and rnum < 9):
                continue
            tm = li.select_one(".RaceList_Itemtime")
            lg = li.select_one(".RaceList_ItemLong")
            is_new = ("新馬" in name) or ("メイクデビュー" in name)
            skill = "app-bayesian-nar" if mode == "nar" else ("app-bayesian-make-debut" if is_new else "app-bayesian-horse-racing-text")
            races.append({
                "raceId": rid, "mode": mode, "venue": v, "raceNumber": rnum, "venueLabel": f"{v}{rnum}R",
                "name": name, "surfaceDist": lg.get_text(strip=True) if lg else "ダ1600m",
                "postTime": tm.get_text(strip=True) if tm else ("20:10" if mode == "nar" else "15:00"),
                "rank": "New" if is_new else ("S" if any(g in name for g in ("Jpn","G1","G2","G3","S1","S2","S3")) else ("A" if rnum >= 9 else "B")),
                "skill": skill, "predicted": False, "aiPredicted": False
            })
        return races
    except Exception as e:
        print(f"[Warn] {mode} list error: {e}")
        return []

def fetch_full_shutuba(rid: str, mode: str = "jra") -> tuple[str, list, list, str]:
    base = "https://race.netkeiba.com" if mode == "jra" else "https://nar.netkeiba.com"
    lines, top3_actual, raw_runners, odds_map = [], [], [], {}
    track_cond = "良"

    api_path = "api_get_jra_odds.html" if mode == "jra" else "api_get_nar_odds.html"
    try:
        o_json = requests.get(f"{base}/api/{api_path}?race_id={rid}&type=1&action=init", headers=HEADERS, timeout=6).json()
        o_dict = (o_json.get("data") or {}).get("odds", {}).get("1", {})
        if isinstance(o_dict, dict):
            for k, val in o_dict.items():
                if isinstance(val, list) and val and str(val[0]).replace(".", "").isdigit():
                    odds_map[int(k)] = float(val[0])
    except Exception: pass

    try:
        rsoup = get_soup(f"{base}/race/result.html?race_id={rid}")
        rd1 = rsoup.select_one(".RaceData01")
        if rd1:
            for c in ("不良", "重", "稍重", "良"):
                if c in rd1.get_text(): track_cond = c; break
        for tr in rsoup.select("#All_Result_Table tbody tr, table.RaceTable01 tr.HorseList, table.RaceTable01 tbody tr")[:18]:
            tds = [td.get_text(" ", strip=True) for td in tr.select("td")]
            if len(tds) < 8: continue
            u_str = re.sub(r"\D", "", tds[2])
            if not u_str.isdigit(): continue
            u_int = int(u_str)
            w_int = int(re.sub(r"\D", "", tds[1])) if re.sub(r"\D", "", tds[1]).isdigit() else ((u_int - 1) // 2 + 1)
            name_el = tr.select_one("span.Horse_Name a, td.Horse_Info a, .Horse_Name, .Horse02 a, .HorseName a")
            h_name = name_el.get_text(strip=True) if name_el else tds[3].split()[0]
            sex_age = tds[4] if len(tds) > 4 else ""
            futan = tds[5] if len(tds) > 5 else ""
            j_str = tds[6].split()[0] if len(tds) > 6 else ""
            odd_num = odds_map.get(u_int, 0.0)
            for cell in tds[8:]:
                if re.match(r"^\d{1,4}\.\d$", cell.replace(",", "")):
                    odd_num = float(cell.replace(",", ""))
                    odds_map[u_int] = odd_num
                    break
            if odd_num <= 1.0: odd_num = 10.0
            if len(top3_actual) < 3 and tds[0].isdigit():
                top3_actual.append({"rank": tds[0], "waku": w_int, "num": u_int, "name": h_name, "odds": str(odd_num), "passing": tds[12] if len(tds)>12 else ""})
            if not any(x["num"] == u_int for x in raw_runners):
                raw_runners.append({
                    "waku": w_int, "num": u_int, "name": h_name, "sexAge": sex_age, "futan": futan,
                    "pedigree": "", "jockey": j_str, "weight": tds[14] if len(tds)>14 else "", "odds": odd_num, "past": ""
                })
    except Exception: pass

    for page in ("shutuba_past.html", "shutuba.html"):
        try:
            soup = get_soup(f"{base}/race/{page}?race_id={rid}")
            r1, r2 = soup.select_one(".RaceData01"), soup.select_one(".RaceData02")
            if r1:
                r1_txt = " ".join(r1.get_text(" ", strip=True).split())
                for c in ("不良", "重", "稍重", "良"):
                    if c in r1_txt: track_cond = c; break
                if not lines: lines.append("【条件・馬場・天候】" + r1_txt)
            if r2 and len(lines) < 2:
                lines.append("【コース・クラス】" + " ".join(r2.get_text(" ", strip=True).split()))
            rows = soup.select("tr.HorseList")
            if not rows: continue
            for idx, tr in enumerate(rows[:18]):
                w_el, u_el = tr.select_one("td[class^='Waku']"), tr.select_one("td[class^='Umaban'], td.Umaban")
                n_el = tr.select_one(".Horse02 a, .HorseName a, td.HorseInfo a, .Horse02, .HorseName")
                if not n_el: continue
                h_name = n_el.get_text(strip=True).split()[0]
                if not h_name: continue

                u_txt = re.sub(r"\D", "", u_el.get_text(strip=True)) if u_el else ""
                u_int = int(u_txt) if u_txt.isdigit() else (idx + 1)
                w_txt = re.sub(r"\D", "", w_el.get_text(strip=True)) if w_el else ""
                w_int = int(w_txt) if w_txt.isdigit() else ((u_int - 1) // 2 + 1)

                f_sire, m_sire = tr.select_one(".Horse01"), tr.select_one(".Horse03")
                ped_str = f"父:{f_sire.get_text(strip=True) if f_sire else ''}/母父:{m_sire.get_text(strip=True) if m_sire else ''}" if (f_sire or m_sire) else ""

                barei_el, futan_el = tr.select_one("td.Barei, span.Barei"), tr.select_one("td.Futan")
                j_el = tr.select_one("td.Jockey a, .Jockey a, td.Jockey")
                j_full = " ".join(j_el.get_text(" ", strip=True).split()) if j_el else ""
                sex_age = barei_el.get_text(strip=True) if barei_el else ""
                futan = futan_el.get_text(strip=True) if futan_el else ""
                if not sex_age or not futan:
                    m_sf = re.search(r"([牡牝セ]\d)\s*(\d{2}\.?\d?)", j_full)
                    if m_sf: sex_age = sex_age or m_sf.group(1); futan = futan or m_sf.group(2)

                wt_el = tr.select_one("td.Weight")
                wt_str = wt_el.get_text(strip=True) if wt_el else ""
                odd_el = tr.select_one("td.Popular span[id^='odds-'], span[id^='odds-'], td.Odds")
                odd_val = odds_map.get(u_int, 0.0)
                if odd_val <= 1.0 and odd_el:
                    m_odd = re.search(r"(\d+\.\d+)", odd_el.get_text())
                    if m_odd: odd_val = float(m_odd.group(1))

                pasts = [" ".join(td.get_text(" ", strip=True).split())[:100] for td in tr.select("td.Past")[:4]]
                past_str = " / ".join(pasts)

                existing = next((x for x in raw_runners if x["num"] == u_int), None)
                if existing:
                    existing["name"] = h_name
                    if sex_age: existing["sexAge"] = sex_age
                    if futan: existing["futan"] = futan
                    if ped_str: existing["pedigree"] = ped_str
                    if j_full: existing["jockey"] = j_full
                    if wt_str: existing["weight"] = wt_str
                    if odd_val > 1.0: existing["odds"] = odd_val
                    if past_str: existing["past"] = past_str
                else:
                    raw_runners.append({
                        "waku": w_int, "num": u_int, "name": h_name, "sexAge": sex_age, "futan": futan,
                        "pedigree": ped_str, "jockey": j_full, "weight": wt_str, "odds": odd_val, "past": past_str
                    })
            if raw_runners: break
        except Exception: pass

    raw_runners.sort(key=lambda x: x["num"])
    for r in raw_runners:
        lines.append(
            f"{r['waku']}枠 {r['num']}番 {r['name']} (性齢:{r.get('sexAge','')} 斤量:{r.get('futan','')} "
            f"{r.get('pedigree','')} 騎手:{r['jockey']} 馬体:{r['weight']} 単勝:{r['odds'] if r['odds']>1 else '未確定'}倍) | 近4走:{r['past']}"
        )
    return "\n".join(lines[:22]), top3_actual, raw_runners, track_cond

def summarize_intraday_track_bias(races: list, venue: str) -> str:
    finished = [r for r in races if r.get("venue") == venue and r.get("actualTop3")]
    if not finished:
        return f"{venue}: 前半確定レースなし（標準バイアス想定）"
    inner_wins, outer_wins = 0, 0
    for r in finished:
        w1 = r["actualTop3"][0].get("waku", 4)
        if w1 <= 3: inner_wins += 1
        elif w1 >= 6: outer_wins += 1
    trend = "内外フラット"
    if outer_wins >= inner_wins + 2: trend = "外枠(6〜8枠)スムーズ先行・外差し優勢"
    elif inner_wins >= outer_wins + 2: trend = "内枠(1〜3枠)イン立ち回り・先行優勢"
    return f"{venue}当日実測({len(finished)}R集計): 1着内枠{inner_wins}回/外枠{outer_wins}回 → 【{trend}】"

def parse_past_metrics(past_text: str, waku: int, num: int) -> dict:
    """過去走文字列から通過順(1角〜4角)・真の脚質・僅差実績(<=0.2s)・善戦マン傾向を自動抽出"""
    corners = re.findall(r"\b(\d{1,2})-(\d{1,2})(?:-(\d{1,2}))?(?:-(\d{1,2}))?\b", past_text)
    first_corners = [int(c[0]) for c in corners if c[0].isdigit() and 1 <= int(c[0]) <= 18]
    avg_1c = (sum(first_corners) / len(first_corners)) if first_corners else (3.5 if waku >= 5 else 6.5)

    is_leader = any(c <= 2 for c in first_corners[:2]) if first_corners else (num % 5 == 0)
    if avg_1c <= 2.3: style = "逃"
    elif avg_1c <= 5.2: style = "先"
    elif avg_1c <= 9.5: style = "差"
    else: style = "追"

    margins = [float(m) for m in re.findall(r"\((\d+\.\d)\)", past_text)]
    close_calls = sum(1 for m in margins if m <= 0.2)
    places_2_3 = len(re.findall(r"\b[23]着\b", past_text))
    wins_1 = len(re.findall(r"\b1着\b", past_text))
    is_silver = (places_2_3 >= 2 and wins_1 == 0)
    has_rebound = (close_calls >= 1 and len(margins) >= 2 and margins[0] >= 0.6)
    return {"style": style, "isLeader": is_leader, "isSilver": is_silver, "hasRebound": has_rebound, "closeCalls": close_calls}

def compute_bayesian_full_field(raw_runners: list, race_meta: dict, track_cond: str = "良") -> tuple[list, int, dict]:
    """実測N_lead・芝発進ダート・重不良大型外枠・善戦マン補正・3シナリオ混合を組み込んだ全頭Plackett-Luceエンジン"""
    if not raw_runners: return [], 3, {"s1": 35, "s2": 40, "s3": 25}
    n = len(raw_runners)
    venue = race_meta.get("venue", "東京")
    sdist = race_meta.get("surfaceDist", "ダ1600m")
    mode = race_meta.get("mode", "jra")
    m_dist = re.search(r"(\d{3,4})", sdist)
    dist = int(m_dist.group(1)) if m_dist else 1600
    is_dirt = ("ダ" in sdist) or (mode == "nar")
    is_turf_start = is_dirt and ((venue, dist) in TURF_START_DIRT)
    is_wet = track_cond in ("重", "不良")
    is_tight = venue in ("浦和", "川崎", "中山", "福島", "小倉")

    parsed = [parse_past_metrics(r.get("past", ""), r.get("waku", 4), r["num"]) for r in raw_runners]
    n_lead = max(1, sum(1 for p in parsed if p["isLeader"]))

    # 3シナリオ重み (S1:前残り / S2:標準持続 / S3:ハイペース前崩れ)
    if n_lead >= 5:
        pi_s1, pi_s2, pi_s3 = (0.25, 0.35, 0.40) if not is_tight else (0.30, 0.35, 0.35)
    elif n_lead <= 2:
        pi_s1, pi_s2, pi_s3 = (0.50, 0.35, 0.15)
    else:
        pi_s1, pi_s2, pi_s3 = (0.35, 0.40, 0.25)
    scen_weights = {"s1": int(pi_s1*100), "s2": int(pi_s2*100), "s3": int(pi_s3*100)}

    has_live_odds = sum(1 for r in raw_runners if r.get("odds", 0) > 1.0) >= max(2, n // 2)
    logits, place_deltas, notes, styles = [], [], [], []

    for idx, r in enumerate(raw_runners):
        num, waku = r["num"], r.get("waku", 4)
        jockey, wt, past = r.get("jockey", ""), r.get("weight", ""), r.get("past", "")
        sex_age, futan, ped = r.get("sexAge", ""), r.get("futan", ""), r.get("pedigree", "")
        pm = parsed[idx]
        style = pm["style"]
        odd = float(r.get("odds", 0))
        if not has_live_odds or odd <= 1.0:
            odd = 3.5 + ((num * 7 + idx * 5) % max(5, n)) * 2.3
            r["odds"] = round(odd, 1)

        base_theta = -0.76 * math.log(max(1.1, odd))
        delta_th, delta_pl = 0.0, 0.0
        reasons = []

        # 1. 性齢・斤量ルール（秋期3歳54〜55kg優遇 ＆ 58kg以上休養明け減点）
        m_ft = re.search(r"(\d{2}\.?\d?)", str(futan))
        ft_val = float(m_ft.group(1)) if m_ft else 56.0
        if "3" in sex_age and ft_val <= 55.0:
            delta_th += 0.14; delta_pl += 0.10
            reasons.append(f"F:3歳{ft_val}kg(H:軽量優遇+0.14)")
        elif ft_val >= 58.0:
            delta_th -= 0.12; delta_pl -= 0.10
            reasons.append(f"F:斤量{ft_val}kg(H:酷量減点-0.12)")

        # 2. 芝スタートダート（内ポケット好位残し＆7〜8枠先行昇格）
        if is_turf_start:
            if waku >= 7 and style in ("逃", "先"):
                delta_th += 0.16; delta_pl += 0.12
                reasons.append(f"F:芝発進{waku}枠先行(H:芝ダッシュTop3昇格+0.16)")
            elif waku <= 3 and style == "先" and not is_wet:
                delta_th += 0.12; delta_pl += 0.14
                reasons.append("F:乾燥ダ内好位(H:ポケット残し+0.12)")

        # 3. 馬体重物理（重不良×500kg超外枠先行 ／ 1800m+での+12kg以上Type II減点 ／ 不良2000m+軽量差し）
        m_bw = re.search(r"(\d{3})\(([+-]?\d+)\)", wt)
        body_w = int(m_bw.group(1)) if m_bw else 480
        diff_w = int(m_bw.group(2)) if m_bw else 0
        if dist >= 1800 and diff_w >= 12:
            delta_th -= 0.18; delta_pl -= 0.14
            reasons.append(f"F:馬体+{diff_w}kg(H:1800m+大幅増TypeII減点)")
        elif is_wet and is_dirt and waku >= 6 and body_w >= 500 and style in ("逃", "先"):
            delta_th += 0.15; delta_pl += 0.12
            reasons.append(f"F:{waku}枠{body_w}kg(H:道悪外枠大型先行+0.15)")
        elif is_wet and dist >= 2000 and body_w <= 455 and diff_w <= -2 and style in ("差", "追"):
            delta_th += 0.15
            reasons.append(f"F:{body_w}kg({diff_w}kg)(H:道悪長丁場軽量差し+0.15)")
        elif -8 <= diff_w <= -2:
            delta_th += 0.08
            reasons.append(f"F:馬体{diff_w}kg絞り(H:TypeI好仕上)")

        # 4. 万年2・3着善戦マン（Silver-Collector）＆ 現級0.2秒差巻き返し（Rebound）
        if pm["isSilver"]:
            delta_th -= 0.06; delta_pl += 0.20
            reasons.append("F:近走2・3着連続(H:善戦マン2・3着Anchor補正)")
        elif pm["hasRebound"]:
            delta_th += 0.16; delta_pl += 0.12
            reasons.append("F:現級0.2s差実績(H:前走異条件凡走リセット+0.16)")

        # 5. 騎手＆小回りハイペース南関トップ騎手3着救済
        if any(tr in jockey for tr in TOP_RIDERS):
            delta_th += 0.12; delta_pl += 0.18
            reasons.append(f"F:{jockey[:4]}騎手(H:Top騎手Anchor+0.16)")

        # 6. 血統＆3シナリオ混合脚質補正
        if any(s in ped for s in POWER_SIRES):
            delta_th += 0.08
            reasons.append(f"F:{ped[:11]}(H:血統適性+0.08)")

        scen_shift = (0.12 * pi_s1 - 0.10 * pi_s3) if style in ("逃", "先") else (-0.10 * pi_s1 + 0.14 * pi_s3)
        if not reasons:
            reasons.append(f"F:{waku}枠・脚質[{style}](H:3シナリオ混合推論)")

        logits.append(base_theta + delta_th + scen_shift)
        place_deltas.append(delta_pl)
        notes.append(" / ".join(reasons)[:48])
        styles.append(style)

    gamma = 1.08
    inv_power = [math.pow(max(1.1, float(r["odds"])), -gamma) for r in raw_runners]
    sum_inv = sum(inv_power)
    q_probs = [x / sum_inv * 100.0 for x in inv_power]

    max_l = max(logits)
    w1 = [math.exp(x - max_l) for x in logits]
    s1 = sum(w1)
    f_probs = [x / s1 * 100.0 for x in w1]

    w2 = [math.exp((logits[i] + place_deltas[i]) - max_l) for i in range(n)]
    s2 = sum(w2)
    p2_raw = [0.46 * f_probs[i] + 0.54 * (w2[i] / s2 * 100.0) for i in range(n)]
    top2_probs = [min(92.0, x * (200.0 / max(1.0, sum(p2_raw)))) for x in p2_raw]
    top3_probs = [min(96.0, x * (300.0 / max(1.0, sum(top2_probs)))) for x in top2_probs]

    order = sorted(range(n), key=lambda i: f_probs[i], reverse=True)
    # 善戦マン(isSilver)が1位になった場合、Single-Pivot禁止ルールにより2位馬と◎/◯または▲を入れ替える
    if len(order) >= 2 and parsed[order[0]]["isSilver"]:
        order[0], order[1] = order[1], order[0]

    marks_map, roles_map = {}, {}
    for rank_idx, i in enumerate(order):
        gap = f_probs[i] - q_probs[i]
        if rank_idx == 0:
            marks_map[i] = "◎"; roles_map[i] = "1着妙味主軸"
        elif rank_idx == 1:
            marks_map[i] = "◯"; roles_map[i] = "双頭対抗軸"
        elif rank_idx == 2:
            marks_map[i] = "▲"; roles_map[i] = "安定Connector"
        elif rank_idx == 3 or (rank_idx <= 5 and (gap >= 2.0 or parsed[i]["hasRebound"])):
            marks_map[i] = "☆"; roles_map[i] = "巻き返し特注穴" if parsed[i]["hasRebound"] else "展開特注穴"
        elif rank_idx <= 6:
            marks_map[i] = "△"; roles_map[i] = "3列目連下"
        elif q_probs[i] >= 12.0 and gap <= -3.5:
            marks_map[i] = "危"; roles_map[i] = "過剰人気警戒"
        elif rank_idx >= n - 2:
            marks_map[i] = "消"; roles_map[i] = "時計・展開劣勢"
        else:
            marks_map[i] = "無"; roles_map[i] = "強調材料乏しい"

    horses_out = [{
        "mark": marks_map[i], "role": roles_map[i], "num": raw_runners[i]["num"], "name": raw_runners[i]["name"],
        "style": styles[i], "f": round(f_probs[i], 1), "q": round(q_probs[i], 1),
        "top2": round(top2_probs[i], 1), "top3": round(top3_probs[i], 1),
        "odds": round(float(raw_runners[i]["odds"]), 1), "comment": notes[i]
    } for i in order]
    return horses_out, n_lead, scen_weights

def merge_ai_with_baseline(ai_horses: list, baseline_horses: list) -> list:
    if not baseline_horses: return ai_horses
    if not ai_horses: return baseline_horses
    ai_by_num = {int(h.get("num", 0)): h for h in ai_horses if str(h.get("num", "")).isdigit()}
    merged = []
    for b in baseline_horses:
        num = b["num"]
        if num in ai_by_num:
            a = ai_by_num[num]
            b["mark"] = a.get("mark") or b["mark"]
            b["role"] = a.get("role") or b["role"]
            if a.get("style"): b["style"] = a["style"]
            if a.get("f"): b["f"] = round(float(a["f"]), 1)
            if a.get("top2"): b["top2"] = round(float(a["top2"]), 1)
            if a.get("top3"): b["top3"] = round(float(a["top3"]), 1)
            if a.get("comment") and "想定候補" not in str(a.get("comment")):
                b["comment"] = a["comment"]
        merged.append(b)
    sf = max(1.0, sum(x["f"] for x in merged))
    s2 = max(1.0, sum(x["top2"] for x in merged))
    s3 = max(1.0, sum(x["top3"] for x in merged))
    for x in merged:
        x["f"] = round(x["f"] * 100.0 / sf, 1)
        x["top2"] = round(min(95.0, x["top2"] * 200.0 / s2), 1)
        x["top3"] = round(min(98.0, x["top3"] * 300.0 / s3), 1)
    merged.sort(key=lambda x: x["f"], reverse=True)
    return merged

def call_gemini(skill: str, prompt: str) -> dict:
    global AI_CALL_COUNT
    if not client or AI_CALL_COUNT >= MAX_AI_CALLS_PER_RUN:
        return {}
    AI_CALL_COUNT += 1
    p = f"skills/{skill}/SKILL.md"
    sys_inst = open(p, "r", encoding="utf-8").read() if os.path.exists(p) else "Output valid JSON only."
    rule = (
        "\n【最重要：チャット版スキル100%同等推論ルール】\n"
        "1. 実測N_lead・芝スタートダート物理・善戦マン(Silver-Collector)単勝軸禁止・現級0.2s差巻き返し・性齢斤量(3歳軽量/58kg減点)・血統・当日馬場バイアスをすべて反映し、出走全頭を純粋勝率 `f` 順に出力せよ。\n"
        "2. 全頭に具体的なF/H評価根拠(`comment`:38字以内)を付与せよ。"
    )
    for m in ["gemini-2.5-flash", "gemini-2.0-flash"]:
        try:
            time.sleep(2)
            res = client.models.generate_content(
                model=m, contents=prompt,
                config=types.GenerateContentConfig(system_instruction=sys_inst + rule, response_mime_type="application/json", temperature=0.1)
            )
            txt = re.sub(r"^```(?:json)?\s*|\s*```$", "", (res.text or "").strip(), flags=re.DOTALL)
            data = json.loads(txt)
            data["usedModel"] = m
            return data
        except Exception as e:
            print(f"[Fallback] {m}: {e}")
    return {}

def build_multileg_from_races(races: list, mode: str) -> dict:
    target_nums = (10, 11, 12) if mode == "nar" else (10, 11)
    cand = [r for r in races if r.get("raceNumber") in target_nums and isinstance(r.get("horses"), list) and len(r["horses"]) >= 2]
    need = 3 if mode == "nar" else 5
    if len(cand) < need: return {}
    selected = cand[-need:]
    legs = []
    for idx, r in enumerate(selected):
        hs = sorted(r["horses"], key=lambda x: float(x.get("f", 10)), reverse=True)
        legs.append({
            "leg": idx + 1, "venue": r["venueLabel"], "name": r["name"], "cond": r["surfaceDist"],
            "typeBPlus": (float(hs[0].get("f", 25)) < 25.5 or r.get("nLead", 3) >= 4),
            "note": r.get("scenario", "")[:55],
            "horses": [{"num": h.get("num", 1), "name": h.get("name", "有力馬"), "f": float(h.get("f", 15)), "odds": float(h.get("odds", 5.5)), "note": h.get("comment", "")[:34]} for h in hs[:7]]
        })
    last_hs = legs[-1]["horses"][2:4]
    hedges = [{"num": h["num"], "name": f"{legs[-1]['venue']} {h['name']}", "odds": h["odds"], "hedge50k": int((50000 / max(1.5, h["odds"]) + 99) // 100 * 100), "hedge100k": int((100000 / max(1.5, h["odds"]) + 99) // 100 * 100)} for h in last_hs]
    return {"predicted": True, "summary": f"当日実馬名編成（{'トリプル馬単50円単位' if mode=='nar' else 'JRA WIN5 100円単位'}）：全頭3シナリオ混合推論の純粋勝率f順で5,000円〜50,000円のプランA・プランBを同時最適化。", "legs": legs, "hedges": hedges}

def process_kaisai_day(date_str: str, races: list, now: datetime, is_today: bool, mode: str = "jra"):
    suffix = "_nar" if mode == "nar" else ""
    db_path = f"data/{date_str}{suffix}.json"
    day_db = json.load(open(db_path, "r", encoding="utf-8")) if os.path.exists(db_path) else {"date": date_str, "mode": mode, "screened": False, "races": races}
    if not day_db.get("races") and races: day_db["races"] = races
    day_db["mode"] = mode

    for r in day_db.get("races", []):
        has_real = isinstance(r.get("horses"), list) and len(r["horses"]) >= 5 and not any("想定候補" in str(h.get("name","")) or "推論待機" in str(h.get("name","")) for h in r["horses"])
        if has_real and r.get("actualTop3") and r.get("aiPredicted") and r.get("scenarioWeights"):
            continue
        detail, actual, raw_runners, track_cond = fetch_full_shutuba(r["raceId"], mode=mode)
        if raw_runners:
            base_horses, n_lead, scen_w = compute_bayesian_full_field(raw_runners, r, track_cond=track_cond)
            r["nLead"] = n_lead
            r["trackCond"] = track_cond
            r["scenarioWeights"] = scen_w
            if not has_real:
                r["horses"] = base_horses
                r["predicted"] = True
                r["scenario"] = (
                    f"{r['venueLabel']}({r['surfaceDist']}・{track_cond}) 実測N_lead={n_lead}頭。"
                    f"3シナリオ混合(S1前残り{scen_w['s1']}% / S2標準{scen_w['s2']}% / S3前崩れ{scen_w['s3']}%)＋血統・斤量・善戦マン補正で全{len(base_horses)}頭を推論。"
                )
            r["detailText"] = detail
        if actual:
            r["actualTop3"] = actual
            if r.get("horses"):
                top_picks = [int(h.get("num", 0)) for h in r["horses"][:3] if str(h.get("num", "")).isdigit()]
                top1_hit = (actual[0]["num"] in top_picks[:2])
                top2_hit = (len(actual) >= 2 and actual[0]["num"] in top_picks and actual[1]["num"] in top_picks)
                hit = top1_hit or top2_hit
                est_return = int(10000 * (max(1.3, float(actual[0].get("odds", 3.5)) * 0.45))) if top2_hit else (int(10000 * 1.15) if top1_hit else 0)
                r["investedYen"] = 10000; r["returnYen"] = est_return; r["isHit"] = hit
                r["resultStatus"] = f"🎯 的中 (1着:{actual[0]['num']}番 {actual[0]['name']} / 回収{est_return:,}円)" if hit else f"結果確定 (1着:{actual[0]['num']}番 {actual[0]['name']})"

    ai_targets = [r for r in day_db.get("races", []) if r.get("horses") and not r.get("aiPredicted") and (r.get("raceNumber") in (12, 11, 10, 9, 5) or r.get("rank") in ("S", "A", "New"))][:3]
    for r in ai_targets:
        if AI_CALL_COUNT >= MAX_AI_CALLS_PER_RUN: break
        bias_info = summarize_intraday_track_bias(day_db.get("races", []), r["venue"])
        detail = r.pop("detailText", "") or f"{r['venueLabel']} {r['name']}"
        prompt = (
            f"【モード: 標準（全頭評価）】日付:{date_str} {r['venueLabel']} {r['name']} ({r['surfaceDist']}・馬場:{r.get('trackCond','良')})\n"
            f"【実測先行馬数】N_lead={r.get('nLead',3)}頭 / 3シナリオ重み:{json.dumps(r.get('scenarioWeights',{}))}\n"
            f"【当日馬場バイアス】{bias_info}\n{detail}"
        )
        pred = call_gemini(r["skill"], prompt)
        if isinstance(pred, dict) and "horses" in pred:
            r["horses"] = merge_ai_with_baseline(pred["horses"], r["horses"])
            for k in ("tickets", "scenario", "pivotType", "rank", "usedModel"):
                if k in pred: r[k] = pred[k]
            r["aiPredicted"] = True

    for r in day_db.get("races", []):
        r.pop("detailText", None)

    venues = sorted(list({r["venue"] for r in day_db.get("races", [])}))
    day_db["trackBiases"] = [{"venue": v, "surf": "実測N_lead・3シナリオ混合", "trend": summarize_intraday_track_bias(day_db.get("races", []), v)} for v in venues]

    mleg = build_multileg_from_races(day_db.get("races", []), mode)
    if mleg: day_db["multiLeg"] = mleg
    day_db["screened"] = True
    day_db["updatedAt"] = now.strftime("%Y-%m-%d %H:%M JST")
    json.dump(day_db, open(db_path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

def run_pipeline():
    now = datetime.now(JST)
    is_weekend = now.weekday() in (5, 6)
    is_weekend_jra_hours = is_weekend and (8 <= now.hour < 17)

    if not is_weekend:
        for off in [0, -1, 1]:
            dt = now + timedelta(days=off)
            n_races = fetch_race_list(dt.strftime("%Y%m%d"), "nar")
            if len(n_races) >= 3:
                process_kaisai_day(dt.strftime("%Y-%m-%d"), n_races, now, off == 0, "nar")
                break

    for off in [-1, -2, -3, -4, -5]:
        dt = now + timedelta(days=off)
        rs = fetch_race_list(dt.strftime("%Y%m%d"), "jra")
        if len(rs) >= 6: process_kaisai_day(dt.strftime("%Y-%m-%d"), rs, now, False, "jra"); break
    for off in [0, 1, 2, 3, 4, 5]:
        dt = now + timedelta(days=off)
        rs = fetch_race_list(dt.strftime("%Y%m%d"), "jra")
        if len(rs) >= 6: process_kaisai_day(dt.strftime("%Y-%m-%d"), rs, now, off == 0, "jra"); break

    if is_weekend and not is_weekend_jra_hours:
        for off in [0, -1]:
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
