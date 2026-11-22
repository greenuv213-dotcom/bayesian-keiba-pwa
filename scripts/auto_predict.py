#!/usr/bin/env python3
"""
Bayesian Keiba AI — Automated Prediction & Audit Pipeline (Neon v7.0 / Hydrogen Hybrid / Direct-Scrape Edition)

Free-Tier Safe Architecture:
  - Scrapes real JRA / NAR race lists, full-field shutuba (horses, jockeys, weights, odds),
    and official results/payouts directly via requests + BeautifulSoup (no Google Search Grounding quota required).
  - Model Routing:
      * High Tier (WIN5 / Grade / Make Debut / S-A / Triple Umatan): gemini-4-hydrogen (thinking_level="high")
      * Fast Tier (Screening / Standard Races / Audit)             : gemini-3.8-flash  (thinking_level="medium")
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import sys
import time
from pathlib import Path
from typing import Any

import requests
from bs4 import BeautifulSoup
from google import genai
from google.genai import types

# ===== 設定（環境変数・GitHub Variables で上書き可能）=====
HIGH_TIER_MODEL = os.getenv("GEMINI_HIGH_TIER_MODEL", "gemini-4-hydrogen")
FAST_MODEL = os.getenv("GEMINI_FAST_MODEL", "gemini-3.8-flash")
ENABLE_GOOGLE_SEARCH = os.getenv("ENABLE_GOOGLE_SEARCH", "false").lower() == "true"

DATA_DIR = Path(os.getenv("KEIBA_DATA_DIR", "data"))
LATEST_JSON_PATH = DATA_DIR / "latest.json"
HISTORY_DIR = DATA_DIR / "history"
JST = dt.timezone(dt.timedelta(hours=9))

HOURLY_WINDOW_MIN = 20
HOURLY_WINDOW_MAX = 105
REQUEST_INTERVAL_SEC = 4.0

HTTP_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "ja,en-US;q=0.9,en;q=0.8",
}

NAR_VENUES = (
    "大井", "川崎", "船橋", "浦和",
    "門別", "盛岡", "水沢", "金沢", "笠松", "名古屋", "園田", "姫路", "高知", "佐賀",
)
NANKAN_VENUES = ("大井", "川崎", "船橋", "浦和")


def now_jst() -> dt.datetime:
    return dt.datetime.now(JST)


def now_jst_str() -> str:
    return now_jst().strftime("%Y-%m-%d %H:%M JST")


def detect_org(race: dict[str, Any]) -> str:
    org = str(race.get("org") or "").upper()
    if org in ("JRA", "NAR"):
        return org
    skill = str(race.get("skill") or "")
    if "nar" in skill:
        return "NAR"
    venue = str(race.get("venue") or "")
    if any(v in venue for v in NAR_VENUES):
        return "NAR"
    return "JRA"


def select_model_and_thinking(skill: str, race_name: str = "", rank: str = "") -> tuple[str, str]:
    high_keywords = ("G1", "G2", "G3", "GI", "GII", "GIII", "Jpn", "重賞", "新馬", "WIN5", "記念", "賞", "杯")
    if skill in ("app-bayesian-win5", "app-bayesian-make-debut"):
        return HIGH_TIER_MODEL, "high"
    if rank in ("S", "A") or any(k in race_name for k in high_keywords):
        return HIGH_TIER_MODEL, "high"
    return FAST_MODEL, "medium"


def parse_post_datetime(date_str: str, post_time: str) -> dt.datetime | None:
    if not post_time:
        return None
    m = re.search(r"(\d{1,2})\s*[:：時]\s*(\d{2})", str(post_time))
    if not m:
        return None
    try:
        year, month, day = map(int, date_str.split("-"))
        return dt.datetime(year, month, day, int(m.group(1)), int(m.group(2)), tzinfo=JST)
    except ValueError:
        return None


def minutes_until_post(date_str: str, post_time: str, ref_now: dt.datetime | None = None) -> float | None:
    post_dt = parse_post_datetime(date_str, post_time)
    if post_dt is None:
        return None
    ref = ref_now or now_jst()
    return (post_dt - ref).total_seconds() / 60.0


# ===== 直接スクレイピング（netkeiba JRA / NAR）=====
def fetch_soup(url: str, timeout: int = 15) -> BeautifulSoup | None:
    try:
        resp = requests.get(url, headers=HTTP_HEADERS, timeout=timeout)
        if resp.status_code != 200:
            print(f"[HTTP {resp.status_code}] {url}", file=sys.stderr)
            return None
        resp.encoding = resp.apparent_encoding or "euc-jp"
        return BeautifulSoup(resp.text, "html.parser")
    except Exception as exc:
        print(f"[FETCH WARN] {url}: {exc}", file=sys.stderr)
        return None


def scrape_race_list(org: str, date_str: str) -> list[dict[str, Any]]:
    """指定日の JRA / NAR 開催レース一覧を netkeiba から直接取得"""
    ymd = date_str.replace("-", "")
    host = "nar.netkeiba.com" if org == "NAR" else "race.netkeiba.com"
    url = f"https://{host}/top/race_list_sub.html?kaisai_date={ymd}"
    soup = fetch_soup(url)
    if soup is None:
        return []

    races: list[dict[str, Any]] = []
    seen_ids: set[str] = set()

    for dl in soup.select("dl.RaceList_DataList"):
        title_el = dl.select_one(".RaceList_DataTitle")
        venue_raw = title_el.get_text(" ", strip=True) if title_el else ""
        # 例: "5回 東京 7日目" -> "東京" / "大井" -> "大井"
        venue_short = ""
        for cand in (
            "東京", "中山", "京都", "阪神", "中京", "新潟", "福島", "小倉", "札幌", "函館",
            *NAR_VENUES,
        ):
            if cand in venue_raw:
                venue_short = cand
                break
        if not venue_short:
            venue_short = venue_raw.split()[0] if venue_raw else org

        for item in dl.select("li.RaceList_DataItem"):
            link = item.select_one("a[href*='race_id=']")
            if not link:
                continue
            href = str(link.get("href") or "")
            m_id = re.search(r"race_id=(\d{12})", href)
            if not m_id:
                continue
            race_id = m_id.group(1)
            if race_id in seen_ids:
                continue
            seen_ids.add(race_id)

            rnum_el = item.select_one(".Race_Num")
            rnum_text = rnum_el.get_text(strip=True) if rnum_el else ""
            m_num = re.search(r"(\d+)", rnum_text)
            race_num = int(m_num.group(1)) if m_num else int(race_id[-2:])

            name_el = item.select_one(".ItemTitle")
            race_name = name_el.get_text(strip=True) if name_el else f"{race_num}R"

            data_el = item.select_one(".RaceData")
            data_text = data_el.get_text(" ", strip=True) if data_el else ""
            m_time = re.search(r"(\d{1,2}:\d{2})", data_text)
            post_time = m_time.group(1) if m_time else ""
            m_dist = re.search(r"([芝ダ障]\d{3,4}m?)", data_text)
            surface_dist = m_dist.group(1) if m_dist else data_text

            races.append({
                "raceId": race_id,
                "org": org,
                "venueName": venue_short,
                "venue": f"{venue_short}{race_num}R",
                "raceNumber": race_num,
                "name": race_name,
                "surfaceDist": surface_dist,
                "postTime": post_time,
                "rawMeta": data_text,
            })

    return races


def scrape_shutuba(org: str, race_id: str) -> dict[str, Any]:
    """個別レースの出馬表（全頭・斤量・騎手・馬体重・オッズ・条件）を取得"""
    host = "nar.netkeiba.com" if org == "NAR" else "race.netkeiba.com"
    url = f"https://{host}/race/shutuba.html?race_id={race_id}"
    soup = fetch_soup(url)
    if soup is None:
        return {"url": url, "horses": [], "raceInfo": ""}

    name_el = soup.select_one(".RaceName")
    d1_el = soup.select_one(".RaceData01")
    d2_el = soup.select_one(".RaceData02")
    race_info = " / ".join(
        x.get_text(" ", strip=True) for x in (name_el, d1_el, d2_el) if x
    )

    horses: list[dict[str, Any]] = []
    for tr in soup.select("tr.HorseList"):
        waku_el = tr.select_one("td[class*='Waku']")
        uma_el = tr.select_one("td[class*='Umaban']")
        hname_el = tr.select_one(".HorseName")
        barei_el = tr.select_one(".Barei")
        jockey_el = tr.select_one(".Jockey")
        trainer_el = tr.select_one(".Trainer")
        weight_el = tr.select_one(".Weight")
        odds_el = tr.select_one("td.Txt_R.Popular") or tr.select_one("span[id^='odds-']")

        tds = tr.select("td")
        kinryo = ""
        if len(tds) >= 6:
            kinryo = tds[5].get_text(strip=True)

        uma_txt = uma_el.get_text(strip=True) if uma_el else ""
        if not uma_txt.isdigit():
            continue

        horses.append({
            "gate": waku_el.get_text(strip=True) if waku_el else "",
            "num": int(uma_txt),
            "name": hname_el.get_text(strip=True) if hname_el else "",
            "sexAge": barei_el.get_text(strip=True) if barei_el else "",
            "kinryo": kinryo,
            "jockey": jockey_el.get_text(strip=True) if jockey_el else "",
            "trainer": trainer_el.get_text(strip=True) if trainer_el else "",
            "bodyWeight": weight_el.get_text(strip=True) if weight_el else "未発表",
            "odds": odds_el.get_text(strip=True) if odds_el else "未発表",
        })

    return {"url": url, "raceInfo": race_info, "horses": horses}


def scrape_result(org: str, race_id: str) -> dict[str, Any]:
    """確定レースの着順と公式払戻金テーブルを取得"""
    host = "nar.netkeiba.com" if org == "NAR" else "race.netkeiba.com"
    url = f"https://{host}/race/result.html?race_id={race_id}"
    soup = fetch_soup(url)
    if soup is None:
        return {"settled": False, "url": url}

    finishers: list[dict[str, Any]] = []
    for tr in soup.select("table.RaceTable01 tr.HorseList")[:6]:
        rank_el = tr.select_one(".Rank")
        uma_el = tr.select_one("td.Num.Txt_C") or tr.select_one("td[class*='Umaban']")
        hname_el = tr.select_one(".Horse_Name") or tr.select_one(".HorseName")
        time_el = tr.select_one(".RaceTime")
        if rank_el and uma_el:
            finishers.append({
                "rank": rank_el.get_text(strip=True),
                "num": uma_el.get_text(strip=True),
                "name": hname_el.get_text(strip=True) if hname_el else "",
                "time": time_el.get_text(strip=True) if time_el else "",
            })

    payouts: list[str] = []
    for tbl in soup.select("table.Payout_Detail_Table"):
        for tr in tbl.select("tr"):
            th = tr.select_one("th")
            tds = [td.get_text(" ", strip=True) for td in tr.select("td")]
            if th and tds:
                payouts.append(f"{th.get_text(strip=True)}: {' / '.join(tds)}")

    if len(finishers) < 3 or not payouts:
        return {"settled": False, "url": url}

    return {
        "settled": True,
        "url": url,
        "finishers": finishers,
        "payouts": payouts,
    }


def filter_screening_targets(org: str, scraped: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """API負荷を抑えるため重要レース（重賞・メイン・新馬・南関後半）を最大16レースへ絞り込み"""
    if org == "NAR":
        nankan = [r for r in scraped if r.get("venueName") in NANKAN_VENUES]
        pool = nankan if nankan else scraped
        # 南関なら9R〜12Rおよび重賞/特別を優先
        priority = [
            r for r in pool
            if r.get("raceNumber", 0) >= 9
            or any(k in r.get("name", "") for k in ("Jpn", "重賞", "記念", "賞", "杯", "特別", "スプリント", "カップ"))
        ]
        return (priority or pool)[:12]

    # JRA: 新馬戦 + 9R〜12R + 重賞（最大16レース）
    priority = [
        r for r in scraped
        if "新馬" in r.get("name", "")
        or r.get("raceNumber", 0) >= 9
        or any(k in r.get("name", "") for k in ("G1", "G2", "G3", "S", "特別", "杯", "賞", "記念"))
    ]
    return (priority or scraped)[:16]


def format_shutuba_for_prompt(shutuba: dict[str, Any]) -> str:
    if not shutuba.get("horses"):
        return "（出馬表の自動取得に失敗。取得可能な情報のみで評価し未確認項目はtriggersへ明記）"
    lines = [f"レース条件: {shutuba.get('raceInfo', '')}"]
    lines.append("枠 | 馬番 | 馬名 | 性齢 | 斤量 | 騎手 | 厩舎 | 馬体重 | 単勝オッズ")
    for h in shutuba["horses"]:
        lines.append(
            f"{h['gate']} | {h['num']} | {h['name']} | {h['sexAge']} | {h['kinryo']} | "
            f"{h['jockey']} | {h['trainer']} | {h['bodyWeight']} | {h['odds']}"
        )
    return "\n".join(lines)


# ===== プロンプト構築 =====
def build_common_neon_rules() -> str:
    return """
