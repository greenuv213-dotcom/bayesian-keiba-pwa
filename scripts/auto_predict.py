#!/usr/bin/env python3
"""
Bayesian Keiba AI — Automated Prediction & Audit Pipeline (Neon v7.0 / v11.1 Hybrid Edition)

Model Routing:
  - High Tier (WIN5 / Grade / Make Debut / Triple Umatan): gemini-4-hydrogen (thinking_level="high")
  - Fast Tier (Screening / Standard Races / Audit)       : gemini-3.8-flash  (thinking_level="medium")
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

from google import genai
from google.genai import types

# ===== 設定（環境変数・GitHub Variables で上書き可能）=====
HIGH_TIER_MODEL = os.getenv("GEMINI_HIGH_TIER_MODEL", "gemini-4-hydrogen")
FAST_MODEL = os.getenv("GEMINI_FAST_MODEL", "gemini-3.8-flash")
DATA_DIR = Path(os.getenv("KEIBA_DATA_DIR", "data"))
LATEST_JSON_PATH = DATA_DIR / "latest.json"
HISTORY_DIR = DATA_DIR / "history"
JST = dt.timezone(dt.timedelta(hours=9))

# 発走1時間前パイプラインの許容ウィンドウ（分）
HOURLY_WINDOW_MIN = 20
HOURLY_WINDOW_MAX = 105

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
    """WIN5・重賞・新馬戦・S/A勝負レースは Hydrogen(high)、それ以外は 3.8-Flash(medium)"""
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
        hour, minute = int(m.group(1)), int(m.group(2))
        return dt.datetime(year, month, day, hour, minute, tzinfo=JST)
    except ValueError:
        return None


def minutes_until_post(date_str: str, post_time: str, ref_now: dt.datetime | None = None) -> float | None:
    post_dt = parse_post_datetime(date_str, post_time)
    if post_dt is None:
        return None
    ref = ref_now or now_jst()
    return (post_dt - ref).total_seconds() / 60.0


def build_common_neon_rules() -> str:
    return """
【Neon v7.0 Maximum Hit-Rate 共通絶対規約】
1. 全頭取得必須ゲート: Google検索で全出走馬（枠・馬番・馬名・斤量・騎手・最新オッズ・発表済なら公式馬体重増減）、馬場（クッション値/含水率/砂厚/風向）、当日1R〜直前Rの結果を必ず確認する。未発表項目は捏造せず triggers に「未発表」と明記。
2. 2-Stage Benter ベイジアン融合: まずオッズ完全遮断の基礎勝率 fFund を算出し、FLB Power法で補正した市場確率 q と適応重み wR で融合した事後勝率 f を算出する。危険人気馬/中穴Override/大幅増Type II/ダート1-2枠未経験人気馬等は wUsed を 0.10〜0.15 以下へ非対称クランプ。
3. 当日バイアス3レース一致ガード: 同一馬場・同ペース系統で3R以上一致時のみシナリオ重みを±10〜20%更新。2R一致は±6〜10%、1Rのみ・ペース不一致は±5%上限。
4. 全頭厳密Plackett-Luce＆保存則: 全N頭を内部演算し、sum(f)=100.0%、sum(top2)=200.0%、sum(top3)=300.0% を厳密に満たすこと（下位馬は tailSummary に集約）。総シフト幅は |sum(Δθ)| <= 0.45 にソフトクランプ。
5. 的中率最大化 Core Shield 規約:
   - strategyProfile は "hit_rate_max" をデフォルトとする。
   - ◎は融合後3着内率最上位の安全軸とし、上位2〜4頭へ必ず直結（coreConnections、飛び石結線禁止）。
   - Core比率 0.70〜0.80、単発目標払戻 dutchTargetReturn = 11500〜12500（-15%下落耐性）。
   - 単一穴馬（単勝10倍以上）への合計配分上限 singleLongshotCapPct <= 0.30。
   - 反実仮想セルフ監査（◎破綻時の○-▲防衛状態と消し人気馬の復活条件）を counterfactualAudit に明記。
