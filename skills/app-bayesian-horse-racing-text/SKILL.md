---
name: bayesian-horse-racing-text
description: "Execute text-based hierarchical Bayesian horse racing prediction for Gemini 4 Neon Maximum Hit-Rate Engine (JRA Turf/Dirt, Nankan 4 tracks) with mandatory full-field auto-gathering, 2-Stage Benter Fusion (f_fund + FLB de-vigged q via w_r), 3-race intraday bias & 3-straight-winner win-side shift, visiting foreign G1 vs returning Japanese horse split, dirt winning-streak riser & inner-gate soft cap, 2yo extreme final-2F/record override, long-stretch dirt handicap light closer & gear/weight bounce-back exception, exact Plackett-Luce, confrontation graph, positional micro-simulation, rule-stacking clamp, counterfactual self-audit, ◎-top-contender & High-ROI Top2-Fav defense, single-longshot <=30% cap, Anti-Torigami Dutching (70-80%, 11.5k-12.5k JPY), Level B weight fallback, High-ROI mode, pre-race updates, post-race audit, and M3 Screening."
---
# Bayesian Horse Racing (Text Edition — Neon Maximum Hit-Rate Engine)

Autonomous text-based hierarchical Bayesian analysis and portfolio optimization system for **JRA (Turf & Dirt) and South Kanto 4 Tracks (南関4場: 大井・川崎・船橋・浦和)**, engineered to maximize **Gemini 4 Neon's multi-step quantitative reasoning**, **autonomous full-field web data acquisition**, and **composite hit rate + break-even recovery rate (`的中率 × 元返し率最大化`)** without external executable script dependencies. It strictly separates **"Highest-Reliability Top-3 Anchor (`◎・○` 融合後3着内率上位)"**, **"3rd Triangle Connector (`▲`)"**, and **"Asymmetric Value Booster (`☆` 歪み馬)"**, treating **"Pass / No Bet (見送り / 0円)"** as a first-class conclusion whenever hit-rate or anti-Torigami criteria fail.

## Phase 0: Mandatory Full-Field Autonomous Web Data Acquisition Protocol (全頭データ自動調査・必須ゲート)

When the user requests a prediction, screening, pre-race update, or post-race audit without pasting full race data (e.g., providing only a race name, venue/race number, or date), **automatically gather all required `F` (Verifiable Fact) data via web search** before running Phases 1–7—do NOT ask the user to manually paste entry lists or odds.

1. **Full-Field Mandatory Gate (`全頭取得必須ゲート` — No Partial-Field Betting) & Level B Conditional Weight Lock**:
   - Before outputting any single-race betting portfolio (`標準` / `詳細`), you **MUST fetch and inspect the complete declared field (all $N$ runners: gate, horse number, name, sex/age, weight carried, jockey, and latest live odds)**—NEVER leave uninspected horses in a `"残余X頭未取得"` placeholder bucket, which risks omitting live 3rd–5th favorites or ascending risers.
   - If the current time is within 50–60 minutes of post time (when official JRA/NAR weights are published), also fetch **official horse weights/diffs (`公式馬体重・増減`)** and live Wide/Quinella/Trio pool odds before finalizing stakes.
   - **Level B Weight-Sensitive Conditional Lock (`馬体重未発表段階の条件付きロック`)**: Whenever outputting a `Level B` portfolio (before official horse weights are released ~50 min pre-post) where a **`◎ / ○ / ▲` anchor or primary Alpha ticket** relies on a weight-sensitive premise—(1) prior heavy gain trim assumption (previous start $\ge +10\text{kg}$, requiring $-4\text{kg}$ or better trim today), (2) long layoff return ($\ge 12$ weeks), or (3) 2yo stakes / long-distance shipping runner—explicitly mark the verdict as **`条件付き購入（Level B・馬体重確認必須）`** and append a 1-line **Pre-Registered Fallback Rule (`【自動差替ルール】`)** directly below the Section 4 betting table.
2. **Zero-Paste Auto-Fetch Checklist (Parallel Web Search Batches)**:
   - **Racecard & Live Market**: Declared full field (`全N頭の枠番・馬番・馬名・性齢・斤量・騎手・調教師・取消/除外`), latest official Win/Place/Quinella/Wide/Trio odds (`最新オッズ・取得時刻JST`), large-bet/smart-money signals (`大口投票`), and official horse weights/diffs (`馬体重・増減`).
   - **Track Physics & Intraday 1R–Prior-R Telemetry**: JRA official `クッション値`, goal-front & 4-corner `含水率 %`, temporary rail (`A/B/C/Dコース`), official going (`良〜不良`); NAR official `馬場状態・含水率・砂厚`; racecourse weather/rain timing & wind speed/direction (`風速 m/s・風向`); **same-day earlier race results (`当日1R〜直前Rの勝ち馬・2〜3着馬の枠順/4角位置取り/1000m通過ラップ/上がり・走破時計`)** for bias validation.
   - **Form, Splits & Confrontation Data**: Recent 3–5 starts, winning streaks (`連勝中昇級馬`), and exact course/distance records for all realistic contenders (`着順・着差・走破時計・通過順・テン3F/1000m通過・上がり3F・後半2F/1Fラップ・斤量・馬体重・馬場状態・共通対戦相手・次走好走馬`), gate-delay history (`出遅れ歴`), layoff/gelding status (`休養明け・去勢明け`), and gear changes (`ブリンカー等`).
   - **Workouts & Pre-Race Cues**: Final and 1-week-prior workout clocks (`坂路/CW/美W 全体時計・後半2F/1Fラップ・加速/減速・併せ馬先着・陣営コメント`) plus intraday paddock notes or late jockey/scratch updates when running `直前更新`.
   - **Post-Race Audit (`事後検証`)**: Official finish order, margins, race lap splits (`レースラップ・1000m通過・上がり3F`), corner passing orders, and official payouts (`払戻金`).
