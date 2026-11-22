---
name: app-bayesian-nar
description: App-dedicated copy of bayesian-nar (v7.0 Neon Maximum Hit-Rate Edition) for the JRA/NAR Racing AI PWA and 1-hour-before pipeline. Executes mandatory full-field evaluation, 2-Stage Benter Bayesian Fusion (fFund pooled with FLB de-vigged q via adaptive wR), 3-race-consistent intraday bias guard, full-field exact Plackett-Luce, confrontation graph, positional micro-simulation, rule-stacking soft clamp, counterfactual self-audit, NAR dirt moisture/sand-depth/sloppy-dual-regime/outer-G-winner/tight-oval-closer/1800m+ heavy-gain/Nankan-DG-local-anchor physics, dominant-favorite Pass guard, mandatory ◎-top-contender connection, single-longshot <=30% cap, Drop-Buffered Anti-Torigami Dutching Core Shield (70-80%, 11,500-12,500 JPY target, >=60% hit rate, >=45% break-even), and Triple Umatan optimization, outputting backward-compatible compact JSON for Screening, 1-Hour-Before Prediction, Triple Umatan, and Post-Race Skill Patch generation.
---
# App Bayesian NAR Local Horse Racing (v7.0 — Neon Maximum Hit-Rate JSON Edition)

Autonomous hierarchical Bayesian analysis system specialized for **Japanese Local Horse Racing (地方競馬: 南関東4場 [大井・川崎・船橋・浦和] および全国NAR・ダートグレード競走)** dedicated to the **Racing AI App (PWA) and automated 1-hour-before GitHub Actions pipeline**. This is the app-dedicated copy of `bayesian-nar` (**v7.0 Neon Maximum Hit-Rate & Deep-Reasoning Edition**), synchronizing 100% of its mandatory full-field gate, 2-Stage Benter Bayesian Fusion (with asymmetric $w_{r,i} \le 0.15$ hazard/distortion clamp), 3-race-consistent intraday bias guard, full-field exact Plackett-Luce, confrontation graph, gate-to-4C positional micro-simulation, rule-stacking soft clamp, NAR dirt/venue/weight physics, mandatory `◎`-top-contender connection, single-longshot $\le 30\%$ cap, Drop-Buffered Anti-Torigami Dutching Core Shield (`11,500–12,500 JPY` target payout), Dominant-Favorite Pass discipline, Counterfactual Self-Audit, and Probability-Shell Triple Umatan (`トリプル馬単`) optimization—while outputting **backward-compatible compact JSON** so the browser PWA can dynamically scale allocations across any user budget without extra API calls.

## When to Use

- **Batch Screening (`スクリーニング`)**: Filtering Nankan / NAR cards using **Top-3 Posterior Mass ($M_3$)**, exact hit rate, break-even probability, and Expected ROI into `S` (勝負), `A` (好機), `B` (標準), or `Pass` (見送り: トリガミ懸念の一強レースやカオス戦).
- **1-Hour-Before Automated Prediction (`発走1時間前本予想`)**: Generating full-field 2-Stage Benter Fused Plackett-Luce probabilities (`f`, `fFund`, `q`, `wUsed`, `top2`, `top3`, `mark`, `role`, `tags`), `coreConnections`, Drop-Buffered Anti-Torigami `portfolioRules`, `tickets`, and `counterfactualAudit` in compact JSON.
- **Triple Umatan Optimization (`トリプル馬単`)**: Generating 2-Stage Fused 1st/2nd-place Exacta probabilities and Probability-Shell orthogonal ticket sets (Core Shell + Wing Shell) across the final 3 Nankan legs (`10R, 11R, 12R`) for `50円` unit dynamic scaling.
- **Post-Race Audit & Skill Patch Generation (`事後検証・スキル改訂パッチ生成`)**: Decomposing NAR results across 3 factors and outputting an actionable skill patch.

## Steps

### Step 0: Mandatory Full-Field Data Gate (`全頭取得必須ゲート`)

