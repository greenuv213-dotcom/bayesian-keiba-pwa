---
name: app-bayesian-nar
description: App-dedicated copy of bayesian-nar (v7.1 Neon Maximum Hit-Rate Edition) for the JRA/NAR Racing AI PWA and 1-hour-before pipeline. Executes mandatory full-field evaluation (excluding scratches and non-flat Ban'ei harness races), 2-Stage Benter Bayesian Fusion (fFund pooled with FLB de-vigged q via adaptive wR with 50x+ extreme-longshot cap and >=0.28 inner-gate Top-2 fav guard), 3-race-consistent intraday bias guard, full-field exact Plackett-Luce, confrontation graph, positional micro-simulation, rule-stacking soft clamp, counterfactual self-audit, NAR real-distance dirt moisture/sand-depth/sloppy-dual-regime/outer-G-winner/tight-oval-closer/1800m+ heavy-gain/Nankan-DG-JRA-fav-protection & local-anchor physics, synthetic-odds <1.35x / <=8-runner / dominant-fav <=1.6x Pass guard, O◎<=2.0 2-line Core compression, mandatory ◎-top-contender & Top-2 market fav connection, single-longshot <=30% cap, Drop-Buffered Anti-Torigami Dutching Core Shield (70-80%, 11,500-12,500 JPY target, >=60% hit rate, >=45% break-even), and Nankan 4-track asymmetric Triple Umatan optimization, outputting backward-compatible compact JSON for Screening, 1-Hour-Before Prediction, Triple Umatan, and Post-Race Skill Patch generation.
---

# App Bayesian NAR Local Horse Racing (v7.1 — Neon Maximum Hit-Rate JSON Edition)

Autonomous hierarchical Bayesian analysis system specialized for **Japanese Local Flat Horse Racing (地方平地競馬: 南関東4場 [大井・川崎・船橋・浦和] および全国NARダートグレード競走; strictly excluding Ban'ei harness racing ばんえい帯広)** dedicated to the **Racing AI App (PWA) and automated 1-hour-before GitHub Actions pipeline**. This is the app-dedicated copy of `bayesian-nar` (**v7.1 Neon Maximum Hit-Rate & Deep-Reasoning Edition**), synchronizing 100% of its mandatory full-field gate, verified real-distance enforcement, 2-Stage Benter Bayesian Fusion (with 50x+ extreme-longshot cap and tight-oval inner-gate Top-2 favorite soft cap), 3-race-consistent intraday bias guard, full-field exact Plackett-Luce, confrontation graph, gate-to-4C positional micro-simulation, rule-stacking soft clamp, NAR dirt/venue/weight physics, JRA Dirt-Grade favorite protection + Nankan local top-rider 3rd-place anchor, mandatory `◎`-top-contender & Top-2 market-favorite connection, single-longshot $\le 30\%$ cap, synthetic-odds $< 1.35\text{x}$ / $\le 8$-runner / dominant-favorite $\le 1.6\text{x}$ auto-Pass discipline, $O_{\text{◎}} \le 2.0\text{x}$ 2-line Core compression, Drop-Buffered Anti-Torigami Dutching Core Shield (`11,500–12,500 JPY` target payout), Counterfactual Self-Audit, and Nankan 4-track Probability-Shell Triple Umatan (`トリプル馬単`) optimization—while outputting **backward-compatible compact JSON** so the browser PWA can dynamically scale allocations across any user budget without extra API calls.

## When to Use

  - **Batch Screening (`スクリーニング`)**: Filtering Nankan / NAR Dirt-Grade cards using **Top-3 Posterior Mass ($M_3$)**, Core synthetic odds, exact hit rate, break-even probability, and Expected ROI into `S` (勝負), `A` (好機), `B` (標準), or `Pass` (見送り: トリガミ懸念の一強レース・少頭数低配当・カオス戦).
  - **1-Hour-Before Automated Prediction (`発走1時間前本予想`)**: Generating full-field 2-Stage Benter Fused Plackett-Luce probabilities (`f`, `fFund`, `q`, `wUsed`, `top2`, `top3`, `mark`, `role`, `tags`), `coreConnections`, Drop-Buffered Anti-Torigami `portfolioRules`, `tickets`, and `counterfactualAudit` in compact JSON.
  - **Triple Umatan Optimization (`トリプル馬単`)**: Generating 2-Stage Fused 1st/2nd-place Exacta probabilities and asymmetric Probability-Shell orthogonal ticket sets (Core Shell + Wing Shell) strictly across the final 3 **Nankan 4-track legs (`大井・川崎・船橋・浦和 10R, 11R, 12R`)** for `50円` unit dynamic scaling.
  - **Post-Race Audit & Skill Patch Generation (`事後検証・スキル改訂パッチ生成`)**: Decomposing NAR results across 3 factors and outputting an actionable skill patch.

## Steps

### Step 0: Mandatory Full-Field Data Gate & Real-Distance Verification (`全頭取得＆実距離確認必須ゲート`)

  - **No Partial-Field Prediction & Flat-Only Guard**: Before computing probabilities or assigning ranks/tickets, inspect **all $N$ active declared runners** (gate, horse number, name, sex/age, carried weight & apprentice claim `▲☆◇★`, jockey, trainer/affiliation, live odds, and official horse weights/diffs once announced ~50–60 min pre-post). Exclude scratched/withdrawn (`取消・除外`) runners completely before normalization. Never apply this flat-dirt model to Ban'ei Obihiro (`ばんえい帯広`) harness races.
  - **Real-Distance Enforcement (`Patch N3`)**: Always verify the exact official distance (`800m / 900m / 1200m / 1400m / 1500m / 1600m / 1800m / 2000m / 2100m / 2400m`) and inner/outer loop before triggering distance-dependent switches (`<=1200m` sprint waiver vs. `>=1800m` `+12kg+` Type II downgrade). Never assume a default `1600m` distance.
  - **Hybrid Auto-Fetch**: When invoked with search enabled and partial/missing inputs, automatically gather missing full-field entries, latest live odds, official horse weights, official NAR moisture/sand depth/night conditions, and same-day earlier race results (`1R〜直前R` passing orders, inner-dead-sand status, times). Never fabricate unpublished weights or odds; mark missing items as `未発表` in `triggers`.

### Step 1: Evidence Taxonomy (F / E / H), Confrontation Graph & NAR Track/Venue/Weight Physics

Classify all inputs into **`F` (Verifiable Fact)**, **`E` (Validated Effect)**, or **`H` (Heuristic / Candidate Prior)** on a dimensionless Plackett-Luce logit scale ($\theta_i \in \mathbb{R}$, baseline $0.00$). Internally construct a **Transitive Confrontation Graph** (direct meetings, 1-hop shared opponents, weight diffs, same-day class clock comparisons). Bundle overlapping positional switches into $\le +0.16$ and enforce the **global soft clamp ($|\sum \Delta \theta_i| \le 0.45$, $\delta^{\text{place}}_i \in [-0.30, +0.25]$)** unless overridden by clear `F`-level discontinuity.

1.  **Moisture ($m_{\text{dirt}}$), Sand Depth, Sloppy-Track Dual Regime & Tight-Oval Inner-Gate Soft Cap (`Patch N2`)**:
      - **Dry Power Dirt ($m_{\text{dirt}} < 3.0\%$ / deep white sand)**: Boost power/outer sustained runners ($+0.05\text{ to }+0.10$); penalize kickback-fragile inside draws ($-0.06\text{ to }-0.12$), subject to the Top-2 favorite soft cap below.
      - **Tight-Oval NAR Inner-Gate Top-2 Favorite Soft Cap & Wet-Sprint Waiver (`小回りNAR内枠1〜2人気ソフトキャップ＆重不良短距離免除則` — `Patch N2`)**:
          - On **wet/sloppy short-distance dirt ($\le 1200\text{m}$)**, waive the Frames 1–2 inside kickback penalty ($0.00\text{ to }+0.08$) for fast-gate / Top-3 market runners.
          - On tight-oval NAR tracks (`浦和・川崎・園田・笠松・水沢・名古屋等`), when a Frame 1–2 runner is a **Top-2 market favorite ($O_i \le 4.5$)** without an `1800m+ +12kg+` Type II flaw, **cap its inside-gate penalty at $\Delta \theta^{(1)}_i \in [-0.08, -0.10], \delta^{\text{place}}_i \in [-0.04, -0.06]$, maintain $w_{r,i} \ge 0.28$, and strictly prohibit hard-fading (`消`) or disconnecting it from `◎` Core connections**.
      - **Sloppy/Heavy Track ($m_{\text{dirt}} \ge 10.0\%$): (i) Outer Large-Frame Stalker Boost**: Upgrade large-framed speed/stalker types ($\ge 500\text{kg}$, especially with `-2kg to -10kg` Type I trim) in **Frames 6–8** securing a clean 2nd–4th outside position ($\Delta \theta_i \in [+0.08, +0.16], \delta^{\text{place}}_i \in [+0.06, +0.12]$). **(ii) Extended-Distance Sloppy Attrition ($\ge 2000\text{m}$)**: Do not penalize light-framed horses ($\le 450\text{kg}$); if entering with a `-4kg to -8kg` trim and local stamina, boost $\Delta \theta^{(1)}_{i,\text{attrition}} \in [+0.12, +0.22]$.
      - **Outer Clean-Air Lead Steal & JRA Multi-Grade Winner Immunity**: In Dirt Grade races (1800m–2000m), even on `良〜稍重`, if a proven JRA multi-grade winner draws **Frames 7–8** and can sweep to an unbothered lead or outside 2nd, grant $\Delta \theta^{(1)}_i \in [+0.10, +0.16]$, waive `+200m` extension penalties, and do not over-penalize `57–58kg` base weights.
      - **Inner Deep Sand (`イン死に馬場`)**: When confirmed by intraday consistency guard, penalize rail hugging ($-0.08\text{ to }-0.15$) and boost paths 3–5 ($+0.06\text{ to }+0.12$).
2.  **Nankan 4-Track & Regional Geometry**:
      - **大井 (Right)**: Outer loop (`1200/1400/1800/2000m`, 386m stretch) aids outer stalkers/closers ($+0.06\text{ to }+0.12$). Inner loop (`1500/1600m`, 286m stretch) favors Frames 1–4 speed ($+0.08\text{ to }+0.12$).
      - **川崎 (Left, 300m stretch)**: Sharp hairpin turns; `900m/1600m` favor Frames 1–3 gate speed ($+0.08\text{ to }+0.14$).
      - **船橋 (Left, 308m stretch, Banked Spiral Turns)**: Aids outer stalkers/makuri in Frames 5–8 ($+0.08\text{ to }+0.14$).
      - **浦和 (Left, 220m stretch) & Tight-Oval Pace-Collapse Nankan Top-Rider 3rd-Place Exemption**: Top 3 at 3C–4C is critical ($+0.10\text{ to }+0.16$); Frame 1 slow breakers (outside Top-2 market favorites) face boxed-in risk ($\delta^{\text{place}}_i \in [-0.08, -0.15]$). When $\pi_{\text{collapse}} \ge 30\%$, grant $\delta^{\text{place}}_i \in [+0.12, +0.20]$ to proven Nankan closers ridden by Nankan top riders (`矢野貴之・御神本訓史・笹川翼・吉原寛人`) for 2nd/3rd coverage.
      - **6-Corner Middle/Long-Distance (笠松・名古屋・園田・金沢・川崎2100m)**: Enforce forward-retention scenario floor $\pi_{\text{forward}} \ge 35\%\text{–}40\%$.
3.  **Weight Rules, Prep Bounce-Back, Dirt-Grade JRA Favorite Protection & Nankan Local Anchor (`Patch N3`)**:
      - **1800m+ Heavy-Gain (+12kg+) Strict Type II Penalty**: Any contender ($O_i \le 6.0$) in a verified $1800\text{m}+$ race with $\ge +12\text{kg}$ is unconditionally Type II ($\Delta \theta_i \in [-0.12, -0.20], \delta^{\text{place}}_i \in [-0.10, -0.15]$, **clamp $w_{r,i} \le 0.15$**, barred from 1st-place anchor); boost rival lean-trim (`-8kg to +2kg`) stalkers by $+0.06\text{ to }+0.12$.
      - **JRA Contender Summer/Autumn-Return Weight-Loss Guard**: Proven JRA contenders shipping to regional `Jpn2/Jpn3` off a 2–4 month layoff at `-10kg to -18kg` default to `Type I/Neutral` ($\Delta \theta_i \in [-0.03, +0.02], \delta^{\text{place}}_i \ge +0.08$) unless emaciation/sweating is noted.
      - **Dirt-Grade (`Jpn1–Jpn3`) JRA Top-Favorite Protection & Local Top-Rider 3rd-Place Anchor (`交流重賞JRA上位人気保護＆南関地元トップ騎手3着アンカー` — `Patch N3`)**: In `Jpn1–Jpn3` races, **always protect Top-2 JRA market favorites ($O_i \le 4.5$, lacking `+12kg+` Type II gain) inside `◎` Core connections** so JRA class dominance is never missed; simultaneously, when `#3/#4` JRA horses carry any flaw, grant $\delta^{\text{place}}_i \in [+0.14, +0.22]$ to course-proven local runners ridden by Nankan top riders (`矢野・御神本・笹川・吉原`) for 2nd/3rd slots (`◎◯ JRA − ▲☆ 南関地元`).
      - **JRA Transfer 1st Run (`転入初戦`) & Untested Distance Extension Cap**: Always expand $\sigma_i^2$ for transfer 1st runs; cap `fFund <= 32%–35%` and clamp $w_{r,i} \le 0.15$ for untested $\ge +400\text{m}$ / $\ge 2400\text{m}$ favorites off slow sprint trials.
      - **Prep-Race Bounce-Back**: Restore $\Delta \theta_i \in [+0.12, +0.22], \delta^{\text{place}}_i \in [+0.10, +0.18]$ and clamp $w_{r,i} \le 0.15$ for single-digit-odds prep flops returning with a `-4kg to -8kg` lean trim or favorable pace shift.

### Step 2: Positional Micro-Simulation, 3-Race Intraday Bias Guard, 2-Stage Benter Fusion (`Patch N1`) & Exact Plackett-Luce

1.  **Gate-to-4C Positional Micro-Simulation & Strict 3-Race Intraday Bias Guard**:
      - Simulate `発馬 → 1角 → 3-4角 → 直線進路` across **3 to 4 MECE scenarios** ($\sum_s \pi_s^{\text{post}} = 1.00$), including Tail-Risk/Shock ($\pi_{\text{shock}} \in [10\%, 20\%]$).
      - Update $\pi_s^{\text{post}}$ from same-day earlier races (`1R〜直前R`) with strict consistency caps: **$\ge 3$ consistent pace-matched races ($\pm 10\%\text{–}20\%$)**, **2 consistent races ($\pm 6\%\text{–}10\%$)**, **$< 2$ races or pace mismatch ($\le \pm 5\%$)**.
2.  **2-Stage Benter Bayesian Fusion & Extreme-Longshot Anchor Cap (`Patch N1`)**:
      - **Stage 1 (Odds-Blind)**: Apply variance attenuation $\tilde{\theta}^{\text{fund}}_{i,s} = \theta^{\text{fund}}_{i,s} / \sqrt{1 + 0.304\sigma_i^2}$ to compute fundamental win probability `fFund` ($f^{\text{fund}}_i$).
      - **Stage 2 (Adaptive Market Fusion)**: Compute FLB Power de-vigged $q_i = (1/O_i)^\gamma / \sum_k (1/O_k)^\gamma$ ($\gamma \in [1.05, 1.15]$) and pool via $w_{r,i}$ ($0.35\text{–}0.48$ baseline; $0.45\text{–}0.52$ high-opacity C2–C3/transfer/juvenile; $0.28\text{–}0.38$ A1–B2/DG mispricings; keep $w_{r,i} \ge 0.28$ on tight-oval inner-gate Top-2 favorites per Patch N2; **asymmetric clamp $w_{r,i} \le 0.15$** on `1800m+ +12kg+` Type II favorites, untested-distance favorites, and prep bounce-back horses): $$\theta^{\text{post}}_{i,s} = (1 - w_{r,i})\tilde{\theta}^{\text{fund}}_{i,s} + w_{r,i} \ln q_i, \qquad \theta^{\text{post},(2,3)}_{i,s} = \theta^{\text{post}}_{i,s} + \delta^{\text{place}}_i$$
      - **Extreme-Longshot Anchor Cap (`単勝50倍超のCore中核禁止・f<=6%上限`)**: Unless backed by indisputable `F`-level physical discontinuity, cap any runner trading at **$O_i \ge 50.0\text{x}$** to **`f <= 6.0%`** and limit its mark to `△ / ☆`, prohibiting promotion into `◎ / ◯ / ▲` Core nucleus slots.
      - Compute exact full-field Stage-Adjusted Plackett-Luce probabilities across ALL $N$ active runners, outputting **Fused Posterior Win Probability into `f` ($p_i$)**, Odds-Blind probability into `fFund`, and applied weight into `wUsed`. Verify strict conservation: $\sum f = 100.0\%, \sum \text{top2} = 200.0\%, \sum \text{top3} = 300.0\%$, and compute **$M_3 = p_{(1)} + p_{(2)} + p_{(3)}$**.

### Step 3: Maximum Hit-Rate Core Shield, Mandatory `◎` Connection, Auto-Pass / 2-Line Compression (`Patch N1`) & Counterfactual Self-Audit

Default strategy profile is **`hit_rate_max`** (`的中率最大化モード`; switch to `high_roi` only when requested):

  - **Pivot & Mandatory `◎`-Top-Contender Connection (`飛び石結線禁止＆市場1〜2人気強制Core結線則`)**:
      - **`Single-Pivot`**: Only when $P(\text{Top 3}_{\text{◎}}) \ge 62\%$ (`high_roi`: $\ge 52\%, p_{\text{◎}}-p_{\text{◯}} \ge 4.0\%$) with NO flaw.
      - **`Dual-Pivot` (3-Node Triangle Core — Default)**: ALWAYS connect **`◎` directly to the Top 2–4 highest Posterior $P(\text{Top 3}_i)$ contenders** AND **never exclude a Top-2 market favorite ($O_i \le 5.0$, lacking `+12kg+` Type II flaw) from `◎`'s direct Core connections even if ranked 4th (`☆`)**, plus `○−▲` fallback.
  - **Single-Longshot Stake Cap ($\le 30\%$)**: Combined outlay across ALL pools containing any single longshot (`☆`, $O_i \ge 10.0$) MUST NOT exceed **`30%`** of total budget (`3,000円 / 10,000円`).
  - **Drop-Buffered Anti-Torigami Dutching Core Shield (`70%–80%`, `11,500–12,500 JPY` Target) & Heavy-Favorite 2-Line Compression (`Patch N1`)**:
      - Size Core Wide/Quinella(/Place) stakes targeting **`11,500–12,500 JPY` payout on a single Core hit** (per `10,000 JPY` baseline) to survive `-15% to -20%` late NAR pool compression.
      - **Heavy-Favorite ($O_{\text{◎}} \le 2.0\text{x}$) 2-Line Core Compression**: Whenever `◎` trades at $O_{\text{◎}} \le 2.0\text{x}$ and valid mid-longshot partners ($O_j \ge 6.0\text{x}$) keep Core synthetic odds $\ge 1.35\text{x}$, **prohibit 4-Wide dispersion** and compress Core strictly to **2 lines** to protect break-even return.
      - Alpha Booster (`20%–30%`): positive-edge `馬連`, `馬単`, compact `3連複` (verify exact counts $3M+1$ / $5M+4$), or capped `☆` Wide.
  - **Auto-Pass Discipline & Inclusion-Exclusion Thresholds (`Patch N1`)**:
      - **Mandatory Structural Auto-Pass**: Immediately enforce **`rank: "Pass"` and `pivotType: "Pass"`** whenever ANY of the following holds:
          1. **Core Synthetic Odds $< 1.35\text{x}$** (even after 2-line compression).
          2. **Small Field ($\le 8$ active runners)** with Core Wide average odds $< 3.0\text{x}$ OR both Top-2 favorites $\le 2.5\text{x}$.
          3. **NAR Dominant-Favorite Compression**: Top favorite **$O_{\text{fav}} \le 1.6\text{x}$** (or $O_{\text{fav}} \le 2.2\text{x}, p_{\text{fav}} \ge 50\%$ with no flaw) AND Core Wide average odds $< 2.8\text{x}$.
      - Require exact disjoint-state **`hitRate >= 60.0%`** (`>= 55.0%` in 14–16 runner full-gate NAR races), **`breakEvenRate >= 45.0%`**, **`expectedRoi >= 102.0%`** (`>= 105.0%` pre-market), and `-15%` stress ROI `>= 90.0%`; otherwise set `rank: "Pass"`.
  - **Counterfactual Self-Audit**: Internally verify (a) `◎` failure mode & `○−▲` coverage, (b) faded favorite comeback path, and (c) conservation + 50x+ cap + Core synthetic odds $\ge 1.35\text{x}$ + single-longshot $\le 30\%$ + exact Trio counts before emitting JSON.

### Step 4: App-Optimized Backward-Compatible JSON Schemas

All existing keys are preserved verbatim for zero-breakage PWA compatibility; new v7.1 fields (`coreSyntheticOdds` optional) are additive. Output **ONLY a single valid JSON object** when invoked by the automated pipeline.

#### Mode A: `スクリーニング` (Venue Batch Screening JSON)

```json
{
  "date": "YYYY-MM-DD",
  "venue": "大井",
  "strategyProfile": "hit_rate_max",
  "trackBias": {
    "going": "良",
    "dirtMoisture": "4.2%",
    "sandDepth": "10cm",
    "intradayBiasConsistentR": 3,
    "summary": "ナイター良・3R一致で外3〜5頭目有利"
  },
  "races": [
    {
      "raceNumber": 11,
      "name": "サンタアニタT",
      "surfaceDist": "ダ1600m",
      "postTime": "20:10",
      "rank": "S | A | B | Pass",
      "skill": "app-bayesian-nar",
      "pivotType": "Single-Pivot | Dual-Pivot | Pass",
      "nLead": 4,
      "m3": 54.8,
      "coreSyntheticOdds": 1.74,
      "expectedRoi": 116.5,
      "hitRate": 62.4,
      "breakEvenRate": 53.0,
      "summary": "35字以内のM3・合成オッズ・判定根拠"
    }
  ]
}
```

#### Mode B: `標準` (1-Hour-Before Single-Race Prediction JSON)

Evaluate **all $N$ active declared runners internally** (excluding scratches). Output marked contenders (`◎◯▲△☆`) + notable faded favorites (`消`)—or **all $N$ runners if requested by the app prompt**—with `tailSummary` verifying $\sum f = 100.0\%$ and $\sum \text{top3} = 300.0\%$:

```json
{
  "raceId": "202611184411",
  "venue": "大井11R",
  "name": "サンタアニタT",
  "surfaceDist": "ダ1600m",
  "postTime": "20:10",
  "skill": "app-bayesian-nar",
  "strategyProfile": "hit_rate_max",
  "rank": "S | A | B | Pass",
  "pivotType": "Single-Pivot | Dual-Pivot | Pass",
  "nLead": 4,
  "wR": 0.40,
  "m3": 54.8,
  "coreSyntheticOdds": 1.74,
  "intradayBiasConsistentR": 3,
  "expectedRoi": 116.5,
  "hitRate": 62.4,
  "breakEvenRate": 53.0,
  "scenario": "ナイター含水率・当日3R一致バイアス・3〜4MECEシナリオ要約(80字以内)",
  "horses": [
    {
      "mark": "◎ | ◯ | ▲ | △ | ☆ | 消",
      "role": "最安定Top-3軸 | 双頭対抗軸 | 南関Top騎手3着Anchor | 外枠大型先行 | 危険人気馬",
      "num": 12,
      "name": "馬名",
      "style": "逃 | 先 | 差 | マ",
      "f": 24.8,
      "fFund": 27.0,
      "q": 18.0,
      "wUsed": 0.40,
      "top2": 44.5,
      "top3": 60.2,
      "odds": 4.5,
      "tags": ["F:大井外1600好績", "H:2段階融合軸+0.14"],
      "comment": "45字以内のF/H核心根拠"
    }
  ],
  "tailSummary": { "count": 8, "sumF": 9.8, "sumTop3": 28.4 },
  "coreConnections": [[12, 7], [12, 3], [12, 9], [7, 3]],
  "portfolioRules": {
    "coreRatio": 0.76,
    "coreLineCap": 4,
    "dutchTargetReturn": 11800,
    "singleLongshotCapPct": 0.30,
    "maxLongshotAllocPct": 0.20
  },
  "tickets": [
    {
      "zone": "Core",
      "type": "ワイド | 馬連 | 馬単 | 3連複F | 3連単F",
      "comb": "12 - 7",
      "points": 1,
      "share": 0.28,
      "odds": "4.3倍",
      "desc": "25字以内の根拠"
    }
  ],
  "counterfactualAudit": "◎破綻時の○-▲防衛状態と消し人気馬の復活条件(60字以内)",
  "triggers": ["直前馬体重(1800m+の+12kg+ Type II警戒)・-30%急落検知(40字以内)"]
}
```

#### Mode C: `トリプル馬単` (Nankan 4-Track Asymmetric Probability-Shell Exacta JSON — `Patch N4`)

Strictly target **Nankan 4-track (`大井・川崎・船橋・浦和`) final 3 races (`10R, 11R, 12R`)**. Output `legs` (2-Stage Fused `f`, `fFund`, `q`, `top2`, and top Exacta pairs `exactaPairs`) plus asymmetric orthogonal `shellTickets` (`T1_Core` tightening 1st-place to Top 1–2 while expanding 2nd-place to Top 3–5, and disjoint `T2_Wing` for upset 1st-place coverage, scaled in `50円` units) and joint `hitRate` / `expectedRoi`.

#### Mode D: `事後検証` (Post-Race Audit & Skill Patch JSON)

Output `auditSummary`, 3-factor decomposition (`scenarioError` including intraday-bias overreaction & verified real-distance check, `ratingError` including 1800m+ `+12kg+` / tight-oval inner-gate Top-2 fav soft cap / 50x+ cap / JRA DG fav protection & Nankan local anchor check, and `portfolioError` including `◎` connection leaks, Auto-Pass `<1.35x` / `<=8` runners / `<=1.6x` dominant-fav audit, single-longshot $>30\%$, and late-drop Torigami audit), and `skillPatch` (`targetSkill`, `targetVersion`, `moduleName`, `patchRule`).

## Gotchas

  - Never output a betting rank without inspecting all $N$ active declared runners (excluding scratches), never run flat-dirt modeling on Ban'ei Obihiro (`ばんえい`), never assume a default `1600m` distance without verifying official distance, and never confuse past-race CSV odds with live market odds.
  - Never hard-fade (`消`) or omit from `◎` Core connections a Top-2 market favorite ($O_i \le 4.5$) drawn in tight-oval NAR Frames 1–2 (cap penalty at `-0.08 to -0.10`, keep $w_{r,i} \ge 0.28$), and waive the inner kickback penalty on wet/sloppy $\le 1200\text{m}$ sprints.
  - Never promote an extreme longshot ($O_i \ge 50.0\text{x}$) into `◎ / ◯ / ▲` or above `f = 6.0%` without indisputable `F`-level physical discontinuity.
  - Always enforce `rank: "Pass"` when Core Wide synthetic odds are `< 1.35x`, active field size is `<= 8` with compressed odds, or an NAR dominant favorite ($O_{\text{fav}} \le 1.6\text{x}$, avg Core Wide `< 2.8x`) collapses returns; when $O_{\text{◎}} \le 2.0\text{x}$ is playable, compress Core to 2 lines instead of 4.
  - Always clamp $w_{r,i} \le 0.15$ on verified `1800m+ +12kg+` Type II favorites, untested-distance favorites, and prep-bounce-back contenders.
  - Never shift intraday scenario weights $\ge 10\%$ from fewer than 3 pace-consistent earlier races (`2R一致は±6〜10%`, `1R/不一致は±5%上限`).
  - Always lock `トリプル馬単` strictly to Nankan 4 tracks (`大井・川崎・船橋・浦和 10R–12R`), never omit direct `◎` Core links to Top 2–4 contenders / Top-2 market favorites (`飛び石結線禁止`), never allocate $> 30\%$ to any single longshot (`☆`), and always size Core Dutching to `11,500–12,500 JPY` per `10,000 JPY` baseline to survive `-15% to -20%` late NAR pool compression.
  - Always output valid, parseable JSON without conversational filler in app pipeline mode.
