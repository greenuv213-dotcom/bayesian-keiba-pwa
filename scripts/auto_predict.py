#!/usr/bin/env python3
"""
Bayesian Keiba AI — Automated Prediction & Audit Pipeline (Neon v7.0 / v11.1 Edition)

Supports:
  - JRA Flat / Grade (app-bayesian-horse-racing-text)
  - JRA Make Debut (app-bayesian-make-debut)
  - NAR Local / Nankan / Triple Umatan (app-bayesian-nar)
  - JRA WIN5 Plan C (app-bayesian-win5)
  - Post-Race 10,000 JPY Baseline Audit & ROI Tracking
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import sys
from pathlib import Path
from typing import Any

from google import genai
from google.genai import types

# ===== 設定（環境変数で上書き可能）=====
HIGH_TIER_MODEL = os.getenv("GEMINI_HIGH_TIER_MODEL", "gemini-2.5-pro")
FAST_MODEL = os.getenv("GEMINI_FAST_MODEL", "gemini-2.5-flash")
DATA_DIR = Path(os.getenv("KEIBA_DATA_DIR", "data"))
LATEST_JSON_PATH = DATA_DIR / "latest.json"
HISTORY_DIR = DATA_DIR / "history"
JST = dt.timezone(dt.timedelta(hours=9))


def now_jst_str() -> str:
    return dt.datetime.now(JST).strftime("%Y-%m-%d %H:%M JST")


def select_model(skill: str, race_name: str = "") -> str:
    """WIN5・重賞・新馬戦・ダートグレードは上位モデル、それ以外は高速モデルへ振り分け"""
    high_keywords = ("G1", "G2", "G3", "GI", "GII", "GIII", "Jpn", "重賞", "新馬", "WIN5")
    if skill in ("app-bayesian-win5", "app-bayesian-make-debut"):
        return HIGH_TIER_MODEL
    if any(k in race_name for k in high_keywords):
        return HIGH_TIER_MODEL
    return FAST_MODEL


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
        {{ "mark": "◎", "num": 5, "name": "馬名", "shell": "Core | Wing", "f": 28.5, "fFund": 30.0, "q": 25.0, "wUsed": 0.40, "odds": 3.2, "comment": "35字以内" }}
      ]
    }}
  ],
  "planC": {{
    "tickets": [
      {{ "id": "T1", "label": "Core本線(45%上限)", "formation": "5,8 × 2,4 × 1,9 × 6 × 3,7", "points": 32, "hitProb": 8.4 }}
    ]
  }},
  "hedgeCandidates": [{{ "num": 11, "name": "馬名", "odds": 14.5 }}]
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
    """モデル出力からJSONオブジェクトを安全に抽出"""
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


def validate_and_normalize_race(race: dict[str, Any], skill: str) -> dict[str, Any]:
    """Neon v7.0 新フィールドを透過保持しつつ後方互換キーを正規化"""
    race.setdefault("skill", skill)
    race.setdefault("strategyProfile", "hit_rate_max")
    race.setdefault("org", "NAR" if "nar" in skill else "JRA")

    if "intradayBiasConsistentR" not in race and "intradayBias3R" in race:
        race["intradayBiasConsistentR"] = 3 if race["intradayBias3R"] else 1

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


def call_gemini_json(client: genai.Client, model: str, prompt: str) -> dict[str, Any]:
    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config=types.GenerateContentConfig(
            tools=[types.Tool(google_search=types.GoogleSearch())],
            temperature=0.2,
        ),
    )
    if not response.text:
        raise RuntimeError("Gemini API returned empty text.")
    return extract_json(response.text)


def load_store(date_str: str) -> dict[str, Any]:
    if LATEST_JSON_PATH.exists():
        data = json.loads(LATEST_JSON_PATH.read_text(encoding="utf-8"))
        if data.get("date") == date_str:
            return data
    return {
        "date": date_str,
        "updatedAt": now_jst_str(),
        "races": [],
        "win5": None,
        "tripleUmatan": None,
    }


def save_store(store: dict[str, Any]) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    HISTORY_DIR.mkdir(parents=True, exist_ok=True)
    store["updatedAt"] = now_jst_str()
    payload = json.dumps(store, ensure_ascii=False, indent=2)
    LATEST_JSON_PATH.write_text(payload, encoding="utf-8")
    hist_path = HISTORY_DIR / f"{store['date']}.json"
    hist_path.write_text(payload, encoding="utf-8")
    print(f"[OK] Saved {LATEST_JSON_PATH} & {hist_path}")


def upsert_race(store: dict[str, Any], new_race: dict[str, Any]) -> None:
    rid = new_race.get("raceId")
    races = store.setdefault("races", [])
    for idx, existing in enumerate(races):
        if existing.get("raceId") == rid:
            if "result" in existing and "result" not in new_race:
                new_race["result"] = existing["result"]
            races[idx] = new_race
            return
    races.append(new_race)


def run_audit(client: genai.Client, store: dict[str, Any]) -> None:
    """確定レースの公式着順・払戻を自動取得し、1万円基準の的中・払戻金を更新"""
    targets = [
        r for r in store.get("races", [])
        if r.get("rank") != "Pass" and r.get("subRank") != "Pass" and not (r.get("result") or {}).get("settled")
    ]
    if not targets:
        print("[INFO] No unsettled races to audit.")
        return

    for race in targets:
        prompt = f"""