3. **Hybrid Merge with User-Provided Data (`TARGET / JRA-VAN` 併用則)**:
   - When the user supplies TARGET frontier JV / JRA-VAN CSV exports or pasted tables, treat user-provided facts as primary ground truth and automatically search **only for missing or live-updating items** (e.g., today's cushion value, moisture, wind, intraday 1R–prior-R bias, latest live odds, final workouts, official horse weights, scratches).
4. **Screening Search Efficiency (`スクリーニング` 2段階探索)**:
   - For multi-race screening, first fetch the day's race list, track conditions, intraday results, and full-field odds/top contenders across all target races in parallel; then run targeted deep searches (form lines, lap splits, workouts) on high-predictability A/B-candidate races.
5. **Source Integrity & Unreleased-Data Guard**:
   - Prioritize official/authoritative sources (JRA公式, netkeiba, nankankeiba/SPAT4, weather telemetry, major racing media) and record `{Value, Unit, Timestamp(JST), Source}` for key `F` facts.
   - **Never fabricate missing data**: If horse weights or live pool odds are not yet published, mark them explicitly as `未発表（直前更新で確認）` and set Execution Level accurately (`Level B` with verified pre-market odds; `Level C` only if market odds are unavailable, labeling estimates as `推定想定オッズ`).

## Neon Maximum Hit-Rate & Deep-Reasoning Protocol (的中率最大化・内部厳密演算ルール)

Execute all 7 phases of hierarchical Bayesian inference and quantitative verification internally at 100% mathematical fidelity while keeping external output concise and high-density:

1. **2-Stage Benter Bayesian Fusion (`オッズ非依存基礎モデル × 市場情報の適応融合` — Hit-Rate Core #1)**:
   - **Stage 1 (Odds-Blind Fundamental Model)**: Compute every runner's fundamental log-ability $\tilde{\theta}^{\text{fund}}_{i,s}$ and fundamental win probability $f^{\text{fund}}_i$ purely from Phases 1–5 **before incorporating market odds** to eliminate anchoring bias.
   - **Stage 2 (Adaptive Market Fusion)**: Strip takeout and Favorite-Longshot Bias from live odds via the Power method ($q_i = (1/O_i)^{\gamma} / \sum_k (1/O_k)^{\gamma}, \gamma \in [1.05, 1.15]$), then fuse into the **Log-Loss-Optimal Posterior** using an adaptive reliability weight $w_r \in [0.25, 0.55]$:
     $$\theta^{\text{post}}_{i,s} = (1 - w_r)\,\tilde{\theta}^{\text{fund}}_{i,s} + w_r \ln q_i, \qquad \theta^{\text{post},(2,3)}_{i,s} = \theta^{\text{post}}_{i,s} + \delta^{\text{place}}_i$$
     - Set $w_r \in [0.45, 0.55]$ in high-opacity races (2yo/3yo juveniles $n_i \le 3$, large handicaps, long-layoff fields, or races featuring elite visiting international G1 runners) where private market info (paddock/overseas fitness/stable intent) carries high predictive signal.
     - Set $w_r \in [0.25, 0.35]$ when clear `F`-level physical mispricings exist (e.g., turf-start Frame 1–2 dirt kickback favorite, returning Japanese overseas-fatigue runner, extreme +10kg weight gain, or 3+ race verified intraday rail-bias inversion).
     - Use the **Fused Posterior $p_i$** (NOT raw unfused $f^{\text{fund}}_i$) for all Plackett-Luce joint arrival probabilities $P(y_1=i, y_2=j, y_3=m)$, Top-2/Top-3 rankings, and hit-rate optimization.
2. **3-Race-Consistent & Pace-Matched Intraday Bias Assimilation (`当日バイアス3レース一致＋ラップ整合制限` — Hit-Rate Core #2)**:
   - Update prior scenario weights $\pi_s^{\text{prior}}$ via $\pi_s^{\text{post}} \propto \pi_s^{\text{prior}} \cdot L(\text{Intraday}_{1\text{R}\sim(R-1)} \mid s)$ **ONLY when at least 3 earlier races on the same surface & rail consistently demonstrate the same bias AND their pace/lap structure (S/M/H) matches the target race**.
   - **Win-Side 3-Straight-Winner Assimilation**: When $\ge 3$ earlier same-surface races consecutively produce **winners from the same outer/closer zone (e.g., Frames 6–8 closers winning 3 straight)**—even if some inside runners still fill 2nd–4th—allow a **win-side scenario shift of `+8% to +12%`** toward the matching scenario while keeping place-side inside survival intact via $\delta^{\text{place}}_i$.
   - **Single-Race Overreaction Ban**: NEVER shift $\pi_s$ by $\ge 10\%$ based on a single earlier race (e.g., an ultra-slow 2-Win conditional race where outer closers swept a 59.9s 1000m pace does NOT prove inner-rail traffic or dead inside turf in a G1 race on C-course Day 2). When sample size is $< 3$ or pace profiles diverge, cap intraday shift to $\le \pm 5\%$.
3. **Full-Field Exact Plackett-Luce & Transitive Confrontation Graph (`全頭厳密演算＆推移的対戦グラフ`)**:
   - Internally assign explicit numerical $\theta^{\text{post}}_{i,s}, \delta^{\text{place}}_i, \sigma_i^2$ to **every declared runner ($i = 1 \dots N$) across 3 to 4 MECE scenarios**, normalize $\exp(\theta^{\text{post}}_{i,s})$ directly, and compute exact 2nd/3rd-stage Plackett-Luce joint probabilities.
   - Internally construct a **pairwise margin graph** (direct meetings, 1-hop shared opponents, same-day class clock diffs) and run a **gate-by-gate positional micro-simulation (`スタート→1角→3-4角→直線進路`)** scoring boxed-in risk $P(\text{box}_i \mid s)$ and dirt kickback exposure.
4. **Mechanism Deduplication & Soft-Clamp Regularization (`重複ルール統合＆総シフト幅クランプ`)**:
   - Merge overlapping Phase 1–4 heuristics sharing the same physical mechanism into a single bounded term and enforce a **soft clamp ($|\sum \Delta \theta_i| \le 0.45$, $\delta^{\text{place}}_i \in [-0.30, +0.25]$)** unless overridden by clear `F`-level discontinuity.
5. **Mandatory `◎`-Top-Contender Connection, High-ROI Anti-Leakage Defense, Single-Longshot Cap & Drop-Buffered Dutching (`◎強制結線・高回収1〜2人気防衛・穴馬30%上限・11,500円ダッチング` — Hit-Rate Core #3)**:
   - Select **`◎`** as the highest Posterior $P(\text{Top 3}_i)$ anchor passing structural safety checks.
   - **Mandatory `◎` × Top 2–4 Contender Connection (`飛び石結線禁止則`)**: In Core Shield, ALWAYS connect **`◎` directly to the Top 2–4 highest Posterior $P(\text{Top 3}_i)$ contenders** (especially any Top-3 market favorite without a disqualifying Type II/physical failure) via Wide—NEVER skip `◎ − △1` while betting `○ − △1`.
   - **High-ROI Anti-Leakage Defense (`高回収モードにおける「◎ × 高信頼1〜2人気」完全除外禁止則`)**: Even in **`高回収モード`**, NEVER leave **`◎` completely disconnected** from a Top-2 market favorite whose Fused Posterior $P(\text{Top 3}_i) \ge 40.0\%$ (especially a 3yo/4yo dirt winning-streak riser or Grade-proven runner without a disqualifying Type II $+10\text{kg}$ gain or severe surface mismatch). If `◎ − Fav` Wide odds are too compressed ($< 3.5\text{x}$) for Core Dutching, connect via **Quinella (`馬連 ◎−Fav`)** or a **break-even rescue Wide/Trio anchor** sized to recover `60%–100%` of stake on a `◎ − Fav` finish.
   - **Single-Longshot Stake Cap ($\le 30\%$)**: Cap the combined outlay across all pools involving any single longshot (`☆`, $O_i \ge 10.0$) at **$\le 30\%$ of total budget (`3,000円` max)** so mainline `◎ − ○/▲` hits are never starved of return.
   - **Drop-Buffered Anti-Torigami Dutching**: Size Core Shield Wide/Quinella stakes to target **`11,500円〜12,500円` payout on a single Core hit** (at current/estimated odds) so that even after a **`-15%` late odds compression**, a single Core hit still returns **`9,800円〜10,600円` (practical break-even)**.
6. **Counterfactual Self-Audit & Exact Disjoint-State Verification (`反実仮想チェック＆包除原理厳密検算`)**:
   - Internally verify: (a) #1 physically plausible failure mode of `◎` and whether Core covers `○−▲`; (b) exact comeback path of any faded Top-3 market favorite; (c) $\sum P(\text{Win}) = 100.0\%$, $\sum P(\text{Top 2}) = 200.0\%$, $\sum P(\text{Top 3}) = 300.0\%$; (d) exact Trio counts ($3M+1$ / $5M+4$); (e) total stakes = `10,000円` and single-longshot total $\le 3,000\text{円}$; (f) exact **Inclusion-Exclusion / disjoint elementary state union** for $P(\text{Any Hit})$, $P(\text{元返し以上})$, $P(\text{トリガミ赤字})$, and $P(\text{不的中})$.
7. **Zero Redundant Prose & Tail-Runner Compression**: Eliminate filler and keep table cells under `35 chars`. In `標準` mode, display individual rows for marked/notable contenders (`◎◯▲△☆` and key faded favorites) plus 1 summary row (`無印計 X頭` — AFTER full-field internal evaluation of all $N$ runners) verifying `100.0% / 200.0% / 300.0%`. (Show all rows only in `詳細` mode).

## When to Use

- Predicting any JRA race (芝・ダート平地競走) or local Nankan race—either from just a race name/date (auto-gathering full-field data via Phase 0) or from user-supplied TARGET/JRA-VAN data
- Screening multiple races (`スクリーニング`) to identify high-predictability, high-hit-rate races (default: composite hit rate $\ge 60\%$ / Grade $\ge 55\%$, break-even-or-profit $\ge 45\%$, Expected ROI $\ge 102\%$ [pre-market $\ge 105\%$])
- Updating predictions 5 to 15 minutes before post time (`直前更新`) by auto-fetching official horse weights, paddock cues, 3+ race intraday bias, rain/wind shifts, and late odds movements
- Auditing finished races (`事後検証`) by auto-fetching official results/laps/payouts, or running backtest/simulation analyses (`シミュレーション`) on provided datasets

## 1. Evidence Taxonomy (F / E / H) & Scale Rules

Classify every input factor into one of three categories and never mix raw observations with interpretations:

1. **`F` (Verifiable Fact)**: Course geometry, temporary rail settings (`A/B/C/Dコース`), JRA turf cushion value (`クッション値`), goal-front and 4-corner moisture (`含水率 %`), dirt sand depth (`砂厚`), weather/wind speed & direction, same-day earlier race bias (`1R〜直前R` with lap splits), carried weight and apprentice claims (`▲☆◇★`), horse weight/diff, corner passing order, opening 3F (`テン3F`), individual and race `PCI` / `RPCI`, last 3F and final 2F/1F lap splits, workout clocks (`坂路 / CW / W`), gate delay history, and observable paddock/race cues. Always record `{Value, Unit, Location, Timestamp(JST), Source}`.
2. **`E` (Validated Effect)**: Statistical effects backed by verified sample size, period, baseline, and out-of-sample validation on a dimensionless logit scale.
3. **`H` (Heuristic / Candidate Prior)**: Candidate priors from domain physics and reference tables. Operate strictly on a **dimensionless Plackett-Luce log-ability (logit) scale ($\theta_i \in \mathbb{R}$, field baseline $0.00$)**, separating **expected ability shift ($\Delta \theta_i$)** from **uncertainty ($\sigma_i^2$ / $\sigma_i$)**.

## 2. Execution Modes, Strategy Profiles & Defaults

Switch execution modes based on user intent (default: `標準` for a single race, `スクリーニング` for multiple races):

- **Strategy Profile Toggle (Default: `的中率最大化モード`)**:
  - **`的中率最大化モード` (Default — Max Hit-Rate & Break-Even Shield)**:
    - Allocation: **Core Shield `70%–80%` (`7,000円〜8,000円`) / Alpha Booster `20%–30%` (`2,000円〜3,000円`)**, with single-longshot total $\le 30\%$ (`3,000円`) and Core single-hit Dutching target `11,500円〜12,500円`.
    - Targets: Exact $P(\text{Any Hit}) \ge \mathbf{60\%}$ ($\ge \mathbf{55\%}$ in 16–18 runner Grade races), $P(\text{元返し以上}) \ge \mathbf{45\%}$, Expected ROI $\ge \mathbf{102\%}$ (pre-market $\ge \mathbf{105\%}$), surviving `-15%` late odds drop (stress ROI $\ge 90\%$ with positive edge intact).
  - **`高回収モード` (Optional — when user explicitly requests ROI/high-payout focus)**:
    - Allocation: **Core `50%–60%` / Alpha `40%–50%`** (enforcing High-ROI Anti-Leakage Defense for `◎ × Top-2 Fav` with $P(\text{Top 3}) \ge 40\%$).
    - Targets: Exact $P(\text{Any Hit}) \ge 40\%$ ($\ge 36\%$ Grade), Expected ROI $\ge 105\%$ (pre-market $\ge 108\%$).
- **Execution Modes**:
  - **`スクリーニング` (Entropy & Hit-Rate Screening Mode)**: Auto-fetch card/track/intraday-bias/odds data across all runners and rank races by **Predictability (Top-3 Mass $M_3$ & Shannon Entropy $H_r$)**, composite hit rate, break-even probability, and ROI.
  - **`標準` (Standard Mode — Concise High-Density Output)**: Phase 0 mandatory full-field fetch + full 7-phase 2-stage Bayesian inference, counterfactual self-audit, and dual portfolio optimization (`10,000円` fixed + `1/4 Kelly`), rendered in the streamlined 4-section format.
  - **`詳細` (Detailed Mode)**: Full 18-runner individual rows, transitive confrontation graph, scenario-by-scenario logit tables, and cross-pool synthetic odds comparison.
  - **`直前更新` (Pre-Race Diff Update)**: Auto-fetch official horse weights (Type I/II/III), paddock observations, verified intraday bias, rain/wind telemetry, and late odds movement for a fast Bayesian update (10–15 lines max).
  - **`事後検証` (Post-Race Audit)**: Auto-fetch official results, race laps, and payouts for a concise hindsight-free 3-factor decomposition into (1) Scenario/intraday-bias error $\pi_s$, (2) Fusion weight $w_r$ & conditional rating error $\theta^{\text{post}}_{i,s}, \delta^{\text{place}}_i$, and (3) Pool/Dutching/Connection coverage audit.

**Budget & Bankroll Defaults**:

- **Per-Race Budget**: `10,000円` (`100円` units; respect explicit user caps).
- **Assumed Bankroll ($B$)**: `100,000円（試算用の仮設定）`. Keep Fixed Budget (`10,000円`), Kelly Cap ($L$), and Bankroll ($B$) strictly distinct.
- **Interactive HTML Output**: Omit by default to conserve tokens; output only when the user explicitly requests `"スライダー表あり"` or `"HTML出力"`.

## 3. Multi-Race Screening Mode (`スクリーニング` — Entropy & Hit-Rate First)

Evaluate all target races internally using Phase 0–6 rules (inspecting full fields so Top-3/4 favorites are never missed), computing **Top-3 Posterior Mass ($M_3 = p_{(1)} + p_{(2)} + p_{(3)}$)** and **Effective Field Concentration**, then output in a **two-tier compact format**:

1. **【A判定（高的中率×プラス期待値：的中率60%超・元返し率45%超・前売りROI105%超）】＆【B判定（直前条件次第）】レース（各レース3行ブロック）**:
   - **1行目（予測難度・馬場・展開・軸診断）**: 上位3頭集中度 $M_3$・馬場/当日バイアス（3R以上一致の有無）・先行頭数 $N_{\text{lead}}$・最安定軸 `◎・○` の信頼度 vs 人気馬死角とPivot型（`Single` / `Dual`）。
   - **2行目（融合後勝率 $p_i$・3着内率上位＆妙味馬）**: `馬番 馬名(印・型 | p_i[f_fund] | 3着内率 | 単勝オッズ | 狙い目券種)` を候補馬のみ1〜2行で列挙。
   - **3行目（判定・推定的中率/元返し率・直前条件）**: `【A or B】` + 推定合成的中率/元返し率/期待ROI・最大反証リスクまたは直前確認トリガー（1行）。
2. **【C判定（見送り：高エントロピー混戦 $M_3 < 38\%$ ／トリガミ過密・歪みなし）】レース（全レースまとめて1行リストまたは小表に圧縮）**:
   - `レース名 | 判定[C:見送り] | M_3 | 見送り理由（30字以内：混戦カオスで的中率55%未達／ガチガチでダッチング不可 等）` の1行リストにまとめる。
3. **優先勝負レース順位**: 的中率×期待値の総合スコア上位1〜3位を最後に1行で提示。

## 4. Core 7-Phase Modeling Workflow

### Phase 1: Track Physics, Venue Geometry & Structural Priors (`F` vs. `H`)

1. **JRA Turf Cushion Value (`クッション値`), Moisture (`含水率 %`) & Wind Shift (`F` -> `H`)**:
   - **高反発・高速芝 ($\text{CV} \ge 10.0$ / 低含水率)**: Boost high cruising speed, inside-rail savers (`A/Bコース` opening weeks and fresh `C/Dコース` Day 1–2), and fast Last-3F instantaneous accelerators ($\Delta \theta \in [+0.06, +0.12]$); penalize wide deep closers and heavy-action grinders ($[-0.06, -0.12]$).
   - **高速芝1200mスプリント「テン3F基礎ダッシュ力 × 外枠先行残存・行った行った決着」モデル (`High-CV Sprint Speed Persistence & Dual Outer-Speed Survival`)**: In turf 1200m sprints with $\text{CV} \ge 9.6$ (or firm turf moisture $< 12\%$), do NOT over-weight pace-collapse scenarios solely because opening 3F is fast. Sprinters with proven top-tier opening 3F speed ($\le 33.2\text{s}$ or Top 2 early speed in the field) drawn in outer frames (Frames 6 to 8) that can clear or sit 2nd without inside pinch receive $\Delta \theta^{(1)}_i \in [+0.10, +0.18]$ under a mandatory speed-persistence scenario ($\pi_{\text{speed\_persist}} \ge 35\%$). When $\text{CV} \ge 9.8$ and inner-drawn favorites prefer stalking/closing, explicitly evaluate a **dual outer-speed wire-to-wire/2nd-tracking finish (`☆_pace1 - ☆_pace2`)**.
   - **標準芝 ($8.5 \le \text{CV} < 10.0$) & 名目稍重・中盤息入り時の3歳軽量外差し昇格 (`Nominal-Wet Mid-Race Breather 3yo 54kg Wide-Closer Promotion`)**: Balanced; governed by early-pace topology, rail wear, and post position. On nominal `稍重〜重` turf where surface drainage or a mid-race breather (`中盤緩み`) allows 3yo fillies/colts carrying light imposts ($53\sim 55\text{kg}$) with proven fast final-3F acceleration to sweep from outer draws without bogging down, grant $\Delta \theta^{(1)}_i \in [+0.10, +0.16]$.
   - **低反発・タフ芝 ($\text{CV} < 8.5$ または 含水率 $\ge 15\%$) & 洋芝（札幌・函館）**: Boost European/stayer bloodlines, power-striding stalkers, course repeaters, and outer clean-turf paths ($\Delta \theta \in [+0.08, +0.14]$); penalize pure fast-ground turn-of-foot specialists ($[-0.08, -0.15]$).
   - **午後降雨・直線向かい風/追い風シフト (`Intraday Rain & Straight-Line Wind Physics`)**: When afternoon rain begins or homestretch headwind is $\ge 5\text{m/s}$, penalize exposed lone leaders ($\Delta \theta^{(1)}_i \in [-0.10, -0.15]$) and boost draft-saving slipstream stalkers/closers; under strong tailwinds on fast turf/wet dirt, boost high-cruising-speed leaders.
2. **JRA Dirt & Nankan Moisture ($m_{\text{dirt}}$), Sand Depth, Turf-Start & 15+ Full-Gate Kickback Physics (`F` -> `H`)**:
   - **乾燥・パサパサ良 ($m_{\text{dirt}} < 3.0\%$ / 深砂)**: Boost power/outer sustained runners ($[+0.05, +0.10]$); penalize kickback-fragile inside draws ($[-0.06, -0.12]$).
   - **湿潤・脚抜き良〜不良 ($m_{\text{dirt}} \ge 6.0\%$)**: Boost front/rail speed persistence ($[+0.06, +0.14]$) while maintaining a speed-duel collapse scenario branch.
   - **Turf-Start Dirt & 15+ Full-Gate Inside Kickback Hazard vs. Outer Large-Frame Stalker Survival (`芝スタート＆15頭以上多頭数ダートの内枠砂被りハザードと外枠大型先行馬のハイペース残存ボーナス`)**:
     - On turf-start dirt courses (東京ダ1400/1600m, 中山ダ1200m, 京都/阪神ダ1400m, 新潟ダ1200m, 中京ダ1400m) or 15+ runner full-gate dirt races, penalize 1st/2nd favorites drawn in Frames 1 to 2 if they lack proven pack/kickback tolerance: apply $\Delta \theta^{(1)}_i \in [-0.15, -0.22], \delta^{\text{place}}_i \in [-0.10, -0.18], \sigma_i^2 \uparrow$, and **bar from `Single-Pivot`**.
     - **3yo/4yo Dirt Winning-Streak Riser Inner-Gate Soft Cap (`3〜4歳ダート連勝昇級馬の内枠減点ソフトキャップ`)**: On 15+ full-gate dirt races, when an inner-drawn (Frames 1–2) 1st/2nd favorite is a **3yo/4yo winning-streak riser ($\ge 2$ consecutive wins) carrying light weight ($\le 56\text{kg}$)** with proven mid/late-pack passing ability, cap its inside-kickback penalty to $\Delta \theta^{(1)}_i \in [-0.08, -0.12]$ and $\delta^{\text{place}}_i \in [-0.05, -0.08]$ (do NOT stack heavy fade penalties that push it below Core connection thresholds).
     - Conversely, grant $\Delta \theta^{(1)}_i \in [+0.10, +0.16]$ to tactical stalkers/front-runners drawn in **Frames 6 to 8** (especially large-framed horses $\ge 500\text{kg}$ in tight-oval dirt races such as Fukushima/Nakayama/Kokura 1700m–1800m) that enjoy clean air outside the kickback zone.
3. **Venue Geometry, Handicap/Filly Physics, Age-Class Growth & Variance Caps (`H`)**:
   - **Fillies/Mares-Only Stakes Inside-Pocket Last-1F Bonus vs. Wide-Sweep Penalty (`牝馬限定戦1〜4枠イン溜め瞬発力ボーナス＆7〜8枠大外回し減点`)**:
     - In fillies/mares-only stakes and Open/conditional turf races (1400m to 2000m), grant $\Delta \theta^{(1)}_i \in [+0.10, +0.16], \delta^{\text{place}}_i \in [+0.08, +0.14]$ to fillies/mares drawn in **Frames 1 to 4** that can sit in the inside pocket (4th–8th) with **proven final 1F $\le 11.3\text{s}$**. Penalize popular closers drawn in **Frames 7 to 8** forced 3–4 wide around 4C ($\Delta \theta^{(1)}_i \in [-0.10, -0.14]$).
   - **Tight-Oval Local Handicap Light-Weight Front-Runner Boost, Long-Stretch Dirt Handicap Light-Weight Closer Boost & Frame-Weight Physics (`ハンデ戦の軽量先行＆長直線ダート54kg以下差しボーナス・馬格×斤量物理`)**:
     - In tight-oval or short-stretch ($\le 310\text{m}$) handicap races, a runner carrying **$50.0\sim 53.0\text{kg}$ (or $\ge 2.0\text{kg}$ drop)** with top-3 early corner speed and Frames 1–5 draw receives $\Delta \theta^{(1)}_i \in [+0.14, +0.20]$ as a mandatory `☆_pace` candidate.
     - **Long-Stretch Dirt Handicap Light-Weight Closer Boost (`長直線ダートハンデ戦1800m〜2100mの軽量54kg以下差し馬ボーナス`)**: In 3-Win/Open dirt handicap races at $\ge 1800\text{m}$ with long homestretches (e.g., Tokyo 2100m, Chukyo 1800m/1900m, Niigata 1800m), when a mid-pack/closer carries **$\le 54.0\text{kg}$ AND drops $\ge 3.0\text{kg}$** from its previous start (or is an ascending 3yo at $\le 54.0\text{kg}$), grant $\Delta \theta^{(1)}_i \in [+0.08, +0.14], \delta^{\text{place}}_i \in [+0.08, +0.15]$ under contested/attrition scenarios (`S2/S3`) and flag as a mandatory `☆_closer / ☆_handi` candidate.
     - On steep uphill finishes or dirt starts, penalize small-to-medium framed favorites ($< 480\text{kg}$) carrying $58.0\sim 59.5\text{kg}$ ($\Delta \theta^{(1)}_i \in [-0.08, -0.14]$); large-framed horses ($\ge 520\text{kg}$) absorb $58\text{kg}$ with minimal penalty.
   - **Class-Standard & Final-2F Breaker 3yo/4yo Promotion, Dirt Winning-Streak Riser Rule, 3yo Course-Grade Winner 55kg / Grade-Placed 57kg Boost & 4yo Classic-Trial Ascending Closer**:
     - **3yo/4yo Class-Standard & Final-2F Breaker**: When an ascending 3yo/4yo horse won its previous lower-class race while **clearing both the target upper-class average winning time AND the closing 2F lap benchmark (Turf final 2F $\le 22.8\text{s}$ / Dirt final 2F $\le 24.4\text{s}$)**, boost $\Delta \theta^{(1)}_i \in [+0.14, +0.22]$. Discount older horses promoted via slow, unpressured lower-class front-running (`スロー楽逃げ昇級馬`, $[-0.10, -0.16]$).
     - **3yo/4yo Dirt Winning-Streak Riser Rule (`3〜4歳ダート連勝中昇級馬・小幅距離延長の成長余地加点則`)**: In Dirt 3-Win/Open/Listed races, never auto-dismiss a 3yo or 4yo horse entering on a **$\ge 2$-race winning streak (`2連勝以上の昇級馬`)** with strong closing speed (Top-3 Last-3F in prior win) even when stepping up slightly in distance (e.g., 1200m $\to$ 1400m on long-stretch Tokyo/Kyoto dirt) and trading at double-digit odds. Grant an ascending-form bonus $\Delta \theta^{(1)}_i \in [+0.08, +0.15], \delta^{\text{place}}_i \in [+0.06, +0.12]$ and evaluate as a live `△/☆_riser` candidate over stagnant older Open repeaters.
     - **3yo Course-Grade Winner 55kg Boost & 3yo Grade-Placed 57kg Exemption in Autumn Listed/Open**: A 3yo that already won a Grade race over the exact course/distance carrying $\le 55\text{kg}$ vs. older horses receives $\Delta \theta^{(1)}_i \in [+0.10, +0.16], \delta^{\text{place}}_i \in [+0.12, +0.18]$. Do NOT penalize a 3yo carrying $57\text{kg}$ when it reflects prior Grade 1st–2nd prize money ($\Delta \theta_i \in [+0.10, +0.15]$).
     - **4yo Classic-Trial Top-4 & Elite-Pedigree Ascending Closer in Older Grade/G1 Races**: Elevate a 4yo stepping up from 3-Win/Open ($O_i \in [15.0, 60.0]$) with (a) 3yo Classic-trial G2/G3 Top-4, (b) recent win with accelerating lap or Top-2 Last-3F ($\le 33.8\text{s}$), and (c) elite pedigree or top-rider switch ($\Delta \theta^{(1)}_i \in [+0.10, +0.16], \delta^{\text{place}}_i \in [+0.14, +0.22]$) as primary `☆_closer`.
     - **洋芝（札幌・函館）および低反発タフ芝（$\text{CV} < 9.0$）・消耗戦（想定 $\text{RPCI} \le 48.5$）での時計ボーナス半減則**: Attenuate fast-track clock bonuses by 50% ($\Delta \theta_i \le +0.05$) and upgrade proven Subarctic/tough-turf sustained-pace (`RPCI <= 48.5`) top-3 horses ($\Delta \theta_i \in [+0.08, +0.14], \delta^{\text{place}}_i \in [+0.12, +0.18]$) as mandatory Core place anchors.
     - **Chronic Silver-Collector & Slow-Starter Ceiling (`現級3戦以上連続2〜4着・ソラ・出遅れ常習馬の1着減点＆2・3着アンカー活用則`)**: Cap 1st-place hazard ($\Delta \theta^{(1)}_i \in [-0.12, -0.22]$) and bar from Win-only `Single-Pivot`, while boosting 2nd/3rd retention ($\delta^{\text{place}}_i \in [+0.12, +0.20]$)—making them **prime Wide/Place Core Shield anchors** in Maximum Hit-Rate Mode! *Exception*: Do NOT apply this 1st-place cap to a Multiple-G1 / Course-G1 Winner returning to its optimal course with S-grade workouts (Phase 3-4).
   - **Stayer-to-Middle Distance ($\le 2000\text{m}$) Shortening Slow-Pace Position Hazard**: When a favorite ($O_i \le 5.0$) carrying $\ge 58.0\text{kg}$ (especially $\ge 530\text{kg}$) drops from $\ge 2400\text{m}\sim 3200\text{m}$ Grade races into a $\le 2000\text{m}$ high-CV ($\ge 9.8$) or inner-track race with $N_{\text{lead}} \le 2$ (1000m $\ge 60.0\text{s}$), apply $\Delta \theta^{(1)}_{i,\text{slow}} \in [-0.14, -0.22]$, cap $\delta^{\text{place}}_i \le +0.05$, and bar from `Single-Pivot`.
   - **Ultra-Long Stayer ($\ge 3000\text{m}$) 4yo Priority vs. 6yo+ Repeater Cap**: Prioritize 4yo Grade-stamina contenders ($\Delta \theta_i \in [+0.08, +0.16]$) as primary pivots; cap 6yo+ repeaters to $\Delta \theta^{(1)}_i \le 0.00$ with $\delta^{\text{place}}_i \in [+0.08, +0.15]$ for Wide/Trio 2nd–3rd slots.
   - **Untested Distance Extension Cap, 3yo Older Dirt G1 Cap, Juvenile Stakes ($n_i \le 2$) Cap & Extreme 2yo Turf Acceleration/Record Override**:
     - Untested marathon extension ($\ge +400\text{m}$ or $\ge 2400\text{m}$ off $\text{PCI} \ge 58$): expand $\sigma_i^2$, $\Delta \theta^{(1)}_{i,\text{attrition}} \in [-0.20, -0.40]$, cap $f^{\text{fund}}_i \le 32\%\sim 35\%$.
     - 3yo first-time older dirt G1/Grade favorite ($O_i \le 3.5$): expand $\sigma_i^2$, $\Delta \theta^{(1)}_i \in [-0.15, -0.30]$, cap $f^{\text{fund}}_i \le 32\%$.
     - Low-experience juvenile stakes ($n_i \le 2$): $\sigma_{\text{juv}}^2 \ge 0.28$, bar from `Single-Pivot`, cap $f^{\text{fund}}_i \le 30\%$, prioritize final 1F $\le 11.2\text{s}$ or $\text{PCI} \le 50$ proven runners.
     - **Extreme 2yo Turf Acceleration / Record Override (`2歳芝重賞・OP「極限ラップ・レコード勝ち」調教遅れオーバーライド則`)**: In 2yo turf stakes/Open races (1600m–2000m), if a runner won its prior turf start in a **course/2yo record time OR clocked a race/individual final 2F $\le 22.0\text{s}$ (or final 1F $\le 11.1\text{s}$ on firm ground)**, grant $\Delta \theta^{(1)}_i \in [+0.12, +0.18], \delta^{\text{place}}_i \in [+0.10, +0.16]$. **Anti-Dismissal Guard**: Do NOT drop an Extreme-Lap/Record 2yo qualifier into the unmarked (`無印`) tail bucket solely due to an outer gate (Frames 7–8) or a minor match-workout lag (`併せ馬遅れ` with solid clock); retain it at minimum as a live `△ / ☆_closer` candidate in Trio/Wide structures.
   - **Effective Field Size ($N_{\text{eff}}$)**: Keep all declared runners in the Plackett-Luce denominator, assigning $\theta_i \le -2.5$ to non-competitive tail runners.

### Phase 2: JRA-VAN / TARGET / Web Ingestion, Transitive Confrontation Graph & Form-Line Calibration

- Parse structured full-field race data from Phase 0 web searches and/or user-provided TARGET/JRA-VAN exports while keeping raw facts separate from ability ratings.
- Classify each past start as **`通常利用`**, **`条件付き利用`**, or **`欠測・除外 (state reason)`** (e.g., hurdle races, mid-race pull-up, extreme track abnormalities, severe mechanical interference).
- **Transitive Confrontation Graph & Race-Level Calibration (`対戦グラフ＆レースレベル補正`)**:
  - Internally extract all **direct meetings** and **1-hop shared-opponent links** among contenders, computing condition-adjusted relative ability gaps $\Delta \theta_{i-j}$ after controlling for carried weight ($1\text{kg} \approx 0.15\sim 0.20\text{s}$), wide-corner ground loss, and pace bias.
  - Cross-check each contender's key prior race against **same-day/same-venue upper/lower class clocks and next-out winner counts (`次走好走数`)** to adjust for hidden high-level fields (`ハイレベル戦3〜5着の再評価`, $[+0.06, +0.14]$) vs. weak-field inflation (`低レベル戦勝ちの割引`, $[-0.06, -0.12]$).
- **CSV Past-Odds vs. Live-Odds Guard**: Never confuse past-race `単勝オッズ` with live odds. Fetch live odds in Phase 0; if unavailable online, declare **`Level C`** and label estimates as `推定想定オッズ`.

### Phase 3: Trouble/Pace Audit, Returning Japanese Overseas Cap vs. Elite Visiting Foreign G1 Split, Course-Repeater Reset & Regularization Guard

1. **Two-Step Trouble & High-Pace (`PCI`) Persistence Audit**:
   - Separate **(1) Past latent ability understatement** (boxed-in traffic with unspent energy, kickback timidity, 4–5 wide loss, track/draw bias inversion, or surviving an unsustainably fast early pace $\text{PCI} \le 45\sim 48$ within $0.5\sim 0.8\text{s}$ while other leaders collapsed) from **(2) Today's recurrence risk**.
2. **Domestic Bounce-Back, Gear/Weight-Relief Exception, Returning Japanese Overseas Cap vs. Elite Visiting Foreign G1 Split (`国内前哨戦＆ギア変更軽量リバウンド vs. 日本馬海外帰り減点 vs. 来日トップ外国馬の独立評価則`)**:
   - **Domestic Prep-Race / Mismatched-Surface Bounce-Back**: When a contender backed at $O_{\text{prev}} \le 7.0$ (Top 4 favorite) in a domestic prep/mismatched condition suffered a surface defeat ($\ge 4\text{th}\sim 10\text{th}$ or $\ge 0.5\text{s}$ loss) due to heavy ground, Subarctic turf, layoff trim, pace mismatch, or traffic, and returns to proven course conditions, classify as `条件付き利用`, restore $\Delta \theta_i \in [+0.12, +0.22]$, and boost $\delta^{\text{place}}_i \in [+0.10, +0.18]$.
   - **Gear-Change & Weight-Relief Bounce-Back Exception (`同条件1人気大敗からの「ギア変更＋軽量化」リバウンド例外則`)**: When a horse that started as **1st–2nd favorite ($O_{\text{prev}} \le 4.0$)** in its last start suffered an uncharacteristic blowout ($\ge 1.5\text{s}$ loss) over the same course, do NOT auto-fade it if it returns with **TWO OR MORE structural resets**: (a) first-time/re-applied blinkers or cheekpieces (`ブリンカー着用`), (b) $\ge 2.0\text{kg}$ weight relief ($\le 54.0\text{kg}$ handicap), or (c) top-tier jockey booking (`ルメール/モレイラ/川田等`). Lift $\sigma_i^2$ while preserving $\delta^{\text{place}}_i \in [+0.05, +0.12]$ as a 3rd-slot Trio/Wide defender rather than a hard fade (`消`).
   - **Returning Japanese Overseas-Expedition First-Start Ceiling (`日本馬の海外遠征大敗明け帰国初戦の分散拡大・主軸制限則`)**: Applies strictly to **Japanese-trained horses returning from a heavy defeat ($\ge 5\text{th}$ or $\ge 1.0\text{s}$ loss) overseas** (especially European tough-turf G1s) on their first start back in Japan without a domestic prep run: apply $\sigma_{\text{overseas}}^2 \ge 0.25$, $\Delta \theta^{(1)}_i \in [-0.12, -0.20]$, cap $f^{\text{fund}}_i \le 20\%$, and bar from `Single-Pivot` or locking up a 2-horse `Dual-Pivot`.
   - **Elite Visiting Foreign G1 Contender Evaluation (`来日トップ外国馬の分離評価則` — Do NOT Confuse with Returning Japanese Horses)**: NEVER apply the returning-Japanese-horse fatigue/fade cap to a **foreign-trained active G1 winner/top-class international raider** targeting a Japanese G1 fresh from a win or top-3 G1 finish (e.g., elite European/Hong Kong stable + top international rider + proven firm-ground speed/high international rating + strong workout/large-bet market support). Evaluate its **true international G1 class + firm-turf adaptability + fresh C-course rail draw** without blanket foreign-horse penalties, and respect strong market/smart-money signals via $w_r \ge 0.40$—keeping it at minimum as a live Connector / Core-connected contender whenever it ranks Top 4–5 in Posterior $P(\text{Top 3}_i)$.
3. **G2/G3 Prep-Race G1-Target Favorite Fade vs. Lone-Speed Survivor**:
   - In G2/G3 prep races, when a 1st/2nd favorite carries penalty weight ($\ge 57\text{kg}$, especially $58\sim 59\text{kg}$), draws wide, or returns from a $\ge 3$-month layoff at $+4\text{kg}+$ targeting a later G1, attenuate 1st-place hazard ($\Delta \theta^{(1)}_i \in [-0.10, -0.18]$) while preserving 2nd/3rd class retention ($\delta^{\text{place}}_i \in [+0.05, +0.12]$) as a high-reliability Wide/Place Connector, and elevate the top unbothered front-runner/inside-pocket stalker (`☆_pace`, $[+0.08, +0.16]$).
4. **Course-Specialist Off-Condition Reset & Proven Course-G1 Winner Outer-Gate Deep-Wait Override**:
   - Reset course-specific rating ($\delta^{\text{place}}_i \in [+0.12, +0.20]$) for proven exact-course/distance specialists trading at $O_i \ge 7.5\sim 20.0$ off 1–3 mismatched runs (subject to $\ge 3000\text{m}$ 6yo+ 1st-place cap).
   - **Proven Course-G1 Winner Outer-Gate Deep-Wait Override**: Do NOT apply outer-gate 1st-place penalty or Silver-Collector cap to a horse that (a) already won a G1 on the same venue's long-stretch turf (or multiple G1s) AND (b) records an S-grade pre-race workout (e.g., 6F $\le 78.5\text{s}$ or Last 1F $\le 11.3\text{s}$ with trim weight `-2kg to -6kg`). Under contested pace ($\text{1000m} \le 59.0\text{s}$ or $N_{\text{lead}} \ge 3$), boost $\Delta \theta^{(1)}_{i,\text{collapse}} \in [+0.14, +0.24]$ as a primary `◎/◯` contender.
5. **Collinearity Guard & Rule-Stacking Regularization (`重複加点防止＆総シフト幅クランプ`)**:
   - Merge overlapping switches sharing one physical mechanism into a single bounded term ($\le \pm 0.18$).
   - Across all Phase 1–4 adjustments for any horse, apply a **soft regularization clamp**: $|\sum \Delta \theta_i| \le 0.45$ and $\delta^{\text{place}}_i \in [-0.30, +0.25]$ unless overridden by indisputable `F`-level discontinuity.

### Phase 4: Pedigree Shrinkage, Workout 5-Axis Evaluation & Run-Cycle Trajectory

- Shrink pedigree priors by career starts ($\theta_{i,\text{ped}} = \frac{\tau_0}{\tau_0 + n_i}\Delta \theta_{\text{sire}}$), except on first-time surface switches, extreme distance extensions ($\ge 2400\text{m}$), or 4yo first-time G1 challenges.
- Decompose workouts (`坂路 / CW / W`) across 5 axes: (1) Total clock vs. time-of-day/track moisture, (2) Last 2F/1F acceleration lap (`1F 11.0〜11.6s 馬なり余力` vs. deceleration penalty), (3) Course path (`外ラチ沿い` vs. `内回り`), (4) Stablemate match workout intensity (`併せ馬先着`), and (5) Run-cycle state (`国内叩き2〜3走目の上昇` vs. `日本馬海外帰国初戦割引` / `激走反動割引`). Separate fitness shift ($\Delta \theta_i$) from uncertainty ($\sigma_i^2$).
- **Extreme 2yo Turf Lap Anti-Dismissal Guard**: Never let a minor stablemate workout lag (`併せ馬遅れ` with solid overall/closing clock) override a proven 2yo turf record or final-2F $\le 22.0\text{s}$ race performance (Phase 1-3).

### Phase 5: Positional Micro-Simulation, 3-Race Intraday Bias Assimilation, 2-Stage Benter Fusion & Exact Plackett-Luce

1. **Execution Level**: Declare **`Level A`**, **`Level B`**, or **`Level C`**.
2. **Positional Micro-Simulation, 3–4 MECE Scenarios & Strict 3-Race Intraday Assimilation**:
   - Count genuine early-speed horses ($N_{\text{lead}}$) and internally simulate each horse's `スタート → 1角 → 3-4角 → 直線進路` trajectory across **3 to 4 MECE scenarios** ($\sum_s \pi_s = 1.00$), scoring boxed-in risk $P(\text{box}_i \mid s)$ and dirt kickback exposure:
     - **Standard / Slow Pace ($N_{\text{lead}} \le 2$) or High-CV ($\ge 9.6$) 1200m Sprints / Fresh C/D-Course Day 1–2**: Enforce $\pi_{\text{speed\_persist/rail}} \ge 35\%\sim 50\%$, respect inside-pocket rail savers (`1〜4枠`), and retain 1–2 proven sub-$33.2\text{s}$ final-3F closers (`☆_closer`) for 2nd/3rd slots.
     - **Contested / Fast Mid-Pace Cluster ($N_{\text{lead}} \ge 3$ in 15+ runner fields, $\text{1000m} \le 59.0\text{s}$) or Stayer Races ($\ge 2400\text{m}$)**: Trigger $\pi_{\text{attrition/collapse}} \ge 35\%\sim 45\%$, penalize inner-drawn stalker favorites for homestretch boxed-in risk ($\Delta \theta^{(1)}_{i,\text{collapse}} \in [-0.10, -0.16]$), and elevate both the #1 proven course closer AND #1 ascending 3yo/4yo closer (`☆_closer`).
     - **Tail-Risk / External-Shock Branch (Scenario 3 or 4)**: Allocate $\pi_{\text{shock}} \in [10\%, 25\%]$ to intraday weather/wind shift, rail bias inversion, or lone-speed surprise steal.
   - **Strict 3-Race Intraday Bias Assimilation Gate (`当日バイアス3レース一致＋ラップ整合制限`)**:
     - Update $\pi_s^{\text{post}} \propto \pi_s^{\text{prior}} \cdot L(\text{Intraday} \mid s)$ by $+10\%\sim +20\%$ **ONLY when $\ge 3$ same-day, same-surface races consistently show the same rail/running-style bias AND have compatible pace/lap structures (S/M/H)**.
     - **3-Straight-Winner Win-Side Shift (`3R連続同サイド勝馬出現時の勝率限定同化`)**: When $\ge 3$ earlier same-surface races consecutively produce winners from the same outer/closer zone (e.g., Frames 6–8 closers winning 3 straight races)—even if some inside runners still fill 2nd–4th—allow a **win-side scenario shift of `+8% to +12%`** toward the matching scenario while preserving place-side inside survival via $\delta^{\text{place}}_i$.
     - If fewer than 3 races exist or an earlier race was distorted by an extreme slow/fast pace mismatch, cap the intraday weight shift to $\le \pm 5\%$.
3. **2-Stage Benter Bayesian Fusion & Exact Stage-Adjusted Plackett-Luce**:
   - **Stage 1 (Odds-Blind Fundamental)**: Apply variance attenuation $\tilde{\theta}^{\text{fund}}_{i,s} = \theta^{\text{fund}}_{i,s} / \sqrt{1 + 0.304 \cdot \sigma_i^2}$ to compute Odds-Blind fundamental win probability $f^{\text{fund}}_i$.
   - **Stage 2 (Market Fusion)**: Compute FLB Power de-vigged market probability $q_i = (1/O_i)^{\gamma} / \sum_k (1/O_k)^{\gamma}$ ($\gamma \in [1.05, 1.15]$) and pool via adaptive weight $w_r \in [0.25, 0.55]$:
     $$\theta^{\text{post}}_{i,s} = (1 - w_r)\,\tilde{\theta}^{\text{fund}}_{i,s} + w_r \ln q_i, \qquad \theta^{\text{post},(2,3)}_{i,s} = \theta^{\text{post}}_{i,s} + \delta^{\text{place}}_i$$
     - Assign $\delta^{\text{place}}_i \in [-0.12, -0.25]$ (or capped $\le +0.05$) to boom-or-bust front-runners, unproven inside-kickback dirt favorites (subject to Phase 1-2 3yo/4yo winning-streak soft cap), returning Japanese overseas runners with traffic risk, untested-distance favorites, shortened $\ge 58\text{kg}$ stayers in slow $\le 2000\text{m}$ races, $n_i \le 2$ slow-debut juveniles, and 3yo first-time older dirt G1 favorites.
     - Assign $\delta^{\text{place}}_i \in [+0.10, +0.20]$ to High-Floor Place Anchors, Chronic Silver Collectors, Course Specialists, and Sustained Stalkers/Closers.
   - Compute exact conditional probabilities per scenario $s$ across all $N$ runners:
     $$P_s(y_1 = i) = \frac{\exp(\theta^{\text{post}}_{i,s})}{\sum_k \exp(\theta^{\text{post}}_{k,s})}, \quad P_s(y_2 = j \mid y_1 = i) = \frac{\exp(\theta^{\text{post},(2,3)}_{j,s})}{\sum_{k \neq i} \exp(\theta^{\text{post},(2,3)}_{k,s})}, \quad P_s(y_3 = m \mid y_1 = i, y_2 = j) = \frac{\exp(\theta^{\text{post},(2,3)}_{m,s})}{\sum_{k \notin \{i,j\}} \exp(\theta^{\text{post},(2,3)}_{k,s})}$$
   - Mix across posterior scenario weights: $P(E) = \sum_s \pi_s^{\text{post}} P_s(E)$. Verify strict conservation: $\sum_i P(\text{Win}_i) = 100.0\%$, $\sum_i P(\text{Top 2}_i) = 200.0\%$, $\sum_i P(\text{Top 3}_i) = 300.0\%$.

### Phase 6: Maximum Hit-Rate Portfolio Optimization, Mandatory `◎` Connection, Longshot Cap & Drop-Buffered Dutching

1. **Hit-Rate-First Pool Selection, Mandatory `◎`-Top-Contender Connection & High-ROI Anti-Leakage Defense (`◎×融合上位3〜4頭強制結線＆高回収1〜2人気防衛則`)**:
   - Evaluate exact joint probabilities $P(\text{Wide}_{i,j})$, $P(\text{Quinella}_{i,j})$, $P(\text{Place}_i)$, and $P(\text{Trio}_{i,j,m})$ against live/estimated pool odds, prioritizing **`ワイド` > `馬連` / `複勝` > コンパクト`3連複` > `単勝`**.
   - **Mandatory `◎` Connection Rule (`飛び石結線禁止`)**: Because 2-Stage Fusion `◎` exhibits exceptional Top-3 stability, ALWAYS include direct Wide Core links from **`◎` to the next 2 to 3 highest Posterior $P(\text{Top 3}_i)$ contenders** (and never omit a Top-3 market favorite with Posterior $P(\text{Top 3}_i) \ge 35\%$ and no disqualifying Type II/physical failure from `◎`'s Wide links in `的中率最大化モード`). NEVER skip `◎ − △1` while funding `○ − △1`.
   - **High-ROI Anti-Leakage Defense (`高回収モードにおける「◎ × 高信頼1〜2人気」完全除外禁止則`)**: Even in **`高回収モード`**, NEVER leave **`◎` completely disconnected** from a Top-2 market favorite whose Fused Posterior $P(\text{Top 3}_i) \ge 40.0\%$ (especially a 3yo/4yo dirt winning-streak riser or Grade-proven runner without a disqualifying Type II $+10\text{kg}$ gain or severe injury/surface mismatch). If `◎ − Fav` Wide odds are too compressed ($< 3.5\text{x}$) for Core Dutching, connect them via **Quinella (`馬連 ◎−Fav`)** or a **break-even rescue Wide/Trio anchor** sized to recover at least `60%–100%` of stake on a `◎ − Fav` finish rather than taking a 0-yen miss.
2. **Dynamic Pivot Selection & Anti-Single-Point-of-Failure Rule**:
   - **`Hit-Rate Single-Anchor Core (絶対安定軸型)`**: Use ONLY when $P(\text{Top 3}_{\text{◎}}) \ge 62\%$ (in `高回収モード`: $\ge 52\%$ and $p_{\text{◎}} - p_{\text{◯}} \ge 4.0\%$) AND `◎` has NO structural ban.
   - **`3-Node Triangle Core (3頭トライアングル防衛型 — Default in Competitive/Grade Races)`**: Anchor Core on `◎` connected to top contenders (`◎−○`, `◎−▲`, `◎−△1`) plus the `○−▲` fallback link so **ANY 2 of the Top-3 nodes finishing Top 3** triggers a Core Shield hit.
3. **Exact Trio Formation Combinatorial Count Guard (`3連複フォーメーション点数厳密検算`)**:
   - Standard 3-pair format **`(◎, ◯) − (◯, ▲) − (▲, △, ☆...)`** where `C` contains `▲` plus $M$ other horses ($|C| = M + 1$, disjoint from `◎, ◯`): $\mathbf{3M + 1\text{ 点}}$ *(e.g., $M=2 \implies 7\text{点}$, $M=3 \implies 10\text{点}$, $M=4 \implies 13\text{点}$)*.
   - Extended 2nd-row format **`(◎, ◯) − (◯, ▲, △1) − C`** ($|C| = M + 2$): $\mathbf{5M + 4\text{ 点}}$. Verify `点数 × 100円 = 購入額` and total outlay = **`10,000円`**.
4. **Drop-Buffered Anti-Torigami Dutching & Single-Longshot 30% Cap (`11,500円ダッチング＆単一穴馬30%上限則`)**:
   - **Inclusion-Exclusion Audit**: Compute $P(\text{Any Hit})$, $P(\text{元返し以上}: \text{Payout} \ge 10,000\text{円})$, $P(\text{トリガミ赤字}: 0 < \text{Payout} < 10,000\text{円})$, and $P(\text{不的中}: \text{Payout} = 0)$ strictly over mutually exclusive Top-3 arrival states $e = (y_1, y_2, y_3)$.
   - **Single-Longshot Stake Cap (`単一穴馬への配分上限30%則`)**: Across ALL tranches and pools (Win + Wide + Quinella + Trio), the **sum of stakes on all tickets containing any single longshot (`☆`, $O_i \ge 10.0$) MUST NOT exceed `30%` of total budget (`3,000円`)**. Never let a high-EV longshot siphon budget away from mainline Core pairs.
   - **Default `的中率最大化モード` Allocation (`10,000円` Fixed)**:
     - **Core Shield Tranche (`基礎的中・元返し防衛枠`: `70%–80%` = `7,000円〜8,000円`)**: Select the 3 to 6 highest probability-per-yen Wide/Quinella(/Place) tickets covering `◎ × {○, ▲, △1}` and `○ − ▲`. Size each Core stake via **Drop-Buffered Anti-Torigami Dutching**: set $x_k \approx \lceil \text{TargetReturn} / O_k \rceil_{100}$ with **`TargetReturn = 11,500円〜12,500円`** at reference odds so that even a **`-15%` late odds drop** still pays `9,800円〜10,600円` (eliminating late-drop Torigami).
     - **Alpha Booster Tranche (`上振れ・期待値上乗せ枠`: `20%–30%` = `2,000円〜3,000円`)**: Allocate to positive-edge ($p > q$) tickets (`馬連 ◎−○/▲`, compact `3連複 3〜10点`, `単勝` on value `◎/○/☆`, or `ワイド ◎−☆` respecting the $\le 3,000\text{円}$ single-longshot cap). In high-variance races (Subarctic/heavy turf, 15+ full-gate dirt, $n_i \le 2$ juveniles), shift Alpha from Trio to Quinella/Wide/Win.
     - **Pass Gate (`見送り基準`)**: Require exact $P(\text{Any Hit}) \ge \mathbf{60\%}$ ($\ge \mathbf{55\%}$ in 16–18 runner Grade races), $P(\text{元返し以上}) \ge \mathbf{45\%}$, Expected ROI $\ge \mathbf{102\%}$ (pre-market $\ge \mathbf{105\%}$), and `-15%` stress-test ROI $\ge 90\%$. If no valid Drop-Buffered Anti-Torigami cover satisfies these thresholds, declare **`見送り (Pass / 0円)`**.
   - Provide both **10,000-Yen Fixed Allocation** and **Budget-Constrained 1/4 Kelly** ($B = 100,000\text{円}$, cap $L = 10,000\text{円}$).

### Phase 7: Pre-Race Diff Update, Post-Race Audit & Simulation Guard

- **Anti-Hallucination & Simulation Integrity Guard**:
  - Never fabricate unverified race results, historical entry tables, or winning payouts. Clearly distinguish **(A) Empirical Backtest** on provided datasets from **(B) Analytical / Parametric Monte Carlo Simulation**.
- **Pre-Race Weight 3-Classification, Extreme Gain Fade, Gelding/Layoff Trim & Level B Auto-Fallback Rule (`直前更新`)**:
  - **Type I (`① 成長・回復・太め解消・去勢明けシェイプアップ`)**: $\Delta \theta_i \in [0.00, +0.08]$ (includes post-gelding/long-layoff 3yo/4yo returning at `-10kg to -18kg` if weight $\ge 490\text{kg}$, final 1F $\le 11.5\text{s}$, calm paddock).
  - **Type II (`② 太め残り・前哨戦余裕残し・+10kg以上大幅増の1着消し`)**: $\Delta \theta_i \in [-0.06, -0.22]$ ($\ge +6\text{kg}$ off $\ge 3\text{m}$ layoff in G2/G3 prep or $\ge +8\text{kg}$ in $\ge 1800\text{m}$; for $\ge +10\text{kg}$ extreme gain in fast/tight races, apply $\Delta \theta^{(1)}_i \in [-0.15, -0.25]$ and demote from Core anchors).
  - **Type III (`③ 輸送減り・消耗・細化`)**: $\Delta \theta_i \in [-0.06, -0.15]$ and $\sigma_i^2 \uparrow$ when unscheduled $\le -10\text{kg}$ (especially light horses dropping below `435kg`) coincides with dull coat/flank tuck/heavy sweating.
  - **Level B Pre-Registered Auto-Fallback (`馬体重未発表時の自動差替ルール`)**: Whenever a `Level B` anchor (`◎/○/▲`) carries a weight-sensitive premise (prior $\ge +10\text{kg}$ needing trim, $\ge 12\text{w}$ layoff, or 2yo/shipping), state the exact threshold and immediate stake-shift rule (e.g., `+6kg以上または絞り込み未達なら単勝・馬連を50%削減し、馬体重±4kg以内の次点馬へ移行`) right below the Section 4 betting table.
  - **Intraday Bias / Rain / Headwind Shift**: Re-run 3-race-consistent intraday Bayesian update $\pi_s^{\text{post}}$ and apply $\Delta \theta^{(1)}_i \in [-0.10, -0.15]$ to exposed leaders if afternoon rain or $\ge 5\text{m/s}$ headwind develops.
- **Smart-Money Surge Trigger**: Because Phase 5 fuses live market $q_i$ via $w_r$, a $\ge 30\%$ late odds drop or verified large-bet surge automatically lifts posterior $p_i$; additionally relax conditional penalties ($\Delta \theta^{\text{fund}}_i \in [+0.08, +0.14]$) for discounted course specialists (`△_course`) or elite foreign contenders surging late.

## 5. Required Output Structure (`標準`：高密度4セクション構成)

Keep `標準` mode output compact and scannable in **4 streamlined sections** (in `詳細` mode, expand all 18 rows, confrontation graph, and full scenario matrices):

1. **結論・前提・展開シナリオ (Conclusion, Premises & Scenarios — 4〜5行以内)**:
   - **判定・モード・構造**: `購入 / 条件付き購入（Level B・馬体重確認必須） / 見送り` ｜ `的中率最大化モード（or 高回収モード）` ｜ `Single-Anchor / 3-Node Triangle` ｜ 水準 `Level A/B/C` ｜ 予算 `10,000円`（仮資金 `100,000円`）｜ 全頭確認済・取得時刻（JST・出典）
   - **印と役割**: `◎(最安定Top-3軸)` / `○・▲(融合上位強制結線軸)` / `△` / `☆_pace・☆_closer・☆_handi・☆_riser・△_course(妙味穴・配分30%上限)`
   - **馬場・当日バイアス同化（3R一致判定）・融合重み $w_r$・MECEシナリオ $\pi_s^{\text{post}}$**: クッション値/含水率/風向・当日3R以上一致の有無（3R連続勝馬同化含む）・先行頭数 $N_{\text{lead}}$・融合重み $w_r$・上位3頭集中度 $M_3$・3〜4シナリオ確率 $\pi_s^{\text{post}}$ を1〜2行で凝縮記載。
2. **有力馬・妙味馬 確率一覧表 (Core Evaluation Table — 全頭演算後の印上位＆注目人気馬＋無印合算行)**:
   - Internally compute ALL $N$ declared runners (fetched in Phase 0) via 2-Stage Fusion + exact Plackett-Luce so $\sum \text{Win}=100.0\%, \sum \text{Top 2}=200.0\%, \sum \text{Top 3}=300.0\%$.
   - Display individual rows for marked horses (`◎◯▲△☆`) and notable faded favorites (6–10 rows) plus **1 summary row (`無印計 X頭[馬番列挙]`)**: `印・役割 | 馬番 馬名 | 脚質 | 融合勝率 p_i(基礎f) | 市場 q_i | 2着内率 | 3着内率 | 単勝オッズ | 期待値 | 核心根拠・懸念(F/H 35字以内)`
3. **重要材料・人気馬死角・反証チェック・直前トリガー (Key Edge, Favorite Audit, Counterfactual Check & Triggers — 箇条書き最大5点)**:
   - **◎・○・▲の軸選定と強制結線根拠 (F/H)**: 2段階融合・推移的対戦比較・当日バイアス判定・クラス基準時計/ダート連勝昇級/2歳極限ラップ/コース実績の決定打（1〜2行）。
   - **上位人気馬（外国馬/海外帰り/ギア変更含む）の死角と扱い**: 減点理由と `◎` 結線（Core Shield / 高回収防衛線）残留可否（1〜2行）。
   - **特化穴 (`☆_closer / ☆_pace / ☆_handi / ☆_riser / △_course`) ＆ 穴馬30%上限確認**: ワイド/馬連での確率密度優位性と単一穴馬の合計投資額（1行）。
   - **反実仮想チェック (`◎`の最大破綻経路 / 消し人気馬の復活条件)**: `◎`4着以下時の `○−▲` 防衛状態と最大リスク（1行）。
   - **直前更新トリガー (最大3点・1行凝縮)**: 馬体重(Type I〜III)・パドック・当日3R一致バイアス/雨風急変・スマートマネー急落による昇格/見送り条件と出典。
4. **1万円購入案とポートフォリオ指標 (10,000-Yen Drop-Buffered Anti-Torigami Allocation & Metrics)**:
   - Table columns: `枠(Core/Alpha) | 券種・組番 | 推定的中率 | 基準オッズ(元返しライン) | 期待回収率 | 購入額 | 期待払戻額`
   - Verify exact Trio formation counts (`計X点×100円`), `◎`×上位勢（および高回収モード時の融合3着内率40%超Top-2人気）の結線漏れゼロ、単一穴馬合計 $\le 3,000\text{円}$、Core単発目標 `11,500〜12,500円`、and total `購入額` = **`10,000円`**.
   - If `Level B` with weight-sensitive anchors, append 1 line **`【自動差替ルール】`** immediately below the table.
   - 1-line Portfolio Summary (exact disjoint-state Inclusion-Exclusion basis): **合計購入額 (`10,000円` or `0円`) ｜ 厳密合成的中率 $P(\text{Any Hit})$ ｜ 元返し以上確率（`-15%`下落時元返し） ｜ トリガミ赤字確率 / 不的中確率 ｜ 期待払戻額（純利益） ｜ 全体期待回収率 (`-15%`下落時ROI) ｜ 1/4 Kelly参考総額（内訳略記）**.
