# A Trajectory-Level Identity for the Thermodynamics of Prediction

This repository holds a theoretical-physics paper and the machine-checked verification
suite that certifies it. The paper derives an exact, trajectory-level identity for the
**thermodynamics of prediction** — how much work a physical system must dissipate to
track a structured signal, and how that cost is accounted for by the information the
system stores about the signal.

## The question

A physical system driven by a structured input cannot avoid becoming correlated with
it, and thermodynamics charges for the correlation. Still, Sivak, Bell & Crooks (2012)
made this precise for a system that cannot influence its own input: the dissipated work
per driving step is at least $k_BT$ times the system's *nostalgia* — the memory it keeps
about the last input beyond what is useful for predicting the next one. That bound is
per-step and assumes no back-action (no feedback from the system onto its environment).

## What this work adds

Starting from a single exact identity that makes **no causal assumption at all**, the
paper generalizes the 2012 result to whole trajectories and to agents that act back on
their environment. The central object is the two-stroke driven chain of Still et al. over
a finite horizon $T$: each step, the environment signal $x_t \to x_{t+1}$ quenches the
system's energy landscape, and the system then relaxes one step toward the new
equilibrium. The environment may be arbitrary (hidden-Markov, long-memory,
non-stationary) and, in the second half, may respond to the system's state.

The identity states that total dissipated work equals the summed **cryptic information**

$$\beta\langle W_{\mathrm{diss}}\rangle \;=\; \sum_t I[S_t;\,X_t \mid X_{t+1:T}] \;+\; \text{(a residual of characterized sign)},$$

where the cryptic information is *what the state stores about the present signal that the
signal's entire future never discloses again*. Information the future reveals anyway is
thermodynamically free. Every downstream result is a sign analysis of the residual under
a different choice of what to condition on (a "filtration"): future-conditioned choices
give prediction-type bounds; past-conditioned choices give feedback-type bounds.

### Headline results

- **Exact, feedback-robust identity** (Theorem 1) — holds for arbitrary environment
  statistics and arbitrary back-action.
- **The window family is ordered** (Theorem 4) — without back-action the summed
  sliding-window bounds are monotone in window width, so the original 2012 bound is the
  *tightest* aggregate member. A rising window profile is therefore a certificate of
  back-action, visible on the information layer alone.
- **A kinetic completion** (Theorem 2) — pure information bounds recover only 4–30% of
  dissipation; the deficit is kinetic, not informational. Adding *one number per bath* —
  the relaxation kernel's Dobrushin contraction coefficient — yields a hybrid bound that
  recovers 74–100%, exact at complete relaxation.
- **The oracular discount** (Theorems 5–6) — with feedback the penalty is proved
  non-negative and equals the state's *oracular information* about the observable future:
  *an agent pays for memory by dissipating it or by writing it into the world's future.*
- **Unification with directed information** (Theorem 7) — the past-conditioned filtration
  of the same identity is exactly Massey's directed-information second law. "Prediction
  pays" and "action pays back" are two σ-algebra choices in one decomposition.
- **Chaotic observation, computed exactly** (§6) — for quantized expanding maps the
  window profile is computed by exact interval arithmetic (no sampling); it is a rising
  sigmoid with a single knee at the Lyapunov resolution horizon, asymptoting to the map's
  folding entropy.

Everything is machine-verified by **exact enumeration of the full joint path
distribution** $p(s_{0:T}, x_{1:T})$ — no sampling — including adversarial model searches
(12,000 models attacking the sign of the feedback penalty) and net-work-extraction
regimes.

## Repository contents

| File / dir | What it is |
|---|---|
| `ttp_paper.md` | The manuscript. Start here for the full theory, proofs (Appendix A), and tables. |
| `research_report.md` | Deep-dive verification report on the eight research directions, with `[proved]` / `[verified]` / `[empirical]` tags. Also records where verification *corrected* earlier claims (e.g. the pad-separation claim requires feedback; chaotic-map profiles rise rather than fall; one corollary is invalid at partial relaxation). |
| `notes.md` | Working notes and scratch derivations. |
| `scripts/` | The verification suite — `engine.py` (exact-enumeration engine) plus one script per manuscript claim. |
| `results/` | Captured stdout of every script from the certification run. |
| `requirements.txt` | Python dependencies (numpy, scipy). |

