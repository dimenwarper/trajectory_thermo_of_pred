# A Trajectory-Level Identity for the Thermodynamics of Prediction, With and Without Back-Action

*Working notes, v2. Derived and numerically certified across two sessions. Status: unrefereed; each claim is tagged **[proved]**, **[verified]** (machine-checked on exactly enumerable models, or exact interval arithmetic for the chaotic maps), **[empirical]** (observed in ensembles, no proof), or **[open]**. v2 incorporates the results of an adversarial verification session: two conjectures of v1 are proved (Theorems 4 and 6), one corollary of v1 is withdrawn with an explicit counterexample and replaced by two valid bounds (Corollaries 5 and 6), the §5.1 chaos predictions are corrected against exact computation, and three open problems of v1 are closed.*

---

## Abstract

Still, Sivak, Bell & Crooks (2012) bounded dissipation below by per-step *nostalgia* — memory minus predictive power — absent back-action. We derive the trajectory-level generalization and its kinetic completion. The setup is an exact identity, valid under arbitrary back-action: dissipated work equals the summed *cryptic information* $\sum_t I[S_t;X_t\mid X_{t+1:T}]$ — what the state stores about the present that the signal's future never discloses — plus a residual of characterized sign; supplementing the information terms with one kinetic number per bath, the relaxation kernel's Dobrushin coefficient, converts the residual into a computable charge.

**Without back-action:** summed window nostalgia is monotone decreasing in window width, so the 2012 bound is provably the tightest of the sliding-window family; the information–kinetic hybrid then recovers 74–100% of dissipated work where information alone recovers 4–30%, exactly at complete relaxation.

**With back-action:** the feedback penalty is proved non-negative and equals the state's *oracular information* about the observable future, yielding
$$\beta\langle W_{\mathrm{diss}}\rangle \ \ge\ \sum_t I[S_t;X_t\mid X_{t+1:T}] \ -\ \sum_t I[S_{t+1};X_{t+2:T}\mid X_{t+1}] \ -\ I[S_0;X_{1:T}]:$$
*an agent pays for memory by dissipating it or by writing it into the world's future.* The dual filtration of the same identity is exactly Massey's directed-information second law.

All identities and bounds are machine-verified by exact enumeration, including net-work-extraction regimes.

---

## 1. Setup and conventions

Discrete time $t=0,\dots,T$. Environment states $x$, system states $s$. The system's energy landscape $E(s|x)$ depends on the current environment state. Inverse temperature $\beta = 1/k_BT$; informations in nats; $\pi_x(s) \equiv e^{-\beta E(s|x)}/Z(x)$ the equilibrium distribution at landscape $x$; $F_{\mathrm{eq}}(x) = -k_BT\ln Z(x)$.

**Two-stroke dynamics.** Each step $t \to t+1$:

1. **Drive stroke (quench).** The environment jumps $x_t \to x_{t+1}$ with kernel $\mathcal{T}(x_{t+1}\mid x_t, s_t)$. The landscape shifts at fixed $s_t$; work $W(t) = E(s_t|x_{t+1}) - E(s_t|x_t)$ is done on the system.
2. **Relaxation stroke.** The system updates $s_t \to s_{t+1}$ by a Markov kernel $K_{x_{t+1}}(s_{t+1}|s_t)$ with stationary distribution $\pi_{x_{t+1}}$ (e.g., detailed-balanced), exchanging heat with the bath. The kernel's fresh noise is independent of everything else.

**Back-action.** If $\mathcal{T}$ depends on $s_t$, the system influences its own input — the agent setting. The no-back-action case is $\mathcal{T}(x_{t+1}|x_t,s_t) = \mathcal{T}(x_{t+1}|x_t)$, or more generally an autonomous (possibly hidden-state, non-Markov-in-observables) environment process. **Nothing in §3 assumes either case.**

**Initialization.** $s_0$ is drawn from the equilibrium distribution of a flat reference landscape ($E \equiv \text{const}$), independent of the environment; the first drive stroke quenches from the flat landscape to $x_1$. (Any equilibrium start works; flatness only simplifies boundary terms.)

**Dissipated work.** $\beta\langle W_{\mathrm{diss}}\rangle \equiv \beta\langle W_{\mathrm{tot}}\rangle - \beta\,\Delta F_{\mathrm{eq}}$, with $\Delta F_{\mathrm{eq}}$ evaluated along the realized landscape sequence and averaged.

**Notation.** $X_{a:b} = (X_a,\dots,X_b)$; the "future at $t$" is $\vec X_t \equiv X_{t+1:T}$. Index convention below follows the derivation frame: at step $t$ the state $s_t$ (formed under $x_t$) experiences the quench to $x_{t+1}$.

---

## 2. Two lemmas

**Lemma 1 (Conditioning-robust work identity). [proved; verified to $1.1\times10^{-15}$ per step over 60 random feedback models]**
For any random variable $C$ that determines $(x_t, x_{t+1})$ (e.g., any superset of the environment trajectory),
$$\beta\big\langle W(t) - \Delta F_{\mathrm{eq}}(t)\big\rangle \;=\; \big\langle D[\,p(s_t|C)\,\|\,\pi_{x_{t+1}}]\big\rangle \;-\; \big\langle D[\,p(s_t|C)\,\|\,\pi_{x_t}]\big\rangle .$$

*Proof.* $D[p(s|C)\|\pi_x] = -H[S|C{=}c] + \beta\langle E(s|x)\rangle_{p(\cdot|c)} - \beta F_{\mathrm{eq}}(x)$. Subtracting the two KLs, the (conditioning-dependent) entropy terms cancel; averaging over $C$ gives $\beta\langle E(s_t|x_{t+1}) - E(s_t|x_t)\rangle - \beta\langle\Delta F_{\mathrm{eq}}\rangle$, which is the left side. No causal structure is used. ∎

**Lemma 2 (Filtration split). [proved; verified under random coarsened filtrations to $2.2\times10^{-16}$]**
For any sub-conditioning $G \subseteq C$ with $x^\*$ measurable w.r.t. $G$,
$$\big\langle D[\,p(s|C)\,\|\,\pi_{x^\*}]\big\rangle \;=\; I[S;C] - I[S;G] \;+\; \big\langle D[\,p(s|G)\,\|\,\pi_{x^\*}]\big\rangle .$$

*Proof.* Write $\log\frac{p(s|C)}{\pi_{x^\*}(s)} = \log\frac{p(s|C)}{p(s)} + \log\frac{p(s)}{p(s|G)} + \log\frac{p(s|G)}{\pi_{x^\*}(s)}$ and average over the true joint. The three terms give $I[S;C]$, $-I[S;G]$, and the stated conditional KL (well-defined because $\pi_{x^\*}$ is $G$-measurable). ∎

The entire theory below consists of applying Lemma 1 with $C$ = full environment trajectory and choosing the filtration $G$ in Lemma 2. **Future-conditioned** choices produce prediction-type bounds; **past-conditioned** choices produce feedback-type bounds.

---

## 3. The exact identity (feedback-robust)

Apply Lemma 1 with $C = X_{1:T}$ (full trajectory), and Lemma 2 with:

- for the post-quench term ($x^\* = x_{t+1}$): $G = X_{t+1:T}$, defining $R_t \equiv \langle D[\,p(s_t|x_{t+1:T})\,\|\,\pi_{x_{t+1}}]\rangle \ge 0$;
- for the pre-quench term ($x^\* = x_t$): $G = X_{t:T}$, defining $R''_t \equiv \langle D[\,p(s_t|x_{t:T})\,\|\,\pi_{x_t}]\rangle \ge 0$.

