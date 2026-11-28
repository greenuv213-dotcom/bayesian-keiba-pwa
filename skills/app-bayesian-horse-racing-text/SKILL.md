---
name: app-bayesian-horse-racing-text
description: App-dedicated copy of bayesian-horse-racing-text (v7.2 Neon Balanced ROI Engine) for the JRA/NAR Racing AI PWA and 1-hour-before pipeline. Excludes obstacle races, executes mandatory full-field evaluation, strict 0.0-100.0 percentage output (no decimals like 0.232), 2-Stage Benter Fusion (fFund + FLB q via wR) with Top-2 market favorite protection (O<=4.5 wR>=0.42, no fade without severe Type II weight disqualify), O>=8.0x calibration cap (min(18%, q+10pt)) and O>=50x cap (<=5.5%), 3-race intraday bias & 3-straight-winner shift, visiting foreign G1 vs returning Japanese split, dirt inner-gate soft cap (Top-2 fav / turf-start / wet <=1200m waiver), 2yo extreme final-2F/record override, long-stretch dirt handicap light closer & gear/weight bounce-back, exact Plackett-Luce, confrontation graph, positional micro-simulation, rule clamp, counterfactual audit, ◎ 1.4-4.0x anchor band & ◎-☆/Top2-Fav mandatory Core connection, single-longshot <=30% cap, Core 62% (2-4 Wide lines) / Alpha 38% (◎ Win protection + 2 Quinellas + compact Trio), synthetic-odds <1.10x / avgWide <3.0x / <=8-runner auto-Pass, Type II/Level B weight alerts, outputting backward-compatible compact JSON for Screening, 1-Hour Prediction, and Post-Race Skill Patch.
---

# App Bayesian Horse Racing (v7.2 — Neon v12.0 Balanced ROI JSON Edition)

Autonomous hierarchical Bayesian analysis system for **JRA Flat Races (芝・ダート平地競走; strictly excluding obstacle races 障害戦) and South Kanto 4 Tracks (南関4場)** dedicated to the **Racing AI App (PWA) and automated 1-hour-before GitHub Actions pipeline**. Synchronized with `auto_predict.py` (**v12.0-neon**), executing mandatory full-field evaluation, **strict `0.0–100.0` percentage scaling (Patch S7)**, **Top-2 market favorite protection (`O <= 4.5` $w_{r,i} \ge 0.42$, no `消/危` without severe Type II weight disqualify — Patch S5)**, **mid/extreme-longshot calibration caps (`O >= 8.0x`: `f <= min(18.0%, q + 10.0%)`; `O >= 50.0x`: `f <= 5.5%` — Patch S6)**, 3-race intraday bias guard, visiting foreign G1 vs. returning Japanese horse split, dirt inner-gate soft cap, 2yo extreme final-2F/record override, long-stretch dirt handicap light closer & gear/weight bounce-back exception, **`◎` 1.4–4.0x anchor discipline** (preventing adverse-selection mid-longshot pivots), mandatory `◎-☆` & Top-2 market-favorite Core connection, single-longshot $\le 30\%$ cap, **Core 62% / Alpha 38% (`◎` Win priority protection + 2 Quinellas + compact Trio)**, and auto-Pass gating (`◎` outside `1.4–4.0x`, `coreSyntheticOdds < 1.10x`, `avgCoreWide < 3.0x`, `M3 < 38%`, or `<= 8` runners compressed odds), while outputting **backward-compatible compact JSON**.

## When to Use

  - **Morning Batch Screening (`朝一括スクリーニング`)**: Filtering all flat races of a venue in a single API call using **Top-3 Posterior Mass ($M_3$)**, `◎` anchor odds (`1.4–4.0x`), Core synthetic odds, average Core Wide odds, and Expected ROI into `S` (最優先勝負), `A` (厳選好機), or `Pass` (見送り).
  - **1-Hour-Before Automated Prediction (`発走1時間前本予想`)**: Generating full-field odds-blind `fFund` and 2-Stage Benter Fused Plackett-Luce probabilities (`f`, `fFund`, `q`, `top2`, `top3`, `wUsed`, `mark`, `role`, `tags`), `alerts` (Type II weight downgrades or Level B conditional fallbacks), and Core 62% / Alpha 38% rules in compact JSON.
  - **Weekend Post-Race Audit & Skill Patch Generation (`事後検証・スキル改訂パッチ生成`)**: Decomposing prediction vs. actual results across 3 factors and outputting an actionable skill patch.

