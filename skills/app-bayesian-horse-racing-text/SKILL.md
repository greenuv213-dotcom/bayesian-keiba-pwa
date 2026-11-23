---
name: app-bayesian-horse-racing-text
description: "App-dedicated copy of bayesian-horse-racing-text (Neon Maximum Hit-Rate Engine) for the JRA/NAR Racing AI PWA and 1-hour-before pipeline. Executes mandatory full-field evaluation, 2-Stage Benter Fusion (fFund + FLB q via wR), 3-race intraday bias & 3-straight-winner shift, visiting foreign G1 vs returning Japanese split, dirt winning-streak riser & inner-gate soft cap, 2yo extreme final-2F/record override, long-stretch dirt handicap light closer & gear/weight bounce-back, exact Plackett-Luce, confrontation graph, positional micro-simulation, rule clamp, counterfactual audit, ◎-top & High-ROI Top2-Fav connection, single-longshot <=30% cap, Type II/Level B weight alerts, and Drop-Buffered Dutching (70-80%, 11.5k-12.5k JPY), outputting backward-compatible compact JSON for Screening, 1-Hour Prediction, and Post-Race Skill Patch."
---
# App Bayesian Horse Racing (Neon Maximum Hit-Rate JSON Edition)

Autonomous hierarchical Bayesian analysis system for **JRA (Turf & Dirt) and South Kanto 4 Tracks (南関4場)** dedicated to the **Racing AI App (PWA) and automated 1-hour-before GitHub Actions pipeline**. This is the app-dedicated copy of `bayesian-horse-racing-text` (**Neon Maximum Hit-Rate Engine**), synchronizing 100% of its 7-phase deep-reasoning physics, 2-Stage Benter Bayesian Fusion, mandatory full-field gate, 3-race intraday bias guard, visiting foreign G1 vs. returning Japanese horse split, 2yo extreme final-2F/record override, long-stretch dirt handicap light closer & gear/weight bounce-back exception, mandatory `◎`-top-contender & High-ROI `◎`-Top2-Fav anti-leakage connection, single-longshot $\le 30\%$ cap, Type II/Level B weight auto-alerts, and Drop-Buffered Anti-Torigami Dutching (`11,500–12,500 JPY` target payout), while outputting **backward-compatible compact JSON** so the browser PWA can dynamically scale allocations across any user budget (`1,000–30,000+ JPY`) without extra API calls.

## When to Use

- **Morning Batch Screening (`朝一括スクリーニング`)**: Filtering all races of a venue in a single API call using **Top-3 Posterior Mass ($M_3$)**, exact hit rate, break-even probability, and Expected ROI into `S` (勝負), `A` (好機), `B` (標準), or `Pass` (見送り).
- **1-Hour-Before Automated Prediction (`発走1時間前本予想`)**: Generating full-field 2-Stage Benter Fused Plackett-Luce probabilities (`f`, `fFund`, `q`, `top2`, `top3`, `mark`, `role`, `tags`), `alerts` (Type II weight downgrades or Level B conditional fallbacks), and Drop-Buffered Anti-Torigami Core/Alpha rules in compact JSON.
- **Weekend Post-Race Audit & Skill Patch Generation (`事後検証・スキル改訂パッチ生成`)**: Decomposing prediction vs. actual results across 3 factors (including intraday bias, `◎` connection coverage, and longshot concentration) and outputting an actionable skill patch.

## Steps

### Step 0: Mandatory Full-Field Data Gate & Weight-Alert Gate (`全頭取得必須ゲート＆馬体重自動アラート`)

