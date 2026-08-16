# A Trajectory-Level Identity for the Thermodynamics of Prediction, With and Without Back-Action

**Author:** [author list]
**Date:** August 2026

---

## Abstract

Still, Sivak, Bell and Crooks (2012) bounded dissipation below by per-step *nostalgia* — memory minus predictive power — absent back-action. We derive the trajectory-level generalization and its kinetic completion. The setup is an exact identity, valid under arbitrary back-action: dissipated work equals the summed *cryptic information* $\sum_t I[S_t;X_t\mid X_{t+1:T}]$ — what the state stores about the present that the signal's future never discloses — plus a residual of characterized sign; supplementing the information terms with one kinetic number per bath, the relaxation kernel's Dobrushin coefficient, converts the residual into a computable charge. Without back-action, summed window nostalgia is monotone decreasing in window width, so the 2012 bound is provably the tightest of the sliding-window family; the information–kinetic hybrid then recovers 74–100% of dissipated work where information alone recovers 4–30%, exactly at complete relaxation. With back-action, the feedback penalty is proved non-negative and equals the state's *oracular information* about the observable future, yielding
$$\beta\langle W_{\mathrm{diss}}\rangle \ \ge\ \sum_t I[S_t;X_t\mid X_{t+1:T}] \ -\ \sum_t I[S_{t+1};X_{t+2:T}\mid X_{t+1}] \ -\ I[S_0;X_{1:T}]:$$
*an agent pays for memory by dissipating it or by writing it into the world's future.* The dual filtration of the same identity is exactly Massey's directed-information second law. All identities and bounds are machine-verified by exact enumeration, including net-work-extraction regimes.

---

## 1. Introduction

A physical system driven by a structured signal cannot avoid representing that signal: its microstate becomes statistically correlated with the drive, and thermodynamics prices the correlation. Still, Sivak, Bell and Crooks [1] made this precise for a system with no influence on its input: the dissipated work per driving step is at least $k_BT$ times the system's *nostalgia*, the information it retains about the previous input beyond what is useful for predicting the next one. The result initiated a line of work connecting predictive inefficiency to dissipation [1–4], complementary to the feedback and measurement second laws in which information about a system is a *resource* for work extraction [5–8].

This paper develops both lines from a single exact identity and maps, with proofs and machine-checked certificates, exactly where each has content. Our object is the two-stroke driven chain of [1] over a finite horizon $T$: at each step the environment signal $x_t \to x_{t+1}$ quenches the system's energy landscape, and the system then relaxes one step toward the new equilibrium. The environment may be an arbitrary stochastic process — hidden-Markov, long-memory, non-stationary — and, in the second half of the paper, may respond to the system's state (*back-action*, the agent setting).

Our contributions are the following.

**1. An exact, feedback-robust identity (Theorem 1).** Total dissipated work equals the summed *cryptic information* $\sum_t I[S_t; X_t \mid X_{t+1:T}]$ — what the state stores about the present signal that the entire future of the signal never discloses again — plus a residual $\sum_t(R_t - R''_t)$ built from relative entropies to instantaneous equilibrium. The identity uses no causal assumption; every subsequent result is a sign analysis of the residual under a choice of conditioning filtration.

**2. The ordering of the window family (Theorem 4).** The 2012 bound and the cryptic bound are the $k{=}1$ and $k{=}T$ endpoints of a sliding-window family of valid lower bounds. We prove that, without back-action, the summed family is *monotone decreasing* in the window width: the 2012 bound is always the tightest aggregate member. In particular, a natural conjecture — that "one-time-pad" environments, whose present symbol is explained only by synergy between state and future, separate the cryptic bound above the one-step bound — is false in aggregate for every autonomous environment, although it holds per-step. Rising summed window profiles are therefore a *certificate of back-action*, observable on the information layer alone.

**3. A kinetic completion (Theorem 2).** In all tested regimes the information bounds recover only 4–30% of dissipation; the deficit is kinetic, not informational. Supplementing the ledger with a single number per bath — the Dobrushin contraction coefficient of the relaxation kernel — yields a hybrid bound recovering 74–100% of dissipated work, exact at complete relaxation. The message inverts the standard looseness critique of information bounds: the missing dissipation is a property of the hardware, not the signal, and one kernel constant prices it.

**4. Quantized chaotic observation, computed exactly (§6).** For expanding maps observed at finite precision we compute the window profile by exact interval arithmetic. The profile is a rising sigmoid with a single knee at the Lyapunov resolution horizon $k^* \approx \ln(1/\delta)/\lambda$ (scaling verified) whose asymptote equals the map's *folding entropy* — the profile is a dissipation-side meter of information destruction, exactly $\lambda$ for full-branch maps. For invertible maps, generic observables lower but do not close the asymptote under future-only conditioning: future words cannot resolve the stable direction. This corrects the natural delay-embedding intuition and locates precisely what a Takens-type closure requires (two-sided windows).

**5. The oracular discount (Theorems 5–6, Corollary 6).** With back-action the residual acquires a per-step penalty $\Phi_t$. We prove $\Phi_t \ge 0$ via an exact identity: $\Phi_t$ equals the state's *oracular information* about the observable future, $I[S_{t+1}; X_{t+2:T} \mid X_{t+1}]$, minus a non-negative defect with a twin-channel (data-processing) interpretation. The corollary is a purely informational feedback bound — dissipation is at least hidden state information minus oracular state information minus an initial coding cost — valid at any relaxation speed. The naive bound obtained by substituting backward transfer entropy for $\Phi_t$ is shown *invalid* at partial relaxation by explicit counterexample, and is recovered as the complete-relaxation limit of our bound.

**6. Unification with the directed-information second law (Theorem 7).** The dual (past-conditioned) filtration in the same identity yields the feedback second law, which we identify exactly with Massey's directed information: state-level and history-level transfer entropies coincide in this model class. "Prediction pays" and "action pays back" are two σ-algebra choices in one decomposition, splitting a conserved total (Massey–Kim).

**7. Certification and estimation (§9).** Every identity and bound is machine-verified by exact enumeration of the full joint path distribution, including adversarially optimized model searches (12,000 models attacking the sign of $\Phi_t$) and regimes of net work extraction. We further characterize finite-sample estimation of the bounds from sampled trajectories: full-future conditioning inflates plug-in estimates an order of magnitude more than one-step terms at small sample size, and plug-in "certificates" are not one-sided.

**Organization.** §2 fixes the model. §3 states two lemmas and the exact identity. §4 treats autonomous environments: the trajectory bound, the window family and its ordering, and the hybrid bound. §5–6 analyze when the family can bite, including exact chaotic-map computations. §7 treats back-action. §8 gives the dual filtration and the Massey identification. §9 describes numerical certification and finite-sample estimation. §10 discusses related work; §11 concludes with implications and open problems. Proofs longer than a few lines are collected in Appendix A; Appendix B documents reproducibility.

---

## 2. Setup and conventions

Discrete time $t = 0, \dots, T$. Environment states $x$, system states $s$, both finite. The system's energy landscape $E(s|x)$ depends on the current environment state. Inverse temperature $\beta = 1/k_BT$; informations in nats; $\pi_x(s) \equiv e^{-\beta E(s|x)}/Z(x)$ the equilibrium distribution at landscape $x$; $F_{\mathrm{eq}}(x) = -k_BT \ln Z(x)$.

**Two-stroke dynamics.** Each step $t \to t+1$ consists of:

1. *Drive stroke (quench).* The environment jumps $x_t \to x_{t+1}$ with kernel $\mathcal{T}(x_{t+1} \mid x_t, s_t)$. The landscape shifts at fixed $s_t$; work $W(t) = E(s_t|x_{t+1}) - E(s_t|x_t)$ is done on the system.
2. *Relaxation stroke.* The system updates $s_t \to s_{t+1}$ by a Markov kernel $K_{x_{t+1}}(s_{t+1}|s_t)$ with stationary distribution $\pi_{x_{t+1}}$ (e.g., detailed-balanced), exchanging heat with the bath. The kernel's fresh noise is independent of everything else.