- **No Partial-Field Prediction**: Before computing probabilities or assigning ranks/tickets, inspect **all $N$ declared runners** (gate, horse number, name, sex/age, carried weight & apprentice claim `▲☆◇★`, jockey, trainer/affiliation, live odds, and official horse weights/diffs once announced ~50–60 min pre-post). NEVER leave uninspected horses in an unchecked residual bucket.
- **Hybrid Auto-Fetch**: When invoked with search enabled and partial/missing inputs, automatically gather missing full-field entries, latest live odds, official horse weights, official NAR moisture/sand depth/night conditions, and same-day earlier race results (`1R〜直前R` passing orders, inner-dead-sand status, times). Never fabricate unpublished weights or odds; mark missing items as `未発表` in `triggers`.

### Step 1: Evidence Taxonomy (F / E / H), Confrontation Graph & NAR Track/Venue/Weight Physics

Classify all inputs into **`F` (Verifiable Fact)**, **`E` (Validated Effect)**, or **`H` (Heuristic / Candidate Prior)** on a dimensionless Plackett-Luce logit scale ($\theta_i \in \mathbb{R}$, baseline $0.00$). Internally construct a **Transitive Confrontation Graph** (direct meetings, 1-hop shared opponents, weight diffs, same-day class clock comparisons). Bundle overlapping positional switches into $\le +0.16$ and enforce the **global soft clamp ($|\sum \Delta \theta_i| \le 0.45$, $\delta^{\text{place}}_i \in [-0.30, +0.25]$)** unless overridden by clear `F`-level discontinuity.

1. **Moisture ($m_{\text{dirt}}$), Sand Depth & Sloppy-Track Dual Regime**:
   - **Dry Power Dirt ($m_{\text{dirt}} < 3.0\%$ / deep white sand)**: Boost power/outer sustained runners ($+0.05\text{ to }+0.10$); penalize kickback-fragile inside draws ($-0.06\text{ to }-0.12$).
   - **Sloppy/Heavy Track ($m_{\text{dirt}} \ge 10.0\%$): (i) Outer Large-Frame Stalker Boost**: Upgrade large-framed speed/stalker types ($\ge 500\text{kg}$, especially with `-2kg to -10kg` Type I trim) in **Frames 6–8** securing a clean 2nd–4th outside position ($\Delta \theta_i \in [+0.08, +0.16], \delta^{\text{place}}_i \in [+0.06, +0.12]$). **(ii) Extended-Distance Sloppy Attrition ($\ge 2000\text{m}$)**: Do not penalize light-framed horses ($\le 450\text{kg}$); if entering with a `-4kg to -8kg` trim and local stamina, boost $\Delta \theta^{(1)}_{i,\text{attrition}} \in [+0.12, +0.22]$.
   - **Outer Clean-Air Lead Steal & JRA Multi-Grade Winner Immunity**: In Dirt Grade races (1800m–2000m), even on `良〜稍重`, if a proven JRA multi-grade winner draws **Frames 7–8** and can sweep to an unbothered lead or outside 2nd, grant $\Delta \theta^{(1)}_i \in [+0.10, +0.16]$, waive `+200m` extension penalties, and do not over-penalize `57–58kg` base weights.
   - **Inner Deep Sand (`イン死に馬場`)**: When confirmed by intraday consistency guard, penalize rail hugging ($-0.08\text{ to }-0.15$) and boost paths 3–5 ($+0.06\text{ to }+0.12$).
