# Trajectory-Level Thermodynamics of Prediction: Research Report on Items 1–8

**Scope.** Deep-dive on the eight research directions from the peer review of *Trajectory-level thermodynamics of prediction* (excluding item 9). All identities and bounds were tested against an exact-enumeration engine (`engine.py`) that computes the full joint path distribution p(s₀:T, x₁:T) for the two-stroke chain; "verified numerically" below means machine-precision agreement (≲10⁻¹⁴) or zero violations over the stated random-model ensembles. Tags: **[proved]** = analytic derivation supplied; **[verified]** = numerically confirmed at machine precision / zero violations; **[empirical]** = observed in ensembles, no proof.

**Conventions.** β = 1, nats. Steps t = 0..T−1. Work stroke x_t→x_{t+1} at frozen s_t; relaxation stroke s_t→s_{t+1} via K_{x_{t+1}} with stationary π_{x_{t+1}}. R_t = ⟨D[p(s_t|x_{t+1:T}) ‖ π_{x_{t+1}}]⟩, R''_t = ⟨D[p(s_t|x_{t:T}) ‖ π_{x_t}]⟩, q = p(s_{t+1}|x_{t+1:T}), C_t = R_t − ⟨D[q‖π_{x_{t+1}}]⟩, Φ_t = R''_{t+1} − ⟨D[q‖π_{x_{t+1}}]⟩ = Δ_t + Ξ×_t, bTE_t = I[S_{t+1}; X_{t+2:T} | S_t, X_{t+1}].

---

## Headline results

1. **Theorem A (hybrid bound):** an information + kinetics bound that recovers 73–100% of βW_diss where the pure cryptic bound covers only 4–23%, closing most of the manuscript's reported 3–20× residual gap. Exact at full relaxation. **[proved + verified]**
2. **Theorem C (horizon monotonicity):** *without* environmental back-action, the summed horizon family is monotone **decreasing** in k: Σ_t N_{k+1}(t) ≤ Σ_t N_k(t). The summed Still (k=1) bound is always the tightest of the family, and the manuscript's pad-separation claim (line 91, "[proved by construction; not numerically instantiated]") is **false as stated** — it requires feedback. With feedback the separation is real and can be large (+0.53 nats demonstrated). **[proved + verified]**
3. **Theorem D (Φ ≥ 0):** resolves the manuscript's Open Problem 2 affirmatively via an exact identity Φ_t = I[S_{t+1}; X_{t+2:T} | X_{t+1}] − I_ν(t) and a fresh-noise-twin double-DPI argument. **[proved + verified]**
4. **Corollary E:** a new, purely informational feedback bound βW ≥ Σcry − Σ_t I[S_{t+1}; X_{t+2:T} | X_{t+1}] − I[S₀; X_{1:T}], tighter than the Pinsker-based Theorem B in 200/200 test models. **[proved + verified]**
5. **Corollary 4 of the manuscript is invalid at partial relaxation:** explicit counterexamples with Φ_t > bTE_t (overshoot up to +0.196 after optimization). Theorem B provides the corrected version. **[verified counterexample]**
6. **Theorem 4 ≡ Massey:** the manuscript's dual-filtration transfer-entropy law is *exactly* Massey's directed-information second law, βW ≥ −I[Sᵀ→Xᵀ], because the per-step state-TE equals the history-TE identically in this model class. **[proved + verified]**
7. **Chaos (§5.1) largely corrected:** N_k profiles are *rising* sigmoids 0 → λ (folding entropy), not falling; there is **one** knee (Lyapunov/resolution knee at k* ≈ ln(1/δ)/λ, scaling verified), not two; and for invertible maps generic observables lower but do **not** close the crypticity asymptote — future-only words cannot resolve the stable direction. **[verified, exact interval arithmetic + MC]**
8. **Estimation:** plug-in estimates of the cryptic sum are biased upward ~10× more than the Still sum at small N (full-future conditioning); Miller–Madow halves the bias; the estimated bound is not certified without a trusted marginal probe. **[verified]**

---

## Item 1 — Theorem A: hybrid information–kinetic bound

**Statement [proved].** Without back-action, for jump-type relaxation kernels (or any kernel with Dobrushin coefficient η_TV(K_x) < 1),

βW_diss ≥ Σ_t I[S_t; X_t | X_{t+1:T}]  +  Σ_{t≤T−2} (1 − η_TV(K_{x_{t+1}})) · Q_t  +  R_{T−1},