**Back-action.** If $\mathcal{T}$ depends on $s_t$, the system influences its own input — the agent setting. The no-back-action case is $\mathcal{T}(x_{t+1}|x_t,s_t) = \mathcal{T}(x_{t+1}|x_t)$, or more generally an autonomous (possibly hidden-state, non-Markov-in-observables) environment process. Nothing in §3 assumes either case.

**Initialization.** $s_0$ is drawn from the equilibrium distribution of a flat reference landscape ($E \equiv$ const), independent of the environment; the first drive stroke quenches from the flat landscape to $x_1$. Any equilibrium start works; flatness only simplifies boundary terms.

**Dissipated work.** $\beta\langle W_{\mathrm{diss}}\rangle \equiv \beta\langle W_{\mathrm{tot}}\rangle - \beta\,\Delta F_{\mathrm{eq}}$, with $\Delta F_{\mathrm{eq}}$ evaluated along the realized landscape sequence and averaged.

**Notation.** $X_{a:b} = (X_a, \dots, X_b)$. At step $t$, the state $s_t$ (formed under $x_t$) experiences the quench to $x_{t+1}$. Throughout, $q \equiv K_{x_{t+1}} \, p(s_t \mid x_{t+1:T})$ denotes the *no-peeking pushforward* of the future-conditioned state distribution through the bare relaxation kernel.

---

## 3. Two lemmas and the exact identity

**Lemma 1 (Conditioning-robust work identity).**
*For any random variable $C$ that determines $(x_t, x_{t+1})$ — e.g., any superset of the environment trajectory —*
$$\beta\big\langle W(t) - \Delta F_{\mathrm{eq}}(t)\big\rangle \;=\; \big\langle D[\,p(s_t|C)\,\|\,\pi_{x_{t+1}}]\big\rangle \;-\; \big\langle D[\,p(s_t|C)\,\|\,\pi_{x_t}]\big\rangle .$$

*Proof.* $D[p(s|C)\|\pi_x] = -H[S|C{=}c] + \beta\langle E(s|x)\rangle_{p(\cdot|c)} - \beta F_{\mathrm{eq}}(x)$. Subtracting the two divergences, the conditioning-dependent entropy terms cancel; averaging over $C$ gives $\beta\langle E(s_t|x_{t+1}) - E(s_t|x_t)\rangle - \beta\langle\Delta F_{\mathrm{eq}}\rangle$. No causal structure is used. ∎

**Lemma 2 (Filtration split).**
*For any sub-conditioning $G \subseteq C$ with $x^\*$ measurable with respect to $G$,*
$$\big\langle D[\,p(s|C)\,\|\,\pi_{x^\*}]\big\rangle \;=\; I[S;C] - I[S;G] \;+\; \big\langle D[\,p(s|G)\,\|\,\pi_{x^\*}]\big\rangle .$$

*Proof.* Write $\log\frac{p(s|C)}{\pi_{x^\*}(s)} = \log\frac{p(s|C)}{p(s)} + \log\frac{p(s)}{p(s|G)} + \log\frac{p(s|G)}{\pi_{x^\*}(s)}$ and average over the true joint. ∎

The entire theory consists of applying Lemma 1 with $C$ the full environment trajectory and choosing the filtration $G$ in Lemma 2: future-conditioned choices produce prediction-type bounds; past-conditioned choices produce feedback-type bounds.

Apply Lemma 1 with $C = X_{1:T}$ and Lemma 2 with, for the post-quench term ($x^\* = x_{t+1}$), $G = X_{t+1:T}$, defining $R_t \equiv \langle D[\,p(s_t|x_{t+1:T})\,\|\,\pi_{x_{t+1}}]\rangle \ge 0$; and for the pre-quench term ($x^\* = x_t$), $G = X_{t:T}$, defining $R''_t \equiv \langle D[\,p(s_t|x_{t:T})\,\|\,\pi_{x_t}]\rangle \ge 0$. The $I[S_t;X_{1:T}]$ terms cancel between the two applications — this is why no causal assumption enters — leaving $I[S_t;X_{t:T}] - I[S_t;X_{t+1:T}] = I[S_t;X_t \mid X_{t+1:T}]$ by the chain rule. Summing over steps:

> **Theorem 1 (Cryptic-information identity).**
> $$\beta\langle W_{\mathrm{diss}}^{\mathrm{tot}}\rangle \;=\; \sum_{t} I[S_t;\,X_t \mid X_{t+1:T}] \;+\; \sum_t\big(R_t - R''_t\big)$$
> *for arbitrary environment statistics and arbitrary back-action.*

We call $I[S_t;X_t\mid X_{t+1:T}]$ the **cryptic information**: what the state stores about the present signal that the entire future of the signal will never disclose again. Information about $x_t$ that the future reveals anyway makes no appearance — it is thermodynamically free, whether or not the system ever "uses" it. The term is the finite-horizon, driven-system analogue of crypticity in computational mechanics [9,10], with the physical memory $S$ in place of causal states. Everything below is a sign analysis of $\sum_t(R_t - R''_t)$.

---

## 4. Autonomous environments

Assume the environment is autonomous: an arbitrary process — hidden-Markov, long-memory, non-stationary — not influenced by $S$. Two facts follow. **(CI)** $S_t \perp X_{t+1:T} \mid X_{1:t}$: the state, a function of the past signal and private noise, is conditionally independent of the future signal. **(KM)** Conditioned on $X_{t+1:T}$, the relaxation stroke is still the bare kernel $K_{x_{t+1}}$ — the future cannot peek at the update — so $p(s_{t+1}|x_{t+1:T}) = q$ exactly and, by contraction of relative entropy to the kernel's fixed point, $R''_{t+1} \le R_t$. Pairing $R_t$ with $R''_{t+1}$, with $R''_0 = 0$ (equilibrium start, no influence on $X$) and the final boundary non-negative:

> **Corollary 1 (Trajectory bound).** $\beta\langle W_{\mathrm{diss}}^{\mathrm{tot}}\rangle \;\ge\; \sum_{t} I[S_t;\,X_t \mid X_{t+1:T}]$.

> **Corollary 2 (Markov collapse).** *If the environment is Markov in its observables, screening reduces Corollary 1 exactly to the summed Still–Sivak–Bell–Crooks bound. The trajectory extension has content only for non-Markovian environments.*

> **Corollary 3 (Learning duality).** *Chain-rule algebra rearranges Corollary 1's underlying identity into $\beta\langle W_{\mathrm{diss}}^{\mathrm{tot}}\rangle \ge \sum_t (I[S_{t+1};X_{t+1:T}] - I[S_t;X_{t+1:T}]) - I[S_T;X_T]$: total anticipation gained about the future is paid in dissipation. The nostalgia-type and Sagawa–Ueda-type readings are one identity read in two directions.*

### 4.1 The horizon family and its ordering

Fix a window width $k \ge 1$ and choose matched finite windows in Lemma 2: $G = X_{t+1:t+k}$ post-quench, $G = X_{t:t+k-1}$ pre-quench (windows clipped at $T$). The information terms combine to the **horizon-$k$ nostalgia**
$$N_k(t) \;\equiv\; I[S_t;\,X_{t:t+k-1}] \;-\; I[S_t;\,X_{t+1:t+k}],$$
the drop in the state's information about a width-$k$ window as the window slides one step into the future.

> **Theorem 3 (Horizon family).** *Without back-action, for every $k \ge 1$ simultaneously, $\beta\langle W_{\mathrm{diss}}^{\mathrm{tot}}\rangle = \sum_t N_k(t) + \Sigma^{(k)}$ with $\Sigma^{(k)} \ge 0$.*

At $k = 1$, $N_1(t) = I[S_t;X_t] - I[S_t;X_{t+1}]$ is the Still–Sivak–Bell–Crooks nostalgia exactly; at $k = T$, telescoping gives $N_T(t) = I[S_t;X_t \mid X_{t+1:T}]$, Corollary 1. Defining the teacher-forced autoregressive informations $\alpha_k(t) = I[S_t;X_{t+k}\mid X_{t:t+k-1}]$ and $\bar\alpha_{k}(t) = I[S_t;X_{t+k}\mid X_{t+1:t+k-1}]$, the chain rule gives the increment formula $N_{k+1}(t) - N_k(t) = \alpha_k(t) - \bar\alpha_{k+1}(t)$; for Markov environments both spectra vanish and the family is flat, generalizing Corollary 2.