- **No Partial-Field Prediction**: Before computing probabilities or assigning ranks/tickets, inspect **all $N$ declared runners** (gate, horse number, name, sex/age, carried weight, jockey, live odds, and official horse weights/diffs once announced ~50–60 min pre-post). NEVER leave uninspected horses in an unchecked residual bucket.
- **Hybrid Auto-Fetch**: When invoked with search enabled and partial/missing inputs, automatically gather missing full-field entries, latest live odds, official horse weights, cushion value/moisture/wind, and same-day 1R–prior-R results (`枠順・4角位置取り・1000m通過・上がり3F`). Never fabricate unpublished weights or odds; mark missing items as `未発表` in `triggers`.
- **1-Hour-Before Weight Auto-Downgrade vs. Level B Conditional Fallback (`alerts` 出力則)**:
  - **When official horse weights ARE available (1-hour-before pipeline)**: Immediately evaluate Type II (`+8kg` in $\ge 1800\text{m}$ / `+6kg` off layoff / `+10kg+` extreme gain) and failed-trim assumptions (prior $\ge +10\text{kg}$ failing to trim by $\ge 4\text{kg}$), apply the downgrade directly inside `fFund`/`f` & `mark`, and record concise diagnostic warnings in `alerts`.
  - **When official horse weights are NOT yet published (`Level B`)**: If any `◎ / ○ / ▲` anchor relies on a weight-sensitive premise (prior $\ge +10\text{kg}$ trim assumption, $\ge 12\text{w}$ layoff, or 2yo/shipping), emit an explicit conditional fallback rule into `alerts` (and `triggers`) specifying the exact weight threshold and replacement horse.

### Step 1: Evidence Taxonomy (F / E / H), Confrontation Graph & Regularization Clamp

- Classify every input strictly into **`F` (Verifiable Fact)**, **`E` (Validated Effect)**, or **`H` (Heuristic / Candidate Prior)** on a dimensionless Plackett-Luce logit scale ($\theta_i \in \mathbb{R}$, baseline $0.00$), separating 1st-place shift ($\Delta \theta^{(1)}_i$), 2nd/3rd retention ($\delta^{\text{place}}_i$), and uncertainty ($\sigma_i^2$).
- **Transitive Confrontation Graph & Race-Level Calibration**: Internally evaluate direct meetings, 1-hop shared opponents, weight differentials ($1\text{kg} \approx 0.15\sim 0.20\text{s}$), and same-day class clocks / next-out winners (`ハイレベル戦再評価 [+0.06,+0.14]` vs. `低レベル戦勝ち割引 [-0.06,-0.12]`).
- **Mechanism Deduplication & Soft-Clamp Regularization**: Merge overlapping Phase 1–4 switches sharing one physical mechanism into a single bounded term ($\le \pm 0.18$) and enforce a **soft clamp ($|\sum \Delta \theta_i| \le 0.45$, $\delta^{\text{place}}_i \in [-0.30, +0.25]$)** unless overridden by clear `F`-level discontinuity.

### Step 2: Core 7-Phase Bayesian Domain Modules (100% Synced with `bayesian-horse-racing-text`)

Execute all domain physics internally across all $N$ runners before generating JSON:

1. **JRA Turf Cushion Value (`CV`), Moisture & Wind Physics**:
   - **High-Rebound Fast Turf ($\text{CV} \ge 10.0$ / low moisture)**: Boost high cruising speed, inside-rail savers (`A/Bコース` opening weeks and fresh `C/Dコース` Day 1–2), and fast Last-3F accelerators ($+0.06\text{ to }+0.12$); penalize wide deep closers ($-0.06\text{ to }-0.12$).
   - **High-CV ($\ge 9.6$) Turf 1200m Sprint Speed Persistence & Dual Outer-Speed Survival**: Sprinters with opening 3F $\le 33.2\text{s}$ (or Top 2 early speed) in **Frames 6–8** receive $\Delta \theta^{(1)}_i \in [+0.10, +0.18]$ under $\pi_{\text{speed\_persist}} \ge 35\%$. When $\text{CV} \ge 9.8$, evaluate dual outer-speed survival (`☆_pace1 - ☆_pace2`).
   - **Nominal-Wet Mid-Race Breather 3yo 54kg Wide-Closer Promotion**: On nominal `稍重〜重` turf with a mid-race breather, grant $\Delta \theta^{(1)}_i \in [+0.10, +0.16]$ to 3yo runners carrying $53\text{–}55\text{kg}$ with proven fast final-3F acceleration sweeping from outer draws.
   - **Low-Rebound Tough Turf ($\text{CV} < 8.5$ or Moisture $\ge 15\%$) & Subarctic Turf (`札幌・函館`)**: Attenuate fast-track 3yo/4yo clock bonuses by 50% ($\le +0.05$) and upgrade proven Subarctic/sustained-pace (`RPCI <= 48.5`) top-3 runners ($\Delta \theta_i \in [+0.08, +0.14], \delta^{\text{place}}_i \in [+0.12, +0.18]$).
   - **Intraday Rain & Straight-Line Wind**: Penalize exposed lone leaders ($\Delta \theta^{(1)}_i \in [-0.10, -0.15]$) under afternoon rain or homestretch headwind $\ge 5\text{m/s}$.