The $I[S_t; X_{1:T}]$ terms **cancel between the two applications** — this is why no causal assumption enters — leaving $I[S_t;X_{t:T}] - I[S_t;X_{t+1:T}] = I[S_t;X_t\mid X_{t+1:T}]$ by the chain rule. Summing over steps:

> **Theorem 1 (Cryptic-information identity). [proved; verified to $10^{-14}$ with and without feedback]**
> $$\boxed{\;\beta\langle W_{\mathrm{diss}}^{\mathrm{tot}}\rangle \;=\; \sum_{t} I[S_t;\,X_t \mid X_{t+1:T}] \;+\; \sum_t\big(R_t - R''_t\big)\;}$$
> for arbitrary environment statistics and arbitrary back-action.

$I[S_t;X_t\mid X_{t+1:T}]$ is the **cryptic information**: what the state stores about the present signal that the entire future of the signal will never disclose again. Information about $x_t$ that the future reveals anyway makes no appearance — it is thermodynamically free, *whether or not the system ever "uses" it*. The term is the finite-horizon, driven-system analogue of crypticity in computational mechanics (Crutchfield–Ellison–Mahoney), with the physical memory $S$ in place of causal states.

Everything else in this note is sign analysis of $\sum_t (R_t - R''_t)$.

---

## 4. No back-action: the trajectory bound, and what actually closes the gap

Assume the environment is autonomous (arbitrary process — hidden-Markov, long-memory, non-stationary — but not influenced by $S$). Two facts follow:

- **(CI)** $S_t \perp X_{t+1:T} \mid X_{1:t}$: the state, a function of the past signal and private noise, is conditionally independent of the future signal. (Holds for hidden-state environments too; only autonomy is needed.)
- **(KM)** Conditioned on $X_{t+1:T}$, the relaxation stroke $s_t \to s_{t+1}$ is still the bare kernel $K_{x_{t+1}}$ — the future cannot "peek" at the update — so the KL to the kernel's fixed point $\pi_{x_{t+1}}$ contracts: with $q$ denoting the pushforward, $\langle D[q\|\pi_{x_{t+1}}]\rangle \le R_t$, and $p(s_{t+1}|x_{t+1:T}) = q$ exactly, hence $R''_{t+1} \le R_t$.

Pairing $R_t$ with $R''_{t+1}$ and using $R''_0 = 0$ (equilibrium start, no influence on $X$) and the final boundary $\ge 0$:

> **Corollary 1 (Trajectory bound). [proved; verified]**
> $$\beta\langle W_{\mathrm{diss}}^{\mathrm{tot}}\rangle \;\ge\; \sum_{t} I[S_t;\,X_t \mid X_{t+1:T}].$$

> **Corollary 2 (Markov collapse). [proved]**
> If the environment is Markov in its observables, screening gives $I[S_t;X_{t:T}] = I[S_t;X_t]$ and $I[S_t;X_{t+1:T}]=I[S_t;X_{t+1}]$, so Corollary 1 reduces **exactly** to the summed Still–Sivak–Bell–Crooks bound. The trajectory extension has content only for non-Markovian environments — precisely the hidden-structure signals (language, biology) where prediction is interesting.

> **Corollary 3 (Learning duality). [proved; verified to $10^{-15}$]**
> Chain-rule algebra alone rearranges Corollary 1's underlying identity into
> $$\beta\langle W_{\mathrm{diss}}^{\mathrm{tot}}\rangle \;\ge\; \sum_t \big(I[S_{t+1};X_{t+1:T}] - I[S_t;X_{t+1:T}]\big) \;-\; I[S_T;X_T]:$$
> total **anticipation gained** about the future must be paid in dissipation. The nostalgia-type reading ("memory of the dead past costs") and the Sagawa–Ueda-type reading ("learning costs") are the same identity read forwards and backwards; the two sums agree term-for-term after telescoping.

**Relation to summed Still.** Without back-action the comparison is *not* symmetric, and v1's conjecture here was wrong. Theorem 4 (§5) shows the summed one-step nostalgia dominates the summed cryptic bound identically, $\sum_t N_1(t) \ge \sum_t N_T(t)$: in the autonomous regime the 2012 bound is always the tighter aggregate, and no environment — one-time-pad constructions included — can reverse the order. Per-step reversals do occur: in a pad environment $x_t = a_t \oplus b_t$ (future later reveals $b_t$, system stores $a_t$) the cryptic term beats the Still term at the pad step exactly as the synergy intuition suggests, but the sums never cross; the deficit is repaid at neighboring steps. **[proved; verified: 0/30 violations across random, hidden-Markov, and designed pad environments; `item2_theoremC.py`]** The aggregate separation $\sum\text{cry} > \sum\text{Still}$ is real but is a *feedback* phenomenon (§6): a designed feedback pad — memory bit re-echoed by the environment two steps later — achieves $\sum\text{cry} - \sum\text{Still} = +0.53$ nats, and under feedback the Still sum can even go negative ($-0.23$ observed) while the cryptic sum cannot.

**Looseness, diagnosed.** The residual $\sum(R_t - R''_t)$ — finite-speed relaxation cost — dominated all information bounds by factors of 3–20 in every tested regime (Table 1), consistent with the standard critique that information bounds price only the informational component of dissipation. v2 adds the diagnosis and the cure: the residual is *kinetic*, and a single kernel-contraction number per bath restores near-tightness.

### 4.1 The hybrid bound: charging the un-contracted fraction

Re-index the residual as $\sum_t(R_t - R''_t) = \sum_{t\le T-2}(R_t - R''_{t+1}) + R_{T-1}$ (the $R''_0 = 0$ boundary is absorbed). Without back-action, $R''_{t+1} = \langle D[pK\|\pi K]\rangle$ is a KL after one application of the relaxation kernel, so it contracts by the kernel's KL contraction coefficient, which is dominated by the Dobrushin (total-variation) coefficient $\eta_{\mathrm{TV}}(K_x)$ — the standard result that $\eta_{\mathrm{TV}}$ dominates the contraction coefficient of every $f$-divergence. For the jump kernel $K = r\pi\mathbf{1}^\top + (1-r)\mathrm{Id}$, $\eta_{\mathrm{TV}} = 1-r$.

> **Theorem 2 (Hybrid information–kinetic bound). [proved; verified; `item1_hybrid.py`]**
> Without back-action, for any relaxation kernels,
> $$\beta\langle W_{\mathrm{diss}}^{\mathrm{tot}}\rangle \;\ge\; \sum_t I[S_t;X_t\mid X_{t+1:T}] \;+\; \sum_{t\le T-2}\big(1 - \eta_{\mathrm{TV}}(K_{x_{t+1}})\big)\,Q_t \;+\; R_{T-1},$$
> where $Q_t$ is $R_t$ itself, or any Lemma-2 coarsening of it (certified-computable choice: $Q_t = \langle D[\,p(s_t|x_{t+1})\,\|\,\pi_{x_{t+1}}]\rangle$, requiring only one-step statistics). The bound is **exact** at complete relaxation ($\eta_{\mathrm{TV}} = 0$ makes $R''_{t+1} = 0$ and the ledger closes).

**Table 2 — closing the residual** (three-phase hidden-cycle environment: hidden period-3 phase, slip $0.05$, emission noise $\eta=0.1$, $J=2$, $T=8$; nats; `gen_tables.py`):

