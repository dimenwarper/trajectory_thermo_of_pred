"""Theorem D (NEW, resolves Open Problem 2): Phi_t >= 0 always.
Identity: Phi_t = I[S_{t+1}; X_{t+2:T} | X_{t+1}]  -  I_nu(t),
where I_nu(t) = <D[q_cell || qbar_{x_{t+1}}]> is the 'twin-channel' information:
q_cell = K_{x_{t+1}} p(s_t|x_{t+1:T}) and qbar = K p(s_t|x_{t+1}) = p(s_{t+1}|x_{t+1}).
Proof of sign: I_nu = I[Stilde; fut|X_{t+1}] with Stilde a fresh-noise twin drawn
from K given s_t; chain Stilde <- S_t -> S_{t+1} -> fut (given x_{t+1}) gives
I_nu <= I[S_t; fut|X_{t+1}] <= I[S_{t+1}; fut|X_{t+1}]  (two DPIs).  QED.
Corollary E (info-only partial-relaxation feedback bound):
  bW >= Sum cryptic - Sum_t I[S_{t+1}; X_{t+2:T} | X_{t+1}] - I[S_0; X_{1:T}].
Verify identity + both DPIs per step; compare Corollary E vs Theorem B tightness."""
import numpy as np
from smoke import random_model

rng = np.random.default_rng(11)

wid, wd1, wd2 = 0.0, 0.0, 0.0
gapE_worst, gapB_worst = np.inf, np.inf
tighter_E = 0
N = 200
for i in range(N):
    m, r = random_model(T=4, rng=rng, feedback=True, metro=(i % 4 == 0))
    T = m.T
    W = m.W_diss()
    Scry = sum(m.cryptic(t) for t in range(T))
    I0 = m.I(({0}, set()), (set(), set(range(1, T+1))))
    sumPhi, sumCapE, sumCapB = 0.0, 0.0, 0.0
    for t in range(T-1):
        led = m.step_ledger(t)
        fut = set(range(t+2, T+1))
        Ifull = m.I(({t+1}, set()), (set(), fut), (set(), {t+1}))   # I[S_{t+1};fut|X_{t+1}]
        Ist   = m.I(({t}, set()),   (set(), fut), (set(), {t+1}))   # I[S_t;fut|X_{t+1}]
        # I_nu directly: <D[q_cell || p(s_{t+1}|x_{t+1})]> over cells x_{t+1:T}
        arr1, dg, _ = m.joint_s_cells([t], t+1, T)
        arr2, _, _ = m.joint_s_cells([t+1], t+1, T)
        pc = arr1.sum(axis=0)
        # p(s_{t+1}|x_{t+1}):
        J2 = m.marg([t+1], [t+1])
        px = J2.sum(axis=0)
        Inu = 0.0
        k = T - t
        from engine import kl
        for c in np.where(pc > 0)[0]:
            xn = dg(c, t+1)
            q = m.Ks[xn] @ (arr1[:, c]/pc[c])
            qbar = J2[:, xn]/px[xn]
            Inu += pc[c]*kl(q, qbar)
        wid = max(wid, abs(led['Phi'] - (Ifull - Inu)))       # identity
        wd1 = max(wd1, Inu - Ist)                             # DPI 1
        wd2 = max(wd2, Ist - Ifull)                           # DPI 2
        sumPhi += led['Phi']
        sumCapE += Ifull
        bTE = max(led['bTE'], 0.0)
        sumCapB += bTE + led['Mmax']*np.sqrt(2*bTE)
    bndE = Scry - sumCapE - I0
    bndB = Scry - sumCapB - I0
    gapE_worst = min(gapE_worst, W - bndE)
    gapB_worst = min(gapB_worst, W - bndB)
    if bndE > bndB: tighter_E += 1

print(f"over {N} random feedback models (T=4, jump+metro kernels):")
print(f"  identity  Phi = I[S_(t+1);fut|X_(t+1)] - I_nu : worst gap {wid:.2e}")
print(f"  DPI1 (I_nu <= I[S_t;fut|X_(t+1)])  worst violation {wd1:.2e}")
print(f"  DPI2 (I[S_t;..] <= I[S_(t+1);..])  worst violation {wd2:.2e}")
print(f"  Corollary E bound: min slack (W - bnd) = {gapE_worst:.4f}  (>=0 required)")
print(f"  Theorem  B bound: min slack (W - bnd) = {gapB_worst:.4f}")
print(f"  Corollary E tighter than Theorem B in {tighter_E}/{N} models")