【Neon v7.0 Maximum Hit-Rate 共通絶対規約】
1. 全頭評価ゲート: 与えられた全出走馬（全N頭）を漏れなく内部評価する。未発表の馬体重・オッズは捏造せず triggers に「未発表」と明記。
2. 2-Stage Benter ベイジアン融合: まずオッズ完全遮断の基礎勝率 fFund を算出し、FLB Power法で補正した市場確率 q と適応重み wR で融合した事後勝率 f を算出する。危険人気馬/中穴Override/大幅増Type II/ダート1-2枠未経験人気馬等は wUsed を 0.10〜0.15 以下へ非対称クランプ。
3. 当日バイアス3レース一致ガード: 3R以上一致の確認データがない場合はバイアス補正を±5%上限に抑制する。
4. 全頭厳密Plackett-Luce＆保存則: 全N頭を内部演算し、sum(f)=100.0%、sum(top2)=200.0%、sum(top3)=300.0% を厳密に満たすこと（下位馬は tailSummary に集約）。総シフト幅は |sum(Δθ)| <= 0.45 にソフトクランプ。
5. 的中率最大化 Core Shield 規約:
   - strategyProfile は "hit_rate_max" をデフォルトとする。
   - ◎は融合後3着内率最上位の安全軸とし、上位2〜4頭へ必ず直結（coreConnections、飛び石結線禁止）。
   - Core比率 0.70〜0.80、単発目標払戻 dutchTargetReturn = 11500〜12500（-15%下落耐性）。
   - 単一穴馬（単勝10倍以上）への合計配分上限 singleLongshotCapPct <= 0.30。
   - 反実仮想セルフ監査（◎破綻時の○-▲防衛状態と消し人気馬の復活条件）を counterfactualAudit に明記。