| $r$ | $\beta W_{\mathrm{diss}}$ | $\sum$ cryptic | $\sum$ Still | hybrid ($Q$ one-step) | hybrid ($Q=R_t$) | hybrid/W |
|------|------|------|------|------|------|------|
| 0.30 | 2.105 | 0.088 | 0.096 | 1.547 | 1.552 | 74% |
| 0.50 | 3.362 | 0.273 | 0.314 | 2.582 | 2.611 | 78% |
| 0.70 | 4.700 | 0.605 | 0.735 | 3.867 | 3.971 | 84% |
| 0.90 | 6.044 | 1.155 | 1.475 | 5.382 | 5.675 | 94% |
| 1.00 | 6.675 | 1.548 | 2.013 | 6.210 | **6.675 (exact)** | 100% |

The pure information bounds recover 4–30% of dissipation across this sweep; the hybrid recovers 74–100%, with the certified-computable one-step $Q$ giving up only a few percent relative to the exact-$R$ version. The message inverts the looseness critique: the information terms were never supposed to price the kinetic cost, and one Dobrushin coefficient per bath — a *property of the hardware, not of the signal* — prices almost all of it.

---

## 5. The horizon family: Still to cryptic as a sliding-window dial

Fix a window width $k \ge 1$ and choose *matched finite windows* as the filtrations in Lemma 2: $G = X_{t+1:t+k}$ for the post-quench term, $G = X_{t:t+k-1}$ for the pre-quench term (all windows clipped at $T$). The information terms combine to the **horizon-$k$ nostalgia**

$$N_k(t) \;\equiv\; I[S_t;\,X_{t:t+k-1}] \;-\; I[S_t;\,X_{t+1:t+k}],$$

the drop in the state's information about a width-$k$ window as that window slides one step into the future.

> **Theorem 3 (Horizon family). [proved; verified to $2\times10^{-14}$ for every $k$ on two environment classes]**
> Without back-action, for **every** $k \ge 1$ simultaneously,
> $$\beta\langle W_{\mathrm{diss}}^{\mathrm{tot}}\rangle \;=\; \sum_t N_k(t) + \Sigma^{(k)}, \qquad \Sigma^{(k)} \ge 0.$$

**Endpoints. [proved]** At $k=1$, $N_1(t) = I[S_t;X_t] - I[S_t;X_{t+1}]$ — the Still–Sivak–Bell–Crooks nostalgia *exactly*. At $k = T$ the windows become the full future and telescoping gives $N_T(t) = I[S_t;X_t\mid X_{t+1:T}]$ — Corollary 1. The 2012 bound and the trajectory bound are the two ends of one dial.

v1 read Theorem 3 as licensing $\max_k \sum_t N_k(t)$. That maximum is now known in closed form:

> **Theorem 4 (Summed horizon monotonicity). [proved; verified: 0/30 violations across three environment classes; `item2_theoremC.py`]**
> Without back-action, the summed family is monotone in the window width:
> $$\sum_t N_{k+1}(t) \;\le\; \sum_t N_k(t) \qquad \text{for every } k \ge 1.$$
> Hence $\sum_t N_1 \ge \sum_t N_2 \ge \dots \ge \sum_t N_T$: the summed Still bound is the tightest member of the family, and the maximum over $k$ is attained at $k=1$.

*Proof.* Define the state's teacher-forced AR informations $\alpha_k(t) = I[S_t;X_{t+k}\mid X_{t:t+k-1}]$ and future-only $\bar\alpha_{k+1}(t) = I[S_t;X_{t+k+1}\mid X_{t+1:t+k}]$; the chain rule gives the increment formula $\sum_t (N_{k+1}(t) - N_k(t)) = \sum_t \big(\alpha_k(t) - \bar\alpha_{k+1}(t)\big)$. Two facts close the telescope. *(i)* $\alpha_k(1) = 0$: conditioned on $X_1$, the fresh relaxation noise in $S_1$ is independent of the autonomous environment's future, so $S_1 \perp X_{2:T}\mid X_1$. *(ii)* $\alpha_k(t+1) \le \bar\alpha_{k+1}(t)$: given $(S_t, X_{t+1:t+k})$, the pair $(S_{t+1}, X_{t+k+1})$ is generated by fresh noise and autonomous environment steps, so $S_{t+1} \perp X_{t+k+1} \mid (S_t, X_{t+1:t+k})$; the conditional data-processing inequality along $S_{t+1} \leftarrow S_t$ then bounds the lag-$k$ AR information of the *later* state by the future-only AR information of the *earlier* one. Pairing each $\alpha_k(t+1)$ with $\bar\alpha_{k+1}(t)$ and using (i) for the unpaired first term makes every bracket nonpositive. ∎

**AR spectrum and increments. [proved]** The chain-rule decompositions $I[S_t;X_{t+1:t+k}] = \sum_{j\le k}\bar\alpha_j(t)$ and $I[S_t;X_{t:t+k-1}] = I[S_t;X_t] + \sum_{j<k}\alpha_j(t)$ stand as in v1: each additional step of lookahead changes the per-step floor by the surviving AR-spectrum mass at that lag; for Markov environments $\alpha_k = \bar\alpha_k = 0$ for all $k \ge 1$ and the family is flat, generalizing Corollary 2.

**Table 3 — horizon profiles** (two-state system, $r=0.7$, $T=8$; per-$k$ identity gaps $\le 2\times10^{-14}$, all residuals $\ge 0$):

| k | HMM ($\eta{=}.1$, slip $.1$), $\beta W_{\mathrm{diss}}{=}4.593$ | echo $x_t{=}x_{t-3}{\oplus}\varepsilon(.05)$, $\beta W_{\mathrm{diss}}{=}4.000$ |
|---|------|------|
| 1 (Still) | 0.780 | 1.075 |
| 2 | 0.708 | 1.029 |
| 3 | 0.687 | **0.478** |
| 4 | 0.684 | 0.478 |
| 8 (cryptic) | 0.680 | 0.478 |

**Reading the profile.** The $k$-profile is a dissipation-side readout of the state's forecasting depth: the echo environment's cliff sits exactly at the echo lag, and the total drop $N_1 - N_T$ is the state's cumulative long-horizon skill discounted against the naive one-step nostalgia charge. Theorem 4 sharpens the profile's meaning: without back-action the summed profile can only fall, so its diagnostic content is in *shape* (flatness onset = Markov order; cliff = forecasting depth), not in bound improvement. Conversely, any measured $\sum_t N_{k+1} > \sum_t N_k$ **falsifies the autonomous-environment hypothesis** at the information layer, before any thermodynamics is invoked: rising summed profiles are a certificate of back-action, realized by the feedback pad of §4 (profile rising to $+0.53$ at echo probability $1$). The profile is not merely a meter of forecasting depth; it is a feedback detector.

**Why autoregression is effective — four remarks.** *(i)* Chain rule is a zero-overhead factorization: the long-horizon objective $I[S_t;X_{t+1:t+k}]$ decomposes *exactly* into teacher-forced next-symbol conditionals, so a model optimal at every one-step conditional is optimal for every long-horizon joint simultaneously — in sharp contrast to the modularity cost of spatial decomposition (Boyd–Mandal–Crutchfield). **[proved as information theory; the contrast is interpretive]** *(ii)* Every quantity this ledger prices is teacher-forced — the environment always delivers its realized symbols; the world never rolls out from the model. Teacher-forced log-loss is not a proxy for the physically priced objective; it *is* that objective. Exposure bias belongs to generation, not to priced prediction. *(iii)* The learning-dual reading (Corollary 3) pays anticipation per step; the chain rule schedules long-horizon information acquisition into exactly-matching per-symbol installments. *(iv)* Every term in the family is a difference of teacher-forced probe log-losses, so the family is in principle certifiable from transcripts by autoregressive probing alone — with the finite-sample caveats now quantified in §8.1: the full-future terms are the most estimation-hungry, and plug-in "certificates" are not one-sided.