One might hope to improve on both endpoints by maximizing over $k$. The maximum is in fact known in closed form:

> **Theorem 4 (Summed horizon monotonicity).** *Without back-action, $\sum_t N_{k+1}(t) \le \sum_t N_k(t)$ for every $k \ge 1$. Hence $\sum_t N_1 \ge \sum_t N_2 \ge \dots \ge \sum_t N_T$: the summed Still bound is the tightest member of the family.*

*Proof: Appendix A.1.* The proof pairs the increment terms telescopically using two facts: the fresh-noise state $S_1$ is independent of the autonomous future given $X_1$, and a conditional data-processing inequality along $S_{t+1} \leftarrow S_t$ bounds each later-state AR term by an earlier future-only term.

Three consequences. *(i)* The maximum over $k$ is attained at $k = 1$; the profile's diagnostic value (below) is in shape, not bound improvement. *(ii)* The pad conjecture fails in aggregate: in a one-time-pad environment $x_t = a_t \oplus b_t$ (future later reveals $b_t$; system stores $a_t$) the cryptic term beats the Still term *at the pad step*, exactly as the synergy intuition suggests, but the sums never cross — the deficit is repaid at neighboring steps (verified: 0/30 violations across random, hidden-Markov, and designed pad environments). *(iii)* Conversely, any measured $\sum_t N_{k+1} > \sum_t N_k$ **falsifies the autonomous-environment hypothesis** on the information layer, before any thermodynamics is invoked: rising summed profiles are a certificate of back-action. Feedback realizes the escape hatch: a designed feedback pad — the environment re-echoes a memory bit two steps later — achieves $\sum_t N_T - \sum_t N_1 = +0.53$ nats, and under feedback the Still sum can go negative ($-0.23$ observed) while the cryptic sum cannot (§7).

**Table 1 — horizon profiles** (two-state system, $r = 0.7$, $T = 8$; nats):

| $k$ | HMM ($\eta{=}.1$, slip $.1$), $\beta W{=}4.593$ | echo $x_t = x_{t-3}\oplus\varepsilon(.05)$, $\beta W{=}4.000$ |
|---|------|------|
| 1 (Still) | 0.780 | 1.075 |
| 2 | 0.708 | 1.029 |
| 3 | 0.687 | 0.478 |
| 4 | 0.684 | 0.478 |
| 8 (cryptic) | 0.680 | 0.478 |

The echo environment's cliff sits at the echo lag: the profile reads off the state's forecasting depth (flatness onset = Markov order, §5), while Theorem 4 guarantees the monotone envelope.

**Remarks on autoregression.** The chain rule decomposes every window objective exactly into teacher-forced next-symbol conditionals, so a model optimal at each one-step conditional is optimal for every long-horizon joint simultaneously — temporal factorization along the causal order is free, in contrast with the modularity cost of spatial decomposition [11]. Every quantity this ledger prices is teacher-forced: the environment always delivers its realized symbols; the world never rolls out from the model. Teacher-forced log-loss is therefore not a proxy for the physically priced objective; it *is* that objective, and every term in the family is a difference of teacher-forced probe log-losses — certifiable in principle from transcripts, with the finite-sample caveats quantified in §9.2.

### 4.2 The hybrid bound: charging the un-contracted fraction

In all tested regimes the residual dominates every information bound by factors of 3–20 (§9, Table 5) — the standard looseness critique. The deficit is kinetic, and one number per bath prices it. Re-index the residual as $\sum_t (R_t - R''_t) = \sum_{t \le T-2}(R_t - R''_{t+1}) + R_{T-1}$. Without back-action, $R''_{t+1} = \langle D[pK \| \pi K]\rangle$ contracts by the kernel's KL contraction coefficient, which is dominated by the Dobrushin (total-variation) coefficient $\eta_{\mathrm{TV}}(K_x)$ [12,13]. For the jump kernel $K = r\pi\mathbf{1}^\top + (1-r)\,\mathrm{Id}$, $\eta_{\mathrm{TV}} = 1 - r$.

> **Theorem 2 (Hybrid information–kinetic bound).** *Without back-action,*
> $$\beta\langle W_{\mathrm{diss}}^{\mathrm{tot}}\rangle \;\ge\; \sum_t I[S_t;X_t\mid X_{t+1:T}] \;+\; \sum_{t\le T-2}\big(1 - \eta_{\mathrm{TV}}(K_{x_{t+1}})\big)\,Q_t \;+\; R_{T-1},$$
> *where $Q_t$ is $R_t$ itself or any Lemma-2 coarsening of it (certified-computable choice: $Q_t = \langle D[\,p(s_t|x_{t+1})\,\|\,\pi_{x_{t+1}}]\rangle$, requiring only one-step statistics). The bound is exact at complete relaxation.*

*Proof: Appendix A.2.*

**Table 2 — closing the residual** (three-phase hidden-cycle environment: hidden period-3 phase, slip 0.05, emission noise 0.1, $J = 2$, $T = 8$; nats):

| $r$ | $\beta W_{\mathrm{diss}}$ | $\sum$ cryptic | $\sum$ Still | hybrid ($Q$ one-step) | hybrid ($Q = R_t$) | hybrid/W |
|------|------|------|------|------|------|------|
| 0.30 | 2.105 | 0.088 | 0.096 | 1.547 | 1.552 | 74% |
| 0.50 | 3.362 | 0.273 | 0.314 | 2.582 | 2.611 | 78% |
| 0.70 | 4.700 | 0.605 | 0.735 | 3.867 | 3.971 | 84% |
| 0.90 | 6.044 | 1.155 | 1.475 | 5.382 | 5.675 | 94% |
| 1.00 | 6.675 | 1.548 | 2.013 | 6.210 | 6.675 (exact) | 100% |

The pure information bounds recover 4–30% of dissipation across this sweep; the hybrid recovers 74–100%, the certified-computable one-step $Q$ giving up only a few percent. The information terms were never supposed to price the kinetic cost; a single Dobrushin coefficient per bath — a property of the hardware, not of the signal — prices almost all of it.

---

## 5. When can the family bite? Vacuousness and diagnostics

The results of this section live on the information layer: the dissipation inequality is not used in any proof. Their thermodynamic content is classificatory — they determine when Theorem 3 is vacuous and when its contrapositive is informative.

> **Proposition 1 (Takens vacuousness).** *Let $x_t = h(z_t)$, $z_{t+1} = f(z_t)$, with $f$ a $C^2$ diffeomorphism of a compact invariant set $A$ of box dimension $d_B$, $h$ in the prevalent set of observables of the Takens / Sauer–Yorke–Casdagli theorems [14,15], observations at infinite precision, no back-action, and $K^* = \lfloor 2d_B\rfloor + 1$. Then almost surely every width-$K^*$ observation window determines the underlying state; by invertibility, consecutive width-$k$ windows ($k \ge K^*$) generate the same σ-algebra as $z$. Hence for every physical state $S_t$, however constructed, $N_k(t) = 0$ and $\bar\alpha_{k+1}(t) = 0$ for all $k \ge K^*$: the horizon family is identically vacuous beyond the embedding window.*

*Proof sketch.* Injectivity of the delay map on $A$ makes each window a measurable bijection of $z_{t+1}$ (resp. $z_t$); $f$ a diffeomorphism gives $\sigma(W_t) = \sigma(W_{t+1}) = \sigma(z_t)$; mutual informations of any $S_t$ with the two windows coincide. ∎

**Finite-horizon codicil.** With windows clipped at $T$, the final $K^*{-}1$ steps retain nonzero $N_k$: their futures are shorter than an embedding window. In the echo register at noise $0.002$, interior steps contribute $\approx 0.0013$ nats each while the two truncated steps carry $0.165 + 0.159$ of the $0.331$ total. Memory is free only if the world outlives it by an embedding window.