6. 出力は有効な単一JSONオブジェクトのみ。前置きや解説文は一切出力しないこと。
""".strip()


def build_screening_prompt(org: str, date_str: str) -> str:
    if org == "NAR":
        target_desc = "本日開催の南関東（大井・川崎・船橋・浦和）および主要ダートグレード競走（非開催なら主要NAR会場のメイン・準メイン）"
        skill_hint = "全レース skill は 'app-bayesian-nar' を設定"
        criteria = "S/A判定: hitRate>=60%（14頭以上>=55%）, breakEvenRate>=45%, expectedRoi>=105%。一強堅軸トリガミ(O<=2.2かつ死角なし)や混戦カオス(M3<38%)は rank='Pass'"
    else:
        target_desc = "本日開催のJRA全会場から、重賞・メイン(9R〜12R)・新馬戦・勝負妙味の高い注目レース（合計最大16レース）"
        skill_hint = "新馬戦は skill='app-bayesian-make-debut' & rank='New' & subRank='A|B|Pass'、それ以外は skill='app-bayesian-horse-racing-text' & rank='S|A|B|Pass'"
        criteria = "S/A判定: 平場重賞は hitRate>=60%（16頭以上重賞>=55%）, breakEvenRate>=45%, expectedRoi>=105%。新馬戦は hitRate>=55%（フルゲート>=50%）, breakEvenRate>=42%, expectedRoi>=105%。混戦カオス(M3<38%/新馬<36%)やトリガミ過密は Pass"

    return f"""
あなたは Bayesian Keiba AI（Neon v7.0）の「朝一括スクリーニング」エンジンです。
対象日: {date_str} / 対象区分: {org}
対象範囲: {target_desc}

【実行手順】
1. Google検索で {date_str} の {org} 開催会場・発走時刻・レース名・距離・出馬表・最新馬場状態（クッション値/含水率/砂厚）および主要人気馬・オッズを取得する。
2. 開催がない場合は `"hasHolding": false, "races": []` を返すこと（架空のレースを絶対に捏造しないこと）。
3. 各対象レースについて Top-3融合集中度 M3、先行頭数 nLead、推定的中率 hitRate、元返し率 breakEvenRate、期待ROI expectedRoi を評価し、上位3〜4頭のプレビュー候補馬を付与する。
4. {skill_hint}。
5. {criteria}。
6. 出力は有効な単一JSONオブジェクトのみ。前置き・解説は一切禁止。

【厳守JSONスキーマ】
{{
  "date": "{date_str}",
  "org": "{org}",
  "hasHolding": true,
  "strategyProfile": "hit_rate_max",
  "trackBias": {{
    "summary": "全会場の馬場傾向・クッション値/含水率/砂厚の要約(80字以内)",
    "intradayBiasConsistentR": 0
  }},
  "races": [
    {{
      "raceId": "20261122-tok-11",
      "org": "{org}",
      "venue": "東京11R",
      "raceNumber": 11,
      "name": "実レース名",
      "surfaceDist": "芝1600m",
      "postTime": "15:40",
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
      "scenario": "朝時点の馬場・展開・注目ポイント(70字以内)",
      "horses": [
        {{
          "mark": "◎",
          "role": "朝スクリーニング本命候補",
          "num": 5,
          "name": "実馬名",
          "style": "先",
          "f": 22.0,
          "fFund": 23.5,
          "q": 18.0,
          "top2": 40.0,
          "top3": 56.0,
          "odds": 4.2,
          "comment": "35字以内の事前根拠"
        }}
      ],
      "triggers": ["発走1時間前本予想で公式馬体重・当日3Rバイアス・実オッズを反映予定"]
    }}
  ]
}}
""".strip()


def build_triple_umatan_prompt(venue_name: str, date_str: str) -> str:
    return f"""
あなたは 南関トリプル馬単専用「app-bayesian-nar (v7.0 Neon Probability-Shell Edition)」エンジンです。
対象日: {date_str} / 対象場: {venue_name}（最終3レース: 10R・11R・12R）