**Caveat.** Theorems 3–4 assume no back-action; the horizon family under feedback inherits window-dependent penalties $\Phi^{(k)}$ analogous to §6, not derived here.

### 5.1 Takens' theorem and quantized chaos: when the horizon family can bite

The results of this subsection live on the information layer: the dissipation inequality is not used in any proof. Their thermodynamic content is classificatory — they determine when Theorem 3 is vacuous and when its contrapositive is informative. The subsection separates into an infinite-precision statement (Proposition 1, unchanged from v1) and a quantized-observation theory that replaces v1's interpretive sketch, which exact computation has partly refuted.

> **Proposition 1 (Takens vacuousness). [proved on the information layer; discrete analogue verified]**
> Let $x_t = h(z_t)$, $z_{t+1} = f(z_t)$, with $f$ a $C^2$ diffeomorphism of a compact invariant set $A$ of box dimension $d_B$, $h$ in the prevalent set of $C^2$ observables of the Takens / Sauer–Yorke–Casdagli theorems, observations at infinite precision, no back-action, and $K^* = \lfloor 2 d_B\rfloor + 1$. Then almost surely every width-$K^*$ observation window determines the underlying state; by invertibility of $f$, consecutive width-$k$ windows ($k \ge K^*$) generate the same σ-algebra as $z$. Hence for **every** physical state $S_t$, however constructed: $N_k(t) = 0$ and $\bar\alpha_{k+1}(t) = 0$ for all $k \ge K^*$. The horizon family is identically vacuous beyond the embedding window.

*Proof sketch.* Injectivity of the delay map on $A$ makes each window a measurable bijection of $z_{t+1}$ (resp. $z_t$); $f$ a diffeomorphism gives $\sigma(W_t) = \sigma(W_{t+1}) = \sigma(z_t)$; mutual informations of any $S_t$ with the two windows therefore coincide. ∎

**Codicil (finite horizons). [verified exactly]** With windows clipped at $T$, the final $K^*{-}1$ steps retain nonzero $N_k$: their futures are shorter than an embedding window. In the echo register at $\eta = 0.002$, interior steps contribute $\approx 0.0013$ nats each while the two truncated steps carry $0.165 + 0.159$ of the $0.331$ total. Memory is free only if the world outlives it by an embedding window.

**Corollary 4 (Markov-order flatness). [proved; verified to machine precision]** If the observable process is Markov of order $m$, screening gives $N_k$ constant for all $k \ge m$ — at every noise level (Table 4: $N_3 = \dots = N_8$ exactly for the order-3 echo at all $\eta$). Flatness onset reads off Markov order; collapse *depth* reads off redeemability.

**Table 4 — vacuousness onset** (echo register $x_t = x_{t-3}\oplus\varepsilon(\eta)$, $K^*{=}3$):

| $\eta$ | $N_1$ | $N_2$ | $N_3 = \dots = N_8$ |
|------|------|------|------|
| 0.002 | 1.077 | 1.020 | 0.331 (interior $\approx 0$; all boundary) |
| 0.05 | 1.075 | 1.029 | 0.478 |
| 0.20 | 1.067 | 1.047 | 0.814 |
| 0.50 (i.i.d.) | 1.048 | 1.048 | 1.048 (fully cryptic pole; flat) |

**Quantized observation: the exact picture. [verified by exact interval-arithmetic enumeration, no sampling; `item5a_tent.py`]** Proposition 1's caveat — infinite precision is essential — is now quantitative, and v1's conjectured signatures are corrected in three respects. Test system: skew tent map $f(z) = z/a$ on $[0,a]$, $(1-z)/(1-a)$ on $(a,1]$ (non-invertible, Lebesgue-invariant, Lyapunov exponent $\lambda = H(a) = $ KS entropy); observable = leading $m$ bits of $z_t$; internal state $S$ = the $\delta$-bin of $z_0$, $\delta = 2^{-p}$. All entropies computed exactly on the common refinement of the iterated preimage partitions ($a \in \{0.6, 0.75\}$, $m \in \{1,2\}$, $p \in \{6,10,14\}$, $k \le 19$).

*(i) The profile rises; it does not fall.* $N_k$ at stationary interior steps is a rising sigmoid from $0$ to a positive asymptote — the opposite of the echo cliff. Mechanism: below the resolution horizon, the $\delta$-cell predicts the width-$k$ window and its shifted copy equally well, and stationarity of the symbol process makes $N_k \approx H(W_{0:k-1}) - H(W_{1:k}) = 0$; crypticity switches on only when the window is long enough to expose the fold — when branch ambiguity of the past symbol becomes visible against the reconstructed present.

*(ii) One knee, not two.* The switch-on occurs at the resolution horizon $k^* \approx \ln(1/\delta)/\lambda = p\ln 2/\lambda$. Measured onsets track the prediction across all parameters — $k^*_{\text{pred}} \to k^*_{\text{meas}}$: $6.2 \to 7$, $10.3 \to 11$, $14.4 \to 15$ ($a{=}0.6$, $m{=}2$) and $7.4 \to 8$, $12.3 \to 14$ ($a{=}0.75$). This *is* v1's conjectured Lyapunov knee $\lambda^{-1}\ln(1/\varepsilon)$, upgraded to **[verified]** with its scaling law. The conjectured *second* (embedding) knee does not exist in this regime: for non-invertible dynamics there is no embedding shoulder to reach, and the exact profiles show a single sigmoid. The two-knee signature is withdrawn for Regime III.

*(iii) The asymptote is the folding entropy.* $N_k \to N_\infty$ equal to the branch (folding) entropy of the map — for full-branch Lebesgue maps, exactly $\lambda$. At $a = 0.75$, $k = 19$: $N_k = 0.5622$ against $\lambda = 0.5623$. The permanently cryptic rate of Regime III is thus not merely nonzero: it *equals* the map's information-destruction rate. The horizon profile, read at large $k$ under quantized observation, is a dissipation-side **meter of KS entropy** for this class, tightening the classificatory claim into a calibration.

**Genericity does not rescue invertible systems under future-only conditioning. [verified, Monte Carlo $10^7$ samples with half-sample stability control; `item5b_baker.py`]** The natural reading of Proposition 1 — invertible + generic observable $\Rightarrow$ crypticity shuts off beyond $K^*$ — fails once observations are quantized, and fails structurally. Skew baker's map ($a = 0.6$, unstable-direction exponent $\lambda_u = 0.673$; $S$ = $64{\times}64$ bin of $(u_0,v_0)$; binary observable):

**Table 5 — baker's map, degenerate vs generic observable** (plug-in + Miller–Madow, $10^7$ samples; asymptote error $\lesssim 0.01$; $k\ge13$ excluded for estimator drift):

| $k$ | 2 | 4 | 6 | 8 | 10 | 12 |
|---|---|---|---|---|---|---|
| $N_k$, degenerate $x=[u\ge\frac12]$ | 0.041 | 0.183 | 0.392 | 0.559 | 0.597 | 0.609 |
| $N_k$, generic $x=[\mathrm{frac}(u+0.618v)\ge\frac12]$ | 0.052 | 0.212 | 0.400 | 0.490 | 0.525 | 0.541 |

The degenerate observable — constant along the stable direction, so the genericity hypothesis fails exactly as Proposition 1 requires — reproduces tent-map behavior, $N_k \to \lambda$. The generic observable gives a strictly lower asymptote ($\approx 0.54$) that is nowhere near zero. The mechanism identifies the culprit as the σ-algebra, not the observable: the family conditions on the **future** word only, and future observations resolve the unstable coordinate at rate $\lambda$ while carrying only exponentially attenuated information about the stable coordinate — the very contraction that makes the dynamics invertible. The branch bit of the previous step is never fully recovered from the future, and

