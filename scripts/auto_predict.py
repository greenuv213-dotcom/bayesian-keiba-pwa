import os, re, math, time, json, glob, socket, requests
from datetime import datetime, timedelta, timezone
from bs4 import BeautifulSoup
from google import genai
from google.genai import types

# Gemini 4 Hydrogen (HIGH) の深い思考時間に対応するためタイムアウトを90秒へ拡張
socket.setdefaulttimeout(90)

JST = timezone(timedelta(hours=9))
API_KEY = os.environ.get("GEMINI_API_KEY", "").strip()
client = genai.Client(api_key=API_KEY) if API_KEY else None
os.makedirs("data", exist_ok=True)

ENGINE_VER = "v10.3"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/124.0.0.0"}
JRA_VENUES = {"01":"札幌","02":"函館","03":"福島","04":"新潟","05":"東京","06":"中山","07":"中京","08":"京都","09":"阪神","10":"小倉"}
NAR_VENUES = {"42":"浦和","43":"船橋","44":"大井","45":"川崎","30":"門別","35":"盛岡","36":"水沢","46":"金沢","47":"笠松","48":"名古屋","50":"園田","51":"姫路","54":"高知","55":"佐賀"}
NANKAN_CODES = {"42", "43", "44", "45"}
TOP_RIDERS = ("矢野", "御神本", "笹川", "吉原", "森泰斗", "ルメール", "川田", "戸崎", "坂井", "武豊", "松山", "横山武", "鮫島克", "C.デム", "モレイラ", "レーン", "マーカン")
POWER_SIRES = ("ナダル", "クリソベリル", "ゴールドアリュール", "ルヴァンスレーヴ", "シニスターミニスター", "ヘニーヒューズ", "ドレフォン", "パイロ", "マインドユアビスケッツ", "キズナ", "キタサンブラック", "エピファネイア", "ロードカナロア", "コントレイル", "モーリス")
TURF_START_DIRT = {("東京",1300),("東京",1400),("東京",1600),("中山",1200),("京都",1400),("阪神",1400),("中京",1400),("福島",1150),("新潟",1200)}
GRADED_KEYWORDS = ("Jpn", "G1", "G2", "G3", "S1", "S2", "S3", "杯", "記念", "賞", "マイルCS", "ジャパンC", "有馬", "天皇賞", "ダービー", "オークス", "皐月", "桜花", "菊花", "秋華")

AI_CALL_COUNT = 0
MAX_AI_CALLS_PER_RUN = 5

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
            if mode == "nar" and (vcode not in NANKAN_CODES) and ("Jpn" not in name and rnum < 9):
                continue
            tm_el = li.select_one(".RaceList_Itemtime, .RaceData")
            m_tm = re.search(r"(\d{1,2}:\d{2})", tm_el.get_text(" ", strip=True) if tm_el else li.get_text(" ", strip=True))
            ptime = m_tm.group(1).zfill(5) if m_tm else ""
            lg = li.select_one(".RaceList_ItemLong")
            is_new = ("新馬" in name) or ("メイクデビュー" in name)
            is_graded = any(g in name for g in GRADED_KEYWORDS)
            skill = "app-bayesian-nar" if mode == "nar" else ("app-bayesian-make-debut" if is_new else "app-bayesian-horse-racing-text")
            races.append({
                "raceId": rid, "mode": mode, "venue": v, "raceNumber": rnum, "venueLabel": f"{v}{rnum}R",
                "name": name, "surfaceDist": lg.get_text(strip=True) if lg else "ダ1600m",
                "postTime": ptime,
                "rank": "New" if is_new else ("S" if is_graded else ("A" if rnum >= 9 else "B")),
                "skill": skill, "predicted": False, "aiPredicted": False
            })
        return races
    except Exception as e:
        print(f"[Warn] {mode} list error: {e}")
        return []

def parse_payout_table(rsoup: BeautifulSoup) -> dict:
    payouts = {"win": [], "umaren": [], "wide": [], "umatan": [], "sanrenpuku": []}
    class_map = {"Tansho": ("win", 1), "Umaren": ("umaren", 2), "Wide": ("wide", 2), "Umatan": ("umatan", 2), "Fuku3": ("sanrenpuku", 3)}
    for tr in rsoup.select("table.Payout_Detail_Table tr"):
        cls_list = tr.get("class") or []
        matched = next((class_map[c] for c in cls_list if c in class_map), None)
        if not matched: continue
        key, group_sz = matched
        res_td, pay_td = tr.select_one("td.Result"), tr.select_one("td.Payout")
        if not res_td or not pay_td: continue
        pays = [int(p.replace(",", "")) for p in re.findall(r"([\d,]+)円", pay_td.get_text(" ", strip=True))]
        if not pays: continue
        num_groups = []
        uls = res_td.select("ul")
        if uls:
            for ul in uls:
                nums = [int(x) for x in re.findall(r"\d+", ul.get_text(" ", strip=True))]
                if len(nums) >= group_sz: num_groups.append(nums[:group_sz])
        else:
            all_nums = [int(x) for x in re.findall(r"\d+", res_td.get_text(" ", strip=True))]
            for i in range(0, len(all_nums) - group_sz + 1, group_sz):
                num_groups.append(all_nums[i:i+group_sz])
        for idx, pay in enumerate(pays):
            if idx < len(num_groups):
                payouts[key].append({"nums": num_groups[idx], "pay": pay})
    return payouts

