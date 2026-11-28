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

# === APIキー完全分離（JRA=有料Tier1 / NAR=無料枠専用・誤課金防止ガード付き） ===
JRA_API_KEY = os.environ.get("GEMINI_API_KEY", "").strip()
NAR_FREE_API_KEY = os.environ.get("GEMINI_FREE_API_KEY", "").strip()

AI_PLAN = os.environ.get("AI_PLAN", "plan2_neon").strip().lower()
CUSTOM_HIGH_MODEL = os.environ.get("GEMINI_HIGH_TIER_MODEL", "").strip()
CUSTOM_FAST_MODEL = os.environ.get("GEMINI_FAST_MODEL", "").strip()

if AI_PLAN == "plan2_neon":
    JRA_WIN5_G1_MODEL = CUSTOM_HIGH_MODEL or "gemini-4-neon"
    JRA_HIGH_MODEL = CUSTOM_HIGH_MODEL or "gemini-4-neon"
    JRA_FAST_MODEL = CUSTOM_FAST_MODEL or "gemini-4-neon"
    DEFAULT_MAX_JRA_CALLS = 10
elif AI_PLAN == "plan1_hydrogen":
    JRA_WIN5_G1_MODEL = CUSTOM_HIGH_MODEL or "gemini-4-hydrogen"
    JRA_HIGH_MODEL = CUSTOM_HIGH_MODEL or "gemini-4-hydrogen"
    JRA_FAST_MODEL = CUSTOM_FAST_MODEL or "gemini-4-hydrogen"
    DEFAULT_MAX_JRA_CALLS = 10
else:
    JRA_WIN5_G1_MODEL = CUSTOM_HIGH_MODEL or "gemini-4-hydrogen"
    JRA_HIGH_MODEL = CUSTOM_HIGH_MODEL or "gemini-4-hydrogen"
    JRA_FAST_MODEL = CUSTOM_FAST_MODEL or "gemini-3.8-flash"
    DEFAULT_MAX_JRA_CALLS = 6

NAR_FREE_HIGH_MODEL = "gemini-4-hydrogen"
NAR_FREE_FAST_MODEL = "gemini-3.8-flash"

MAX_AI_CALLS_JRA = int(os.environ.get("MAX_AI_CALLS_PER_RUN", str(DEFAULT_MAX_JRA_CALLS)))
MAX_AI_CALLS_NAR = int(os.environ.get("MAX_NAR_FREE_CALLS_PER_RUN", "3"))

def make_client(api_key: str, timeout_ms: int):
    if not api_key:
        return None
    try:
        return genai.Client(api_key=api_key, http_options=types.HttpOptions(timeout=timeout_ms))
    except Exception:
        return genai.Client(api_key=api_key)

jra_client = make_client(JRA_API_KEY, 90000)
nar_free_client = make_client(NAR_FREE_API_KEY, 55000)

os.makedirs("data", exist_ok=True)

ENGINE_VER = "v12.0-neon"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/124.0.0.0"}
SESSION = requests.Session()
SESSION.headers.update(HEADERS)

JRA_VENUES = {"01":"札幌","02":"函館","03":"福島","04":"新潟","05":"東京","06":"中山","07":"中京","08":"京都","09":"阪神","10":"小倉"}
NAR_VENUES = {"42":"浦和","43":"船橋","44":"大井","45":"川崎","30":"門別","35":"盛岡","36":"水沢","46":"金沢","47":"笠松","48":"名古屋","50":"園田","51":"姫路","54":"高知","55":"佐賀"}
NANKAN_CODES = {"42", "43", "44", "45"}
NANKAN_NAMES = {"浦和", "船橋", "大井", "川崎"}
BANEI_CODES = {"65"}

TOP_RIDERS = ("矢野", "御神本", "笹川", "吉原", "森泰斗", "ルメール", "川田", "戸崎", "坂井", "武豊", "松山", "横山武", "鮫島克", "C.デム", "モレイラ", "レーン", "マーカン")
POWER_SIRES = ("ナダル", "クリソベリル", "ゴールドアリュール", "ルヴァンスレーヴ", "シニスターミニスター", "ヘニーヒューズ", "ドレフォン", "パイロ", "マインドユアビスケッツ", "キズナ", "キタサンブラック", "エピファネイア", "ロードカナロア", "コントレイル", "モーリス")
TURF_START_DIRT = {("東京",1300),("東京",1400),("東京",1600),("中山",1200),("京都",1400),("阪神",1400),("中京",1400),("福島",1150),("新潟",1200)}

G1_KEYWORDS = ("G1", "GⅠ", "Jpn1", "JpnⅠ", "マイルCS", "ジャパンC", "ジャパンＣ", "有馬", "天皇賞", "ダービー", "オークス", "皐月賞", "桜花賞", "菊花賞", "秋華賞", "エリザベス", "チャンピオンズ", "阪神JF", "朝日杯", "ホープフル", "東京大賞典", "帝王賞", "JBC", "川崎記念", "かしわ記念")
TRUE_GRADED_KEYWORDS = (
    "Jpn", "G1", "G2", "G3", "GⅠ", "GⅡ", "GⅢ", "S1", "S2", "S3", "重賞",
    "記念", "マイルCS", "ジャパンC", "ジャパンＣ", "有馬", "天皇賞", "ダービー", "オークス",
    "皐月賞", "桜花賞", "菊花賞", "秋華賞", "エリザベス", "2歳S", "2歳Ｓ",
    "グランプリ", "兵庫ジュニア", "金賞", "大賞典", "帝王賞", "JBC",
    "かしわ", "マーキュリー", "クラスター", "南部杯", "スパーキング", "テレ玉杯",
    "さきたま杯", "オーバル", "東京盃", "レディスプレ", "京阪杯", "京王杯",
    "チャレンジC", "チャンピオンズ", "ステイヤーズ", "阪神JF", "朝日杯", "ホープフル"
)
NAR_DG_KEYWORDS = ("Jpn", "重賞", "ダートグレード", "兵庫ジュニア", "浦和記念", "名古屋グランプリ", "佐賀記念", "マーキュリー", "クラスター", "マイルCS南部", "JBC", "東京大賞典", "帝王賞", "かしわ記念", "川崎記念")
OBSTACLE_KEYWORDS = ("障害", "ジャンプ", "J・G", "JG1", "JG2", "JG3", "大障害", "グランドジャンプ")

AI_CALL_COUNT_JRA = 0
AI_CALL_COUNT_NAR = 0

def log(msg: str):
    print(f"[{int(time.time() - START_TS):03d}s] {msg}", flush=True)

def time_exceeded() -> bool:
    return (time.time() - START_TS) >= MAX_RUNTIME_SEC

def get_soup(url: str) -> BeautifulSoup:
    res = SESSION.get(url, timeout=8)
    raw = res.content
    txt = raw.decode("utf-8", errors="ignore") if b"utf-8" in raw[:1024].lower() else raw.decode("euc_jp", errors="ignore")
    return BeautifulSoup(txt, "html.parser")

def is_obstacle_race(name: str = "", sdist: str = "") -> bool:
    nm, sd = str(name or ""), str(sdist or "")
    return ("障" in sd) or any(k in nm for k in OBSTACLE_KEYWORDS)

def detect_is_graded(name: str, rnum: int = 0) -> bool:
    nm = str(name or "")
    if is_obstacle_race(nm, ""):
        return False
    if any(k in nm for k in TRUE_GRADED_KEYWORDS):
        return rnum == 0 or rnum >= 8
    return False

def detect_is_g1(name: str) -> bool:
    if is_obstacle_race(name, ""):
        return False
    return any(k in str(name or "") for k in G1_KEYWORDS)

def is_invalid_horse_name(name: str) -> bool:
    s = (name or "").strip()
    if not s or len(s) < 2:
        return True
    bad_tokens = ("[馬記号]", "馬記号", "馬名", "[ブリンカー]", "ブリンカー", "undefined", "null", "取消", "除外")
    if any(tok in s for tok in bad_tokens):
        return True
    if "[" in s or "]" in s or "{" in s or "}" in s:
        return True
    return False

def normalize_horse_name(name: str) -> str:
    s = (name or "").strip()
    s = re.sub(r"\[[^\]]*\]", "", s)
    s = re.sub(r"\s+", "", s)
    s = re.sub(r"([ァ-ヶー一-龥々])[BＢ]$", r"\1", s)
    return s.strip()

def is_scratched_row(tr) -> bool:
    cls_str = " ".join(tr.get("class") or [])
    if "Cancel" in cls_str or "Scratch" in cls_str:
        return True
    row_txt = tr.get_text(" ", strip=True)
    if any(k in row_txt for k in ("出走取消", "競走除外", "除外", "取消")):
        cancel_cells = tr.select("td.Cancel_Txt, td.Popular, td.Odds, td.Weight, td.Rank, td[class*='Cancel']")
        if not cancel_cells or any(any(k in c.get_text() for k in ("取消", "除外", "中止")) for c in cancel_cells):
            return True
    return False

def has_contaminated_cache(r: dict) -> bool:
    hs = r.get("horses")
    if not isinstance(hs, list) or not hs:
        return False
    if len(hs) > 18:
        return True
    nums = [h.get("num") for h in hs]
    if len(nums) != len(set(nums)):
        return True
    for h in hs:
        nm = str(h.get("name", ""))
        if is_invalid_horse_name(nm) or re.search(r"[ァ-ヶー一-龥々][BＢ]$", nm):
            return True
    return False

def extract_surface_dist(text: str) -> str:
    if not text:
        return ""
    m = re.search(r"([芝ダ障])\s*(\d{3,4})\s*m", text)
    if m:
        return f"{m.group(1)}{m.group(2)}m"
    m2 = re.search(r"([芝ダ障])(\d{3,4})", text)
    if m2:
        return f"{m2.group(1)}{m2.group(2)}m"
    return ""

def is_nankan_race(r: dict) -> bool:
    rid = str(r.get("raceId", ""))
    return (len(rid) >= 6 and rid[4:6] in NANKAN_CODES) or (r.get("venue") in NANKAN_NAMES)

