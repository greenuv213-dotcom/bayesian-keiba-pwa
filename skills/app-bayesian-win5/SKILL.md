---
name: app-bayesian-win5
description: App-dedicated copy of bayesian-win5 (v11.1 Neon Maximum Hit-Rate Edition) for the JRA Racing AI PWA and 1-hour-before pipeline. Executes 2-Stage Benter Bayesian Fusion (Odds-Blind 10-module fFund pooled with FLB de-vigged q via adaptive w_r; 0.55-0.60 for visiting foreign G1 legs), Plan C Probability-Shell Orthogonal Decomposition (3-4 disjoint IPAT tickets with T1 Core <=45% hard cap & >=3-leg wing coverage), 3-race-consistent 1R-8R intraday Bayesian bias guard, dry-dirt mandatory Top-4 closer slot, visiting elite foreign G1 vs returning Japanese horse split, confrontation graph, positional micro-simulation, rule-stacking clamp, counterfactual self-audit, difficulty grading, and outputs backward-compatible compact JSON (f/fFund/q/shell/logDeficit/scenarios/planC/legs/hedgeCandidates) for client-side dynamic budget simulation and post-race skill patch generation.
---
# App Bayesian WIN5 (v11.1 — Neon Maximum Hit-Rate App JSON Edition)

Autonomous multi-race hierarchical Bayesian probability modeling and combinatorial optimization system specialized for the **JRA Racing AI App (PWA)** and automated 1-hour-before WIN5 execution pipeline. This is the app-dedicated JSON edition of `bayesian-win5` (v11.1), combining **2-Stage Benter Bayesian Fusion**, **Plan C Probability-Shell Multi-Ticket Orthogonal Decomposition (T1 Core $\le 45\%$ Hard Cap & $\ge 3$-Leg Wing Coverage)**, **Venue-Coupled Bias Synchronization**, **Live 1R–8R Intraday Bayesian Assimilation with 3-Race Minimum Consistency Guard**, and all **10 True-Winner Identification Modules**, while outputting compact, backward-compatible structured JSON consumed directly by the PWA's client-side dynamic budget simulator (5,000 to 50,000 yen) with zero extra API calls.

## When to Use

- Executing automated or manual **WIN5 predictions for the Racing AI App** (1 hour before Leg 1 post time via GitHub Actions or on-demand).
- Generating structured WIN5 JSON (`legs`, `f`, `fFund`, `q`, `shell`, `logDeficit`, `scenarios`, `planC`, `hedgeCandidates`) so the PWA can display 3–4 disjoint IPAT-ready Plan C tickets and dynamically recalculate optimal Plan A/B/C formations across any budget in browser JavaScript.
- Running a **Pre-Race Intraday Bayesian Diff Update (`直前更新`)** assimilating live 1R–8R track bias (with 3-Race Minimum Consistency Guard), horse weights, and smart-money moves, or **Post-Race WIN5 Audit & Skill Patch Generation (`事後検証・スキル改訂パッチ生成`)** for the app.

## Core Hit-Rate Maximization Engines (v11.1)

1. **2-Stage Benter Bayesian Fusion (`2段階分離ベイズ融合`)**:
   - **Stage 1 (Odds-Blind Fundamental)**: Compute pure fundamental win probabilities $f^{\text{fund}}_{r,i,s}$ **completely independently of odds/popularity (`オッズ完全遮断`)** using all 10 Modules, Transitive Confrontation Graph, Positional Micro-Simulation, and Soft-Clamp Regularization.
   - **Stage 2 (Adaptive Posterior Pooling)**: Pool $f^{\text{fund}}_{r,i,s}$ with FLB Power de-vigged live market probabilities $q_{r,i} = (1/O_{r,i})^{\gamma} / \sum_k (1/O_{r,k})^{\gamma}$ ($\gamma \in [1.05, 1.15]$) in log-odds space:
     $$p^{\text{post}}_{r,i,s} \propto \left(f^{\text{fund}}_{r,i,s}\right)^{w_r} \cdot \left(q_{r,i}\right)^{1 - w_r}, \quad p_{r,i} = \sum_{s=1}^S \pi_s p^{\text{post}}_{r,i,s}$$
   - **Adaptive Weight $w_r$**: Default `0.70`; clear `F`-level trap/hazard leg (Mod 2 turf-start inner kickback, Mod 4 58kg+ medical/layoff favorite, Mod 9 S-workout outer exemption) -> `0.80`; low-information leg (**visiting foreign G1 contender races `外国馬参戦G1`**, juvenile stakes $n_i \le 2$, layoff-heavy field, or live $\ge 25\text{–}30\%$ smart-money surge) -> **`0.55–0.60`** so market international/paddock signals are heavily absorbed.
   - **Market-Divergence Re-Audit Guard**: Never exclude any runner with $q_{r,i} \ge 15\%$ or well-backed visiting G1 winner ($O_{r,i} \le 10.0$) from all active shells without an explicit `F`-level physical hazard.
   - **Backward-Compatible JSON Mapping**: Store the final calibrated posterior $p_{r,i}$ in the primary `f` field (so existing PWA JS sorts and simulates using the optimal posterior automatically) and store Stage 1 $f^{\text{fund}}_{r,i}$ in `fFund`.