> **Corollary 4 (Markov-order flatness).** *If the observable process is Markov of order $m$, screening makes $N_k$ constant for all $k \ge m$, at every noise level. Flatness onset reads off Markov order; collapse depth reads off redeemability.*

**Table 3 — vacuousness onset** (echo register $x_t = x_{t-3} \oplus \varepsilon(\eta)$, $K^* = 3$):

| $\eta$ | $N_1$ | $N_2$ | $N_3 = \dots = N_8$ |
|------|------|------|------|
| 0.002 | 1.077 | 1.020 | 0.331 (interior $\approx 0$; all boundary) |
| 0.05 | 1.075 | 1.029 | 0.478 |
| 0.20 | 1.067 | 1.047 | 0.814 |
| 0.50 (i.i.d.) | 1.048 | 1.048 | 1.048 (fully cryptic pole; flat) |

**Where the physics is load-bearing.** Theorem 3 read right-to-left says measured dissipation upper-bounds the retained sliding-window information of *any* internal state: calorimetry constrains representation with no access to internals. Proposition 1 classifies environments by whether this channel carries information: **Regime I** (reversible, deterministic, finite-dimensional, exactly observed) — provably uninformative; **Regime III** (information-destroying dynamics) — informative and, by §6, calibrated; **Regime II** (stochastic dynamics with a stable filter) — δ-informative with informational embedding length $K^*(\delta) \sim \log(1/\delta)/(\text{filter contraction rate})$, imported from filter stability and stochastic Takens theorems [16]. On achievability: a vanished lower bound is vacuous, not a cost statement — every environment jump costs an irreducible quench dissipation of order $D[\pi_{x_t}\|\pi_{x_{t+1}}]$ however predictable the jump was (the near-deterministic echo dissipates $\approx 4.0$ nats against a family maximum of $1.08$). Predictability refunds nothing at finite driving; the refund is kinetic, and Theorem 2 prices it.

---

## 6. Quantized chaotic observation, computed exactly

Proposition 1's infinite-precision hypothesis is essential, and its failure under quantization is quantitative and, it turns out, structured. We compute the window profile exactly — by interval arithmetic on the common refinement of iterated preimage partitions, with no sampling — for the skew tent map $f(z) = z/a$ on $[0,a]$, $(1-z)/(1-a)$ on $(a,1]$: non-invertible, Lebesgue-invariant, with Lyapunov exponent $\lambda = H(a)$ equal to the Kolmogorov–Sinai entropy. The observable is the leading $m$ bits of $z_t$; the internal state $S$ is the $\delta$-bin of $z_0$, $\delta = 2^{-p}$. Parameters: $a \in \{0.6, 0.75\}$, $m \in \{1,2\}$, $p \in \{6,10,14\}$, $k \le 19$.

**(i) The profile rises.** $N_k$ at stationary interior steps is a rising sigmoid from $0$ to a positive asymptote — the opposite of the echo cliff. Below the resolution horizon the $\delta$-cell predicts the width-$k$ window and its shifted copy equally well, and stationarity makes $N_k \approx H(W_{0:k-1}) - H(W_{1:k}) = 0$; crypticity switches on only when the window is long enough to expose the fold — when branch ambiguity of the past symbol becomes visible against the reconstructed present.

**(ii) One knee, at the Lyapunov resolution horizon.** The switch-on occurs at $k^* \approx \ln(1/\delta)/\lambda = p \ln 2/\lambda$. Measured onsets track the prediction across all parameters ($k^*_{\mathrm{pred}} \to k^*_{\mathrm{meas}}$): $6.2 \to 7$, $10.3 \to 11$, $14.4 \to 15$ at $a = 0.6$, $m = 2$; $7.4 \to 8$, $12.3 \to 14$ at $a = 0.75$. No second (embedding) knee exists in this regime: for non-invertible dynamics there is no embedding shoulder to reach, and the exact profiles show a single sigmoid.

**(iii) The asymptote is the folding entropy.** $N_k \to N_\infty$ equal to the branch (folding) entropy of the map — for full-branch Lebesgue maps, exactly $\lambda$: at $a = 0.75$, $k = 19$, $N_k = 0.5622$ against $\lambda = 0.5623$. The permanently cryptic rate is not merely nonzero; it equals the map's information-destruction rate. The window profile, read at large $k$ under quantized observation, is a dissipation-side **meter of KS entropy** for this class: measured dissipation per step below the folding entropy certifies, via the contrapositive of Theorem 3 at large $k$, that no internal state retains the destroyed information — and the folding entropy itself is readable from the profile asymptote.

**Genericity does not rescue invertible systems under future-only conditioning.** The natural reading of Proposition 1 — invertible dynamics plus a generic observable implies crypticity shuts off beyond $K^*$ — fails once observations are quantized, and fails structurally rather than by a small correction. For the skew baker's map ($a = 0.6$, unstable-direction exponent $\lambda_u = 0.673$; $S$ the $64\times64$ bin of $(u_0, v_0)$; binary observable; Monte Carlo, $10^7$ samples, Miller–Madow correction, half-sample stability control):

**Table 4 — baker's map, degenerate vs generic observable** (asymptote error $\lesssim 0.01$; $k \ge 13$ excluded for estimator drift):

| $k$ | 2 | 4 | 6 | 8 | 10 | 12 |
|---|---|---|---|---|---|---|
| $N_k$, degenerate $x = [u \ge \tfrac12]$ | 0.041 | 0.183 | 0.392 | 0.559 | 0.597 | 0.609 |
| $N_k$, generic $x = [\mathrm{frac}(u + 0.618v) \ge \tfrac12]$ | 0.052 | 0.212 | 0.400 | 0.490 | 0.525 | 0.541 |

The degenerate observable — constant along the stable direction, so Proposition 1's genericity hypothesis fails exactly as required — reproduces tent-map behavior, $N_k \to \lambda$. The generic observable gives a strictly lower asymptote ($\approx 0.54$), nowhere near zero. The culprit is the σ-algebra, not the observable: the family conditions on the *future* word only, and future observations resolve the unstable coordinate at rate $\lambda$ while carrying only exponentially attenuated information about the stable coordinate — the very contraction that makes the dynamics invertible. The branch bit of the previous step is never fully recovered from the future, and
$$N_\infty \;=\; (\text{branch entropy}) \;-\; (\text{stable-direction information recoverable from the future}),$$
with genericity controlling only the finite second term. Takens closure — $N_k \to 0$ beyond an embedding window — requires *two-sided* windows, which Lemma 2 permits but the horizon family as defined does not use (Open Problem 4, §11).

**Summary of verified signatures.** Flatness onset = Markov order; collapse depth = redeemability; quantized-chaos profile = rising sigmoid with a single Lyapunov-resolution knee at $k^* \approx \ln(1/\delta)/\lambda$; asymptote = folding entropy = information-destruction rate; and no embedding closure under future-only conditioning, even for invertible dynamics with generic observables. Caveats: the computed systems have one-dimensional unstable directions; prevalence is not universality; Regime II rests on imported theorems.

---

## 7. Back-action: the oracular discount

Now let $\mathcal{T}(x_{t+1}\mid x_t, s_t)$ depend on $s_t$. Theorem 1 stands. What fails is (KM): conditioned on the future, the relaxation stroke becomes a Doob $h$-transform of $K$ — future observations depend on the fresh state — so $p(s_{t+1}\mid x_{t+1:T}) \ne q$; and $R''_0 = I[S_0;X_{1:T}] \ge 0$ no longer vanishes, since the trajectory reads out the initial state.

