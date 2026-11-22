---
name: app-bayesian-make-debut
description: App-dedicated copy of bayesian-make-debut (v7.0 Neon Maximum Hit-Rate Edition) for the JRA Racing AI PWA and 1-hour-before pipeline. Executes mandatory full-field evaluation, 2-Stage Benter Bayesian Fusion (odds-blind fFund pooled with FLB de-vigged q via adaptive wR, clamped <=0.10 on hazards/overrides), 3-race-consistent morning 1R-4R venue bias guard, full-field exact Plackett-Luce, workout confrontation graph, gate-to-4C positional micro-simulation, rule-stacking soft clamp, counterfactual self-audit, 10-Module Make Debut physics, Overbet 6-Trigger Filter, Mid-Longshot Override, mandatory ◎-top-contender connection, single-longshot <=30% cap, Drop-Buffered Anti-Torigami Dutching Core Shield (70-80%, 11,500-12,500 JPY target, >=55% hit rate, >=42% break-even), and Win-Reach Hedge, outputting backward-compatible compact JSON for Screening, 1-Hour-Before Prediction, and Post-Race Skill Patch generation.
---
# App Bayesian Make Debut (v7.0 — Neon Maximum Hit-Rate JSON Edition)

Autonomous hierarchical Bayesian analysis system tailored for **JRA Make Debut (新馬戦 / メイクデビュー, all runners $n_i = 0$)** dedicated to the **Racing AI App (PWA) and automated 1-hour-before GitHub Actions pipeline**. This is the app-dedicated copy of `bayesian-make-debut` (**v7.0 Neon Maximum Hit-Rate & Deep-Reasoning Master Edition**), synchronizing 100% of its mandatory full-field gate, 2-Stage Benter Bayesian Fusion (with asymmetric $w_{r,i} \le 0.10$ hazard/override clamp), 3-race-consistent morning 1R–4R venue bias guard, full-field exact Plackett-Luce, workout confrontation graph, gate-to-4C positional micro-simulation, rule-stacking soft clamp, 10-Module Make Debut physics, mandatory `◎`-top-contender connection, single-longshot $\le 30\%$ cap, Drop-Buffered Anti-Torigami Dutching Core Shield (`11,500–12,500 JPY` target payout), Quantitative Win-Reach Hedge, and Counterfactual Self-Audit—while outputting **backward-compatible compact JSON** so the browser PWA can dynamically scale allocations across any user budget without extra API calls.

## When to Use

- **Morning Batch Screening (`朝一括スクリーニング`)**: Filtering all Make Debut races on the card using **Top-3 Posterior Mass ($M_3$)**, Chaos Type (`Type S/A/B/B+`), exact composite hit rate, break-even probability, and Expected ROI into `New` (`subRank`: `A` 勝負新馬 / `B` 標準新馬 / `Pass` 見送り).
- **1-Hour-Before Automated Prediction (`発走1時間前本予想`)**: Generating full-field 2-Stage Benter Fused Plackett-Luce probabilities (`f`, `fFund`, `q`, `top2`, `top3`, `wUsed`, `mark`, `role`, `tags`), `coreConnections`, Drop-Buffered Anti-Torigami `portfolioRules`, `winReachHedge`, and `counterfactualAudit` in compact JSON.
- **Weekend Post-Race Audit & Skill Patch Generation (`事後検証・スキル改訂パッチ生成`)**: Decomposing Make Debut results across 3 factors (morning-bias overreaction, fusion weight / 10-module rating error, and `◎`-connection / longshot-cap / late-drop Torigami audit) and outputting an actionable skill patch.

## Steps

### Step 0: Mandatory Full-Field Data Gate (`全頭取得必須ゲート`)

- **No Partial-Field Prediction**: Before computing probabilities or assigning ranks/tickets, inspect **all $N$ declared runners** (gate, horse number, name, sex/age, carried weight & apprentice claim `▲☆◇★`, jockey, trainer, Sire × BMS, breeder/gaikyu, latest live odds, and official race-day horse weights vs. mid-week training center weights once announced ~50–60 min pre-post). NEVER leave uninspected horses in an unchecked residual bucket.
- **Hybrid Auto-Fetch**: When invoked with search enabled and partial/missing inputs, automatically gather missing full-field entries, chronological workouts, sparring partner classes, gate test times, mid-week/official horse weights, cushion value/moisture/wind, and same-day morning 1R–4R results (`枠順・4角位置取り・1000m通過/RPCI・上がり3F`). Never fabricate unpublished clocks, gate times, weights, or odds; mark missing items as `未発表` in `triggers`.

