---
name: app-bayesian-win5
description: App-dedicated copy of bayesian-win5 (v11.3 Neon Maximum Hit-Rate Edition) for the JRA Racing AI PWA and 1-hour-before pipeline. Executes strict 0.0-100.0 percentage output (no 0.232 decimals), 2-Stage Benter Bayesian Fusion (Odds-Blind 10-module fFund pooled with FLB de-vigged q via adaptive w_r; 0.50-0.60 for visiting foreign G1 legs, Top-2 fav O<=4.5 protection, O>=8x min(18%, q+10pt) cap & O>=50x <=5.5% cap), Plan C Probability-Shell Orthogonal Decomposition (3-4 disjoint IPAT tickets with T1 Core <=45% hard cap, >=3-leg wing coverage, and priority wing allocation for 5.0-15.0x mid-price Rank #4-#6 contenders with inner-pocket Frames 1-3 or Top-3 closing 3F), 3-race-consistent 1R-8R intraday Bayesian bias guard, dry-dirt mandatory Top-4 closer slot & wet-sprint/Top-2-fav dirt inner-gate soft cap, visiting elite foreign G1 vs returning Japanese horse split, confrontation graph, positional micro-simulation, rule-stacking clamp, counterfactual self-audit, difficulty grading, and outputs backward-compatible compact JSON (f/fFund/q/shell/logDeficit/scenarios/planC/legs/hedgeCandidates) synced with v12.0-neon.
---

# App Bayesian WIN5 (v11.3 — Neon v12.0 Maximum Hit-Rate App JSON Edition)

Autonomous multi-race hierarchical Bayesian probability modeling and combinatorial optimization system specialized for **JRA WIN5** (Saturday/Sunday/Holiday all official WIN5 dates) in the **JRA Racing AI App (PWA)** and automated 1-hour-before WIN5 execution pipeline (`gemini-4-neon HIGH`). Combines **strict `0.0–100.0` percentage scaling (Patch S7)**, **2-Stage Benter Bayesian Fusion with Top-2 market favorite protection (`O <= 4.5` — Patch S5) and mid/extreme-longshot caps (`O >= 8.0x`: `min(18.0%, q + 10.0%)`; `O >= 50.0x`: `<= 5.5%` — Patch S6)**, **Plan C Probability-Shell Multi-Ticket Orthogonal Decomposition (T1 Core $\le 45\%$ Hard Cap, $\ge 3$-Leg Wing Coverage, & Mid-Price 5.0–15.0x Rank `#4–#6` Priority Wing Allocation)**, **Venue-Coupled Bias Synchronization**, **Live 1R–8R Intraday Bayesian Assimilation with 3-Race Minimum Consistency Guard**, and all **10 True-Winner Identification Modules**, outputting compact, backward-compatible structured JSON synced directly with single-race predictions in `auto_predict.py` v12.0.

## When to Use

  - Executing automated or manual **WIN5 predictions for the Racing AI App** across any official JRA WIN5 date (Sunday, Saturday, or Holiday 3-day cards).
  - Generating structured WIN5 JSON (`legs`, `f`, `fFund`, `q`, `shell`, `logDeficit`, `scenarios`, `planC`, `hedgeCandidates`) strictly in **`0.0–100.0` percentage units** so the PWA can display 3–4 disjoint IPAT-ready Plan C tickets and dynamically recalculate optimal Plan A/C formations across any budget (`5,000–50,000 JPY`).
  - Running a **Pre-Race Intraday Bayesian Diff Update (`直前更新`)** or **Post-Race WIN5 Audit & Skill Patch Generation (`事後検証・スキル改訂パッチ生成`)**.

## Core Hit-Rate Maximization Engines (v11.3)

1.  **2-Stage Benter Bayesian Fusion & Strict Calibration Guardrails (`Patch S5 / S6 / S7`)**:
      - **Stage 1 (Odds-Blind Fundamental `fFund`)**: Compute pure fundamental win probabilities $f^{\text{fund}}_{r,i,s}$ independently of odds using all 10 Modules, Transitive Confrontation Graph, Positional Micro-Simulation, and Soft-Clamp Regularization.
      - **Stage 2 (Adaptive Posterior Pooling)**: Pool $f^{\text{fund}}_{r,i,s}$ with FLB Power de-vigged live market probabilities $q_{r,i} = (1/O_{r,i})^{\gamma} / \sum_k (1/O_{r,k})^{\gamma}$ ($\gamma \approx 1.08$) in log-odds space (note: `auto_predict.py` v12.0 also re-verifies Stage 2 fusion mathematically so WIN5 Legs and single-race cards remain 100% consistent): $$p^{\text{post}}_{r,i,s} \propto \left(f^{\text{fund}}_{r,i,s}\right)^{1 - w_r} \cdot \left(q_{r,i}\right)^{w_r}, \quad p_{r,i} = \sum_{s=1}^S \pi_s p^{\text{post}}_{r,i,s}$$
      - **Adaptive Market Weight $w_r$**: Default **`0.45–0.55`** (`0.55–0.60` for **visiting foreign G1 contender legs `外国馬参戦G1`**, juvenile stakes $n_i \le 2$, or layoff-heavy fields; `0.35–0.45` only on clear `F`-level trap legs).
      - **Top-2 Market Favorite Protection (`Patch S5`)**: Never drop a runner with **$O_{r,i} \le 4.5\text{x}$** (or $q_{r,i} \ge 15\%$) or a well-backed visiting G1 winner ($O_{r,i} \le 10.0$) out of all active shells without an explicit, verifiable `F`-level physical hazard (e.g., `+12kg+` in $\ge 1800\text{m}$ or `+14kg+`).
      - **Mid- & Extreme-Longshot Caps (`Patch S6`)**: Cap **`O_{r,i} >= 8.0x`** at **`f <= min(18.0%, q_{r,i} + 10.0%)`**, and cap **`O_{r,i} >= 50.0x`** at **`f <= 5.5%`** (prohibited from Core `C`).
      - **Strict `0.0–100.0` Percentage Format (`Patch S7`)**: ALWAYS output `f`, `fFund`, and `q` as **percentages between `0.0` and `100.0`** (e.g., `23.5`, NEVER `0.235`). Verify $\sum_{i=1}^{N_r} f_{r,i} = 100.0$ in every leg.

2.  **Plan C: L1 Log-Loss Probability-Shell Orthogonal Decomposition & Mid-Price Wing Priority (`T1核上限45%・3レグ以上直交翼・4〜6番手中穴優先編入則`)**:
      - Decompose the Top-$K$ minimum log-loss simplex ($\min \sum d_{r,i_r}$) into **3 to 4 strictly disjoint IPAT-ready tickets ($T_a \cap T_b = \emptyset$)**:
          - `T1` (`最密核 Core` — **HARD CAP $\le 45\%$ of budget, i.e., $\le 48$ points at 10,000 yen; target 32–48 pts**): $C_1 \times C_2 \times C_3 \times C_4 \times C_5$.
          - `T2`–`T4` (`直交翼 / バイアス連動翼 Orthogonal Wings`, **55–70% of budget across $\ge 3$ distinct legs**): Expand at least 3 distinct legs (including `Type A` `#3` when $p_{r,3} \ge 9.0\%$ and `Type B/B+` `#4–#6`) into disjoint Wing sets $W_a$ ($W_a \cap C_a = \emptyset$) while tightening the other 4 legs to Core Top 1–2 ($C'_r \subseteq C_r$).
          - **Mid-Price Rank `#4–#6` Priority Wing Allocation (`4〜6番手・単勝5〜15倍帯中穴の直交翼優先編入則`)**: Prioritize `#4–#6` contenders trading in the **`5.0x–15.0x`** band that hold either (a) an inside pocket draw (Frames 1–3) with rail-saving/tactical speed, OR (b) Top-3 Last-3F closing speed (`上がり3F上位`).
      - Exact disjoint coupled hit rate: $P_{\text{Plan C}} = \sum_{m=1}^M \sum_{s=1}^S \pi_s \prod_{r=1}^5 F_{r,s}(T_m)$, benchmarked directly against `Plan A`.

3.  **Venue-Coupled Bias Synchronization & Live 1R–8R Bayesian Assimilation with 3-Race Minimum Consistency Guard**:
      - Link legs at the same venue via **3 to 4 MECE shared scenarios** ($\sum_s \pi_s = 1.00$). Until **at least 3 same-venue, same-surface races** confirm a consistent directional bias, cap any scenario weight shift at $|\Delta \pi_s| \le 0.05$ ($\pm 5\text{pt}$).

4.  **Difficulty-Adaptive Budget Efficiency Grading**:
      - Classify each WIN5 card into `高確度攻め週`, `標準週`, `超難解カオス週`, or `キャリーオーバー拡張週`.

## Phase 0: Hybrid Data Ingestion & Web Auto-Fetch

  - Treat supplied racecards/odds/track data from `auto_predict.py` as primary ground truth and exclude scratched/withdrawn (`取消・除外`) runners before normalization. Never fabricate missing data.

## Steps

### Step 1: Odds-Blind Evidence Classification (F / E / H), Confrontation Graph & Regularization

  - Estimate Stage 1 log-ability ($\theta^{(1)}_{r,i,s} \in \mathbb{R}$, baseline $0.00$) independently of odds using `F / E / H` taxonomy, Transitive Confrontation Graph, and Soft-Clamp Regularization ($|\sum \Delta \theta^{(1)}_{r,i}| \le 0.45$).

### Step 2: Ten Complete True-Winner Identification Modules (`本当に勝つ馬を見抜く10大完全検算モジュール`)

Evaluate every active runner internally across all 5 legs:

1.  **Pace-Dynamic 4th-Corner Zone, High-Pace Dirt Dual-Closer vs. Turf-Start Dry-Dirt Mandatory Top-4 Closer Slot & High-CV Sprint Outer-Speed Persistence**:
      - $N_{\text{lead}} \le 3$: Boost tactical stalkers/leaders within $\le 0.6\text{s}$ at 4C.
      - $N_{\text{lead}} \ge 4$: Trigger $\pi_{\text{collapse}} \ge 0.35$; elevate `#1` proven mid-pack/outer closer into Top 3–4.
      - Turf-start dry-dirt ($\text{Moisture} \le 5.0\%$): Retain inside-pocket stalker (Frames 2–4) + outer turf-dash stalker (Frames 7–8) **AND mandatorily reserve at least 1 slot in Top 4 for the `#1` proven pure closer** when $N_{\text{lead}} \ge 4$.
      - High-CV ($\ge 9.6$) Turf 1200m Sprint: Boost Frames 6–8 top opening-3F sprinters (`+0.12 to +0.18`).
2.  **Two-Step Trouble Audit, Turf-Start Dirt Outer-Stalker Promotion & Dirt Inner-Gate Soft Cap**:
      - Audit 4th–12th favorites for `F`-level trouble/pace survival.
      - On Good/Dry turf-start dirt: strip `Type S` from Frames 1–4 favorites lacking kickback proof, **but cap inner penalty at `-0.08 to -0.12` (never stripping them from all shells) when they are Top-2 market favorites ($O_{r,i} \le 4.5$) or 3yo/4yo winning-streak risers**, and **waive inner penalty on wet/sloppy $\le 1200\text{m}$**. Promote `#1` Frame 7–8 stalker into Top 3.
3.  **Class-Boundary, 3yo/4yo Class-Standard Breaker & Autumn 3yo Light-Weight / Inner-Frame Ascending Priority**:
      - Penalize slow unpressured older front-running promotions (`-0.12`); boost 3yo/4yo class-standard & final-2F breakers (`+0.16 to +0.22`) and autumn 3yo $53\text{–}55\text{kg}$ / Frames 1–2 streak winners (`+0.16 to +0.22`); halve fast-track bonuses on Subarctic/Low-CV turf.
4.  **1st-Place Conversion Efficiency, Chronic Silver-Collector Ceiling & 58kg+ Layoff/Medical-Return / Prep Favorite Fade**:
      - Silver-Collector ceiling (`-0.15 to -0.22`, no `Type S`); 58kg+ medical/long-layoff fade (`-0.15 to -0.20`, no solo 2-horse lock); G2/G3 prep favorite fade (`-0.12 to -0.18`) + lone-speed promotion.
5.  **Jensen's Inequality Variance Correction & Visiting Elite Foreign G1 vs. Returning Japanese Horse Split**:
      - Returning Japanese horse off overseas defeat ($\ge 5\text{th}$ / $\ge 1.0\text{s}$): $\sigma_{\text{overseas}}^2 \ge 0.25$, `-0.12 to -0.20`, no `Type S`.
      - **Visiting Elite Foreign G1 Winner**: Strictly separate; with sharp local turf workouts (`1F <= 11.5s`), favorable draw (Frames 1–5), and market support ($O_i \le 10.0$), keep $\sigma_{\text{visit}}^2 \le 0.08$, set $w_r = 0.55\text{–}0.60$, and keep eligible for Core `C` or primary Wing `W`.
      - Untested marathon ($\ge 2400\text{m}/\ge 3000\text{m}$), 3yo older dirt G1 debut, and $n_i \le 2$ juvenile stakes caps (`p_1 <= 30–35%`, no `Type S`).
6.  **Handicap Physics, Tight-Oval Light-Weight Boost & Fillies/Mares Inside-Pocket Dynamics**:
      - Tight-oval $50\text{–}53\text{kg}$ speed (`+0.16 to +0.22`); Fillies/Mares Frames 1–4 with 1F $\le 11.3\text{s}$ (`+0.15`) vs. Frames 7–8 wide closers (`-0.12`).
7.  **Special-Course Repeater Priority & Off-Condition / Wet-Track Close-Defeat Reset**:
      - Reset $\le 0.2\text{s}$ current-class contenders losing last 1–3 starts due to wet/draw/distance mismatch (`+0.14 to +0.20`).
8.  **Jockey Tactical Match & Gate Departure Reliability**:
      - $\ge 30\%$ slow-start rate in last 5 starts -> barred from `Type S`.
9.  **Workout Lap Physics, Prep Bounce-Back & G1 S-Workout / 3yo Classic $\le 0.2\text{s}$ Outer-Draw Exemption**:
      - Waive/halve outer-draw penalty (cap $\ge -0.05$) and grant `+0.14 to +0.20` for proven G1 winners with S-grade workouts or autumn 3yos within $\le 0.2\text{s}$ of a Classic G1.
10. **Intraday Cushion Value, Moisture/Wind Shift & Early-Leg `Type B+` Detection**:
      - Penalize front-runners under afternoon rain or headwind $\ge 5\text{m/s}$; enforce 3-Race Minimum Consistency Guard.

### Step 3: Exact Venue-Coupled Tensor, Counterfactual Audit & Plan C Verification

Internally compute full-field Stage 1 `fFund`, Stage 2 calibrated posterior `f` (**strictly `0.0–100.0` percentages**, $\sum_{i=1}^{N_r} f_{r,i} = 100.0$), and exact Plan C disjoint tickets (`T1`–`T4`):

  - **T1 Core Hard Cap**: `T1.points <= 48` (at 10,000 JPY; $\le 45\%$) AND `T2`–`T4` expand **$\ge 3$ distinct legs** prioritizing `5.0x–15.0x` Rank `#4–#6` contenders with inside pockets or Top-3 Last-3F.
  - Verify pairwise disjointness $T_a \cap T_b = \emptyset$, Top-2 market favorite protection ($O \le 4.5$), `O>=8x`/`O>=50x` caps, and **strict `0.0–100.0` percentage output** before emitting JSON.

### Step 4: App-Optimized Output Format (Backward-Compatible Strict JSON Schema)

Output **ONLY a single valid JSON object** matching the schema below in pipeline mode. Keep `note` under 35 characters. **CRITICAL: `f`, `fFund`, and `q` MUST be percentages `0.0–100.0` (e.g., `28.4`, NEVER `0.284`).**

```json
{
  "date": "YYYY-MM-DD",
  "skill": "app-bayesian-win5",
  "version": "11.3",
  "difficultyGrade": "高確度攻め週 | 標準週 | 超難解カオス週 | キャリーオーバー拡張週",
  "budgetGuidance": "通常10,000円（カオス防衛時は3,000〜5,000円）",
  "recommendedPlan": "Plan C | Plan A | Plan B-1 | Plan B-2",
  "intradayBiasGuard": "3戦未満(±5pt制限中) | 3戦以上確認済",
  "summary": "全体戦略・会場連動バイアス・中穴翼配置要約(80字以内)",
  "scenarios": [
    { "id": "s1", "label": "標準高速・外差し均衡", "pi": 0.50 },
    { "id": "s2", "label": "内荒れ・前崩れ外差し", "pi": 0.30 },
    { "id": "s3", "label": "両場高速イン前残り", "pi": 0.20 }
  ],
  "planC": {
    "budget": 10000,
    "totalPoints": 100,
    "t1CoreRatio": 0.36,
    "wingLegCount": 3,
    "coupledHitRate": 5.42,
    "planAHitRate": 4.47,
    "tickets": [
      {
        "id": "T1",
        "role": "最密核(≤45%)",
        "legs": [[11], [5, 6], [9, 1, 5], [5, 6], [14, 5, 8]],
        "points": 36,
        "hitRate": 2.34,
        "scenarioSync": "全シナリオ共通"
      },
      {
        "id": "T2",
        "role": "第1翼(Leg1中穴5-15倍拡張)",
        "legs": [[2, 12, 14], [5, 6], [9, 1], [5, 6], [14, 5]],
        "points": 24,
        "hitRate": 1.38,
        "scenarioSync": "s1/s2中穴上り"
      },
      {
        "id": "T3",
        "role": "第2翼(Leg3純差し+内枠)",
        "legs": [[11], [5, 6], [8, 12, 4], [5, 6], [14, 5]],
        "points": 24,
        "hitRate": 1.05,
        "scenarioSync": "s2前崩れ同期"
      },
      {
        "id": "T4",
        "role": "第3翼(Leg2#3・Leg5内ポケット中穴)",
        "legs": [[11], [14], [9, 1], [5, 6], [14, 5, 2, 1]],
        "points": 16,
        "hitRate": 0.65,
        "scenarioSync": "Type A翼+内ポケット"
      }
    ]
  },
  "legs": [
    {
      "leg": 1,
      "venue": "京都9R",
      "name": "レース名",
      "surfaceDist": "芝1600m外C",
      "postTime": "14:25",
      "nLead": 3,
      "legType": "Type S | Type A | Type B | Type B+",
      "typeBPlus": false,
      "wR": 0.50,
      "paceNote": "展開・バイアス短評(40字以内)",
      "counterfactualRisk": "最大破綻経路・直前入替トリガー(40字以内)",
      "horses": [
        {
          "num": 11,
          "name": "馬名",
          "f": 28.4,
          "fFund": 29.5,
          "q": 26.2,
          "odds": 2.7,
          "style": "先差",
          "shell": "C",
          "logDeficit": 0.00,
          "tags": ["F:重賞3着", "H:前走外回しリセット"],
          "note": "35字以内の核心根拠"
        }
      ],
      "hedgeCandidates": [
        { "num": 12, "name": "馬名", "odds": 12.0, "hedge50k": 4200, "hedge100k": 8400 }
      ]
    }
  ]
}
```

## Gotchas

  - **NEVER output `f`, `fFund`, or `q` as `0.0–1.0` decimals** (e.g., `0.232`); ALWAYS output **`0.0–100.0` percentages** (e.g., `23.2`) so $\sum f = 100.0$ per leg.
  - **NEVER drop a Top-2 market favorite ($O_{r,i} \le 4.5$ or $q_{r,i} \ge 15\%$) or well-backed visiting G1 winner ($O_{r,i} \le 10.0$) from all shells** without a verifiable `F`-level physical hazard (`+12kg+` in $\ge 1800\text{m}$ / `+14kg+`).
  - **NEVER let an $O_{r,i} \ge 8.0\text{x}$ runner exceed `f = min(18.0%, q_{r,i} + 10.0%)`**, and **NEVER let an $O_{r,i} \ge 50.0\text{x}$ extreme longshot exceed `f = 5.5%` or enter Core `C`**.
  - Always sort `horses` strictly by `f` descending, exclude scratched/withdrawn runners, enforce `T1 <= 45%` ($\le 48$ pts at 10k) and $\ge 3$-leg disjoint wings prioritizing `5.0x–15.0x` Rank `#4–#6` contenders, and enforce the 3-Race Minimum Consistency Guard on intraday 1R–8R bias.
  - Always output valid, parseable JSON without conversational filler in app pipeline mode.
