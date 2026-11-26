---
name: bayesian-win5
description: Execute hierarchical Bayesian JRA WIN5 prediction and maximum hit-rate formation optimization across 5 legs for Gemini 4 Neon v11.2 with autonomous 5-leg web data gathering (excluding scratches), 2-Stage Benter Bayesian Fusion (Odds-Blind f_{r,i} pooled with FLB de-vigged market q_{r,i}, w_r=0.55-0.60 for visiting foreign G1 legs, 50x+ extreme-longshot Core cap), Plan C Probability-Shell Multi-Ticket Orthogonal Decomposition (3-4 disjoint IPAT tickets with T1 Core <=45% hard cap, >=3-leg wings, and priority wing allocation for 5.0-15.0x mid-price Rank #4-#6 contenders with inner-pocket Frames 1-3 or Top-3 closing 3F), 3-race-consistent intraday 1R-8R Bayesian bias guard, venue-coupled synchronization, full-field 5-leg softmax, confrontation graph, positional micro-simulation, rule-stacking clamp, counterfactual self-audit, F/E/H classification, 10-module true-winner identification (dry-dirt mandatory Top-4 closer slot, wet-sprint/Top-2-fav dirt inner-gate soft cap, visiting elite foreign G1 vs returning Japanese horse split), difficulty-adaptive budget guidance, post-race audit, and Leg 5 win-hedging.
---

# Bayesian WIN5 (v11.2 — Neon Maximum Hit-Rate Engine)

Autonomous multi-race hierarchical Bayesian probability modeling and combinatorial optimization system specialized for **JRA WIN5** (5 consecutive 1st-place finishes across 5 designated races), engineered to maximize **Gemini 4 Neon's multi-step quantitative reasoning** and **true 5-leg WIN5 hit probability (`WIN5的中率の理論極大化`)** under any given budget, while preserving **concise, high-density output (`重要情報のみに絞った省文字数出力`)**.

## Core Hit-Rate Maximization Architecture (的中率を極大化する5大エンジン)

1.  **2-Stage Benter Bayesian Fusion & Extreme-Longshot Cap (`2段階分離ベイズ融合：オッズ遮断評価 × 市場暗黙情報の適応統合＆50倍超Core中核禁止`)**:
    
      - **Stage 1 (Odds-Blind Fundamental Estimation)**: First compute pure fundamental win probabilities $f^{\text{fund}}_{r,i,s}$ **completely independently of odds/popularity (`オッズ・人気順位の完全遮断`)** via the 10 True-Winner Modules, Transitive Confrontation Graph, and Positional Micro-Simulation—eliminating anchoring bias.
      - **Stage 2 (Calibrated Posterior Pooling for Maximum Hit Rate)**: Pool $f^{\text{fund}}_{r,i,s}$ with FLB Power de-vigged live market probabilities $q_{r,i} = (1/O_{r,i})^{\gamma} / \sum_k (1/O_{r,k})^{\gamma}$ ($\gamma \in [1.05, 1.15]$) in log-odds space to capture unobserved market information (stable feel, minor health cues, late paddock confidence) while retaining physical alpha: $$p^{\text{post}}_{r,i,s} \propto \left(f^{\text{fund}}_{r,i,s}\right)^{w_r} \cdot \left(q_{r,i}\right)^{1 - w_r}$$
      - **Adaptive Model Weight $w_r$ (`局面別適応ウェイト`)**:
          - Default standard leg: $w_r = 0.70$ (Fundamental 70% / Market 30%).
          - Clear `F`-level trap/hazard leg (verified Mod 2 turf-start inner kickback, Mod 4 58kg+ medical/layoff favorite, Mod 9 S-workout outer exemption): raise to **$w_r = 0.80$** so market overreaction/blind spots do not dilute physical edge.
          - Low-information leg (**visiting foreign G1 contender races `外国馬参戦G1`**, 2yo/early-3yo juvenile stakes $n_i \le 2$, multi-month layoff fields, or live smart-money surge $\ge 30\%$ odds drop): lower to **$w_r = 0.55\text{〜}0.60$** so international form-line / private paddock signals priced by the market are absorbed heavily rather than suppressed.
          - **Extreme-Longshot Anchor Cap (`単勝50倍以上のCore中核禁止・勝率6%上限`)**: Unless backed by an indisputable `F`-level physical discontinuity, **cap any runner trading at $O_{r,i} \ge 50.0\text{x}$ at $p_{r,i} \le 6.0\%$** so extreme longshots never displace live Top-3 market or mid-price winners from Core `C`.
          - **Market-Divergence Re-Audit Guard (`乖離監査`)**: If any runner with $q_{r,i} \ge 15\%$ (Top 1–2 market contender) or a well-backed visiting G1 winner ($O_{r,i} \le 10.0$) falls outside the active selection *without* an explicit `F`-level physical hazard (Modules 2, 4, 5, 10), trigger an internal audit before excluding it.
      - **Zero-ROI Distortion Rule (`期待値歪みの排除`)**: Rank and allocate strictly by **Calibrated Posterior Win Probability $p_{r,i} = \sum_s \pi_s p^{\text{post}}_{r,i,s}$** (never replace a higher-$p_{r,i}$ horse with a lower-$p_{r,i}$ longshot for odds appeal).

2.  **Plan C: L1 Log-Loss Probability-Shell Multi-Ticket Orthogonal Decomposition & Mid-Price Wing Priority (`確率シェル分割・T1核上限45%ハードキャップ・3レグ以上直交翼・4〜6番手中穴優先編入則`)**:
    
      - **Theorem**: A single Cartesian formation (`Plan A`) wastes 30–40% of its tickets on low-probability "multi-upset corner cells" while omitting higher-probability single-leg surprises. Defining each horse's **Log-Probability Deficit** $d_{r,i} = \ln(p_{r,(1)} / p_{r,i}) \ge 0$, maximum hit rate under budget $K$ is achieved by buying the **$K$ tuples minimizing total log-loss $\sum_{r=1}^5 d_{r,i_r}$** (a 5D pyramid/L1-simplex, NOT a 5D cube).
      - **IPAT-Ready 3〜4 Disjoint Shell Execution with T1 Core <=45% Hard Cap**: Partition budget $K$ into **3 to 4 strictly mutually exclusive formation tickets ($T_a \cap T_b = \emptyset$)** enterable on JRA IPAT in under 60 seconds:
          - **T1 (`最密核 Core Nucleus` — Hard Cap $\le 45\%$ of budget, i.e., $\le 48\text{点}$ at 10,000 yen; target 30–45%)**: $C_1 \times C_2 \times C_3 \times C_4 \times C_5$ (highest hit-rate density per 100 yen). **Never allow T1 to exceed 45% (48 pts at 10k)**—e.g., do not bloat T1 to 72 points by placing 4 horses in Leg 5 while starving other legs of wings.
          - **T2〜T4 (`直交ウイング Orthogonal Wings`, 55–70% of budget, covering $\ge 3$ distinct legs)**: Use the remaining $\ge 52\text{点}$ (at 10k) to systematically deploy disjoint wings across **at least 3 different legs** (explicitly including the `#3` contender of `Type A` legs when its $p_{r,3} \ge 9.0\%$ and `#4–#6` of `Type B/B+` legs). Each wing expands 1 leg $a$ into $W_a$ ($W_a \cap C_a = \emptyset$) while tightening the other 4 legs to Core Top 1–2 ($C'_r \subseteq C_r$), enforcing strict hierarchical disjointness (T2 uses $W_a$; T3 fixes $a \in C_a$ and uses $W_b$; T4 fixes $a \in C_a, b \in C_b$ and uses $W_c$ or a disjoint venue-bias sweep).
          - **Mid-Price Rank `#4–#6` Priority Wing Allocation (`4〜6番手・単勝5〜15倍帯中穴の直交翼優先編入則`)**: When selecting Wing horses (`W`) for `T2`–`T4`, do NOT blindly pick only the next nominal favorite. **Prioritize `#4–#6` contenders trading in the `5.0x–15.0x` mid-price win-upset band that hold either (a) an inside pocket draw (Frames 1–3) with rail-saving/tactical speed, OR (b) Top-3 Last-3F closing speed (`上がり3F上位`)**—preventing total blind spots when favorite-tier anchors stall in competitive `Type B / G1` legs.
      - **Expected Gain**: Typically increases WIN5 hit rate by **+15% to +25% relative** over Cartesian Plan A at the exact same 10,000-yen budget while eliminating single-leg blind spots.

3.  **Venue-Coupled Bias Scenario Synchronization (`同一開催場バイアス連動チケット同期`)**:
    
      - When 2–3 WIN5 legs run at the same venue (e.g., Kyoto 9R/10R/11R), avoid wasting points on anti-correlated combinations. Align satellite shells (`T3`/`T4`) with coherent venue-bias regimes ($s_2$ Outer-Closer Sweep vs. $s_3$ Fast-Inner Persistence) so coupled capture $\sum_s \pi_s \prod_r F_{r,s}(T_m)$ is maximized.

4.  **Live 1R–8R Intraday Bayesian Posterior Assimilation with 3-Race Minimum Consistency Guard (`当日1R〜8R実績のベイズ同化・最小3戦一貫性ガード`)**:
    
      - Before the WIN5 deadline (10–25 min before Leg 1), run `直前更新` to assimilate **same-day 1R–8R actual winning gates/styles/times** via Bayes' rule ($\pi_s^{\text{live}} \propto \pi_s^{\text{pre}} \cdot L(\text{1R–8R bias} \mid s)$), official horse weights (Type I/II/III), rain/wind shifts, and late smart-money odds drops ($\ge 25\text{〜}30\%$).
      - **3-Race Minimum Consistency Guard (`最小3戦ガード`)**: Never over-react to a single early race (e.g., 1 turf race won by a front-runner). Until **at least 3 same-venue, same-surface (`同一会場・芝/ダ別で3戦以上`)** races confirm a consistent directional bias, **strictly cap any prior scenario weight shift at $|\Delta \pi_s| \le 5\text{pt}$** and **forbid dropping a pre-selected outer closer or inner stalker from Plan C wings based on 1–2 early races alone**. Full Bayesian updating ($|\Delta \pi_s| > 5\text{pt}$) unlocks only when $\ge 3$ same-venue/same-surface races align with corroborating physical telemetry (CV/moisture/wind).

5.  **Difficulty-Adaptive Hit-Rate Efficiency Mode (`開催難易度連動・的中効率ガイド`)**:
    
      - Automatically classify each WIN5 day's structural hit-rate efficiency (`高確度攻め週 [Type S/A ≥ 2]` / `標準週` / `超難解カオス週 [Type S = 0 & Type B/B+ ≥ 4]` / `キャリーオーバー拡張週`) and show both the standard 10,000-yen optimal Plan C and the recommended budget-efficiency guidance.

## Phase 0: Autonomous 5-Leg Web Data Acquisition Protocol (WIN5自動調査・補完ルール)

When the user requests a WIN5 prediction, pre-race update, or post-race audit without pasting full 5-race data, **automatically gather all required `F` (Verifiable Fact) data across all 5 legs via parallel web search batches** before running Steps 1–5—do NOT ask the user to manually paste entry lists or odds.

1.  **Zero-Paste 5-Leg Parallel Auto-Fetch Checklist**:
      - **WIN5 Target Races, Carryover & Market**: All 5 designated races (`開催場・R・レース名・距離・芝/ダート・クラス・ハンデ/定量/別定`), full active declared fields (`枠番・馬番・馬名・性齢・斤量・騎手・調教師・取消/除外`; completely exclude scratched/withdrawn runners before normalization), latest official Win odds & popularity ranks (`最新単勝オッズ・人気・取得時刻JST`), carryover / mega-pool status (`キャリーオーバー有無`), and official horse weights/diffs (`馬体重・増減`, once announced).
      - **Cross-Venue Track Physics & Intraday Telemetry**: For every active venue, JRA official `クッション値`, goal-front & 4-corner `含水率 %`, temporary rail (`A/B/C/Dコース`), official going (`良〜不良`), racecourse weather/rain timing & wind speed/direction (`風速 m/s・風向`), and same-day earlier race results (`1R〜8Rの芝/ダ別勝ち枠・脚質・時計サンプル数`).
      - **Form, Splits & Confrontation Data**: Recent 3–5 starts and exact course/distance records for contenders in each leg (`着順・着差・走破時計・通過順・テン3F/1000m通過・上がり3F・後半2F/1Fラップ・PCI/RPCI・斤量・馬体重・馬場状態・共通対戦相手・次走好走馬`), gate-delay history (`出遅れ歴`), layoff/medical/gelding history (`休養明け・心房細動/鼻出血/骨折明け・去勢明け`), and gear changes (`ブリンカー等`).
      - **Workouts & Pre-Race Cues**: Final and 1-week-prior workout clocks (`坂路/CW/美W 全体時計・後半2F/1Fラップ・加速/減速・併せ馬先着・調教S評価候補・外国馬の芝追い切り評価`) plus intraday paddock notes when running `直前更新`.
      - **Post-Race WIN5 Audit (`事後検証`)**: Official winners/finishing orders, margins, race lap splits, corner passing orders across all 5 legs, and official WIN5 payout & winning ticket count (`払戻金・的中票数`).
2.  **Hybrid Merge with User-Provided Data (`TARGET / JRA-VAN` 併用則)**:
      - When the user supplies TARGET frontier JV / JRA-VAN exports or pasted race tables, treat user-provided facts as primary ground truth and automatically search **only for missing or live-updating items**.
      - **Blind Backtest Guard (`マスク検証モード`)**: If the user explicitly asks for a blind/masked backtest with pasted anonymized data, **strictly disable web search** and evaluate solely from the pasted data (setting $w_r = 1.0$ if odds are omitted, or using only pasted pre-race odds).
3.  **Source Integrity & Unreleased-Data Guard**:
      - Prioritize authoritative sources (JRA公式, netkeiba, weather telemetry, major racing media) and record `{Timestamp(JST), Source}`.
      - **Never fabricate missing data**: Mark unreleased horse weights/live odds explicitly as `未発表（直前更新で確認）`. If live odds are not yet released, run Stage 1 strictly Odds-Blind ($w_r = 1.0$) and label any reference odds as `推定想定オッズ`.

## Neon Deep-Reasoning Protocol & Output Compression (内部厳密演算・出力高密度化ルール)

Execute all multi-leg Bayesian inference and combinatorial optimization internally at 100% mathematical fidelity while keeping the formatted output concise and high-density:

1.  **Full-Field 5-Leg Exact Logit, Softmax & Benter Fusion Tensor (`全5レース×全頭×全シナリオ厳密演算`)**: Internally assign explicit numerical $\theta^{(1)}_{r,i,s}$ and $\sigma_{r,i}^2$ to **every active declared runner ($i = 1 \dots N_r$) across all 5 legs ($r = 1 \dots 5$) and all coupled scenarios ($s = 1 \dots S$)**, compute exact Stage 1 softmax $f^{\text{fund}}_{r,i,s}$, execute Stage 2 adaptive Bayesian pooling with FLB Power de-vigged $q_{r,i}$ (enforcing the 50x+ extreme-longshot cap $p_{r,i} \le 6.0\%$) to obtain $p^{\text{post}}_{r,i,s}$, and normalize so $\sum_{i=1}^{N_r} p_{r,i} = 100.0\%$ in every leg.
2.  **Transitive Confrontation Graph & Race-Level Calibration (`推移的対戦グラフ＆レースレベル補正`)**: Construct an internal pairwise margin graph per leg (direct meetings, 1-hop shared opponents, same-day/same-venue class clock differentials, and next-out winner counts `次走好走数`) adjusted for carried weight ($1\text{kg} \approx 0.15\text{〜}0.20\text{s}$), wide-corner ground loss, and pace bias.
3.  **Gate-by-Gate Positional & Traffic Micro-Simulation (`枠順別位置取り・進路マイクロシミュレーション`)**: Internally simulate `スタート → 1角 → 3-4角 → 直線進路` across **3 to 4 MECE venue-coupled scenarios** ($\sum_s \pi_s = 1.00$), explicitly scoring gate-delay rates, turf-start dry-dirt separation (`見せかけの先行過多`), dirt kickback zones, and boxed-in probabilities $P(\text{box}_{r,i} \mid s)$.
4.  **Mechanism Deduplication & Soft-Clamp Regularization (`重複ルール統合＆総シフト幅クランプ`)**: Bundle overlapping physical heuristics into a single bounded term ($\le \pm 0.16$) and softly clamp total Stage 1 shifts at $|\sum \Delta \theta^{(1)}_{r,i}| \le 0.45$ unless backed by clear `F`-level class/surface discontinuity.
5.  **Cross-Leg Counterfactual Self-Audit & Exact Plan C Disjoint Verification (`5レース横断反実仮想監査＆プランC完全非重複・T1上限45%検算`)**: Internally verify:
      - *(a) Anchor Leg Failure-Mode Check*: For every 1-horse (`Type S`) or Core-only leg, verify its `#1` physically plausible upset sequence is priced into $\pi_s$ and $\sigma_{r,i}^2$—or open a Wing ticket (`T2/T3/T4`) covering it.
      - *(b) Market-Divergence, 50x+ Cap & Mid-Price Wing Audit*: For every runner with $q_{r,i} \ge 15\%$ or visiting G1 winner ($O_{r,i} \le 10.0$) excluded from all shells, verify a concrete `F`-level physical hazard exists; confirm no $O_{r,i} \ge 50.0\text{x}$ longshot sits in Core `C` without `F`-level discontinuity; and verify that `T2`–`T4` wings prioritize `5.0x–15.0x` Rank `#4–#6` contenders with inside-pocket draws (Frames 1–3) or Top-3 closing 3F.
      - *(c) Exact Combinatorial, Disjointness & Hard-Cap Audit*: Verify (i) $\sum_{i=1}^{N_r} p_{r,i} = 100.0\%$ in all 5 legs; (ii) **T1 Core strictly $\le 45\%$ of budget ($\le 48\text{点}$ at 10k)** and **wings expand $\ge 3$ distinct legs**; (iii) pairwise disjointness $T_a \cap T_b = \emptyset$ so total points $= \sum_m |T_m| \le K$; (iv) exact scenario-coupled hit rate $P(\bigcup_m T_m) = \sum_m \sum_s \pi_s \prod_r F_{r,s}(T_m)$ strictly beats Plan A at the same budget; and (v) exact Leg 5 win-hedge math ($B_{\text{hedge},j} = \lceil G_{\text{min}} / O_{5,j} \rceil_{100\text{円}}$).
6.  **Zero Redundant Prose & Strict Concise Output**: Strip all filler paragraphs, formula derivations, and full 16–18 horse tables. Keep per-horse comments under 35 characters (`1行・35字以内`) and summarize unranked tail runners into 1 `その他計` row per leg.

## When to Use

  - The user asks to predict or analyze **JRA WIN5** across 5 target races (Leg 1 to Leg 5)—either from just a date/event name (auto-gathering via Phase 0) or from pasted TARGET/JRA-VAN data.
  - The user wants to maximize **WIN5 hit probability (`的中率最大化`)** under any budget ($B_{\text{WIN5}}$) using optimal multi-ticket probability-shell formations (`Plan C`) vs. Plan A/B.
  - The user asks for a **Pre-Race Diff Update (`直前更新`)** before the WIN5 deadline, auto-fetching live 1R–8R intraday venue bias (subject to the 3-Race Minimum Consistency Guard), official horse weights, weather/wind shifts, late odds surges, and scratches.
  - The user asks for a **Post-Race WIN5 Audit (`事後検証`)**, auto-fetching official results/laps/payouts across all 5 legs and executing a 3-factor + calibration audit.

## Steps

### Step 1: Odds-Blind Evidence Classification (F / E / H), Confrontation Graph & Stage 1 Pure Ability Estimation

Estimate each horse's Stage 1 1st-place log-ability ($\theta^{(1)}_{r,i,s} \in \mathbb{R}$, baseline $0.00$) **completely independently of public win odds or popularity rank (`オッズ・人気順位の完全遮断評価`)**:

  - **`F` (Verifiable Fact)**: Course geometry, turf/dirt start, cushion value (`クッション値`), moisture (`含水率`), temporary rail (`A/B/C/D`), sand depth (`砂厚`), weather/wind, carried weight, horse weight, draw, opening 3F (`テン3F`), individual/race `PCI` & `RPCI`, workout times/laps, and raw past results (`着順・着差・時計・後半2F/1Fラップ・通過順・上がり3F・不利記録・疾病履歴`).
  - **`E` (Validated Effect)**: Empirically validated statistical effects with verified sample size and baseline.
  - **`H` (Heuristic / Prior)**: Pedigree, pace bias, and condition-switch hypotheses. Shrink pedigree priors as starts $n_i$ grow ($\theta_{i,\text{ped}} = \frac{\tau_0}{\tau_0 + n_i}\Delta \theta_{\text{sire}}$), except on first-time surface switches, extreme distance extensions ($\ge 2400\text{m}$), or heavy/Subarctic tracks.
  - **Transitive Confrontation Graph & Race-Level Calibration**: Align direct meetings, 1-hop shared opponents, same-day class clock differentials, and next-out winner counts (`ハイレベル戦3〜5着の再評価`: $+0.06\text{〜}+0.14$ vs. `低レベル戦勝ち割引`: $-0.06\text{〜}-0.12$).
  - **Collinearity Guard & Regularization Clamp**: Bundle overlapping positional factors ($\le \pm 0.16$) and softly clamp total shifts at $|\sum \Delta \theta^{(1)}_{r,i}| \le 0.45$ unless backed by clear `F`-level class/surface discontinuity.

### Step 2: Ten Complete True-Winner Identification Modules (`本当に勝つ馬を見抜く10大完全検算モジュール`)

Evaluate every active runner internally across all 5 legs through all 10 physical, tactical, and conditioning modules (feeding directly into Stage 1 $\theta^{(1)}_{r,i,s}$):

1.  **Pace-Dynamic 4th-Corner Zone, High-Pace Dirt Dual-Closer vs. Turf-Start Dry-Dirt Mandatory Top-4 Closer Slot & High-CV Sprint Outer-Speed Persistence (`先行激化時の前崩れ差し編入・芝発進乾燥ダート「好位ポケット残し＋差し1番手Top4強制確保」＆ 高速芝1200m外枠先行残存モデル`)**:
    
      - Count genuine early-speed horses ($N_{\text{lead}}$: horses with recent 1st-corner pass rank $\le 2$ or aggressive front-running history):
          - **Standard / Slow Pace ($N_{\text{lead}} \le 3$)**: Boost tactical stalkers/leaders positioned within $\le 0.6\text{s}$ at the 4th corner; penalize one-dimensional deep closers.
          - **Contested / High-Pace Cluster ($N_{\text{lead}} \ge 4$ or multiple committed escapers)**: Trigger the **Pace-Collapse Switch ($\pi_{\text{collapse}} \ge 0.35$)**. **Mandatory Closer Slot Rule**: Never fill all selected slots with front-runners/stalkers in an $N_{\text{lead}} \ge 4$ race; **always elevate the `#1` mid-pack/outer-drawn closer (`最速上がり実績のある純差し馬1番手`, especially 4yo ascending or current-class placed closers) into the Top 3–4 (Core or Wing)**.
          - **High-Pace Dirt ($N_{\text{lead}} \ge 5$) Dual-Closer Promotion vs. Turf-Start Dry-Dirt ($\text{Moisture} \le 5.0\%$) Balanced Retention**:
              - In dirt races (1200m–1600m) with $N_{\text{lead}} \ge 5$ on standard/wet dirt or dirt-start courses, front-running favorites face severe collapse risk ($\pi_{\text{collapse}} \ge 0.50$). **Never lock a front-running favorite as a solo anchor (`Type S` / 1頭固定禁止)**; boost both the `#1` and `#2` closers by $+\Delta\theta^{(1)} = +0.14\text{〜}+0.20$.
              - **Turf-Start Dry-Dirt ($\text{Moisture} \le 5.0\%$) Balanced Rule (`好位残し＋差し1番手Top4強制確保`)**: On turf-start dirt courses (Fukushima 1150m, Nakayama/Niigata 1200m, Tokyo/Kyoto/Hanshin 1400m) when dirt moisture is dry ($\le 5.0\%$), a long turf run-up separates early dash speed vertically (`見せかけの先行過多`). **Never fill the Top 3 exclusively with deep closers—AND conversely NEVER fill all 4–5 Core+Wing slots exclusively with front-runners/stalkers when $N_{\text{lead}} \ge 4$**: retain **(a) the top inner/mid-frame (Frames 2–4) 2nd–3rd inside-pocket stalker (`内2〜3番手ポケット好位馬`: $+\Delta\theta^{(1)} = +0.14\text{〜}+0.18$)** AND **(b) the top outer-frame (Frames 7–8) turf-dash stalker**, **AND mandatorily reserve at least 1 slot in the Top 4 (Core or Wing) for the `#1` proven pure closer (`現級連対・最速上がり実績の純差し1番手`)** so an actual front-end meltdown (e.g., 3F $\le 34.5\text{s}$ front-loaded split) is never missed.
          - **High-CV ($\ge 9.6$) Turf 1200m Sprint Speed-Persistence Exception**: In turf 1200m sprints with $\text{CV} \ge 9.6$ (or firm turf moisture $< 12\%$), sprinters with proven top-tier opening 3F speed ($\le 33.2\text{s}$ or Top 2 early speed) in **Frames 6–8** that can clear or sit 2nd without inside pinch receive $+\Delta \theta^{(1)} = +0.12\text{〜}+0.18$ ($\pi_{\text{speed\_persist}} \ge 0.35$).

2.  **Two-Step Trouble Audit, Turf-Start Dirt Outer-Stalker Top-3 Promotion & Dirt Inner-Gate Soft Cap (`前走不利検出・芝スタート7〜8枠先行馬Top3昇格 ＆ ダート内枠1〜2人気ソフトキャップ・重不良短距離免除則`)**:
    
      - **Recent Defeat Trouble Audit**: Audit recent defeats of mid/low-popularity horses (4th–12th favorites) for verifiable physical causes (`F`): Traffic/Boxed In (`直線前壁・どん詰まり`), Track/Draw Bias Inversion (`馬場・枠順バイアス逆行`), or Pace Breakdown Survivor (`ハイペース先行潰れの中で最先着`: $\text{PCI} \le 48.0$, finished within $\le 0.8\text{s}$).
      - **Turf-Start Dirt Inside-Frame Soft Cap, Wet-Sprint Waiver & Frame 7–8 Stalker Top-3 Promotion**: On turf-start dirt courses (Tokyo 1400/1600m, Nakayama 1200m, Kyoto/Hanshin/Chukyo 1400m, Niigata 1200m, Fukushima 1150m):
          - On **重・不良 short-distance dirt ($\le 1200\text{m}$)**, **waive the Frames 1–2 inside kickback penalty ($0.00\text{ to }+0.08$)** for fast-gate / Top-3 market runners.
          - On Good/Dry dirt, strip `Type S` eligibility from Frames 1–4 favorites lacking kickback proof, **but cap the inner-gate penalty at $\Delta\theta^{(1)} = -0.08\text{〜}-0.12$ (never stripping them completely from Core/Wing shells without an explicit `F`-level flaw) when they are Top-2 market favorites ($O_{r,i} \le 4.5$) or 3yo/4yo winning-streak risers**.
          - **Frame 7–8 Stalker/Leader Top-3 Mandatory Promotion**: Grant **$+\Delta\theta^{(1)} = +0.16\text{〜}+0.22$** to tactical leaders/stalkers in **Frames 7–8** that accelerate smoothly on the outer turf strip without kickback. **Never leave the `#1` Frame 7–8 stalker at Rank 5 (`穴候補止め禁止`)—promote it directly into the Top 3**.

3.  **Class-Boundary, 3yo/4yo Class-Standard Breaker & Autumn 3yo Light-Weight / Inner-Frame Ascending Winner Priority (`条件戦クラス基準突破 ＆ 秋期3歳54〜55kg好位馬・最内57kg連勝昇級馬のTop3優先編入`)**:
    
      - Penalize older horses that won slow, unpressured lower-class races (`スロー楽逃げ昇級馬`: $\Delta\theta^{(1)} = -0.12$).
      - **3yo/4yo Ascending Class-Standard Breaker Priority**: In 2-Win/3-Win legs on standard/fast tracks, when a **3yo or 4yo horse** won its previous lower-class race while **clearing both the upper-class average winning time AND the closing 2F lap benchmark (Turf final 2F $\le 22.8\text{s}$ / Dirt final 2F $\le 24.4\text{s}$)**, boost $\Delta\theta^{(1)} = +0.16\text{〜}+0.22$ and **prioritize it into rank `#1–#2`** (attenuate to $+0.08$ if $N_{\text{lead}} \ge 5$ and extending in distance).
      - **Autumn (Oct–Dec) 3yo Light-Weight ($54\text{〜}55\text{kg}$) & Inner-Frame ($57\text{kg}$) Ascending Stalker Priority**: In autumn 3-Win / Listed / Open turf races, **3yo colts/fillies carrying $53\text{〜}55\text{kg}$ with tactical positioning or sharp final-3F acceleration** or **ascending winners on a winning streak drawing Frames 1–2 at $\le 57\text{kg}$ on fast inner/B-rail tracks** receive **$+\Delta\theta^{(1)} = +0.16\text{〜}+0.22$** and must be **elevated into the Top 3–4** above older 58kg+ layoff/prep favorites.
      - **Subarctic Turf (`洋芝：札幌・函館`) & Low-CV Tough Turf ($\text{CV} < 9.0$ / $\text{RPCI} \le 48.5$) Attenuation**: Attenuate fast-track 3yo/4yo clock bonuses by 50% ($\Delta\theta^{(1)} \le +0.06$), and boost runners with proven Subarctic or sustained-pace ($\text{RPCI} \le 48.5$) stamina ($\Delta\theta^{(1)} = +0.12\text{〜}+0.16$) into the Top 3.

4.  **1st-Place Conversion Efficiency, Chronic Silver-Collector Ceiling & 58kg+ Layoff/Medical-Return / Prep Favorite Fade (`シルバーコレクター減点 ＆ 58kg以上病み上がり・長期休養明け人気馬減衰×単騎先行抜擢`)**:
    
      - Separate **1st-place log-ability ($\theta^{(1)}_{r,i,s}$)** from 2nd/3rd-place retention.
      - **Chronic Silver-Collector Ceiling Rule**: Any popular horse with **3+ consecutive 2nd–4th finishes in the current class** or chronic slow starts / hanging (`ソラを使う`) receives **$\Delta\theta^{(1)} = -0.15\text{〜}-0.22$** and is **strictly barred from `Type S`**.
      - **58kg+ Medical-Return / Long-Layoff Favorite Fade in Listed/Open/3-Win**: When a popular older horse ($O_i \le 7.0$) carries **$\ge 58.0\text{kg}$** while returning from a **medical issue (`心房細動明け・鼻出血明け・骨折休養明け`) or a $\ge 6$-month layoff (including its 2nd start back on an inner track)**, **strip `Type S` eligibility**, apply **$\Delta\theta^{(1)} = -0.15\text{〜}-0.20$**, and **never pair two such 58kg+ horses as a 2-horse solo anchor (`2頭軸固定禁止`)**.
      - **G2/G3 Prep-Race G1-Target Favorite Fade vs. Lone-Speed Survivor**: In G2/G3 prep races, when a 1st/2nd favorite carries penalty weight ($\ge 57\text{〜}59\text{kg}$) or returns from a $\ge 3$-month layoff at $+4\text{kg}+$ with a next-race G1 target, **strip `Type S` eligibility**, apply **$\Delta\theta^{(1)} = -0.12\text{〜}-0.18$**, and **elevate the top unbothered front-runner or inside-pocket stalker (`☆_pace`) by $+\Delta\theta^{(1)} = +0.12\text{〜}+0.18$ into the Top 3**.

5.  **Jensen's Inequality Variance Correction & Visiting Elite Foreign G1 vs. Returning Japanese Horse Split (`分散キャップ補正 ＆ 来日欧州・海外G1覇者 vs 海外遠征帰り日本馬の明確分離`)**:
    
      - Apply variance attenuation $\tilde{\theta}^{(1)}_{r,i,s} \approx \theta^{(1)}_{r,i,s} / \sqrt{1 + 0.304 \cdot \sigma_{r,i}^2}$ and the **Anti-Narrowing Rule**:
        1.  **Returning Japanese Horse from Overseas Defeat vs. Visiting Elite Foreign G1 Winner (`海外帰り日本馬減点 vs 来日G1覇者保護`)**:
              - **Returning Japanese horse (`海外遠征大敗明け初戦の日本馬`)** coming off a heavy defeat ($\ge 5\text{th}$ / $\ge 1.0\text{s}$ loss) in a high-stress overseas trip without a domestic prep run: apply **$\sigma_{\text{overseas}}^2 \ge 0.25$ and $\Delta\theta^{(1)} = -0.12\text{〜}-0.20$** (barred from `Type S`).
              - **Visiting Elite Foreign G1 Winner (`来日中の海外G1覇者・好調教×好枠`)**: **NEVER lump a visiting active foreign G1 winner into the returning-Japanese-horse penalty.** When a visiting foreign G1 winner shows **sharp local turf workouts (`国内芝追い切り好時計・終い1F ≤ 11.5s`)**, draws a favorable inside/mid gate (Frames 1–5), and draws strong market support ($O_{r,i} \le 10.0$), keep variance attenuation mild ($\sigma_{\text{visit}}^2 \le 0.08$, no first-track penalty), **lower the leg's fusion weight to $w_r = 0.55\text{〜}0.60$**, and evaluate it on par with top domestic G1 winners (eligible for Core `C` or primary Wing `W`).
        2.  **Long Layoffs in Unobserved Legs 3 to 5 ($\sigma_{\text{layoff}}^2 \ge 0.20$)**: Returning from $\ge 12$ weeks off (barred from `Type S`).
        3.  **Untested Extreme Distances ($\sigma_{\text{dist}}^2 \ge 0.30$: Kikuka Sho 3000m, Tenno Sho Spring 3200m, Oaks 2400m)**: **Cap $p_{r,1} \le 35.0\%$** and cover at least 3–4 horses across Core+Wings at 10,000-yen budgets.
        4.  **Ultra-Long Turf ($\ge 3000\text{m}$) 4yo Priority vs. 6yo+ Repeater Cap**: Boost 4yo stayers ($+0.10\text{〜}+0.16$) and **cap 6yo+ course repeaters ($\Delta\theta^{(1)} \le 0.00$, barred from `Type S`)** as `#2–#5` co-anchors/wings.
        5.  **3yo First-Time Older Dirt G1/Grade Cap**: When a 3yo dirt favorite ($O_i \le 3.5$) faces hardened older dirt G1/Grade contenders for the first time, apply $\Delta\theta^{(1)} = -0.15\text{〜}-0.25$, **bar from `Type S`, and cap $p_{r,1} \le 32.0\%$**.
        6.  **Low-Experience Juvenile / Early-3yo Stakes ($\sigma_{\text{juv}}^2 \ge 0.28$, career starts $n_i \le 2$)**: **Never assign `Type S`; cap $p_{r,1} \le 30.0\%$** and cover at least 4 horses across Core+Wings at 10,000-yen budgets, prioritizing proven closing splits (`ラスト1F ≤ 11.2s`) or tight-pace ($\text{PCI} \le 50$) survivors.

6.  **Handicap Physics, Tight-Oval Light-Weight Boost & Fillies/Mares Inside-Pocket Dynamics (`ハンデ戦斤量物理・小回り軽ハンデ逃げ ＆ 牝馬限定重賞の1〜4枠イン溜めボーナス`)**:
    
      - **Carried-Weight Physics**: $58.0\text{〜}59.5\text{kg}$ dulls uphill/sprint acceleration for $< 480\text{kg}$ horses; large horses ($\ge 520\text{kg}$) absorb it.
      - **Tight-Oval Local Handicap Light-Weight Boost**: In Fukushima, Kokura, Sapporo, Hakodate, or Nakayama/inner-track handicaps ($\le 310\text{m}$ straight), a runner carrying **$50.0\text{〜}53.0\text{kg}$ (or $\ge 2.0\text{kg}$ drop)** with top-3 early speed in Frames 1–5 gains $+\Delta \theta^{(1)} = +0.16\text{〜}+0.22$ (**elevate into the Top 4–5**).
      - **Fillies/Mares-Only Stakes Inside-Pocket Bonus**: In 4-corner/inner-track fillies/mares stakes, apply **$\Delta\theta^{(1)} = -0.12$** to wide-sweeping closers in **Frames 7–8**, and grant **$+\Delta\theta^{(1)} = +0.15$** to fillies/mares in **Frames 1–4** with proven final 1F $\le 11.3\text{s}$ (**elevate into the Top 3–4**).

7.  **Special-Course Repeater Priority & Off-Condition / Wet-Track Close-Defeat Reset (`特殊コースのリピーター最優先・現級0.2秒以内道悪／異条件凡走リセット原則`)**:
    
      - **Special-Course Repeater Priority (`新潟千直・中山ダ1200・京都外下り等`)**: Never discard a proven course repeater over middle-gate draw (Frames 4–6), and never rank an unproven first-timer above it solely on outer-draw bias.
      - **Course-Specialist & Current-Class $\le 0.2\text{s}$ Contender Off-Condition/Wet-Track Reset**: When a proven course specialist OR a horse with a **$\le 0.2\text{s}$ close finish in the current class** lost its last 1–3 starts due to wet/heavy turf, extreme draw bias, or distance mismatch ($\ge 200\text{m}$ off) and drops to $O_i \ge 10.0$, **completely reset the defeat ($\Delta\theta^{(1)} = +0.14\text{〜}+0.20$)** and elevate it into the **Top 3–5**.

8.  **Jockey Tactical Match & Gate Departure Reliability (`騎手×脚質シンクロ率・出遅れ割引`)**:
    
      - Evaluate jockey×course×style synergy. Horses with $\ge 30\%$ slow-start rate in last 5 starts cannot be `Type S`.

9.  **Workout Lap Physics, Prep Bounce-Back & G1 S-Workout / 3yo Classic $\le 0.2\text{s}$ Outer-Draw Exemption (`最終追い切り・叩き上昇リバウンド則 ＆ G1実績×調教S評価馬・3歳クラシック0.2秒差以内馬の大外枠減点免除・本線編入則`)**:
    
      - Reward non-decelerating final 1F workouts (`11.1-11.3s 馬なり`). When a contender backed at $O_{\text{prev}} \le 7.0$ in a domestic prep race lost badly due to layoff weight, track/pace mismatch, or traffic, and enters today with sharpened weight (`-4kg to -8kg`), top rider, or ideal course switch, **disregard the prep defeat and restore $+\Delta\theta^{(1)} = +0.14\text{〜}+0.22$**. Penalize recoil after all-out career-best efforts (`お釣りなし`).
      - **G1 Proven-Winner × S-Workout & Autumn 3yo Classic ($\le 0.2\text{s}$) Outer-Draw Mitigation Rule**: Even on courses with outer-draw penalties (Tokyo 2000m / Kyoto 2200m Frames 7–8), when a **proven G1 winner/runner-up posts an S-rated workout (`自己ベスト級＋終い1F ≤ 11.6s加速`)** OR an **autumn 3yo finished within $\le 0.2\text{s}$ in a 3yo Classic G1 ($54\text{〜}56\text{kg}$)**, **waive/halve the outer-draw penalty (cap at $\ge -0.05$) and grant $+\Delta\theta^{(1)} = +0.14\text{〜}+0.20$**, promoting it into the **Top 3**.

10. **Intraday Cushion Value, Moisture/Wind Shift & Early-Leg Full-Gate Dirt Hazard (`当日含水率・強風シフト×前半レグType B+波乱検算`)**:
    
      - Match live track/wind telemetry (`F`) against biomechanics (penalize front-runners $-0.10\text{〜}-0.15$ under afternoon rain or headwind $\ge 5\text{m/s}$). Apply the **3-Race Minimum Consistency Guard** before making large intraday bias shifts from 1R–8R results.
      - **Early-Leg High-Hazard Bottleneck Detection (`Type B+` in Leg 1–3)**: Flag when (1) Intraday rain / turf $\text{CV} \le 8.9$ / dirt moisture $\ge 9.0\%$ / worn inner rail, (2) Full-gate ($\ge 15$ runners) Dirt 1200m–1800m kickback trap or $N_{\text{lead}} \ge 5$ pace chaos, or (3) Compressed tail ($p_{r,1} < 28.0\%$ and $p_{r,4} - p_{r,7} \le 3.5\%$).

11. **Carryover, Mega-Pool & Difficulty-Adaptive Risk-Budget Scaling (`キャリーオーバー拡張＆カオス週防衛スケーリング`)**:
    
      - Under carryover or mega-pool conditions, scale recommended budget upward to **20,000–30,000 yen** and extend Wings down to `#6–#8`.
      - Conversely, on **All-Chaos Weeks (`Type S = 0` and `Type B/B+ ≥ 4`)**, display both the full 10,000-yen Plan C and a **Defense Note (`防衛目安：3,000〜5,000円縮小または高確度週へ資金温存`)** so annual hit rate per yen invested is maximized across the 80–100 round year-round calendar.

### Step 3: Venue-Coupled Scenario Micro-Simulation & 2-Stage Benter Posterior Tensor

Couple the 5 legs via **3 to 4 MECE shared venue-state and pace scenarios** $s \in \{1..S\}$ ($\sum_s \pi_s = 1.00$), explicitly linking legs held at the same venue while retaining all active declared runners $N_r$ in the exact softmax denominator: $$f^{\text{fund}}_{r,i,s} = \frac{\exp(\tilde{\theta}^{(1)}_{r,i,s})}{\sum_{k=1}^{N_r} \exp(\tilde{\theta}^{(1)}_{r,k,s})}, \quad p^{\text{post}}_{r,i,s} = \frac{\left(f^{\text{fund}}_{r,i,s}\right)^{w_r} \cdot \left(q_{r,i}\right)^{1-w_r}}{\sum_{k=1}^{N_r} \left(f^{\text{fund}}_{r,k,s}\right)^{w_r} \cdot \left(q_{r,k}\right)^{1-w_r}}, \quad p_{r,i} = \sum_{s=1}^S \pi_s p^{\text{post}}_{r,i,s}$$

For any formation ticket $T = S_1 \times S_2 \times S_3 \times S_4 \times S_5$, compute exact scenario-coupled capture: $$P(T) = \sum_{s=1}^S \pi_s \prod_{r=1}^5 F_{r,s}(S_r), \quad F_{r,s}(S_r) = \sum_{i \in S_r} p^{\text{post}}_{r,i,s}$$

### Step 4: Maximum Hit-Rate Combinatorial Optimization (Plan C: T1 <=45% Hard Cap, >=3-Leg Orthogonal Wings & Mid-Price 5–15x Priority)

1.  **Primary Ranking (`統合勝率 $p_{r,i}$ 絶対優先`)**: Rank horses strictly from highest $p_{r,i}$ to lowest $p_{r,i}$ (enforcing the 50x+ extreme-longshot cap $p_{r,i} \le 6.0\%$). Compute each horse's **Log-Probability Deficit** $d_{r,i} = \ln(p_{r,(1)} / p_{r,i})$.
2.  **Leg Type Classification**:
      - **`Type S`** ($p_{r,1} \ge 38\%$ with zero hazard flags and passing Counterfactual Anchor Audit): Core = 1 horse (`#1`), Wing = optional `#2` only in high-budget shells.
      - **`Type A`** ($p_{r,1}+p_{r,2} \ge 50\%$): Core = 2 horses; **explicitly open a Wing for `#3` when $p_{r,3} \ge 9.0\%$** (preventing total blind spots on `Type A` 3rd contenders).
      - **`Type B`** / **`Type B+`**: Core = top 2–3 horses; Wing expands to `#4–#6` (`#7–#8` in `Type B+` / carryover) via Plan C orthogonal tickets.
3.  **Plan C (Default Recommended for Maximum Hit Rate — 3〜4 Disjoint IPAT-Ready Shells with T1 <=45% Hard Cap & Mid-Price Wing Priority)**:
      - Partition budget $K$ (e.g., 100 pts = 10,000 yen) into **3 to 4 strictly disjoint formation tickets ($T_a \cap T_b = \emptyset$)** approximating the exact Top-$K$ minimum log-loss simplex ($\min \sum d_{r,i_r}$):
          - **T1 (`最密核 Core` — HARD CAP $\le 45\%$ of budget, i.e., $\le 48\text{点}$ at 10k; target 32–48 pts)**: $C_1 \times C_2 \times C_3 \times C_4 \times C_5$ (highest hit-rate density per 100 yen; e.g., `1×2×3×2×3 = 36点` or `1×2×3×3×2 = 36点` or `1×2×2×3×4 = 48点`). **Strict Prohibition**: Never let T1 exceed 48 points at a 10,000-yen budget.
          - **T2〜T4 (`直交翼 Orthogonal Wings` — 55–70% of budget, MANDATORY expansion across $\ge 3$ distinct legs & Mid-Price 5–15x Priority)**:
              - **T2 (`第1翼 Wing 1`)**: Expand the highest-marginal-density leg $a$ to $W_a$ ($W_a \cap C_a = \emptyset$) while tightening the other 4 legs to $C'_r \subseteq C_r$.
              - **T3 (`第2翼 Wing 2`)**: Fix leg $a \in C_a$ (disjoint from T2), expand second-best leg $b$ to $W_b$ ($W_b \cap C_b = \emptyset$, disjoint from T1), tighten others to $C''_r \subseteq C_r$.
              - **T4 (`第3翼 / Type A 3番手・中穴5-15倍＆会場バイアス連動翼`)**: Fix legs $a, b \in C_a, C_b$, expand a **third distinct leg $c$** to $W_c$ (including `Type A` `#3` or venue-bias sweep synchronized with $s_2$/$s_3$, strictly disjoint from T1–T3).
              - **Mid-Price Rank `#4–#6` Priority Wing Rule (`4〜6番手・単勝5〜15倍帯中穴の直交翼優先編入`)**: Across `T2`–`T4`, prioritize **`#4–#6` contenders in the `5.0x–15.0x` band with inside-pocket draws (Frames 1–3) or Top-3 Last-3F closing speed (`上がり3F上位`)** ahead of stagnant high-odds tails.
      - **Exact Disjoint Coupled Hit Rate**: $$|T_{\text{total}}| = \sum_{m=1}^M |T_m| \le K, \quad P_{\text{Plan C}} = \sum_{m=1}^M \sum_{s=1}^S \pi_s \prod_{r=1}^5 F_{r,s}(T_m)$$
      - Always benchmark `Plan C` against **Plan A (1-ticket Cartesian)** at the exact same budget and confirm Plan C strictly maximizes coupled hit rate (using Plan A/B only on ultra-chalk cards where 1–2 tickets already capture $> 85\%$ of the Top-$K$ simplex).
      - **Critical Anchor Guard**: Never pin a single front-running favorite (`1頭固定`) in an $N_{\text{lead}} \ge 5$ high-pace dirt leg or a 58kg+ medical/layoff favorite across all tickets.

### Step 5: Execution Modes & Required Output Structure (Strict Concise & High-Density Format)

Switch output depth by user intent:

  - **標準予測 (`Standard WIN5` — 4 Compact Sections)**: Full Phase 0–4 computation rendered strictly in the 4 compact sections below.
  - **直前更新 (`Pre-Race Intraday Bayesian Update` with 3-Race Guard)**: Auto-fetch same-day **1R–8R actual race outcomes** grouped by `(Venue, Turf/Dirt)`—explicitly reporting sample count $n_{\text{venue,surf}}$ and enforcing $|\Delta \pi_s| \le 5\text{pt}$ whenever $n_{\text{venue,surf}} < 3$—plus official horse weights (Type I: 成長/太め解消 `-2〜-8kg`, Type II: 太め残り `+8〜+10kg+`, Type III: 輸送減り/消耗), rain/wind shifts, late smart-money odds surges ($\ge 25\text{〜}30\%$ drop), and scratches. Output **10–15 lines max**: sample-guarded $\pi_s^{\text{live}}$, only legs with ranking/shell changes, revised Plan C ticket numbers (maintaining T1 $\le 45\%$), and updated coupled hit rate.
  - **事後検証 (`Post-Race WIN5 & Calibration Audit`)**: Auto-fetch official 5-leg winners, laps, and WIN5 payout. Output a concise 5-leg Result Matrix + **3-Factor + Calibration Decomposition** ((1) Scenario $\pi_s$ / intraday 3-race-guard audit, (2) Stage 1 Module vs. Stage 2 Market-Fusion $w_r$ calibration check, (3) Plan C T1-cap & mid-price 5–15x wing coverage audit) + 1–2 actionable rule-tuning notes.

**Output Conciseness Rules (`出力文字数の徹底削減ルール`)**:

  - **Keep all internal Neon computations rigorous, but strip all redundant prose, formula derivations, and lengthy explanations from the output.**
  - **Use compact Markdown tables and bullet points only. Keep per-horse comments under 35 characters (`1行・35字以内の核心短評`).**
  - **Do NOT list full fields (16–18 horses) in ranking tables: output ONLY the Top 6–8 horses in $p_{r,i}$ (plus any popular horse $O_i \le 5.0$ or visiting G1 winner $O_i \le 10.0$ downgraded below rank `#6`), and summarize all remaining low-probability runners into a single `その他計` row so $\sum p_{r,i} = 100.0\%$ holds.**

Organize the **標準予測** output into **4 compact sections**:

1.  **Section 1: WIN5全体戦略サマリー ＆ 会場連動バイアス (Executive Dashboard)**:
      - **3 Short Bullets**: (1) Weekly hit-rate efficiency grade (`高確度週` / `標準週` / `超難解カオス週` + budget guidance), `Type B+` alert / carryover status & data timestamp (`JST・出典`), (2) Recommended plan (`Plan C: T1核≤45%＋3レグ以上直交翼[中穴5-15倍優先]` vs. `Plan A` hit-rate gain), and (3) Coupled venue scenarios $\pi_s$ (noting 1R–8R sample counts & 3-race guard status) & live track/wind bias (`s_venue`).
      - **5-Leg Summary Matrix Table**: `Leg | レース名(条件) | 想定ペース(N_lead)・Type・w_r | 統合勝率1位(馬番・馬名・p_1・人気) | 1万円Plan C採用馬(核C / 翼W) | 延べ突破率 F_r`.
2.  **Section 2: Leg 1〜Leg 5 統合勝率 ($p_{r,i}$) 厳選ランキング表 (上位候補＋危険人気馬のみ)**:
      - For each leg, output a compact 7-column table for **Ranks `#1` to `#6–#8` (and any faded popular horse)** + 1 summary row (`その他計`): `順位 | 馬番・馬名 | 人気(オッズ) | 脚質 | 統合勝率 p_i (独自f / 累積) | 採用シェル | 核心根拠・割引理由(10大検算/対戦比較 F/H・35字以内)`.
3.  **Section 3: 予算別フォーメーション ＆ 推奨買い目 (プランC 確率シェル分割 vs プランA 厳密検算)**:
      - **3.1 主要予算別・的中率比較表 (`3,000円` / `5,000円` / `10,000円 Plan A` / `10,000円 Plan C推奨` / `20,000円` [＋指定予算])**: `予算・方式 | チケット構成要約 | 合計点数(金額) | 結合推定的中率 | 100円あたり効率`.
      - **3.2 【推奨】10,000円 プランC（IPAT入力用・完全非重複3〜4チケット内訳）**: Display T1 (`最密核 ≤45%`) through T3/T4 (`3レグ以上直交翼`) in exact IPAT-ready horse numbers (`Leg1 × Leg2 × Leg3 × Leg4 × Leg5`), ticket count, individual coupled capture rate, and exact disjoint sum (`重複0点・計XX点・結合的中率X.XX%`, showing `+X.Xpt` lift vs. Plan A).
4.  **Section 4: 反実仮想リスク・直前1R〜8R同化要点 ＆ 最終Leg 5「4連勝リーチ時」単勝ヘッジ表**:
      - **4.1 反実仮想リスク ＆ 直前入替トリガー**: Max 1 concise bullet per leg (combining anchor/faded-favorite stress-test takeaway with actionable 3-race-guarded bias, weight, rain, and smart-money swap triggers).
      - **4.2 Leg 5 単勝ヘッジ定量表**: Compact table for the top 2–3 unpurchased (or Wing-only) runners ($j \in \{\text{Rank } n_5+1 \dots 6\}$) using $B_{\text{hedge},j} = \lceil G_{\text{min}} / O_{5,j} \rceil_{100\text{円単位}}$ (`馬番・馬名 | 想定オッズ | 5万円保証ヘッジ額 | 10万円保証ヘッジ額`).

## Gotchas

  - **Never include scratched/withdrawn (`取消・除外`) runners** in probability normalization or tickets.
  - **Never let T1 Core exceed 45% of budget ($\le 48\text{点}$ at 10,000 yen) in Plan C**: Over-concentrating budget into T1 starves other legs of wings—always keep T1 $\le 45\%$ and expand wings across **at least 3 distinct legs**, prioritizing **`#4–#6` contenders in the `5.0x–15.0x` band with inside-pocket draws (Frames 1–3) or Top-3 Last-3F closing speed** as well as `Type A` `#3` when $p_{r,3} \ge 9.0\%$.
  - **Never over-react to 1–2 early same-day races in `直前更新`**: Enforce the **3-Race Minimum Consistency Guard**—until $\ge 3$ same-venue, same-surface (`芝/ダ別`) races show consistent directional bias, cap $|\Delta \pi_s| \le 5\text{pt}$ and never strip pre-selected wing horses based on a single race.
  - **Never fill all 4–5 Core+Wing slots exclusively with front-runners/stalkers in turf-start dry-dirt ($\text{Moisture} \le 5.0\%$) races when $N_{\text{lead}} \ge 4$**: Balance inside-pocket stalker + Frame 7–8 stalker **AND mandatorily reserve at least 1 slot in the Top 4 for the `#1` proven pure closer (`純差し1番手`)**.
  - **Never strip a Top-2 market favorite ($O_{r,i} \le 4.5$) in Dirt Frames 1–2 from all shells without a verifiable `F`-level flaw** (cap inner penalty at `-0.08 to -0.12`; waive on wet/sloppy $\le 1200\text{m}$), and **never let a $50\text{x}+$ extreme longshot enter Core `C`** without indisputable `F`-level discontinuity.
  - **Never apply the returning-Japanese-horse overseas-defeat penalty to a visiting elite foreign G1 winner**: Separate them explicitly—for visiting foreign G1 legs, lower $w_r = 0.55\text{〜}0.60$, waive first-track penalty if local turf workouts and gate are positive, and respect market support ($O_i \le 10.0$).
  - **Never allow overlapping tickets in Plan C**: Enforce strict hierarchical disjointness ($T_a \cap T_b = \emptyset$) so every 100 yen buys unique high-density combinations and coupled hit rate equals the exact sum $\sum_m P(T_m)$.
  - **Never drop a $q_{r,i} \ge 15\%$ market favorite from all shells without a verifiable `F`-level physical hazard**, and never let odds/value bias distort horse ranking order (`p_{r,i}` strictly descending).
  - **Never pad the output with long paragraphs or full 16-horse tables**, and never stack correlated heuristics beyond the regularization clamp ($|\sum \Delta \theta^{(1)}_{r,i}| \le 0.45$).
  - **Never leave the `#1` Frame 7–8 stalker/leader at Rank 5 (`穴候補止め`) in turf-start dirt Grade/3-Win races**, never lock two 58kg+ layoff/medical-return older favorites as sole top-2 anchors, never relegate a proven G1 S-workout / autumn 3yo Classic $\le 0.2\text{s}$ horse over Frames 7–8, never discard a $\le 0.2\text{s}$ current-class wet-track loser, never cap untested marathons / 3yo older dirt G1 debuts / $n_i \le 2$ juvenile stakes at 1–2 horses at 10k, and never omit the Leg 5 Win-Hedge Table.