### Step 1: Selective Resource Loading, Evidence Taxonomy (F / E / H), Confrontation Graph & Regularization Clamp

- Reference `references/make_debut_priors.md` when available for Ritto/Miho/Hokkaido workout benchmarks, Final-2F Breakers, Sire × BMS debut priors, and Gaikyu tables.
- Classify every input strictly into **`F` (Verifiable Fact)**, **`E` (Validated Effect)**, or **`H` (Heuristic / Candidate Prior)** on a dimensionless Plackett-Luce logit scale ($\theta_i \in \mathbb{R}$, baseline $0.00$), separating 1st-place shift ($\Delta \theta^{(1)}_i$), 2nd/3rd retention ($\delta^{\text{place}}_i$), and uncertainty ($\sigma_i^2$).
- **Workout Confrontation Graph**: Internally calibrate every sparring win/tie/loss against the sparring partner's actual JRA class (Open/3-Win/2-Win/1-Win/Maiden Top-2 vs. Maiden tail-ender) and cross-center clock standards.
- **Collinearity Guard & Global Soft-Clamp Regularization**: Bound combined camp/pedigree shifts at $\Delta \theta_{\text{camp}} \le +0.20$, overlapping positional synergy at $\le +0.20$, and enforce the **global soft regularization clamp ($|\sum \Delta \theta_i| \le 0.45$, $\delta^{\text{place}}_i \in [-0.30, +0.25]$)** across Phases 1–4 unless overridden by indisputable `F`-level physical discontinuity (e.g., untested Dirt Frame 1–2 kickback + gate re-test).

### Step 2: Ten-Module Make Debut Physics (100% Synced with `bayesian-make-debut` v7.0)

Evaluate all $N$ active runners ($n_i = 0$) internally across all 10 modules before generating JSON:

1. **Module 1 — Dirt All-Runners Untested Kickback Hazard & Outer/Large-Frame Bonus**:
   - **Inner-Frame Kickback Hazard (Frames 1–2 / Horses 1–4)**: Apply mandatory penalty **$\Delta \theta^{(1)}_i \in [-0.22, -0.35]$**, widen $\sigma_i^2$, $\delta^{\text{place}}_i \in [-0.10, -0.18]$, **clamp $w_{r,i} \le 0.10$**, and **strictly bar from `Single-Pivot` & `Type S`**, unless gate 1F $\le 11.8\text{s}$ (lone-lead projection) OR weight $\ge 500\text{kg}$ with verified 3-horse inside/middle kickback training.
   - **Outer-Frame & Large-Frame Bonus (Frames 6–8)**: For forward/stalking runners with Colts/Geldings $\ge 480\text{kg}$ (Fillies $\ge 460\text{kg}$), award **$\Delta \theta^{(1)}_i \in [+0.15, +0.25], \delta^{\text{place}}_i \in [+0.06, +0.12]$**.
2. **Module 2 — Turf 3-Regime Cushion Value (`CV`), Opening-Week Rail & High-CV Sprint Persistence**:
   - **High-Rebound Opening-Week (`CV >= 9.8–10.0`, `A/B` opening weeks / fresh `C/D` Day 1–2)**: Boost Frames 1–3 with gate 1F $\le 12.0\text{s}$ ($+0.08\text{ to }+0.15, \delta^{\text{place}}_i +0.06\text{ to }+0.12$); penalize wide deep closers ($-0.08\text{ to }-0.14$).
   - **Low-Rebound Tough Turf ($\text{CV} < 8.8$ or Moisture $\ge 15\%$) & Subarctic Turf (`札幌・函館`)**: Attenuate fast-track final-1F ($\le 11.3\text{s}$) bonuses by 50% ($\le +0.05$) and upgrade deep woodchip/slope sustained power loads + European/Roberto bloodlines ($+0.08\text{ to }+0.14, \delta^{\text{place}}_i +0.10\text{ to }+0.16$).
   - **High-CV ($\ge 9.6$) Turf Sprint (1200m–1400m) Persistence**: Boost Frames 6–8 with fast gate/Slope dash (`ゲート1F <= 11.8s` or Slope `4F <= 52.8s`) by $+0.10\text{ to }+0.18$ ($\pi_{\text{speed\_persist}} \ge 35\%$). When $\text{CV} \ge 9.8$, evaluate dual outer-speed survival (`☆_pace1 − ☆_pace2`).