2. **JRA Dirt / Nankan Moisture, Turf-Start & 15+ Full-Gate Kickback Physics**:
   - **Dry Dirt ($m_{\text{dirt}} < 3.0\%$ / deep sand)** boosts outer power ($[+0.05,+0.10]$) and penalizes kickback-fragile inside draws ($[-0.06,-0.12]$); **Wet Dirt ($m_{\text{dirt}} \ge 6.0\%$)** boosts front/rail speed ($[+0.06,+0.14]$).
   - **Turf-Start Dirt & 15+ Full-Gate Inside Kickback Hazard**: Penalize 1st/2nd favorites drawn in **Frames 1–2** lacking proven pack/kickback tolerance ($\Delta \theta^{(1)}_i \in [-0.15, -0.22], \delta^{\text{place}}_i \in [-0.10, -0.18], \sigma_i^2 \uparrow$, **bar from `Single-Pivot`**).
   - **3yo/4yo Dirt Winning-Streak Riser Inner-Gate Soft Cap (`3〜4歳ダート連勝昇級馬の内枠減点ソフトキャップ`)**: On 15+ full-gate dirt races, when an inner-drawn (Frames 1–2) 1st/2nd favorite is a **3yo/4yo winning-streak riser ($\ge 2$ consecutive wins) carrying light weight ($\le 56\text{kg}$)** with proven mid/late-pack passing ability, cap its inside-kickback penalty to $\Delta \theta^{(1)}_i \in [-0.08, -0.12]$ and $\delta^{\text{place}}_i \in [-0.05, -0.08]$ (never stack heavy fade penalties that drop it below Core connection thresholds).
   - **Outer Large-Frame Stalker Survival**: Grant $\Delta \theta^{(1)}_i \in [+0.10, +0.16]$ to tactical stalkers/front-runners in **Frames 6–8** (especially $\ge 500\text{kg}$ in tight-oval dirt races such as Fukushima/Nakayama/Kokura 1700m–1800m).