**The exact penalty ledger.** Define, per step,
$$C_t \equiv R_t - \big\langle D[q \,\|\, \pi_{x_{t+1}}]\big\rangle \;\ge\; 0, \qquad
\Phi_t \equiv R''_{t+1} - \big\langle D[q \,\|\, \pi_{x_{t+1}}]\big\rangle,$$
so that $R_t - R''_{t+1} = C_t - \Phi_t$ exactly and Theorem 1 becomes
$$\beta\langle W_{\mathrm{diss}}^{\mathrm{tot}}\rangle = \sum_t I[S_t;X_t\mid X_{t+1:T}] + \sum_t C_t - \sum_t \Phi_t + (\text{final residual} \ge 0) - I[S_0;X_{1:T}].$$
Here $C_t$ is exactly the cell-averaged **mismatch cost** of the relaxation stroke in the sense of Kolchinsky–Wolpert [17]: $C_t = \langle D[p_{\mathrm{cell}} \| \pi_{x_{t+1}}] - D[p_{\mathrm{cell}} K_{x_{t+1}} \| \pi_{x_{t+1}}]\rangle$ (verified identity). The ledger reads: *dissipation = crypticity + mismatch cost − feedback discount + boundary terms.* Dropping the non-negative terms:

> **Theorem 5 (General feedback bound).**
> $$\beta\langle W_{\mathrm{diss}}^{\mathrm{tot}}\rangle \;\ge\; \sum_t I[S_t;X_t\mid X_{t+1:T}] \;-\; \sum_t \Phi_t \;-\; I[S_0;X_{1:T}].$$

**Interpreting $\Phi_t$.** Write $\Phi_t = \Delta_t + \Xi^\times_t$ with $\Delta_t \equiv \langle D[\,p(s_{t+1}|x_{t+1:T})\,\|\,q\,]\rangle \ge 0$ the information the future trajectory carries about the fresh state beyond the no-peeking pushforward, and $\Xi^\times_t$ an explicit cross term.

**Lemma 3 (Backward-transfer-entropy bound on the leakage).** $\Delta_t \le \mathrm{bTE}_t \equiv I[S_{t+1};X_{t+2:T}\mid S_t,X_{t+1}]$.

*Proof.* The divergence between the conditional joints $p(s_t,s_{t+1}|x_{t+1:T})$ and $p(s_t|x_{t+1:T})K_{x_{t+1}}$ equals $\langle D[\,p(s_{t+1}|s_t,x_{t+1:T})\,\|\,K_{x_{t+1}}(\cdot|s_t)]\rangle$; since $K = p(s_{t+1}|s_t,x_{t+1})$ under the true joint — fresh noise, even with feedback — this average is exactly $\mathrm{bTE}_t$. Marginalizing to $s_{t+1}$ contracts the divergence. ∎

This is the discrete backward transfer entropy of Ito [18]: the information the strictly-future environment carries about the system's post-update state, given its pre-update state and current input — nonzero only through back-action.

**Lemma 4 (Complete relaxation kills the cross term).** If $K_x(\cdot|s) = \pi_x$, then $q = \pi_{x_{t+1}}$, $\Xi^\times_t = 0$, and $\Phi_t = \Delta_t$.

**Lemma 5 (History-conditioning is free).** Because the environment transition reads only the current state, past $\perp (S_{t+1}, X_{t+2:T}) \mid (S_t, X_{t+1})$; hence $\mathrm{bTE}_t = I[S_{t+1};X_{t+2:T}\mid S_{0:t},X_{1:t+1}]$: state-level and history-level backward transfer entropies coincide, and no strengthening of Lemma 3 is available by enlarging the conditioning.

**The naive substitution fails at partial relaxation.** Lemmas 3–4 suggest bounding $\Phi_t$ by $\mathrm{bTE}_t$ in Theorem 5. This is valid only where Lemma 4 applies. At partial relaxation the cross term can push $\Phi_t$ *above* $\mathrm{bTE}_t$: adversarial search over 8000 jump-kernel and 4000 Metropolis feedback models followed by simplex polish finds robust overshoots — witness at $r = 0.29$: $\Phi_t = 0.498 > \mathrm{bTE}_t = 0.302$ ($\Delta_t = 0.235$, $\Xi^\times_t = 0.263$); maximum polished overshoot $+0.196$ nats. Substituting $\mathrm{bTE}$ therefore shrinks the subtracted term illegitimately, and the resulting "bound" can exceed the true dissipation. Two valid bounds follow, one kinetic and one purely informational.

> **Corollary 5 (Kinetically corrected bTE bound).** *$\Xi^\times_t = \langle\langle \log(q/\pi)\rangle_{p-q}\rangle$ satisfies $|\Xi^\times_t| \le M_t\sqrt{2\Delta_t}$ with $M_t = \max_s|\log(q(s)/\pi(s))| \le \max(\ln\frac1r,\, \ln(r + \frac{1-r}{\pi_{\min}}))$ for the jump kernel; hence*
> $$\Phi_t \le \mathrm{bTE}_t + M_t\sqrt{2\,\mathrm{bTE}_t}, \qquad
> \beta\langle W_{\mathrm{diss}}^{\mathrm{tot}}\rangle \ge \sum_t I[S_t;X_t\mid X_{t+1:T}] - \sum_t\big[\mathrm{bTE}_t + M_t\sqrt{2\,\mathrm{bTE}_t}\big] - I[S_0;X_{1:T}],$$
> *with $M_t = 0$ at complete relaxation. Proof: Appendix A.3.*

The deeper result is that no kinetic input is needed at all: $\Phi_t$ is itself a difference of two information functionals.

> **Theorem 6 (Exact discount identity; $\Phi_t \ge 0$).** *For every $t$ and arbitrary back-action,*
> $$\Phi_t \;=\; \mathrm{Orac}_t \;-\; I_\nu(t), \qquad
> \mathrm{Orac}_t \equiv I[S_{t+1};X_{t+2:T}\mid X_{t+1}], \qquad
> I_\nu(t) \equiv \big\langle D\big[\,p(s_{t+1}\mid x_{t+1:T})\,\big\|\,p(s_{t+1}\mid x_{t+1})\,\big]\big\rangle,$$
> *with $0 \le I_\nu(t) \le I[S_t;X_{t+2:T}\mid X_{t+1}] \le \mathrm{Orac}_t$; hence $0 \le \Phi_t \le \mathrm{Orac}_t$. Proof: Appendix A.4.*

The export discount never flips sign: back-action can only reduce the certified floor below the no-feedback ledger — the direction the stigmergy reading requires. Adversarial search corroborates: the minimum of $\Phi_t$ over 12,000 optimized models is 0 exactly, attained and never crossed.

> **Corollary 6 (Information-only feedback bound).** *Dropping $I_\nu \ge 0$:*
> $$\beta\langle W_{\mathrm{diss}}^{\mathrm{tot}}\rangle \;\ge\; \sum_t I[S_t;X_t\mid X_{t+1:T}] \;-\; \sum_t I[S_{t+1};X_{t+2:T}\mid X_{t+1}] \;-\; I[S_0;X_{1:T}].$$
> *At complete relaxation $I_\nu = 0$ and $\mathrm{Orac}_t = \mathrm{bTE}_t = \Delta_t = \Phi_t$ exactly, so Corollary 6 coincides there with the naive bTE bound: it is that bound's correct generalization to arbitrary relaxation speed.*

**Reading.** The subtracted quantity is the state's **oracular information** in the sense of computational mechanics [10,19]: what the fresh state tells about the observable future *beyond the current observation*. An $\varepsilon$-machine has zero oracular information — its state is a function of the observation past — so for a purely inferential memory the discount vanishes and the full cryptic charge stands. A memory written into the world's future (stigmergy: pheromone trails, notes, caches flushed to disk) carries positive oracular information, and that — not transfer entropy per se — is the exact currency of the export discount:
$$\textbf{dissipation} \;\ge\; \textbf{hidden state information} \;-\; \textbf{oracular state information} \;-\; \textbf{initial coding cost}.$$
When the oracular sum exceeds the cryptic burden the bound goes negative and net work extraction becomes possible, as Table 6 (§9) realizes. Empirically $\sum\mathrm{bTE} \le \sum\Phi \le \sum\mathrm{Orac}$ at partial relaxation in all sampled models, but the first inequality reverses at complete relaxation (where $\Phi = \Delta \le \mathrm{bTE}$): no universal ordering between $\Phi$ and $\mathrm{bTE}$ exists, which is the abstract content of the failure of the naive substitution.

---