2. **Plan C: L1 Log-Loss Probability-Shell Orthogonal Decomposition (`T1核上限45%ハードキャップ＆3レグ以上直交翼展開`)**:
   - Define each runner's Log-Probability Deficit $d_{r,i} = \ln(p_{r,(1)} / p_{r,i}) \ge 0$ (`logDeficit`).
   - Decompose the Top-$K$ minimum log-loss simplex ($\min \sum d_{r,i_r}$) into **3 to 4 strictly disjoint IPAT-ready tickets ($T_a \cap T_b = \emptyset$)**:
     - `T1` (`最密核 Core` — **HARD CAP $\le 45\%$ of budget, i.e., $\le 48$ points at 10,000 yen; target 32–48 pts**): $C_1 \times C_2 \times C_3 \times C_4 \times C_5$. Never bloat `T1` above 48 points at 10k.
     - `T2`–`T4` (`直交翼 / バイアス連動翼 Orthogonal Wings`, **55–70% of budget across $\ge 3$ distinct legs**): Expand at least 3 distinct legs (including `Type A` `#3` when $p_{r,3} \ge 9.0\%$ and `Type B/B+` `#4–#6`) into disjoint Wing sets $W_a$ ($W_a \cap C_a = \emptyset$) while tightening the other 4 legs to Core Top 1–2 ($C'_r \subseteq C_r$), enforcing strict hierarchical disjointness.
   - Exact disjoint coupled hit rate: $P_{\text{Plan C}} = \sum_{m=1}^M \sum_{s=1}^S \pi_s \prod_{r=1}^5 F_{r,s}(T_m)$, benchmarked directly against `Plan A` at the same budget.

3. **Venue-Coupled Bias Synchronization & Live 1R–8R Bayesian Assimilation with 3-Race Minimum Consistency Guard**:
   - Link legs at the same venue via **3 to 4 MECE shared scenarios** ($\sum_s \pi_s = 1.00$), synchronizing satellite wings (`T3`/`T4`) with coherent bias regimes ($s_2$ Outer-Closer Sweep vs. $s_3$ Fast-Inner Hold).
   - **3-Race Minimum Consistency Guard (`最小3戦ガード`)**: At 1-hour-before execution (`auto_predict.py` / `直前更新`), group intraday 1R–8R results strictly by `(Venue, Turf/Dirt)`. Until **at least 3 same-venue, same-surface races** confirm a consistent directional bias, **cap any scenario weight shift at $|\Delta \pi_s| \le 0.05$ ($\pm 5\text{pt}$)** and never drop pre-selected wing horses based on 1–2 races alone. Full Bayesian updating unlocks only once $n_{\text{venue,surf}} \ge 3$ with consistent telemetry.

4. **Difficulty-Adaptive Budget Efficiency Grading**:
   - Classify each WIN5 card into `高確度攻め週` (`Type S/A ≥ 2`), `標準週`, `超難解カオス週` (`Type S = 0 & Type B/B+ ≥ 4`), or `キャリーオーバー拡張週`, outputting concise `budgetGuidance` alongside the 10,000-yen reference `planC`.

## Phase 0: Hybrid Data Ingestion & Web Auto-Fetch

- When invoked by `auto_predict.py` with scraped racecards/odds/track data, treat supplied facts as primary ground truth and fetch only missing live telemetry (1R–8R bias counts by surface, cushion value, moisture, wind, final workouts, official horse weights, carryover, scratches) if web search is enabled.
- When invoked with only a date/event name, automatically gather all 5 legs via parallel web search batches.
- **Never fabricate missing data**: If horse weights or live odds are unpublished, mark them as unreleased (and use $w_r = 1.0$ if live odds are absent). If explicitly invoked for a blind/masked backtest, disable web search.

## Steps

### Step 1: Odds-Blind Evidence Classification (F / E / H), Confrontation Graph & Regularization

Estimate Stage 1 log-ability ($\theta^{(1)}_{r,i,s} \in \mathbb{R}$, baseline $0.00$) **completely independently of odds/popularity**:

- **`F` (Verifiable Fact)**: Course geometry, turf/dirt start, cushion value, moisture, temporary rail (`A/B/C/D`), sand depth, weather/wind, 1R–8R intraday results by surface, carried weight, horse weight, draw, opening 3F, individual/race `PCI` & `RPCI`, workout times/laps, and raw past results (`着順・着差・時計・後半2F/1Fラップ・通過順・上がり3F・不利・疾病履歴`).
- **`E` (Validated Effect)** & **`H` (Heuristic / Prior)**: Shrink pedigree priors as starts $n_i$ grow ($\theta_{i,\text{ped}} = \frac{\tau_0}{\tau_0 + n_i}\Delta \theta_{\text{sire}}$), except on first-time surface switches, $\ge 2400\text{m}$ extensions, or heavy/Subarctic tracks.
- **Transitive Confrontation Graph & Race-Level Calibration**: Internally align direct meetings, 1-hop shared opponents, same-day class clock differentials, and next-out winner counts (`+0.06 to +0.14` high-level defeat boost vs. `-0.06 to -0.12` weak-field win discount).
- **Collinearity Guard & Soft-Clamp Regularization**: Bundle overlapping positional factors ($\le \pm 0.16$) and softly clamp total Stage 1 shifts at $|\sum \Delta \theta^{(1)}_{r,i}| \le 0.45$ unless backed by clear `F`-level class/surface discontinuity.

### Step 2: Ten Complete True-Winner Identification Modules (`本当に勝つ馬を見抜く10大完全検算モジュール`)

Evaluate every runner internally across all 5 legs (feeding into Stage 1 $\theta^{(1)}_{r,i,s}$):

1. **Pace-Dynamic 4th-Corner Zone, High-Pace Dirt Dual-Closer vs. Turf-Start Dry-Dirt Mandatory Top-4 Closer Slot & High-CV Sprint Outer-Speed Persistence**:
   - $N_{\text{lead}} \le 3$: Boost tactical stalkers/leaders within $\le 0.6\text{s}$ at 4C; penalize deep closers.
   - $N_{\text{lead}} \ge 4$: Trigger Pace-Collapse Switch ($\pi_{\text{collapse}} \ge 0.35$); elevate the `#1` proven mid-pack/outer closer into the Top 3–4 (Core or Wing).
   - **High-Pace Dirt ($N_{\text{lead}} \ge 5$) vs. Turf-Start Dry-Dirt ($\text{Moisture} \le 5.0\%$) Balanced Rule**: On standard/wet/dirt-start $N_{\text{lead}} \ge 5$, bar front-running favorites from `Type S` / 1-horse pins and boost `#1–#2` closers (`+0.14 to +0.20`). On **turf-start dry-dirt ($\le 5.0\%$)**, never fill Top 3 solely with deep closers—**AND never fill all 4–5 Core+Wing slots solely with front-runners/stalkers when $N_{\text{lead}} \ge 4$**: retain **(a) top Frames 2–4 inside 2nd–3rd pocket stalker (`+0.14 to +0.18`)**, **(b) top Frames 7–8 turf-dash stalker**, **AND mandatorily reserve at least 1 slot in the Top 4 (Core or Wing) for the `#1` proven pure closer (`現級連対・最速上がり実績の純差し1番手`)**.
   - **High-CV ($\ge 9.6$) Turf 1200m Sprint**: Boost Frames 6–8 top opening-3F sprinters ($\le 33.2\text{s}$ or Top 2) by `+0.12 to +0.18` ($\pi_{\text{speed\_persist}} \ge 0.35$).
2. **Two-Step Trouble Audit & Turf-Start Dirt Outer-Stalker Top-3 Promotion**:
   - Audit 4th–12th favorites for `F`-level trouble (boxed in, draw/track bias inversion, or $\text{PCI} \le 48.0$ survivor within $\le 0.8\text{s}$).
   - On turf-start dirt courses (Tokyo 1400/1600m, Nakayama 1200m, Kyoto/Hanshin/Chukyo 1400m, Niigata 1200m, Fukushima 1150m): strip `Type S` and apply `-0.15 to -0.20` to Frames 1–4 favorites lacking proven kickback tolerance; grant `+0.16 to +0.22` to **Frames 7–8 stalkers/leaders** and promote the `#1` into the **Top 3**.
3. **Class-Boundary, 3yo/4yo Class-Standard Breaker & Autumn 3yo Light-Weight / Inner-Frame Ascending Winner Priority**:
   - Penalize slow unpressured lower-class front-running older winners (`-0.12`).
   - **3yo/4yo Class-Standard Breaker**: In 2-Win/3-Win legs on standard/fast tracks, boost 3yo/4yo winners clearing both upper-class winning time AND closing 2F benchmark (Turf $\le 22.8\text{s}$ / Dirt $\le 24.4\text{s}$) by `+0.16 to +0.22` into `#1–#2` (attenuate to `+0.08` if $N_{\text{lead}} \ge 5$ + distance extension).
   - **Autumn (Oct–Dec) 3yo $53\text{–}55\text{kg}$ & Inner-Frame $57\text{kg}$ Ascending Priority**: Boost tactical/fast-closing 3yos at $53\text{–}55\text{kg}$ or Frames 1–2 streak winners at $\le 57\text{kg}$ on fast inner/B-rail tracks by `+0.16 to +0.22` into Top 3–4 above older 58kg+ layoff/prep favorites.
   - **Subarctic (`札幌・函館`) / Low-CV ($\text{CV} < 9.0$ or $\text{RPCI} \le 48.5$) Attenuation**: Halve fast-track clock bonuses ($\le +0.06$) and boost proven Subarctic/stamina runners (`+0.12 to +0.16`).
4. **1st-Place Conversion Efficiency, Chronic Silver-Collector Ceiling & 58kg+ Layoff/Medical-Return / Prep Favorite Fade**:
   - **Silver-Collector Ceiling**: 3+ consecutive 2nd–4th finishes in class, chronic slow starts, or hanging -> `-0.15 to -0.22`, barred from `Type S`.
   - **58kg+ Medical-Return / Long-Layoff Fade (Listed/Open/3-Win)**: Popular older horses ($O_i \le 7.0$) at $\ge 58.0\text{kg}$ returning from medical issues (`心房細動・鼻出血・骨折明け`) or $\ge 6$-month layoffs (including 2nd start back on inner tracks) -> strip `Type S`, apply `-0.15 to -0.20`, and **never pair two such horses as sole top-2 anchors**.
   - **G2/G3 Prep G1-Target Favorite Fade**: Penalize penalized-weight ($\ge 57\text{–}59\text{kg}$) or $+4\text{kg}+$ layoff favorites (`-0.12 to -0.18`, strip `Type S`) and boost top lone-speed/inside-pocket stalker (`+0.12 to +0.18`) into Top 3.
5. **Jensen's Inequality Variance Correction & Visiting Elite Foreign G1 vs. Returning Japanese Horse Split (`分散キャップ＆来日G1覇者分離`)**:
   - Attenuate via $\tilde{\theta}^{(1)}_{r,i,s} \approx \theta^{(1)}_{r,i,s} / \sqrt{1 + 0.304 \cdot \sigma_{r,i}^2}$:
     - **Returning Japanese Horse from Overseas Defeat**: Heavy defeat ($\ge 5\text{th}$ / $\ge 1.0\text{s}$ loss) abroad with no domestic prep -> $\sigma_{\text{overseas}}^2 \ge 0.25$, `-0.12 to -0.20`, barred from `Type S`.
     - **Visiting Elite Foreign G1 Winner (`来日中の海外G1覇者`)**: **Strictly separate from returning Japanese horses.** With sharp local turf workouts (final 1F $\le 11.5\text{s}$), favorable gate (Frames 1–5), and market backing ($O_i \le 10.0$), keep $\sigma_{\text{visit}}^2 \le 0.08$ (no first-track penalty), set leg $w_r = 0.55\text{–}0.60$, and keep eligible for Core `C` or primary Wing `W`.
     - Long layoffs ($\ge 12$ wks): barred from `Type S`.
     - Untested extreme distances ($\ge 2400\text{m}$ Oaks / $\ge 3000\text{m}$ Kikuka Sho, Tenno Sho Spring): cap $p_{r,1} \le 35.0\%$, cover $\ge 3\text{–}4$ horses across Core+Wings.
     - Ultra-long turf ($\ge 3000\text{m}$): boost 4yo stayers (`+0.10 to +0.16`), cap 6yo+ repeaters ($\Delta\theta^{(1)} \le 0.00$, barred from `Type S`).
     - 3yo first-time older dirt G1/Grade favorite ($O_i \le 3.5$): `-0.15 to -0.25`, bar from `Type S`, cap $p_{r,1} \le 32.0\%$.
     - Juvenile / early-3yo stakes ($n_i \le 2$): bar from `Type S`, cap $p_{r,1} \le 30.0\%$, cover $\ge 4$ horses, prioritize final 1F $\le 11.2\text{s}$ or $\text{PCI} \le 50$ survivors.
6. **Handicap Physics, Tight-Oval Light-Weight Boost & Fillies/Mares Inside-Pocket Dynamics**:
   - Tight-oval/short-stretch ($\le 310\text{m}$) handicaps: $50.0\text{–}53.0\text{kg}$ (or $\ge 2.0\text{kg}$ drop) with Top-3 early speed in Frames 1–5 -> `+0.16 to +0.22` (into Top 4–5).
   - Fillies/Mares stakes (4-corner/inner): Frames 7–8 wide closers `-0.12`; Frames 1–4 with final 1F $\le 11.3\text{s}$ -> `+0.15` (into Top 3–4).
7. **Special-Course Repeater Priority & Off-Condition / Wet-Track Close-Defeat Reset**:
   - Proven course repeaters or runners with a $\le 0.2\text{s}$ current-class finish losing last 1–3 starts due to wet turf, draw bias, or $\ge 200\text{m}$ distance mismatch ($O_i \ge 10.0$) -> reset defeat (`+0.14 to +0.20`) into Top 3–5.
8. **Jockey Tactical Match & Gate Departure Reliability**:
   - $\ge 30\%$ slow-start rate in last 5 starts -> barred from `Type S`.
9. **Workout Lap Physics, Prep Bounce-Back & G1 S-Workout / 3yo Classic $\le 0.2\text{s}$ Outer-Draw Exemption**:
   - Non-decelerating final 1F workouts (`11.1–11.3s 馬なり`) and domestic prep bounce-backs (`+0.14 to +0.22`).
   - **G1 Proven-Winner × S-Workout & Autumn 3yo Classic ($\le 0.2\text{s}$) Outer-Draw Mitigation**: Waive/halve outer-draw penalty (cap $\ge -0.05$) and grant `+0.14 to +0.20` into Top 3.
10. **Intraday Cushion Value, Moisture/Wind Shift & Early-Leg `Type B+` Detection**:
    - Penalize front-runners `-0.10 to -0.15` under afternoon rain or headwind $\ge 5\text{m/s}$. Enforce the **3-Race Minimum Consistency Guard** on intraday 1R–8R bias updates.
    - Flag `typeBPlus: true` when (1) rain / $\text{CV} \le 8.9$ / dirt moisture $\ge 9.0\%$ / worn inner rail, (2) $\ge 15$ runner Dirt 1200–1800m kickback or $N_{\text{lead}} \ge 5$ chaos, or (3) compressed tail ($p_{r,1} < 28.0\%$ and $p_{r,4} - p_{r,7} \le 3.5\%$).

### Step 3: Exact Venue-Coupled Tensor, Counterfactual Audit & Plan C Hard-Cap Verification

Internally compute full-field Stage 1 softmax $f^{\text{fund}}_{r,i,s}$, Stage 2 adaptive Benter posterior $p^{\text{post}}_{r,i,s}$ ($\sum_{i=1}^{N_r} p_{r,i} = 100.0\%$), and exact Plan C disjoint tickets (`T1`–`T4`). Verify internally before emitting JSON:

- **T1 Core Hard Cap**: `T1.points <= 48` (at 10,000-yen budget; $\le 45\%$ target) AND `T2`–`T4` expand **at least 3 distinct legs** (including `Type A` `#3` when $p_{r,3} \ge 9.0\%$).
- Pairwise disjointness $T_a \cap T_b = \emptyset$ and exact total points $\sum_m |T_m| \le 100$ (at 10,000-yen reference budget).
- Exact coupled hit rate $P_{\text{Plan C}} = \sum_m \sum_s \pi_s \prod_r F_{r,s}(T_m)$ strictly beats `Plan A` (otherwise fall back to `Plan A` or `Plan B`).
- Counterfactual self-audit completed for every anchor leg, every excluded $q_{r,i} \ge 15\%$ favorite, and every well-backed visiting foreign G1 winner.

### Step 4: App-Optimized Output Format (Backward-Compatible Strict JSON Schema)

To minimize Gemini API output token consumption, output **ONLY a single valid JSON object** matching the schema below when invoked by the automated script or in `JSON` mode (no markdown prose outside the JSON block). Keep `note` strings under 35 characters. Output Top 6–8 contenders per leg (plus any faded popular horse with $O_i \le 5.0$, $q_{r,i} \ge 15\%$, or visiting G1 winner $O_i \le 10.0$), **OR all declared runners when the caller prompt requests full-field output**, ensuring `f` values reflect exact full-field normalization ($\sum_{\text{all } N_r} f = 100.0$).

```json
{
  "date": "YYYY-MM-DD",
  "skill": "app-bayesian-win5",
  "version": "11.1",
  "difficultyGrade": "高確度攻め週 | 標準週 | 超難解カオス週 | キャリーオーバー拡張週",
  "budgetGuidance": "通常10,000円（カオス防衛時は3,000〜5,000円）",
  "recommendedPlan": "Plan C | Plan A | Plan B-1 | Plan B-2",
  "intradayBiasGuard": "3戦未満(±5pt制限中) | 3戦以上確認済",
  "summary": "全体戦略・会場連動バイアス要約(80字以内)",
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
        "role": "第1翼(Leg1拡張)",
        "legs": [[2, 12, 14], [5, 6], [9, 1], [5, 6], [14, 5]],
        "points": 24,
        "hitRate": 1.38,
        "scenarioSync": "s1/s2分散"
      },
      {
        "id": "T3",
        "role": "第2翼(Leg3純差し+外枠)",
        "legs": [[11], [5, 6], [8, 12, 4], [5, 6], [14, 5]],
        "points": 24,
        "hitRate": 1.05,
        "scenarioSync": "s2前崩れ同期"
      },
      {
        "id": "T4",
        "role": "第3翼(Leg2#3・Leg5外国馬)",
        "legs": [[11], [14], [9, 1], [5, 6], [14, 5, 2, 1]],
        "points": 16,
        "hitRate": 0.65,
        "scenarioSync": "Type A翼+外G1"
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
      "w": 0.70,
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

When invoked in **`事後検証・スキルパッチ生成` (Post-Race Audit Mode)**, output a compact JSON containing the 3-factor + calibration error decomposition (`scenarioError`, `ratingAndFusionError`, `shellCoverageError`) and an actionable `skillPatch` object (`targetModule`, `issue`, `proposedRuleText`) for one-tap skill evolution in the app.

## Gotchas

- Always sort `horses` strictly by `f` (Stage 2 calibrated posterior $p_{r,i}$) descending; never distort ranking order for odds/value appeal.
- Never let `planC.tickets[0]` (`T1` Core) exceed 45% of budget ($\le 48$ points at 10,000 yen), and ensure `T2`–`T4` expand **at least 3 distinct legs** (including `Type A` `#3` when $p_{r,3} \ge 9.0\%$).
- Never shift intraday $\pi_s$ by more than $\pm 0.05$ (`±5pt`) or drop pre-selected wing horses until **at least 3 same-venue, same-surface (`芝/ダ別`) races** confirm a consistent directional bias.
- Never fill all 4–5 Core+Wing slots exclusively with front-runners/stalkers in turf-start dry-dirt ($\text{Moisture} \le 5.0\%$) races when $N_{\text{lead}} \ge 4$: always reserve at least 1 slot in the Top 4 for the `#1` proven pure closer (`純差し1番手`).
- Never apply the returning-Japanese-horse overseas-defeat penalty to a visiting elite foreign G1 winner: lower $w_r = 0.55\text{–}0.60$, waive first-track penalty with positive local turf workouts/gate, and respect market support ($O_i \le 10.0$).
- Never allow overlapping tickets inside `planC.tickets`: enforce strict pairwise disjointness ($T_a \cap T_b = \emptyset$) and verify `totalPoints == sum(t.points)` and `coupledHitRate == sum(t.hitRate)`.
- Never exclude a $q_{r,i} \ge 15\%$ market favorite from all shells without a verifiable `F`-level physical hazard, and never stack correlated heuristics beyond the regularization clamp ($|\sum \Delta\theta^{(1)}_{r,i}| \le 0.45$).