## Steps

### Step 0: Mandatory Full-Field Data Gate, Flat-Only Guard & Weight-Alert Gate (`全頭取得＆平地限定ゲート`)

  - **Flat Races Only**: Never evaluate obstacle/steeplechase races (`障害戦 / 障`); declare `rank: "Pass"` immediately if invoked on one.
  - **No Partial-Field Prediction**: Inspect **all $N$ active declared runners** (gate, horse number, name, sex/age, carried weight, jockey, live odds, and official horse weights/diffs once announced ~50–60 min pre-post). Exclude scratched/withdrawn (`取消・除外`) runners completely before normalization. NEVER leave uninspected horses in an unchecked residual bucket.
  - **1-Hour-Before Weight Auto-Downgrade vs. Level B Conditional Fallback (`alerts` 出力則)**:
      - **Severe Weight Disqualification (`F`-level)**: `+12kg` or more in $\ge 1800\text{m}$, OR `+14kg` or more at any distance. Only these clear physical disqualifications allow hard-fading (`消/危`) a Top-2 market favorite ($O_i \le 4.5$).
      - **When official horse weights ARE available**: Apply Type II (`+8kg` in $\ge 1800\text{m}$ / `+10kg+` gain) downgrades directly inside `fFund`/`f` & `mark`, and record concise diagnostic warnings in `alerts`.
      - **When official horse weights are NOT yet published (`Level B`)**: Emit an explicit conditional fallback rule into `alerts` (and `triggers`) for any weight-sensitive `◎ / ○ / ▲` anchor.

### Step 1: Evidence Taxonomy (F / E / H), Confrontation Graph & Regularization Clamp

  - Classify every input strictly into **`F` (Verifiable Fact)**, **`E` (Validated Effect)**, or **`H` (Heuristic / Candidate Prior)** on a dimensionless Plackett-Luce logit scale ($\theta_i \in \mathbb{R}$, baseline $0.00$), separating 1st-place shift ($\Delta \theta^{(1)}_i$), 2nd/3rd retention ($\delta^{\text{place}}_i$), and uncertainty ($\sigma_i^2$).
  - **Transitive Confrontation Graph & Race-Level Calibration**: Internally evaluate direct meetings, 1-hop shared opponents, weight differentials ($1\text{kg} \approx 0.15\sim 0.20\text{s}$), and same-day class clocks / next-out winners (`ハイレベル戦再評価 [+0.06,+0.14]` vs. `低レベル戦勝ち割引 [-0.06,-0.12]`).
  - **Mechanism Deduplication & Soft-Clamp Regularization**: Merge overlapping Phase 1–4 switches sharing one physical mechanism into a single bounded term ($\le \pm 0.18$) and enforce a **soft clamp ($|\sum \Delta \theta_i| \le 0.45$, $\delta^{\text{place}}_i \in [-0.30, +0.25]$)** unless overridden by clear `F`-level discontinuity.

### Step 2: Core 7-Phase Bayesian Domain Modules (100% Synced with v7.2)

Execute all domain physics internally across all $N$ active runners before generating JSON:

1.  **JRA Turf Cushion Value (`CV`), Moisture & Wind Physics**:
      - **High-Rebound Fast Turf ($\text{CV} \ge 10.0$ / low moisture)**: Boost high cruising speed, inside-rail savers (`A/Bコース` opening weeks and fresh `C/Dコース` Day 1–2), and fast Last-3F accelerators ($+0.06\text{ to }+0.12$); penalize wide deep closers ($-0.06\text{ to }-0.12$).
      - **High-CV ($\ge 9.6$) Turf 1200m Sprint Speed Persistence & Dual Outer-Speed Survival**: Sprinters with opening 3F $\le 33.2\text{s}$ (or Top 2 early speed) in **Frames 6–8** receive $\Delta \theta^{(1)}_i \in [+0.10, +0.18]$ under $\pi_{\text{speed\_persist}} \ge 35\%$.
      - **Nominal-Wet Mid-Race Breather 3yo 54kg Wide-Closer Promotion**: On nominal `稍重〜重` turf with a mid-race breather, grant $\Delta \theta^{(1)}_i \in [+0.10, +0.16]$ to 3yo runners carrying $53\text{–}55\text{kg}$ with proven fast final-3F acceleration sweeping from outer draws.
      - **Low-Rebound Tough Turf ($\text{CV} < 8.5$ or Moisture $\ge 15\%$) & Subarctic Turf (`札幌・函館`)**: Attenuate fast-track 3yo/4yo clock bonuses by 50% ($\le +0.05$) and upgrade proven Subarctic/sustained-pace (`RPCI <= 48.5`) top-3 runners ($\Delta \theta_i \in [+0.08, +0.14], \delta^{\text{place}}_i \in [+0.12, +0.18]$).
      - **Intraday Rain & Straight-Line Wind**: Penalize exposed lone leaders ($\Delta \theta^{(1)}_i \in [-0.10, -0.15]$) under afternoon rain or homestretch headwind $\ge 5\text{m/s}$.

2.  **JRA Dirt / Nankan Moisture, Turf-Start, Wet-Sprint Waiver & Inner-Gate Soft Cap Physics (`Patch S1`)**:
      - **Dry Dirt ($m_{\text{dirt}} < 3.0\%$ / deep sand)** boosts outer power ($[+0.05,+0.10]$) and penalizes kickback-fragile inside draws ($[-0.06,-0.12]$); **Wet Dirt ($m_{\text{dirt}} \ge 6.0\%$)** boosts front/rail speed ($[+0.06,+0.14]$).
      - **Dry/Standard Dirt 15+ Full-Gate Inside Kickback Hazard**: On **Good/Dry dirt at $\ge 1400\text{m}$**, penalize inside-drawn (Frames 1–2) runners lacking proven pack/kickback tolerance ($\Delta \theta^{(1)}_i \in [-0.15, -0.22], \delta^{\text{place}}_i \in [-0.10, -0.18], \sigma_i^2 \uparrow$, **bar from `Single-Pivot`**), subject strictly to the two guardrails below.
      - **Heavy/Sloppy Short-Distance Dirt ($\le 1200\text{m}$) Inside-Speed Waiver**: On **重・不良 dirt sprints ($1000\text{m}\text{–}1200\text{m}$)**, waive the Frames 1–2 inside kickback penalty ($0.00\text{ to }+0.08$) for runners with Top-3 early speed or Top-3 market popularity.
      - **Top-2 Market Favorite, Turf-Start & 3yo/4yo Riser Inner-Gate Soft Cap**: When a Frame 1–2 runner is a **Top-2 market favorite ($O_i \le 4.5$)** OR on **turf-start dirt** OR a **3yo/4yo winning-streak riser ($\ge 2$ consecutive wins, $\le 56\text{kg}$)**, cap its inside-kickback penalty to $\Delta \theta^{(1)}_i \in [-0.08, -0.12]$ and $\delta^{\text{place}}_i \in [-0.05, -0.08]$, maintain fusion weight $w_{r,i} \ge 0.42$ (for $O_i \le 4.5$ lacking severe weight disqualification), and strictly prohibit hard-fading (`消`) or disconnecting it from `◎` Core connections.
      - **Outer Large-Frame Stalker Survival**: Grant $\Delta \theta^{(1)}_i \in [+0.10, +0.16]$ to tactical stalkers/front-runners in **Frames 6–8** (especially $\ge 500\text{kg}$ in tight-oval dirt races).

