---
name: app-bayesian-make-debut
description: App-dedicated copy of bayesian-make-debut (v7.2 Neon Balanced ROI Edition) for the JRA Racing AI PWA and 1-hour-before pipeline. Executes mandatory full-field evaluation, strict 0.0-100.0 percentage output (no decimals), 2-Stage Benter Bayesian Fusion (odds-blind fFund pooled with FLB de-vigged q via adaptive wR, protecting O<=4.5 Top-2 favs at wR>=0.42 unless Dirt <=400kg / severe Type II / verified Overbet 危, capping O>=8x at min(18%, q+10pt) and O>=50x at <=5.5%), 3-race-consistent morning 1R-4R venue bias guard, full-field exact Plackett-Luce, workout confrontation graph, gate-to-4C positional micro-simulation, rule-stacking soft clamp, counterfactual self-audit, 10-Module Make Debut physics (including Dirt <420kg penalty / <=400kg ◎ ban & Dirt inner-gate Top-2 fav / turf-start / wet <=1200m soft cap), Overbet 6-Trigger Filter, Mid-Longshot Override, ◎ 1.2-4.5x anchor band & ◎-☆/Top2-Fav mandatory Core connection, single-longshot <=30% cap, Core 62% (2-4 Wide lines) / Alpha 38% (◎ Win protection + 2 Quinellas + compact Trio), synthetic-odds <1.08x / avgWide <2.8x / <=8-runner auto-Pass, and Win-Reach Hedge, outputting backward-compatible compact JSON.
---

# App Bayesian Make Debut (v7.2 — Neon v12.0 Balanced ROI JSON Edition)

Autonomous hierarchical Bayesian analysis system tailored for **JRA Make Debut (新馬戦 / メイクデビュー, all runners $n_i = 0$)** dedicated to the **Racing AI App (PWA) and automated 1-hour-before GitHub Actions pipeline**. Synchronized with `auto_predict.py` (**v12.0-neon**), combining mandatory full-field evaluation, **strict `0.0–100.0` percentage output (Patch S7)**, **2-Stage Benter Bayesian Fusion with Top-2 market favorite protection (`O <= 4.5` $w_{r,i} \ge 0.42$ unless Dirt $\le 400\text{kg}$, severe Type II `+14kg+`, or verified `F`-level Overbet `危` — Patch S5)**, **mid/extreme-longshot caps (`O >= 8.0x`: `min(18.0%, q + 10.0%)`; `O >= 50.0x`: `<= 5.5%` — Patch S6)**, 3-race-consistent morning 1R–4R venue bias guard, full-field exact Plackett-Luce, workout confrontation graph, gate-to-4C positional micro-simulation, rule-stacking soft clamp, 10-Module Make Debut physics, **`◎` 1.2–4.5x anchor band**, mandatory `◎-☆` & Top-2 market-favorite Core connection, single-longshot $\le 30\%$ cap, **Core 62% / Alpha 38% (`◎` Win priority protection + 2 Quinellas + compact Trio)**, auto-Pass gating (`coreSyntheticOdds < 1.08x`, `avgCoreWide < 2.8x`, `◎` outside `1.2–4.5x`, or `<= 8` runners compressed odds), Quantitative Win-Reach Hedge, and Counterfactual Self-Audit—while outputting **backward-compatible compact JSON**.

## When to Use

  - **Morning Batch Screening (`朝一括スクリーニング`)**: Filtering all Make Debut races using **Top-3 Posterior Mass ($M_3$)**, Chaos Type (`Type S/A/B/B+`), `◎` odds (`1.2–4.5x`), Core synthetic odds, average Core Wide odds, and Expected ROI into `New` (`subRank`: `A` 勝負新馬 / `Pass` 見送り).
  - **1-Hour-Before Automated Prediction (`発走1時間前本予想`)**: Generating full-field odds-blind `fFund` and 2-Stage Benter Fused Plackett-Luce probabilities (`f`, `fFund`, `q`, `top2`, `top3`, `wUsed`, `mark`, `role`, `tags`), `coreConnections`, Core 62% / Alpha 38% `portfolioRules`, `winReachHedge`, and `counterfactualAudit` in compact JSON.
  - **Weekend Post-Race Audit & Skill Patch Generation (`事後検証・スキル改訂パッチ生成`)**: Decomposing Make Debut results across 3 factors and outputting an actionable skill patch.