3. **Module 3 — Winning 4th-Corner Feasibility Gate ($\le 0.6\text{s}$) vs. $N_{\text{lead}} \ge 4$ Pace-Collapse Closer**:
   - When $N_{\text{lead}} \le 2\text{–}3$ ($\text{RPCI} \ge 58.5$), boost runners projected within $\le 0.6\text{s}$ at 4C with CW/W 1F $\le 11.3\text{s}$ ($+0.12\text{ to }+0.18, \delta^{\text{place}}_i +0.08\text{ to }+0.14$), and penalize back-loaded closers projected $> 1.0\text{s}$ back at 4C ($\Delta \theta^{(1)}_i \in [-0.10, -0.18]$, bar from `Single-Pivot`, boost $\delta^{\text{place}}_i \in [+0.10, +0.18]$ as `Connector ◯/▲`).
   - When $N_{\text{lead}} \ge 4$ ($\text{RPCI} \le 48.5$), trigger $\pi_{\text{collapse}} \ge 35\%\text{–}45\%$ and elevate the `#1` mid-pack/outer closer (`☆_closer`) with inside-sparring pack tolerance and CW/W 2F $\le 22.8\text{s}$ / 1F $\le 11.4\text{s}$ into the top 3–4 of `fFund`.
4. **Module 4 — Educational / Classic-Target Debut Favorite Fade vs. Lone-Speed Steal**:
   - When a 1st/2nd favorite ($O_i \le 3.5$) has explicit camp/jockey orientation toward educational settling (`折り合い専念・教育騎乗・脚測り`), attenuate $\Delta \theta^{(1)}_i \in [-0.10, -0.18]$ (bar from `Single-Pivot`), boost $\delta^{\text{place}}_i \in [+0.10, +0.18]$ as a **`High-Floor Connector (◯/▲)`** (prime Core Shield Wide partner), and elevate the `#1` front-runner (`☆_pace`) by $+0.10\text{ to }+0.16$.
5. **Modules 5 & 6 — Fillies-Only Pocket Bonus, Tight-Oval Apprentice Speed & Steep-Uphill Stature Physics**:
   - In fillies-only turf Make Debuts (1400m–1800m), grant $+0.10\text{ to }+0.16, \delta^{\text{place}}_i +0.08\text{ to }+0.14$ to Frames 1–4 with inside-sparring tolerance + CW/W 1F $\le 11.3\text{s}$; penalize wide closers in Frames 7–8 ($-0.08\text{ to }-0.14$).
   - In tight-oval/short-stretch ($\le 310\text{m}$) Make Debuts, runners carrying $50\text{–}52\text{kg}$ via apprentice claim (`▲☆★`) with fast gate speed gain $+0.12\text{ to }+0.18$ (`☆_pace`). On steep uphills (`中山・阪神・中京・東京`), penalize $< 440\text{kg}$ favorites carrying full weight ($-0.08\text{ to }-0.14$).
6. **Module 7 — Special-Course Geometry (`新潟芝直1000m`), Sibling Heritage (`△_course_ped`), Mismatch Reset & 3yo Late-Debut Cap**:
   - Niigata 1000m Straight: Boost Frames 7–8 (and 6) with fast gate/Slope dash ($+0.18\text{ to }+0.28$), penalize Frames 1–2 ($-0.15\text{ to }-0.25$, `Single-Pivot` ban).
   - Sibling/dam with proven Top-3 record on today's exact specialized course grants $+0.06\text{ to }+0.12, \delta^{\text{place}}_i +0.08\text{ to }+0.15$ (`△_course_ped`). Reset negative half-sibling $n=0$ records if surface/sire mismatched ($+0.06\text{ to }+0.12$).
   - In 3yo late Make Debuts (Jan–Apr), reset late-foal penalty to $0.00$; expand $\sigma_i^2 \ge 0.28$, cap `fFund <= 30%`, and bar from `Single-Pivot` for setback-delayed popular horses.