$$N_\infty \;=\; \big(\text{branch entropy}\big) \;-\; \big(\text{stable-direction information recoverable from the future}\big),$$

with genericity controlling only the (finite) second term. **[empirical; mechanism argued, not proved]** Takens closure — $N_k \to 0$ beyond an embedding window — requires *two-sided* windows, which the matched-filtration construction of Lemma 2 permits but the horizon family as defined does not use. Making the two-sided family and its residuals explicit is Open Problem 4 (§11).

**Where the physics is load-bearing.** Two places, neither used above. *(i) The contrapositive.* Theorem 3 read right-to-left says measured dissipation upper-bounds the retained sliding-window information of *any* internal state: calorimetry constrains representation with no access to internals. **Regime I** (reversible, deterministic, finite-dimensional, exactly observed): the channel is provably uninformative. **Regime III** (information-destroying dynamics): the channel is not merely informative but *calibrated* — measured dissipation per step below the folding entropy certifies, via the contrapositive at large $k$, that no internal state retains the destroyed information, and the folding entropy itself is readable from the profile asymptote. **Regime II** (stochastic dynamics with a stable filter): δ-informative, with informational embedding length $K^*(\delta) \sim \log(1/\delta)/(\text{filter contraction rate})$ — imported from filter stability and the stochastic Takens theorems of Stark et al. *(ii) Achievability.* A vanished lower bound is vacuous, not a cost statement: every environment jump costs an irreducible quench dissipation of order $D[\pi_{x_t}\|\pi_{x_{t+1}}]$ *however predictable the jump was* — the near-deterministic echo dissipates $\approx 4.0$ nats against a family maximum of $1.08$. Predictability refunds nothing at finite driving; the refund is kinetic and is exactly what Theorem 2 prices. The defensible summary: *dynamical complexity — dimension, nonlinearity, chaos — carries no informational floor; the priced quantity is information destruction; the remaining cost is implementation-bound and is captured by the hybrid bound.*

**Signature summary (corrected).** The profile is a measuring instrument with four verified readouts and one withdrawn: flatness onset = Markov order **[proved]**; collapse depth = redeemability **[verified]**; quantized-chaos profile = rising sigmoid with a single Lyapunov-resolution knee at $k^* \approx \ln(1/\delta)/\lambda$ **[verified, scaling law]**; nonzero asymptote = folding entropy = the dynamics' information-destruction rate **[verified; exact at full-branch]**; the second (embedding) knee is withdrawn for non-invertible dynamics and, under future-only conditioning, does not close crypticity even for invertible dynamics with generic observables **[verified]**.

**Caveats.** The tent/baker computations have one-dimensional unstable directions; smooth higher-dimensional attractors remain untested. Prevalence-not-universality and the imported Regime II theorems remain as in v1.

---

## 6. Back-action: the export discount, now with the exact currency

Now let $\mathcal{T}(x_{t+1}\mid x_t, s_t)$ depend on $s_t$. Theorem 1 stands. What fails is (KM): conditioned on the future, the relaxation stroke becomes a Doob $h$-transform of $K$ (future environment observations depend on the fresh state), and $p(s_{t+1}\mid x_{t+1:T}) \ne q$. Also $R''_0 = I[S_0;X_{1:T}] \ge 0$ no longer vanishes: the trajectory reads out the initial state.

**Exact penalty ledger. [proved; verified]** Define, per step,
$$C_t \equiv R_t - \big\langle D[q\,\|\,\pi_{x_{t+1}}]\big\rangle \ \ge 0, \qquad
\Phi_t \equiv R''_{t+1} - \big\langle D[q\,\|\,\pi_{x_{t+1}}]\big\rangle,$$
so that $R_t - R''_{t+1} = C_t - \Phi_t$ exactly and Theorem 1 becomes
$$\beta\langle W_{\mathrm{diss}}^{\mathrm{tot}}\rangle = \sum_t I[S_t;X_t\mid X_{t+1:T}] + \sum_t C_t - \sum_t \Phi_t + (\text{final residual} \ge 0) - I[S_0;X_{1:T}].$$
Two remarks sharpen the ledger before it is bounded. First, $C_t$ is exactly the (cell-averaged) **mismatch cost** of the relaxation stroke in the sense of Kolchinsky–Wolpert: $C_t = \langle D[p_{\text{cell}}\|\pi_{x_{t+1}}] - D[p_{\text{cell}}K_{x_{t+1}}\|\pi_{x_{t+1}}]\rangle$ **[verified to $2\times10^{-16}$; `item7_kw.py`]** — the ledger reads: *dissipation = crypticity + mismatch cost − feedback discount + boundary terms*. Second, the discount $\Phi_t$ has an exact information-theoretic identity (Theorem 6 below) that settles its sign — v1's Open Problem 2 — and names its currency.

> **Theorem 5 (General feedback bound). [proved; verified, including regimes where naive bounds fail]**
> $$\beta\langle W_{\mathrm{diss}}^{\mathrm{tot}}\rangle \;\ge\; \sum_t I[S_t;X_t\mid X_{t+1:T}] \;-\; \sum_t \Phi_t \;-\; I[S_0;X_{1:T}].$$

**Interpreting $\Phi_t$.** Write $\Phi_t = \Delta_t + \Xi^{\times}_t$ where $\Delta_t \equiv \langle D[\,p(s_{t+1}|x_{t+1:T})\,\|\,q\,]\rangle \ge 0$ measures how much the future trajectory knows about the fresh state beyond the no-peeking pushforward, and $\Xi^\times_t$ is an explicit cross term.

**Lemma 3 (Backward-transfer-entropy bound on the leakage). [proved; intermediate equality verified to $1.3\times10^{-15}$]**
$$\Delta_t \;\le\; \mathrm{bTE}_t \equiv I\big[S_{t+1};\,X_{t+2:T}\,\big|\,S_t,\,X_{t+1}\big].$$
*Proof.* The KL between the conditional joints $p(s_t,s_{t+1}|x_{t+1:T})$ and $p(s_t|x_{t+1:T})\,K_{x_{t+1}}$ equals $\langle D[\,p(s_{t+1}|s_t,x_{t+1:T})\,\|\,K_{x_{t+1}}(\cdot|s_t)]\rangle$; since $K = p(s_{t+1}|s_t,x_{t+1})$ under the true joint (fresh noise, even with feedback), this average is exactly $\mathrm{bTE}_t$. Marginalizing to $s_{t+1}$ contracts KL. ∎

This is the discrete backward transfer entropy in the sense of Ito (Sci. Rep. 6:36831, 2016): the information the strictly-future environment carries about the system's post-update state, given its pre-update state and current input — nonzero only through back-action.

**Lemma 4 (Complete relaxation kills the cross term). [proved; verified to $10^{-16}$]**
If relaxation is complete ($K_x(\cdot|s) = \pi_x$), then $q = \pi_{x_{t+1}}$, the cross term vanishes identically, and $\Phi_t = \Delta_t$ exactly.

**Lemma 5 (History-conditioning is free). [proved; verified to machine precision on 60 random feedback models; `item8_massey.py`]**
Because the environment transition reads only the current state, past $\perp (S_{t+1}, X_{t+2:T}) \mid (S_t, X_{t+1})$, hence $\mathrm{bTE}_t = I[S_{t+1};X_{t+2:T}\mid S_{0:t},X_{1:t+1}]$: state-level and history-level backward transfer entropies coincide, and no strengthening of Lemma 3 is available by enlarging the conditioning.