以下のレースの公式確定結果と払戻金をGoogle検索で確認し、10,000円基準の推定払戻金を算出して単一JSONのみで返してください。
対象日: {store['date']} / レース: {race.get('venue')} {race.get('name')}
推奨Core結線: {race.get('coreConnections')} / 推奨馬券: {race.get('tickets')}

未確定の場合は {{"settled": false}} を返してください。確定済みの場合は以下の形式で返してください:
{{
  "settled": true,
  "order": "1着番-2着番-3着番",
  "payout10k": 12400,
  "note": "30字以内の結果・3要因振り返り"
}}
""".strip()
        try:
            res = call_gemini_json(client, FAST_MODEL, prompt)
            if res.get("settled"):
                race["result"] = res
                print(f"[AUDIT] {race.get('venue')} {race.get('name')} -> {res.get('order')} / ¥{res.get('payout10k')}")
        except Exception as exc:
            print(f"[WARN] Audit failed for {race.get('raceId')}: {exc}", file=sys.stderr)


def main() -> None:
    parser = argparse.ArgumentParser(description="Bayesian Keiba AI Neon Pipeline")
    parser.add_argument("--mode", choices=["predict", "win5", "audit"], required=True)
    parser.add_argument("--date", default=dt.datetime.now(JST).strftime("%Y-%m-%d"))
    parser.add_argument("--skill", default="app-bayesian-horse-racing-text")
    parser.add_argument("--race", default="", help="例: 東京11R 霜月S / 大井11R サンタアニタT")
    args = parser.parse_args()

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise EnvironmentError("GEMINI_API_KEY is not set.")

    client = genai.Client(api_key=api_key)
    store = load_store(args.date)

    if args.mode == "predict":
        if not args.race:
            raise ValueError("--race is required for predict mode.")
        model = select_model(args.skill, args.race)
        print(f"[RUN] {args.skill} ({model}) -> {args.race}")
        prompt = build_prompt_for_skill(args.skill, args.race, args.date)
        race_json = call_gemini_json(client, model, prompt)
        normalized = validate_and_normalize_race(race_json, args.skill)
        upsert_race(store, normalized)
        save_store(store)

    elif args.mode == "win5":
        model = select_model("app-bayesian-win5", "WIN5")
        print(f"[RUN] app-bayesian-win5 ({model}) -> {args.date}")
        prompt = build_prompt_for_skill("app-bayesian-win5", "WIN5", args.date)
        store["win5"] = call_gemini_json(client, model, prompt)
        save_store(store)

    elif args.mode == "audit":
        run_audit(client, store)
        save_store(store)


if __name__ == "__main__":
    main()