7. **Module 8 — Workout 8-Axis Audit, Gate Cap, Pre-Race Transport Loss & Stayer Slope-Only Cap**:
   - **Older-Class & Final-2F Sustained Breaker**: Clearing both older total clock (`CW 6F <= 81.5s` / `Miho W 5F <= 65.8s` / `Slope 4F <= 52.2–52.5s`) AND sustained closing 2F (`CW/W 2F <= 22.8s` / `Slope 2F <= 24.4–24.6s`) awards $+0.16\text{ to }+0.24$, clamps $w_{r,i} \le 0.10$ if underbet, and promotes to rank `#1–#2` of `fFund`.
   - **Sparring Class Calibration**: Pulling away inside/middle vs. Open/3-Win/2-Win/1-Win/Maiden Top-2 awards $+0.16\text{ to }+0.25$. Discount wins over slow Maiden tail-enders by 50–70% ($\le +0.04$).
   - **Debut Silver-Collector Ceiling**: Repeated ties (`同入常習`) or hanging (`ソラ`) incurs $\Delta \theta^{(1)}_i \in [-0.10, -0.18]$ (`Single-Pivot` ban) and $\delta^{\text{place}}_i \in [+0.12, +0.20]$ (`High-Floor Connector ◯/▲`).
   - **Two-Step Trouble / High-Pace Load Survivor & Pipe-Opener V-Bounce**: Rescue late-session/wide-lane clocks ($+0.08\text{ to }+0.15$), reward high-opening-load survivors (`CW前半3F <= 36.2s` / `坂路前半2F <= 24.4s`: $+0.10\text{ to }+0.18$, clamp $w_{r,i} \le 0.10$ if underbet), and ignore slow initial gate-pass pipe-openers when final 1–2 works drop $\ge 1.5\text{s}$ ($+0.10\text{ to }+0.18$).
   - **Gate Hazard & Transport Weight-Loss Guard**: Mediocre gate ($\ge 12.3\text{s}$ 1F), gate re-test, or standing/temperament warnings prohibit `Single-Pivot` ($\Delta \theta^{(1)}_i \in [-0.10, -0.18], \delta^{\text{place}}_i \in [-0.08, -0.16]$). Official weight dropping $\ge -8\text{kg}\text{ to }-12\text{kg}$ below mid-week weight (`Type III 初輸送減り`) incurs $\Delta \theta_i \in [-0.10, -0.22], \delta^{\text{place}}_i -0.10$, and `Single-Pivot` ban.
   - **Stayer Slope-Only Cap**: In Turf $\ge 2000\text{m}$ or Dry Dirt $1800\text{m}$ debuts, slope-only training incurs $\Delta \theta^{(1)}_i \in [-0.15, -0.28]$, caps `fFund <= 32%`, and bars from `Single-Pivot`.
8. **Modules 9 & 10 — Overbet 6-Trigger Filter (`危`) & Mid-Longshot Override (`☆_override`)**:
   - Flag any $O_i \le 2.5$ favorite with light 1-week load, $< 5$ breezes, slack body (`Type II`), Dirt Frame 1–2/Gate hazard, Slope-only 2000m+/D1800m wall, or 1-week-out peak-out reaction as **`危`** ($\Delta \theta_i \in [-0.12, -0.22], \delta^{\text{place}}_i \in [-0.08, -0.16]$, **clamp $w_{r,i} \le 0.10$**, prohibit `◎` & `Single-Pivot`).
   - Promote modest-pedigree runners ($O_i \in [8.0, 25.0]$) with $\ge 6\text{–}8$ uninterrupted breezes + sparring win/tie vs. older horse (or trouble/load rescue/V-bounce) + clean draw via **$\Delta \theta_{\text{override}} \in [+0.18, +0.28]$** and **clamp $w_{r,i} \le 0.10$ (`☆_override`)**.

### Step 3: Gate-to-4C Positional Micro-Simulation, 3-Race-Consistent Morning Bias Guard, 2-Stage Benter Fusion & Exact Plackett-Luce

