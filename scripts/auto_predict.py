import os
import json
import glob
from datetime import datetime, timedelta, timezone
from google import genai
from google.genai import types

JST = timezone(timedelta(hours=9))
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

# 作成したアプリ専用スキルのプロンプト定義ファイルを読み込む関数
def load_skill_prompt(skill_name: str) -> str:
    path = f"skills/{skill_name}/SKILL.md"
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def call_gemini_json(skill_name: str, race_input: str, use_pro: bool = True) -> dict:
    """構造化JSONのみを返させて出力トークンを最小化する"""
    model_id = "gemini-2.5-pro" if use_pro else "gemini-2.5-flash"
    system_instruction = load_skill_prompt(skill_name)
    
    response = client.models.generate_content(
        model=model_id,
        contents=race_input,
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            response_mime_type="application/json",
            temperature=0.1,
        ),
    )
    return json.loads(response.text)

def run_morning_screening(date_str: str, card_data: dict) -> dict:
    """【朝1回のみ実行】会場ごとに全12Rを一括スクリーニング（計2〜3リクエスト）"""
    skill_prompt = "app-bayesian-horse-racing-text"
    screened_races = []
    for venue, venue_payload in card_data["venues"].items():
        prompt = f"【モード: スクリーニング】日付:{date_str} 会場:{venue}\n{json.dumps(venue_payload, ensure_ascii=False)}"
        res = call_gemini_json(skill_prompt, prompt, use_pro=False)
        screened_races.extend(res.get("races", []))
    return screened_races

def run_one_hour_before(date_str: str):
    """【発走1時間前チェック】現在時刻から45〜75分後に発走するレースのみ本予想を実行"""
    now = datetime.now(JST)
    db_path = f"data/{date_str}.json"
    with open(db_path, "r", encoding="utf-8") as f:
        day_db = json.load(f)

    updated = False
    for race in day_db["races"]:
        # すでに本予想済み、または見送り(Pass)設定のレースはAPI節約のためスキップ
        if race.get("predicted") or race.get("rank") == "Pass":
            continue

        post_dt = datetime.strptime(f"{date_str} {race['postTime']}", "%Y-%m-%d %H:%M").replace(tzinfo=JST)
        mins_to_post = (post_dt - now).total_seconds() / 60.0

        if 45 <= mins_to_post <= 75:
            is_debut = "新馬" in race["name"]
            skill_name = "app-bayesian-make-debut" if is_debut else "app-bayesian-horse-racing-text"
            use_pro = race.get("rank") in ("S", "A", "New")

            # TARGET出力テキストまたは直前オッズ・馬体重データを結合
            race_raw = race.get("rawInput", json.dumps(race, ensure_ascii=False))
            pred_json = call_gemini_json(skill_name, f"【モード: 標準】\n{race_raw}", use_pro=use_pro)

            race.update(pred_json)
            race["predicted"] = True
            race["updatedAt"] = now.strftime("%H:%M")
            updated = True

    # WIN5（Leg 1発走の1時間前に5鞍一括で1リクエスト実行）
    win5_info = day_db.get("win5", {})
    if win5_info and not win5_info.get("predicted"):
        leg1_dt = datetime.strptime(f"{date_str} {win5_info['leg1PostTime']}", "%Y-%m-%d %H:%M").replace(tzinfo=JST)
        if 45 <= (leg1_dt - now).total_seconds() / 60.0 <= 75:
            win5_res = call_gemini_json("app-bayesian-win5", json.dumps(win5_info["rawInput"], ensure_ascii=False), use_pro=True)
            day_db["win5"].update(win5_res)
            day_db["win5"]["predicted"] = True
            updated = True

    if updated:
        with open(db_path, "w", encoding="utf-8") as f:
            json.dump(day_db, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    today_str = datetime.now(JST).strftime("%Y-%m-%d")
    if os.path.exists(f"data/{today_str}.json"):
        run_one_hour_before(today_str)