3.  **Fillies Pocket, Handicap Physics, Class/Age Growth & Dirt Winning-Streak Riser Rules**:
      - **Fillies/Mares-Only Inside-Pocket Bonus**: Grant $\Delta \theta^{(1)}_i \in [+0.10, +0.16], \delta^{\text{place}}_i \in [+0.08, +0.14]$ to fillies/mares in **Frames 1–4** with proven final 1F $\le 11.3\text{s}$; penalize wide closers in **Frames 7–8** on 4-corner/inner tracks ($-0.10\text{ to }-0.14$).
      - **Tight-Oval Local Handicap Light-Weight Boost & Long-Stretch Dirt Handicap Light-Weight Closer Boost**: Boost $50.0\text{–}53.0\text{kg}$ (or $\ge 2.0\text{kg}$ drop) early-speed runners in Frames 1–5 on tight ovals ($+0.14\text{ to }+0.20$), and $\le 54.0\text{kg}$ ($\ge 3.0\text{kg}$ drop or 3yo) closers on long-stretch $\ge 1800\text{m}$ dirt handicaps ($+0.08\text{ to }+0.14$).
      - **3yo/4yo Class-Standard & Final-2F Breaker & Dirt Winning-Streak Riser Rule**: Boost ascending 3yo/4yo winners clearing both upper-class average time AND closing 2F benchmark (Turf $\le 22.8\text{s}$ / Dirt $\le 24.4\text{s}$) by $[+0.14, +0.22]$, and 3yo/4yo dirt $\ge 2$-win streak risers with Top-3 Last-3F by $[+0.08, +0.15]$.
      - **3yo Course-Grade Winner 55kg / Grade-Placed 57kg Exemption & 4yo Classic-Trial Closer**: Grant $[+0.10, +0.16]$ to proven 3yo course-grade winners ($\le 55\text{kg}$) or 57kg Grade-placed 3yos, and elevate 4yo Classic-trial Top-4 closers ($O_i \in [15,60]$) as `☆_closer`.

4.  **Favorite Hazards, Bounce-Back Exceptions, Returning Japanese vs. Visiting Elite Foreign G1 Split, 2yo Extreme Lap Override & Weights**:
      - **Chronic Silver-Collector & Slow-Starter Ceiling**: Cap 1st-place hazard ($\Delta \theta^{(1)}_i \in [-0.12, -0.22]$) while boosting 2nd/3rd retention ($\delta^{\text{place}}_i \in [+0.12, +0.20]$) as Wide Core anchors.
      - **Gear-Change & Weight-Relief Bounce-Back Exception**: Do NOT auto-fade a prior 1st–2nd favorite ($O_{\text{prev}} \le 4.0$) off a blowout if returning with $\ge 2$ structural resets (blinkers, $\ge 2\text{kg}$ relief, or top jockey).
      - **Returning Japanese Overseas Cap vs. Elite Visiting Foreign G1 Split**: Apply overseas fatigue cap ($\sigma_{\text{overseas}}^2 \ge 0.25, f^{\text{fund}}_i \le 20\%$) **strictly to Japanese-trained horses returning from heavy overseas defeats ($\ge 5\text{th}$ or $\ge 1.0\text{s}$)**. Evaluate active **elite visiting foreign G1 contenders** independently with $w_r \ge 0.45$.
      - **Proven Course-G1 Winner Outer-Gate Deep-Wait Override**: Exempt venue long-stretch G1 winners posting S-grade workouts from outer-gate/Silver-Collector penalties.
      - **Extreme 2yo Turf Acceleration / Record Override**: Never drop a 2yo turf record winner or final-2F $\le 22.0\text{s}$ (1F $\le 11.1\text{s}$) qualifier into `無印` solely due to outer draw or minor match-workout lag.
      - **Pre-Race Weight 3-Classification**: **Type I** (`-2kg to -8kg` trim: $[0.00,+0.08]$); **Type II** ($\ge +8\text{kg}$ in $\ge 1800\text{m}$ or $\ge +10\text{kg}$ gain: $[-0.12,-0.22]$; **severe disqualify at $\ge +12\text{kg}$ in $\ge 1800\text{m}$ or $\ge +14\text{kg}$**); **Type III** (unscheduled $\le -10\text{kg}$, especially $< 435\text{kg}$: $[-0.06,-0.15], \sigma_i^2 \uparrow$).

### Step 3: Positional Micro-Simulation, 3-Race Intraday Bias Guard, 2-Stage Benter Fusion (`Patch S5/S6/S7`) & Exact Plackett-Luce

1.  **Positional Micro-Simulation & Strict 3-Race Intraday Bias Assimilation**:
      - Simulate `スタート → 1角 → 3-4角 → 直線進路` across **3 to 4 MECE scenarios** ($\sum_s \pi_s = 1.00$). Shift $\pi_s^{\text{post}}$ by $+10\%\sim +20\%$ **ONLY when $\ge 3$ earlier same-surface, pace-matched races consistently confirm the bias** (or `+8% to +12%` win-side on 3 consecutive same-zone winners); otherwise cap at $\le \pm 5\%$.