1. **Gate-to-4C Positional Micro-Simulation & Strict 3-Race Morning Venue Bias Guard (`午前1R〜4Rバイアス3R一致＋ラップ整合制限`)**:
   - Internally simulate `発馬 → 芝/ダ境目 → 1角 → 4角0.6秒射程圏 → 直線進路` across **3 to 4 MECE scenarios** ($\sum_s \pi_s^{\text{post}} = 1.00$), including a **Tail-Risk / Shock branch ($\pi_{\text{shock}} \in [10\%, 25\%]$)** for gate-break chaos, first-time kickback panic, or surprise lone-speed steal.
   - Update $\pi_s^{\text{post}} \propto \pi_s^{\text{prior}} \cdot L(\text{Intraday}_{1\text{R}\sim(R-1)} \mid s)$ from same-day morning 1R–4R results on the exact same surface & rail ($s_{\text{venue}}$) with strict consistency caps:
     - **$\ge 3$ consistent races with compatible pace (`S/M/H`)**: Full shift ($\pm 10\%\text{–}20\%$ on $\pi_s$, $\pm 0.06\text{–}0.12$ on logits).
     - **2 consistent races with compatible pace**: Moderate shift capped at **$\pm 6\%\text{–}10\%$** ($\pm 0.04\text{–}0.08$ on logits).
     - **$< 2$ races or pace/lap mismatch (Single-Race Overreaction Ban)**: Strictly cap shift to **$\le \pm 5\%$**.
   - Under afternoon rain or homestretch headwind $\ge 5\text{m/s}$, apply $\Delta \theta^{(1)}_i \in [-0.10, -0.15]$ to exposed lone leaders.
2. **2-Stage Benter Bayesian Fusion for $n_i = 0$**:
   - **Stage 1 (Odds-Blind Fundamental)**: Apply Jensen's Inequality variance attenuation $\tilde{\theta}^{\text{fund}}_{i,s} = \theta^{\text{fund}}_{i,s} / \sqrt{1 + 0.304 \sigma_i^2}$ to compute pure win probability `fFund` ($f^{\text{fund}}_i$).
   - **Stage 2 (Adaptive Market Fusion with Asymmetric Hazard/Override Clamp)**: Compute FLB Power de-vigged $q_i = (1/O_i)^\gamma / \sum_k (1/O_k)^\gamma$ ($\gamma \in [1.05, 1.15]$) and pool via $w_{r,i}$:
     - Baseline $n_i = 0$: $w_r \in [0.40, 0.50]$ ($0.25\text{–}0.35$ when clear `F`-level physical mispricings exist).
     - **Asymmetric Clamp ($w_{r,i} \le 0.10$)**: Strictly clamp $w_{r,i} \le 0.10$ for `危`, `☆_override`, Final-2F Breakers, High-Pace Load Survivors, and untested Dirt Frame 1–2 favorites.
     $$\theta^{\text{post}}_{i,s} = (1 - w_{r,i})\tilde{\theta}^{\text{fund}}_{i,s} + w_{r,i} \ln q_i, \qquad \theta^{\text{post},(2,3)}_{i,s} = \theta^{\text{post}}_{i,s} + \delta^{\text{place}}_i$$
   - Compute exact full-field Stage-Adjusted Plackett-Luce probabilities across ALL $N$ declared runners and scenarios, outputting **Fused Posterior Win Probability into `f` ($p_i$)**, Odds-Blind win probability into `fFund`, and individual fusion weight into `wUsed`. Verify strict conservation: $\sum f = 100.0\%, \sum \text{top2} = 200.0\%, \sum \text{top3} = 300.0\%$.
   - Compute **Top-3 Posterior Mass ($M_3 = p_{(1)} + p_{(2)} + p_{(3)}$)** and Chaos Type (`Type S / A / B / B+`).

### Step 4: Maximum Hit-Rate Portfolio Rules, Mandatory `◎` Connection, Longshot Cap, Drop-Buffered Dutching & Counterfactual Self-Audit

Default strategy profile is **`hit_rate_max`** (`的中率最大化モード`; switch to `high_roi_plan_b` only when requested):