3. **Fillies Pocket, Handicap Physics, Class/Age Growth & Dirt Winning-Streak Riser Rules**:
   - **Fillies/Mares-Only Inside-Pocket Bonus**: Grant $\Delta \theta^{(1)}_i \in [+0.10, +0.16], \delta^{\text{place}}_i \in [+0.08, +0.14]$ to fillies/mares in **Frames 1–4** with proven final 1F $\le 11.3\text{s}$; penalize wide closers in **Frames 7–8** on 4-corner/inner tracks ($-0.10\text{ to }-0.14$).
   - **Tight-Oval Local Handicap Light-Weight Boost**: Runners carrying **$50.0\text{–}53.0\text{kg}$ (or $\ge 2.0\text{kg}$ drop)** with top-3 early corner speed in Frames 1–5 gain $\Delta \theta^{(1)}_i \in [+0.14, +0.20]$ as mandatory `☆_pace`. Penalize $< 480\text{kg}$ favorites carrying $58.0\text{–}59.5\text{kg}$ on uphill/dirt starts ($[-0.08,-0.14]$).
   - **Long-Stretch Dirt Handicap Light-Weight Closer Boost (`長直線ダートハンデ戦1800m〜2100mの軽量54kg以下差し馬ボーナス`)**: In 3-Win/Open dirt handicap races at $\ge 1800\text{m}$ with long homestretches (Tokyo 2100m, Chukyo 1800m/1900m, Niigata 1800m), when a mid-pack/closer carries **$\le 54.0\text{kg}$ AND drops $\ge 3.0\text{kg}$** (or is an ascending 3yo at $\le 54.0\text{kg}$), grant $\Delta \theta^{(1)}_i \in [+0.08, +0.14], \delta^{\text{place}}_i \in [+0.08, +0.15]$ under contested/attrition scenarios (`S2/S3`) as a mandatory `☆_closer / ☆_handi` candidate.
   - **3yo/4yo Class-Standard & Final-2F Breaker**: Boost ascending 3yo/4yo winners clearing both upper-class average time AND closing 2F benchmark (Turf $\le 22.8\text{s}$ / Dirt $\le 24.4\text{s}$) by $\Delta \theta^{(1)}_i \in [+0.14, +0.22]$. Discount slow unpressured older-horse front-running promotions ($[-0.10,-0.16]$).
   - **3yo/4yo Dirt Winning-Streak Riser Rule (`3〜4歳ダート連勝中昇級馬・小幅距離延長の成長余地加点則`)**: In Dirt 3-Win/Open/Listed races, never auto-dismiss a 3yo or 4yo runner entering on a **$\ge 2$-race winning streak** with Top-3 Last-3F closing speed even when stepping up slightly in distance (e.g., 1200m $\to$ 1400m on Tokyo/Kyoto dirt) at double-digit odds. Grant $\Delta \theta^{(1)}_i \in [+0.08, +0.15], \delta^{\text{place}}_i \in [+0.06, +0.12]$ as a live `△/☆_riser` candidate.
   - **3yo Course-Grade Winner 55kg & Grade-Placed 57kg Exemption**: Grant $\Delta \theta^{(1)}_i \in [+0.10, +0.16], \delta^{\text{place}}_i \in [+0.12, +0.18]$ to a 3yo carrying $\le 55\text{kg}$ with a Grade win over the exact course/distance; treat $57\text{kg}$ on a Grade-placed 3yo as class proof ($+0.10\text{ to }+0.15$).
   - **4yo Classic-Trial Ascending Closer in Older Grade/G1 Races**: Elevate 4yo step-ups ($O_i \in [15,60]$) with 3yo Classic-trial G2/G3 Top-4 + accelerating recent win ($\le 33.8\text{s}$) + elite pedigree/rider ($\Delta \theta^{(1)}_i \in [+0.10,+0.16], \delta^{\text{place}}_i \in [+0.14,+0.22]$) as `☆_closer`.