**v1's Corollary 4 is withdrawn at partial relaxation. [verified counterexample; `item3_adversarial.py`]** The bound obtained by substituting $\mathrm{bTE}_t$ for $\Phi_t$ in Theorem 5 is valid only where Lemma 4 applies. At partial relaxation the cross term can push $\Phi_t$ *above* $\mathrm{bTE}_t$: adversarial search over $8000$ jump-kernel and $4000$ Metropolis feedback models followed by simplex polish finds robust overshoots — witness at $r = 0.29$: $\Phi_t = 0.498 > \mathrm{bTE}_t = 0.302$ (with $\Delta_t = 0.235$, $\Xi^\times_t = 0.263$); maximum polished overshoot $+0.196$ nats. Substituting bTE therefore shrinks the subtracted term illegitimately and the resulting "bound" can exceed the true dissipation. Two valid replacements follow, one kinetic and one purely informational.

> **Corollary 5 (Kinetically corrected bTE bound). [proved; verified: 0/8000 violations]**
> $\Xi^\times_t = \langle\langle \log(q/\pi)\rangle_{p - q}\rangle$, hence by Pinsker and Jensen $|\Xi^\times_t| \le M_t\sqrt{2\Delta_t}$ with $M_t = \max_s|\log(q(s)/\pi(s))| \le \max\big(\ln\tfrac1r,\ \ln(r + \tfrac{1-r}{\pi_{\min}})\big)$ for the jump kernel. With Lemma 3,
> $$\Phi_t \le \mathrm{bTE}_t + M_t\sqrt{2\,\mathrm{bTE}_t}, \qquad
> \beta\langle W_{\mathrm{diss}}^{\mathrm{tot}}\rangle \;\ge\; \sum_t I[S_t;X_t\mid X_{t+1:T}] - \sum_t\big[\mathrm{bTE}_t + M_t\sqrt{2\,\mathrm{bTE}_t}\big] - I[S_0;X_{1:T}].$$
> At $r=1$, $M_t = 0$ and v1's boxed corollary is recovered exactly.

The deeper result is that no kinetic input is needed at all, because $\Phi_t$ itself is a difference of two information functionals:

> **Theorem 6 (Exact discount identity; $\Phi_t \ge 0$). [proved; identity verified to $1.1\times10^{-15}$, both inequalities 0 violations over 200 feedback models; minimum of $\Phi$ over 12,000 adversarially optimized models is 0 exactly; `item3_theoremD.py`]**
> For every $t$ and arbitrary back-action,
> $$\Phi_t \;=\; \mathrm{Orac}_t \;-\; I_\nu(t), \qquad
> \mathrm{Orac}_t \equiv I[S_{t+1};X_{t+2:T}\mid X_{t+1}], \qquad
> I_\nu(t) \equiv \big\langle D\big[\,p(s_{t+1}\mid x_{t+1:T})\ \big\Vert\ p(s_{t+1}\mid x_{t+1})\,\big]\big\rangle_{\text{cells at fixed }x_{t+1}},$$
> with $0 \le I_\nu(t) \le I[S_t;X_{t+2:T}\mid X_{t+1}] \le \mathrm{Orac}_t$, whence $0 \le \Phi_t \le \mathrm{Orac}_t$.

*Proof.* **Identity:** expand both KL terms of $\Phi_t$ against the common reference $\pi_{x_{t+1}}$. The barycenter of the future-conditioned cells at fixed $x_{t+1}$ is $\langle q\rangle_{\text{cells}} = K_{x_{t+1}}\,p(s_t\mid x_{t+1}) = p(s_{t+1}\mid x_{t+1})$, because $p(s_{t+1}\mid s_t, x_{t+1}) = K_{x_{t+1}}$ holds *even under feedback* when the future is not conditioned upon (fresh noise). The two barycenter terms cancel; the $R''_{t+1}$ side leaves $\mathrm{Orac}_t$ and the $q$ side leaves $I_\nu$. **Sign:** $I_\nu = I[\tilde S; X_{t+2:T}\mid X_{t+1}]$ where $\tilde S$ is a *fresh-noise twin* drawn from $K_{x_{t+1}}(\cdot\mid s_t)$ independently of the realized transition; two applications of the conditional data-processing inequality along $\tilde S \leftarrow S_t \rightarrow S_{t+1} \rightarrow X_{t+2:T}$ (given $x_{t+1}$; the environment reads only the current state) give $I_\nu \le I[S_t;X_{t+2:T}\mid X_{t+1}] \le \mathrm{Orac}_t$. ∎

**Remark (v1 Open Problem 2 resolved).** $\Phi_t \ge 0$ always: the export discount never flips sign, so back-action can only *reduce* the certified floor below the no-feedback ledger — the direction the stigmergy reading requires.

> **Corollary 6 (Information-only feedback bound). [proved; verified: valid in 200/200 models, min slack 0.077; tighter than Corollary 5 in 200/200]**
> Dropping $I_\nu \ge 0$ in Theorem 6:
> $$\boxed{\;\beta\langle W_{\mathrm{diss}}^{\mathrm{tot}}\rangle \;\ge\; \sum_t I[S_t;X_t\mid X_{t+1:T}] \;-\; \sum_t I[S_{t+1};X_{t+2:T}\mid X_{t+1}] \;-\; I[S_0;X_{1:T}]\;}$$
> At complete relaxation $I_\nu = 0$ and $\mathrm{Orac}_t = \mathrm{bTE}_t = \Delta_t = \Phi_t$ exactly, so Corollary 6 coincides with v1's corollary there: it is that bound's correct generalization to partial relaxation, not merely a replacement.

**Reading.** The subtracted quantity is the state's **oracular information** in the sense of computational mechanics (Ruebeck–James–Mahoney–Crutchfield): what the fresh state tells about the observable future *beyond the current observation*. An $\varepsilon$-machine has zero oracular information — its state is a function of the observation past — so for any system whose memory is purely inferential the discount vanishes and the full cryptic charge stands. A system whose memory is written into the world's future (stigmergy: pheromone trails, notes, caches flushed to disk) carries positive oracular information, and *that* — not transfer entropy per se — is the exact currency of the export discount:

$$\textbf{dissipation} \;\ge\; \textbf{hidden state information} \;-\; \textbf{oracular state information} \;-\; \textbf{initial coding cost}.$$

Corollary 5 and v1's bTE corollary are kinetically weakened shadows of this statement. When the oracular sum exceeds the cryptic burden the bound goes negative and net work extraction becomes possible, as Table 6 realizes. Empirically $\sum \mathrm{bTE} \le \sum\Phi \le \sum\mathrm{Orac}$ at partial relaxation in all sampled models, but the first inequality reverses at $r=1$ (where $\Phi = \Delta \le \mathrm{bTE}$): no universal ordering between $\Phi$ and bTE exists, which is the abstract content of the withdrawal above. **[empirical]**

**Table 6 — feedback ledger with the oracular column** (copy environment: $x_{t+1} = s_t$ w.p. $g$, else $x$ flips w.p. $0.3$; two states, $J=1.5$, $T=6$; nats; `gen_tables.py`). Bounds: Thm 5 (exact $\Phi$), Cor 5 (kinetic), Cor 6 (oracular), Massey $-\mathcal{T}_{S\to X}$ (§7):