def fetch_full_shutuba(rid: str, mode: str = "jra") -> tuple[str, list, list, str, str, dict]:
    base = "https://race.netkeiba.com" if mode == "jra" else "https://nar.netkeiba.com"
    lines, top3_actual, raw_runners, odds_map = [], [], [], {}
    track_cond, post_time, payouts = "良", "", {}

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
        soup = get_soup(f"{base}/race/shutuba.html?race_id={rid}")
        r1, r2 = soup.select_one(".RaceData01"), soup.select_one(".RaceData02")
        if r1:
            r1_txt = " ".join(r1.get_text(" ", strip=True).split())
            m_pt = re.search(r"(\d{1,2}:\d{2})\s*発走", r1_txt)
            if m_pt: post_time = m_pt.group(1).zfill(5)
            for c in ("不良", "重", "稍重", "良"):
                if c in r1_txt: track_cond = c; break
            lines.append("【条件・馬場】" + r1_txt)
        if r2: lines.append("【コース・クラス】" + " ".join(r2.get_text(" ", strip=True).split()))
        for idx, tr in enumerate(soup.select("tr.HorseList")[:18]):
            n_el = tr.select_one("span.HorseName a, .HorseName a, td.HorseInfo a")
            if not n_el: continue
            h_name = n_el.get_text(strip=True)
            if not h_name: continue
            w_el, u_el = tr.select_one("td[class*='Waku']"), tr.select_one("td[class*='Umaban'], td.Num")
            u_txt = re.sub(r"\D", "", u_el.get_text(strip=True)) if u_el else ""
            u_int = int(u_txt) if u_txt.isdigit() else (idx + 1)
            w_txt = re.sub(r"\D", "", w_el.get_text(strip=True)) if w_el else ""
            w_int = int(w_txt) if w_txt.isdigit() else ((u_int - 1) // 2 + 1)
            sex_age = tr.select_one("td.Barei, span.Barei")
            futan = tr.select_one("td.Futan")
            j_el = tr.select_one("td.Jockey a, td.Jockey")
            wt_el = tr.select_one("td.Weight")
            odd_el = tr.select_one("td.Popular span[id^='odds-'], span[id^='odds-'], td.Odds")
            odd_val = odds_map.get(u_int, 0.0)
            if odd_val <= 1.0 and odd_el:
                m_o = re.search(r"(\d+\.\d+)", odd_el.get_text())
                if m_o: odd_val = float(m_o.group(1))
            raw_runners.append({
                "waku": w_int, "num": u_int, "name": h_name,
                "sexAge": sex_age.get_text(strip=True) if sex_age else "",
                "futan": futan.get_text(strip=True) if futan else "",
                "pedigree": "", "jockey": j_el.get_text(" ", strip=True) if j_el else "",
                "weight": wt_el.get_text(strip=True) if wt_el else "", "odds": odd_val, "past": ""
            })
    except Exception: pass

    try:
        psoup = get_soup(f"{base}/race/shutuba_past.html?race_id={rid}")
        if not post_time:
            pr1 = psoup.select_one(".RaceData01")
            if pr1:
                m_pt = re.search(r"(\d{1,2}:\d{2})\s*発走", pr1.get_text(" ", strip=True))
                if m_pt: post_time = m_pt.group(1).zfill(5)
        for idx, tr in enumerate(psoup.select("tr.HorseList")[:18]):
            n_el = tr.select_one(".Horse02 a, .HorseName a, .Horse02")
            if not n_el: continue
            h_name = n_el.get_text(strip=True).split()[0]
            f_sire, m_sire = tr.select_one(".Horse01"), tr.select_one(".Horse03")
            ped = f"父:{f_sire.get_text(strip=True) if f_sire else ''}/母父:{m_sire.get_text(strip=True) if m_sire else ''}" if (f_sire or m_sire) else ""
            pasts = " / ".join([" ".join(td.get_text(" ", strip=True).split())[:95] for td in tr.select("td.Past")[:4]])
            target = next((x for x in raw_runners if x["name"] == h_name), None)
            if target:
                if ped: target["pedigree"] = ped
                if pasts: target["past"] = pasts
            else:
                u_el = tr.select_one("td[class*='Umaban'], td.Num")
                u_txt = re.sub(r"\D", "", u_el.get_text(strip=True)) if u_el else ""
                u_int = int(u_txt) if u_txt.isdigit() else (idx + 1)
                raw_runners.append({"waku": (u_int-1)//2+1, "num": u_int, "name": h_name, "sexAge": "", "futan": "", "pedigree": ped, "jockey": "", "weight": "", "odds": odds_map.get(u_int, 0.0), "past": pasts})
    except Exception: pass

    try:
        rsoup = get_soup(f"{base}/race/result.html?race_id={rid}")
        rd1 = rsoup.select_one(".RaceData01")
        if rd1:
            rd1_txt = rd1.get_text(" ", strip=True)
            if not post_time:
                m_pt = re.search(r"(\d{1,2}:\d{2})\s*発走", rd1_txt)
                if m_pt: post_time = m_pt.group(1).zfill(5)
            for c in ("不良", "重", "稍重", "良"):
                if c in rd1_txt: track_cond = c; break
        for tr in rsoup.select("#All_Result_Table tbody tr, table.RaceTable01 tbody tr")[:18]:
            tds = [td.get_text(" ", strip=True) for td in tr.select("td")]
            if len(tds) < 8: continue
            rank_s, w_s, u_s = re.sub(r"\D", "", tds[0]), re.sub(r"\D", "", tds[1]), re.sub(r"\D", "", tds[2])
            if not u_s.isdigit(): continue
            u_int, w_int = int(u_s), (int(w_s) if w_s.isdigit() else 4)
            n_el = tr.select_one("span.Horse_Name a, .Horse_Name, td.Horse_Info a")
            h_name = n_el.get_text(strip=True) if n_el else tds[3].split()[0]
            odd_num = odds_map.get(u_int, 0.0)
            for cell in tds[8:]:
                if re.match(r"^\d{1,4}\.\d$", cell.replace(",", "")):
                    odd_num = float(cell.replace(",", "")); break
            ex = next((x for x in raw_runners if x["name"] == h_name), None)
            if ex:
                ex["num"], ex["waku"] = u_int, w_int
                if odd_num > 1.0: ex["odds"] = odd_num
            else:
                raw_runners.append({"waku": w_int, "num": u_int, "name": h_name, "sexAge": tds[4] if len(tds)>4 else "", "futan": tds[5] if len(tds)>5 else "", "pedigree": "", "jockey": tds[6].split()[0] if len(tds)>6 else "", "weight": tds[14] if len(tds)>14 else "", "odds": odd_num or 0.0, "past": ""})
            if len(top3_actual) < 3 and rank_s.isdigit():
                top3_actual.append({"rank": rank_s, "waku": w_int, "num": u_int, "name": h_name, "odds": str(odd_num or 10.0)})
        if top3_actual:
            payouts = parse_payout_table(rsoup)
    except Exception: pass

    raw_runners.sort(key=lambda x: x["num"])
    for r in raw_runners:
        lines.append(f"{r['waku']}枠 {r['num']}番 {r['name']} (性齢:{r.get('sexAge','')} 斤量:{r.get('futan','')} {r.get('pedigree','')} 騎手:{r['jockey']} 馬体:{r['weight']} 単勝:{r['odds'] if r['odds']>1 else '未発売'}倍) | 近4走:{r['past']}")
    return "\n".join(lines[:22]), top3_actual, raw_runners, track_cond, post_time, payouts

def summarize_intraday_track_bias(races: list, venue: str) -> str:
    finished = [r for r in races if r.get("venue") == venue and r.get("actualTop3")]
    if not finished: return f"{venue}: 前半確定レースなし（標準バイアス想定）"
    inner_w = sum(1 for r in finished if r["actualTop3"][0].get("waku", 4) <= 3)
    outer_w = sum(1 for r in finished if r["actualTop3"][0].get("waku", 4) >= 6)
    trend = "外枠(6〜8枠)優勢" if outer_w >= inner_w + 2 else ("内枠(1〜3枠)優勢" if inner_w >= outer_w + 2 else "内外フラット")
    return f"{venue}当日実測({len(finished)}R集計): 1着内枠{inner_w}回/外枠{outer_w}回 → 【{trend}】"

def parse_past_metrics(past_text: str, waku: int) -> dict:
    corners = re.findall(r"\b(\d{1,2})-(\d{1,2})(?:-(\d{1,2}))?(?:-(\d{1,2}))?\b", past_text)
    c1s = [int(c[0]) for c in corners if c[0].isdigit() and 1 <= int(c[0]) <= 18]
    avg_1c = (sum(c1s) / len(c1s)) if c1s else (4.0 if waku >= 5 else 6.0)
    is_leader = any(c <= 2 for c in c1s[:2]) if c1s else False
    style = "逃" if avg_1c <= 2.3 else ("先" if avg_1c <= 5.2 else ("差" if avg_1c <= 9.5 else "追"))

    ranks = [int(m[0] or m[1]) for m in re.findall(r"(?:^|\s)(\d{1,2})着|\s(\d{1,2})\s+[芝ダ]", past_text) if (m[0] or m[1]).isdigit()]
    ranks = [rk for rk in ranks if 1 <= rk <= 18][:4]
    avg_rank = (sum(ranks) / len(ranks)) if ranks else 7.5
    margins = [float(m) for m in re.findall(r"\((\d+\.\d)\)", past_text)]
    is_silver = (sum(1 for rk in ranks if rk in (2, 3)) >= 2 and 1 not in ranks)
    has_rebound = (any(m <= 0.2 for m in margins) and len(margins) >= 2 and margins[0] >= 0.6)
    return {"style": style, "isLeader": is_leader, "avgRank": avg_rank, "ranks": ranks, "isSilver": is_silver, "hasRebound": has_rebound}

def compute_bayesian_full_field(raw_runners: list, race_meta: dict, track_cond: str = "良") -> tuple[list, int, dict]:
    if not raw_runners: return [], 3, {"s1": 35, "s2": 40, "s3": 25}
    n = len(raw_runners)
    venue, sdist, mode = race_meta.get("venue", "東京"), race_meta.get("surfaceDist", "ダ1600m"), race_meta.get("mode", "jra")
    m_dist = re.search(r"(\d{3,4})", sdist)
    dist = int(m_dist.group(1)) if m_dist else 1600
    is_dirt = ("ダ" in sdist) or (mode == "nar")
    is_turf_start = is_dirt and ((venue, dist) in TURF_START_DIRT)
    is_wet, is_tight = (track_cond in ("重", "不良")), (venue in ("浦和", "川崎", "中山", "福島", "小倉"))

    parsed = [parse_past_metrics(r.get("past", ""), r.get("waku", 4)) for r in raw_runners]
    n_lead = max(1, sum(1 for p in parsed if p["isLeader"]))
    pi_s1, pi_s2, pi_s3 = ((0.25, 0.35, 0.40) if not is_tight else (0.30, 0.35, 0.35)) if n_lead >= 5 else ((0.50, 0.35, 0.15) if n_lead <= 2 else (0.35, 0.40, 0.25))
    scen_w = {"s1": int(pi_s1*100), "s2": int(pi_s2*100), "s3": int(pi_s3*100)}

    has_live_odds = sum(1 for r in raw_runners if r.get("odds", 0) > 1.0) >= max(3, n // 2)
    logits, place_deltas, notes, styles = [], [], [], []

    for idx, r in enumerate(raw_runners):
        waku, jockey, wt, sex_age, futan, ped = r.get("waku", 4), r.get("jockey", ""), r.get("weight", ""), r.get("sexAge", ""), r.get("futan", ""), r.get("pedigree", "")
        pm, style = parsed[idx], parsed[idx]["style"]
        odd = float(r.get("odds", 0))

        if has_live_odds and odd > 1.0:
            base_theta = -0.82 * math.log(odd)
        else:
            win_bonus = 0.45 if (pm["ranks"] and pm["ranks"][0] == 1) else (0.25 if (pm["ranks"] and pm["ranks"][0] <= 3) else 0.0)
            base_theta = -0.26 * (pm["avgRank"] - 6.0) + win_bonus

        delta_th, delta_pl, reasons = 0.0, 0.0, []
        m_ft = re.search(r"(\d{2}\.?\d?)", str(futan))
        ft_val = float(m_ft.group(1)) if m_ft else 56.0
        if "3" in sex_age and ft_val <= 55.0: delta_th += 0.18; delta_pl += 0.12; reasons.append(f"F:3歳{ft_val}kg(H:軽量優遇)")
        elif ft_val >= 58.0: delta_th -= 0.14; delta_pl -= 0.10; reasons.append(f"F:斤量{ft_val}kg(H:酷量減点)")
        if is_turf_start:
            if waku >= 7 and style in ("逃", "先"): delta_th += 0.20; delta_pl += 0.15; reasons.append(f"F:芝発進{waku}枠先行(H:Top3昇格)")
            elif waku <= 3 and style == "先" and not is_wet: delta_th += 0.15; delta_pl += 0.16; reasons.append("F:乾燥ダ内好位(H:ポケット残し)")
        m_bw = re.search(r"(\d{3})\(([+-]?\d+)\)", wt)
        body_w, diff_w = (int(m_bw.group(1)), int(m_bw.group(2))) if m_bw else (480, 0)
        if dist >= 1800 and diff_w >= 12: delta_th -= 0.22; delta_pl -= 0.16; reasons.append(f"F:馬体+{diff_w}kg(H:TypeII減点)")
        elif is_wet and is_dirt and waku >= 6 and body_w >= 500 and style in ("逃", "先"): delta_th += 0.18; delta_pl += 0.14; reasons.append(f"F:{waku}枠{body_w}kg(H:道悪外枠大型先行)")
        elif -8 <= diff_w <= -2: delta_th += 0.10; reasons.append(f"F:馬体{diff_w}kg絞り(H:好仕上)")
        if pm["isSilver"]: delta_th -= 0.08; delta_pl += 0.22; reasons.append("F:近走2・3着連続(H:善戦Anchor)")
        elif pm["hasRebound"]: delta_th += 0.20; delta_pl += 0.14; reasons.append("F:現級0.2s差実績(H:巻き返し)")
        if any(tr in jockey for tr in TOP_RIDERS): delta_th += 0.22; delta_pl += 0.20; reasons.append(f"F:{jockey[:4]}騎手(H:Top騎手)")
        if any(s in ped for s in POWER_SIRES): delta_th += 0.12; reasons.append(f"F:{ped[:10]}(H:血統適性)")
        scen_shift = (0.14 * pi_s1 - 0.10 * pi_s3) if style in ("逃", "先") else (-0.10 * pi_s1 + 0.16 * pi_s3)
        if not reasons: reasons.append(f"F:{waku}枠・近走平均{pm['avgRank']:.1f}着")
        logits.append(base_theta + delta_th + scen_shift); place_deltas.append(delta_pl); notes.append(" / ".join(reasons)[:46]); styles.append(style)

    max_l = max(logits)
    w1 = [math.exp((x - max_l) * 1.15) for x in logits]
    f_probs = [x / sum(w1) * 100.0 for x in w1]
    w2 = [math.exp(((logits[i] + place_deltas[i]) - max_l) * 1.05) for i in range(n)]
    p2_raw = [0.46 * f_probs[i] + 0.54 * (w2[i] / sum(w2) * 100.0) for i in range(n)]
    top2_probs = [min(92.0, x * (200.0 / max(1.0, sum(p2_raw)))) for x in p2_raw]
    top3_probs = [min(96.0, x * (300.0 / max(1.0, sum(top2_probs)))) for x in top2_probs]

    final_odds = [round(float(r["odds"]), 1) if (has_live_odds and r.get("odds", 0) > 1.0) else round(max(1.5, min(99.9, 80.0 / max(0.8, f_probs[i]))), 1) for i, r in enumerate(raw_runners)]
    inv_power = [math.pow(max(1.1, o), -1.08) for o in final_odds]
    q_probs = [x / sum(inv_power) * 100.0 for x in inv_power]

    order = sorted(range(n), key=lambda i: f_probs[i], reverse=True)
    if len(order) >= 2 and parsed[order[0]]["isSilver"]: order[0], order[1] = order[1], order[0]
    marks_map, roles_map = {}, {}
    for rk, i in enumerate(order):
        gap = f_probs[i] - q_probs[i]
        if rk == 0: marks_map[i], roles_map[i] = "◎", "1着妙味主軸"
        elif rk == 1: marks_map[i], roles_map[i] = "◯", "双頭対抗軸"
        elif rk == 2: marks_map[i], roles_map[i] = "▲", "安定Connector"
        elif rk == 3 or (rk <= 5 and (gap >= 2.0 or parsed[i]["hasRebound"])): marks_map[i], roles_map[i] = "☆", "展開特注穴"
        elif rk <= 6: marks_map[i], roles_map[i] = "△", "3列目連下"
        elif q_probs[i] >= 12.0 and gap <= -3.5: marks_map[i], roles_map[i] = "危", "過剰人気警戒"
        elif rk >= n - 2: marks_map[i], roles_map[i] = "消", "時計・展開劣勢"
        else: marks_map[i], roles_map[i] = "無", "強調材料乏しい"

    return [{
        "mark": marks_map[i], "role": roles_map[i], "num": raw_runners[i]["num"], "name": raw_runners[i]["name"],
        "style": styles[i], "f": round(f_probs[i], 1), "q": round(q_probs[i], 1),
        "top2": round(top2_probs[i], 1), "top3": round(top3_probs[i], 1),
        "odds": final_odds[i], "comment": notes[i]
    } for i in order], n_lead, scen_w

def evaluate_10k_payout(race: dict) -> dict:
    payouts, horses = race.get("payouts") or {}, race.get("horses") or []
    if not payouts or len(horses) < 3 or race.get("rank") == "Pass": return {}
    sorted_h = sorted(horses, key=lambda x: float(x.get("f", 0)), reverse=True)
    valid = [h for h in sorted_h if h.get("mark") not in ("消", "危", "無")]
    pool = valid if len(valid) >= 4 else [h for h in sorted_h if h.get("mark") != "消"]
    if len(pool) < 3: pool = sorted_h
    h1, h2, h3, h4 = pool[0], pool[1], pool[2], (pool[3] if len(pool) > 3 else pool[2])
    himos = [h for h in sorted_h if h["num"] not in (h1["num"], h2["num"], h3["num"], h4["num"]) and h.get("mark") != "消"][:4]
    is_sp = (float(h1.get("f", 0)) >= 28.0 and race.get("pivotType") != "Dual-Pivot") or race.get("pivotType") == "Single-Pivot"
    B = 10000
    if is_sp:
        row1, row2, row3 = [h1["num"]], [h2["num"], h3["num"], h4["num"]], [h2["num"], h3["num"], h4["num"]] + [x["num"] for x in himos]
        specs = [("wide",[h1["num"],h2["num"]],0.24,f"ワイド {h1['num']}-{h2['num']}"),("wide",[h1["num"],h3["num"]],0.18,f"ワイド {h1['num']}-{h3['num']}"),("win",[h1["num"]],0.14,f"単勝 {h1['num']}"),("umaren",[h1["num"],h2["num"]],0.10,f"馬連 {h1['num']}-{h2['num']}"),("umaren",[h1["num"],h3["num"]],0.08,f"馬連 {h1['num']}-{h3['num']}"),("umatan",[h1["num"],h2["num"]],0.06,f"馬単 {h1['num']}→{h2['num']}"),("umatan",[h1["num"],h3["num"]],0.05,f"馬単 {h1['num']}→{h3['num']}")]
    else:
        row1, row2, row3 = [h1["num"], h2["num"]], sorted({h2["num"], h3["num"], h4["num"]}), sorted({h3["num"], h4["num"]} | {x["num"] for x in himos})
        specs = [("wide",[h1["num"],h3["num"]],0.22,f"ワイド {h1['num']}-{h3['num']}"),("wide",[h2["num"],h3["num"]],0.15,f"ワイド {h2['num']}-{h3['num']}"),("wide",[h1["num"],h2["num"]],0.15,f"ワイド {h1['num']}-{h2['num']}"),("win",[h1["num"]],0.08,f"単勝 {h1['num']}"),("win",[h2["num"]],0.05,f"単勝 {h2['num']}"),("umaren",[h1["num"],h3["num"]],0.09,f"馬連 {h1['num']}-{h3['num']}"),("umaren",[h2["num"],h3["num"]],0.06,f"馬連 {h2['num']}-{h3['num']}"),("umaren",[h1["num"],h2["num"]],0.05,f"馬連 {h1['num']}-{h2['num']}")]
    trio_set = {tuple(sorted((a, b, c))) for a in row1 for b in row2 if a != b for c in row3 if c != a and c != b}
    trio_pts = max(1, len(trio_set))
    trio_amt = min(B - 800, trio_pts * 100)
    rem, sum_sh = max(800, B - trio_amt), sum(s[2] for s in specs)
    run_rem, total_ret, hit_labels = rem, 0, []
    for idx, (tk, nums, sh, label) in enumerate(specs):
        amt = max(100, round(run_rem / 100) * 100) if idx == len(specs) - 1 else max(100, round((rem * sh / sum_sh) / 100) * 100)
        run_rem = max(100, run_rem - amt)
        for entry in payouts.get(tk, []):
            if (entry["nums"] == nums if tk in ("win", "umatan") else sorted(entry["nums"]) == sorted(nums)):
                pay_yen = int((amt // 100) * entry["pay"]); total_ret += pay_yen; hit_labels.append(f"{label} ({pay_yen:,}円)")
    per_pt = max(100, (trio_amt // trio_pts) // 100 * 100)
    for entry in payouts.get("sanrenpuku", []):
        if tuple(sorted(entry["nums"])) in trio_set:
            pay_yen = int((per_pt // 100) * entry["pay"]); total_ret += pay_yen; hit_labels.append(f"3連複F ({pay_yen:,}円)")
    return {"investedYen": B, "returnYen": total_ret, "actualRoi": round(total_ret * 100.0 / B, 1), "isHit": total_ret > 0, "hitTickets": hit_labels}

def classify_race_tier(r: dict) -> str:
    """ハイブリッド振り分け: WIN5・重賞・S・メイン11R=high_h / 新馬=med_h / その他A=flash"""
    if r.get("rank") == "New":
        return "med_h"
    if r.get("rank") == "S" or r.get("raceNumber") == 11 or any(g in r.get("name", "") for g in GRADED_KEYWORDS):
        return "high_h"
    return "flash"

def call_gemini(skill: str, prompt: str, tier: str = "flash") -> dict:
    """
    無料枠計40回/日のハイブリッド呼び出し:
      - tier='high_h': WIN5・重賞・Sランク・メイン11R -> gemini-4-hydrogen (HIGH) -> 3.8 Flash
      - tier='med_h' : 新馬戦                        -> gemini-4-hydrogen (MEDIUM) -> 3.8 Flash
      - tier='flash' : その他のAランク等              -> gemini-3.8-flash (MEDIUM) のみ（Hydrogen枠を温存）
    """
    global AI_CALL_COUNT
    if not client or AI_CALL_COUNT >= MAX_AI_CALLS_PER_RUN: return {}
    AI_CALL_COUNT += 1
    p = f"skills/{skill}/SKILL.md"
    sys_inst = open(p, "r", encoding="utf-8").read() if os.path.exists(p) else "Output valid JSON only."

    if tier == "high_h":
        candidates = [("gemini-4-hydrogen", "HIGH"), ("gemini-3.8-flash", "MEDIUM")]
    elif tier == "med_h":
        candidates = [("gemini-4-hydrogen", "MEDIUM"), ("gemini-3.8-flash", "MEDIUM")]
    else:
        candidates = [("gemini-3.8-flash", "MEDIUM")]

    for m, think_lvl in candidates:
        try:
            time.sleep(2)
            try:
                cfg = types.GenerateContentConfig(
                    system_instruction=sys_inst,
                    response_mime_type="application/json",
                    thinking_config=types.ThinkingConfig(thinking_level=think_lvl),
                )
            except Exception:
                cfg = types.GenerateContentConfig(
                    system_instruction=sys_inst,
                    response_mime_type="application/json",
                )
            res = client.models.generate_content(model=m, contents=prompt, config=cfg)
            data = json.loads(re.sub(r"^```(?:json)?\s*|\s*```$", "", (res.text or "").strip(), flags=re.DOTALL))
            data["usedModel"] = f"{m}({think_lvl})"
            print(f"[AI Success] {skill} -> {data['usedModel']}")
            return data
        except Exception as e:
            print(f"[Fallback] {m}({think_lvl}): {e}")
    return {}

def fetch_official_win5_ids() -> list:
    try:
        soup = get_soup("https://race.netkeiba.com/top/win5.html")
        ids = []
        for a in soup.select("a[href*='race_id=']"):
            m = re.search(r"race_id=(\d{12})", a.get("href", ""))
            if m and m.group(1) not in ids: ids.append(m.group(1))
        if len(ids) >= 5: return ids[:5]
    except Exception: pass
    return []

def build_multileg_with_ai(races: list, mode: str, date_str: str) -> dict:
    """JRA日曜WIN5は app-bayesian-win5 を Gemini 4 Hydrogen (HIGH) で5鞍一括推論"""
    dt = datetime.strptime(date_str, "%Y-%m-%d")
    if mode == "nar":
        cand = [r for r in races if r.get("raceNumber") in (10, 11, 12) and isinstance(r.get("horses"), list) and len(r["horses"]) >= 2]
        if len(cand) < 3: return {}
        selected = sorted(cand[-3:], key=lambda x: x.get("postTime") or "20:00")
    else:
        if dt.weekday() != 6: return {}
        off_ids = fetch_official_win5_ids()
        matched = [r for r in races if r["raceId"] in off_ids and isinstance(r.get("horses"), list) and len(r["horses"]) >= 2]
        if len(matched) == 5:
            selected = sorted(matched, key=lambda x: x.get("postTime") or "15:00")
        else:
            pool = [r for r in races if r.get("raceNumber") in (9, 10, 11) and isinstance(r.get("horses"), list) and len(r["horses"]) >= 2]
            pool.sort(key=lambda x: (x["raceNumber"], x.get("postTime") or "14:30"), reverse=True)
            if len(pool) < 5: return {}
            selected = sorted(pool[:5], key=lambda x: x.get("postTime") or "15:00")

    # すでに全対象レースが終了している過去日はAPI消費せずスキップ
    all_finished = all(bool(r.get("actualTop3")) for r in selected)
    if mode == "jra" and len(selected) == 5 and not all_finished:
        blocks = []
        for idx, r in enumerate(selected):
            h_txt = "\n".join([f" {h['num']}番{h['name']}(脚質:{h['style']} 単勝:{h['odds']}倍 {h['comment']})" for h in r["horses"][:16]])
            blocks.append(f"=== Leg{idx+1} {r['venueLabel']} {r['name']} ({r['surfaceDist']} 発走{r.get('postTime','')}) ===\n{h_txt}")
        w_prompt = (
            f"日付:{date_str} のJRA WIN5対象5レースを10大モジュールで一括推論し、以下のJSONスキーマで出力せよ:\n"
            "{\"summary\":\"5レース全体の攻略総括(100字以内)\",\"legs\":[{\"leg\":1,\"venue\":\"会場R\",\"name\":\"レース名\",\"postTime\":\"HH:MM\",\"typeBPlus\":true/false,\"note\":\"展開・バイアス見解(45字以内)\",\"horses\":[{\"num\":馬番,\"name\":\"馬名\",\"f\":純粋勝率(合計100%のうち上位7頭で80〜92%程度),\"odds\":オッズ,\"note\":\"F/H根拠(30字以内)\"}]}],\"hedges\":[{\"num\":馬番,\"name\":\"Leg5伏兵名\",\"odds\":オッズ,\"hedge50k\":円,\"hedge100k\":円}]}\n\n"
            + "\n".join(blocks)
        )
        ai_w = call_gemini("app-bayesian-win5", w_prompt, tier="high_h")
        if isinstance(ai_w, dict) and isinstance(ai_w.get("legs"), list) and len(ai_w["legs"]) == 5:
            ai_w["predicted"] = True
            ai_w["aiPredicted"] = True
            ai_w["date"] = date_str
            ai_w["engineVer"] = ENGINE_VER
            for idx, r in enumerate(selected):
                leg_hs = ai_w["legs"][idx].get("horses", [])
                by_num = {int(h["num"]): h for h in leg_hs if str(h.get("num","")).isdigit()}
                if by_num:
                    for h in r["horses"]:
                        if h["num"] in by_num:
                            ah = by_num[h["num"]]
                            if ah.get("f"): h["f"] = round(float(ah["f"]), 1)
                            if ah.get("note"): h["comment"] = ah["note"]
                    sf = max(1.0, sum(float(x["f"]) for x in r["horses"]))
                    for x in r["horses"]:
                        x["f"] = round(float(x["f"]) * 100.0 / sf, 1)
                        x["top2"] = round(min(92.0, x["f"] * 1.9), 1)
                        x["top3"] = round(min(96.0, x["f"] * 2.8), 1)
                    r["horses"].sort(key=lambda x: float(x["f"]), reverse=True)
                    for rk, x in enumerate(r["horses"]):
                        x["mark"] = ["◎","◯","▲","☆","△","△","△"][rk] if rk < 7 else "無"
                    r["aiPredicted"] = True
                    r["usedModel"] = ai_w.get("usedModel", "gemini-4-hydrogen(HIGH)")
                    if ai_w["legs"][idx].get("note"): r["scenario"] = ai_w["legs"][idx]["note"]
            return ai_w

    legs = []
    for idx, r in enumerate(selected):
        hs = sorted(r["horses"], key=lambda x: float(x.get("f", 10)), reverse=True)
        legs.append({
            "leg": idx + 1, "venue": r["venueLabel"], "name": r["name"], "cond": r["surfaceDist"],
            "postTime": r.get("postTime", ""), "typeBPlus": (float(hs[0].get("f", 25)) < 25.5 or r.get("nLead", 3) >= 4),
            "note": r.get("scenario", "")[:55],
            "horses": [{"num": h.get("num", 1), "name": h.get("name", "有力馬"), "f": float(h.get("f", 15)), "odds": float(h.get("odds", 5.5)), "note": h.get("comment", "")[:34]} for h in hs[:7]]
        })
    last_hs = legs[-1]["horses"][2:4]
    hedges = [{"num": h["num"], "name": f"{legs[-1]['venue']} {h['name']}", "odds": h["odds"], "hedge50k": int((50000 / max(1.5, h["odds"]) + 99) // 100 * 100), "hedge100k": int((100000 / max(1.5, h["odds"]) + 99) // 100 * 100)} for h in last_hs]
    return {"predicted": True, "aiPredicted": False, "date": date_str, "engineVer": ENGINE_VER, "summary": f"【{date_str} 実力ベースライン編成（{'トリプル馬単50円単位' if mode=='nar' else 'JRA WIN5 100円単位'}）】", "legs": legs, "hedges": hedges}

def process_kaisai_day(date_str: str, races: list, now: datetime, is_today: bool, mode: str = "jra"):
    suffix = "_nar" if mode == "nar" else ""
    db_path = f"data/{date_str}{suffix}.json"
    day_db = json.load(open(db_path, "r", encoding="utf-8")) if os.path.exists(db_path) else {"date": date_str, "mode": mode, "races": races}
    if not day_db.get("races") and races: day_db["races"] = races
    day_db["mode"] = mode
    need_upgrade = (day_db.get("engineVer") != ENGINE_VER)

    dt = datetime.strptime(date_str, "%Y-%m-%d")
    if mode == "jra" and dt.weekday() != 6:
        day_db.pop("multiLeg", None)

    for r in day_db.get("races", []):
        needs_fix = need_upgrade or (not r.get("postTime") or (r.get("postTime") == "15:00" and r.get("raceNumber", 11) < 10))
        needs_payout = (not r.get("payouts")) or (not r.get("actualTop3"))
        has_real = isinstance(r.get("horses"), list) and len(r["horses"]) >= 5
        if has_real and not needs_fix and not needs_payout and r.get("evalDone"):
            continue
        detail, actual, raw_runners, track_cond, ptime, payouts = fetch_full_shutuba(r["raceId"], mode=mode)
        if ptime: r["postTime"] = ptime
        if raw_runners:
            base_horses, n_lead, scen_w = compute_bayesian_full_field(raw_runners, r, track_cond=track_cond)
            r["nLead"], r["trackCond"], r["scenarioWeights"] = n_lead, track_cond, scen_w
            if not has_real or (need_upgrade and not r.get("aiPredicted")):
                r["horses"] = base_horses
                r["predicted"] = True
                r["scenario"] = f"{r['venueLabel']}({r['surfaceDist']}・{track_cond}) 実測N_lead={n_lead}頭。3シナリオ混合(S1前残り{scen_w['s1']}% / S2標準{scen_w['s2']}% / S3前崩れ{scen_w['s3']}%)で全{len(base_horses)}頭を推論。"
            else:
                by_name = {x["name"]: x for x in raw_runners}
                for h in r["horses"]:
                    if h.get("name") in by_name:
                        h["num"] = by_name[h["name"]]["num"]
                        if by_name[h["name"]]["odds"] > 1.0: h["odds"] = by_name[h["name"]]["odds"]
            r["detailText"] = detail
        if actual: r["actualTop3"] = actual
        if payouts and any(payouts.values()):
            r["payouts"] = payouts
            ev = evaluate_10k_payout(r)
            if ev:
                r.update(ev); r["evalDone"] = True
                prof = ev["returnYen"] - ev["investedYen"]
                r["resultStatus"] = f"🎯 的中 払戻{ev['returnYen']:,}円 (回収率{ev['actualRoi']}% / {prof:+,}円)" if ev["isHit"] else f"❌ 不的中 回収率0.0%"

    # 1. 日曜WIN5（Hydrogen HIGH 一括）または地方トリプル馬単
    if (mode == "jra" and dt.weekday() == 6) or mode == "nar":
        cur_ml = day_db.get("multiLeg") or {}
        need_ml_ai = (not cur_ml.get("aiPredicted")) or (need_upgrade and "hydrogen" not in str(cur_ml.get("usedModel", "")))
        if need_ml_ai:
            mleg = build_multileg_with_ai(day_db.get("races", []), mode, date_str)
            if mleg: day_db["multiLeg"] = mleg

    # 2. 未発走の勝負レースへハイブリッドAI本推論を適用（重賞・S・11R・新馬 -> Hydrogen / その他A -> 3.8 Flash）
    ai_candidates = []
    for r in day_db.get("races", []):
        if not r.get("horses") or r.get("actualTop3") or r.get("rank") == "Pass":
            continue
        if not (r.get("rank") in ("S", "A", "New") or r.get("raceNumber") in (12, 11, 10, 9, 5)):
            continue
        tier = classify_race_tier(r)
        used = str(r.get("usedModel", ""))
        needs_ai = (not r.get("aiPredicted")) or (need_upgrade and tier in ("high_h", "med_h") and "hydrogen" not in used)
        if not needs_ai:
            continue
        # 発走1時間前優先、それ以外は重要度順（重賞/11R -> 新馬 -> その他A）
        prio = 0 if tier == "high_h" else (1 if tier == "med_h" else 2)
        if is_today and re.match(r"^\d{2}:\d{2}$", r.get("postTime", "")):
            pdt = datetime.strptime(f"{date_str} {r['postTime']}", "%Y-%m-%d %H:%M").replace(tzinfo=JST)
            mins = (pdt - now).total_seconds() / 60.0
            if 15 <= mins <= 95: prio -= 10
        ai_candidates.append((prio, tier, r))

    ai_candidates.sort(key=lambda x: x[0])
    for _, tier, r in ai_candidates[:4]:
        if AI_CALL_COUNT >= MAX_AI_CALLS_PER_RUN: break
        bias_info = summarize_intraday_track_bias(day_db.get("races", []), r["venue"])
        detail = r.pop("detailText", "") or f"{r['venueLabel']} {r['name']}"
        pred = call_gemini(
            r["skill"],
            f"【モード: 標準（全頭評価）】日付:{date_str} {r['venueLabel']} {r['name']} ({r['surfaceDist']}・{r.get('trackCond','良')})\n"
            f"【当日バイアス】{bias_info}\n"
            f"全頭について mark, role, style, f(勝率), top2(2着内率), top3(3着内率), comment(35字以内) と scenario, pivotType, rank をJSON出力せよ:\n{detail}",
            tier=tier,
        )
        if isinstance(pred, dict) and "horses" in pred:
            by_name = {h["name"]: h for h in r["horses"]}
            for ah in pred["horses"]:
                t = by_name.get(ah.get("name")) or next((x for x in r["horses"] if str(x["num"]) == str(ah.get("num"))), None)
                if t:
                    for k in ("mark", "role", "style", "comment"):
                        if ah.get(k): t[k] = ah[k]
                    for k in ("f", "top2", "top3"):
                        if ah.get(k): t[k] = round(float(ah[k]), 1)
            sf = max(1.0, sum(float(x["f"]) for x in r["horses"]))
            s2 = max(1.0, sum(float(x["top2"]) for x in r["horses"]))
            s3 = max(1.0, sum(float(x["top3"]) for x in r["horses"]))
            for x in r["horses"]:
                x["f"] = round(float(x["f"]) * 100.0 / sf, 1)
                x["top2"] = round(min(94.0, float(x["top2"]) * 200.0 / s2), 1)
                x["top3"] = round(min(97.0, float(x["top3"]) * 300.0 / s3), 1)
            r["horses"].sort(key=lambda x: float(x["f"]), reverse=True)
            for k in ("scenario", "pivotType", "rank", "usedModel"):
                if k in pred: r[k] = pred[k]
            r["aiPredicted"] = True

    for r in day_db.get("races", []): r.pop("detailText", None)
    venues = sorted(list({r["venue"] for r in day_db.get("races", [])}))
    day_db["trackBiases"] = [{"venue": v, "surf": "Gemini 4 Hybrid・実配当照合済", "trend": summarize_intraday_track_bias(day_db.get("races", []), v)} for v in venues]
    day_db["engineVer"] = ENGINE_VER
    day_db["updatedAt"] = now.strftime("%Y-%m-%d %H:%M JST")
    json.dump(day_db, open(db_path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

def update_global_stats(now: datetime):
    jra, nar = {"races": 0, "hits": 0, "invest": 0, "ret": 0, "passSaved": 0}, {"races": 0, "hits": 0, "invest": 0, "ret": 0, "passSaved": 0}
    recent = []
    for fp in sorted(glob.glob("data/20*.json"), reverse=True):
        try:
            d = json.load(open(fp, "r", encoding="utf-8"))
            is_nar = d.get("mode") == "nar" or fp.endswith("_nar.json")
            b = nar if is_nar else jra
            for r in d.get("races", []):
                if r.get("rank") == "Pass": b["passSaved"] += 10000
                elif r.get("evalDone") and r.get("investedYen"):
                    inv, ret = int(r["investedYen"]), int(r.get("returnYen", 0))
                    b["races"] += 1; b["invest"] += inv; b["ret"] += ret
                    if ret > 0: b["hits"] += 1
                    if len(recent) < 12:
                        recent.append({"date": d.get("date",""), "race": f"{r['venueLabel']} {r['name']}", "status": r.get("resultStatus",""), "roi": f"{r.get('actualRoi',0)}%", "hits": r.get("hitTickets", [])})
        except Exception: pass
    json.dump({"updatedAt": now.strftime("%Y-%m-%d %H:%M JST"), "jra": jra, "nar": nar, "recentResults": recent}, open("data/stats.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)

def run_pipeline():
    now = datetime.now(JST)
    is_weekend = now.weekday() in (5, 6)
    is_weekend_jra_hours = is_weekend and (8 <= now.hour < 17)

    upcoming_days = []
    for off in [0, 1, 2, 3, 4, 5]:
        dt = now + timedelta(days=off)
        rs = fetch_race_list(dt.strftime("%Y%m%d"), "jra")
        if len(rs) >= 6:
            upcoming_days.append((dt, rs, off == 0))
            if len(upcoming_days) >= 2: break

    # 日曜WIN5対象日を最優先で処理し、Gemini 4 Hydrogen枠を確実に確保する
    upcoming_days.sort(key=lambda x: 0 if x[0].weekday() == 6 else 1)
    for dt, rs, is_td in upcoming_days:
        process_kaisai_day(dt.strftime("%Y-%m-%d"), rs, now, is_td, "jra")

    for off in [-1, -2, -3, -4, -5]:
        dt = now + timedelta(days=off)
        rs = fetch_race_list(dt.strftime("%Y%m%d"), "jra")
        if len(rs) >= 6: process_kaisai_day(dt.strftime("%Y-%m-%d"), rs, now, False, "jra"); break

    if not is_weekend_jra_hours:
        for off in [0, -1, 1]:
            dt = now + timedelta(days=off)
            n_races = fetch_race_list(dt.strftime("%Y%m%d"), "nar")
            if len(n_races) >= 3: process_kaisai_day(dt.strftime("%Y-%m-%d"), n_races, now, off == 0, "nar"); break

    update_global_stats(now)
    jra_files = sorted([os.path.basename(p).replace(".json", "") for p in glob.glob("data/20*.json") if not p.endswith("_nar.json")])
    nar_files = sorted([os.path.basename(p).replace(".json", "") for p in glob.glob("data/20*_nar.json")])
    json.dump({"availableDates": jra_files, "narDates": nar_files, "lastSync": now.strftime("%Y-%m-%d %H:%M JST")}, open("data/index.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)

if __name__ == "__main__":
    run_pipeline()
# === END OF FILE ===