4. **Favorite Hazards, Bounce-Back Exceptions, Returning Japanese vs. Visiting Elite Foreign G1 Split, 2yo Extreme Lap Override & Weights**:
   - **Chronic Silver-Collector & Slow-Starter Ceiling**: Cap 1st-place hazard ($\Delta \theta^{(1)}_i \in [-0.12, -0.22]$, bar from Win-only `Single-Pivot`) while boosting 2nd/3rd retention ($\delta^{\text{place}}_i \in [+0.12, +0.20]$)—ideal Wide Core Shield anchors in Maximum Hit-Rate Mode.
   - **Gear-Change & Weight-Relief Bounce-Back Exception (`同条件1人気大敗からの「ギア変更＋軽量化」リバウンド例外則`)**: When a horse that started as **1st–2nd favorite ($O_{\text{prev}} \le 4.0$)** in its last start suffered an uncharacteristic blowout ($\ge 1.5\text{s}$ loss) over the same course, do NOT auto-fade it if it returns with **TWO OR MORE structural resets**: (a) first-time/re-applied blinkers/cheekpieces, (b) $\ge 2.0\text{kg}$ weight relief ($\le 54.0\text{kg}$ handicap), or (c) top-tier jockey booking (`ルメール/モレイラ/川田等`). Lift $\sigma_i^2$ while preserving $\delta^{\text{place}}_i \in [+0.05, +0.12]$ as a 3rd-slot defender rather than `消`.
   - **Stayer-to-Middle ($\le 2000\text{m}$) Shortening Slow-Pace Hazard**: For favorites ($O_i \le 5.0$, $\ge 58.0\text{kg}$) dropping from $\ge 2400\text{m}$ into $\le 2000\text{m}$ high-CV ($\ge 9.8$)/inner tracks with $N_{\text{lead}} \le 2$, apply $\Delta \theta^{(1)}_{i,\text{slow}} \in [-0.14,-0.22]$, cap $\delta^{\text{place}}_i \le +0.05$, bar from `Single-Pivot`.
   - **Returning Japanese Overseas Cap vs. Elite Visiting Foreign G1 Split (`日本馬海外大敗帰り減点 vs. 来日トップ外国馬の独立評価則`)**:
     - Apply the overseas first-start fatigue ceiling ($\sigma_{\text{overseas}}^2 \ge 0.25, \Delta \theta^{(1)}_i \in [-0.12,-0.20], f^{\text{fund}}_i \le 20\%$, bar from `Single-Pivot`/2-horse lock) **strictly to Japanese-trained horses returning from heavy overseas defeats ($\ge 5\text{th}$ or $\ge 1.0\text{s}$ loss)** without a domestic prep.
     - **NEVER apply this fatigue cap to active elite visiting foreign G1 contenders** (top European/Hong Kong stable + top rider + fresh G1 win/Top-3 + firm-turf speed + strong workout/large-bet support). Evaluate international G1 class + fresh rail draw independently and respect market/large-bet signals via $w_r \ge 0.40$, keeping them Core-connected whenever Top 4–5 in Posterior $P(\text{Top 3}_i)$.
   - **Proven Course-G1 Winner Outer-Gate Deep-Wait Override**: Exempt venue long-stretch G1 winners posting S-grade workouts (`6F <= 78.5s` or `1F <= 11.3s` with trim weight) from outer-gate/Silver-Collector 1st-place penalties; boost $\Delta \theta^{(1)}_{i,\text{collapse}} \in [+0.14,+0.24]$ under contested pace.
   - **Distance/Age/Experience Caps & Extreme 2yo Turf Acceleration/Record Override**:
     - Ultra-long $\ge 3000\text{m}$ favors 4yo stamina ($[+0.08,+0.16]$) over 6yo+ repeaters ($\Delta \theta^{(1)}_i \le 0.00$); cap $f^{\text{fund}}_i \le 32\%\sim 35\%$ for untested marathon extensions, $\le 32\%$ for 3yo first-time older dirt G1 favorites, and $\le 30\%$ ($\sigma_{\text{juv}}^2 \ge 0.28$, no `Single-Pivot`) for $n_i \le 2$ juvenile stakes.
     - **Extreme 2yo Turf Acceleration / Record Override (`2歳芝重賞・OP「極限ラップ・レコード勝ち」調教遅れオーバーライド則`)**: In 2yo turf stakes/Open races (1600m–2000m), if a runner won its prior turf start in a **course/2yo record time OR clocked a race/individual final 2F $\le 22.0\text{s}$ (or final 1F $\le 11.1\text{s}$ on firm ground)**, grant $\Delta \theta^{(1)}_i \in [+0.12, +0.18], \delta^{\text{place}}_i \in [+0.10, +0.16]$. **Anti-Dismissal Guard**: Never drop an Extreme-Lap/Record 2yo qualifier into `tailSummary` (`無印`) solely due to an outer gate (Frames 7–8) or minor match-workout lag (`併せ馬遅れ` with solid clock); retain at minimum as a live `△ / ☆_closer`.
   - **Pre-Race Weight 3-Classification**: **Type I** (`-2kg to -8kg` trim, or post-gelding/long-layoff 3yo/4yo `-10kg to -18kg` keeping $\ge 490\text{kg}$ & 1F $\le 11.5\text{s}$: $[0.00,+0.08]$); **Type II** ($\ge +6\text{kg}$ off layoff in prep, $\ge +8\text{kg}$ in $\ge 1800\text{m}$, or **$\ge +10\text{kg}$ extreme gain**: $\Delta \theta^{(1)}_i \in [-0.15,-0.25]$, demote from Core anchors and emit `alerts`); **Type III** (unscheduled $\le -10\text{kg}$, especially dropping below `435kg`: $[-0.06,-0.15], \sigma_i^2 \uparrow$).

### Step 3: Positional Micro-Simulation, 3-Race Intraday Bias Guard, 2-Stage Benter Fusion & Exact Plackett-Luce