def is_nar_bettable_race(r: dict) -> bool:
    if r.get("mode") != "nar":
        return True
    if r.get("isGraded") or any(k in str(r.get("name", "")) for k in NAR_DG_KEYWORDS):
        return True
    return is_nankan_race(r) and int(r.get("raceNumber", 0)) >= 10

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
            if mode == "nar":
                if vcode in BANEI_CODES or vcode not in NAR_VENUES:
                    continue
            v = vmap.get(vcode, "JRA")
            rnum = int(rid[10:12])
            name = (li.select_one(".ItemTitle") or li).get_text(strip=True)[:18]
            lg = li.select_one(".RaceList_ItemLong, .RaceData")
            full_li_txt = li.get_text(" ", strip=True)
            sdist = extract_surface_dist(lg.get_text(" ", strip=True) if lg else full_li_txt)
            # Code Patch P10: 障害レースを一覧取得段階で完全除外
            if is_obstacle_race(name, sdist):
                continue
            if mode == "nar":
                if "ばんえい" in name:
                    continue
                is_dg = any(k in name for k in NAR_DG_KEYWORDS)
                if (vcode in NANKAN_CODES and rnum < 9 and not is_dg):
                    continue
                if (vcode not in NANKAN_CODES) and not (is_dg and rnum >= 9):
                    continue
            tm_el = li.select_one(".RaceList_Itemtime, .RaceData")
            m_tm = re.search(r"(\d{1,2}:\d{2})", tm_el.get_text(" ", strip=True) if tm_el else full_li_txt)
            ptime = m_tm.group(1).zfill(5) if m_tm else ""
            is_new = ("新馬" in name) or ("メイクデビュー" in name)
            is_graded = detect_is_graded(name, rnum)
            skill = "app-bayesian-nar" if mode == "nar" else ("app-bayesian-make-debut" if is_new else "app-bayesian-horse-racing-text")
            races.append({
                "raceId": rid, "mode": mode, "venue": v, "raceNumber": rnum, "venueLabel": f"{v}{rnum}R",
                "name": name, "surfaceDist": sdist or "",
                "postTime": ptime,
                "isNew": is_new,
                "isGraded": is_graded,
                "rank": "New" if is_new else "Pass",
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

def fetch_live_odds_multi(base: str, rid: str, mode: str) -> tuple[dict, dict]:
    odds_map, wide_map = {}, {}
    api_path = "api_get_jra_odds.html" if mode == "jra" else "api_get_nar_odds.html"

    for q_extra in ("&action=init", "&compress=0", ""):
        if odds_map: break
        try:
            res = SESSION.get(f"{base}/api/{api_path}?race_id={rid}&type=1{q_extra}", timeout=5)
            o_json = res.json()
            o_dict = (o_json.get("data") or {}).get("odds", {}).get("1", {})
            if isinstance(o_dict, dict):
                for k, val in o_dict.items():
                    if str(k).isdigit() and isinstance(val, list) and val:
                        v0 = str(val[0]).replace(",", "")
                        if re.match(r"^\d+(\.\d+)?$", v0) and float(v0) >= 1.0:
                            odds_map[int(k)] = float(v0)
        except Exception: pass

    if not odds_map:
        try:
            osoup = get_soup(f"{base}/odds/index.html?type=b1&race_id={rid}")
            for tr in osoup.select("table tr"):
                u_el = tr.select_one("td.Waku + td, td[class*='Umaban'], td.Num")
                o_el = tr.select_one("span[id^='odds-1_'], td.Odds")
                if not u_el or not o_el: continue
                u_s = re.sub(r"\D", "", u_el.get_text(strip=True))
                m_o = re.search(r"(\d+\.\d+)", o_el.get_text().replace(",", ""))
                if u_s.isdigit() and m_o and 1 <= int(u_s) <= 18:
                    odds_map[int(u_s)] = float(m_o.group(1))
        except Exception: pass

    for q_extra in ("&action=init", ""):
        if wide_map: break
        try:
            w_json = SESSION.get(f"{base}/api/{api_path}?race_id={rid}&type=5{q_extra}", timeout=5).json()
            w_dict = (w_json.get("data") or {}).get("odds", {}).get("5", {})
            if isinstance(w_dict, dict):
                for k, val in w_dict.items():
                    if len(str(k)) == 4 and str(k).isdigit() and isinstance(val, list) and val:
                        low_s = str(val[0]).replace(",", "")
                        if re.match(r"^\d+(\.\d+)?$", low_s):
                            a, b = int(str(k)[:2]), int(str(k)[2:4])
                            if a != b and float(low_s) >= 1.1:
                                wide_map[f"{min(a,b)}-{max(a,b)}"] = round(float(low_s), 1)
        except Exception: pass

    return odds_map, wide_map

def fetch_full_shutuba(rid: str, mode: str = "jra", need_shutuba: bool = True, need_result: bool = True) -> tuple[str, list, list, str, str, dict, dict, bool, str]:
    base = "https://race.netkeiba.com" if mode == "jra" else "https://nar.netkeiba.com"
    lines, top3_actual, odds_map, wide_map = [], [], {}, {}
    runners_by_num: dict[int, dict] = {}
    scratched_nums: set[int] = set()
    track_cond, post_time, payouts, surface_dist = "良", "", {}, ""

    if need_shutuba:
        odds_map, wide_map = fetch_live_odds_multi(base, rid, mode)

        try:
            soup = get_soup(f"{base}/race/shutuba.html?race_id={rid}")
            r1, r2 = soup.select_one(".RaceData01"), soup.select_one(".RaceData02")
            if r1:
                r1_txt = " ".join(r1.get_text(" ", strip=True).split())
                m_pt = re.search(r"(\d{1,2}:\d{2})\s*発走", r1_txt)
                if m_pt: post_time = m_pt.group(1).zfill(5)
                sd = extract_surface_dist(r1_txt)
                if sd: surface_dist = sd
                for c in ("不良", "重", "稍重", "良"):
                    if c in r1_txt: track_cond = c; break
                lines.append("【条件・馬場】" + r1_txt)
            if r2:
                r2_txt = " ".join(r2.get_text(" ", strip=True).split())
                if not surface_dist:
                    sd2 = extract_surface_dist(r2_txt)
                    if sd2: surface_dist = sd2
                lines.append("【コース・クラス】" + r2_txt)
            for tr in soup.select("tr.HorseList"):
                n_el = tr.select_one("span.HorseName a, .HorseName a, td.HorseInfo a")
                if not n_el: continue
                raw_name = n_el.get_text(strip=True)
                if is_invalid_horse_name(raw_name): continue
                h_name = normalize_horse_name(raw_name)
                if is_invalid_horse_name(h_name): continue

                w_el, u_el = tr.select_one("td[class*='Waku']"), tr.select_one("td[class*='Umaban'], td.Num")
                u_txt = re.sub(r"\D", "", u_el.get_text(strip=True)) if u_el else ""
                if not u_txt.isdigit(): continue
                u_int = int(u_txt)
                if not (1 <= u_int <= 18): continue

                if is_scratched_row(tr):
                    scratched_nums.add(u_int)
                    continue

                w_txt = re.sub(r"\D", "", w_el.get_text(strip=True)) if w_el else ""
                w_int = int(w_txt) if w_txt.isdigit() and 1 <= int(w_txt) <= 8 else ((u_int - 1) // 2 + 1)
                sex_age = tr.select_one("td.Barei, span.Barei")
                futan = tr.select_one("td.Futan")
                j_el = tr.select_one("td.Jockey a, td.Jockey")
                wt_el = tr.select_one("td.Weight")
                odd_el = tr.select_one("td.Popular span[id^='odds-'], span[id^='odds-'], td.Odds, td.Txt_R")
                odd_val = odds_map.get(u_int, 0.0)
                if odd_val <= 1.0 and odd_el:
                    m_o = re.search(r"(\d+\.\d+)", odd_el.get_text().replace(",", ""))
                    if m_o: odd_val = float(m_o.group(1))
                runners_by_num[u_int] = {
                    "waku": w_int, "num": u_int, "name": h_name,
                    "sexAge": sex_age.get_text(strip=True) if sex_age else "",
                    "futan": futan.get_text(strip=True) if futan else "",
                    "pedigree": "", "jockey": j_el.get_text(" ", strip=True) if j_el else "",
                    "weight": wt_el.get_text(strip=True) if wt_el else "", "odds": odd_val, "past": ""
                }
        except Exception: pass

        try:
            psoup = get_soup(f"{base}/race/shutuba_past.html?race_id={rid}")
            pr1 = psoup.select_one(".RaceData01")
            if pr1:
                pr1_txt = pr1.get_text(" ", strip=True)
                if not post_time:
                    m_pt = re.search(r"(\d{1,2}:\d{2})\s*発走", pr1_txt)
                    if m_pt: post_time = m_pt.group(1).zfill(5)
                if not surface_dist:
                    sd = extract_surface_dist(pr1_txt)
                    if sd: surface_dist = sd
            for tr in psoup.select("tr.HorseList"):
                n_el = tr.select_one(".Horse02 a, .HorseName a, .Horse02")
                if not n_el: continue
                raw_name = n_el.get_text(strip=True).split()[0]
                if is_invalid_horse_name(raw_name): continue
                h_name = normalize_horse_name(raw_name)
                if is_invalid_horse_name(h_name): continue

                u_el = tr.select_one("td[class*='Umaban'], td.Num")
                u_txt = re.sub(r"\D", "", u_el.get_text(strip=True)) if u_el else ""
                u_int = int(u_txt) if (u_txt.isdigit() and 1 <= int(u_txt) <= 18) else 0

                if is_scratched_row(tr):
                    if u_int: scratched_nums.add(u_int)
                    continue
                if u_int and u_int in scratched_nums:
                    continue

                f_sire, m_sire = tr.select_one(".Horse01"), tr.select_one(".Horse03")
                ped = f"父:{f_sire.get_text(strip=True) if f_sire else ''}/母父:{m_sire.get_text(strip=True) if m_sire else ''}" if (f_sire or m_sire) else ""
                pasts = " / ".join([" ".join(td.get_text(" ", strip=True).split())[:95] for td in tr.select("td.Past")[:4]])

                target = runners_by_num.get(u_int) if u_int else None
                if not target:
                    target = next((x for x in runners_by_num.values() if normalize_horse_name(x["name"]) == h_name), None)
                if target:
                    if ped: target["pedigree"] = ped
                    if pasts: target["past"] = pasts
                elif u_int and not runners_by_num:
                    runners_by_num[u_int] = {
                        "waku": (u_int - 1) // 2 + 1, "num": u_int, "name": h_name,
                        "sexAge": "", "futan": "", "pedigree": ped, "jockey": "", "weight": "",
                        "odds": odds_map.get(u_int, 0.0), "past": pasts
                    }
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
                if not surface_dist:
                    sd = extract_surface_dist(rd1_txt)
                    if sd: surface_dist = sd
                for c in ("不良", "重", "稍重", "良"):
                    if c in rd1_txt: track_cond = c; break
            for tr in rsoup.select("#All_Result_Table tbody tr, table.RaceTable01 tbody tr"):
                tds = [td.get_text(" ", strip=True) for td in tr.select("td")]
                if len(tds) < 8: continue
                rank_txt = tds[0]
                rank_s, w_s, u_s = re.sub(r"\D", "", rank_txt), re.sub(r"\D", "", tds[1]), re.sub(r"\D", "", tds[2])
                if not u_s.isdigit(): continue
                u_int = int(u_s)
                if not (1 <= u_int <= 18): continue

                if any(k in rank_txt for k in ("取消", "除外")):
                    scratched_nums.add(u_int)
                    runners_by_num.pop(u_int, None)
                    continue

                w_int = int(w_s) if (w_s.isdigit() and 1 <= int(w_s) <= 8) else ((u_int - 1) // 2 + 1)
                n_el = tr.select_one("span.Horse_Name a, .Horse_Name, td.Horse_Info a")
                raw_name = n_el.get_text(strip=True) if n_el else tds[3].split()[0]
                h_name = normalize_horse_name(raw_name)
                if is_invalid_horse_name(h_name): continue

                odd_num = odds_map.get(u_int, 0.0)
                for cell in tds[8:]:
                    if re.match(r"^\d{1,4}\.\d$", cell.replace(",", "")):
                        odd_num = float(cell.replace(",", "")); break
                ex = runners_by_num.get(u_int)
                if ex:
                    ex["name"] = h_name
                    ex["waku"] = w_int
                    if odd_num > 1.0: ex["odds"] = odd_num
                    if len(tds) > 14 and re.search(r"\d{3}\(", tds[14]): ex["weight"] = tds[14]
                elif need_shutuba:
                    runners_by_num[u_int] = {
                        "waku": w_int, "num": u_int, "name": h_name,
                        "sexAge": tds[4] if len(tds) > 4 else "",
                        "futan": tds[5] if len(tds) > 5 else "",
                        "pedigree": "", "jockey": tds[6].split()[0] if len(tds) > 6 else "",
                        "weight": tds[14] if len(tds) > 14 else "",
                        "odds": odd_num or 0.0, "past": ""
                    }
                if len(top3_actual) < 3 and rank_s.isdigit():
                    top3_actual.append({"rank": rank_s, "waku": w_int, "num": u_int, "name": h_name, "odds": str(odd_num or 10.0)})
            if top3_actual:
                payouts = parse_payout_table(rsoup)
        except Exception: pass

    for sc in scratched_nums:
        runners_by_num.pop(sc, None)

    raw_runners = [runners_by_num[k] for k in sorted(runners_by_num.keys())]
    wt_cnt = sum(1 for r in raw_runners if re.search(r"\d{3}\([+-]?\d+\)", str(r.get("weight", ""))))
    weights_ready = bool(raw_runners) and (wt_cnt >= max(3, len(raw_runners) // 2))
    for r in raw_runners:
        lines.append(f"{r['waku']}枠 {r['num']}番 {r['name']} (性齢:{r.get('sexAge','')} 斤量:{r.get('futan','')} {r.get('pedigree','')} 騎手:{r['jockey']} 馬体:{r['weight'] or '未発表'} 単勝:{r['odds'] if r['odds']>1 else '未発売'}倍) | 近4走:{r['past']}")
    return "\n".join(lines[:22]), top3_actual, raw_runners, track_cond, post_time, payouts, wide_map, weights_ready, surface_dist

def summarize_intraday_track_bias(races: list, venue: str) -> tuple[str, int]:
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

def parse_body_weight(wt_str: str) -> tuple[int, int]:
    m_bw = re.search(r"(\d{3})\(([+-]?\d+)\)", str(wt_str or ""))
    if m_bw:
        return int(m_bw.group(1)), int(m_bw.group(2))
    m_only = re.search(r"\b(\d{3})\b", str(wt_str or ""))
    return (int(m_only.group(1)), 0) if m_only else (0, 0)

def has_severe_weight_disqualify(h: dict, dist: int = 1600, is_new: bool = False, is_dirt: bool = False) -> bool:
    """単勝4.5倍以下の上位人気を例外的に危険視できる明確なFレベル馬体失格のみ判定"""
    bw, dw = parse_body_weight(str(h.get("weight", "")))
    if dist >= 1800 and dw >= 12:
        return True
    if dw >= 14:
        return True
    if is_new and is_dirt and bw > 0 and bw <= 400:
        return True
    return False

def normalize_prob_scale_list(horses_dicts: list):
    """Code Patch P12: AIが0〜1の小数(例:0.232)で確率を返した場合に自動で×100補正"""
    if not horses_dicts:
        return
    f_vals = [float(h.get("f", 0) or 0) for h in horses_dicts if h.get("f") is not None]
    if f_vals and sum(f_vals) <= 1.8 and max(f_vals) <= 1.0:
        for h in horses_dicts:
            for k in ("f", "fFund", "q", "top2", "top3"):
                if h.get(k) is not None and float(h[k]) <= 3.1:
                    h[k] = round(float(h[k]) * 100.0, 1)

def apply_python_benter_fusion(race: dict, w_mkt_base: float = 0.55):
    """Code Patch P9 + Patch S5/S6: AI出力のfFundと実オッズqをPython側で厳密2-Stage融合＆過大評価キャップ"""
    horses = race.get("horses") or []
    n = len(horses)
    if n < 3:
        return

    normalize_prob_scale_list(horses)
    sdist = str(race.get("surfaceDist", "ダ1600m"))
    m_dist = re.search(r"(\d{3,4})", sdist)
    dist = int(m_dist.group(1)) if m_dist else 1600
    is_dirt = ("ダ" in sdist) or (race.get("mode") == "nar")
    is_new = bool(race.get("isNew")) or race.get("skill") == "app-bayesian-make-debut" or "新馬" in str(race.get("name", ""))

    # 基礎勝率 fFund を正規化
    raw_ff = []
    for h in horses:
        ff = float(h.get("fFund") or h.get("f") or 1.0)
        raw_ff.append(max(0.2, ff))
    sum_ff = max(1.0, sum(raw_ff))
    ff_probs = [x * 100.0 / sum_ff for x in raw_ff]

    # 実オッズ存在判定とFLB市場確率 q の厳密計算
    live_odds = [float(h.get("odds", 0) or 0) for h in horses]
    has_live = sum(1 for o in live_odds if o > 1.0) >= max(3, n // 2)
    if not has_live:
        for i, h in enumerate(horses):
            h["fFund"] = round(ff_probs[i], 1)
            h["f"] = round(ff_probs[i], 1)
        return

    inv_p = [math.pow(max(1.1, o if o > 1.0 else 99.0), -1.08) for o in live_odds]
    sum_inv = max(1e-6, sum(inv_p))
    q_probs = [x * 100.0 / sum_inv for x in inv_p]

    ln_q = [math.log(max(0.001, q_probs[i] / 100.0)) for i in range(n)]
    ln_f = [math.log(max(0.001, ff_probs[i] / 100.0)) for i in range(n)]
    mean_q, mean_f = sum(ln_q) / n, sum(ln_f) / n
    std_q = math.sqrt(sum((x - mean_q) ** 2 for x in ln_q) / max(1, n))
    std_f = math.sqrt(sum((x - mean_f) ** 2 for x in ln_f) / max(1, n))
    f_gain = min(1.50, max(0.75, (std_q / max(0.30, std_f)) * 0.85))

    post_logits = []
    for i, h in enumerate(horses):
        o = live_odds[i]
        severe_disq = has_severe_weight_disqualify(h, dist=dist, is_new=is_new, is_dirt=is_dirt)
        ai_w = float(h.get("wUsed") if h.get("wUsed") is not None else w_mkt_base)
        # Patch S5: 単勝4.5倍以下の1〜2番人気は明確な馬体失格がない限り市場ウェイト0.42以上を強制確保
        if 1.0 < o <= 4.5 and not severe_disq:
            w_i = max(0.42, min(0.70, w_mkt_base))
            if h.get("mark") in ("消", "危"):
                h["mark"] = "△"
        elif severe_disq:
            w_i = 0.18
        else:
            w_i = max(0.35, min(0.68, 0.5 * w_mkt_base + 0.5 * ai_w))
        h["wUsed"] = round(w_i, 2)
        ln_f_aligned = mean_q + (ln_f[i] - mean_f) * f_gain
        post_logits.append((1.0 - w_i) * ln_f_aligned + w_i * ln_q[i])

    max_pl = max(post_logits)
    w_post = [math.exp(x - max_pl) for x in post_logits]
    f_probs = [x * 100.0 / max(1e-6, sum(w_post)) for x in w_post]

    # Patch S6: 中穴・超穴の過大評価キャリブレーション上限
    capped = False
    for i, o in enumerate(live_odds):
        if o >= 50.0 and f_probs[i] > 5.5:
            f_probs[i] = 5.5
            capped = True
        elif o >= 8.0:
            cap_val = min(18.0, q_probs[i] + 10.0)
            if f_probs[i] > cap_val:
                f_probs[i] = cap_val
                capped = True
    if capped:
        sf = max(1.0, sum(f_probs))
        f_probs = [x * 100.0 / sf for x in f_probs]

    # 2着内・3着内を融合勝率と整合させて保存則正規化
    raw_t2, raw_t3 = [], []
    for i, h in enumerate(horses):
        old_t2 = float(h.get("top2") or (f_probs[i] * 1.9))
        old_t3 = float(h.get("top3") or (f_probs[i] * 2.8))
        raw_t2.append(0.65 * (f_probs[i] * 1.95) + 0.35 * old_t2)
        raw_t3.append(0.65 * (f_probs[i] * 2.85) + 0.35 * old_t3)
    s2, s3 = max(1.0, sum(raw_t2)), max(1.0, sum(raw_t3))

    for i, h in enumerate(horses):
        h["fFund"] = round(ff_probs[i], 1)
        h["q"] = round(q_probs[i], 1)
        h["f"] = round(f_probs[i], 1)
        h["top2"] = round(min(94.0, raw_t2[i] * 200.0 / s2), 1)
        h["top3"] = round(min(97.0, raw_t3[i] * 300.0 / s3), 1)

    # 融合後スコア順でソート＆印再確定（50倍超の◎◯▲進入禁止）
    horses.sort(
        key=lambda x: (float(x["f"]) * 0.58 + float(x["top3"]) * 0.42) - (12.0 if float(x.get("odds", 0)) >= 50.0 else 0.0),
        reverse=True,
    )
    for rk, h in enumerate(horses):
        o = float(h.get("odds", 99))
        severe_disq = has_severe_weight_disqualify(h, dist=dist, is_new=is_new, is_dirt=is_dirt)
        if severe_disq and o <= 6.0:
            h["mark"] = "危" if is_new else "消"
        elif o >= 50.0:
            h["mark"] = "△" if rk <= 6 else "無"
        elif rk == 0: h["mark"] = "◎"
        elif rk == 1: h["mark"] = "◯"
        elif rk == 2: h["mark"] = "▲"
        elif rk == 3: h["mark"] = "☆"
        elif rk <= 6: h["mark"] = "△"
        else: h["mark"] = "無"

    race["wR"] = round(w_mkt_base, 2)
    race["hasLiveOdds"] = True

def compute_bayesian_full_field(raw_runners: list, race_meta: dict, track_cond: str = "良") -> tuple[list, int, dict, dict]:
    if not raw_runners:
        return [], 3, {"s1": 35, "s2": 40, "s3": 25}, {"wR": 0.65, "m3": 0.0, "coreConnections": [], "counterfactualAudit": ""}

    n = len(raw_runners)
    venue, sdist, mode = race_meta.get("venue", "東京"), race_meta.get("surfaceDist") or "ダ1400m", race_meta.get("mode", "jra")
    is_new = bool(race_meta.get("isNew")) or race_meta.get("rank") == "New" or "新馬" in str(race_meta.get("name", ""))
    m_dist = re.search(r"(\d{3,4})", sdist)
    dist = int(m_dist.group(1)) if m_dist else 1400
    is_dirt = ("ダ" in sdist) or (mode == "nar")
    is_turf_start = is_dirt and ((venue, dist) in TURF_START_DIRT)
    is_wet, is_tight = (track_cond in ("重", "不良")), (venue in ("浦和", "川崎", "中山", "福島", "小倉", "園田", "笠松", "水沢"))
    is_wet_short_dirt = is_dirt and is_wet and dist <= 1200

    parsed = [parse_past_metrics(r.get("past", ""), r.get("waku", 4)) for r in raw_runners]
    n_lead = max(1, sum(1 for p in parsed if p["isLeader"]))
    pi_s1, pi_s2, pi_s3 = ((0.25, 0.35, 0.40) if not is_tight else (0.30, 0.35, 0.35)) if n_lead >= 5 else ((0.50, 0.35, 0.15) if n_lead <= 2 else (0.35, 0.40, 0.25))
    scen_w = {"s1": int(pi_s1 * 100), "s2": int(pi_s2 * 100), "s3": int(pi_s3 * 100)}

    has_live_odds = sum(1 for r in raw_runners if r.get("odds", 0) > 1.0) >= max(3, n // 2)
    base_wr = 0.72 if is_new else (0.65 if mode == "jra" else 0.66)

    fund_logits, place_deltas, notes, styles = [], [], [], []
    clamp_flags, soft_inner_flags, ban_honmei_flags = [], [], []

    for idx, r in enumerate(raw_runners):
        waku, jockey, wt, sex_age, futan, ped = r.get("waku", 4), r.get("jockey", ""), r.get("weight", ""), r.get("sexAge", ""), r.get("futan", ""), r.get("pedigree", "")
        pm, style = parsed[idx], parsed[idx]["style"]
        live_odd = float(r.get("odds", 0))
        is_top2_fav_odd = has_live_odds and (1.0 < live_odd <= 4.5)

        if is_new:
            base_theta = 0.0
        else:
            win_bonus = 0.52 if (pm["ranks"] and pm["ranks"][0] == 1) else (0.28 if (pm["ranks"] and pm["ranks"][0] <= 3) else 0.0)
            base_theta = -0.34 * (pm["avgRank"] - 6.0) + win_bonus

        delta_th, delta_pl, reasons = 0.0, 0.0, []
        is_hazard, is_soft_inner, ban_honmei = False, False, False

        m_ft = re.search(r"(\d{2}\.?\d?)", str(futan))
        ft_val = float(m_ft.group(1)) if m_ft else 56.0
        if "3" in sex_age and ft_val <= 55.0:
            delta_th += 0.14; delta_pl += 0.10; reasons.append(f"F:3歳{ft_val}kg(H:軽量)")
        elif ft_val >= 58.0:
            delta_th -= 0.12; delta_pl -= 0.08; reasons.append(f"F:斤量{ft_val}kg(H:酷量)")

        if is_dirt and waku <= 2:
            if is_wet_short_dirt:
                if style in ("逃", "先") or is_top2_fav_odd:
                    delta_th += 0.06; delta_pl += 0.06; reasons.append(f"F:道悪短ダ{waku}枠(H:内前免除)")
            elif is_top2_fav_odd or is_turf_start or (pm["isStreakRiser"] and ("3" in sex_age or "4" in sex_age)):
                delta_th -= 0.09; delta_pl -= 0.05; is_soft_inner = True
                reasons.append(f"F:ダ{waku}枠上位/芝発(H:減点ソフト上限)")
            elif is_new:
                delta_th -= 0.22; delta_pl -= 0.12; is_hazard = True
                reasons.append(f"F:ダ新馬{waku}枠(H:砂被り危)")
            elif style != "逃":
                delta_th -= 0.12; delta_pl -= 0.08; is_hazard = True
                reasons.append(f"F:ダ{waku}枠(H:砂被り警戒)")
        elif is_turf_start and waku >= 7 and style in ("逃", "先"):
            delta_th += 0.16; delta_pl += 0.12; reasons.append(f"F:芝発進{waku}枠先行(H:外加速)")

        body_w, diff_w = parse_body_weight(wt)
        if is_new and is_dirt and body_w > 0:
            if body_w <= 400:
                delta_th -= 0.22; delta_pl -= 0.16; is_hazard = True; ban_honmei = True
                reasons.append(f"F:ダ新馬{body_w}kg(H:極小◎禁止)")
            elif body_w < 420:
                delta_th -= 0.16; delta_pl -= 0.12; ban_honmei = True
                reasons.append(f"F:ダ新馬{body_w}kg(H:小柄減点)")
            elif body_w >= 470:
                delta_th += 0.10; delta_pl += 0.06; reasons.append(f"F:ダ新馬{body_w}kg(H:馬格加点)")

        if dist >= 1800 and diff_w >= 12:
            delta_th -= 0.20; delta_pl -= 0.14; is_hazard = True; ban_honmei = True
            reasons.append(f"F:1800m+馬体+{diff_w}kg(H:TypeII減点)")
        elif diff_w >= 14:
            delta_th -= 0.18; delta_pl -= 0.14; is_hazard = True; ban_honmei = True
            reasons.append(f"F:馬体+{diff_w}kg(H:TypeII大幅増)")
        elif diff_w >= 10:
            delta_th -= 0.12; delta_pl -= 0.08; ban_honmei = True
            reasons.append(f"F:馬体+{diff_w}kg(H:TypeII警戒)")
        elif is_wet and is_dirt and waku >= 6 and body_w >= 500 and style in ("逃", "先"):
            delta_th += 0.16; delta_pl += 0.12; reasons.append(f"F:{waku}枠{body_w}kg(H:道悪外枠大型)")
        elif -8 <= diff_w <= -2:
            delta_th += 0.08; reasons.append(f"F:馬体{diff_w}kg絞り(H:好仕上)")

        if is_dirt and pm["isStreakRiser"] and ("3" in sex_age or "4" in sex_age):
            delta_th += 0.14; delta_pl += 0.10; reasons.append("F:ダ連勝昇級(H:Riser加点)")
        if pm["isSilver"]:
            delta_th -= 0.10; delta_pl += 0.18; reasons.append("F:2・3着連続(H:安定Connector)")
        elif pm["hasRebound"]:
            delta_th += 0.16; delta_pl += 0.12; reasons.append("F:0.2s差実績(H:巻き返し)")
        if any(tr in jockey for tr in TOP_RIDERS):
            delta_th += 0.14; delta_pl += 0.16; reasons.append(f"F:{jockey[:4]}騎手(H:Top騎手)")
        if any(s in ped for s in POWER_SIRES):
            delta_th += 0.08; reasons.append(f"F:{ped[:10]}(H:血統適性)")

        scen_shift = (0.12 * pi_s1 - 0.08 * pi_s3) if style in ("逃", "先") else (-0.08 * pi_s1 + 0.14 * pi_s3)
        clamped_th = max(-0.45, min(0.45, delta_th + scen_shift))
        clamped_pl = max(-0.30, min(0.25, delta_pl))

        if not reasons: reasons.append(f"F:{waku}枠・近走平均{pm['avgRank']:.1f}着")
        fund_logits.append(base_theta + clamped_th)
        place_deltas.append(clamped_pl)
        notes.append(" / ".join(reasons)[:46])
        styles.append(style)
        clamp_flags.append(is_hazard)
        soft_inner_flags.append(is_soft_inner)
        ban_honmei_flags.append(ban_honmei)

    max_fl = max(fund_logits)
    w_fund = [math.exp((x - max_fl) * 1.25) for x in fund_logits]
    f_fund_probs = [x / sum(w_fund) * 100.0 for x in w_fund]

    final_odds = [
        round(float(r["odds"]), 1) if (has_live_odds and r.get("odds", 0) > 1.0)
        else round(max(1.5, min(99.9, 80.0 / max(0.8, f_fund_probs[i]))), 1)
        for i, r in enumerate(raw_runners)
    ]
    inv_power = [math.pow(max(1.1, o), -1.08) for o in final_odds]
    q_probs = [x / sum(inv_power) * 100.0 for x in inv_power]

    ln_q_list = [math.log(max(0.001, q_probs[i] / 100.0)) for i in range(n)]
    ln_f_list = [math.log(max(0.001, f_fund_probs[i] / 100.0)) for i in range(n)]
    mean_q = sum(ln_q_list) / n
    mean_f = sum(ln_f_list) / n
    std_q = math.sqrt(sum((x - mean_q) ** 2 for x in ln_q_list) / max(1, n))
    std_f = math.sqrt(sum((x - mean_f) ** 2 for x in ln_f_list) / max(1, n))
    f_gain = min(1.85, max(1.0, (std_q / max(0.28, std_f)) * 0.72)) if has_live_odds else 1.0

    post_logits, w_used_list = [], []
    for i in range(n):
        if not has_live_odds:
            w_i = 0.0
        elif clamp_flags[i]:
            w_i = 0.15 if is_new else 0.20
        elif soft_inner_flags[i]:
            w_i = max(0.45, base_wr - 0.12)
        else:
            w_i = base_wr
        w_used_list.append(round(w_i, 2))
        ln_f_aligned = mean_q + (ln_f_list[i] - mean_f) * f_gain
        post_logits.append((1.0 - w_i) * ln_f_aligned + w_i * ln_q_list[i])

    max_pl = max(post_logits)
    w_post = [math.exp(x - max_pl) for x in post_logits]
    f_probs = [x / sum(w_post) * 100.0 for x in w_post]

    if has_live_odds:
        capped_any = False
        for i in range(n):
            if final_odds[i] >= 50.0 and f_probs[i] > 5.5:
                f_probs[i] = 5.5
                capped_any = True
            elif final_odds[i] >= 8.0:
                cap_v = min(18.0, q_probs[i] + 10.0)
                if f_probs[i] > cap_v:
                    f_probs[i] = cap_v
                    capped_any = True
        if capped_any:
            sf_c = max(1.0, sum(f_probs))
            f_probs = [x * 100.0 / sf_c for x in f_probs]

    w2 = [math.exp((post_logits[i] + place_deltas[i]) - max_pl) for i in range(n)]
    p2_raw = [0.46 * f_probs[i] + 0.54 * (w2[i] / sum(w2) * 100.0) for i in range(n)]
    top2_probs = [min(92.0, x * (200.0 / max(1.0, sum(p2_raw)))) for x in p2_raw]
    top3_probs = [min(96.0, x * (300.0 / max(1.0, sum(top2_probs)))) for x in top2_probs]

    def sort_score(i: int) -> float:
        base_s = f_probs[i] * 0.55 + top3_probs[i] * 0.45
        if has_live_odds and final_odds[i] >= 50.0:
            base_s -= 12.0
        if ban_honmei_flags[i]:
            base_s -= 4.0
        return base_s

    order = sorted(range(n), key=sort_score, reverse=True)
    if len(order) >= 2 and (parsed[order[0]]["isSilver"] or clamp_flags[order[0]] or ban_honmei_flags[order[0]]):
        for k in range(1, min(4, len(order))):
            if not ban_honmei_flags[order[k]] and not clamp_flags[order[k]] and not (has_live_odds and final_odds[order[k]] >= 50.0):
                order[0], order[k] = order[k], order[0]
                break

    marks_map, roles_map = {}, {}
    for rk, i in enumerate(order):
        gap = f_probs[i] - q_probs[i]
        is_extreme_ls = has_live_odds and final_odds[i] >= 50.0
        is_protected_fav = has_live_odds and final_odds[i] <= 4.5 and not has_severe_weight_disqualify(raw_runners[i], dist=dist, is_new=is_new, is_dirt=is_dirt)
        if clamp_flags[i] and q_probs[i] >= 14.0 and not soft_inner_flags[i] and not is_protected_fav:
            marks_map[i], roles_map[i] = ("危" if is_new else "消"), "過剰人気ハザード"
        elif is_extreme_ls:
            marks_map[i], roles_map[i] = ("△" if rk <= 6 else "無"), "超穴抑え上限"
        elif rk == 0: marks_map[i], roles_map[i] = "◎", "最安定Top-3軸"
        elif rk == 1: marks_map[i], roles_map[i] = "◯", "融合上位強制結線"
        elif rk == 2: marks_map[i], roles_map[i] = "▲", "安定Connector"
        elif rk == 3 or (rk <= 5 and (gap >= 2.0 or parsed[i]["hasRebound"] or parsed[i]["isStreakRiser"])):
            marks_map[i], roles_map[i] = "☆", "展開・連勝特注穴"
        elif rk <= 6: marks_map[i], roles_map[i] = "△", "3列目連下"
        elif q_probs[i] >= 12.0 and gap <= -3.5 and not soft_inner_flags[i] and not is_protected_fav:
            marks_map[i], roles_map[i] = "危", "過剰人気警戒"
        elif rk >= n - 2 and not is_protected_fav:
            marks_map[i], roles_map[i] = "消", "時計・展開劣勢"
        else:
            marks_map[i], roles_map[i] = "無", "強調材料乏しい"

    horses_out = [{
        "mark": marks_map[i], "role": roles_map[i], "num": raw_runners[i]["num"], "name": raw_runners[i]["name"],
        "style": styles[i], "weight": raw_runners[i].get("weight", ""),
        "f": round(f_probs[i], 1), "fFund": round(f_fund_probs[i], 1),
        "q": round(q_probs[i], 1), "wUsed": w_used_list[i],
        "top2": round(top2_probs[i], 1), "top3": round(top3_probs[i], 1),
        "odds": final_odds[i], "comment": notes[i]
    } for i in order]

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
        f"◎{safe_nodes[0]['num']}番破綻時は◯{safe_nodes[1]['num']}-▲{safe_nodes[2]['num']}の防衛線カバー。"
        if len(safe_nodes) >= 3 else "上位3頭のCore結線で防衛。"
    )
    if faded:
        cf_audit += f" 危険視{faded['num']}番は単騎楽逃げ時のみ復活。"

    neon_meta = {
        "wR": base_wr if has_live_odds else 0.0,
        "hasLiveOdds": has_live_odds,
        "m3": m3_val, "coreConnections": conns,
        "portfolioRules": {"coreRatio": 0.62, "alphaRatio": 0.38, "singleLongshotCapPct": 0.30},
        "counterfactualAudit": cf_audit,
        "strategyProfile": "v12_balanced_roi"
    }
    return horses_out, n_lead, scen_w, neon_meta

def lookup_wide_odds(wide_map: dict, a: int, b: int, fallback: float) -> float:
    if isinstance(wide_map, dict):
        val = wide_map.get(f"{min(a,b)}-{max(a,b)}")
        if val and float(val) >= 1.1:
            return float(val)
    return fallback

def build_neon_core_shield_specs(race: dict, B: int = 10000) -> tuple[list, dict, dict]:
    """Code Patch P11: Core 62% (◎-☆結線復活・2〜4点ダッチング) + Alpha 38% (◎単勝優先保護・馬連2点・少点数3連複)"""
    horses = race.get("horses") or []
    sorted_h = sorted(horses, key=lambda x: (float(x.get("f", 0)) * 0.55 + float(x.get("top3", 0)) * 0.45), reverse=True)
    valid = [h for h in sorted_h if h.get("mark") not in ("消", "危", "無")]
    pool = valid if len(valid) >= 4 else [h for h in sorted_h if h.get("mark") != "消"]
    if len(pool) < 3: pool = sorted_h
    h1, h2, h3 = pool[0], pool[1], pool[2]
    h4 = pool[3] if len(pool) > 3 else h3

    # 市場1〜2番人気(O<=5.0・欠格なし)が漏れていればh4へ強制結線編入
    by_odds = sorted([h for h in horses if float(h.get("odds", 99)) > 1.0], key=lambda x: float(x.get("odds", 99)))
    core_nums = {h1["num"], h2["num"], h3["num"], h4["num"]}
    forced_fav = False
    for fav in by_odds[:2]:
        if float(fav.get("odds", 99)) <= 5.0 and fav.get("mark") not in ("消", "危") and fav["num"] not in core_nums:
            h4 = fav
            forced_fav = True
            break

    himos = [h for h in sorted_h if h["num"] not in (h1["num"], h2["num"], h3["num"], h4["num"]) and h.get("mark") != "消"][:2]

    o1 = max(1.1, float(h1.get("odds", 3.5)))
    o2 = max(1.2, float(h2.get("odds", 5.5)))
    o3 = max(1.2, float(h3.get("odds", 7.5)))
    o4 = max(1.5, float(h4.get("odds", 10.0)))
    wm = race.get("wideOddsMap") or {}

    core_budget = int(round((B * 0.62) / 100) * 100)
    alpha_budget = max(500, B - core_budget)
    max_longshot = int(B * 0.30)

    w12 = lookup_wide_odds(wm, h1["num"], h2["num"], max(1.3, round(math.sqrt(o1 * o2) * 0.62, 1)))
    w13 = lookup_wide_odds(wm, h1["num"], h3["num"], max(1.5, round(math.sqrt(o1 * o3) * 0.68, 1)))
    w23 = lookup_wide_odds(wm, h2["num"], h3["num"], max(1.8, round(math.sqrt(o2 * o3) * 0.72, 1)))
    w14 = lookup_wide_odds(wm, h1["num"], h4["num"], max(1.9, round(math.sqrt(o1 * o4) * 0.75, 1)))

    # Core 62%: O◎<=1.8は2点圧縮、1.8<O◎<=2.2は◎軸3点(◎-◯/▲/☆)、O◎>2.2は4点(◎-◯/▲/☆ + ◯-▲)
    if o1 <= 1.8:
        cand_partners = [
            (h2, w12, o2, f"ワイド {h1['num']}-{h2['num']} (◎-◯ 2点Core)"),
            (h3, w13, o3, f"ワイド {h1['num']}-{h3['num']} (◎-▲ 2点Core)"),
        ]
        if h4["num"] != h3["num"]:
            cand_partners.append((h4, w14, o4, f"ワイド {h1['num']}-{h4['num']} (◎-{'人気' if forced_fav else '☆'} 2点Core)"))
        cand_partners.sort(key=lambda x: (x[1] >= 2.6, x[1]), reverse=True)
        chosen = cand_partners[:2]
        core_pairs = [("wide", [h1["num"], p[0]["num"]], p[1], p[3], o1 >= 10 or p[2] >= 10) for p in chosen]
    elif o1 <= 2.2:
        core_pairs = [
            ("wide", [h1["num"], h2["num"]], w12, f"ワイド {h1['num']}-{h2['num']} (◎-◯ 3点Core)", o1 >= 10 or o2 >= 10),
            ("wide", [h1["num"], h3["num"]], w13, f"ワイド {h1['num']}-{h3['num']} (◎-▲ 3点Core)", o1 >= 10 or o3 >= 10),
        ]
        if h4["num"] != h3["num"]:
            core_pairs.append(("wide", [h1["num"], h4["num"]], w14, f"ワイド {h1['num']}-{h4['num']} (◎-{'人気馬' if forced_fav else '☆'} 3点Core)", o1 >= 10 or o4 >= 10))
    else:
        core_pairs = [
            ("wide", [h1["num"], h2["num"]], w12, f"ワイド {h1['num']}-{h2['num']} (◎-◯ Core)", o1 >= 10 or o2 >= 10),
            ("wide", [h1["num"], h3["num"]], w13, f"ワイド {h1['num']}-{h3['num']} (◎-▲ Core)", o1 >= 10 or o3 >= 10),
            ("wide", [h2["num"], h3["num"]], w23, f"ワイド {h2['num']}-{h3['num']} (◯-▲ タテ目防衛)", o2 >= 10 or o3 >= 10),
        ]
        if h4["num"] != h3["num"]:
            core_pairs.append(("wide", [h1["num"], h4["num"]], w14, f"ワイド {h1['num']}-{h4['num']} (◎-{'人気馬' if forced_fav else '☆'} 強制Core)", o1 >= 10 or o4 >= 10))

    inv_sum = sum(1.0 / max(1.1, p[2]) for p in core_pairs)
    core_synth_odds = round(1.0 / max(0.05, inv_sum), 2)
    avg_core_wide = round(sum(p[2] for p in core_pairs) / max(1, len(core_pairs)), 2)

    raw_w = [1.0 / max(1.1, p[2]) for p in core_pairs]
    sum_rw = max(1e-6, sum(raw_w))
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

    # Alpha 38% (3,800円): ◎単勝優先保護(1,400円) + 馬連2点(約1,600円) + 少点数3連複(約800円)
    row1 = [h1["num"], h2["num"]]
    row2 = sorted({h2["num"], h3["num"]})
    row3 = sorted({h3["num"], h4["num"]} | {x["num"] for x in himos})
    trio_set = {tuple(sorted((a, b, c))) for a in row1 for b in row2 if a != b for c in row3 if c != a and c != b}
    trio_pts = max(1, len(trio_set))
    trio_cap = int(round((alpha_budget * 0.22) / 100) * 100)
    trio_amt = min(max(400, trio_cap), trio_pts * 100)

    win_budget = max(400, int(round((alpha_budget * 0.37) / 100) * 100))
    if o1 >= 2.0 or o2 < 2.8:
        specs.append({"poolKey": "win", "nums": [h1["num"]], "amt": win_budget, "label": f"単勝 {h1['num']} (◎ {h1['name']} 本線保護)", "zone": "Alpha"})
    else:
        w1_amt = max(300, int(round((win_budget * (0.58 if o1 >= 1.5 else 0.45)) / 100) * 100))
        w2_amt = max(100, win_budget - w1_amt)
        specs.append({"poolKey": "win", "nums": [h1["num"]], "amt": w1_amt, "label": f"単勝 {h1['num']} (◎ {h1['name']} 本線保護)", "zone": "Alpha"})
        specs.append({"poolKey": "win", "nums": [h2["num"]], "amt": w2_amt, "label": f"単勝 {h2['num']} (◯ {h2['name']} 逆転Alpha)", "zone": "Alpha"})

    rem_umaren = max(200, alpha_budget - trio_amt - win_budget)
    u2_partner = h4 if (forced_fav and h4["num"] != h2["num"]) else h3
    u2_tag = "人気馬" if (forced_fav and h4["num"] != h2["num"]) else "▲"
    u12 = max(100, int(round((rem_umaren * 0.56) / 100) * 100))
    u13 = max(100, rem_umaren - u12)

    specs.append({"poolKey": "umaren", "nums": [h1["num"], h2["num"]], "amt": u12, "label": f"馬連 {h1['num']}-{h2['num']} (◎-◯ Alpha)", "zone": "Alpha"})
    specs.append({"poolKey": "umaren", "nums": [h1["num"], u2_partner["num"]], "amt": u13, "label": f"馬連 {h1['num']}-{u2_partner['num']} (◎-{u2_tag} Alpha)", "zone": "Alpha"})

    trio_meta = {"trioSet": trio_set, "trioPts": trio_pts, "trioAmt": trio_amt}

    top_ev_vals = []
    for h in sorted_h[:4]:
        od = float(h.get("odds", 0))
        if h.get("mark") not in ("消", "危") and 1.0 < od < 50.0:
            top_ev_vals.append((float(h.get("f", 0)) / 100.0) * od)
    max_ev = round(max(top_ev_vals), 2) if top_ev_vals else 0.0

    metrics = {
        "coreSyntheticOdds": core_synth_odds,
        "avgCoreWide": avg_core_wide,
        "coreLines": len(core_pairs),
        "maxEv": max_ev,
        "top1Odds": o1,
        "top2Odds": sorted([float(h.get("odds", 99)) for h in horses if float(h.get("odds", 99)) > 1.0])[:2],
        "coreConnections": [p[1] for p in core_pairs],
    }
    return specs, trio_meta, metrics

def compute_market_m3(horses: list) -> tuple[float, bool]:
    odds_list = [float(h.get("odds", 0)) for h in horses if float(h.get("odds", 0)) > 1.0]
    if len(odds_list) < 3:
        return 0.0, False
    has_spread = (max(odds_list) / max(1.0, min(odds_list))) >= 2.2
    inv_p = [math.pow(max(1.1, o), -1.08) for o in odds_list]
    s_inv = max(1e-6, sum(inv_p))
    q_sorted = sorted([x * 100.0 / s_inv for x in inv_p], reverse=True)
    return round(sum(q_sorted[:3]), 1), has_spread

def apply_auto_pass_and_rank(r: dict, is_historical: bool = False):
    """Code Patch P10: ◎1.4〜4.0倍の上位人気軸限定・障害完全除外・相手妙味(平均W/合成)×M3による逆選択ゼロ判定"""
    horses = r.get("horses") or []
    if len(horses) < 3:
        return

    normalize_prob_scale_list(horses)
    r["isGraded"] = detect_is_graded(r.get("name", ""), int(r.get("raceNumber", 0)))
    _, _, metrics = build_neon_core_shield_specs(r, B=10000)
    synth = metrics["coreSyntheticOdds"]
    avg_w = metrics["avgCoreWide"]
    max_ev = metrics["maxEv"]
    top2_o = metrics["top2Odds"]
    n_active = len(horses)
    is_nar = r.get("mode") == "nar"
    is_new = bool(r.get("isNew")) or r.get("skill") == "app-bayesian-make-debut" or "新馬" in str(r.get("name", ""))
    is_ai = bool(r.get("aiPredicted"))
    o1 = metrics["top1Odds"]

    m3_f = round(sum(sorted([float(h.get("f", 0)) for h in horses], reverse=True)[:3]), 1)
    m3_q, has_real_odds_spread = compute_market_m3(horses)
    is_pseudo_odds = (r.get("hasLiveOdds") is False) or (
        not is_ai and all(abs(float(h.get("f", 0)) - float(h.get("fFund", -1))) < 0.05 for h in horses[:4]) and not has_real_odds_spread
    )

    if is_historical and not is_pseudo_odds and m3_f < 42.0 and m3_q >= 46.0:
        m3_eval = round(0.35 * m3_f + 0.65 * m3_q, 1)
    else:
        m3_eval = m3_f

    r["m3"] = m3_eval
    r["maxEv"] = max_ev
    r["coreSyntheticOdds"] = synth
    r["avgCoreWide"] = avg_w
    r["coreConnections"] = metrics["coreConnections"]
    r["portfolioRules"] = {"coreRatio": 0.62, "alphaRatio": 0.38, "coreLineCap": metrics["coreLines"], "singleLongshotCapPct": 0.30}
    r["strategyProfile"] = "v12_balanced_roi"

    pass_reason = ""
    if is_obstacle_race(r.get("name", ""), r.get("surfaceDist", "")):
        pass_reason = "障害レース対象外見送り"
    elif is_nar and not is_nar_bettable_race(r):
        pass_reason = "NAR下級平場・対象外見送り(南関10-12R/重賞限定)"
    elif is_pseudo_odds:
        pass_reason = "ライブオッズ未取得のため見送り"
    elif n_active <= 8 and (avg_w < 3.0 or (len(top2_o) >= 2 and top2_o[0] <= 2.5 and top2_o[1] <= 2.5)):
        pass_reason = f"少頭数({n_active}頭)・低配当圧縮(平均W {avg_w}倍)"
    elif is_nar and len(top2_o) >= 1 and top2_o[0] <= 1.6 and avg_w < 2.8:
        pass_reason = f"NAR一強圧縮(1人気{top2_o[0]}倍・平均W {avg_w}倍)"
    elif is_new:
        if not (1.2 <= o1 <= 4.5):
            pass_reason = f"新馬◎オッズ{o1}倍が適正軸帯(1.2-4.5)外"
        elif synth < 1.08 or avg_w < 2.8:
            pass_reason = f"新馬低配当圧縮(合成{synth}倍/平均W {avg_w}倍)"
    else:
        # 赤字の7割を占めた◎4.1倍以上の中穴軸を遮断し、上位人気軸(1.4-4.0倍)×相手妙味のみを厳選
        if not (1.4 <= o1 <= 4.0):
            pass_reason = f"◎オッズ{o1}倍が上位軸適正帯(1.4-4.0)外"
        elif synth < 1.10 or avg_w < 3.0:
            pass_reason = f"Core低配当圧縮(合成{synth}倍/平均W {avg_w}倍)"
        elif m3_eval < 38.0:
            pass_reason = f"混戦カオス(M3 {m3_eval}%<38%)"

    if pass_reason:
        r["rank"] = "Pass"
        r["pivotType"] = "Pass"
        r["passReason"] = pass_reason
        r["investedYen"] = 0
        r["returnYen"] = 0
        r["actualRoi"] = 0.0
        r["isHit"] = False
        r["hitTickets"] = []
        r["evalDone"] = False
        if r.get("actualTop3"):
            r["resultStatus"] = f"💤 見送りPass ({pass_reason})"
        return

    r.pop("passReason", None)

    if is_new:
        r["rank"] = "New"
    elif (
        (1.5 <= o1 <= 3.8 and (avg_w >= 4.0 or synth >= 1.28) and m3_eval >= 46.0)
        or (is_ai and 1.5 <= o1 <= 4.0 and (avg_w >= 3.8 or synth >= 1.24) and m3_eval >= 44.0)
    ):
        r["rank"] = "S"
    else:
        r["rank"] = "A"

def evaluate_10k_payout(race: dict) -> dict:
    payouts, horses = race.get("payouts") or {}, race.get("horses") or []
    if not payouts or len(horses) < 3 or race.get("rank") in ("Pass", "B"):
        return {}
    B = 10000
    specs, trio_meta, _ = build_neon_core_shield_specs(race, B=B)
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
    if detect_is_g1(r.get("name", "")):
        return "g1_win5"
    if r.get("rank") == "S":
        return "high_h"
    if r.get("rank") == "New":
        return "med_h"
    if r.get("isGraded") and r.get("rank") == "A":
        return "high_h"
    return "flash"

def call_gemini(skill: str, prompt: str, tier: str = "flash", mode: str = "jra") -> dict:
    global AI_CALL_COUNT_JRA, AI_CALL_COUNT_NAR
    if time_exceeded():
        return {}

    if mode == "nar":
        if not nar_free_client:
            log("[NAR Free Guard] GEMINI_FREE_API_KEY未設定のためNARのAI呼出をスキップ（有料キー誤課金防止）")
            return {}
        if AI_CALL_COUNT_NAR >= MAX_AI_CALLS_NAR:
            return {}
        AI_CALL_COUNT_NAR += 1
        active_client = nar_free_client
        route_tag = "NAR-FREE"
        if tier in ("g1_win5", "high_h"):
            candidates = [(NAR_FREE_HIGH_MODEL, "HIGH"), (NAR_FREE_FAST_MODEL, "MEDIUM")]
        elif tier == "med_h":
            candidates = [(NAR_FREE_HIGH_MODEL, "MEDIUM"), (NAR_FREE_FAST_MODEL, "MEDIUM")]
        else:
            candidates = [(NAR_FREE_FAST_MODEL, "MEDIUM"), (NAR_FREE_HIGH_MODEL, "MEDIUM")]
    else:
        if not jra_client or AI_CALL_COUNT_JRA >= MAX_AI_CALLS_JRA:
            return {}
        AI_CALL_COUNT_JRA += 1
        active_client = jra_client
        route_tag = f"JRA-{AI_PLAN}"
        # Code Patch P12: WIN5・G1は安定したNeon(HIGH)を第一候補に固定
        if tier in ("g1_win5", "high_h"):
            candidates = [(JRA_WIN5_G1_MODEL, "HIGH"), (JRA_FAST_MODEL, "MEDIUM")]
        elif tier == "med_h":
            candidates = [(JRA_HIGH_MODEL, "MEDIUM"), (JRA_HIGH_MODEL, "HIGH")]
        else:
            candidates = [(JRA_FAST_MODEL, "MEDIUM"), (JRA_HIGH_MODEL, "HIGH")]

    p = f"skills/{skill}/SKILL.md"
    sys_inst = open(p, "r", encoding="utf-8").read() if os.path.exists(p) else "Output valid JSON only."

    dedup = []
    for c in candidates:
        if c not in dedup: dedup.append(c)

    for m, think_lvl in dedup:
        if time_exceeded():
            log("Time cap reached during AI fallback; stopping cleanly.")
            return {}
        try:
            log(f"Calling AI [{route_tag}]: {skill} -> {m}({think_lvl})")
            time.sleep(1.5)
            try:
                cfg = types.GenerateContentConfig(
                    system_instruction=sys_inst,
                    response_mime_type="application/json",
                    thinking_config=types.ThinkingConfig(thinking_level=think_lvl),
                )
            except Exception:
                cfg = types.GenerateContentConfig(system_instruction=sys_inst, response_mime_type="application/json")

            res = active_client.models.generate_content(model=m, contents=prompt, config=cfg)
            fence_pat = r"^\x60{3}(?:json)?\s*|\s*\x60{3}$"
            data = json.loads(re.sub(fence_pat, "", (res.text or "").strip(), flags=re.DOTALL))
            data["usedModel"] = f"{m}({think_lvl})"
            log(f"[AI Success {route_tag}] {skill} -> {data['usedModel']}")
            return data
        except Exception as e:
            log(f"[Fallback {route_tag}] {m}({think_lvl}): {str(e)[:120]}")
    return {}

def fetch_official_win5_ids(ymd: str = "", valid_ids: set | None = None) -> list:
    urls = []
    if ymd:
        urls.append(f"https://race.netkeiba.com/top/win5.html?kaisai_date={ymd}")
    urls.append("https://race.netkeiba.com/top/win5.html")

    for url in urls:
        try:
            soup = get_soup(url)
            for selector in (
                ".Win5_TargetRace a[href*='race_id='], .Win5RaceList a[href*='race_id='], .Win5_Table a[href*='race_id='], table a[href*='race_id=']",
                "a[href*='race_id=']",
            ):
                ids = []
                for a in soup.select(selector):
                    m = re.search(r"race_id=(\d{12})", a.get("href", ""))
                    if not m:
                        continue
                    rid = m.group(1)
                    if valid_ids is not None and rid not in valid_ids:
                        continue
                    if rid not in ids:
                        ids.append(rid)
                if len(ids) >= 5:
                    return ids[:5]
        except Exception:
            pass
    return []

def fetch_official_win5_payout(target_race_ids: list, ymd: str = "") -> int:
    urls = []
    if ymd:
        urls.append(f"https://race.netkeiba.com/top/win5.html?kaisai_date={ymd}")
    urls.append("https://race.netkeiba.com/top/win5.html")
    for url in urls:
        try:
            soup = get_soup(url)
            page_ids = set(re.findall(r"race_id=(\d{12})", str(soup)))
            if target_race_ids and sum(1 for rid in target_race_ids if rid in page_ids) < 3:
                continue
            txt = soup.get_text(" ", strip=True)
            m = re.search(r"(?:払戻金|配当)[^\d]{0,15}([\d,]{3,12})\s*円", txt)
            if m:
                val = int(m.group(1).replace(",", ""))
                if val >= 100:
                    return val
        except Exception:
            pass
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
        if isinstance(leg.get("horses"), list):
            normalize_prob_scale_list(leg["horses"])
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
        ymd = str(day_db.get("date", "")).replace("-", "")
        pay = fetch_official_win5_payout(leg_rids, ymd=ymd)
        if pay > 0: ml["officialPayout"] = pay

def build_multileg_with_ai(races: list, mode: str, date_str: str) -> dict:
    dt = datetime.strptime(date_str, "%Y-%m-%d")
    if mode == "nar":
        nankan_cand = [
            r for r in races
            if is_nankan_race(r) and r.get("raceNumber") in (10, 11, 12)
            and isinstance(r.get("horses"), list) and len(r["horses"]) >= 2
        ]
        by_venue = {}
        for r in nankan_cand:
            by_venue.setdefault(r["venue"], []).append(r)
        selected = []
        for v, v_list in by_venue.items():
            if len(v_list) >= 3:
                selected = sorted(v_list, key=lambda x: x["raceNumber"])[-3:]
                break
        if len(selected) < 3:
            return {}
    else:
        ymd = date_str.replace("-", "")
        valid_ids = {r["raceId"] for r in races if r.get("raceId")}
        off_ids = fetch_official_win5_ids(ymd=ymd, valid_ids=valid_ids)
        matched = [r for r in races if r["raceId"] in off_ids and isinstance(r.get("horses"), list) and len(r["horses"]) >= 2]
        if len(matched) == 5:
            selected = sorted(matched, key=lambda x: (x.get("postTime") or "15:00", x.get("raceNumber", 10)))
            log(f"[WIN5] Official 5 legs matched for {date_str}: {[x['venueLabel'] for x in selected]}")
        elif dt.weekday() == 6:
            pool = [
                r for r in races
                if (r.get("raceNumber") in (9, 10, 11) or detect_is_g1(r.get("name", "")))
                and isinstance(r.get("horses"), list) and len(r["horses"]) >= 2
            ]
            pool.sort(key=lambda x: (1 if detect_is_g1(x.get("name", "")) else 0, 1 if x["raceNumber"] >= 10 else 0, x["raceNumber"], x.get("postTime") or "14:30"), reverse=True)
            if len(pool) < 5: return {}
            selected = sorted(pool[:5], key=lambda x: (x.get("postTime") or "15:00", x["raceNumber"]))
        else:
            return {}

    all_finished = all(bool(r.get("actualTop3")) for r in selected)
    if mode == "jra" and len(selected) == 5 and not all_finished and not time_exceeded():
        blocks = []
        for idx, r in enumerate(selected):
            h_txt = "\n".join([f" {h['num']}番{h['name']}(脚質:{h['style']} 単勝:{h['odds']}倍 {h['comment']})" for h in r["horses"][:16]])
            blocks.append(f"=== Leg{idx+1} {r['venueLabel']} {r['name']} ({r['surfaceDist']} 発走{r.get('postTime','')}) ===\n{h_txt}")
        w_prompt = (
            f"日付:{date_str} のJRA WIN5対象5レースを Neon v11.3（2-Stage Benter融合・単勝50倍超Core中核禁止・乾燥ダート上位4頭差し枠・来日外国馬wR=0.55-0.60・Plan C直交翼の4〜6番手/単勝5〜15倍帯中穴優先編入）で一括推論せよ。\n"
            "【重要】f, fFund, q は必ず 0.0〜100.0 のパーセント表記（例: 23.5。0.235のような小数表記は絶対禁止）で以下のJSONスキーマで出力せよ:\n"
            "{\"summary\":\"5レース全体の攻略総括(100字以内)\",\"legs\":[{\"leg\":1,\"venue\":\"会場R\",\"name\":\"レース名\",\"postTime\":\"HH:MM\",\"wR\":0.40,\"typeBPlus\":true/false,\"note\":\"展開・バイアス見解(45字以内)\",\"horses\":[{\"num\":馬番,\"name\":\"馬名\",\"f\":23.5,\"fFund\":21.0,\"q\":25.0,\"odds\":3.2,\"shell\":\"Core|Wing\",\"note\":\"F/H根拠(30字以内)\"}]}],\"hedges\":[{\"num\":馬番,\"name\":\"Leg5伏兵名\",\"odds\":オッズ,\"hedge50k\":円,\"hedge100k\":円}]}\n\n"
            + "\n".join(blocks)
        )
        ai_w = call_gemini("app-bayesian-win5", w_prompt, tier="g1_win5", mode="jra")
        if isinstance(ai_w, dict) and isinstance(ai_w.get("legs"), list) and len(ai_w["legs"]) == 5:
            ai_w["predicted"] = True; ai_w["aiPredicted"] = True; ai_w["date"] = date_str; ai_w["engineVer"] = ENGINE_VER
            for idx, r in enumerate(selected):
                leg_obj = ai_w["legs"][idx]
                leg_obj["raceId"], leg_obj["venue"], leg_obj["name"] = r["raceId"], r["venueLabel"], r["name"]
                leg_obj["postTime"] = r.get("postTime", leg_obj.get("postTime", ""))
                leg_hs = leg_obj.get("horses") or []
                # Code Patch P12: WIN5の小数(0.232)出力バグを自動でパーセント(23.2)へ補正
                normalize_prob_scale_list(leg_hs)

                by_num = {int(h["num"]): h for h in leg_hs if str(h.get("num","")).isdigit()}
                if by_num:
                    for h in r["horses"]:
                        if h["num"] in by_num:
                            ah = by_num[h["num"]]
                            if ah.get("fFund") is not None: h["fFund"] = round(float(ah["fFund"]), 1)
                            elif ah.get("f") is not None: h["fFund"] = round(float(ah["f"]), 1)
                            if ah.get("f") is not None: h["f"] = round(float(ah["f"]), 1)
                            if ah.get("note"): h["comment"] = ah["note"]
                    # Python側で厳密2-Stage Benter融合を実行し、WIN5と個別レースの見解を完全一致させる
                    apply_python_benter_fusion(r, w_mkt_base=0.50)
                    r["aiPredicted"] = True
                    r["usedModel"] = ai_w.get("usedModel", f"{JRA_WIN5_G1_MODEL}(HIGH)")
                    if leg_obj.get("note"): r["scenario"] = leg_obj["note"]
                    apply_auto_pass_and_rank(r)

                    # 融合済みの正規化上位7頭をWIN5 Leg表示へ書き戻す（100%整合・小数バグ完全消滅）
                    leg_obj["horses"] = [{
                        "num": h["num"], "name": h["name"],
                        "f": float(h["f"]), "fFund": float(h.get("fFund", h["f"])),
                        "q": float(h.get("q", 10.0)), "odds": float(h.get("odds", 5.5)),
                        "note": str(h.get("comment", ""))[:34]
                    } for h in r["horses"][:7]]
            return ai_w

    legs = []
    for idx, r in enumerate(selected):
        hs = sorted(r["horses"], key=lambda x: float(x.get("f", 10)), reverse=True)
        legs.append({
            "leg": idx + 1, "raceId": r["raceId"], "venue": r["venueLabel"], "name": r["name"], "cond": r.get("surfaceDist") or "ダ1400m",
            "postTime": r.get("postTime", ""), "wR": r.get("wR", 0.50),
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
    return {"predicted": True, "aiPredicted": False, "date": date_str, "engineVer": ENGINE_VER, "summary": f"【{date_str} Neon v12.0 2-Stage融合編成（{'南関トリプル馬単50円単位' if mode=='nar' else 'JRA WIN5 Plan A/C直交3枚対応'}）】", "legs": legs, "hedges": hedges}

def should_check_result(date_str: str, post_time: str, now: datetime) -> bool:
    today_str = now.strftime("%Y-%m-%d")
    if date_str < today_str: return True
    if date_str > today_str: return False
    if re.match(r"^\d{2}:\d{2}$", post_time or ""):
        pdt = datetime.strptime(f"{date_str} {post_time}", "%Y-%m-%d %H:%M").replace(tzinfo=JST)
        return now >= (pdt + timedelta(minutes=5))
    return now.hour >= 10

def is_pre_post_window(date_str: str, post_time: str, now: datetime, low_m: int = 10, high_m: int = 90) -> bool:
    if date_str != now.strftime("%Y-%m-%d"): return False
    if not re.match(r"^\d{2}:\d{2}$", post_time or ""): return False
    pdt = datetime.strptime(f"{date_str} {post_time}", "%Y-%m-%d %H:%M").replace(tzinfo=JST)
    mins = (pdt - now).total_seconds() / 60.0
    return low_m <= mins <= high_m

def process_kaisai_day(date_str: str, races: list, now: datetime, is_today: bool, mode: str = "jra"):
    route_desc = f"JRA:{AI_PLAN}" if mode == "jra" else ("NAR:free" if nar_free_client else "NAR:baseline-only")
    log(f"Processing {date_str} ({mode}, fetched={len(races)} races, route={route_desc})")
    suffix = "_nar" if mode == "nar" else ""
    db_path = f"data/{date_str}{suffix}.json"
    day_db = json.load(open(db_path, "r", encoding="utf-8")) if os.path.exists(db_path) else {"date": date_str, "mode": mode, "races": races}

    if not day_db.get("races") and races:
        day_db["races"] = races
    elif races:
        existing_ids = {r.get("raceId") for r in day_db.get("races", [])}
        added = [r for r in races if r.get("raceId") not in existing_ids]
        if added:
            log(f"[Merge] Added {len(added)} newly published races to {date_str}")
            day_db["races"].extend(added)
            day_db["races"].sort(key=lambda x: (x.get("venue", ""), int(x.get("raceNumber", 0))))
    day_db["mode"] = mode

    # 障害レース・ばんえい帯広をキャッシュから除外
    day_db["races"] = [
        r for r in day_db.get("races", [])
        if not is_obstacle_race(r.get("name", ""), r.get("surfaceDist", ""))
        and not (mode == "nar" and (str(r.get("raceId", ""))[4:6] in BANEI_CODES or r.get("venue") == "地方"))
    ]
    if mode == "nar":
        cur_ml = day_db.get("multiLeg")
        if isinstance(cur_ml, dict) and isinstance(cur_ml.get("legs"), list):
            if any(not any(nv in str(lg.get("venue", "")) for nv in NANKAN_NAMES) for lg in cur_ml["legs"]):
                day_db.pop("multiLeg", None)

    for r in day_db.get("races", []):
        if time_exceeded():
            log("Time cap reached in scraping loop; saving progress.")
            break
        contaminated = has_contaminated_cache(r)
        if contaminated:
            log(f"[Purge] Contaminated cache in {r.get('venueLabel')} {r.get('name')} -> refreshing")
            r["horses"] = []
            r["evalDone"] = False

        has_real = isinstance(r.get("horses"), list) and len(r["horses"]) >= 5
        has_neon = has_real and ("fFund" in r["horses"][0])
        is_unsettled = not bool(r.get("actualTop3"))
        need_ver_refresh = is_unsettled and (not r.get("aiPredicted")) and (day_db.get("engineVer") != ENGINE_VER)
        missing_live_odds = is_unsettled and (
            (has_neon and float(r.get("wR", 0)) == 0.0)
            or (r.get("hasLiveOdds") is False)
            or ("ライブオッズ未取得" in str(r.get("passReason", "")))
        )
        missing_dist = (not r.get("surfaceDist")) or (mode == "nar" and r.get("surfaceDist") == "ダ1600m" and day_db.get("engineVer") != ENGINE_VER)
        bad_time = (not r.get("postTime")) or (r.get("postTime") == "15:00" and r.get("raceNumber", 11) < 10)
        can_have_result = should_check_result(date_str, r.get("postTime", ""), now)
        need_res = can_have_result and ((not r.get("evalDone") and r.get("rank") != "Pass") or is_unsettled or contaminated)
        in_live_win = is_today and is_pre_post_window(date_str, r.get("postTime", ""), now, 10, 95)
        need_live_refresh = in_live_win and (not r.get("weightsAnnounced") or not r.get("wideOddsMap") or missing_live_odds)
        need_sh = contaminated or (not has_real) or bad_time or missing_dist or missing_live_odds or need_ver_refresh or (not has_neon and is_unsettled) or need_live_refresh

        if need_sh or need_res:
            detail, actual, raw_runners, track_cond, ptime, payouts, wide_map, weights_ready, fetched_sd = fetch_full_shutuba(
                r["raceId"], mode=mode, need_shutuba=need_sh, need_result=need_res
            )
            if ptime: r["postTime"] = ptime
            if fetched_sd: r["surfaceDist"] = fetched_sd
            elif not r.get("surfaceDist"): r["surfaceDist"] = "ダ1400m" if mode == "nar" else "ダ1600m"

            if raw_runners and need_sh:
                base_horses, n_lead, scen_w, neon_meta = compute_bayesian_full_field(raw_runners, r, track_cond=track_cond)
                r["nLead"], r["trackCond"], r["scenarioWeights"] = n_lead, track_cond, scen_w
                if wide_map:
                    top_nums = {h["num"] for h in base_horses[:10]}
                    r["wideOddsMap"] = {
                        k: v for k, v in wide_map.items()
                        if all(int(x) in top_nums for x in k.split("-"))
                    }
                if weights_ready:
                    r["weightsAnnounced"] = True
                if not has_real or not r.get("aiPredicted") or contaminated:
                    r["horses"] = base_horses
                    r["predicted"] = True
                    r.update(neon_meta)
                    r["scenario"] = f"{r['venueLabel']}({r['surfaceDist']}・{track_cond}) 実測N_lead={n_lead}頭 / 2-Stage融合(wR={neon_meta['wR']}, M3={neon_meta['m3']}%)。3シナリオ混合(S1:{scen_w['s1']}% / S2:{scen_w['s2']}% / S3:{scen_w['s3']}%)で全{len(base_horses)}頭を厳密演算。"
                else:
                    by_num_raw = {x["num"]: x for x in raw_runners}
                    r["horses"] = [h for h in r["horses"] if h["num"] in by_num_raw]
                    for h in r["horses"]:
                        rw = by_num_raw[h["num"]]
                        h["name"] = rw["name"]
                        if rw.get("odds", 0) > 1.0: h["odds"] = round(float(rw["odds"]), 1)
                        if rw.get("weight"): h["weight"] = rw["weight"]
                    r["hasLiveOdds"] = neon_meta.get("hasLiveOdds", True)
                    # オッズ更新時にPython側2-Stage融合も最新オッズへ再同期
                    apply_python_benter_fusion(r, w_mkt_base=(0.52 if r.get("isNew") else 0.55))
                r["detailText"] = detail
            if actual: r["actualTop3"] = actual
            if payouts and any(payouts.values()):
                r["payouts"] = payouts

        if r.get("horses") and (not r.get("evalDone") or contaminated or day_db.get("engineVer") != ENGINE_VER or missing_live_odds):
            apply_auto_pass_and_rank(r, is_historical=bool(r.get("actualTop3")))

        if r.get("payouts") and any(r["payouts"].values()) and r.get("rank") not in ("Pass", "B"):
            if not r.get("evalDone") or contaminated or day_db.get("engineVer") != ENGINE_VER:
                ev = evaluate_10k_payout(r)
                if ev:
                    r.update(ev); r["evalDone"] = True
                    prof = ev["returnYen"] - ev["investedYen"]
                    r["resultStatus"] = f"🎯 的中 払戻{ev['returnYen']:,}円 (回収率{ev['actualRoi']}% / {prof:+,}円)" if ev["isHit"] else f"❌ 不的中 回収率0.0%"

    is_past_day = date_str < now.strftime("%Y-%m-%d")
    if not time_exceeded():
        cur_ml = day_db.get("multiLeg") or {}
        has_ml = isinstance(cur_ml.get("legs"), list) and len(cur_ml["legs"]) >= 3
        need_ml_ai = (
            (not has_ml and not is_past_day)
            or (has_ml and not cur_ml.get("aiPredicted") and not is_past_day)
            or (has_ml and not is_past_day and cur_ml.get("engineVer") != ENGINE_VER and JRA_WIN5_G1_MODEL not in str(cur_ml.get("usedModel", "")))
        )
        if need_ml_ai:
            mleg = build_multileg_with_ai(day_db.get("races", []), mode, date_str)
            if mleg: day_db["multiLeg"] = mleg

    can_call_ai = (jra_client is not None) if mode == "jra" else (nar_free_client is not None)
    ai_candidates = []
    if can_call_ai:
        for r in day_db.get("races", []):
            if not r.get("horses") or r.get("actualTop3"):
                continue
            is_target_nankan_ml = (mode == "nar") and is_nankan_race(r) and r.get("raceNumber") in (10, 11, 12)
            if r.get("hasLiveOdds") is False and not (r.get("isGraded") or r.get("isNew")):
                continue
            is_promising_pre = (r.get("rank") in ("S", "A", "New")) or r.get("isGraded") or is_target_nankan_ml
            if not is_promising_pre:
                continue
            if r.get("rank") == "Pass" and not (r.get("isGraded") or is_target_nankan_ml):
                continue
            tier = classify_race_tier(r)
            used = str(r.get("usedModel", ""))
            if mode == "nar":
                target_model = NAR_FREE_HIGH_MODEL if tier in ("g1_win5", "high_h", "med_h") else NAR_FREE_FAST_MODEL
            else:
                target_model = JRA_WIN5_G1_MODEL if tier == "g1_win5" else (JRA_HIGH_MODEL if tier in ("high_h", "med_h") else JRA_FAST_MODEL)
            need_weight_repredict = bool(r.get("weightsAnnounced")) and not bool(r.get("aiPredictedWithWeights"))
            needs_ai = (not r.get("aiPredicted")) or (target_model not in used) or need_weight_repredict
            if not needs_ai:
                continue
            prio = -8 if r.get("rank") == "S" else (-5 if r.get("rank") == "New" else (-3 if r.get("rank") == "A" else 0))
            if r.get("isGraded"): prio -= 2
            if is_target_nankan_ml: prio -= 1
            if is_today and is_pre_post_window(date_str, r.get("postTime", ""), now, 12, 95):
                prio -= 12
                if need_weight_repredict:
                    prio -= 4
            ai_candidates.append((prio, tier, r))

    ai_candidates.sort(key=lambda x: x[0])
    per_day_limit = 3 if mode == "nar" else (8 if (is_today and AI_PLAN != "free") else (5 if AI_PLAN != "free" else 4))
    for _, tier, r in ai_candidates[:per_day_limit]:
        cur_cnt = AI_CALL_COUNT_NAR if mode == "nar" else AI_CALL_COUNT_JRA
        cur_max = MAX_AI_CALLS_NAR if mode == "nar" else MAX_AI_CALLS_JRA
        if cur_cnt >= cur_max or time_exceeded(): break
        bias_info, bias_cnt = summarize_intraday_track_bias(day_db.get("races", []), r["venue"])
        detail = r.pop("detailText", "") or "\n".join([f"{h['num']}番{h['name']}(脚質:{h['style']} 単勝:{h['odds']}倍 馬体:{h.get('weight','未発表')} {h['comment']})" for h in r["horses"]])
        wt_note = "公式馬体重発表済（Type I〜III・1800m+の+12kg+・ダート新馬<420kg補正必須）" if r.get("weightsAnnounced") else "馬体重未発表"
        pred = call_gemini(
            r["skill"],
            f"【モード: 標準（Neon v12.0 上位軸1.4〜4.0倍×Core62%/Alpha38%・全頭評価 / {wt_note}）】日付:{date_str} {r['venueLabel']} {r['name']} ({r['surfaceDist']}・{r.get('trackCond','良')}・{len(r['horses'])}頭)\n"
            f"【当日バイアス(3R一致ガード)】{bias_info}\n"
            f"【重要厳守】f, fFund, top2, top3 は必ず 0.0〜100.0 のパーセント表記（小数禁止）。単勝4.5倍以下の1〜2番人気を明確な馬体失格なしに全消し・消扱いしてはならない。単勝8倍以上の馬のfは18%上限。\n"
            f"全頭について mark, role, style, f(融合後勝率%), fFund(オッズ遮断基礎勝率%), wUsed(市場重み), top2, top3, comment(35字以内) と、"
            f"scenario, pivotType, rank, wR, m3, coreSyntheticOdds, hitRate, breakEvenRate, expectedRoi, coreConnections([[◎番,◯番],...]), counterfactualAudit(60字以内) をJSON出力せよ:\n{detail}",
            tier=tier,
            mode=mode,
        )
        if isinstance(pred, dict) and "horses" in pred:
            pred_hs = pred["horses"]
            normalize_prob_scale_list(pred_hs)
            by_num_cur = {int(h["num"]): h for h in r["horses"] if str(h.get("num", "")).isdigit()}
            by_norm_name = {normalize_horse_name(h["name"]): h for h in r["horses"]}
            for ah in pred_hs:
                t = None
                if str(ah.get("num", "")).isdigit():
                    t = by_num_cur.get(int(ah["num"]))
                if not t and ah.get("name"):
                    t = by_norm_name.get(normalize_horse_name(str(ah["name"])))
                if t:
                    for k in ("mark", "role", "style", "comment"):
                        if ah.get(k): t[k] = ah[k]
                    if ah.get("fFund") is not None:
                        t["fFund"] = round(float(ah["fFund"]), 1)
                    elif ah.get("f") is not None:
                        t["fFund"] = round(float(ah["f"]), 1)
                    for k in ("f", "top2", "top3"):
                        if ah.get(k) is not None: t[k] = round(float(ah[k]), 1)
                    if ah.get("wUsed") is not None: t["wUsed"] = round(float(ah["wUsed"]), 2)

            # Code Patch P9: Python側で実オッズqとの厳密2-Stage Benter融合＆過大評価キャップを強制実行
            w_base = 0.52 if r.get("isNew") else (0.50 if r.get("isGraded") else 0.55)
            apply_python_benter_fusion(r, w_mkt_base=w_base)

            ai_explicit_pass = (pred.get("rank") == "Pass")
            for k in ("scenario", "pivotType", "usedModel", "hitRate", "breakEvenRate", "expectedRoi", "counterfactualAudit"):
                if k in pred and pred[k] is not None:
                    r[k] = pred[k]
            r["intradayBiasConsistentR"] = bias_cnt
            r["aiPredicted"] = True
            if r.get("weightsAnnounced"):
                r["aiPredictedWithWeights"] = True
            if ai_explicit_pass:
                r["rank"] = "Pass"
                r["pivotType"] = "Pass"
                r["passReason"] = "AI本推論見送り判定"
            else:
                apply_auto_pass_and_rank(r, is_historical=False)

    sync_multileg_results(day_db, mode)

    for r in day_db.get("races", []): r.pop("detailText", None)
    venues = sorted(list({r["venue"] for r in day_db.get("races", [])}))
    day_db["trackBiases"] = []
    for v in venues:
        b_txt, b_cnt = summarize_intraday_track_bias(day_db.get("races", []), v)
        day_db["trackBiases"].append({"venue": v, "surf": f"Neon v12.0 ({route_desc})", "trend": b_txt, "consistentR": b_cnt})
    day_db["engineVer"] = ENGINE_VER
    day_db["aiPlan"] = f"JRA:{AI_PLAN}(Neon統一) / NAR:無料枠"
    day_db["updatedAt"] = now.strftime("%Y-%m-%d %H:%M JST")
    json.dump(day_db, open(db_path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    log(f"Saved {db_path}")

def recalibrate_historical_data(now: datetime):
    updated_cnt = 0
    for fp in sorted(glob.glob("data/20*.json")):
        try:
            d = json.load(open(fp, "r", encoding="utf-8"))
            if d.get("engineVer") == ENGINE_VER:
                continue
            is_nar = d.get("mode") == "nar" or fp.endswith("_nar.json")
            # 障害戦・ばんえい帯広をパージ
            d["races"] = [
                r for r in d.get("races", [])
                if not is_obstacle_race(r.get("name", ""), r.get("surfaceDist", ""))
                and not (is_nar and (str(r.get("raceId", ""))[4:6] in BANEI_CODES or r.get("venue") == "地方"))
            ]
            # 過去WIN5の小数スケールバグ(0.232%)を自動修復
            ml = d.get("multiLeg")
            if isinstance(ml, dict) and isinstance(ml.get("legs"), list):
                if is_nar and any(not any(nv in str(lg.get("venue", "")) for nv in NANKAN_NAMES) for lg in ml["legs"]):
                    d.pop("multiLeg", None)
                else:
                    for lg in ml["legs"]:
                        if isinstance(lg.get("horses"), list):
                            normalize_prob_scale_list(lg["horses"])

            for r in d.get("races", []):
                if not r.get("horses"):
                    r["isGraded"] = detect_is_graded(r.get("name", ""), int(r.get("raceNumber", 0)))
                    continue
                apply_auto_pass_and_rank(r, is_historical=True)
                if r.get("rank") not in ("Pass", "B") and r.get("payouts") and any(r["payouts"].values()):
                    ev = evaluate_10k_payout(r)
                    if ev:
                        r.update(ev); r["evalDone"] = True
                        prof = ev["returnYen"] - ev["investedYen"]
                        r["resultStatus"] = f"🎯 的中 払戻{ev['returnYen']:,}円 (回収率{ev['actualRoi']}% / {prof:+,}円)" if ev["isHit"] else f"❌ 不的中 回収率0.0%"
            d["engineVer"] = ENGINE_VER
            json.dump(d, open(fp, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
            updated_cnt += 1
        except Exception as e:
            log(f"[Warn] recalibrate {fp}: {e}")
    if updated_cnt > 0:
        log(f"Recalibrated {updated_cnt} historical files to {ENGINE_VER}.")

def empty_scope_stats() -> dict:
    return {
        "races": 0, "hits": 0, "invest": 0, "ret": 0, "passCount": 0, "passSaved": 0,
        "byRank": {rk: {"races": 0, "hits": 0, "invest": 0, "ret": 0} for rk in ("S", "A", "New", "B")},
        "bySource": {
            "ai": {"races": 0, "hits": 0, "invest": 0, "ret": 0},
            "baseline": {"races": 0, "hits": 0, "invest": 0, "ret": 0}
        }
    }

def update_global_stats(now: datetime):
    scopes = {"all": empty_scope_stats(), "jra": empty_scope_stats(), "nar": empty_scope_stats()}
    recent, daily_trend = [], []
    for fp in sorted(glob.glob("data/20*.json"), reverse=True):
        try:
            d = json.load(open(fp, "r", encoding="utf-8"))
            is_nar = d.get("mode") == "nar" or fp.endswith("_nar.json")
            mode_key = "nar" if is_nar else "jra"
            day_races, day_hits, day_inv, day_ret = 0, 0, 0, 0
            for r in d.get("races", []):
                if is_obstacle_race(r.get("name", ""), r.get("surfaceDist", "")):
                    continue
                if is_nar and (str(r.get("raceId", ""))[4:6] in BANEI_CODES or r.get("venue") == "地方"):
                    continue
                rk_raw = r.get("rank", "Pass")
                if rk_raw in ("Pass", "B"):
                    for sk in ("all", mode_key):
                        scopes[sk]["passCount"] += 1
                        scopes[sk]["passSaved"] += 10000
                elif r.get("evalDone") and r.get("investedYen"):
                    rk = rk_raw if rk_raw in ("S", "A", "New") else "A"
                    src_k = "ai" if r.get("aiPredicted") else "baseline"
                    inv, ret = int(r["investedYen"]), int(r.get("returnYen", 0))
                    is_hit = ret > 0
                    day_races += 1; day_inv += inv; day_ret += ret
                    if is_hit: day_hits += 1
                    for sk in ("all", mode_key):
                        b = scopes[sk]
                        b["races"] += 1; b["invest"] += inv; b["ret"] += ret
                        if is_hit: b["hits"] += 1
                        rb = b["byRank"][rk]
                        rb["races"] += 1; rb["invest"] += inv; rb["ret"] += ret
                        if is_hit: rb["hits"] += 1
                        sb = b["bySource"][src_k]
                        sb["races"] += 1; sb["invest"] += inv; sb["ret"] += ret
                        if is_hit: sb["hits"] += 1
                    if len(recent) < 50:
                        recent.append({
                            "date": d.get("date", ""), "mode": mode_key, "rank": rk,
                            "isGraded": bool(r.get("isGraded")),
                            "ai": bool(r.get("aiPredicted")),
                            "race": f"{r['venueLabel']} {r['name']}",
                            "status": r.get("resultStatus", ""),
                            "roi": float(r.get("actualRoi", 0)),
                            "returnYen": ret, "investedYen": inv, "isHit": is_hit,
                            "hits": r.get("hitTickets", [])
                        })
            if day_races > 0:
                daily_trend.append({
                    "date": d.get("date", ""), "mode": mode_key,
                    "races": day_races, "hits": day_hits, "invest": day_inv, "ret": day_ret,
                    "roi": round(day_ret * 100.0 / max(1, day_inv), 1)
                })
        except Exception: pass
    payload = {
        "updatedAt": now.strftime("%Y-%m-%d %H:%M JST"),
        "aiPlan": f"JRA:Neon統一 / NAR:{'無料枠' if nar_free_client else '無料キー待機'}",
        **scopes,
        "dailyTrend": daily_trend[:12],
        "recentResults": recent
    }
    json.dump(payload, open("data/stats.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    log("Updated data/stats.json")

def run_pipeline():
    now = datetime.now(JST)
    log(f"Pipeline start ({ENGINE_VER}, JRA={AI_PLAN}/Neon max={MAX_AI_CALLS_JRA}, NAR={'FREE' if nar_free_client else 'NO-FREE-KEY'} max={MAX_AI_CALLS_NAR}) at {now.strftime('%Y-%m-%d %H:%M JST')}")
    is_weekend = now.weekday() in (5, 6)
    is_weekend_jra_hours = is_weekend and (8 <= now.hour < 17)

    if not is_weekend:
        for off in [0, -1, 1]:
            if time_exceeded(): break
            dt = now + timedelta(days=off)
            n_races = fetch_race_list(dt.strftime("%Y%m%d"), "nar")
            if len(n_races) >= 3:
                process_kaisai_day(dt.strftime("%Y-%m-%d"), n_races, now, off == 0, "nar")
                break

    upcoming_days = []
    for off in [0, 1, 2, 3, 4, 5]:
        if time_exceeded(): break
        dt = now + timedelta(days=off)
        rs = fetch_race_list(dt.strftime("%Y%m%d"), "jra")
        if len(rs) >= 6:
            upcoming_days.append((dt, rs, off == 0))
            if len(upcoming_days) >= 2: break

    upcoming_days.sort(key=lambda x: (0 if x[2] else 1, 0 if x[0].weekday() == 6 else 1))
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

    if is_weekend and not is_weekend_jra_hours and not time_exceeded():
        for off in [0, -1, 1]:
            if time_exceeded(): break
            dt = now + timedelta(days=off)
            n_races = fetch_race_list(dt.strftime("%Y%m%d"), "nar")
            if len(n_races) >= 3:
                process_kaisai_day(dt.strftime("%Y-%m-%d"), n_races, now, off == 0, "nar")
                break

    recalibrate_historical_data(now)
    update_global_stats(now)

    jra_files = sorted([os.path.basename(p).replace(".json", "") for p in glob.glob("data/20*.json") if not p.endswith("_nar.json")])
    nar_files = sorted([os.path.basename(p).replace(".json", "") for p in glob.glob("data/20*_nar.json")])
    json.dump({"availableDates": jra_files, "narDates": nar_files, "lastSync": now.strftime("%Y-%m-%d %H:%M JST")}, open("data/index.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    log("Pipeline finished successfully.")

if __name__ == "__main__":
    run_pipeline()
# === END OF FILE ===
