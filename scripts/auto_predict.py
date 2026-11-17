import os
import re
import time
import json
import glob
from datetime import datetime, timedelta, timezone
from google import genai
from google.genai import types

JST = timezone(timedelta(hours=9))
API_KEY = os.environ.get("GEMINI_API_KEY", "").strip()
client = genai.Client(api_key=API_KEY) if API_KEY else None

# dataフォルダとinputsフォルダが存在しない場合は自動で作成する
os.makedirs("data", exist_ok=True)
os.makedirs("inputs", exist_ok=True)

def load_skill_prompt(skill_name: str) -> str:
    path = f"skills/{skill_name}/SKILL.md"
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return "Output valid JSON only."

def call_gemini_json(skill_name: str, prompt_text: str, prefer_pro: bool = False) -> dict:
    if not client:
        return {"error": "GEMINI_API_KEY is not set"}

    system_instruction = load_skill_prompt(skill_name)
    models_to_try = ["gemini-2.5-pro", "gemini-2.5-flash"] if prefer_pro else ["gemini-2.5-flash"]

    for model_id in models_to_try:
        try:
            time.sleep(4)
            response = client.models.generate_content(
                model=model_id,
                contents=prompt_text,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    response_mime_type="application/json",
                    temperature=0.1,
                ),
            )
            text = (response.text or "").strip()
            if text.startswith("```"):
                text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text, flags=re.DOTALL)
            return json.loads(text)
        except Exception as e:
            print(f"[Warn] {model_id} failed: {e}")
            continue
    return {"error": "API limit or error"}

def load_target_inputs(date_str: str) -> str:
    texts = []
    for ext in ("*.csv", "*.txt", "*.json"):
        for fp in glob.glob(os.path.join("inputs", ext)):
            if date_str.replace("-", "") in fp or date_str in fp or "target" in fp.lower():
                try:
                    with open(fp, "r", encoding="utf-8", errors="ignore") as f:
                        texts.append(f"--- File: {os.path.basename(fp)} ---\n" + f.read()[:15000])
                except Exception:
                    pass
    return "\n".join(texts)

def run_pipeline():
    now = datetime.now(JST)
    date_str = now.strftime("%Y-%m-%d")
    db_path = f"data/{date_str}.json"
    target_extra = load_target_inputs(date_str)

    if os.path.exists(db_path):
        with open(db_path, "r", encoding="utf-8") as f:
            day_db = json.load(f)
    else:
        day_db = {
            "date": date_str,
            "updatedAt": now.strftime("%Y-%m-%d %H:%M JST"),
            "screened": False,
            "audited": False,
            "races": [],
            "win5": {},
            "skillPatches": []
        }

    if target_extra and not day_db.get("screened"):
        prompt = f"【モード: スクリーニング】日付:{date_str}\n{target_extra}"
        res = call_gemini_json("app-bayesian-horse-racing-text", prompt, prefer_pro=False)
        if "races" in res:
            day_db["races"] = res["races"]
            day_db["trackBias"] = res.get("trackBias", {})
            day_db["screened"] = True

    for race in day_db.get("races", []):
        if race.get("predicted") or race.get("rank") == "Pass":
            continue
        post_time = race.get("postTime", "")
        if not re.match(r"^\d{2}:\d{2}$", post_time):
            continue
        post_dt = datetime.strptime(f"{date_str} {post_time}", "%Y-%m-%d %H:%M").replace(tzinfo=JST)
        mins_to_post = (post_dt - now).total_seconds() / 60.0
        if 40 <= mins_to_post <= 80:
            is_debut = "新馬" in race.get("name", "") or race.get("rank") == "New"
            skill_name = "app-bayesian-make-debut" if is_debut else "app-bayesian-horse-racing-text"
            prompt = f"【モード: 標準】日付:{date_str}\n対象レース:{json.dumps(race, ensure_ascii=False)}\n{target_extra[:8000]}"
            pred = call_gemini_json(skill_name, prompt, prefer_pro=(race.get("rank") == "S"))
            if "horses" in pred:
                race.update(pred)
                race["predicted"] = True
                race["predictedAt"] = now.strftime("%H:%M")

    day_db["updatedAt"] = now.strftime("%Y-%m-%d %H:%M JST")
    with open(db_path, "w", encoding="utf-8") as f:
        json.dump(day_db, f, ensure_ascii=False, indent=2)

    all_files = sorted([os.path.basename(p).replace(".json", "") for p in glob.glob("data/20*.json")])
    with open("data/index.json", "w", encoding="utf-8") as f:
        json.dump({"availableDates": all_files, "lastSync": day_db["updatedAt"]}, f, ensure_ascii=False, indent=2)

    print(f"Success: Updated {db_path}")

if __name__ == "__main__":
    run_pipeline()