6. 出力は有効な単一JSONオブジェクトのみ。前置きや解説文は一切出力しないこと。
""".strip()


def build_screening_prompt(org: str, date_str: str, race_rows: list[dict[str, Any]]) -> str:
    summary_lines = [
        f"- raceId={r['raceId']} | {r['venue']} | {r['name']} | {r['surfaceDist']} | 発走{r['postTime']}"
        for r in race_rows
    ]
    race_list_block = "\n".join(summary_lines) if summary_lines else "（開催レース一覧が空）"

    if org == "NAR":
        skill_hint = "全レース skill='app-bayesian-nar'、rank='S|A|B|Pass'"
        criteria = "S/A判定: hitRate>=60%（14頭以上>=55%）, breakEvenRate>=45%, expectedRoi>=105%。一強堅軸トリガミや混戦カオス(M3<38%)は Pass"
    else:
        skill_hint = "新馬戦は skill='app-bayesian-make-debut' & rank='New' & subRank='A|B|Pass'、それ以外は skill='app-bayesian-horse-racing-text' & rank='S|A|B|Pass'"
        criteria = "S/A判定: 平場重賞 hitRate>=60%(重賞>=55%)/breakEven>=45%/ROI>=105%、新馬 hitRate>=55%(フルゲート>=50%)/breakEven>=42%/ROI>=105%。混戦カオスやトリガミ過密は Pass"

    return f"""
あなたは Bayesian Keiba AI（Neon v7.0）の「朝一括スクリーニング」エンジンです。
対象日: {date_str} / 対象区分: {org}

【netkeibaから直接取得した本日開催レース一覧（raceIdをそのまま厳守して出力すること）】
{race_list_block}

【指示】
1. 上記リストに含まれるレースのみを評価し、各レースの raceId・venue・name・surfaceDist・postTime は上記をそのまま使うこと（架空のレース追加は厳禁）。
2. {skill_hint}。
3. {criteria}。
4. 出力は有効な単一JSONオブジェクトのみ。

【厳守JSONスキーマ】
{{
  "date": "{date_str}",
  "org": "{org}",
  "hasHolding": true,
  "strategyProfile": "hit_rate_max",
  "trackBias": {{
    "summary": "対象開催の想定馬場・展開傾向(70字以内)",
    "intradayBiasConsistentR": 0
  }},
  "races": [
    {{
      "raceId": "上記の12桁raceId",
      "org": "{org}",
      "venue": "大井11R",
      "raceNumber": 11,
      "name": "上記の実レース名",
      "surfaceDist": "ダ1600m",
      "postTime": "20:10",
      "skill": "app-bayesian-horse-racing-text | app-bayesian-make-debut | app-bayesian-nar",
      "strategyProfile": "hit_rate_max",
      "rank": "S | A | B | New | Pass",
      "subRank": "A | B | Pass",
      "chaosType": "Type S | Type A | Type B | Type B+",
      "pivotType": "Single-Pivot | Dual-Pivot | Pass",
      "nLead": 3,
      "m3": 54.0,
      "expectedRoi": 110.5,
      "hitRate": 61.5,
      "breakEvenRate": 49.0,
      "scenario": "スクリーニング段階の展開・判定根拠(65字以内)",
      "horses": [],
      "triggers": ["発走1時間前本予想で全頭出馬表・馬体重・実オッズを反映予定"]
    }}
  ]
}}
""".strip()


def build_prompt_for_skill(
    skill: str,
    race_meta: dict[str, Any],
    shutuba_text: str,
    date_str: str,
) -> str:
    common = build_common_neon_rules()
    race_desc = f"{race_meta.get('venue', '')} {race_meta.get('name', '')} ({race_meta.get('surfaceDist', '')} 発走{race_meta.get('postTime', '')})"
    rid = race_meta.get("raceId", "")

    if skill == "app-bayesian-make-debut":
        return f"""
あなたは JRA新馬戦専用「app-bayesian-make-debut (v7.0 Neon)」エンジンです。
対象日: {date_str} / raceId: {rid} / 対象レース: {race_desc}

【公式出馬表データ（全頭実名・枠・馬番を厳守）】
{shutuba_text}