2.  **2-Stage Benter Bayesian Fusion & Calibration Guardrails (`Patch S5 / S6 / S7`)**:
      - **Stage 1 (Odds-Blind Fundamental `fFund`)**: Compute pure odds-blind fundamental win probabilities `fFund` on a **strict `0.0–100.0` percentage scale** ($\sum f^{\text{fund}} = 100.0\%$) via variance-attenuated logits $\tilde{\theta}^{\text{fund}}_{i,s} = \theta^{\text{fund}}_{i,s} / \sqrt{1 + 0.304\sigma_i^2}$. (Note: The v12.0 pipeline also re-verifies Stage 2 fusion mathematically from your `fFund` and live odds `q`, so supply clean, well-separated `fFund` values.)
      - **Stage 2 (Adaptive Market Fusion)**: Pool `fFund` with FLB Power de-vigged $q_i = (1/O_i)^\gamma / \sum_k (1/O_k)^\gamma$ ($\gamma \approx 1.08$) using baseline market weight $w_r \in [0.45, 0.55]$: $$\theta^{\text{post}}_{i,s} = (1 - w_{r,i})\,\tilde{\theta}^{\text{fund}}_{i,s} + w_{r,i} \ln q_i, \qquad \theta^{\text{post},(2,3)}_{i,s} = \theta^{\text{post}}_{i,s} + \delta^{\text{place}}_i$$
      - **Top-2 Market Favorite Protection (`Patch S5`)**: For any runner trading at **$O_i \le 4.5\text{x}$** without a severe `F`-level weight disqualification (`+12kg+` in $\ge 1800\text{m}$ or `+14kg+`), **maintain $w_{r,i} \ge 0.42$, strictly prohibit `消` or `危`, and keep it inside Core connections**. NEVER elevate a $> 4.5\text{x}$ mid-longshot to `◎` above clean $\le 4.5\text{x}$ favorites without indisputable `F`-level flaws on every favorite.
      - **Mid- & Extreme-Longshot Calibration Caps (`Patch S6`)**:
          - **`O_i >= 8.0x`**: Cap Fused Posterior win probability at **`f <= min(18.0%, q_i + 10.0%)`** so uncalibrated longshot optimism never distorts rankings or triggers adverse selection.
          - **`O_i >= 50.0x`**: Cap Fused Posterior win probability at **`f <= 5.5%`** and restrict mark to `△ / ☆ / 無` (strictly barred from `◎ / ◯ / ▲`).
      - **Strict Percentage Format (`Patch S7`)**: Output ALL probability fields (`f`, `fFund`, `q`, `top2`, `top3`, `m3`, `hitRate`, `breakEvenRate`) strictly in **`0.0` to `100.0` percentage units** (e.g., `23.5`, NEVER `0.235`). Verify conservation strictly: $\sum f = 100.0\%, \sum \text{top2} = 200.0\%, \sum \text{top3} = 300.0\%$.