【トリプル馬単 Neon v7.0 規約】
1. Google検索で {date_str} {venue_name} の最終3レース（通常10R・11R・12R）の全出走馬・最新オッズ・公式馬体重・当日含水率/砂厚・当日1R〜9Rのバイアス（3R一致ガード）を取得する。
2. 各レースで 2-Stage Benter 融合 Plackett-Luce により 1着確率 f、2着内率 top2、および上位馬単ペア確率を厳密算出する。
3. 予算目安 3,000円（50円単位・計60点前後）を Probability-Shell 直交分解し、重複ゼロの T1_Core（本線シェル）と T2_Wing（高エントロピー戦の穴差し込みシェル）に分割する。
4. 出力は有効な単一JSONオブジェクトのみ。

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
      "exactaPairs": [
        {{ "first": 5, "second": 8, "prob": 11.2, "note": "先行粘り→差し" }}
      ]
    }}
  ],
  "shellTickets": [
    {{ "id": "T1_Core", "formation": "10R(5→8,2) × 11R(12→7,3) × 12R(4→1,9)", "points": 8, "unit": 150 }},
    {{ "id": "T2_Wing", "formation": "10R(8→5,2) × 11R(12,7→3,9) × 12R(4,1→9,6)", "points": 24, "unit": 50 }}
  ]
}}
""".strip()


def build_prompt_for_skill(skill: str, race_query: str, date_str: str) -> str:
    common = build_common_neon_rules()

    if skill == "app-bayesian-make-debut":
        return f"""
あなたは JRA新馬戦専用「app-bayesian-make-debut (v7.0 Neon)」エンジンです。
対象日: {date_str} / 対象レース: {race_query}
{common}

【新馬戦10モジュール固有ルール】
- ダート1〜2枠の砂被り未経験人気馬は Δθ∈[-0.22,-0.35], wUsed<=0.10, Single-Pivot禁止（ゲート1F<=11.8s単騎ハナ or 500kg以上3頭併せ内確認済のみ緩和）。外6〜8枠大型馬は+0.15〜+0.25。
- 4角0.6秒射程圏ゲート（スロー想定RPCI>=58.5） vs 先行4頭以上前崩れ差し（☆_closer）。
- 古馬基準時計×後半2F持続加速突破馬（CW 6F<=81.5&2F<=22.8 / 美W 5F<=65.8&2F<=22.8 / 坂路4F<=52.2-52.5&2F<=24.4-24.6）は wUsed<=0.10 で上位抜擢。
- 過剰人気6大フィルター該当馬は mark="危", wUsed<=0.10, Single-Pivot禁止。
- 中穴仕上がり早オーバーライド（☆_override）は wUsed<=0.10。
- 目標: hitRate>=55%（フルゲート>=50%）, breakEvenRate>=42%, expectedRoi>=102%（未達なら subRank="Pass", pivotType="Pass"）。