where Q_t is any Lemma-2 coarsening of R_t (certified-computable choice: Q_t = ⟨D[p(s_t|x_{t+1}) ‖ π_{x_{t+1}}]⟩; exact choice: Q_t = R_t).

**Derivation.** The Theorem-1 residual is Σ_t(R_t − R''_t) = Σ_{t≤T−2}(R_t − R''_{t+1}) + R_{T−1} (re-index; R''₀ absorbed into the cryptic telescope). Since p(s_{t+1}|x_{t+1:T}) at the *pre-relaxation* filtration is the pushforward p K when there is no back-action, R''_{t+1} = ⟨D[pK ‖ πK]⟩ ≤ η_KL(K) R_t ≤ η_TV(K) R_t, using the standard result that the Dobrushin coefficient dominates the contraction coefficient of every f-divergence, including KL. Then R_t ≥ Q_t by the manuscript's own Lemma 2 (filtration coarsening). For the jump kernel K = rπ1ᵀ + (1−r)I, η_TV = 1 − r.

**Numbers (three-phase hidden-cycle HMM environment, T = 8, J = 2, η_emit = 0.1).** Fraction of βW_diss recovered:

| r | pure cryptic | hybrid (Q one-step) | hybrid (full R) |
|------|------|------|------|
| 0.3 | 4% | 73% | 74% |
| 0.5 | 8% | 80% | 82% |
| 0.7 | 13% | 85% | 88% |
| 0.9 | 19% | 90% | 95% |
| 1.0 | 23% | 93% | **100% (exact)** |

Exactness at r = 1 is structural: full relaxation makes R''_{t+1} = 0, so the hybrid bound reproduces the exact ledger. Emission-noise sweep at r = 0.7 gives 80–87% recovery. **Conclusion:** the "residual dominates the information bounds 3–20×" gap (manuscript line 93) is mostly *kinetic*, and a single kernel-contraction number per bath restores near-tightness.

## Item 2 — Theorem C: summed horizon monotonicity; the pad claim needs feedback

**Statement [proved].** Without back-action (environment statistics autonomous given its own state; memory receives x but does not influence it):

Σ_t N_{k+1}(t) ≤ Σ_t N_k(t) for every k ≥ 1.

Hence Σ_t N_1 (Still) ≥ Σ_t N_2 ≥ … ≥ Σ_t N_T (cryptic): **the summed Still bound is always the tightest member of the horizon family**, the "take the max over k" prescription is vacuous, and no pad construction without feedback can make the cryptic sum exceed the Still sum.

**Proof sketch.** Σ_t (N_{k+1}(t) − N_k(t)) = Σ_t (g_t − h_t) with g_t = I[S_t; X_{t+k} | X_{t:t+k−1}] and h_t = I[S_t; X_{t+k+1} | X_{t+1:t+k}]. Two facts: (i) g at t = 1 vanishes (S₁ ⊥ X_{2:T} | X₁: fresh relaxation noise plus autonomous environment); (ii) g_{t+1} ≤ h_t by conditional DPI along S_{t+1} ⊥ X-future | (S_t, X_{t+1:t+k}). Pairing telescopically makes the sum ≤ 0.

**Verification.** 0/30 violations across random no-feedback models, HMM environments, and the physical pad environment (hidden bits a, b; A-step coupled with J = 2.5, C = a⊕b flat, B echoes b — per-step pad separation appears at the C step exactly as the manuscript intends, but the sums never cross; profiles monotone).

**Escape hatch [verified].** With feedback the theorem's premise fails at fact (i)/(ii), and separation is real: random feedback models reach Σcry − ΣStill = +0.61 (the Still sum can even go negative, −0.23, while cryptic stays ≥ 0); a designed feedback pad (memory bit re-echoed by the environment two steps later with probability ρ) gives rising N_k profiles and Σcry − ΣStill = +0.53 at ρ = 1. **Manuscript correction:** line 91's claim should be restated as "pad separation holds only with environmental back-action," and §5's "take the max over k" is useful only in the feedback regime.

## Item 3 — Theorems B & D, Corollary E, and an overshoot counterexample