| $g$ | $r$ | $\beta W_{\mathrm{diss}}$ | $\sum$cry | $\sum\Phi$ | $\sum$bTE | $\sum$Orac | $I[S_0;X]$ | Thm 5 | Cor 5 | Cor 6 | $-\mathcal{T}_{S\to X}$ |
|------|-----|--------|-------|-------|-------|-------|-------|--------|--------|--------|--------|
| 0.00 | 0.5 | +1.107 | 0.310 | 0.000 | 0.000 | 0.000 | 0.000 | +0.310 | +0.310 | +0.310 | 0.000 |
| 0.00 | 1.0 | +1.687 | 0.927 | 0.000 | 0.000 | 0.000 | 0.000 | +0.927 | +0.927 | +0.927 | 0.000 |
| 0.30 | 0.5 | +0.459 | 0.344 | 0.220 | 0.170 | 0.240 | 0.017 | +0.107 | −1.373 | +0.088 | −0.187 |
| 0.30 | 1.0 | +0.848 | 0.652 | 0.157 | 0.157 | 0.157 | 0.000 | +0.496 | +0.496 | +0.496 | −0.157 |
| 0.70 | 0.5 | −0.299 | 0.302 | 0.953 | 0.784 | 1.006 | 0.081 | −0.732 | −3.840 | −0.784 | −0.865 |
| 0.70 | 1.0 | −0.271 | 0.291 | 0.914 | 0.914 | 0.914 | 0.000 | −0.623 | −0.623 | −0.623 | −0.914 |
| 0.95 | 0.5 | −0.721 | 0.085 | 1.591 | 1.444 | 1.629 | 0.136 | −1.642 | −5.940 | −1.680 | −1.580 |
| 0.95 | 1.0 | −0.970 | 0.050 | 1.962 | 1.962 | 1.962 | 0.000 | −1.912 | −1.912 | −1.912 | −1.962 |

Certifies: Theorem 1 under feedback; $\Phi \ge 0$ throughout; $\Phi = \mathrm{bTE} = \mathrm{Orac}$ at $r=1$ (Corollary 6 = v1's bound there); Corollary 6 dominates Corollary 5 wherever they differ (dramatically at partial relaxation: $+0.088$ vs $-1.373$ at $g{=}0.3$); every bound holds in the net-work-extraction rows. Note also the honest comparison with the Massey bound: Corollary 6 is tighter in most feedback rows but **not all** ($g{=}0.95, r{=}0.5$: Massey $-1.580$ beats Corollary 6's $-1.680$) — v1's claim of strict dominance over the transfer-entropy bound is withdrawn; the two bounds cross, and their maximum is the operative floor.

---

## 7. The dual filtration: the Massey directed-information second law

Choosing **past**-conditioned filtrations in Lemma 2 instead ($G = X_{1:t+1}$ post-quench, $G = X_{1:t}$ pre-quench) makes the residuals contract under feedback *automatically* (the past cannot peek at fresh noise), while the information terms telescope to a directed sum:

> **Theorem 7 (Dual identity → directed-information second law). [proved; verified to $10^{-14}$; Massey equality verified to $2.7\times10^{-15}$ on 60 feedback models; `item8_massey.py`]**
> $$\beta\langle W_{\mathrm{diss}}^{\mathrm{tot}}\rangle \;=\; -\sum_t I[S_t;\,X_{t+1}\mid X_{1:t}] \;+\; \sum_t (P_t - P''_t), \qquad \sum_t(P_t - P''_t) \ge 0.$$
> Moreover, by the same screening property as Lemma 5 ($X_{t+1} \perp S_{0:t-1} \mid S_t, X_{1:t}$), the state-level transfer entropy equals the history-level one, $I[S_t;X_{t+1}\mid X_{1:t}] = I[S_{0:t};X_{t+1}\mid X_{1:t}]$, and the sum is **exactly Massey's directed information** $\mathcal{T}_{S\to X} = I(S^T \to X^T)$. Hence
> $$\beta\langle W_{\mathrm{diss}}^{\mathrm{tot}}\rangle \;\ge\; -\,I(S^T \to X^T),$$
> verbatim the directed-information second law (Massey 1990; Sagawa–Ueda; Ito–Sagawa). The Massey–Kim conservation law $I[S^T;X^T] = I(S^T\to X^T) + I(X^T \to S^T, \text{delayed})$ holds in the model to machine precision; the "resource" and "liability" filtrations split exactly this conserved total.

**Unification.** Theorems 1 and 7 are the *same* work identity split along two filtrations. Future-conditioned splitting yields "prediction pays" (Still-type); past-conditioned splitting yields "action pays back" (Sagawa–Ueda-type). In the tested feedback regimes the interpolated bounds of §6 are typically, but not always, tighter than the pure directed-information bound (Table 6); the bounds cross, and $\max$ of the two is the operative floor. This closes v1's Open Problem 1.

---

## 8. Numerical certificates

All identity and bound checks by exact enumeration of the full joint path distribution (no sampling); the chaotic-map entropies of §5.1 by exact interval arithmetic; only Table 5 (baker) and §8.1 involve sampling, with stated controls.

**Table 1 — no back-action** (hidden 3-phase environment, emission noise $\eta$, phase-slip probability, two-state system, partial relaxation $r=0.7$, $T=8$; nats):

| η | slip | βW_diss | Σ cryptic | Σ Still | residual | identity gap |
|------|------|---------|-----------|---------|----------|--------------|
| 0.02 | 0.02 | 5.026 | 0.219 | 0.475 | 4.807 | 6e−15 |
| 0.02 | 0.20 | 4.453 | 0.613 | 0.757 | 3.840 | 1e−14 |
| 0.10 | 0.02 | 4.763 | 0.550 | 0.708 | 4.213 | 9e−16 |
| 0.10 | 0.20 | 4.365 | 0.797 | 0.862 | 3.568 | 9e−16 |
| 0.30 | 0.02 | 4.315 | 0.968 | 0.983 | 3.347 | 5e−15 |
| 0.30 | 0.20 | 4.215 | 1.004 | 1.008 | 3.212 | 9e−16 |

Certifies: Theorem 1 identity; residual ≥ 0; both bounds valid; learning duality (1e−15); Still ≥ cryptic in aggregate, as Theorem 4 requires; residual dominance — now addressed by Table 2's hybrid bound rather than lamented.

Tables 2–6 appear in-line above (§4.1, §5, §5.1, §6). Additional certification runs: Lemmas 1–3 hardened over 60 random feedback models at machine precision (`harden.py`); Theorem 6's identity and inequalities over 200 models plus a 12,000-model adversarial search for the sign of $\Phi$ (`item3_adversarial.py`, `item3_theoremD.py`); Theorem 4 over 30 models in three environment classes (`item2_theoremC.py`); the Massey equality, bTE history-collapse, and Massey–Kim conservation over 60 models (`item8_massey.py`).

### 8.1 Finite-sample estimation of the bounds

The horizon family is certifiable from transcripts in principle (§5, remark iv); §8.1 quantifies the practice. Trajectories sampled from the exact path law of the three-phase environment (Table 2 model, $r{=}0.7$: exact $\beta W = 4.700$, $\sum\text{Still} = 0.735$, $\sum\text{cry} = 0.605$); 20 replicates per sample size.

**Table 7 — plug-in bias, Still vs cryptic** (mean ± sd of estimate − exact; `item6_bias.py`):

| $N$ | Still bias | cryptic bias (plug-in) | cryptic bias (Miller–Madow) |
|---|---|---|---|
| $10^3$ | +0.009 ± 0.032 | **+0.094 ± 0.038** | +0.067 ± 0.040 |
| $10^4$ | −0.004 ± 0.012 | +0.009 ± 0.012 | −0.000 ± 0.012 |
| $10^5$ | −0.001 ± 0.004 | +0.002 ± 0.004 | +0.000 ± 0.004 |