{common}

【新馬戦10モジュール固有ルール】
- ダート1〜2枠の砂被り未経験人気馬は Δθ∈[-0.22,-0.35], wUsed<=0.10, Single-Pivot禁止。外6〜8枠大型馬は+0.15〜+0.25。
- 4角0.6秒射程圏ゲート（スロー想定RPCI>=58.5） vs 先行4頭以上前崩れ差し（☆_closer）。
- 過剰人気6大フィルター該当馬は mark="危", wUsed<=0.10, Single-Pivot禁止。中穴Override（☆_override）は wUsed<=0.10。
- 目標: hitRate>=55%（フルゲート>=50%）, breakEvenRate>=42%, expectedRoi>=102%（未達なら subRank="Pass", pivotType="Pass"）。

【厳守JSONスキーマ】
{{
  "raceId": "{rid}",
  "org": "JRA",
  "venue": "{race_meta.get('venue', '')}",
  "name": "{race_meta.get('name', '')}",
  "surfaceDist": "{race_meta.get('surfaceDist', '')}",
  "postTime": "{race_meta.get('postTime', '')}",
  "skill": "app-bayesian-make-debut",
  "strategyProfile": "hit_rate_max",
  "rank": "New",
  "subRank": "A | B | Pass",
  "chaosType": "Type S | Type A | Type B | Type B+",
  "pivotType": "Single-Pivot | Dual-Pivot | Plan B 2-Zone | Pass",
  "nLead": 2,
  "rpci": 59.5,
  "wR": 0.42,
  "m3": 56.2,
  "intradayBiasConsistentR": 1,
  "expectedRoi": 112.4,
  "hitRate": 59.8,
  "breakEvenRate": 49.5,
  "scenario": "コース物理・想定RPCI・3〜4MECEシナリオ要約(80字以内)",
  "activeModules": ["M2:高CV開幕イン", "M3:4角0.6sゲート"],
  "horses": [
    {{
      "mark": "◎ | ◯ | ▲ | △ | ☆ | 危",
      "role": "役割(15字以内)",
      "num": 6,
      "name": "実馬名",
      "style": "逃 | 先 | 差 | 追",
      "f": 26.8,
      "fFund": 28.5,
      "q": 18.0,
      "wUsed": 0.42,
      "top2": 45.2,
      "top3": 61.0,
      "odds": 4.2,
      "tags": ["F:枠/斤量/馬体重", "H:補正理由"],
      "comment": "45字以内の核心根拠"
    }}
  ],
  "tailSummary": {{ "count": 8, "sumF": 11.2, "sumTop3": 36.5 }},
  "coreConnections": [[6, 3], [6, 11], [6, 2], [3, 11]],
  "portfolioRules": {{ "coreRatio": 0.75, "dutchTargetReturn": 11800, "singleLongshotCapPct": 0.30, "maxLongshotAllocPct": 0.22 }},
  "winReachHedge": [{{ "num": 11, "name": "馬名", "odds": 12.5, "hedge10k": 800, "hedge20k": 1600 }}],
  "counterfactualAudit": "◎破綻時の○-▲防衛状態と危人気馬の復活条件(60字以内)",
  "triggers": ["直前馬体重(週中比-8kg超Type III警戒)・実オッズ確認"]
}}
""".strip()

    if skill == "app-bayesian-nar":
        return f"""
あなたは 地方競馬・南関東専用「app-bayesian-nar (v7.0 Neon)」エンジンです。
対象日: {date_str} / raceId: {rid} / 対象レース: {race_desc}

【公式出馬表データ（全頭実名・枠・馬番を厳守）】
{shutuba_text}

{common}

【NAR固有ルール】
- 重・不良馬場の二極化: 外枠6-8枠大型先行(500kg以上)ブースト、2000m以上不良消耗戦での軽量絞り差し(-4〜-8kg)1着突き抜け補正。
- 1800m以上での+12kg以上馬体増は人気馬でも無条件Type II降格（wUsed<=0.15, 1着軸禁止）。
- 浦和/川崎前崩れ時および南関DG戦での地元トップ騎手（矢野・御神本・笹川・吉原）3着アンカー補正。
- 一強堅軸（単勝2.2倍以下・死角なし・コアオッズ4倍未満）は厳格に rank="Pass"。
- 目標: hitRate>=60%（14頭以上>=55%）, breakEvenRate>=45%, expectedRoi>=102%。

【厳守JSONスキーマ】
{{
  "raceId": "{rid}",
  "org": "NAR",
  "venue": "{race_meta.get('venue', '')}",
  "name": "{race_meta.get('name', '')}",
  "surfaceDist": "{race_meta.get('surfaceDist', '')}",
  "postTime": "{race_meta.get('postTime', '')}",
  "skill": "app-bayesian-nar",
  "strategyProfile": "hit_rate_max",
  "rank": "S | A | B | Pass",
  "pivotType": "Single-Pivot | Dual-Pivot | Pass",
  "nLead": 4,
  "wR": 0.35,
  "m3": 54.8,
  "intradayBiasConsistentR": 1,
  "expectedRoi": 116.5,
  "hitRate": 62.4,
  "breakEvenRate": 53.0,
  "scenario": "コース物理・馬場・3〜4MECEシナリオ要約(80字以内)",
  "horses": [
    {{
      "mark": "◎ | ◯ | ▲ | △ | ☆ | 消",
      "role": "役割(15字以内)",
      "num": 12,
      "name": "実馬名",
      "style": "逃 | 先 | 差 | マ",
      "f": 24.8,
      "fFund": 27.0,
      "q": 18.0,
      "wUsed": 0.35,
      "top2": 44.5,
      "top3": 60.2,
      "odds": 4.5,
      "tags": ["F:実績/枠/馬体重", "H:補正根拠"],
      "comment": "45字以内の核心根拠"
    }}
  ],
  "tailSummary": {{ "count": 8, "sumF": 9.8, "sumTop3": 28.4 }},
  "coreConnections": [[12, 7], [12, 3], [12, 9], [7, 3]],
  "portfolioRules": {{ "coreRatio": 0.76, "dutchTargetReturn": 11800, "singleLongshotCapPct": 0.30, "maxLongshotAllocPct": 0.20 }},
  "tickets": [
    {{ "zone": "Core", "type": "ワイド", "comb": "12 - 7", "points": 1, "share": 0.28, "odds": "4.3倍", "desc": "◎-◯本線元返し防衛" }}
  ],
  "counterfactualAudit": "◎破綻時の○-▲防衛状態と消し人気馬の復活条件(60字以内)",
  "triggers": ["直前馬体重(1800m+の+12kg+警戒)・-30%急落検知"]
}}
""".strip()

    # Default: app-bayesian-horse-racing-text (JRA平場・重賞)
    return f"""