**Overshoot counterexample [verified].** Adversarial search (8000 jump-kernel + 4000 Metropolis random feedback models, T = 4, plus Nelder–Mead polish) finds Φ_t > bTE_t robustly; polished witness: r = 0.29, Φ = 0.498 > bTE = 0.302 (Δ = 0.235, Ξ× = 0.263; polished max overshoot +0.196). So the manuscript's Corollary 4 (substituting bTE for Φ) is **invalid at partial relaxation**; it survives only at r = 1 where Ξ× = 0 and Φ = Δ ≤ bTE.

**Theorem B (corrected bTE bound) [proved + verified].** Ξ×_t = ⟨⟨log(q/π)⟩_{p−q}⟩ obeys |Ξ×_t| ≤ M_t √(2Δ_t) (Pinsker + Jensen), with M_t ≤ max(ln(1/r), ln(r + (1−r)/π_min)) for the jump kernel. Since Δ_t ≤ bTE_t (manuscript Lemma 3),

Φ_t ≤ bTE_t + M_t √(2 bTE_t),  hence  βW ≥ Σcry − Σ_t [bTE_t + M_t√(2 bTE_t)] − I[S₀; X_{1:T}].

0/8000 violations.

**Theorem D (Φ_t ≥ 0; resolves Open Problem 2) [proved + verified].** Exact identity:

Φ_t = I[S_{t+1}; X_{t+2:T} | X_{t+1}] − I_ν(t),  I_ν(t) = ⟨D[q_cell ‖ q̄_{x_{t+1}}]⟩,

where q̄ = K p(s_t|x_{t+1}) = p(s_{t+1}|x_{t+1}); the barycenter terms cancel exactly because p(s_{t+1}|s_t, x_{t+1}) = K even under feedback when the future is not conditioned on. Sign: I_ν = I[S̃; X_{t+2:T} | X_{t+1}] for a fresh-noise twin S̃ drawn from K independently, and two data-processing steps along S̃ ← S_t → S_{t+1} → future (given x_{t+1}; the environment sees only the current s) give I_ν ≤ I[S_t; fut|X_{t+1}] ≤ I[S_{t+1}; fut|X_{t+1}]. Verified: identity to 1.05×10⁻¹⁵ and both DPIs with 0 violations over 200 models. Consequence: the feedback ledger term C_t − Φ_t can be bounded without any kinetic input.

**Corollary E (new info-only feedback bound) [proved + verified].** Dropping I_ν ≥ 0 in Theorem D:

βW ≥ Σ_t cryptic_t − Σ_{t≤T−2} I[S_{t+1}; X_{t+2:T} | X_{t+1}] − I[S₀; X_{1:T}].

Valid in 200/200 models (min slack 0.077) and **tighter than Theorem B in every one of them**. The subtracted term is precisely the state's *oracular* information about the observable future beyond the current observation — see the dictionary below.

## Item 4 — Hardening the lemma chain [verified]

60 random feedback models: Lemma 1 per-step identity to 1.1×10⁻¹⁵; Lemma 2 under random coarsened filtrations to 2.2×10⁻¹⁶; Lemma 3's intermediate equality ⟨D[p(s_t,s_{t+1}|cells) ‖ p(s_t|cells)K]⟩ = bTE_t to 1.3×10⁻¹⁵; Δ ≤ joint (DPI step) 0 violations. No gaps found in Lemmas 1–3 themselves; the only failure in §6 is Corollary 4's Φ→bTE substitution (see Item 3).

## Item 5 — Chaotic maps: §5.1 predictions tested exactly

**5a. Skew tent map (non-invertible), exact interval arithmetic.** f(z) = z/a, (1−z)/(1−a); Lebesgue invariant; λ = H(a) = KS entropy. m-bit observable; S = δ-bin of z₀; entropies computed exactly by breakpoint enumeration (no sampling). Findings across a ∈ {0.6, 0.75}, m ∈ {1, 2}, δ = 2⁻ᵖ, p ∈ {6, 10, 14}, k ≤ 19:

- **N_k is a rising sigmoid 0 → λ**, not the falling/two-knee shape sketched in §5.1. Saturation N_∞ → λ verified (0.5622 vs λ = 0.5623 at a = 0.75, k = 19 — essentially exact). Mechanism: below the resolution horizon the δ-state predicts both windows equally (stationarity makes N_k ≈ 0); crypticity turns on at k* ≈ ln(1/δ)/λ where folding/branch ambiguity becomes visible; the asymptote equals the branch (folding) entropy, which is λ for full-branch Lebesgue maps.
- **Lyapunov knee scaling confirmed:** predicted k* = p·ln2/λ vs measured support cutoff: 6.2→7, 10.3→11, 14.4→15 (a = 0.6, m = 2); 7.4→8, 12.3→14 (a = 0.75). The ᾱ_k spectrum decays smoothly.
- **Sharp two-knee structure refuted for Regime III** (non-invertible): one knee only, no embedding shoulder — consistent with the impossibility of state reconstruction under non-invertibility. (Incidental: a = 0.75, m = 2 has exact N_k = 0 for k ≤ 4 from dyadic alignment.)

**5b. Skew baker's map (invertible), Monte Carlo, 10⁷ samples.** a = 0.6, λ_u = 0.673; S = 64×64 bin of (u₀,v₀); words k ≤ 14; plug-in + Miller–Madow, half-sample stability checks.

- Degenerate observable x = [u ≥ 0.5] (constant along the stable direction): N_k rises to 0.606 by k = 13, heading to λ = 0.673 — tent-map behavior, genericity fails exactly as Prop 1's caveat anticipates.
- Generic observable x = [frac(u + 0.618v) ≥ 0.5]: N_k rises to only ≈ 0.54 — **lower asymptote, but far from zero.** Interpretation [empirical + mechanism]: conditioning is on the *future word only*; future observations resolve the unstable coordinate but carry exponentially attenuated information about the stable coordinate (contraction), so the branch bit of the previous step is never fully recovered. N_∞ = branch entropy − (stable-direction information recoverable from the future). Genericity therefore *lowers* but does **not close** the crypticity asymptote; the manuscript's "embedding knee → crypticity shuts off" prediction fails for future-conditioned crypticity even in invertible systems. A two-sided (past+future) conditioning would be needed to realize Takens closure — a concrete revision suggestion for §5.1.

## Item 6 — Finite-sample estimation of the bounds [verified]

Three-phase HMM (T = 8, binary S/X), exact path law sampled directly; 20 reps per N. Exact values: βW = 4.700, ΣStill = 0.735, Σcry = 0.605 (note: Still > cryptic, as Theorem C requires without feedback).

| N | Still bias | cryptic bias (plug-in) | cryptic bias (Miller–Madow) |
|---|---|---|---|
| 10³ | +0.009 ± 0.032 | **+0.094 ± 0.038** | +0.067 ± 0.040 |
| 10⁴ | −0.004 ± 0.012 | +0.009 ± 0.012 | −0.000 ± 0.012 |
| 10⁵ | −0.001 ± 0.004 | +0.002 ± 0.004 | +0.000 ± 0.004 |

Full-future conditioning inflates the plug-in cryptic estimate ~10× more than the Still estimate at small N (the conditioning alphabet grows as |X|^{T−t}). Miller–Madow removes roughly a third at N = 10³ and essentially all at N ≥ 10⁴ in this small model; in larger alphabets the crossover N scales with the conditioning-cell count. **Caution for practitioners:** the plug-in decomposition Î = I + KL_marg − KL_cond is *not* one-sided — an estimated "lower bound on dissipation" is not certified; a trusted marginal probe model (giving a true KL_marg) is needed to certify a floor. In tight systems the upward bias can manufacture false second-law "violations."

## Item 7 — Dictionaries to adjacent formalisms

**Computational mechanics (Crutchfield–Ellison–Mahoney).** The per-step cryptic term I[S_t; X_t | X_{t+1:T}] is a driven, finite-horizon analogue of CEM *crypticity* — state information hidden from (here: future) observations — with the physical memory S in place of causal states; the manuscript's name is apt and the citation should be added. More sharply: the subtracted term in Corollary E, I[S_{t+1}; X_{t+2:T} | X_{t+1}], is exactly the finite-horizon form of *oracular information* ζ = I[R; future | observed] — state information that improves prediction beyond what observation provides. Corollary E then reads: **dissipation ≥ hidden (cryptic) state information − oracular state information − initial coding cost**, a clean computational-mechanics sentence. ε-machines have ζ = 0; a physical memory driven by feedback generically has ζ > 0, and that is precisely what feedback "pays for."