1. **Positional Micro-Simulation & Strict 3-Race Intraday Bias Assimilation**:
   - Internally simulate `スタート → 1角 → 3-4角 → 直線進路` across **3 to 4 MECE scenarios** ($\sum_s \pi_s = 1.00$), scoring $P(\text{box}_i \mid s)$ and dirt kickback exposure.
   - **3-Race-Consistent & Pace-Matched Bias Gate (`当日バイアス3レース一致＋ラップ整合制限`)**: Shift $\pi_s^{\text{post}} \propto \pi_s^{\text{prior}} \cdot L(\text{Intraday} \mid s)$ by $+10\%\sim +20\%$ **ONLY when $\ge 3$ earlier same-day, same-surface races consistently show the same rail/running-style bias AND match the target race's pace structure (S/M/H)**.
   - **3-Straight-Winner Win-Side Shift (`3R連続同サイド勝馬出現時の勝率限定同化`)**: When $\ge 3$ earlier same-surface races consecutively produce winners from the same outer/closer zone (e.g., Frames 6–8 closers winning 3 straight)—even if inside runners fill 2nd–4th—allow a **win-side scenario shift of `+8% to +12%`** toward the matching scenario while preserving place-side inside survival via $\delta^{\text{place}}_i$.
   - If $< 3$ races exist or pace profiles diverge (e.g., a single slow conditional race before a G1), cap intraday shift to $\le \pm 5\%$.
2. **2-Stage Benter Bayesian Fusion**:
   - **Stage 1 (Odds-Blind Fundamental)**: Apply variance attenuation $\tilde{\theta}^{\text{fund}}_{i,s} = \theta^{\text{fund}}_{i,s} / \sqrt{1 + 0.304\sigma_i^2}$ to compute fundamental win probability `fFund` ($f^{\text{fund}}_i$).
   - **Stage 2 (Adaptive Market Fusion)**: Compute FLB Power de-vigged market probability $q_i = (1/O_i)^\gamma / \sum_k (1/O_k)^\gamma$ ($\gamma \in [1.05, 1.15]$) and fuse via adaptive weight $w_r \in [0.25, 0.55]$ ($0.45\text{–}0.55$ for juveniles/handicaps/visiting foreign G1s; $0.25\text{–}0.35$ for clear `F`-level physical mispricings):
     $$\theta^{\text{post}}_{i,s} = (1 - w_r)\,\tilde{\theta}^{\text{fund}}_{i,s} + w_r \ln q_i, \qquad \theta^{\text{post},(2,3)}_{i,s} = \theta^{\text{post}}_{i,s} + \delta^{\text{place}}_i$$
   - Compute exact full-field Stage-Adjusted Plackett-Luce probabilities across all $N$ runners and scenarios, outputting **Fused Posterior Win Probability into `f` ($p_i$)** and Odds-Blind probability into `fFund`. Verify conservation strictly: $\sum f = 100.0\%, \sum \text{top2} = 200.0\%, \sum \text{top3} = 300.0\%$.

### Step 4: Maximum Hit-Rate Portfolio Rules, Mandatory `◎` Connection & Counterfactual Self-Audit

Default strategy profile is **`hit_rate_max`** (`的中率最大化モード`; switch to `high_roi` only when requested):

- **Hit-Rate-First Node & Pivot Selection**:
  - Select **`◎`** as the highest Posterior $P(\text{Top 3}_i)$ anchor passing structural safety checks.
  - **`Single-Pivot`**: Only when $P(\text{Top 3}_{\text{◎}}) \ge 62\%$ (in `high_roi`: $\ge 52\%, p_{\text{◎}}-p_{\text{◯}} \ge 4.0\%$) with NO structural ban.
  - **`Dual-Pivot` / `3-Node Triangle` (Default in competitive/Grade races)**: Connect `◎` directly to the next 2–3 highest Posterior $P(\text{Top 3}_i)$ contenders plus `○−▲` fallback.