あなたは JRA平場・重賞専用「app-bayesian-horse-racing-text (v7.0 Neon)」エンジンです。
対象日: {date_str} / raceId: {rid} / 対象レース: {race_desc}

【公式出馬表データ（全頭実名・枠・馬番を厳守）】
{shutuba_text}

{common}

【JRA平場・重賞固有ルール】
- 来日トップ外国馬と日本馬の海外大敗帰りを厳密分離（来日トップ外国馬には疲労上限を適用せず wR>=0.40 で独立評価）。
- 3〜4歳ダート2連勝以上昇級馬・小幅距離延長の成長余地加点則（△/☆_riser）。
- 目標: hitRate>=60%（16〜18頭重賞>=55%）, breakEvenRate>=45%, expectedRoi>=102%（未達なら rank="Pass", pivotType="Pass"）。

【厳守JSONスキーマ】
{{
  "raceId": "{rid}",
  "org": "JRA",
  "venue": "{race_meta.get('venue', '')}",
  "name": "{race_meta.get('name', '')}",
  "surfaceDist": "{race_meta.get('surfaceDist', '')}",
  "postTime": "{race_meta.get('postTime', '')}",
  "skill": "app-bayesian-horse-racing-text",
  "strategyProfile": "hit_rate_max",
  "rank": "S | A | B | Pass",
  "pivotType": "Single-Pivot | Dual-Pivot | Pass",
  "nLead": 3,
  "rpci": 50.5,
  "wR": 0.35,
  "m3": 52.4,
  "intradayBiasConsistentR": 1,
  "intradayBias3R": false,
  "expectedRoi": 111.5,
  "hitRate": 61.2,
  "breakEvenRate": 54.0,
  "scenario": "コース物理・展開・3〜4MECEシナリオ重み要約(80字以内)",
  "activeModules": ["2-Stage Benter融合", "Core Shieldダッチング"],
  "horses": [
    {{
      "mark": "◎ | ◯ | ▲ | △ | ☆ | 消",
      "role": "役割(15字以内)",
      "num": 5,
      "name": "実馬名",
      "style": "逃 | 先 | 差 | 追",
      "f": 19.6,
      "fFund": 21.5,
      "q": 16.0,
      "wUsed": 0.35,
      "top2": 38.8,
      "top3": 55.4,
      "odds": 5.2,
      "tags": ["F:実績/枠/体重", "H:補正理由"],
      "comment": "45字以内の核心根拠"
    }}
  ],
  "tailSummary": {{ "count": 10, "sumF": 14.2, "sumTop3": 38.5 }},
  "coreConnections": [[5, 6], [5, 1], [5, 14], [6, 14]],
  "portfolioRules": {{ "coreRatio": 0.76, "dutchTargetReturn": 11800, "singleLongshotCapPct": 0.30, "maxLongshotAllocPct": 0.24 }},
  "counterfactualAudit": "◎破綻時の○-▲防衛状態と消し人気馬の復活条件(60字以内)",
  "triggers": ["直前馬体重(Type I-III)・実オッズ下限確認"]
}}
""".strip()


def build_triple_umatan_prompt(venue_name: str, date_str: str, legs_text: str) -> str:
    return f"""
あなたは 南関トリプル馬単専用「app-bayesian-nar (v7.0 Neon Probability-Shell Edition)」エンジンです。
対象日: {date_str} / 対象場: {venue_name}（最終3レース）

【直接取得した対象3レース出馬表】
{legs_text}

【トリプル馬単 Neon v7.0 規約】
- 各レースで 2-Stage Benter 融合 Plackett-Luce により 1着確率 f、2着内率 top2、上位馬単ペア確率を算出。
- 予算目安 3,000円（50円単位）を Probability-Shell 直交分解し、重複ゼロの T1_Core と T2_Wing に分割。
- 出力は有効な単一JSONオブジェクトのみ。

【厳守JSONスキーマ】
{{
  "date": "{date_str}",
  "venue": "{venue_name}",
  "skill": "app-bayesian-nar",
  "hitRate": 6.8,
  "expectedRoi": 132.0,
  "legs": [
    {{
      "raceNumber": 10,
      "venue": "{venue_name}10R",
      "name": "実レース名",
      "surfaceDist": "ダ1400m",
      "wR": 0.35,
      "exactaPairs": [{{ "first": 5, "second": 8, "prob": 11.2, "note": "先行→差し" }}]
    }}
  ],
  "shellTickets": [
    {{ "id": "T1_Core", "formation": "10R(5→8,2) × 11R(12→7,3) × 12R(4→1,9)", "points": 8, "unit": 150 }},
    {{ "id": "T2_Wing", "formation": "10R(8→5,2) × 11R(12,7→3,9) × 12R(4,1→9,6)", "points": 24, "unit": 50 }}
  ]
}}
""".strip()


def build_win5_prompt(date_str: str, legs_text: str) -> str:
    return f"""
あなたは JRA WIN5専用「app-bayesian-win5 (v11.1 Neon Plan C)」エンジンです。
対象日: {date_str}

【直接取得した対象5レース出馬表】
{legs_text}

【WIN5 v11.1 規約】
- 2-Stage Benter融合（来日トップ外国馬参戦時は wR=0.55〜0.60）で各レースの勝率 f, fFund, q を算出。
- 乾燥ダート戦は上位4頭内に差し馬枠を最低1頭確保。
- Plan C 確率シェル直交分解（T1 Core 45%上限厳守、T2〜T4 Wing は重複ゼロの3〜4チケット構成）。
- 出力は有効な単一JSONオブジェクトのみ。