## 8. The dual filtration: the directed-information second law

Choosing past-conditioned filtrations in Lemma 2 instead ($G = X_{1:t+1}$ post-quench, $G = X_{1:t}$ pre-quench) makes the residuals contract under feedback automatically — the past cannot peek at fresh noise — while the information terms telescope to a directed sum.

> **Theorem 7 (Dual identity and the Massey second law).**
> $$\beta\langle W_{\mathrm{diss}}^{\mathrm{tot}}\rangle \;=\; -\sum_t I[S_t;X_{t+1}\mid X_{1:t}] \;+\; \sum_t(P_t - P''_t), \qquad \sum_t(P_t - P''_t) \ge 0.$$
> *Moreover, by the screening property of Lemma 5 ($X_{t+1} \perp S_{0:t-1} \mid S_t, X_{1:t}$), the state-level transfer entropy equals the history-level one, $I[S_t;X_{t+1}\mid X_{1:t}] = I[S_{0:t};X_{t+1}\mid X_{1:t}]$, and the sum is exactly Massey's directed information $I(S^T \to X^T)$ [20]. Hence*
> $$\beta\langle W_{\mathrm{diss}}^{\mathrm{tot}}\rangle \;\ge\; -\,I(S^T \to X^T),$$
> *verbatim the directed-information second law [5–7]. The Massey–Kim conservation law $I[S^T;X^T] = I(S^T \to X^T) + I(X^T \to S^T, \mathrm{delayed})$ [21] holds in the model to machine precision; the "resource" and "liability" filtrations split exactly this conserved total.*

Theorems 1 and 7 are the same work identity split along two filtrations: future-conditioned splitting yields "prediction pays"; past-conditioned splitting yields "action pays back." In the tested feedback regimes the interpolated bounds of §7 are typically, but not always, tighter than the pure directed-information bound (Table 6): the bounds cross, and their maximum is the operative floor.

---

## 9. Numerical certification and finite-sample estimation

### 9.1 Exact certification

All identity and bound checks are by exact enumeration of the full joint path distribution $p(s_{0:T}, x_{1:T})$ — no sampling — implemented in an open verification suite (Appendix B). The chaotic-map entropies of §6 are computed by exact interval arithmetic; only the baker's-map study and §9.2 involve sampling, with stated controls. Identities hold to $10^{-14}$–$10^{-16}$; inequality checks report zero violations over their stated ensembles (Lemmas 1–3 over 60 random feedback models; Theorem 4 over 30 models in three environment classes; Theorem 6 over 200 models plus the 12,000-model adversarial search; Corollary 5 over 8000 models).

**Table 5 — autonomous environments** (hidden 3-phase environment, emission noise $\eta$, phase slip, two-state system, $r = 0.7$, $T = 8$; nats):

| $\eta$ | slip | $\beta W$ | $\sum$ cryptic | $\sum$ Still | residual |
|------|------|---------|-----------|---------|----------|
| 0.02 | 0.02 | 5.026 | 0.219 | 0.475 | 4.807 |
| 0.02 | 0.20 | 4.453 | 0.613 | 0.757 | 3.840 |
| 0.10 | 0.02 | 4.763 | 0.550 | 0.708 | 4.213 |
| 0.10 | 0.20 | 4.365 | 0.797 | 0.862 | 3.568 |
| 0.30 | 0.02 | 4.315 | 0.968 | 0.983 | 3.347 |
| 0.30 | 0.20 | 4.215 | 1.004 | 1.008 | 3.212 |

The rows certify Theorem 1, the residual sign, both bounds, the learning duality, the Still ≥ cryptic aggregate ordering (Theorem 4), and the residual dominance addressed by Theorem 2 (Table 2).

**Table 6 — feedback ledger with the oracular column** (copy environment: $x_{t+1} = s_t$ with probability $g$, else $x$ flips with probability $0.3$; two states, $J = 1.5$, $T = 6$; nats). Bounds: Theorem 5 (exact $\Phi$), Corollary 5 (kinetic), Corollary 6 (oracular), Massey $-I(S^T{\to}X^T)$:

| $g$ | $r$ | $\beta W$ | $\sum$cry | $\sum\Phi$ | $\sum$bTE | $\sum$Orac | $I[S_0;X]$ | Thm 5 | Cor 5 | Cor 6 | Massey |
|------|-----|--------|-------|-------|-------|-------|-------|--------|--------|--------|--------|
| 0.00 | 0.5 | +1.107 | 0.310 | 0.000 | 0.000 | 0.000 | 0.000 | +0.310 | +0.310 | +0.310 | 0.000 |
| 0.00 | 1.0 | +1.687 | 0.927 | 0.000 | 0.000 | 0.000 | 0.000 | +0.927 | +0.927 | +0.927 | 0.000 |
| 0.30 | 0.5 | +0.459 | 0.344 | 0.220 | 0.170 | 0.240 | 0.017 | +0.107 | −1.373 | +0.088 | −0.187 |
| 0.30 | 1.0 | +0.848 | 0.652 | 0.157 | 0.157 | 0.157 | 0.000 | +0.496 | +0.496 | +0.496 | −0.157 |
| 0.70 | 0.5 | −0.299 | 0.302 | 0.953 | 0.784 | 1.006 | 0.081 | −0.732 | −3.840 | −0.784 | −0.865 |
| 0.70 | 1.0 | −0.271 | 0.291 | 0.914 | 0.914 | 0.914 | 0.000 | −0.623 | −0.623 | −0.623 | −0.914 |
| 0.95 | 0.5 | −0.721 | 0.085 | 1.591 | 1.444 | 1.629 | 0.136 | −1.642 | −5.940 | −1.680 | −1.580 |
| 0.95 | 1.0 | −0.970 | 0.050 | 1.962 | 1.962 | 1.962 | 0.000 | −1.912 | −1.912 | −1.912 | −1.962 |

The rows certify: Theorem 1 under feedback; $\Phi \ge 0$ throughout; $\Phi = \mathrm{bTE} = \mathrm{Orac}$ at $r = 1$ (Corollary 6 collapses to the naive bound exactly there); Corollary 6 dominates Corollary 5 wherever they differ, dramatically at partial relaxation ($+0.088$ vs $-1.373$ at $g = 0.3$); every bound holds in the net-work-extraction rows. Note the crossing with the Massey bound at $g = 0.95$, $r = 0.5$ (Massey $-1.580$ vs Corollary 6's $-1.680$): neither dominates.

### 9.2 Finite-sample estimation

The horizon family is certifiable from transcripts in principle (§4.1); this subsection quantifies the practice. Trajectories are sampled from the exact path law of the Table 2 model at $r = 0.7$ (exact $\beta W = 4.700$, $\sum$Still $= 0.735$, $\sum$cryptic $= 0.605$); 20 replicates per sample size $N$.

**Table 7 — plug-in bias, Still vs cryptic** (mean ± sd of estimate − exact):

| $N$ | Still bias | cryptic bias (plug-in) | cryptic bias (Miller–Madow) |
|---|---|---|---|
| $10^3$ | +0.009 ± 0.032 | +0.094 ± 0.038 | +0.067 ± 0.040 |
| $10^4$ | −0.004 ± 0.012 | +0.009 ± 0.012 | −0.000 ± 0.012 |
| $10^5$ | −0.001 ± 0.004 | +0.002 ± 0.004 | +0.000 ± 0.004 |

Full-future conditioning inflates the plug-in cryptic estimate an order of magnitude more than the Still estimate at small $N$ — the conditioning alphabet grows as $|X|^{T-t}$ — and the crossover sample size scales with the conditioning-cell count; Miller–Madow [22] removes part of the bias. The estimated bound is not a certificate: the plug-in error decomposes as $\hat I = I + \mathrm{KL}_{\mathrm{marg}} - \mathrm{KL}_{\mathrm{cond}}$, which is not one-sided — an estimated dissipation floor can exceed the true floor and, in tight systems, manufacture false second-law violations. A certified floor requires a trusted *marginal* probe model, placing the probing burden on the unconditional window statistics rather than the state-conditional ones.

---

## 10. Related work

**Prediction costs.** Still–Sivak–Bell–Crooks [1] is the $k = 1$ endpoint of the horizon family; Corollary 2 shows their bound is complete for Markov signals, and Theorem 4 shows it is the tightest aggregate member of the entire family whenever the environment is autonomous — the trajectory extension's aggregate advantage lives entirely in the feedback regime, its autonomous value being diagnostic (profile shape) and kinetic (Theorem 2's pairing). Related trade-offs between prediction and dissipation appear in [2–4].