2. **Nankan 4-Track & Regional Geometry**:
   - **大井 (Right)**: Outer loop (`1200/1400/1800/2000m`, 386m stretch) aids outer stalkers/closers ($+0.06\text{ to }+0.12$). Inner loop (`1500/1600m`, 286m stretch) favors Frames 1–4 speed ($+0.08\text{ to }+0.12$).
   - **川崎 (Left, 300m stretch)**: Sharp hairpin turns; `900m/1600m` favor Frames 1–3 gate speed ($+0.08\text{ to }+0.14$).
   - **船橋 (Left, 308m stretch, Banked Spiral Turns)**: Aids outer stalkers/makuri in Frames 5–8 ($+0.08\text{ to }+0.14$).
   - **浦和 (Left, 220m stretch) & Tight-Oval Pace-Collapse Nankan Top-Rider 3rd-Place Exemption**: Top 3 at 3C–4C is critical ($+0.10\text{ to }+0.16$); Frame 1 slow breakers face boxed-in risk ($\delta^{\text{place}}_i \in [-0.08, -0.15]$, clamp $w_{r,i} \le 0.15$ if favorite). However, when $\pi_{\text{collapse}} \ge 30\%$, grant $\delta^{\text{place}}_i \in [+0.12, +0.20]$ to proven Nankan closers ridden by Nankan top riders (`矢野貴之・御神本訓史・笹川翼・吉原寛人`) for 2nd/3rd coverage.
   - **6-Corner Middle/Long-Distance (笠松・名古屋・園田・金沢・川崎2100m)**: Enforce forward-retention scenario floor $\pi_{\text{forward}} \ge 35\%\text{–}40\%$.
3. **Weight Rules, Prep Bounce-Back, Nankan DG Local Anchor & Transfer/Distance Caps**:
   - **1800m+ Heavy-Gain (+12kg+) Strict Type II Penalty**: Any contender ($O_i \le 6.0$) in an $1800\text{m}+$ race with $\ge +12\text{kg}$ is unconditionally Type II ($\Delta \theta_i \in [-0.12, -0.20], \delta^{\text{place}}_i \in [-0.10, -0.15]$, **clamp $w_{r,i} \le 0.15$**, barred from 1st-place anchor); boost rival lean-trim (`-8kg to +2kg`) stalkers by $+0.06\text{ to }+0.12$.
   - **JRA Contender Summer/Autumn-Return Weight-Loss Guard**: Proven JRA contenders shipping to regional `Jpn2/Jpn3` off a 2–4 month layoff at `-10kg to -18kg` default to `Type I/Neutral` ($\Delta \theta_i \in [-0.03, +0.02], \delta^{\text{place}}_i \ge +0.08$) unless emaciation/sweating is noted.
   - **JRA Transfer 1st Run (`転入初戦`) & Untested Distance Extension Cap**: Always expand $\sigma_i^2$ for transfer 1st runs; cap `fFund <= 32%–35%` and clamp $w_{r,i} \le 0.15$ for untested $\ge +400\text{m}$ / $\ge 2400\text{m}$ favorites off slow sprint trials.
   - **Prep-Race Bounce-Back**: Restore $\Delta \theta_i \in [+0.12, +0.22], \delta^{\text{place}}_i \in [+0.10, +0.18]$ and clamp $w_{r,i} \le 0.15$ for single-digit-odds prep flops returning with a `-4kg to -8kg` lean trim or favorable pace shift.
   - **Nankan DG Local Top-Rider 3rd-Place Anchor**: In South Kanto `Jpn1–Jpn3` races when `#3/#4` JRA horses carry flaws, grant $\delta^{\text{place}}_i \in [+0.14, +0.22]$ to course-proven local runners ridden by Nankan top riders (`矢野・御神本・笹川・吉原`) for 2nd/3rd slots (`◎◯ JRA − ▲☆ 南関地元`).

### Step 2: Positional Micro-Simulation, 3-Race Intraday Bias Guard, 2-Stage Benter Fusion & Exact Plackett-Luce

1. **Gate-to-4C Positional Micro-Simulation & Strict 3-Race Intraday Bias Guard**:
   - Simulate `発馬 → 1角 → 3-4角 → 直線進路` across **3 to 4 MECE scenarios** ($\sum_s \pi_s^{\text{post}} = 1.00$), including Tail-Risk/Shock ($\pi_{\text{shock}} \in [10\%, 20\%]$).
   - Update $\pi_s^{\text{post}}$ from same-day earlier races (`1R〜直前R`) with strict consistency caps: **$\ge 3$ consistent pace-matched races ($\pm 10\%\text{–}20\%$)**, **2 consistent races ($\pm 6\%\text{–}10\%$)**, **$< 2$ races or pace mismatch ($\le \pm 5\%$)**.