### Step 4: v12.0 Balanced ROI Portfolio Rules (`Core 62% / Alpha 38%`), `◎` Anchor Discipline & Auto-Pass Gate

  - **Anchor Discipline (`◎ 1.4–4.0x` Band — `Patch S5`)**:
      - Select **`◎`** as the highest Posterior composite (`0.55*f + 0.45*top3`) anchor passing safety checks.
      - **Mandatory Adverse-Selection Pass**: If `◎`'s live odds fall **outside `1.4x–4.0x`** (especially `> 4.0x` wide-open mid-longshot chaos), declare **`rank: "Pass"` and `pivotType: "Pass"`**.
  - **Core 62% / Alpha 38% Structure (Synced 100% with `auto_predict.py` v12.0)**:
      - **Core Shield (`62%` = `6,200 JPY` / `10,000 JPY`)**: Adaptive Wide Dutching with mandatory `◎-☆` & Top-2 market-favorite (`O <= 5.0`) connection:
          - $O_{\text{◎}} \le 1.8\text{x}$: Compress strictly to **2 Wide lines** (`◎` × top 2 value partners).
          - $1.8\text{x} < O_{\text{◎}} \le 2.2\text{x}$: **3 Wide lines** (`◎-◯`, `◎-▲`, `◎-☆/人気`).
          - $O_{\text{◎}} > 2.2\text{x}$: **4 Wide lines** (`◎-◯`, `◎-▲`, `◯-▲`, `◎-☆/人気`).
      - **Alpha Booster (`38%` = `3,800 JPY`)**:
          - **`◎` Win Priority Protection (`約1,400 JPY`)**: ALWAYS protect `◎` to win (`単勝 ◎`) when $O_{\text{◎}} \ge 2.0\text{x}$ so `◎` 1st-place finishes never suffer 0-yen leaks; when $O_{\text{◎}} < 2.0\text{x}$ and $O_{\text{◯}} \ge 2.8\text{x}$, split Win across `◎` (~58% / 45%) and `◯` (~42% / 55%).
          - **Quinella 2 lines (`約1,600 JPY`)**: `馬連 ◎-◯` and `馬連 ◎-▲` (or forced market favorite).
          - **Compact Trio (`約800 JPY`)**: Verify exact formation counts ($3M+1$ / $5M+4$).
      - **Single-Longshot Cap**: Total combined stake on any single longshot ($O_i \ge 10.0$) $\le 30\%$ (`3,000 JPY`).
  - **Auto-Pass Gate & Rank Criteria (Zero Adverse Selection)**:
      - Declare **`rank: "Pass"`** immediately if: (1) obstacle race, (2) live odds missing, (3) `◎` odds outside `1.4x–4.0x`, (4) `coreSyntheticOdds < 1.10x` OR `avgCoreWide < 3.0x`, (5) `m3 < 38.0%`, OR (6) `<= 8` active runners with compressed odds (`avgCoreWide < 3.0x` or Top-2 favs `<= 2.5x`).
      - **`rank: "S"`**: `1.5 <= O_◎ <= 4.0`, (`avgCoreWide >= 3.8` or `coreSyntheticOdds >= 1.24`), and `m3 >= 44.0%`.
      - **`rank: "A"`**: Passes all Pass gates but below `S` thresholds.
  - **Counterfactual Self-Audit**: Internally verify (a) `◎` failure mode & `◯-▲` coverage, (b) Top-2 market fav protection, and (c) strict percentage scaling (`0.0–100.0`) + conservation + `O>=8x`/`O>=50x` caps before emitting JSON.

### Step 5: App-Optimized Backward-Compatible JSON Schemas

All existing keys are preserved verbatim for zero-breakage PWA compatibility; output **ONLY a single valid JSON object** in app pipeline mode.

#### Mode A: `スクリーニング` (Morning Venue Batch Screening JSON)

```json
{
  "date": "YYYY-MM-DD",
  "venue": "東京",
  "strategyProfile": "v12_balanced_roi",
  "trackBias": {
    "turfCv": 9.6,
    "turfMoisture": "11.2%",
    "dirtMoisture": "4.5%",
    "intradayBias3R": false,
    "summary": "Cコース2日目・芝標準良・ダやや湿"
  },
  "races": [
    {
      "raceNumber": 11,
      "name": "キャピタルS(L)",
      "surfaceDist": "芝1600m",
      "postTime": "15:25",
      "rank": "S | A | Pass",
      "skill": "app-bayesian-horse-racing-text",
      "pivotType": "Single-Pivot | Dual-Pivot | Pass",
      "nLead": 4,
      "m3": 52.4,
      "coreSyntheticOdds": 1.34,
      "avgCoreWide": 4.2,
      "expectedRoi": 111.5,
      "hitRate": 58.2,
      "breakEvenRate": 51.0,
      "summary": "35字以内の◎オッズ・平均W・M3判定根拠"
    }
  ]
}
```

#### Mode B: `標準` (1-Hour-Before Single-Race Prediction JSON)

Evaluate **all $N$ active declared runners internally** (excluding scratches). Output **all $N$ runners** when requested by the pipeline prompt (or marked contenders + notable favorites with `tailSummary`), strictly using **`0.0–100.0` percentage values** so $\sum f = 100.0\%$ and $\sum \text{top3} = 300.0\%$:

```json
{
  "raceId": "20261129-tok-12",
  "venue": "東京12R",
  "name": "ジャパンC(G1)",
  "surfaceDist": "芝2400m",
  "postTime": "15:40",
  "skill": "app-bayesian-horse-racing-text",
  "strategyProfile": "v12_balanced_roi",
  "rank": "S | A | Pass",
  "pivotType": "Single-Pivot | Dual-Pivot | Pass",
  "nLead": 3,
  "rpci": 51.2,
  "wR": 0.50,
  "m3": 54.6,
  "coreSyntheticOdds": 1.32,
  "avgCoreWide": 4.1,
  "intradayBias3R": true,
  "expectedRoi": 112.5,
  "hitRate": 59.4,
  "breakEvenRate": 52.0,
  "scenario": "当日3R一致バイアス・展開・3〜4MECEシナリオ重み要約(80字以内)",
  "horses": [
    {
      "mark": "◎ | ◯ | ▲ | ☆ | △ | 消",
      "role": "最安定Top-3軸 | 融合上位強制結線 | 安定Connector | 展開特注穴 | 危険人気馬",
      "num": 5,
      "name": "馬名",
      "style": "逃 | 先 | 差 | 追",
      "f": 26.4,
      "fFund": 24.8,
      "q": 28.0,
      "wUsed": 0.50,
      "top2": 46.2,
      "top3": 62.8,
      "odds": 2.9,
      "tags": ["F:東京芝2400好績", "H:2段階融合軸+0.14"],
      "comment": "45字以内のF/H核心根拠"
    }
  ],
  "tailSummary": { "count": 8, "sumF": 9.8, "sumTop3": 28.4 },
  "coreConnections": [[5, 6], [5, 1], [6, 1], [5, 14]],
  "portfolioRules": {
    "coreRatio": 0.62,
    "alphaRatio": 0.38,
    "coreLineCap": 4,
    "singleLongshotCapPct": 0.30
  },
  "alerts": ["馬体重Type II(+12kg超)自動減点、またはLevel B自動差替ルール(50字以内)"],
  "counterfactualAudit": "◎破綻時の◯-▲防衛状態と上位人気馬保護状態(60字以内)",
  "triggers": ["直前馬体重(Type I-III)・実オッズ確認トリガー(40字以内)"]
}
```

#### Mode C: `事後検証` (Weekend Batch Post-Race Audit & Skill Patch JSON)

Output a JSON object containing `auditSummary`, 3-factor decomposition (`scenarioError`, `ratingError` including Top-2 fav protection, `O>=8x`/`O>=50x` cap & percentage-scale check, and `portfolioError` including `◎` 1.4–4.0x band, `◎` Win protection, `◎-☆` connection, and Core 62%/Alpha 38% audit), and `skillPatch` (`targetSkill`, `targetVersion`, `moduleName`, `patchRule`).

## Gotchas

  - **NEVER output probabilities as `0.0–1.0` decimals** (e.g., `0.232`); ALWAYS output **`0.0–100.0` percentages** (e.g., `23.2`) so $\sum f = 100.0$.
  - **NEVER hard-fade (`消/危`) or omit from Core connections a Top-2 market favorite ($O_i \le 4.5$)** unless it has a verifiable severe `F`-level weight disqualification (`+12kg+` in $\ge 1800\text{m}$ or `+14kg+`); always keep $w_{r,i} \ge 0.42$.
  - **NEVER let a mid-longshot ($O_i \ge 8.0\text{x}$) exceed `f = min(18.0%, q + 10.0%)`**, and **NEVER promote an extreme longshot ($O_i \ge 50.0\text{x}$) above `f = 5.5%` or into `◎ / ◯ / ▲`**.
  - **NEVER bet races where `◎` is outside `1.4x–4.0x`**, obstacle races (`障害戦`), or compressed races (`coreSyntheticOdds < 1.10x`, `avgCoreWide < 3.0x`, `m3 < 38%`, or `<= 8` runners low-yield); declare `rank: "Pass"`.
  - Never include scratched/withdrawn (`取消・除外`) runners, never apply the returning-Japanese-horse overseas fatigue cap to elite visiting foreign G1 contenders, and always output valid, parseable JSON without conversational filler in app pipeline mode.