【厳守JSONスキーマ】
{{
  "date": "{date_str}",
  "skill": "app-bayesian-win5",
  "difficulty": "A | B | C",
  "legs": [
    {{
      "venue": "東京10R",
      "name": "実レース名",
      "surfaceDist": "芝1600m",
      "wR": 0.40,
      "grade": "堅 | 中 | 波乱",
      "horses": [
        {{ "mark": "◎", "num": 5, "name": "実馬名", "shell": "Core | Wing", "f": 28.5, "fFund": 30.0, "q": 25.0, "wUsed": 0.40, "odds": 3.2, "comment": "35字以内" }}
      ]
    }}
  ],
  "planC": {{
    "tickets": [
      {{ "id": "T1", "label": "Core本線(45%上限)", "formation": "5,8 × 2,4 × 1,9 × 6 × 3,7", "points": 32, "hitProb": 8.4 }}
    ]
  }},
  "hedgeCandidates": [{{ "num": 11, "name": "実馬名", "odds": 14.5 }}]
}}
""".strip()


# ===== Gemini API 呼び出し =====
def extract_json(raw_text: str) -> dict[str, Any]:
    text = raw_text.strip()
    fence = re.search(r"```(?:json)?\s*(\{.*\})\s*```", text, re.DOTALL)
    if fence:
        text = fence.group(1)
    else:
        start = text.find("{")
        end = text.rfind("}")
        if start != -1 and end != -1:
            text = text[start : end + 1]
    return json.loads(text)


def call_gemini_json(
    client: genai.Client,
    model: str,
    prompt: str,
    thinking_level: str = "medium",
    retries: int = 2,
) -> dict[str, Any]:
    fallback_model = FAST_MODEL if model == HIGH_TIER_MODEL else HIGH_TIER_MODEL
    candidates: list[tuple[str, str]] = [(model, thinking_level)]
    if fallback_model != model:
        fb_level = "medium" if fallback_model == FAST_MODEL else "high"
        candidates.append((fallback_model, fb_level))

    errors_log: list[str] = []
    for idx, (cur_model, cur_level) in enumerate(candidates):
        for attempt in range(retries + 1):
            try:
                config_kwargs: dict[str, Any] = {
                    "temperature": 0.2,
                    "response_mime_type": "application/json",
                }
                if ENABLE_GOOGLE_SEARCH:
                    config_kwargs["tools"] = [types.Tool(google_search=types.GoogleSearch())]
                    config_kwargs.pop("response_mime_type", None)
                try:
                    config_kwargs["thinking_config"] = types.ThinkingConfig(
                        thinking_level=cur_level
                    )
                except Exception:
                    pass

                response = client.models.generate_content(
                    model=cur_model,
                    contents=prompt,
                    config=types.GenerateContentConfig(**config_kwargs),
                )
                if not response.text:
                    raise RuntimeError("Gemini API returned empty text.")
                return extract_json(response.text)
            except Exception as exc:
                err_msg = f"{cur_model} (attempt {attempt + 1}): {exc}"
                errors_log.append(err_msg)
                print(f"[API ERROR] {err_msg}", file=sys.stderr)
                err_str = str(exc)
                if ("429" in err_str or "RESOURCE_EXHAUSTED" in err_str or "404" in err_str) and idx < len(candidates) - 1:
                    print(f"[FALLBACK] Switching to {candidates[idx + 1][0]}", file=sys.stderr)
                    time.sleep(2.0)
                    break
                if attempt < retries:
                    wait_sec = 5 * (attempt + 1)
                    time.sleep(wait_sec)
    raise RuntimeError("Gemini call failed across models:\n" + "\n".join(errors_log))


# ===== データ永続化・正規化 =====
def validate_and_normalize_race(race: dict[str, Any], skill: str, stage: str = "final") -> dict[str, Any]:
    race.setdefault("skill", skill)
    race.setdefault("strategyProfile", "hit_rate_max")
    race["org"] = detect_org(race)
    race["stage"] = stage
    race["updatedAt"] = now_jst_str()

    if not race.get("raceId"):
        race["raceId"] = re.sub(r"\s+", "-", f"{race.get('venue', 'race')}-{race.get('name', 'unknown')}")

    if "intradayBiasConsistentR" not in race and "intradayBias3R" in race:
        race["intradayBiasConsistentR"] = 3 if race["intradayBias3R"] else 1
    elif "intradayBiasConsistentR" in race and "intradayBias3R" not in race:
        race["intradayBias3R"] = int(race["intradayBiasConsistentR"]) >= 3

    rules = race.get("portfolioRules") or {}
    rules.setdefault("coreRatio", 0.75)
    rules.setdefault("dutchTargetReturn", 11800)
    rules["singleLongshotCapPct"] = min(0.30, float(rules.get("singleLongshotCapPct", 0.30)))
    race["portfolioRules"] = rules

    horses = race.get("horses") or []
    for h in horses:
        if "fFund" not in h and "f" in h:
            h["fFund"] = h["f"]
        if "wUsed" not in h and "wR" in race:
            h["wUsed"] = race["wR"]
    horses.sort(key=lambda x: float(x.get("f", 0.0)), reverse=True)
    race["horses"] = horses

    if "m3" not in race and len(horses) >= 3:
        race["m3"] = round(sum(float(h.get("f", 0.0)) for h in horses[:3]), 1)

    return race


def load_store(date_str: str) -> dict[str, Any]:
    if LATEST_JSON_PATH.exists():
        try:
            data = json.loads(LATEST_JSON_PATH.read_text(encoding="utf-8"))
            if data.get("date") == date_str:
                data.setdefault("races", [])
                data.setdefault("trackBias", {})
                return data
        except Exception as exc:
            print(f"[WARN] Could not load existing latest.json: {exc}", file=sys.stderr)
    return {
        "date": date_str,
        "updatedAt": now_jst_str(),
        "trackBias": {},
        "races": [],
        "win5": None,
        "tripleUmatan": None,
    }


def save_store(store: dict[str, Any]) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    HISTORY_DIR.mkdir(parents=True, exist_ok=True)
    store["updatedAt"] = now_jst_str()
    store["races"].sort(key=lambda r: (str(r.get("postTime") or "99:99"), str(r.get("venue") or "")))
    payload = json.dumps(store, ensure_ascii=False, indent=2)
    LATEST_JSON_PATH.write_text(payload, encoding="utf-8")
    hist_path = HISTORY_DIR / f"{store['date']}.json"
    hist_path.write_text(payload, encoding="utf-8")
    print(f"[OK] Saved {LATEST_JSON_PATH} & {hist_path} (races={len(store['races'])})")


def upsert_race(store: dict[str, Any], new_race: dict[str, Any], allow_downgrade: bool = False) -> None:
    rid = new_race.get("raceId")
    v_key = f"{new_race.get('venue', '')}|{new_race.get('name', '')}"
    races = store.setdefault("races", [])

    for idx, existing in enumerate(races):
        same_id = rid and existing.get("raceId") == rid
        same_vn = f"{existing.get('venue', '')}|{existing.get('name', '')}" == v_key
        if same_id or same_vn:
            if not allow_downgrade and new_race.get("stage") == "screened":
                if existing.get("stage") == "final" or (existing.get("result") or {}).get("settled"):
                    return
            if "result" in existing and "result" not in new_race:
                new_race["result"] = existing["result"]
            races[idx] = new_race
            return
    races.append(new_race)


def resolve_orgs(org_arg: str) -> list[str]:
    return ["JRA", "NAR"] if org_arg.upper() == "ALL" else [org_arg.upper()]


# ===== 各モード実行 =====
def run_screening(client: genai.Client, store: dict[str, Any], org_arg: str, date_str: str) -> None:
    for org in resolve_orgs(org_arg):
        scraped = scrape_race_list(org, date_str)
        if not scraped:
            print(f"[INFO] No {org} races found on netkeiba for {date_str}.")
            continue

        targets = filter_screening_targets(org, scraped)
        print(f"[SCREENING] {date_str} {org}: scraped={len(scraped)}, selected={len(targets)} ({FAST_MODEL})")
        prompt = build_screening_prompt(org, date_str, targets)
        res = call_gemini_json(client, FAST_MODEL, prompt, thinking_level="medium")

        if res.get("trackBias"):
            store.setdefault("trackBias", {})[org] = res["trackBias"]

        screened_races = res.get("races") or []
        for raw_race in screened_races:
            raw_race["org"] = org
            skill = raw_race.get("skill")
            if not skill:
                if org == "NAR":
                    skill = "app-bayesian-nar"
                elif "新馬" in str(raw_race.get("name", "")) or raw_race.get("rank") == "New":
                    skill = "app-bayesian-make-debut"
                else:
                    skill = "app-bayesian-horse-racing-text"
            normalized = validate_and_normalize_race(raw_race, skill, stage="screened")
            upsert_race(store, normalized, allow_downgrade=False)

        save_store(store)
        time.sleep(REQUEST_INTERVAL_SEC)


def run_hourly(
    client: genai.Client,
    store: dict[str, Any],
    org_arg: str,
    date_str: str,
    force_all: bool = False,
) -> None:
    target_orgs = resolve_orgs(org_arg)

    for org in target_orgs:
        if not any(detect_org(r) == org for r in store.get("races", [])):
            print(f"[INFO] No screened {org} races in store -> running screening first.")
            run_screening(client, store, org, date_str)

    ref_now = now_jst()
    due_races: list[dict[str, Any]] = []
    for race in store.get("races", []):
        if detect_org(race) not in target_orgs:
            continue
        if race.get("stage") == "final":
            continue
        if race.get("rank") == "Pass" or race.get("subRank") == "Pass":
            continue

        mins = minutes_until_post(date_str, str(race.get("postTime") or ""), ref_now)
        if force_all or (mins is not None and HOURLY_WINDOW_MIN <= mins <= HOURLY_WINDOW_MAX):
            due_races.append(race)
        else:
            print(f"[SKIP] {race.get('venue')} {race.get('name')} (post={race.get('postTime')}, delta={mins})")

    print(f"[HOURLY] Due races to finalize: {len(due_races)}")
    for race in due_races:
        org = detect_org(race)
        skill = race.get("skill") or (
            "app-bayesian-nar" if org == "NAR"
            else ("app-bayesian-make-debut" if "新馬" in str(race.get("name", "")) else "app-bayesian-horse-racing-text")
        )
        rid = str(race.get("raceId") or "")
        shutuba = scrape_shutuba(org, rid) if re.fullmatch(r"\d{12}", rid) else {"horses": [], "raceInfo": ""}
        shutuba_text = format_shutuba_for_prompt(shutuba)

        model, t_level = select_model_and_thinking(skill, str(race.get("name") or ""), str(race.get("rank") or ""))
        print(f"[HOURLY-PREDICT] {skill} ({model}, thinking={t_level}) -> {race.get('venue')} {race.get('name')}")
        try:
            prompt = build_prompt_for_skill(skill, race, shutuba_text, date_str)
            pred = call_gemini_json(client, model, prompt, thinking_level=t_level)
            if rid:
                pred["raceId"] = rid
            normalized = validate_and_normalize_race(pred, skill, stage="final")
            upsert_race(store, normalized, allow_downgrade=True)
            save_store(store)
            time.sleep(REQUEST_INTERVAL_SEC)
        except Exception as exc:
            print(f"[WARN] Failed hourly prediction for {race.get('venue')}: {exc}", file=sys.stderr)

    # 南関トリプル馬単の自動生成
    if "NAR" in target_orgs:
        existing_triple = store.get("tripleUmatan") or {}
        if existing_triple.get("date") != date_str:
            nar_list = scrape_race_list("NAR", date_str)
            nankan_10r = [r for r in nar_list if r.get("venueName") in NANKAN_VENUES and r.get("raceNumber") == 10]
            for r10 in nankan_10r:
                mins = minutes_until_post(date_str, str(r10.get("postTime") or ""), ref_now)
                if force_all or (mins is not None and HOURLY_WINDOW_MIN <= mins <= HOURLY_WINDOW_MAX):
                    vname = r10["venueName"]
                    legs = [r for r in nar_list if r.get("venueName") == vname and r.get("raceNumber") in (10, 11, 12)]
                    legs_blocks = []
                    for leg in sorted(legs, key=lambda x: x["raceNumber"]):
                        sh = scrape_shutuba("NAR", leg["raceId"])
                        legs_blocks.append(f"### {leg['venue']} {leg['name']} ({leg['surfaceDist']})\n{format_shutuba_for_prompt(sh)}")
                    if len(legs_blocks) == 3:
                        print(f"[TRIPLE-UMATAN] Generating for {vname} ({HIGH_TIER_MODEL}, thinking=high)")
                        try:
                            t_prompt = build_triple_umatan_prompt(vname, date_str, "\n\n".join(legs_blocks))
                            store["tripleUmatan"] = call_gemini_json(client, HIGH_TIER_MODEL, t_prompt, thinking_level="high")
                            save_store(store)
                        except Exception as exc:
                            print(f"[WARN] Triple Umatan failed: {exc}", file=sys.stderr)
                    break


def run_single_predict(
    client: genai.Client,
    store: dict[str, Any],
    skill: str,
    race_query: str,
    date_str: str,
) -> None:
    org = "NAR" if "nar" in skill or any(v in race_query for v in NAR_VENUES) else "JRA"
    scraped = scrape_race_list(org, date_str)
    matched = None
    for r in scraped:
        if r["venue"] in race_query or (r["name"] and r["name"] in race_query) or r["raceId"] == race_query.strip():
            matched = r
            break

    if matched:
        shutuba = scrape_shutuba(org, matched["raceId"])
        race_meta = matched
    else:
        shutuba = {"horses": [], "raceInfo": race_query}
        race_meta = {"raceId": "", "venue": race_query, "name": race_query, "surfaceDist": "", "postTime": ""}

    model, t_level = select_model_and_thinking(skill, race_query, rank="A")
    print(f"[RUN] {skill} ({model}, thinking={t_level}) -> {race_meta.get('venue')} {race_meta.get('name')}")
    prompt = build_prompt_for_skill(skill, race_meta, format_shutuba_for_prompt(shutuba), date_str)
    pred = call_gemini_json(client, model, prompt, thinking_level=t_level)
    if race_meta.get("raceId"):
        pred["raceId"] = race_meta["raceId"]
    normalized = validate_and_normalize_race(pred, skill, stage="final")
    upsert_race(store, normalized, allow_downgrade=True)
    save_store(store)


def run_win5(client: genai.Client, store: dict[str, Any], date_str: str) -> None:
    jra_races = scrape_race_list("JRA", date_str)
    # 14:40〜15:50 頃のメイン5レース（10R〜11R）を抽出
    candidates = [r for r in jra_races if r.get("raceNumber") in (9, 10, 11)]
    candidates.sort(key=lambda r: (str(r.get("postTime") or "99:99"), r.get("raceNumber", 0)))
    legs = candidates[-5:] if len(candidates) >= 5 else candidates
    if not legs:
        print(f"[INFO] No JRA races found for WIN5 on {date_str}.")
        return

    blocks = []
    for idx, leg in enumerate(legs, 1):
        sh = scrape_shutuba("JRA", leg["raceId"])
        blocks.append(f"### Leg {idx}: {leg['venue']} {leg['name']} ({leg['surfaceDist']} 発走{leg['postTime']})\n{format_shutuba_for_prompt(sh)}")

    print(f"[RUN] app-bayesian-win5 ({HIGH_TIER_MODEL}, thinking=high) -> {date_str}")
    prompt = build_win5_prompt(date_str, "\n\n".join(blocks))
    store["win5"] = call_gemini_json(client, HIGH_TIER_MODEL, prompt, thinking_level="high")
    save_store(store)


def run_audit(client: genai.Client, store: dict[str, Any], org_arg: str) -> None:
    target_orgs = resolve_orgs(org_arg)
    targets = [
        r for r in store.get("races", [])
        if detect_org(r) in target_orgs
        and r.get("rank") != "Pass"
        and r.get("subRank") != "Pass"
        and not (r.get("result") or {}).get("settled")
    ]
    if not targets:
        print(f"[INFO] No unsettled {org_arg} races to audit.")
        return

    updated_any = False
    for race in targets:
        rid = str(race.get("raceId") or "")
        org = detect_org(race)
        if not re.fullmatch(r"\d{12}", rid):
            continue
        official = scrape_result(org, rid)
        if not official.get("settled"):
            print(f"[AUDIT SKIP] Not settled yet: {race.get('venue')} {race.get('name')}")
            continue

        prompt = f"""