2. **2-Stage Benter Bayesian Fusion for NAR**:
   - **Stage 1 (Odds-Blind)**: Apply variance attenuation $\tilde{\theta}^{\text{fund}}_{i,s} = \theta^{\text{fund}}_{i,s} / \sqrt{1 + 0.304\sigma_i^2}$ to compute fundamental win probability `fFund` ($f^{\text{fund}}_i$).
   - **Stage 2 (Adaptive Market Fusion)**: Compute FLB Power de-vigged $q_i = (1/O_i)^\gamma / \sum_k (1/O_k)^\gamma$ ($\gamma \in [1.05, 1.15]$) and pool via $w_{r,i}$ ($0.30\text{–}0.45$ baseline; $0.40\text{–}0.50$ high-opacity C2–C3/transfer/juvenile; $0.25\text{–}0.35$ high-transparency A1–B2/DG mispricings; **asymmetric clamp $w_{r,i} \le 0.15$** on `1800m+ +12kg+` Type II favorites, untested-distance favorites, Frame 1 kickback traps, and prep bounce-back horses):
     $$\theta^{\text{post}}_{i,s} = (1 - w_{r,i})\tilde{\theta}^{\text{fund}}_{i,s} + w_{r,i} \ln q_i, \qquad \theta^{\text{post},(2,3)}_{i,s} = \theta^{\text{post}}_{i,s} + \delta^{\text{place}}_i$$
   - Compute exact full-field Stage-Adjusted Plackett-Luce probabilities across ALL $N$ runners, outputting **Fused Posterior Win Probability into `f` ($p_i$)**, Odds-Blind probability into `fFund`, and applied weight into `wUsed`. Verify strict conservation: $\sum f = 100.0\%, \sum \text{top2} = 200.0\%, \sum \text{top3} = 300.0\%$, and compute **$M_3 = p_{(1)} + p_{(2)} + p_{(3)}$**.

### Step 3: Maximum Hit-Rate Core Shield, Mandatory `◎` Connection, Pass Guard & Counterfactual Self-Audit

Default strategy profile is **`hit_rate_max`** (`的中率最大化モード`; switch to `high_roi` only when requested):

- **Pivot & Mandatory `◎`-Top-Contender Connection (`飛び石結線禁止則`)**:
  - **`Single-Pivot`**: Only when $P(\text{Top 3}_{\text{◎}}) \ge 62\%$ (`high_roi`: $\ge 52\%, p_{\text{◎}}-p_{\text{◯}} \ge 4.0\%$) with NO flaw.
  - **`Dual-Pivot` (3-Node Triangle Core — Default)**: ALWAYS connect **`◎` directly to the Top 2–4 highest Posterior $P(\text{Top 3}_i)$ contenders** (never omitting a Top-3 market favorite with $P(\text{Top 3}_i) \ge 35\%$ and no Type II/physical flaw) plus `○−▲` fallback.
- **Single-Longshot Stake Cap ($\le 30\%$)**: Combined outlay across ALL pools containing any single longshot (`☆`, $O_i \ge 10.0$) MUST NOT exceed **`30%`** of total budget (`3,000円 / 10,000円`).
- **Drop-Buffered Anti-Torigami Dutching Core Shield (`70%–80%`, `11,500–12,500 JPY` Target)**:
  - Size Core Wide/Quinella(/Place) stakes targeting **`11,500–12,500 JPY` payout on a single Core hit** (per `10,000 JPY` baseline) to survive `-15% to -20%` late NAR pool compression.
  - Alpha Booster (`20%–30%`): positive-edge `馬連`, `馬単`, compact `3連複` (verify exact counts $3M+1$ / $5M+4$), or capped `☆` Wide.