## Steps

### Step 0: Mandatory Full-Field Data Gate (`全頭取得必須ゲート`)

  - **No Partial-Field Prediction**: Inspect **all $N$ active declared runners** (gate, horse number, name, sex/age, carried weight & apprentice claim `▲☆◇★`, jockey, trainer, Sire × BMS, breeder/gaikyu, latest live odds, and official race-day horse weights vs. mid-week training center weights once announced ~50–60 min pre-post). Exclude scratched/withdrawn (`取消・除外`) runners completely before normalization.
  - **Hybrid Auto-Fetch**: When invoked with search enabled and partial/missing inputs, automatically gather missing full-field entries, chronological workouts, sparring partner classes, gate test times, mid-week/official horse weights, cushion value/moisture/wind, and same-day morning 1R–4R results. Never fabricate unpublished data; mark missing items as `未発表` in `triggers`.

### Step 1: Selective Resource Loading, Evidence Taxonomy (F / E / H), Confrontation Graph & Regularization Clamp

  - Load `references/make_debut_priors.md` via `skills:get_skill_resources` when running full `標準` predictions if not already in context.
  - Classify every input strictly into **`F` (Verifiable Fact)**, **`E` (Validated Effect)**, or **`H` (Heuristic / Candidate Prior)** on a dimensionless Plackett-Luce logit scale ($\theta_i \in \mathbb{R}$, baseline $0.00$), separating 1st-place shift ($\Delta \theta^{(1)}_i$), 2nd/3rd retention ($\delta^{\text{place}}_i$), and uncertainty ($\sigma_i^2$).
  - **Workout Confrontation Graph**: Calibrate sparring results against the sparring partner's actual JRA class and cross-center clock standards.
  - **Collinearity Guard & Global Soft-Clamp Regularization**: Bound combined camp/pedigree shifts at $\Delta \theta_{\text{camp}} \le +0.20$, overlapping positional synergy at $\le +0.20$, and enforce the **global soft regularization clamp ($|\sum \Delta \theta_i| \le 0.45$, $\delta^{\text{place}}_i \in [-0.30, +0.25]$)** unless overridden by indisputable `F`-level discontinuity (e.g., Dirt $\le 400\text{kg}$ physique wall or gate re-test).

### Step 2: Ten-Module Make Debut Physics (100% Synced with v7.2)

Evaluate all $N$ active runners ($n_i = 0$) internally across all 10 modules before generating JSON:

1.  **Module 1 — Dirt Untested Kickback Hazard, Inner-Gate Soft Cap, Ultra-Lightweight Penalty & Outer/Large-Frame Bonus (`Patch S1`)**:
      - **Standard Inner-Frame Kickback Hazard (Frames 1–2 on Good/Dry Dirt)**: Apply $\Delta \theta^{(1)}_i \in [-0.22, -0.35], \delta^{\text{place}}_i \in [-0.10, -0.18], \sigma_i^2 \uparrow$, bar from `Single-Pivot`, unless lone-lead gate ($\le 11.8\text{s}$), $\ge 500\text{kg}$ with 3-horse kickback training, or mitigated by the Soft Cap below.
      - **Top-2 Market Favorite, Turf-Start & Wet-Sprint Inner-Gate Soft Cap**: On **重・不良 $\le 1200\text{m}$**, waive the inner penalty ($0.00\text{ to }+0.08$). On **turf-start dirt** OR for a **Top-2 market favorite ($O_i \le 4.5$)** lacking verified `危` workout/gate/$\le 400\text{kg}$ flaws, **cap the inner kickback penalty to $\Delta \theta^{(1)}_i \in [-0.08, -0.12], \delta^{\text{place}}_i \in [-0.05, -0.08]$, maintain $w_{r,i} \ge 0.42$, and strictly prohibit `消` or disconnecting it from `◎` Core connections**.
      - **Dirt Make Debut Ultra-Lightweight Physique Penalty**: On `良・稍重` dirt Make Debuts, penalize body weight **$< 420\text{kg}$** by $[-0.14, -0.22], \delta^{\text{place}}_i \in [-0.10, -0.16]$. If **$\le 400\text{kg}$**, strictly prohibit `◎` & `Single-Pivot` and boost competing $\ge 470\text{kg}$ runners ($+0.08\text{ to }+0.12$).
      - **Outer-Frame & Large-Frame Bonus (Frames 6–8)**: Forward/stalkers with Colts/Geldings $\ge 480\text{kg}$ (Fillies $\ge 460\text{kg}$) gain $[+0.15, +0.25], \delta^{\text{place}}_i \in [+0.06, +0.12]$.