以下の公式確定結果・払戻金と推奨配分から、10,000円基準の正確な払戻金を算出して単一JSONのみで返してください。
レース: {race.get('venue')} {race.get('name')}
公式着順: {json.dumps(official['finishers'], ensure_ascii=False)}
公式払戻: {json.dumps(official['payouts'], ensure_ascii=False)}
推奨Core結線: {race.get('coreConnections')}
推奨馬券: {race.get('tickets')}
配分ルール: {race.get('portfolioRules')}

{{
  "settled": true,
  "order": "1着番-2着番-3着番",
  "payout10k": 12400,
  "hit": true,
  "note": "35字以内の結果・3要因振り返り"
}}
""".strip()
        try:
            res = call_gemini_json(client, FAST_MODEL, prompt, thinking_level="medium")
            if res.get("settled"):
                res["payout10k"] = int(round(float(res.get("payout10k", 0))))
                res["hit"] = bool(res.get("hit", res["payout10k"] > 0))
                race["result"] = res
                updated_any = True
                print(f"[AUDIT] {race.get('venue')} {race.get('name')} -> {res.get('order')} / ¥{res['payout10k']}")
            time.sleep(REQUEST_INTERVAL_SEC)
        except Exception as exc:
            print(f"[WARN] Audit failed for {rid}: {exc}", file=sys.stderr)

    if updated_any:
        save_store(store)


def main() -> None:
    parser = argparse.ArgumentParser(description="Bayesian Keiba AI Neon Pipeline (Direct-Scrape Hybrid)")
    parser.add_argument("--mode", choices=["screening", "hourly", "predict", "win5", "audit"], required=True)
    parser.add_argument("--date", default=now_jst().strftime("%Y-%m-%d"))
    parser.add_argument("--org", choices=["JRA", "NAR", "ALL"], default="JRA")
    parser.add_argument("--skill", default="app-bayesian-horse-racing-text")
    parser.add_argument("--race", default="", help="例: 東京11R 霜月S / 大井11R / 12桁raceId")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise EnvironmentError("GEMINI_API_KEY is not set.")

    client = genai.Client(api_key=api_key)
    store = load_store(args.date)

    if args.mode == "screening":
        run_screening(client, store, args.org, args.date)
    elif args.mode == "hourly":
        run_hourly(client, store, args.org, args.date, force_all=args.force)
    elif args.mode == "predict":
        if not args.race:
            raise ValueError("--race is required for predict mode.")
        run_single_predict(client, store, args.skill, args.race, args.date)
    elif args.mode == "win5":
        run_win5(client, store, args.date)
    elif args.mode == "audit":
        run_audit(client, store, args.org)


if __name__ == "__main__":
    main()