- **Mandatory `◎`-Top-Contender Connection & High-ROI Anti-Leakage Defense (`飛び石結線禁止＆高回収1〜2人気防衛則`)**:
  - In `hit_rate_max`, ALWAYS include direct Wide Core links from **`◎` to the Top 2–4 Posterior $P(\text{Top 3}_i)$ contenders** (never omitting a Top-3 market favorite with $P(\text{Top 3}_i) \ge 35\%$ and no disqualifying Type II/physical failure). NEVER skip `◎−△1` while funding `○−△1`.
  - **High-ROI Anti-Leakage Defense**: Even in `high_roi`, NEVER leave **`◎` completely disconnected** from a Top-2 market favorite with Fused Posterior $P(\text{Top 3}_i) \ge 40.0\%$ (unless disqualified by Type II $+10\text{kg}$ gain or severe surface mismatch). Include `[◎, Fav]` in `coreConnections` via Quinella (`馬連`) or break-even rescue Wide/Trio recovering `60%–100%` of stake if Wide odds are $< 3.5\text{x}$.
- **Single-Longshot Stake Cap ($\le 30\%$)**: Total combined outlay across all pools containing any single longshot (`☆`, $O_i \ge 10.0$) MUST NOT exceed **`30%`** of total budget (`3,000円 / 10,000円`).
- **Drop-Buffered Anti-Torigami Dutching Core Shield (`70%–80%`, `11,500–12,500 JPY` Target)**:
  - Size Core Wide/Quinella(/Place) stakes via $x_k \approx \lceil \text{TargetReturn} / O_k \rceil_{100}$ targeting **`11,500–12,500 JPY` payout on a single Core hit** (per `10,000 JPY` baseline) so a **`-15%` late odds drop** still yields `9,800–10,600 JPY` (practical break-even).
  - Alpha Booster (`20%–30%`): positive-edge `馬連`, compact `3連複` (verify exact counts $3M+1$ / $5M+4$), `単勝`, or capped `☆` Wide. Shift Alpha away from Trio toward Quinella/Win on Subarctic/heavy turf, 15+ full-gate dirt, and $n_i \le 2$ juvenile stakes.
- **Inclusion-Exclusion Thresholds & Pass Gate**: Compute exact disjoint-state $P(\text{Any Hit})$, $P(\text{BreakEven}: \text{Payout} \ge 100\%)$, and Expected ROI. Require **`hitRate >= 60.0%`** (`>= 55.0%` in 16–18 runner Grade races), **`breakEvenRate >= 45.0%`**, **`expectedRoi >= 102.0%`** (`>= 105.0%` pre-market), and `-15%` stress ROI `>= 90.0%`; otherwise set `rank: "Pass"` and `pivotType: "Pass"`.
- **Counterfactual Self-Audit**: Internally verify (a) `◎` failure mode & `○−▲` coverage, (b) faded Top-3 favorite comeback path, and (c) conservation + single-longshot $\le 30\%$ + exact Trio counts before emitting JSON.

### Step 5: App-Optimized Backward-Compatible JSON Schemas

All existing keys are preserved verbatim for zero-breakage PWA compatibility; new Neon Hit-Rate & Weight-Alert fields (`alerts`) are additive.

#### Mode A: `スクリーニング` (Morning Venue Batch Screening JSON)

```json
{
  "date": "YYYY-MM-DD",
  "venue": "東京",
  "strategyProfile": "hit_rate_max",
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
      "name": "オーロラC(L)",
      "surfaceDist": "芝1400m",
      "postTime": "15:25",
      "rank": "S | A | B | Pass",
      "skill": "app-bayesian-horse-racing-text",
      "pivotType": "Single-Pivot | Dual-Pivot | Pass",
      "nLead": 4,
      "m3": 52.4,
      "expectedRoi": 111.5,
      "hitRate": 62.1,
      "breakEvenRate": 54.0,
      "summary": "35字以内のM3・的中率・判定根拠"
    }
  ]
}
```

#### Mode B: `標準` (1-Hour-Before Single-Race Prediction JSON)

Evaluate **all $N$ declared runners internally** (never skipping any horse). Output all marked contenders (`◎◯▲△☆`) plus notable faded favorites (`消`, $O_i \le 6.0$)—or **all $N$ runners if the app prompt requests full-field rows**—with `tailSummary` ensuring $\sum f = 100.0\%$ and $\sum \text{top3} = 300.0\%$:

```json
{
  "raceId": "20261122-tok-11",
  "venue": "東京11R",
  "name": "レース名",
  "surfaceDist": "ダ1400m",
  "postTime": "15:20",
  "skill": "app-bayesian-horse-racing-text",
  "strategyProfile": "hit_rate_max",
  "rank": "S | A | B | Pass",
  "pivotType": "Single-Pivot | Dual-Pivot | Pass",
  "nLead": 4,
  "rpci": 48.2,
  "wR": 0.35,
  "m3": 52.4,
  "intradayBias3R": true,
  "expectedRoi": 111.5,
  "hitRate": 61.2,
  "breakEvenRate": 58.4,
  "scenario": "当日3R一致バイアス・展開・3〜4MECEシナリオ重み要約(80字以内)",
  "horses": [
    {
      "mark": "◎ | ◯ | ▲ | △ | ☆ | 消",
      "role": "最安定Top-3軸 | 双頭対抗軸 | 第3軸Connector | 連勝昇級穴 | 危険人気馬",
      "num": 5,
      "name": "馬名",
      "style": "逃 | 先 | 差 | 追",
      "f": 19.6,
      "fFund": 21.5,
      "q": 16.0,
      "top2": 38.8,
      "top3": 55.4,
      "odds": 5.2,
      "tags": ["F:東ダ1400[3-1-0-0]", "H:2段階融合軸+0.16"],
      "comment": "45字以内のF/H核心根拠"
    }
  ],
  "tailSummary": { "count": 8, "sumF": 10.3, "sumTop3": 29.6 },
  "coreConnections": [[5, 6], [5, 1], [5, 14], [6, 14]],
  "portfolioRules": {
    "coreRatio": 0.76,
    "dutchTargetReturn": 11800,
    "singleLongshotCapPct": 0.30,
    "maxLongshotAllocPct": 0.24
  },
  "alerts": ["馬体重Type II(+8kg超)自動減点・絞り込み未達警告、またはLevel B自動差替ルール(50字以内)"],
  "counterfactualAudit": "◎破綻時の○-▲防衛状態と消し人気馬の復活条件(60字以内)",
  "triggers": ["直前馬体重(Type I-III)・実オッズ確認トリガー(40字以内)"]
}
```

#### Mode C: `事後検証` (Weekend Batch Post-Race Audit & Skill Patch JSON)

Output a JSON object containing `auditSummary`, 3-factor decomposition (`scenarioError` including intraday-bias overreaction & 3-straight-winner check, `ratingError` including foreign G1 vs. returning Japanese split, dirt riser, 2yo extreme-lap, & handicap bounce-back checks, and `portfolioError` including `◎` connection leaks, High-ROI Top-2 Fav defense, single-longshot $>30\%$ concentration, and late-drop Torigami audit), and `skillPatch` (`targetSkill`, `targetVersion`, `moduleName`, `patchRule`) ready to be applied via `skill-updater`.

## Gotchas

- Never confuse a past-race odds column with live market odds, and never output a betting rank without inspecting all $N$ declared runners.
- Never apply the returning-Japanese-horse overseas fatigue cap to elite visiting foreign G1 contenders; evaluate them independently with $w_r \ge 0.40$.
- Never shift intraday scenario weights $\ge 10\%$ from fewer than 3 pace-consistent earlier races on the same surface (except the win-side `+8% to +12%` shift when $\ge 3$ consecutive same-surface winners come from the same outer/closer zone).
- Never drop a 2yo turf record or final-2F $\le 22.0\text{s}$ winner into `tailSummary` solely for an outer gate or minor match-workout lag.
- Never omit direct `◎` Wide links to Top 2–4 Posterior contenders (`飛び石結線禁止`) or leave `◎` disconnected from a Top-2 favorite with $P(\text{Top 3}) \ge 40\%$ even in `high_roi`, never allocate $> 30\%$ of total budget to any single longshot (`☆`), and always size Core Dutching to `11,500–12,500 JPY` per `10,000 JPY` baseline to survive `-15%` late odds drops.
- Always output valid, parseable JSON without conversational filler when invoked in app pipeline mode.