- **Hit-Rate-First Node & Pivot Selection**:
  - Select **`◎`** as the highest Posterior $P(\text{Top 3}_i)$ & breakthrough anchor passing all `Single-Pivot` / `危` safety checks.
  - **`Single-Pivot`**: Only when $P(\text{Top 3}_{\text{◎}}) \ge 60\%$ (`high_roi_plan_b`: $\ge 52\%, p_{\text{◎}}-p_{\text{◯}} \ge 4.0\%$) with NO structural ban.
  - **`Dual-Pivot` (3-Node Triangle Core — Default in Competitive/Full-Gate Make Debuts)**: Connect `◎` directly to the Top 2–4 Posterior $P(\text{Top 3}_i)$ contenders plus the `○−▲` fallback link.
  - **`Plan B 2-Zone`** *(Optional — `high_roi_plan_b`)*: Zone 1 Core `55%–65%` + Zone 2 Deep Sniper (`#5–#7` + Win-Reach Hedge) `35%–45%`.
- **Mandatory `◎`-Top-Contender Connection (`飛び石結線禁止則`)**: ALWAYS include direct Wide/Quinella Core links from **`◎` to the Top 2–4 highest Posterior $P(\text{Top 3}_i)$ contenders** (never omitting a Top-3 market favorite with NO `危` trigger and $P(\text{Top 3}_i) \ge 35\%$). NEVER skip `◎−△1` while funding `○−△1`.
- **Single-Longshot Stake Cap ($\le 30\%$)**: Total combined outlay across all pools (Wide + Quinella + Trio + Win-Reach Hedge) containing any single longshot (`☆`, $O_i \ge 10.0$) MUST NOT exceed **`30%`** of total budget (`3,000円 / 10,000円`).
- **Drop-Buffered Anti-Torigami Dutching Core Shield (`70%–80%`, `11,500–12,500 JPY` Target)**:
  - Size Core Wide/Quinella(/Place) stakes via $x_k \approx \lceil \text{TargetReturn} / O_k \rceil_{100}$ targeting **`11,500–12,500 JPY` payout on a single Core hit** (per `10,000 JPY` baseline) so a **`-15%` late odds drop** still yields `9,800–10,600 JPY` (practical break-even).
  - Alpha & Win-Reach Tranche (`20%–30%`): positive-edge `馬連`, compact `3連複` (verify exact counts $3M+1$ / $5M+4$), capped `☆` Wide, or Quantitative Win-Reach Hedge ($B_{\text{hedge},j} = \lceil G_{\text{min}} / O_j \rceil_{100}$ for `#2–#5` value horses with $p_j \ge 8.0\%, O_j \ge 8.0$).
- **Inclusion-Exclusion Thresholds & Pass Gate**: Compute exact disjoint-state $P(\text{Any Hit})$, $P(\text{BreakEven}: \text{Payout} \ge 100\%)$, and Expected ROI. In `hit_rate_max`, require **`hitRate >= 55.0%`** (`>= 50.0%` in 15–18 runner full-gate Make Debuts), **`breakEvenRate >= 42.0%`**, **`expectedRoi >= 102.0%`** (`>= 105.0%` pre-market), and `-15%` stress ROI `>= 90.0%`; otherwise set `subRank: "Pass"` and `pivotType: "Pass"`.
- **Counterfactual Self-Audit**: Internally verify (a) `#1` failure mode of `◎` (gate miss/kickback/4C traffic) & `○−▲` coverage, (b) comeback path of any faded/`危` Top-3 favorite, and (c) conservation + single-longshot $\le 30\%$ + exact Trio counts before emitting JSON.

### Step 5: App-Optimized Backward-Compatible JSON Schemas

All existing v6.1 keys are preserved verbatim for zero-breakage PWA compatibility; new Neon v7.0 fields are additive. Output **ONLY a single valid JSON object** when invoked by the automated pipeline.

#### Mode A: `スクリーニング` (Morning Make Debut Batch Screening JSON)

```json
{
  "date": "YYYY-MM-DD",
  "venue": "東京",
  "strategyProfile": "hit_rate_max",
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
      "subRank": "A | B | Pass",
      "chaosType": "Type S | Type A | Type B | Type B+",
      "skill": "app-bayesian-make-debut",
      "pivotType": "Single-Pivot | Dual-Pivot | Plan B 2-Zone | Pass",
      "nLead": 2,
      "rpci": 59.5,
      "m3": 56.2,
      "expectedRoi": 112.4,
      "hitRate": 59.8,
      "breakEvenRate": 49.5,
      "summary": "35字以内のM3・危人気有無・判定根拠"
    }
  ]
}
```

#### Mode B: `標準` (1-Hour-Before Single-Race Prediction JSON)