---

# Verification suite

Every **[verified]** tag in the manuscript maps to a script here. All computations are
exact enumeration of the full joint path distribution p(s_{0:T}, x_{1:T}) (no sampling),
except: the tent-map study (exact *interval arithmetic*, still no sampling) and the
baker's-map / estimation studies (Monte Carlo, with stated controls).

## Requirements

Python ≥ 3.10, `numpy`, `scipy` (scipy only for `item3_adversarial.py`).
Tested with Python 3.12.3, numpy 2.4.4, scipy 1.17.1.

```
pip install -r requirements.txt
```

## Layout

- `scripts/engine.py` — exact-enumeration engine (`TwoStroke` class): joint path
  distribution, W_diss, information functionals over arbitrary axis subsets,
  per-step ledger (R, R'', C, Φ, Δ, Ξ×, bTE), Dobrushin coefficients,
  Massey directed information, HMM-environment builder.
- `scripts/smoke.py` — model factory + identity smoke tests (Theorems 1, 3, 5, 7 identities;
  boundary terms; no-feedback Φ=0).
- `results/*.out` — captured stdout of every script from the certification run.

## Claim → script map (manuscript v2 numbering)

| Manuscript claim | Script | Runtime* |
|---|---|---|
| Lemmas 1–3 hardening (machine-precision, 60 feedback models) | `harden.py` | ~1 min |
| Theorem 2 hybrid bound; Table 2 sweep | `item1_hybrid.py`, `gen_tables.py` | ~5 min |
| Theorem 4 monotonicity (0/30 violations); feedback escape hatch | `item2_theoremC.py` | ~3 min |
| Pad environment: per-step reversal, no aggregate crossing | `item2_pad.py` | ~2 min |
| Corollary 5 (0/8000); overshoot counterexample Φ>bTE; min Φ = 0 | `item3_adversarial.py` | ~20 min |
| Theorem 6 identity + both DPIs (200 models); Corollary 6 validity/tightness | `item3_theoremD.py` | ~2 min |
| §5.1 tent map: rising sigmoid, knee scaling, N∞ = folding entropy | `item5a_tent.py` | ~10 min |
| §5.1 Table 5 baker's map: degenerate vs generic observable | `item5b_baker.py` | ~25 min |
| §8.1 Table 7 estimation bias | `item6_bias.py` | ~10 min |
| §6 mismatch-cost identity for C_t (Kolchinsky–Wolpert) | `item7_kw.py` | ~1 min |
| Theorem 7 Massey equality; bTE history collapse; Massey–Kim conservation | `item8_massey.py` | ~3 min |
| Tables 2 and 6 as printed in the manuscript | `gen_tables.py` | ~5 min |

*Single core, commodity hardware; the two slow scripts are embarrassingly parallel if needed.

## Reproducing everything

```
cd scripts
for s in smoke harden item7_kw item2_theoremC item3_theoremD item8_massey \
         gen_tables item2_pad item1_hybrid item6_bias item5a_tent \
         item3_adversarial item5b_baker; do
  python3 $s.py | tee ../results/$s.out
done
```

Determinism: all Monte Carlo scripts use fixed seeds (`np.random.default_rng(seed)`),
so `results/` should reproduce bit-for-bit on the same numpy version; exact-enumeration
outputs are deterministic up to floating-point associativity.

## Conventions (match manuscript §1)

β = 1, nats. Steps t = 0..T−1: quench x_t→x_{t+1} at fixed s_t (x_0 = flat landscape),
then relaxation s_t→s_{t+1} via K_{x_{t+1}}. Joint array dims ordered (s_0..s_T, x_1..x_T).
Kernel indexing `Ks[x][s_new, s_old]`. Cryptic term at t=0 is 0 (x_0 constant).

## Caveats

- "Verified" = machine-checked on these model classes at the stated tolerances;
  it is evidence, not proof, wherever the manuscript tags it so.
- `item5b_baker.py` plug-in estimates drift for k ≥ 13 (see half-sample column);
  the manuscript's Table 5 excludes those points.
- v1 scripts (`verify.py` etc.) are superseded by `engine.py` and not included.