**Computational mechanics.** The cryptic term is the driven, finite-horizon analogue of crypticity [9,10]; the discount of Corollary 6 is exactly finite-horizon *oracular information* [19]. The inequality "dissipation ≥ crypticity − oracularity − coding cost" appears to be new, and gives these quantities a ledger in which they are the two sides of one physical account.

**Feedback second laws.** Theorem 7 is identified exactly with Massey's directed-information second law [5–7,20,21] via the screening collapse of Lemma 5; Lemma 3 is Ito's backward transfer entropy [18], and the failure of the naive substitution at partial relaxation is a cautionary instance of the loss/gain asymmetry Ito emphasizes. The filtration-choice mechanism systematizes conditioning constructions of the type in Crooks–Still [23]; continuous-time information flow appears in [8].

**Mismatch cost.** The residual term $C_t$ is exactly the Kolchinsky–Wolpert mismatch cost [17] of the relaxation stroke (verified identity, §7).

**Contraction coefficients.** Theorem 2 imports the domination of every $f$-divergence contraction coefficient by the Dobrushin coefficient [12,13]; the application to the prediction ledger appears new.

**Delay embedding.** §§5–6 read Takens / Sauer–Yorke–Casdagli / stochastic Takens [14–16] as statements about which conditional-information functionals can be nonzero, with the correction that the reading is sharply asymmetric under future-only conditioning, where embedding closure fails even for invertible dynamics with generic quantized observables; Fraser–Swinney's mutual-information heuristics [24] are early shadows of the $\bar\alpha$-spectrum diagnostics.

---

## 11. Discussion

**Implications for learning systems.** The thermodynamic content does not constrain GPU joules — real hardware sits far above any Landauer-scale floor [25] — but the representational identity transfers once $\beta$ is stripped. (i) The correct penalty for a recurrent state is the future-conditioned $I[S_t;X_t\mid X_{t+1:T}]$, not a marginal bottleneck that squeezes predictive and wasted bits alike; it is implementable with a bidirectional teacher, subject to the estimation asymmetry of §9.2. (ii) For agents, the regularizer becomes *cryptic memory minus oracular memory*: writing state into the environment is a legitimate substitute for internal retention at a 1:1 rate in nats, and the correct credit is the oracular term — only state information the future re-exposes beyond what the current input already shows earns the discount, with Theorem 6 guaranteeing the credit never overdraws. (iii) Cache eviction with write-out: an entry is safely evictable if non-cryptic given retained plus upcoming context, or if exported to a persistent substrate the future computation will read. (iv) Where $\beta$ is literal — analog and stochastic computing, molecular machines — Corollary 6 is a design law valid at any relaxation speed, and Theorem 2 supplies the kinetic complement.

**Open problems.** (1) Continuous time: merging with information-flow formalisms [8] should replace sums with integrals of a cryptic-information rate; the $h$-transform structure suggests Schrödinger-bridge connections. (2) Saturation: whether any non-trivial system saturates the trajectory bound away from quasi-static limits, and whether quantum implementations lower the cryptic floor. (3) Feedback interpolation: characterize the crossing between Corollary 6 and the Massey bound, and derive the feedback horizon family with its window-dependent penalties. (4) Two-sided windows: define the past-and-future windowed family permitted by Lemma 2, prove its residual signs, and show it realizes Takens closure where the future-only family provably does not; quantify the baker's-map defect analytically. (5) Stochastic Takens internally: prove $K^*(\delta) \lesssim \log(1/\delta)/(\text{filter contraction rate})$ as a theorem about the $\bar\alpha$-spectrum, and extend the folding-entropy asymptote to general piecewise-expanding and higher-dimensional systems. (6) Certified estimation: construct the trusted-marginal-probe estimator with finite-sample one-sided guarantees, so that transcript-based dissipation floors become certificates.

---

## Appendix A. Proofs

### A.1 Theorem 4 (summed horizon monotonicity)

By the increment formula, $\sum_t (N_{k+1}(t) - N_k(t)) = \sum_t (\alpha_k(t) - \bar\alpha_{k+1}(t))$ with $\alpha_k(t) = I[S_t;X_{t+k}\mid X_{t:t+k-1}]$ and $\bar\alpha_{k+1}(t) = I[S_t;X_{t+k+1}\mid X_{t+1:t+k}]$ (windows clipped at $T$; clipped terms vanish). Two facts close the telescope.

*(i)* $\alpha_k(1) = 0$: conditioned on $X_1$, the state $S_1 = $ (relaxation noise applied to $S_0$) is a function of $(S_0, X_1, \text{fresh noise})$, each independent of the autonomous environment's future given $X_1$; hence $S_1 \perp X_{2:T} \mid X_1$, and a fortiori $\alpha_k(1) = I[S_1;X_{1+k}\mid X_{1:k}] = 0$.

*(ii)* $\alpha_k(t+1) \le \bar\alpha_{k+1}(t)$: condition on $(S_t, X_{t+1:t+k})$. The pair $(S_{t+1}, X_{t+k+1})$ is generated from this conditioning by fresh relaxation noise (for $S_{t+1}$) and autonomous environment steps (for $X_{t+k+1}$), which are mutually independent given the conditioning; hence $S_{t+1} \perp X_{t+k+1} \mid (S_t, X_{t+1:t+k})$. The conditional data-processing inequality along the chain $S_{t+1} \leftarrow (S_t, \text{noise})$ then gives
$$\alpha_k(t+1) = I[S_{t+1};X_{t+1+k}\mid X_{t+1:t+k}] \;\le\; I[S_t;X_{t+1+k}\mid X_{t+1:t+k}] = \bar\alpha_{k+1}(t).$$
Pairing each $\alpha_k(t+1)$ with $\bar\alpha_{k+1}(t)$ and using (i) for the unpaired first term makes every bracket in the sum nonpositive. ∎

### A.2 Theorem 2 (hybrid bound)

Without back-action, $p(s_{t+1}\mid x_{t+1:T})$ equals the bare pushforward $q = K_{x_{t+1}} p(s_t \mid x_{t+1:T})$ cell-by-cell (fact (KM)), and $\pi_{x_{t+1}}$ is a fixed point of $K_{x_{t+1}}$; hence
$$R''_{t+1} = \big\langle D[\,pK \,\|\, \pi K\,]\big\rangle \le \eta_{\mathrm{KL}}(K_{x_{t+1}})\, R_t \le \eta_{\mathrm{TV}}(K_{x_{t+1}})\, R_t,$$
the last step by the domination of the KL contraction coefficient by the Dobrushin coefficient [12,13]. (When $\eta$ varies with the realized $x_{t+1}$, apply the contraction inside each conditioning cell before averaging; this is how the verification suite evaluates it.) Therefore $R_t - R''_{t+1} \ge (1-\eta_{\mathrm{TV}})R_t \ge (1-\eta_{\mathrm{TV}})Q_t$ for any Lemma-2 coarsening $Q_t \le R_t$, and summing the re-indexed residual gives the claim. At complete relaxation $\eta_{\mathrm{TV}} = 0$, $R''_{t+1} = 0$, and the inequality chain is an equality with $Q_t = R_t$. ∎

### A.3 Corollary 5 (kinetic bTE bound)

