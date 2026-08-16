# Verification suite: "A Trajectory-Level Identity for the Thermodynamics of Prediction" (v2)

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