2.  **Module 2 — Turf 3-Regime Cushion Value (`CV`), Opening-Week Rail & High-CV Sprint Persistence**:
      - High-Rebound Opening-Week (`CV >= 9.8–10.0`): Boost Frames 1–3 with gate 1F $\le 12.0\text{s}$ ($+0.08\text{ to }+0.15$); penalize wide closers ($-0.08\text{ to }-0.14$).
      - Low-Rebound Tough Turf ($\text{CV} < 8.8$ or Moisture $\ge 15\%$) & Subarctic Turf (`札幌・函館`): Attenuate fast-track 1F bonuses by 50% ($\le +0.05$) and upgrade sustained woodchip/slope loads + European/Roberto pedigrees.
      - High-CV ($\ge 9.6$) Turf Sprint (1200m–1400m): Boost Frames 6–8 with fast gate/Slope dash ($+0.10\text{ to }+0.18$).
3.  **Module 3 — Winning 4th-Corner Feasibility Gate ($\le 0.6\text{s}$) vs. $N_{\text{lead}} \ge 4$ Pace-Collapse Closer**:
      - $N_{\text{lead}} \le 2\text{–}3$ ($\text{RPCI} \ge 58.5$): Boost runners projected within $\le 0.6\text{s}$ at 4C with 1F $\le 11.3\text{s}$ ($+0.12\text{ to }+0.18$); attenuate deep closers' 1st-place ($-0.10\text{ to }-0.18$) while preserving $\delta^{\text{place}}_i \in [+0.10, +0.18]$ as `Connector`.
      - $N_{\text{lead}} \ge 4$ ($\text{RPCI} \le 48.5$): Trigger $\pi_{\text{collapse}} \ge 35\%\text{–}45\%$ and elevate `#1` pack-tolerant closer (`☆_closer`).
4.  **Module 4 — Educational / Classic-Target Debut Favorite Fade vs. Lone-Speed Steal**:
      - Attenuate 1st-place ($-0.10\text{ to }-0.18$, bar `Single-Pivot`) for educational-riding favorites while boosting $\delta^{\text{place}}_i \in [+0.10, +0.18]$ as `High-Floor Connector (◯/▲)` and elevating `#1` lone speed (`☆_pace`).
5.  **Modules 5 & 6 — Fillies-Only Pocket Bonus, Tight-Oval Apprentice Speed & Steep-Uphill Stature Physics**:
      - Fillies-only turf (1400m–1800m): Boost Frames 1–4 with 1F $\le 11.3\text{s}$ ($+0.10\text{ to }+0.16$); penalize Frames 7–8 wide closers.
      - Tight-oval apprentice claims ($50\text{–}52\text{kg}$) with fast gate gain $+0.12\text{ to }+0.18$; steep uphill `< 440kg` full-weight favorites lose $-0.08\text{ to }-0.14$.
6.  **Module 7 — Special-Course Geometry (`新潟芝直1000m`), Sibling Heritage (`△_course_ped`), Mismatch Reset & 3yo Late-Debut Cap**:
      - Niigata 1000m Straight boosts Frames 7–8 ($+0.18\text{ to }+0.28$), penalizes Frames 1–2 ($-0.15\text{ to }-0.25$). Sibling exact-course Top-3 grants $+0.06\text{ to }+0.12$. 3yo setback favorites capped at `fFund <= 30%`.
7.  **Module 8 — Workout 8-Axis Audit, Gate Cap, Pre-Race Transport Loss & Stayer Slope-Only Cap**:
      - Older-Class & Final-2F Sustained Breakers (`+0.16 to +0.24`), High-Class Sparring calibration (`+0.16 to +0.25`), Debut Silver-Collector (`-0.10 to -0.18` 1st, `+0.12 to +0.20` place), Trouble/High-Pace Load Survivor & Pipe-Opener V-Bounce (`+0.08 to +0.18`), Gate/Transport-Loss `-8kg to -12kg` guards, and Stayer Slope-Only Cap (`2000m+` turf / `1800m` dry dirt).