【厳守JSONスキーマ】
{{
  "raceId": "YYYYMMDD-venue-RR",
  "org": "JRA",
  "venue": "東京5R",
  "name": "2歳新馬",
  "surfaceDist": "芝1800m",
  "postTime": "12:15",
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
  "intradayBiasConsistentR": 2,
  "expectedRoi": 112.4,
  "hitRate": 59.8,
  "breakEvenRate": 49.5,
  "scenario": "午前バイアス・想定RPCI・3〜4MECEシナリオ要約(80字以内)",
  "activeModules": ["M2:高CV開幕イン", "M3:4角0.6sゲート", "M8:後半2F突破"],
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
      "tags": ["F:調教/枠事実", "H:補正理由"],
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
対象日: {date_str} / 対象レース: {race_query}
{common}

【NAR固有ルール】
- 重・不良馬場の二極化: 外枠6-8枠大型先行(500kg以上)ブースト、および2000m以上不良消耗戦での軽量絞り差し(-4〜-8kg)1着突き抜け補正。
- 外枠JRA重賞複数勝馬の単騎ハナ強奪＆斤量/距離延長免除。
- 1800m以上での+12kg以上馬体増は人気馬でも無条件Type II降格（wUsed<=0.15, 1着軸禁止）。
- 浦和/川崎前崩れ時および南関DG戦での地元トップ騎手（矢野・御神本・笹川・吉原）3着アンカー補正。
- 一強堅軸（単勝2.2倍以下・死角なし・コアオッズ4倍未満）は厳格に rank="Pass"。
- 目標: hitRate>=60%（14頭以上>=55%）, breakEvenRate>=45%, expectedRoi>=102%。

【厳守JSONスキーマ】
{{
  "raceId": "YYYYMMDD-nar-RR",
  "org": "NAR",
  "venue": "大井11R",
  "name": "レース名",
  "surfaceDist": "ダ1600m",
  "postTime": "20:10",
  "skill": "app-bayesian-nar",
  "strategyProfile": "hit_rate_max",
  "rank": "S | A | B | Pass",
  "pivotType": "Single-Pivot | Dual-Pivot | Pass",
  "nLead": 4,
  "wR": 0.35,
  "m3": 54.8,
  "intradayBiasConsistentR": 3,
  "expectedRoi": 116.5,
  "hitRate": 62.4,
  "breakEvenRate": 53.0,
  "scenario": "ナイター含水率・砂厚・当日バイアス・3〜4MECEシナリオ要約(80字以内)",
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
      "tags": ["F:実績/馬場", "H:補正根拠"],
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

    if skill == "app-bayesian-win5":
        return f"""
あなたは JRA WIN5専用「app-bayesian-win5 (v11.1 Neon Plan C)」エンジンです。
対象日: {date_str}
{common}

【WIN5 v11.1固有ルール】
- 全5レースの全出走馬を並列取得し、2-Stage Benter融合（来日トップ外国馬参戦レースは wR=0.55〜0.60）で各レースの勝率 f, fFund, q を算出。
- 乾燥ダート戦は上位4頭内に差し馬枠（closer）を最低1頭確保。
- 当日1R〜8Rバイアス同化は3R以上一致・ラップ整合時のみ反映（未満は±5%上限）。
- Plan C 確率シェル直交分解（T1 Core は予算上限45%厳守、T2〜T4 Wing は重複ゼロの3〜4チケット構成）。
- 5レース目の単勝ヘッジ候補 hedgeCandidates も出力。

【厳守JSONスキーマ】
{{
  "date": "{date_str}",
  "skill": "app-bayesian-win5",
  "difficulty": "A | B | C",
  "legs": [
    {{
      "venue": "東京10R",
      "name": "レース名",
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

    # Default: app-bayesian-horse-racing-text (JRA平場・重賞)
    return f"""
あなたは JRA平場・重賞専用「app-bayesian-horse-racing-text (v7.0 Neon)」エンジンです。
対象日: {date_str} / 対象レース: {race_query}
{common}

【JRA平場・重賞固有ルール】
- 来日トップ外国馬と日本馬の海外大敗帰りを厳密分離（来日トップ外国馬には疲労上限を適用せず wR>=0.40 で独立評価）。
- 3〜4歳ダート2連勝以上昇級馬・小幅距離延長の成長余地加点則（△/☆_riser）。
- 目標: hitRate>=60%（16〜18頭重賞>=55%）, breakEvenRate>=45%, expectedRoi>=102%（未達なら rank="Pass", pivotType="Pass"）。

【厳守JSONスキーマ】
{{
  "raceId": "YYYYMMDD-jra-RR",
  "org": "JRA",
  "venue": "東京11R",
  "name": "レース名",
  "surfaceDist": "芝1600m",
  "postTime": "15:40",
  "skill": "app-bayesian-horse-racing-text",
  "strategyProfile": "hit_rate_max",
  "rank": "S | A | B | Pass",
  "pivotType": "Single-Pivot | Dual-Pivot | Pass",
  "nLead": 3,
  "rpci": 50.5,
  "wR": 0.35,
  "m3": 52.4,
  "intradayBiasConsistentR": 3,
  "intradayBias3R": true,
  "expectedRoi": 111.5,
  "hitRate": 61.2,
  "breakEvenRate": 54.0,
  "scenario": "当日バイアス・展開・3〜4MECEシナリオ重み要約(80字以内)",
  "activeModules": ["2-Stage Benter融合", "当日3R一致バイアス"],
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
      "tags": ["F:実績/時計", "H:補正理由"],
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
    """ThinkingConfig付きでAPI呼出。429上限時は相方モデルへ自動フォールバック"""
    fallback_model = FAST_MODEL if model == HIGH_TIER_MODEL else HIGH_TIER_MODEL
    candidates: list[tuple[str, str]] = [(model, thinking_level)]
    if fallback_model != model:
        fb_level = "medium" if fallback_model == FAST_MODEL else "high"
        candidates.append((fallback_model, fb_level))

    last_err: Exception | None = None
    for idx, (cur_model, cur_level) in enumerate(candidates):
        for attempt in range(retries + 1):
            try:
                config_kwargs: dict[str, Any] = {
                    "tools": [types.Tool(google_search=types.GoogleSearch())],
                    "temperature": 0.2,
                }
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
                last_err = exc
                err_str = str(exc)
                # 429 (レート上限) や 404 (モデル不在) は即座にフォールバックモデルへ切替
                if ("429" in err_str or "RESOURCE_EXHAUSTED" in err_str or "404" in err_str) and idx < len(candidates) - 1:
                    print(f"[FALLBACK] {cur_model} failed ({err_str[:120]}) -> switching to {candidates[idx + 1][0]}", file=sys.stderr)
                    break
                if attempt < retries:
                    wait_sec = 3 * (attempt + 1)
                    print(f"[RETRY {attempt + 1}/{retries}] {cur_model}: {exc} -> sleep {wait_sec}s", file=sys.stderr)
                    time.sleep(wait_sec)
    raise RuntimeError(f"Gemini call failed across models: {last_err}") from last_err


def validate_and_normalize_race(
    race: dict[str, Any],
    skill: str,
    stage: str = "final",
) -> dict[str, Any]:
    race.setdefault("skill", skill)
    race.setdefault("strategyProfile", "hit_rate_max")
    race["org"] = detect_org(race)
    race["stage"] = stage
    race["updatedAt"] = now_jst_str()

    if not race.get("raceId"):
        slug = re.sub(r"\s+", "-", f"{race.get('venue', 'race')}-{race.get('name', 'unknown')}")
        race["raceId"] = slug

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
    if org_arg.upper() == "ALL":
        return ["JRA", "NAR"]
    return [org_arg.upper()]


def run_screening(client: genai.Client, store: dict[str, Any], org_arg: str, date_str: str) -> None:
    for org in resolve_orgs(org_arg):
        print(f"[SCREENING] {date_str} {org} ({FAST_MODEL}, thinking=medium)")
        prompt = build_screening_prompt(org, date_str)
        res = call_gemini_json(client, FAST_MODEL, prompt, thinking_level="medium")
        if res.get("hasHolding") is False:
            print(f"[INFO] No {org} races scheduled on {date_str}.")
            continue

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

        print(f"[SCREENING] Upserted {len(screened_races)} {org} races.")
        save_store(store)


def run_hourly(
    client: genai.Client,
    store: dict[str, Any],
    org_arg: str,
    date_str: str,
    force_all: bool = False,
) -> None:
    target_orgs = resolve_orgs(org_arg)

    for org in target_orgs:
        has_org_races = any(detect_org(r) == org for r in store.get("races", []))
        if not has_org_races:
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
        if force_all:
            due_races.append(race)
        elif mins is not None and HOURLY_WINDOW_MIN <= mins <= HOURLY_WINDOW_MAX:
            due_races.append(race)
        else:
            print(f"[SKIP] {race.get('venue')} {race.get('name')} (post={race.get('postTime')}, delta={mins})")

    print(f"[HOURLY] Due races to finalize: {len(due_races)}")
    for race in due_races:
        skill = race.get("skill") or (
            "app-bayesian-nar" if detect_org(race) == "NAR"
            else ("app-bayesian-make-debut" if "新馬" in str(race.get("name", "")) else "app-bayesian-horse-racing-text")
        )
        race_query = f"{race.get('venue', '')} {race.get('name', '')} ({race.get('surfaceDist', '')} 発走{race.get('postTime', '')})".strip()
        model, t_level = select_model_and_thinking(skill, race_query, str(race.get("rank") or ""))
        print(f"[HOURLY-PREDICT] {skill} ({model}, thinking={t_level}) -> {race_query}")
        try:
            prompt = build_prompt_for_skill(skill, race_query, date_str)
            pred = call_gemini_json(client, model, prompt, thinking_level=t_level)
            if race.get("raceId"):
                pred["raceId"] = race["raceId"]
            normalized = validate_and_normalize_race(pred, skill, stage="final")
            upsert_race(store, normalized, allow_downgrade=True)
            save_store(store)
        except Exception as exc:
            print(f"[WARN] Failed hourly prediction for {race_query}: {exc}", file=sys.stderr)

    if "NAR" in target_orgs:
        existing_triple = store.get("tripleUmatan") or {}
        if existing_triple.get("date") != date_str:
            nankan_10r = [
                r for r in store.get("races", [])
                if detect_org(r) == "NAR"
                and any(v in str(r.get("venue", "")) for v in NANKAN_VENUES)
                and ("10R" in str(r.get("venue", "")) or r.get("raceNumber") == 10)
            ]
            for r10 in nankan_10r:
                mins = minutes_until_post(date_str, str(r10.get("postTime") or ""), ref_now)
                if force_all or (mins is not None and HOURLY_WINDOW_MIN <= mins <= HOURLY_WINDOW_MAX):
                    venue_name = next(v for v in NANKAN_VENUES if v in str(r10.get("venue", "")))
                    print(f"[TRIPLE-UMATAN] Generating for {venue_name} ({HIGH_TIER_MODEL}, thinking=high)")
                    try:
                        t_prompt = build_triple_umatan_prompt(venue_name, date_str)
                        store["tripleUmatan"] = call_gemini_json(client, HIGH_TIER_MODEL, t_prompt, thinking_level="high")
                        save_store(store)
                    except Exception as exc:
                        print(f"[WARN] Triple Umatan generation failed: {exc}", file=sys.stderr)
                    break


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
        prompt = f"""
以下のレースの公式確定結果（1〜3着馬番）と公式払戻金をGoogle検索で確認し、10,000円基準の推定払戻金（Drop-Buffered Core Shield配分）を算出して単一JSONのみで返してください。
対象日: {store['date']} / レース: {race.get('venue')} {race.get('name')}
推奨◎○▲☆: {[f"{h.get('mark')}{h.get('num')}{h.get('name')}" for h in (race.get('horses') or [])[:5]]}
推奨Core結線: {race.get('coreConnections')}
推奨馬券: {race.get('tickets')}
配分ルール: {race.get('portfolioRules')}

未確定・中止の場合は {{"settled": false}} を返してください。確定済みの場合は以下の形式で返してください:
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
        except Exception as exc:
            print(f"[WARN] Audit failed for {race.get('raceId')}: {exc}", file=sys.stderr)

    if updated_any:
        save_store(store)


def main() -> None:
    parser = argparse.ArgumentParser(description="Bayesian Keiba AI Neon Pipeline (Hydrogen Hybrid)")
    parser.add_argument(
        "--mode",
        choices=["screening", "hourly", "predict", "win5", "audit"],
        required=True,
    )
    parser.add_argument("--date", default=now_jst().strftime("%Y-%m-%d"))
    parser.add_argument("--org", choices=["JRA", "NAR", "ALL"], default="JRA")
    parser.add_argument("--skill", default="app-bayesian-horse-racing-text")
    parser.add_argument("--race", default="", help="例: 東京11R 霜月S / 大井11R サンタアニタT")
    parser.add_argument(
        "--force",
        action="store_true",
        help="hourly モードで発走時刻ウィンドウを無視して未確定レースをすべて本予想化",
    )
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
        model, t_level = select_model_and_thinking(args.skill, args.race, rank="A")
        print(f"[RUN] {args.skill} ({model}, thinking={t_level}) -> {args.race}")
        prompt = build_prompt_for_skill(args.skill, args.race, args.date)
        race_json = call_gemini_json(client, model, prompt, thinking_level=t_level)
        normalized = validate_and_normalize_race(race_json, args.skill, stage="final")
        upsert_race(store, normalized, allow_downgrade=True)
        save_store(store)

    elif args.mode == "win5":
        print(f"[RUN] app-bayesian-win5 ({HIGH_TIER_MODEL}, thinking=high) -> {args.date}")
        prompt = build_prompt_for_skill("app-bayesian-win5", "WIN5", args.date)
        store["win5"] = call_gemini_json(client, HIGH_TIER_MODEL, prompt, thinking_level="high")
        save_store(store)

    elif args.mode == "audit":
        run_audit(client, store, args.org)


if __name__ == "__main__":
    main()
