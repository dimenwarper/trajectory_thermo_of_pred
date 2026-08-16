"""Item 7b: verify C_t is exactly the Kolchinsky-Wolpert mismatch/contraction
cost of the relaxation stroke:
  C_t = < D[p_cell || pi_{x_{t+1}}] - D[p_cell K_{x_{t+1}} || pi_{x_{t+1}}] >
averaged over posterior cells (x_{t+1:T}). Expected: agreement ~1e-16."""
import numpy as np
from engine import kl
from smoke import random_model

worst = 0.0
for trial in range(30):
    m, r = random_model(T=4, feedback=True)
    for t in range(m.T - 1):
        led = m.step_ledger(t)
        cells = m._post_cells(t)   # (weight, p(s_t|cell), x_{t+1})
        c2 = sum(w * (kl(p, m.pi[:, xn]) - kl(m.Ks[xn] @ p, m.pi[:, xn]))
                 for w, p, xn in cells)
        worst = max(worst, abs(led['C'] - c2))
print("max |C_t - mismatch-cost form| over 30 feedback models:", worst)
assert worst < 1e-12, "KW mismatch-cost identity FAILED"
print("PASS")