- **Inclusion-Exclusion Thresholds & Dominant-Favorite Pass Guard**: Require exact disjoint-state **`hitRate >= 60.0%`** (`>= 55.0%` in 14–16 runner full-gate NAR races), **`breakEvenRate >= 45.0%`**, **`expectedRoi >= 102.0%`** (`>= 105.0%` pre-market), and `-15%` stress ROI `>= 90.0%`. When an odds-on favorite ($O_{\text{fav}} \le 2.2, p_{\text{fav}} \ge 50\%$) has no flaw and compressed odds prevent Anti-Torigami Dutching (`< 4.0x`), strictly enforce `rank: "Pass"` and `pivotType: "Pass"`.
- **Counterfactual Self-Audit**: Internally verify (a) `◎` failure mode & `○−▲` coverage, (b) faded favorite comeback path, and (c) conservation + single-longshot $\le 30\%$ + exact Trio counts before emitting JSON.

### Step 4: App-Optimized Backward-Compatible JSON Schemas

All existing v6 keys are preserved verbatim for zero-breakage PWA compatibility; new Neon v7.0 fields are additive. Output **ONLY a single valid JSON object** when invoked by the automated pipeline.

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
      "expectedRoi": 116.5,
      "hitRate": 62.4,
      "breakEvenRate": 53.0,
      "summary": "35字以内のM3・的中率・判定根拠"
    }
  ]
}
```

#### Mode B: `標準` (1-Hour-Before Single-Race Prediction JSON)

Evaluate **all $N$ declared runners internally**. Output marked contenders (`◎◯▲△☆`) + notable faded favorites (`消`)—or **all $N$ runners if requested by the app prompt**—with `tailSummary` verifying $\sum f = 100.0\%$ and $\sum \text{top3} = 300.0\%$:

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
  "wR": 0.35,
  "m3": 54.8,
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
      "wUsed": 0.35,
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

#### Mode C: `トリプル馬単` (3-Leg Probability-Shell Exacta JSON)

Output `legs` (`10R, 11R, 12R` with 2-Stage Fused `f`, `fFund`, `q`, `top2`, and top Exacta pairs `exactaPairs`) plus orthogonal `shellTickets` (`T1_Core` and `T2_Wing` disjoint sets scaled in `50円` units) and joint `hitRate` / `expectedRoi`.

#### Mode D: `事後検証` (Post-Race Audit & Skill Patch JSON)

Output `auditSummary`, 3-factor decomposition (`scenarioError` including intraday-bias overreaction check, `ratingError` including 1800m+ `+12kg+` / sloppy dual-regime / Nankan DG local anchor check, and `portfolioError` including `◎` connection leaks, single-longshot $>30\%$, and late-drop Torigami audit), and `skillPatch` (`targetSkill`, `targetVersion`, `moduleName`, `patchRule`).

## Gotchas

- Never output a betting rank without inspecting all $N$ declared runners; never confuse past-race CSV odds with live market odds.
- Always clamp $w_{r,i} \le 0.15$ on `1800m+ +12kg+` Type II favorites, untested-distance favorites, Frame 1 kickback traps, and prep-bounce-back contenders.
- Never shift intraday scenario weights $\ge 10\%$ from fewer than 3 pace-consistent earlier races (`2R一致は±6〜10%`, `1R/不一致は±5%上限`).
- Never omit direct `◎` Core links to Top 2–4 Posterior contenders (`飛び石結線禁止`), never allocate $> 30\%$ to any single longshot (`☆`), and always size Core Dutching to `11,500–12,500 JPY` per `10,000 JPY` baseline to survive `-15% to -20%` late NAR pool compression.
- Always enforce `rank: "Pass"` on dominant-favorite low-yield races ($O_{\text{fav}} \le 2.2, p_{\text{fav}} \ge 50\%$, core odds $< 4.0\text{x}$), and output valid, parseable JSON without conversational filler in app pipeline mode.
