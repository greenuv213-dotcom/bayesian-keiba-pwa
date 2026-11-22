import os, re, math, time, json, glob, socket, requests
from datetime import datetime, timedelta, timezone
from bs4 import BeautifulSoup
from google import genai
from google.genai import types

socket.setdefaulttimeout(45)
START_TS = time.time()
# 10分タイムアウトを絶対に踏まないよう、5分30秒で新規通信を切り上げて確実に保存完了させる
MAX_RUNTIME_SEC = 330

JST = timezone(timedelta(hours=9))
API_KEY = os.environ.get("GEMINI_API_KEY", "").strip()
HIGH_TIER_MODEL = os.environ.get("GEMINI_HIGH_TIER_MODEL", "gemini-4-hydrogen").strip()
FAST_MODEL = os.environ.get("GEMINI_FAST_MODEL", "gemini-3.8-flash").strip()

try:
    client = genai.Client(api_key=API_KEY, http_options=types.HttpOptions(timeout=55000)) if API_KEY else None
except Exception:
    client = genai.Client(api_key=API_KEY) if API_KEY else None

os.makedirs("data", exist_ok=True)

ENGINE_VER = "v11.0-neon"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/124.0.0.0"}
SESSION = requests.Session()
SESSION.headers.update(HEADERS)

JRA_VENUES = {"01":"札幌","02":"函館","03":"福島","04":"新潟","05":"東京","06":"中山","07":"中京","08":"京都","09":"阪神","10":"小倉"}
NAR_VENUES = {"42":"浦和","43":"船橋","44":"大井","45":"川崎","30":"門別","35":"盛岡","36":"水沢","46":"金沢","47":"笠松","48":"名古屋","50":"園田","51":"姫路","54":"高知","55":"佐賀"}
NANKAN_CODES = {"42", "43", "44", "45"}
TOP_RIDERS = ("矢野", "御神本", "笹川", "吉原", "森泰斗", "ルメール", "川田", "戸崎", "坂井", "武豊", "松山", "横山武", "鮫島克", "C.デム", "モレイラ", "レーン", "マーカン")
POWER_SIRES = ("ナダル", "クリソベリル", "ゴールドアリュール", "ルヴァンスレーヴ", "シニスターミニスター", "ヘニーヒューズ", "ドレフォン", "パイロ", "マインドユアビスケッツ", "キズナ", "キタサンブラック", "エピファネイア", "ロードカナロア", "コントレイル", "モーリス")
TURF_START_DIRT = {("東京",1300),("東京",1400),("東京",1600),("中山",1200),("京都",1400),("阪神",1400),("中京",1400),("福島",1150),("新潟",1200)}
GRADED_KEYWORDS = ("Jpn", "G1", "G2", "G3", "S1", "S2", "S3", "杯", "記念", "賞", "マイルCS", "ジャパンC", "有馬", "天皇賞", "ダービー", "オークス", "皐月", "桜花", "菊花", "秋華")

AI_CALL_COUNT = 0
MAX_AI_CALLS_PER_RUN = 3

def log(msg: str):
    print(f"[{int(time.time() - START_TS):03d}s] {msg}", flush=True)

def time_exceeded() -> bool:
    return (time.time() - START_TS) >= MAX_RUNTIME_SEC

def get_soup(url: str) -> BeautifulSoup:
    res = SESSION.get(url, timeout=8)
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
        log(f"[Warn] {mode} list error: {e}")
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

def fetch_full_shutuba(rid: str, mode: str = "jra", need_shutuba: bool = True, need_result: bool = True) -> tuple[str, list, list, str, str, dict]:
    base = "https://race.netkeiba.com" if mode == "jra" else "https://nar.netkeiba.com"
    lines, top3_actual, raw_runners, odds_map = [], [], [], {}
    track_cond, post_time, payouts = "良", "", {}

    if need_shutuba:
        api_path = "api_get_jra_odds.html" if mode == "jra" else "api_get_nar_odds.html"
        try:
            o_json = SESSION.get(f"{base}/api/{api_path}?race_id={rid}&type=1&action=init", timeout=5).json()
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

    if need_result:
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
                elif need_shutuba:
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

def summarize_intraday_track_bias(races: list, venue: str) -> tuple[str, int]:
    """Neon v7.0: 3レース一致ガード付きの当日バイアス集計"""
    finished = [r for r in races if r.get("venue") == venue and r.get("actualTop3")]
    cnt = len(finished)
    if cnt == 0:
        return f"{venue}: 前半確定レースなし（標準バイアス・補正±5%上限）", 0
    inner_w = sum(1 for r in finished if r["actualTop3"][0].get("waku", 4) <= 3)
    outer_w = sum(1 for r in finished if r["actualTop3"][0].get("waku", 4) >= 6)
    if cnt < 3:
        return f"{venue}当日実測({cnt}R参考・3R未満のため±5%上限): 内{inner_w}/外{outer_w}", cnt
    trend = "外枠(6〜8枠)優勢" if outer_w >= inner_w + 2 else ("内枠(1〜3枠)優勢" if inner_w >= outer_w + 2 else "内外フラット")
    return f"{venue}当日実測({cnt}R一致検証済): 1着内枠{inner_w}回/外枠{outer_w}回 → 【{trend}】", cnt

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
    is_streak_riser = (len(ranks) >= 2 and ranks[0] == 1 and ranks[1] == 1)
    return {"style": style, "isLeader": is_leader, "avgRank": avg_rank, "ranks": ranks, "isSilver": is_silver, "hasRebound": has_rebound, "isStreakRiser": is_streak_riser}