Full-future conditioning inflates the plug-in cryptic estimate an order of magnitude more than the Still estimate at small $N$ (the conditioning alphabet grows as $|X|^{T-t}$); Miller–Madow removes part of it, and the crossover sample size scales with the conditioning-cell count. **The estimated bound is not a certificate:** the plug-in error decomposes as $\hat I = I + \mathrm{KL}_{\text{marg}} - \mathrm{KL}_{\text{cond}}$, which is not one-sided — an estimated "dissipation floor" can exceed the true floor and, in tight systems, manufacture false second-law violations. A certified floor requires a trusted *marginal* probe model (making $\mathrm{KL}_{\text{marg}}$ a known quantity), i.e., the probing burden falls on the unconditional window statistics, not on the state-conditional ones.

Verification scripts: `engine.py` (exact enumeration engine), `smoke.py`, `harden.py`, `item1_hybrid.py`, `item2_pad.py`, `item2_theoremC.py`, `item3_adversarial.py`, `item3_theoremD.py`, `item5a_tent.py`, `item5b_baker.py`, `item6_bias.py`, `item7_kw.py`, `item8_massey.py`, `gen_tables.py`, shipped alongside. (v1 scripts `verify.py`, `feedback.py`, `verify_horizon.py`, `verify_takens.py` are superseded by the engine.)

---

## 9. Relation to prior work; honest novelty assessment

- **Still–Sivak–Bell–Crooks (2012).** Corollary 2 shows their bound is *complete* for Markov signals. v2 goes further: Theorem 4 shows that without back-action their bound, summed, is the tightest of the entire sliding-window family — the trajectory extension's aggregate advantage lives entirely in the feedback regime, and its no-feedback value is diagnostic (profile shape) and kinetic (Theorem 2's pairing).
- **Crutchfield–Ellison–Mahoney; Ruebeck–James–Mahoney–Crutchfield.** The cryptic term is the driven, finite-horizon analogue of CEM crypticity; the discount of Corollary 6 is exactly finite-horizon *oracular information*. The identity "dissipation ≥ crypticity − oracularity − coding cost" appears to be new; it gives the computational-mechanics quantities a ledger in which they are the two sides of one physical account.
- **Sagawa–Ueda; Ito–Sagawa; Ito (backward TE); Massey; Kim.** Theorem 7 is now identified *exactly* with Massey's directed-information second law (state-TE = history-TE in this model class, Lemma 5's screening); Lemma 3 is Ito's backward transfer entropy, and the v1 corollary's failure at partial relaxation is a cautionary instance of the loss/gain asymmetry Ito emphasizes. The Massey–Kim conservation law is verified inside the model.
- **Crooks–Still (2019).** The filtration-choice mechanism is a systematic version of their conditioning constructions.
- **Kolchinsky–Wolpert.** The dictionary conjectured in v1 is now closed: $C_t$ *is* the mismatch cost of the relaxation stroke (verified identity, §6).
- **Dobrushin coefficients / $f$-divergence contraction.** Theorem 2 imports the standard domination of all $f$-divergence contraction coefficients by the TV coefficient; the application to the prediction ledger appears new.
- **Takens; Sauer–Yorke–Casdagli; Stark et al.; Fraser–Swinney.** §5.1 is delay-embedding theory read as a statement about which conditional-information functionals can be nonzero — with the v2 correction that the reading is sharply asymmetric under future-only conditioning, where embedding closure fails even for invertible dynamics with generic quantized observables.

**Caveats.** Derived and machine-checked across two sessions, the second adversarial; the surviving claims withstood 12,000-model optimization attacks on the sign of $\Phi$ and the bTE substitution, and 0-violation sweeps on Theorem 4 — but "verified" remains model-class evidence, not proof, wherever tagged so. Discrete two-stroke dynamics; continuous time is open. Cryptic information inherits the coarse-graining dependence of all such quantities: it is a property of system-plus-description.

---

## 10. Implications for learning systems

The thermodynamic content does not constrain GPU joules (real hardware is ~10 orders above any Landauer-scale floor). What transfers is the representational identity, pure information theory once $\beta$ is stripped:

1. **Future-conditioned compression.** The correct penalty for a recurrent state is $I[S_t;X_t\mid X_{t+1:T}]$ — bits not recoverable from the future — rather than the marginal bottleneck, which squeezes predictive and wasted bits alike. Implementable with a bidirectional teacher (critic predicting $x_t$ from $(s_t, x_{>t})$ vs from $x_{>t}$ alone). §8.1's caution applies: the state-conditional probe is the estimation-hungry one, and the regularizer estimate is biased upward exactly where data is short.
2. **Agents: compress or externalize, with the exchange rate now exact.** Corollary 6 extends the principle to systems whose outputs shape their inputs (RL, tool use, deployed models): the regularizer is **cryptic memory minus oracular memory** — bits hidden from the future minus bits the future will testify to. Writing state into the environment (scratchpads, files, the world itself) is a legitimate substitute for internal retention at a 1:1 rate in nats, and the correct credit is the *oracular* term $I[S_{t+1};X_{t+2:T}\mid X_{t+1}]$, not raw transfer entropy: only state information the future re-exposes *beyond what the current input already shows* earns the discount.
3. **Cache eviction with write-out.** A cached entry is safely evictable if non-cryptic given retained + upcoming context, *or* if its content has been exported to a persistent substrate the future computation will read — the oracular term is precisely the credit for the latter, and Theorem 6 guarantees the credit never overdraws ($\Phi \ge 0$).
4. **Thermodynamic hardware.** Where $\beta$ is literal (analog/stochastic computing, molecular machines), Corollary 6 is a design law valid at *any* relaxation speed — v1's version required complete relaxation and is now known to fail without it — and Theorem 2 supplies the kinetic complement: per-update energy floors are cryptic retention net of environmental write-out, plus the un-contracted fraction of each equilibration.

---

## 11. Open problems

Closed in v2: v1's Problems 1 (Massey identification — Theorem 7), 2 (sign of $\Phi$ — Theorem 6), and 3 (partial relaxation with feedback — Corollaries 5–6); v1's Problem 7 is partially closed (Lyapunov knee verified with scaling; two-knee structure refuted for non-invertible dynamics) and is restated below. Remaining and new:

1. **Continuous time.** Merging with Horowitz–Esposito information flow should replace sums with integrals of a cryptic-information *rate*; the $h$-transform structure suggests Schrödinger-bridge connections. **[open]**
2. **Saturation.** Whether any non-trivial physical system saturates the trajectory bound away from quasi-static limits; whether quantum implementations lower the cryptic floor. **[open]**
3. **Tightness of the interpolation under feedback.** Table 6 shows Corollary 6 and the Massey bound cross; characterize the crossing, and derive the feedback horizon family with its $\Phi^{(k)}$ penalties. **[open]**
4. **Two-sided windows.** Define the past-and-future windowed family permitted by Lemma 2, prove its residual signs, and show it realizes Takens closure for invertible dynamics where the future-only family provably does not (§5.1). Quantify the stable-direction information recoverable from the future (the baker's-map defect) analytically. **[open]**
5. **Stochastic Takens inside the formalism.** Prove $K^*(\delta) \lesssim \log(1/\delta)/(\text{filter contraction rate})$ as a theorem about the $\bar\alpha$-spectrum under filter stability; extend the folding-entropy asymptote ($N_\infty = \lambda$ for full-branch maps, verified) to a theorem for general piecewise-expanding and higher-dimensional systems. **[open]**
6. **Certified estimation.** Construct the trusted-marginal-probe estimator of §8.1 with finite-sample one-sided guarantees, so that transcript-based dissipation floors become certificates. **[open]**