Evaluate **all $N$ declared runners internally** (never skipping any horse). Sort `horses` by **Fused Posterior Win Probability `f` descending**, outputting Top 6–8 contenders + marked/Overbet (`危`) horses—or **all $N$ runners if the app prompt requests full-field rows**—with `tailSummary` ensuring $\sum f = 100.0\%$ and $\sum \text{top3} = 300.0\%$:

```json
{
  "raceId": "20261122-tok-05",
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
  "scenario": "午前バイアス(s_venue一致R数)・想定RPCI・3〜4MECEシナリオ要約(80字以内)",
  "activeModules": ["M2:高CV開幕イン先行", "M3:4角0.6s射程圏ゲート", "M8:古馬基準×後半2F突破"],
  "horses": [
    {
      "mark": "◎ | ◯ | ▲ | △ | ☆ | 危",
      "role": "最安定Top-3＆突破軸 | 安定Connector | 中穴Override | 過剰人気危",
      "num": 6,
      "name": "馬名",
      "style": "逃 | 先 | 差 | 追",
      "f": 26.8,
      "fFund": 28.5,
      "q": 18.0,
      "wUsed": 0.42,
      "top2": 45.2,
      "top3": 61.0,
      "odds": 4.2,
      "tags": ["F:CW 6F 80.9-22.4s", "H:古馬基準突破+0.22"],
      "comment": "45字以内のF/H核心根拠"
    }
  ],
  "tailSummary": { "count": 8, "sumF": 11.2, "sumTop3": 36.5 },
  "coreConnections": [[6, 3], [6, 11], [6, 2], [3, 11]],
  "portfolioRules": {
    "coreRatio": 0.75,
    "dutchTargetReturn": 11800,
    "singleLongshotCapPct": 0.30,
    "maxLongshotAllocPct": 0.22
  },
  "winReachHedge": [
    { "num": 11, "name": "馬名", "odds": 12.5, "hedge10k": 800, "hedge20k": 1600 }
  ],
  "counterfactualAudit": "◎出遅れ/進路詰まり時の○-▲防衛状態と危人気馬の復活条件(60字以内)",
  "triggers": ["直前馬体重(週中比-8kg超Type III警戒)・午前バイアス確認トリガー(40字以内)"]
}
```

#### Mode C: `事後検証` (Weekend Batch Post-Race Audit & Skill Patch JSON)

Output a JSON object containing `auditSummary`, 3-factor decomposition (`scenarioError` including morning-bias overreaction check, `ratingError` including 2-Stage fusion $w_{r,i}$ & 10-Module audit, and `portfolioError` including `◎` connection leaks, single-longshot $>30\%$ concentration, late-drop Torigami, and Win-Reach Hedge audit), and `skillPatch` (`targetSkill`, `targetVersion`, `moduleName`, `patchRule`) ready to be applied via skill update.

## Gotchas

- Never output a betting rank without inspecting all $N$ declared runners; never fabricate missing workout clocks, gate times, or horse weights.
- Never assign `Single-Pivot` to a Dirt Frame 1–2 newcomer (without elite gate $\le 11.8\text{s}$ or $\ge 500\text{kg}$ 3-horse kickback proof), a Gate-Risk runner ($\ge 12.3\text{s}$ 1F), a Slope-Only 2000m+/D1800m favorite, a 3yo setback favorite, or an Overbet `危` favorite.
- Always clamp 2-Stage Fusion market weight at $w_{r,i} \le 0.10$ for `危`, `☆_override`, Final-2F Breakers, High-Pace Load Survivors, and untested Dirt Frame 1–2 favorites so brand-bias odds never wash out verified `F`-level edges.
- Never shift morning venue bias scenario weights $\ge 10\%$ from fewer than 3 pace-consistent earlier races on the same surface (`2R一致は±6〜10%上限`, `1R/ペース不一致は±5%上限`).
- Never omit direct `◎` Wide links to Top 2–4 Posterior contenders (`飛び石結線禁止`), never allocate $> 30\%$ of total budget to any single longshot (`☆`), and always size Core Dutching to `11,500–12,500 JPY` per `10,000 JPY` baseline to survive `-15%` late odds drops.
- Always sort `horses` by Fused Posterior Win Probability `f` descending and output valid, parseable JSON without conversational filler when invoked in app pipeline mode.