def compute_bayesian_full_field(raw_runners: list, race_meta: dict, track_cond: str = "良") -> tuple[list, int, dict, dict]:
    """Neon v7.0: 2-Stage Benter ベイジアン融合 + ソフトクランプ(|ΣΔθ|<=0.45) + 非対称wUsedクランプ"""
    if not raw_runners:
        return [], 3, {"s1": 35, "s2": 40, "s3": 25}, {"wR": 0.35, "m3": 0.0, "coreConnections": [], "counterfactualAudit": ""}

    n = len(raw_runners)
    venue, sdist, mode = race_meta.get("venue", "東京"), race_meta.get("surfaceDist", "ダ1600m"), race_meta.get("mode", "jra")
    is_new = race_meta.get("rank") == "New" or "新馬" in str(race_meta.get("name", ""))
    m_dist = re.search(r"(\d{3,4})", sdist)
    dist = int(m_dist.group(1)) if m_dist else 1600
    is_dirt = ("ダ" in sdist) or (mode == "nar")
    is_turf_start = is_dirt and ((venue, dist) in TURF_START_DIRT)
    is_wet, is_tight = (track_cond in ("重", "不良")), (venue in ("浦和", "川崎", "中山", "福島", "小倉"))

    parsed = [parse_past_metrics(r.get("past", ""), r.get("waku", 4)) for r in raw_runners]
    n_lead = max(1, sum(1 for p in parsed if p["isLeader"]))
    pi_s1, pi_s2, pi_s3 = ((0.25, 0.35, 0.40) if not is_tight else (0.30, 0.35, 0.35)) if n_lead >= 5 else ((0.50, 0.35, 0.15) if n_lead <= 2 else (0.35, 0.40, 0.25))
    scen_w = {"s1": int(pi_s1 * 100), "s2": int(pi_s2 * 100), "s3": int(pi_s3 * 100)}

    has_live_odds = sum(1 for r in raw_runners if r.get("odds", 0) > 1.0) >= max(3, n // 2)
    base_wr = 0.42 if is_new else (0.35 if mode == "jra" else 0.38)

    fund_logits, place_deltas, notes, styles, clamp_flags = [], [], [], [], []

    for idx, r in enumerate(raw_runners):
        waku, jockey, wt, sex_age, futan, ped = r.get("waku", 4), r.get("jockey", ""), r.get("weight", ""), r.get("sexAge", ""), r.get("futan", ""), r.get("pedigree", "")
        pm, style = parsed[idx], parsed[idx]["style"]
        odd = float(r.get("odds", 0))

        # Stage 1: オッズ非依存基礎モデル（未出走新馬で成績皆無時のみ枠・騎手・血統ベース）
        if is_new:
            base_theta = 0.0
        else:
            win_bonus = 0.45 if (pm["ranks"] and pm["ranks"][0] == 1) else (0.25 if (pm["ranks"] and pm["ranks"][0] <= 3) else 0.0)
            base_theta = -0.26 * (pm["avgRank"] - 6.0) + win_bonus

        delta_th, delta_pl, reasons, is_hazard = 0.0, 0.0, [], False
        m_ft = re.search(r"(\d{2}\.?\d?)", str(futan))
        ft_val = float(m_ft.group(1)) if m_ft else 56.0
        if "3" in sex_age and ft_val <= 55.0: delta_th += 0.14; delta_pl += 0.10; reasons.append(f"F:3歳{ft_val}kg(H:軽量)")
        elif ft_val >= 58.0: delta_th -= 0.12; delta_pl -= 0.08; reasons.append(f"F:斤量{ft_val}kg(H:酷量)")

        # ダート新馬1-2枠未経験砂被りハザード / 芝発進ダート物理
        if is_new and is_dirt and waku <= 2:
            delta_th -= 0.28; delta_pl -= 0.14; is_hazard = True; reasons.append(f"F:ダ新馬{waku}枠(H:砂被り危)")
        elif is_turf_start:
            if waku >= 7 and style in ("逃", "先"): delta_th += 0.18; delta_pl += 0.12; reasons.append(f"F:芝発進{waku}枠先行(H:外加速)")
            elif waku <= 2 and style != "逃": delta_th -= 0.14; delta_pl -= 0.10; is_hazard = True; reasons.append(f"F:芝発進{waku}枠(H:砂被り警戒)")

        m_bw = re.search(r"(\d{3})\(([+-]?\d+)\)", wt)
        body_w, diff_w = (int(m_bw.group(1)), int(m_bw.group(2))) if m_bw else (480, 0)
        if dist >= 1800 and diff_w >= 12:
            delta_th -= 0.20; delta_pl -= 0.14; is_hazard = True; reasons.append(f"F:馬体+{diff_w}kg(H:TypeII減点)")
        elif is_wet and is_dirt and waku >= 6 and body_w >= 500 and style in ("逃", "先"):
            delta_th += 0.16; delta_pl += 0.12; reasons.append(f"F:{waku}枠{body_w}kg(H:道悪外枠大型)")
        elif -8 <= diff_w <= -2:
            delta_th += 0.08; reasons.append(f"F:馬体{diff_w}kg絞り(H:好仕上)")

        # 3〜4歳ダート連勝中昇級馬ルール
        if is_dirt and pm["isStreakRiser"] and ("3" in sex_age or "4" in sex_age):
            delta_th += 0.14; delta_pl += 0.10; reasons.append("F:ダ連勝昇級(H:Riser加点)")
        if pm["isSilver"]:
            delta_th -= 0.10; delta_pl += 0.18; reasons.append("F:2・3着連続(H:安定Connector)")
        elif pm["hasRebound"]:
            delta_th += 0.16; delta_pl += 0.12; reasons.append("F:0.2s差実績(H:巻き返し)")
        if any(tr in jockey for tr in TOP_RIDERS):
            delta_th += 0.16; delta_pl += 0.14; reasons.append(f"F:{jockey[:4]}騎手(H:Top騎手)")
        if any(s in ped for s in POWER_SIRES):
            delta_th += 0.10; reasons.append(f"F:{ped[:10]}(H:血統適性)")

        scen_shift = (0.12 * pi_s1 - 0.08 * pi_s3) if style in ("逃", "先") else (-0.08 * pi_s1 + 0.14 * pi_s3)
        # Neon v7.0: 総シフト幅ソフトクランプ |ΣΔθ| <= 0.45, δ_place ∈ [-0.30, +0.25]
        clamped_th = max(-0.45, min(0.45, delta_th + scen_shift))
        clamped_pl = max(-0.30, min(0.25, delta_pl))

        if not reasons: reasons.append(f"F:{waku}枠・近走平均{pm['avgRank']:.1f}着")
        fund_logits.append(base_theta + clamped_th)
        place_deltas.append(clamped_pl)
        notes.append(" / ".join(reasons)[:46])
        styles.append(style)
        clamp_flags.append(is_hazard)

    # Stage 1 基礎勝率 fFund
    max_fl = max(fund_logits)
    w_fund = [math.exp((x - max_fl) * 1.05) for x in fund_logits]
    f_fund_probs = [x / sum(w_fund) * 100.0 for x in w_fund]

    # FLB Power De-vigged 市場確率 q
    final_odds = [
        round(float(r["odds"]), 1) if (has_live_odds and r.get("odds", 0) > 1.0)
        else round(max(1.5, min(99.9, 80.0 / max(0.8, f_fund_probs[i]))), 1)
        for i, r in enumerate(raw_runners)
    ]
    inv_power = [math.pow(max(1.1, o), -1.10) for o in final_odds]
    q_probs = [x / sum(inv_power) * 100.0 for x in inv_power]

    # Stage 2: 2-Stage Benter ベイジアン融合 (θ_post = (1-w)*θ_fund + w*ln(q))
    post_logits, w_used_list = [], []
    for i in range(n):
        w_i = (0.10 if is_new else 0.15) if clamp_flags[i] else (base_wr if has_live_odds else 0.0)
        w_used_list.append(round(w_i, 2))
        ln_q = math.log(max(0.001, q_probs[i] / 100.0))
        ln_f = math.log(max(0.001, f_fund_probs[i] / 100.0))
        post_logits.append((1.0 - w_i) * ln_f + w_i * ln_q)

    max_pl = max(post_logits)
    w_post = [math.exp(x - max_pl) for x in post_logits]
    f_probs = [x / sum(w_post) * 100.0 for x in w_post]

    # Stage-Adjusted Top2 / Top3（保存則 200% / 300%）
    w2 = [math.exp((post_logits[i] + place_deltas[i]) - max_pl) for i in range(n)]
    p2_raw = [0.46 * f_probs[i] + 0.54 * (w2[i] / sum(w2) * 100.0) for i in range(n)]
    top2_probs = [min(92.0, x * (200.0 / max(1.0, sum(p2_raw)))) for x in p2_raw]
    top3_probs = [min(96.0, x * (300.0 / max(1.0, sum(top2_probs)))) for x in top2_probs]

    # 融合後3着内率＆突破力の総合順で印選定（◎は安全軸）
    order = sorted(range(n), key=lambda i: (f_probs[i] * 0.55 + top3_probs[i] * 0.45), reverse=True)
    if len(order) >= 2 and (parsed[order[0]]["isSilver"] or clamp_flags[order[0]]):
        order[0], order[1] = order[1], order[0]

    marks_map, roles_map = {}, {}
    for rk, i in enumerate(order):
        gap = f_probs[i] - q_probs[i]
        if clamp_flags[i] and q_probs[i] >= 14.0:
            marks_map[i], roles_map[i] = ("危" if is_new else "消"), "過剰人気ハザード"
        elif rk == 0: marks_map[i], roles_map[i] = "◎", "最安定Top-3軸"
        elif rk == 1: marks_map[i], roles_map[i] = "◯", "融合上位強制結線"
        elif rk == 2: marks_map[i], roles_map[i] = "▲", "安定Connector"
        elif rk == 3 or (rk <= 5 and (gap >= 2.0 or parsed[i]["hasRebound"] or parsed[i]["isStreakRiser"])):
            marks_map[i], roles_map[i] = "☆", "展開・連勝特注穴"
        elif rk <= 6: marks_map[i], roles_map[i] = "△", "3列目連下"
        elif q_probs[i] >= 12.0 and gap <= -3.5: marks_map[i], roles_map[i] = "危", "過剰人気警戒"
        elif rk >= n - 2: marks_map[i], roles_map[i] = "消", "時計・展開劣勢"
        else: marks_map[i], roles_map[i] = "無", "強調材料乏しい"

    horses_out = [{
        "mark": marks_map[i], "role": roles_map[i], "num": raw_runners[i]["num"], "name": raw_runners[i]["name"],
        "style": styles[i],
        "f": round(f_probs[i], 1), "fFund": round(f_fund_probs[i], 1),
        "q": round(q_probs[i], 1), "wUsed": w_used_list[i],
        "top2": round(top2_probs[i], 1), "top3": round(top3_probs[i], 1),
        "odds": final_odds[i], "comment": notes[i]
    } for i in order]

    # Neonメタ指標: M3集中度・◎強制結線・反実仮想セルフ監査
    top3_sorted_f = sorted([h["f"] for h in horses_out], reverse=True)
    m3_val = round(sum(top3_sorted_f[:3]), 1)
    safe_nodes = [h for h in horses_out if h["mark"] not in ("危", "消", "無")]
    conns = []
    if len(safe_nodes) >= 3:
        n1, n2, n3 = safe_nodes[0]["num"], safe_nodes[1]["num"], safe_nodes[2]["num"]
        conns = [[n1, n2], [n1, n3], [n2, n3]]
        if len(safe_nodes) >= 4:
            conns.append([n1, safe_nodes[3]["num"]])
    faded = next((h for h in horses_out if h["mark"] in ("危", "消") and h["q"] >= 10.0), None)
    cf_audit = (
        f"◎{safe_nodes[0]['num']}番破綻時は◯{safe_nodes[1]['num']}-▲{safe_nodes[2]['num']}のCore結線で元返し防衛。"
        if len(safe_nodes) >= 3 else "上位3頭のCore結線で防衛。"
    )
    if faded:
        cf_audit += f" 危険視{faded['num']}番は単騎楽逃げ時のみ復活。"

    neon_meta = {
        "wR": base_wr, "m3": m3_val, "coreConnections": conns,
        "portfolioRules": {"coreRatio": 0.75, "dutchTargetReturn": 11800, "singleLongshotCapPct": 0.30},
        "counterfactualAudit": cf_audit,
        "strategyProfile": "hit_rate_max"
    }
    return horses_out, n_lead, scen_w, neon_meta

def build_neon_core_shield_specs(race: dict, B: int = 10000) -> tuple[list, dict]:
    """Neon v7.0 的中率最大化 Core Shield (75% Drop-Buffered 11,800円ダッチング + ◎強制結線 + 穴30%上限) + Alpha (25%)"""
    horses = race.get("horses") or []
    sorted_h = sorted(horses, key=lambda x: (float(x.get("f", 0)) * 0.55 + float(x.get("top3", 0)) * 0.45), reverse=True)
    valid = [h for h in sorted_h if h.get("mark") not in ("消", "危", "無")]
    pool = valid if len(valid) >= 4 else [h for h in sorted_h if h.get("mark") != "消"]
    if len(pool) < 3: pool = sorted_h
    h1, h2, h3 = pool[0], pool[1], pool[2]
    h4 = pool[3] if len(pool) > 3 else h3
    himos = [h for h in sorted_h if h["num"] not in (h1["num"], h2["num"], h3["num"], h4["num"]) and h.get("mark") != "消"][:3]

    o1 = max(1.5, float(h1.get("odds", 4.5)))
    o2 = max(1.8, float(h2.get("odds", 6.0)))
    o3 = max(1.8, float(h3.get("odds", 7.5)))
    o4 = max(2.2, float(h4.get("odds", 10.0)))

    # Core Shield 75%: ◎×{○,▲,△1}強制結線 + ○-▲タテ目防衛 を11,800円目標でダッチング
    core_budget = int(round((B * 0.75) / 100) * 100)
    alpha_budget = max(500, B - core_budget)
    target_ret = 1.18 * B
    max_longshot = int(B * 0.30)

    core_pairs = [
        ("wide", [h1["num"], h2["num"]], max(1.8, round(math.sqrt(o1 * o2) * 0.62, 1)), f"ワイド {h1['num']}-{h2['num']} (◎-◯ Core)", o1 >= 10 or o2 >= 10),
        ("wide", [h1["num"], h3["num"]], max(2.1, round(math.sqrt(o1 * o3) * 0.68, 1)), f"ワイド {h1['num']}-{h3['num']} (◎-▲ Core)", o1 >= 10 or o3 >= 10),
        ("wide", [h2["num"], h3["num"]], max(2.4, round(math.sqrt(o2 * o3) * 0.72, 1)), f"ワイド {h2['num']}-{h3['num']} (◯-▲ 防衛)", o2 >= 10 or o3 >= 10),
    ]
    if h4["num"] != h3["num"]:
        core_pairs.append(("wide", [h1["num"], h4["num"]], max(2.6, round(math.sqrt(o1 * o4) * 0.75, 1)), f"ワイド {h1['num']}-{h4['num']} (◎-☆ 強制結線)", o1 >= 10 or o4 >= 10))

    raw_w = [target_ret / p[2] for p in core_pairs]
    sum_rw = max(1.0, sum(raw_w))
    specs = []
    used_core = 0
    for idx, (tk, nums, est_o, label, is_ls) in enumerate(core_pairs):
        amt = max(100, int(round((raw_w[idx] / sum_rw * core_budget) / 100) * 100))
        if is_ls: amt = min(amt, max_longshot)
        specs.append({"poolKey": tk, "nums": nums, "amt": amt, "label": label, "zone": "Core"})
        used_core += amt
    if used_core != core_budget and specs:
        diff = core_budget - used_core
        if specs[0]["amt"] + diff >= 100:
            specs[0]["amt"] += diff

    # Alpha 25%: 馬連◎-◯, 馬連◎-▲, コンパクト3連複F
    row1 = [h1["num"], h2["num"]]
    row2 = sorted({h2["num"], h3["num"]})
    row3 = sorted({h3["num"], h4["num"]} | {x["num"] for x in himos})
    trio_set = {tuple(sorted((a, b, c))) for a in row1 for b in row2 if a != b for c in row3 if c != a and c != b}
    trio_pts = max(1, len(trio_set))
    trio_amt = min(max(300, alpha_budget - 600), trio_pts * 100)
    rem_alpha = max(200, alpha_budget - trio_amt)
    u12 = max(100, int(round((rem_alpha * 0.58) / 100) * 100))
    u13 = max(100, rem_alpha - u12)

    specs.append({"poolKey": "umaren", "nums": [h1["num"], h2["num"]], "amt": u12, "label": f"馬連 {h1['num']}-{h2['num']} (◎-◯ Alpha)", "zone": "Alpha"})
    specs.append({"poolKey": "umaren", "nums": [h1["num"], h3["num"]], "amt": u13, "label": f"馬連 {h1['num']}-{h3['num']} (◎-▲ Alpha)", "zone": "Alpha"})
    trio_meta = {"trioSet": trio_set, "trioPts": trio_pts, "trioAmt": trio_amt}
    return specs, trio_meta

def evaluate_10k_payout(race: dict) -> dict:
    payouts, horses = race.get("payouts") or {}, race.get("horses") or []
    if not payouts or len(horses) < 3 or race.get("rank") == "Pass": return {}
    B = 10000
    specs, trio_meta = build_neon_core_shield_specs(race, B=B)
    total_ret, hit_labels = 0, []
    for sp in specs:
        tk, nums, amt, label = sp["poolKey"], sp["nums"], sp["amt"], sp["label"]
        for entry in payouts.get(tk, []):
            if (entry["nums"] == nums if tk in ("win", "umatan") else sorted(entry["nums"]) == sorted(nums)):
                pay_yen = int((amt // 100) * entry["pay"])
                total_ret += pay_yen
                hit_labels.append(f"{label} ({pay_yen:,}円)")
    per_pt = max(100, (trio_meta["trioAmt"] // trio_meta["trioPts"]) // 100 * 100)
    for entry in payouts.get("sanrenpuku", []):
        if tuple(sorted(entry["nums"])) in trio_meta["trioSet"]:
            pay_yen = int((per_pt // 100) * entry["pay"])
            total_ret += pay_yen
            hit_labels.append(f"3連複F ({pay_yen:,}円)")
    return {"investedYen": B, "returnYen": total_ret, "actualRoi": round(total_ret * 100.0 / B, 1), "isHit": total_ret > 0, "hitTickets": hit_labels}

def classify_race_tier(r: dict) -> str:
    if r.get("rank") == "New":
        return "med_h"
    if r.get("rank") == "S" or r.get("raceNumber") == 11 or any(g in r.get("name", "") for g in GRADED_KEYWORDS):
        return "high_h"
    return "flash"

def call_gemini(skill: str, prompt: str, tier: str = "flash") -> dict:
    global AI_CALL_COUNT
    if not client or AI_CALL_COUNT >= MAX_AI_CALLS_PER_RUN or time_exceeded():
        return {}
    AI_CALL_COUNT += 1
    p = f"skills/{skill}/SKILL.md"
    sys_inst = open(p, "r", encoding="utf-8").read() if os.path.exists(p) else "Output valid JSON only."

    # 廃止された gemini-2.5-flash は削除し、Hydrogen + 3.8-Flash の2モデル無料枠ハイブリッドへ統一
    if tier == "high_h":
        candidates = [(HIGH_TIER_MODEL, "HIGH"), (FAST_MODEL, "MEDIUM")]
    elif tier == "med_h":
        candidates = [(HIGH_TIER_MODEL, "MEDIUM"), (FAST_MODEL, "MEDIUM")]
    else:
        candidates = [(FAST_MODEL, "MEDIUM"), (HIGH_TIER_MODEL, "MEDIUM")]

    for m, think_lvl in candidates:
        if time_exceeded():
            log("Time cap reached during AI fallback; stopping cleanly.")
            return {}
        try:
            log(f"Calling AI: {skill} -> {m}({think_lvl})")
            time.sleep(2)
            try:
                cfg = types.GenerateContentConfig(
                    system_instruction=sys_inst,
                    response_mime_type="application/json",
                    thinking_config=types.ThinkingConfig(thinking_level=think_lvl),
                )
            except Exception:
                cfg = types.GenerateContentConfig(system_instruction=sys_inst, response_mime_type="application/json")

            res = client.models.generate_content(model=m, contents=prompt, config=cfg)
            data = json.loads(re.sub(r"^```(?:json)?\s*|\s*```$", "", (res.text or "").strip(), flags=re.DOTALL))
            data["usedModel"] = f"{m}({think_lvl})"
            log(f"[AI Success] {skill} -> {data['usedModel']}")
            return data
        except Exception as e:
            log(f"[Fallback] {m}: {str(e)[:120]}")
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

def fetch_official_win5_payout(target_race_ids: list) -> int:
    try:
        soup = get_soup("https://race.netkeiba.com/top/win5.html")
        page_ids = re.findall(r"race_id=(\d{12})", str(soup))
        if target_race_ids and not any(rid in page_ids for rid in target_race_ids):
            return 0
        txt = soup.get_text(" ", strip=True)
        m = re.search(r"(?:払戻金|配当)[^\d]{0,15}([\d,]{3,12})\s*円", txt)
        if m:
            val = int(m.group(1).replace(",", ""))
            if val >= 100: return val
    except Exception: pass
    return 0

def sync_multileg_results(day_db: dict, mode: str):
    ml = day_db.get("multiLeg")
    if not isinstance(ml, dict) or not isinstance(ml.get("legs"), list):
        return
    races = day_db.get("races") or []
    by_id = {r.get("raceId"): r for r in races if r.get("raceId")}
    by_vlabel = {r.get("venueLabel"): r for r in races if r.get("venueLabel")}

    finished, leg_rids = 0, []
    for leg in ml["legs"]:
        r = by_id.get(leg.get("raceId")) or by_vlabel.get(leg.get("venue")) or next((x for x in races if x.get("name") == leg.get("name")), None)
        if not r: continue
        leg["raceId"] = r.get("raceId", leg.get("raceId", ""))
        if r.get("postTime"): leg["postTime"] = r["postTime"]
        if leg["raceId"]: leg_rids.append(leg["raceId"])
        if r.get("actualTop3"):
            leg["actualTop3"] = r["actualTop3"]
            leg["actualWinner"] = r["actualTop3"][0]
            finished += 1
    ml["finishedLegs"] = finished
    if mode == "jra" and finished == len(ml["legs"]) and finished == 5 and not ml.get("officialPayout"):
        pay = fetch_official_win5_payout(leg_rids)
        if pay > 0: ml["officialPayout"] = pay

def build_multileg_with_ai(races: list, mode: str, date_str: str) -> dict:
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

    all_finished = all(bool(r.get("actualTop3")) for r in selected)
    if mode == "jra" and len(selected) == 5 and not all_finished and not time_exceeded():
        blocks = []
        for idx, r in enumerate(selected):
            h_txt = "\n".join([f" {h['num']}番{h['name']}(脚質:{h['style']} 単勝:{h['odds']}倍 {h['comment']})" for h in r["horses"][:16]])
            blocks.append(f"=== Leg{idx+1} {r['venueLabel']} {r['name']} ({r['surfaceDist']} 発走{r.get('postTime','')}) ===\n{h_txt}")
        w_prompt = (
            f"日付:{date_str} のJRA WIN5対象5レースを Neon v11.1（2-Stage Benter融合・乾燥ダート上位4頭差し枠・来日外国馬wR=0.55-0.60・Plan C確率シェル）で一括推論し、以下のJSONスキーマで出力せよ:\n"
            "{\"summary\":\"5レース全体の攻略総括(100字以内)\",\"legs\":[{\"leg\":1,\"venue\":\"会場R\",\"name\":\"レース名\",\"postTime\":\"HH:MM\",\"wR\":0.40,\"typeBPlus\":true/false,\"note\":\"展開・バイアス見解(45字以内)\",\"horses\":[{\"num\":馬番,\"name\":\"馬名\",\"f\":融合勝率,\"fFund\":基礎勝率,\"q\":市場確率,\"odds\":オッズ,\"shell\":\"Core|Wing\",\"note\":\"F/H根拠(30字以内)\"}]}],\"hedges\":[{\"num\":馬番,\"name\":\"Leg5伏兵名\",\"odds\":オッズ,\"hedge50k\":円,\"hedge100k\":円}]}\n\n"
            + "\n".join(blocks)
        )
        ai_w = call_gemini("app-bayesian-win5", w_prompt, tier="high_h")
        if isinstance(ai_w, dict) and isinstance(ai_w.get("legs"), list) and len(ai_w["legs"]) == 5:
            ai_w["predicted"] = True; ai_w["aiPredicted"] = True; ai_w["date"] = date_str; ai_w["engineVer"] = ENGINE_VER
            for idx, r in enumerate(selected):
                leg_obj = ai_w["legs"][idx]
                leg_obj["raceId"], leg_obj["venue"], leg_obj["name"] = r["raceId"], r["venueLabel"], r["name"]
                leg_obj["postTime"] = r.get("postTime", leg_obj.get("postTime", ""))
                by_num = {int(h["num"]): h for h in leg_obj.get("horses", []) if str(h.get("num","")).isdigit()}
                if by_num:
                    for h in r["horses"]:
                        if h["num"] in by_num:
                            ah = by_num[h["num"]]
                            if ah.get("f"): h["f"] = round(float(ah["f"]), 1)
                            if ah.get("fFund"): h["fFund"] = round(float(ah["fFund"]), 1)
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
                    r["usedModel"] = ai_w.get("usedModel", f"{HIGH_TIER_MODEL}(HIGH)")
                    if leg_obj.get("note"): r["scenario"] = leg_obj["note"]
                    if leg_obj.get("wR"): r["wR"] = leg_obj["wR"]
            return ai_w

    legs = []
    for idx, r in enumerate(selected):
        hs = sorted(r["horses"], key=lambda x: float(x.get("f", 10)), reverse=True)
        legs.append({
            "leg": idx + 1, "raceId": r["raceId"], "venue": r["venueLabel"], "name": r["name"], "cond": r["surfaceDist"],
            "postTime": r.get("postTime", ""), "wR": r.get("wR", 0.35),
            "typeBPlus": (float(hs[0].get("f", 25)) < 25.5 or r.get("nLead", 3) >= 4),
            "note": r.get("scenario", "")[:55],
            "horses": [{
                "num": h.get("num", 1), "name": h.get("name", "有力馬"),
                "f": float(h.get("f", 15)), "fFund": float(h.get("fFund", h.get("f", 15))),
                "q": float(h.get("q", 10)), "odds": float(h.get("odds", 5.5)),
                "note": h.get("comment", "")[:34]
            } for h in hs[:7]]
        })
    last_hs = legs[-1]["horses"][2:4]
    hedges = [{"num": h["num"], "name": f"{legs[-1]['venue']} {h['name']}", "odds": h["odds"], "hedge50k": int((50000 / max(1.5, h["odds"]) + 99) // 100 * 100), "hedge100k": int((100000 / max(1.5, h["odds"]) + 99) // 100 * 100)} for h in last_hs]
    return {"predicted": True, "aiPredicted": False, "date": date_str, "engineVer": ENGINE_VER, "summary": f"【{date_str} Neon v11.0 2-Stage融合編成（{'トリプル馬単50円単位' if mode=='nar' else 'JRA WIN5 Plan A/B/C対応'}）】", "legs": legs, "hedges": hedges}

def should_check_result(date_str: str, post_time: str, now: datetime) -> bool:
    today_str = now.strftime("%Y-%m-%d")
    if date_str < today_str: return True
    if date_str > today_str: return False
    if re.match(r"^\d{2}:\d{2}$", post_time or ""):
        pdt = datetime.strptime(f"{date_str} {post_time}", "%Y-%m-%d %H:%M").replace(tzinfo=JST)
        return now >= (pdt + timedelta(minutes=5))
    return now.hour >= 10

def process_kaisai_day(date_str: str, races: list, now: datetime, is_today: bool, mode: str = "jra"):
    log(f"Processing {date_str} ({mode}, {len(races)} races)")
    suffix = "_nar" if mode == "nar" else ""
    db_path = f"data/{date_str}{suffix}.json"
    day_db = json.load(open(db_path, "r", encoding="utf-8")) if os.path.exists(db_path) else {"date": date_str, "mode": mode, "races": races}
    if not day_db.get("races") and races: day_db["races"] = races
    day_db["mode"] = mode

    dt = datetime.strptime(date_str, "%Y-%m-%d")
    if mode == "jra" and dt.weekday() != 6:
        day_db.pop("multiLeg", None)

    for r in day_db.get("races", []):
        if time_exceeded():
            log("Time cap reached in scraping loop; saving progress.")
            break
        has_real = isinstance(r.get("horses"), list) and len(r["horses"]) >= 5
        has_neon = has_real and ("fFund" in r["horses"][0])
        bad_time = (not r.get("postTime")) or (r.get("postTime") == "15:00" and r.get("raceNumber", 11) < 10)
        can_have_result = should_check_result(date_str, r.get("postTime", ""), now)
        need_res = can_have_result and ((not r.get("evalDone")) or (not r.get("actualTop3")))
        need_sh = (not has_real) or bad_time or (not has_neon and not r.get("actualTop3"))

        if not need_sh and not need_res:
            continue

        detail, actual, raw_runners, track_cond, ptime, payouts = fetch_full_shutuba(r["raceId"], mode=mode, need_shutuba=need_sh, need_result=need_res)
        if ptime: r["postTime"] = ptime
        if raw_runners and need_sh:
            base_horses, n_lead, scen_w, neon_meta = compute_bayesian_full_field(raw_runners, r, track_cond=track_cond)
            r["nLead"], r["trackCond"], r["scenarioWeights"] = n_lead, track_cond, scen_w
            if not has_real or not r.get("aiPredicted"):
                r["horses"] = base_horses
                r["predicted"] = True
                r.update(neon_meta)
                r["scenario"] = f"{r['venueLabel']}({r['surfaceDist']}・{track_cond}) 実測N_lead={n_lead}頭 / 2-Stage融合(wR={neon_meta['wR']}, M3={neon_meta['m3']}%)。3シナリオ混合(S1:{scen_w['s1']}% / S2:{scen_w['s2']}% / S3:{scen_w['s3']}%)で全{len(base_horses)}頭を厳密演算。"
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
    if ((mode == "jra" and dt.weekday() == 6) or mode == "nar") and not time_exceeded():
        cur_ml = day_db.get("multiLeg") or {}
        need_ml_ai = (not cur_ml.get("aiPredicted")) or (cur_ml.get("engineVer") != ENGINE_VER and "hydrogen" not in str(cur_ml.get("usedModel", "")))
        if need_ml_ai:
            mleg = build_multileg_with_ai(day_db.get("races", []), mode, date_str)
            if mleg: day_db["multiLeg"] = mleg

    # 2. 未発走の勝負レースへ Neon v7.0 ハイブリッドAI本推論を適用
    ai_candidates = []
    for r in day_db.get("races", []):
        if not r.get("horses") or r.get("actualTop3") or r.get("rank") == "Pass":
            continue
        if not (r.get("rank") in ("S", "A", "New") or r.get("raceNumber") in (12, 11, 10, 9, 5)):
            continue
        tier = classify_race_tier(r)
        used = str(r.get("usedModel", ""))
        needs_ai = (not r.get("aiPredicted")) or (tier in ("high_h", "med_h") and "hydrogen" not in used)
        if not needs_ai:
            continue
        prio = 0 if tier == "high_h" else (1 if tier == "med_h" else 2)
        if is_today and re.match(r"^\d{2}:\d{2}$", r.get("postTime", "")):
            pdt = datetime.strptime(f"{date_str} {r['postTime']}", "%Y-%m-%d %H:%M").replace(tzinfo=JST)
            mins = (pdt - now).total_seconds() / 60.0
            if 15 <= mins <= 95: prio -= 10
        ai_candidates.append((prio, tier, r))

    ai_candidates.sort(key=lambda x: x[0])
    for _, tier, r in ai_candidates[:2]:
        if AI_CALL_COUNT >= MAX_AI_CALLS_PER_RUN or time_exceeded(): break
        bias_info, bias_cnt = summarize_intraday_track_bias(day_db.get("races", []), r["venue"])
        detail = r.pop("detailText", "") or "\n".join([f"{h['num']}番{h['name']}(脚質:{h['style']} 単勝:{h['odds']}倍 {h['comment']})" for h in r["horses"]])
        pred = call_gemini(
            r["skill"],
            f"【モード: 標準（Neon v7.0 的中率最大化・全頭評価）】日付:{date_str} {r['venueLabel']} {r['name']} ({r['surfaceDist']}・{r.get('trackCond','良')})\n"
            f"【当日バイアス(3R一致ガード)】{bias_info}\n"
            f"全頭について mark, role, style, f(2-Stage融合後勝率), fFund(オッズ遮断基礎勝率), wUsed(個別融合重み), top2, top3, comment(35字以内) と、"
            f"scenario, pivotType, rank, wR, m3, hitRate, breakEvenRate, expectedRoi, coreConnections([[◎番,◯番],...]), counterfactualAudit(60字以内) をJSON出力せよ:\n{detail}",
            tier=tier,
        )
        if isinstance(pred, dict) and "horses" in pred:
            by_name = {h["name"]: h for h in r["horses"]}
            for ah in pred["horses"]:
                t = by_name.get(ah.get("name")) or next((x for x in r["horses"] if str(x["num"]) == str(ah.get("num"))), None)
                if t:
                    for k in ("mark", "role", "style", "comment"):
                        if ah.get(k): t[k] = ah[k]
                    for k in ("f", "fFund", "top2", "top3"):
                        if ah.get(k) is not None: t[k] = round(float(ah[k]), 1)
                    if ah.get("wUsed") is not None: t["wUsed"] = round(float(ah["wUsed"]), 2)
            sf = max(1.0, sum(float(x["f"]) for x in r["horses"]))
            s2 = max(1.0, sum(float(x["top2"]) for x in r["horses"]))
            s3 = max(1.0, sum(float(x["top3"]) for x in r["horses"]))
            for x in r["horses"]:
                x["f"] = round(float(x["f"]) * 100.0 / sf, 1)
                x["top2"] = round(min(94.0, float(x["top2"]) * 200.0 / s2), 1)
                x["top3"] = round(min(97.0, float(x["top3"]) * 300.0 / s3), 1)
                x.setdefault("fFund", x["f"])
            r["horses"].sort(key=lambda x: float(x["f"]), reverse=True)
            for k in ("scenario", "pivotType", "rank", "usedModel", "wR", "m3", "hitRate", "breakEvenRate", "expectedRoi", "coreConnections", "portfolioRules", "counterfactualAudit", "strategyProfile"):
                if k in pred and pred[k] is not None:
                    r[k] = pred[k]
            r["intradayBiasConsistentR"] = bias_cnt
            r.setdefault("strategyProfile", "hit_rate_max")
            if "m3" not in r:
                r["m3"] = round(sum(float(x["f"]) for x in r["horses"][:3]), 1)
            r["aiPredicted"] = True

    sync_multileg_results(day_db, mode)

    for r in day_db.get("races", []): r.pop("detailText", None)
    venues = sorted(list({r["venue"] for r in day_db.get("races", [])}))
    day_db["trackBiases"] = []
    for v in venues:
        b_txt, b_cnt = summarize_intraday_track_bias(day_db.get("races", []), v)
        day_db["trackBiases"].append({"venue": v, "surf": f"Neon v7.0・実配当照合済", "trend": b_txt, "consistentR": b_cnt})
    day_db["engineVer"] = ENGINE_VER
    day_db["updatedAt"] = now.strftime("%Y-%m-%d %H:%M JST")
    json.dump(day_db, open(db_path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    log(f"Saved {db_path}")

def empty_scope_stats() -> dict:
    return {
        "races": 0, "hits": 0, "invest": 0, "ret": 0, "passCount": 0, "passSaved": 0,
        "byRank": {rk: {"races": 0, "hits": 0, "invest": 0, "ret": 0} for rk in ("S", "A", "New", "B")}
    }

def update_global_stats(now: datetime):
    scopes = {"all": empty_scope_stats(), "jra": empty_scope_stats(), "nar": empty_scope_stats()}
    recent = []
    for fp in sorted(glob.glob("data/20*.json"), reverse=True):
        try:
            d = json.load(open(fp, "r", encoding="utf-8"))
            is_nar = d.get("mode") == "nar" or fp.endswith("_nar.json")
            mode_key = "nar" if is_nar else "jra"
            for r in d.get("races", []):
                rk_raw = r.get("rank", "B")
                if rk_raw == "Pass":
                    for sk in ("all", mode_key):
                        scopes[sk]["passCount"] += 1
                        scopes[sk]["passSaved"] += 10000
                elif r.get("evalDone") and r.get("investedYen"):
                    rk = rk_raw if rk_raw in ("S", "A", "New", "B") else "B"
                    inv, ret = int(r["investedYen"]), int(r.get("returnYen", 0))
                    is_hit = ret > 0
                    for sk in ("all", mode_key):
                        b = scopes[sk]
                        b["races"] += 1; b["invest"] += inv; b["ret"] += ret
                        if is_hit: b["hits"] += 1
                        rb = b["byRank"][rk]
                        rb["races"] += 1; rb["invest"] += inv; rb["ret"] += ret
                        if is_hit: rb["hits"] += 1
                    if len(recent) < 40:
                        recent.append({
                            "date": d.get("date", ""), "mode": mode_key, "rank": rk,
                            "race": f"{r['venueLabel']} {r['name']}",
                            "status": r.get("resultStatus", ""),
                            "roi": float(r.get("actualRoi", 0)),
                            "returnYen": ret, "investedYen": inv, "isHit": is_hit,
                            "hits": r.get("hitTickets", [])
                        })
        except Exception: pass
    payload = {"updatedAt": now.strftime("%Y-%m-%d %H:%M JST"), **scopes, "recentResults": recent}
    json.dump(payload, open("data/stats.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    log("Updated data/stats.json")

def run_pipeline():
    now = datetime.now(JST)
    log(f"Pipeline start ({ENGINE_VER}) at {now.strftime('%Y-%m-%d %H:%M JST')}")
    is_weekend = now.weekday() in (5, 6)
    is_weekend_jra_hours = is_weekend and (8 <= now.hour < 17)

    upcoming_days = []
    for off in [0, 1, 2, 3, 4, 5]:
        dt = now + timedelta(days=off)
        rs = fetch_race_list(dt.strftime("%Y%m%d"), "jra")
        if len(rs) >= 6:
            upcoming_days.append((dt, rs, off == 0))
            if len(upcoming_days) >= 2: break

    upcoming_days.sort(key=lambda x: 0 if x[0].weekday() == 6 else 1)
    for dt, rs, is_td in upcoming_days:
        if time_exceeded(): break
        process_kaisai_day(dt.strftime("%Y-%m-%d"), rs, now, is_td, "jra")

    for off in [-1, -2, -3, -4, -5]:
        if time_exceeded(): break
        dt = now + timedelta(days=off)
        rs = fetch_race_list(dt.strftime("%Y%m%d"), "jra")
        if len(rs) >= 6:
            process_kaisai_day(dt.strftime("%Y-%m-%d"), rs, now, False, "jra")
            break

    if not is_weekend_jra_hours and not time_exceeded():
        for off in [0, -1, 1]:
            if time_exceeded(): break
            dt = now + timedelta(days=off)
            n_races = fetch_race_list(dt.strftime("%Y%m%d"), "nar")
            if len(n_races) >= 3:
                process_kaisai_day(dt.strftime("%Y-%m-%d"), n_races, now, off == 0, "nar")
                break

    update_global_stats(now)
    jra_files = sorted([os.path.basename(p).replace(".json", "") for p in glob.glob("data/20*.json") if not p.endswith("_nar.json")])
    nar_files = sorted([os.path.basename(p).replace(".json", "") for p in glob.glob("data/20*_nar.json")])
    json.dump({"availableDates": jra_files, "narDates": nar_files, "lastSync": now.strftime("%Y-%m-%d %H:%M JST")}, open("data/index.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    log("Pipeline finished successfully.")

if __name__ == "__main__":
    run_pipeline()
# === END OF FILE ===