**Ito's backward transfer entropy (Sci. Rep. 6:36831).** The manuscript's Lemma-3 quantity bTE_t = I[S_{t+1}; X_{t+2:T} | S_t, X_{t+1}] conditions the *later* memory state on the future — structurally Ito's backward TE, which bounds losses where forward TE bounds gains. The overshoot counterexample (Item 3) shows the manuscript's Corollary 4 conflated the two roles at partial relaxation; Theorem B/Corollary E restore the correct backward-TE-flavored accounting. Also verified: per-step bTE with single-state conditioning equals history-conditioned bTE exactly (pair-Markov property; see Item 8), so the "state vs history" distinction is vacuous here.

**Kolchinsky–Wolpert mismatch cost.** Verified to 2.2×10⁻¹⁶: C_t = ⟨D[p_cell ‖ π_{x_{t+1}}] − D[p_cell K_{x_{t+1}} ‖ π_{x_{t+1}}]⟩ — i.e., C_t is exactly the (cell-averaged) relative-entropy contraction / mismatch cost of the relaxation stroke with prior π. The ledger of Theorem 3 is thus: dissipation = crypticity + Σ(mismatch cost − oracular gain) + boundary terms, connecting the manuscript to the mismatch-cost literature with no new work.

## Item 8 — Theorem 4 is Massey's directed-information law [proved + verified]

Over 60 random feedback models: Σ_t I[S_{0:t}; X_{t+1} | X_{1:t}] = Σ_t I[S_t; X_{t+1} | X_{1:t}] **exactly** — because the environment transition reads only the current s, per-step history-TE collapses to state-TE. Hence the manuscript's Theorem 4,

βW ≥ − Σ_t I[S_t; X_{t+1} | X_{1:t}] = − I[Sᵀ → Xᵀ] (Massey directed information),

*is* the directed-information second law; the manuscript should say so and cite Massey (1990) and the Sagawa–Ueda/Ito–Sagawa feedback second laws. Also verified: Massey–Kim conservation I[Sᵀ; Xᵀ] = I(Sᵀ→Xᵀ) + I(Xᵀ→Sᵀ, delayed) to 2.7×10⁻¹⁵; and the bTE history-collapse lemma (sum_bTE = sum_bTE_histS = sum_bTE_histSX, provable from past ⊥ (S_{t+1}, future) | (S_t, X_{t+1})). Empirically ΣbTE ≤ ΣΦ ≤ Σ_t I[S_{t+1}; X_{t+2:T}|X_{t+1}] at partial relaxation in all samples, but the ordering of the first pair flips at r = 1 (there Φ = Δ ≤ bTE), so no universal ordering should be claimed.

---

## Consolidated corrections to the manuscript

1. §4 line 91: pad separation Σcry > ΣStill is **impossible without back-action** (Theorem C); restate as a feedback phenomenon (designed feedback pad achieves +0.53).
2. §5 "take the max over k": vacuous without feedback (summed family is monotone); keep only for the feedback regime, or report per-step profiles.
3. §5.1: replace the two-knee falling picture with: rising sigmoid, single Lyapunov knee at k* ≈ ln(1/δ)/λ, asymptote = folding/branch entropy (= λ for full-branch maps); genericity lowers but does not close the asymptote under future-only conditioning (baker's map); Takens closure requires two-sided conditioning.
4. §6 Corollary 4: **withdraw at partial relaxation** (overshoot counterexample); replace with Theorem B (kinetic constant) or Corollary E (info-only, tighter).
5. Open Problem 2: **solved** — Φ ≥ 0 always (Theorem D).
6. Theorem 4: identify with Massey directed information (exact equality of state- and history-TE in this model class).
7. Add: hybrid bound (Theorem A) to address the residual-dominance limitation the manuscript itself flags at line 93.
8. Numerics appendix: report plug-in bias asymmetry (cryptic vs Still) and the non-one-sidedness of estimated bounds.

## File index

`engine.py` (exact enumeration engine); `smoke.py` (identity checks); `harden.py` (item 4); `item1_hybrid.py` (Theorem A); `item2_pad.py`, `item2_theoremC.py` (Theorem C, pads); `item3_adversarial.py`, `item3_theoremD.py` (overshoot, Theorems B/D, Corollary E); `item5a_tent.py` (exact tent-map study); `item5b_baker.py` (baker MC); `item6_bias.py` (estimation); `item7_kw.py` (mismatch-cost check); `item8_massey.py` (Massey equality).