8.  **Modules 9 & 10 — Overbet 6-Trigger Filter (`危`) & Mid-Longshot Override (`☆_override`)**:
      - Only flag a $O_i \le 2.5$ favorite as **`危`** when supported by verifiable `F`-level flaws (light 1-week load, `< 5` breezes, Dirt $\le 400\text{kg}$, severe Type II `+14kg+`, gate re-test, Slope-only 2000m+/D1800m wall, or peak-out reaction). Promote modest-pedigree runners ($O_i \in [8.0, 25.0]$) with $\ge 6\text{–}8$ works + sparring proof via `☆_override` (subject to Patch S6 cap `f <= min(18.0%, q + 10.0%)`).

### Step 3: Gate-to-4C Positional Micro-Simulation, 3-Race Morning Bias Guard, 2-Stage Benter Fusion (`Patch S5/S6/S7`) & Exact Plackett-Luce

1.  **Gate-to-4C Positional Micro-Simulation & Strict 3-Race Morning Venue Bias Guard**:
      - Simulate `発馬 → 芝/ダ境目 → 1角 → 4角0.6秒射程圏 → 直線進路` across **3 to 4 MECE scenarios** ($\sum_s \pi_s^{\text{post}} = 1.00$), including Tail-Risk/Shock ($\pi_{\text{shock}} \in [10\%, 25\%]$).
      - Cap morning 1R–4R venue bias shifts strictly: $\ge 3$ consistent pace-matched races ($\pm 10\%\text{–}20\%$), 2 consistent races ($\pm 6\%\text{–}10\%$), $< 2$ races or pace mismatch ($\le \pm 5\%$).
2.  **2-Stage Benter Bayesian Fusion & Calibration Guardrails (`Patch S5 / S6 / S7`)**:
      - **Stage 1 (Odds-Blind Fundamental `fFund`)**: Compute clean odds-blind win probability `fFund` on a **strict `0.0–100.0` percentage scale** ($\sum f^{\text{fund}} = 100.0\%$).
      - **Stage 2 (Adaptive Market Fusion)**: Compute FLB Power de-vigged $q_i$ ($\gamma \approx 1.08$) and pool via baseline $w_r \in [0.48, 0.55]$: $$\theta^{\text{post}}_{i,s} = (1 - w_{r,i})\tilde{\theta}^{\text{fund}}_{i,s} + w_{r,i} \ln q_i, \qquad \theta^{\text{post},(2,3)}_{i,s} = \theta^{\text{post}}_{i,s} + \delta^{\text{place}}_i$$
      - **Top-2 Market Favorite Protection (`Patch S5`)**: Keep **$w_{r,i} \ge 0.42$** and strictly prohibit `消/危` for any runner with **$O_i \le 4.5\text{x}$** unless backed by Dirt $\le 400\text{kg}$, severe Type II (`+12kg+` in $\ge 1800\text{m}$ / `+14kg+`), or verified `F`-level `危` workout/gate failure.
      - **Calibration Caps (`Patch S6`)**: Cap **`O_i >= 8.0x`** at **`f <= min(18.0%, q_i + 10.0%)`** and **`O_i >= 50.0x`** at **`f <= 5.5%`** (barred from `◎ / ◯ / ▲`).
      - **Strict Percentage Format (`Patch S7`)**: Output ALL probabilities (`f`, `fFund`, `q`, `top2`, `top3`, `m3`, `hitRate`, `breakEvenRate`) strictly in **`0.0–100.0` percentage units** (NEVER `0.0–1.0` decimals). Verify $\sum f = 100.0\%, \sum \text{top2} = 200.0\%, \sum \text{top3} = 300.0\%$.