Expanding the two divergences defining $\Phi_t$ and $\Delta_t$ against $q$ gives $\Xi^\times_t = \langle \sum_s (p(s) - q(s))\log(q(s)/\pi(s))\rangle$ with $p = p(s_{t+1}|x_{t+1:T})$ cell-wise. Hölder gives $|\Xi^\times_t| \le M_t \,\langle\|p - q\|_1\rangle$ with $M_t = \max_s|\log(q(s)/\pi(s))|$; Pinsker and Jensen give $\langle\|p-q\|_1\rangle \le \langle\sqrt{2D[p\|q]}\rangle \le \sqrt{2\Delta_t}$. For the jump kernel, $q = r\pi + (1-r)p'$ for some distribution $p'$, so $q/\pi \in [r,\, r + (1-r)/\pi_{\min}]$, giving the stated $M_t$. Combine with $\Delta_t \le \mathrm{bTE}_t$ (Lemma 3), noting $x \mapsto x + M\sqrt{2x}$ is increasing. ∎

### A.4 Theorem 6 (exact discount identity and sign)

*Identity.* Expand both divergences in $\Phi_t = \langle D[p'\|\pi]\rangle - \langle D[q\|\pi]\rangle$ (with $p' = p(s_{t+1}|x_{t+1:T})$, $q$ the no-peeking pushforward, both within cells at fixed $x_{t+1}$) against the common reference $\pi_{x_{t+1}}$, and add and subtract the barycenter $\bar q_{x_{t+1}} \equiv \langle q\rangle_{\text{cells at fixed } x_{t+1}}$. The key observation is that $p(s_{t+1}\mid s_t, x_{t+1}) = K_{x_{t+1}}$ holds *even under feedback* when the future is not conditioned upon (the kernel's noise is fresh); hence $\bar q = K_{x_{t+1}}\, p(s_t\mid x_{t+1}) = p(s_{t+1}\mid x_{t+1})$, and likewise $\langle p'\rangle_{\text{cells}} = p(s_{t+1}\mid x_{t+1})$. The two barycenter cross-terms therefore cancel, leaving
$$\Phi_t = \big\langle D[p' \,\|\, \bar q]\big\rangle - \big\langle D[q \,\|\, \bar q]\big\rangle = I[S_{t+1};X_{t+2:T}\mid X_{t+1}] - I_\nu(t),$$
the first term because $\bar q = p(s_{t+1}|x_{t+1})$ makes the averaged divergence a conditional mutual information, the second by the definition of $I_\nu$.

*Sign.* Let $\tilde S$ be a *fresh-noise twin*: given $(s_t, x_{t+1})$, draw $\tilde S \sim K_{x_{t+1}}(\cdot\mid s_t)$ independently of the realized transition and of the environment's continuation. Then the cell-wise law of $\tilde S$ given $x_{t+1:T}$ is exactly $q$, and its law given $x_{t+1}$ is $\bar q$; hence $I_\nu(t) = I[\tilde S;X_{t+2:T}\mid X_{t+1}]$. Given $x_{t+1}$, the environment's continuation depends on the system only through $S_{t+1}$ (it reads only the current state), and $\tilde S$ depends on the pair only through $S_t$; two applications of the conditional data-processing inequality along $\tilde S \leftarrow S_t \rightarrow S_{t+1} \rightarrow X_{t+2:T}$ give
$$I_\nu(t) \le I[S_t;X_{t+2:T}\mid X_{t+1}] \le I[S_{t+1};X_{t+2:T}\mid X_{t+1}] = \mathrm{Orac}_t.$$
Nonnegativity of $\Phi_t$ follows from the identity. ∎

---

## Appendix B. Reproducibility

All results are reproducible from the open verification suite accompanying this paper (directory `ttp-repo/`): an exact-enumeration engine (`engine.py`) computing the full joint path distribution and all information functionals; thirteen verification scripts mapped one-to-one to the claims (README claim table); and the captured outputs of the certification run (`results/`). All Monte Carlo scripts use fixed seeds. Identity checks hold to $10^{-14}$–$10^{-16}$; ensemble inequality checks report zero violations at the stated sizes. Runtimes range from under a minute (identity smoke tests) to ~25 minutes (baker's-map Monte Carlo) on a single core.

---

## References

[1] S. Still, D. A. Sivak, A. J. Bell, and G. E. Crooks, *Thermodynamics of prediction*, Phys. Rev. Lett. **109**, 120604 (2012).
[2] A. C. Barato, D. Hartich, and U. Seifert, *Efficiency of cellular information processing*, New J. Phys. **16**, 103024 (2014).
[3] D. Hartich, A. C. Barato, and U. Seifert, *Sensory capacity: an information theoretical measure of the performance of a sensor*, Phys. Rev. E **93**, 022116 (2016).
[4] S. Still, *Thermodynamic cost and benefit of memory*, Phys. Rev. Lett. **124**, 050601 (2020).
[5] T. Sagawa and M. Ueda, *Generalized Jarzynski equality under nonequilibrium feedback control*, Phys. Rev. Lett. **104**, 090602 (2010); *Fluctuation theorem with information exchange*, Phys. Rev. Lett. **109**, 180602 (2012).
[6] S. Ito and T. Sagawa, *Information thermodynamics on causal networks*, Phys. Rev. Lett. **111**, 180603 (2013).
[7] J. M. R. Parrondo, J. M. Horowitz, and T. Sagawa, *Thermodynamics of information*, Nat. Phys. **11**, 131 (2015).
[8] J. M. Horowitz and M. Esposito, *Thermodynamics with continuous information flow*, Phys. Rev. X **4**, 031015 (2014).
[9] J. P. Crutchfield, C. J. Ellison, and J. R. Mahoney, *Time's barbed arrow: irreversibility, crypticity, and stored information*, Phys. Rev. Lett. **103**, 094101 (2009).
[10] C. J. Ellison, J. R. Mahoney, and J. P. Crutchfield, *Prediction, retrodiction, and the amount of information stored in the present*, J. Stat. Phys. **136**, 1005 (2009).
[11] A. B. Boyd, D. Mandal, and J. P. Crutchfield, *Thermodynamics of modularity: structural costs beyond the Landauer bound*, Phys. Rev. X **8**, 031036 (2018).
[12] R. L. Dobrushin, *Central limit theorem for nonstationary Markov chains I, II*, Theory Probab. Appl. **1**, 65, 329 (1956).
[13] M. Raginsky, *Strong data processing inequalities and Φ-Sobolev inequalities for discrete channels*, IEEE Trans. Inf. Theory **62**, 3355 (2016).
[14] F. Takens, *Detecting strange attractors in turbulence*, Lecture Notes in Math. **898**, 366 (1981).
[15] T. Sauer, J. A. Yorke, and M. Casdagli, *Embedology*, J. Stat. Phys. **65**, 579 (1991).
[16] J. Stark, D. S. Broomhead, M. E. Davies, and J. Huke, *Delay embeddings for forced systems II: stochastic forcing*, J. Nonlinear Sci. **13**, 519 (2003).
[17] A. Kolchinsky and D. H. Wolpert, *Dependence of dissipation on the initial distribution over states*, J. Stat. Mech. 083202 (2017).
[18] S. Ito, *Backward transfer entropy: informational measure for detecting hidden Markov models and its interpretations in thermodynamics, gambling and causality*, Sci. Rep. **6**, 36831 (2016).
[19] J. Ruebeck, R. G. James, J. R. Mahoney, and J. P. Crutchfield, *Prediction and generation of binary Markov processes: can a finite-state fox catch a Markov mouse?*, Chaos **28**, 013109 (2018).
[20] J. L. Massey, *Causality, feedback and directed information*, Proc. Int. Symp. Inf. Theory Applic. (ISITA), 303 (1990).
[21] J. L. Massey and P. C. Massey, *Conservation of mutual and directed information*, Proc. IEEE ISIT, 157 (2005).
[22] G. A. Miller, *Note on the bias of information estimates*, in *Information Theory in Psychology*, 95 (1955).
[23] G. E. Crooks and S. E. Still, *Marginal and conditional second laws of thermodynamics*, Europhys. Lett. **125**, 40005 (2019).
[24] A. M. Fraser and H. L. Swinney, *Independent coordinates for strange attractors from mutual information*, Phys. Rev. A **33**, 1134 (1986).
[25] R. Landauer, *Irreversibility and heat generation in the computing process*, IBM J. Res. Dev. **5**, 183 (1961).