### Step 4: v12.0 Balanced ROI Portfolio Rules (`Core 62% / Alpha 38%`), `◎` Anchor Discipline & Auto-Pass Gate

  - **Anchor Discipline (`◎ 1.2–4.5x` Band)**: Select **`◎`** from verified high-reliability contenders; if `◎` falls outside **`1.2x–4.5x`**, declare **`subRank: "Pass"` / `rank: "Pass"`**.
  - **Core 62% / Alpha 38% Structure (Synced 100% with `auto_predict.py` v12.0)**:
      - **Core Shield (`62%` = `6,200 JPY`)**: Wide Dutching with mandatory `◎-☆` & Top-2 market-favorite (`O <= 5.0`) connection:
          - $O_{\text{◎}} \le 1.8\text{x}$: **2 Wide lines** (`◎` × top 2 value partners).
          - $1.8\text{x} < O_{\text{◎}} \le 2.2\text{x}$: **3 Wide lines** (`◎-◯`, `◎-▲`, `◎-☆/人気`).
          - $O_{\text{◎}} > 2.2\text{x}$: **4 Wide lines** (`◎-◯`, `◎-▲`, `◯-▲`, `◎-☆/人気`).
      - **Alpha Booster (`38%` = `3,800 JPY`)**:
          - **`◎` Win Priority Protection (`約1,400 JPY`)**: Protect `◎` to win (`単勝 ◎`) when $O_{\text{◎}} \ge 2.0\text{x}$; split across `◎` + `◯` when $O_{\text{◎}} < 2.0\text{x}$ and $O_{\text{◯}} \ge 2.8\text{x}$.
          - **Quinella 2 lines (`約1,600 JPY`)** + **Compact Trio (`約800 JPY`)** + optional **Win-Reach Hedge** (`B_hedge = ⌈G_min / O_j⌉`).
      - **Single-Longshot Cap**: $\le 30\%$ (`3,000 JPY`).
  - **Auto-Pass Gate**: Declare **`Pass`** whenever: (1) live odds missing, (2) `◎` outside `1.2x–4.5x`, (3) `coreSyntheticOdds < 1.08x` OR `avgCoreWide < 2.8x`, OR (4) `<= 8` active runners with compressed odds (`avgCoreWide < 3.0x` or Top-2 favs `<= 2.5x`).
  - **Counterfactual Self-Audit**: Internally verify `◎` failure mode, `◯-▲` coverage, Dirt `> 400kg` check, percentage scaling (`0.0–100.0`), and `O>=8x`/`O>=50x` caps before emitting JSON.

### Step 5: App-Optimized Backward-Compatible JSON Schemas

All existing keys are preserved verbatim for zero-breakage PWA compatibility. Output **ONLY a single valid JSON object** when invoked by the automated pipeline.

#### Mode A: `スクリーニング` (Morning Make Debut Batch Screening JSON)

```json
{
  "date": "YYYY-MM-DD",
  "venue": "東京",
  "strategyProfile": "v12_balanced_roi",
  "trackBias": {
    "turfCv": 9.8,
    "turfMoisture": "11.0%",
    "dirtMoisture": "3.2%",
    "intradayBiasConsistentR": 2,
    "summary": "Aコース開幕週・芝高速良・ダ乾砂"
  },
  "races": [
    {
      "raceNumber": 5,
      "name": "2歳新馬",
      "surfaceDist": "芝1800m",
      "postTime": "12:15",
      "rank": "New",
      "subRank": "A | Pass",
      "chaosType": "Type S | Type A | Type B | Type B+",
      "skill": "app-bayesian-make-debut",
      "pivotType": "Single-Pivot | Dual-Pivot | Pass",
      "nLead": 2,
      "rpci": 59.5,
      "m3": 56.2,
      "coreSyntheticOdds": 1.38,
      "avgCoreWide": 4.4,
      "expectedRoi": 114.2,
      "hitRate": 59.8,
      "breakEvenRate": 49.5,
      "summary": "35字以内の◎オッズ・平均W・M3判定根拠"
    }
  ]
}
```

#### Mode B: `標準` (1-Hour-Before Single-Race Prediction JSON)

Evaluate **all $N$ active declared runners internally** (excluding scratches). Sort `horses` by **Fused Posterior Win Probability `f` descending**, strictly using **`0.0–100.0` percentage values** so $\sum f = 100.0\%$ and $\sum \text{top3} = 300.0\%$:

```json
{
  "raceId": "20261129-tok-05",
  "venue": "東京5R",
  "name": "2歳新馬",
  "surfaceDist": "芝1800m",
  "postTime": "12:15",
  "skill": "app-bayesian-make-debut",
  "strategyProfile": "v12_balanced_roi",
  "rank": "New",
  "subRank": "A | Pass",
  "chaosType": "Type S | Type A | Type B | Type B+",
  "pivotType": "Single-Pivot | Dual-Pivot | Pass",
  "nLead": 2,
  "rpci": 59.5,
  "wR": 0.52,
  "m3": 56.2,
  "coreSyntheticOdds": 1.38,
  "avgCoreWide": 4.4,
  "intradayBiasConsistentR": 2,
  "expectedRoi": 114.2,
  "hitRate": 59.8,
  "breakEvenRate": 49.5,
  "scenario": "午前バイアス(s_venue一致R数)・想定RPCI・3〜4MECEシナリオ要約(80字以内)",
  "activeModules": ["M2:高CV開幕イン先行", "M3:4角0.6s射程圏ゲート", "M8:古馬基準×後半2F突破"],
  "horses": [
    {
      "mark": "◎ | ◯ | ▲ | ☆ | △ | 危",
      "role": "最安定Top-3＆突破軸 | 安定Connector | 中穴Override | 過剰人気危",
      "num": 6,
      "name": "馬名",
      "style": "逃 | 先 | 差 | 追",
      "f": 28.4,
      "fFund": 26.5,
      "q": 30.2,
      "wUsed": 0.52,
      "top2": 48.2,
      "top3": 63.0,
      "odds": 2.6,
      "tags": ["F:CW 6F 80.9-22.4s", "H:古馬基準突破+0.22"],
      "comment": "45字以内のF/H核心根拠"
    }
  ],
  "tailSummary": { "count": 8, "sumF": 11.2, "sumTop3": 36.5 },
  "coreConnections": [[6, 3], [6, 11], [3, 11], [6, 2]],
  "portfolioRules": {
    "coreRatio": 0.62,
    "alphaRatio": 0.38,
    "coreLineCap": 4,
    "singleLongshotCapPct": 0.30
  },
  "winReachHedge": [
    { "num": 11, "name": "馬名", "odds": 12.5, "hedge10k": 800, "hedge20k": 1600 }
  ],
  "counterfactualAudit": "◎出遅れ/進路詰まり時の◯-▲防衛状態と上位人気馬保護状態(60字以内)",
  "triggers": ["直前馬体重(週中比-8kg超Type III・ダート420kg未満警戒)・午前バイアス確認トリガー(45字以内)"]
}
```

#### Mode C: `事後検証` (Weekend Batch Post-Race Audit & Skill Patch JSON)

Output a JSON object containing `auditSummary`, 3-factor decomposition (`scenarioError`, `ratingError`, `portfolioError`), and `skillPatch`.

## Gotchas

  - **NEVER output probabilities as `0.0–1.0` decimals** (e.g., `0.265`); ALWAYS output **`0.0–100.0` percentages** (e.g., `26.5`) so $\sum f = 100.0$.
  - **NEVER hard-fade (`消/危`) or omit from `◎` Core connections a Top-2 market favorite ($O_i \le 4.5$)** lacking Dirt $\le 400\text{kg}$, severe Type II (`+14kg+`), or verified `F`-level `危` workout/gate flaws; maintain $w_{r,i} \ge 0.42$.
  - **NEVER let a mid-longshot ($O_i \ge 8.0\text{x}$) exceed `f = min(18.0%, q + 10.0%)`**, and **NEVER promote an extreme longshot ($O_i \ge 50.0\text{x}$) above `f = 5.5%` or into `◎ / ◯ / ▲`**.
  - Never assign `◎` or `Single-Pivot` to a Dirt newcomer weighing $\le 400\text{kg}$ (penalize `< 420kg` by `-0.14 to -0.22`).
  - Always declare `Pass` when `◎` is outside `1.2x–4.5x`, `coreSyntheticOdds < 1.08x`, `avgCoreWide < 2.8x`, or active field `<= 8` with compressed odds.
  - Always sort `horses` by Fused Posterior Win Probability `f` descending and output valid, parseable JSON without conversational filler in app pipeline mode.
