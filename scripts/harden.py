"""Item 4: verify each lemma separately (not just final identities), incl.
Lemma 3's averaging-measure step, on random FEEDBACK models."""
import numpy as np
from engine import TwoStroke, jump_kernel, metropolis_kernel, kl
from smoke import random_model

rng = np.random.default_rng(42)

worst = dict(L1=0, L2=0, L3joint=0, L3dpi=0)
for trial in range(60):
    m, r = random_model(T=4, rng=rng, feedback=True, metro=(trial % 3 == 0))
    T, nS, nX = m.T, m.nS, m.nX

    # ---- Lemma 1 per step, C = full trajectory ----
    for t in range(T):
        # LHS: beta<W(t) - dF(t)>
        if t == 0:
            J = m.marg([0], [1])
            w = np.sum(J * m.E)
            px1 = J.sum(axis=0)
            dF = float(np.dot(px1, m.F)) - m.F_flat
        else:
            J = m.marg([t], [t, t+1])
            w = np.einsum('sab,sb->', J, m.E) - np.einsum('sab,sa->', J, m.E)
            pxx = J.sum(axis=0)
            dF = float(np.einsum('ab,b->', pxx, m.F) - np.einsum('ab,a->', pxx, m.F))
        lhs = w - dF
        # RHS: <D[p(s_t|x_{1:T})||pi_{x_{t+1}}]> - <D[p(s_t|x_{1:T})||pi_{x_t}]>
        arr, digit, k = m.joint_s_cells([t], 1, T)
        pc = arr.sum(axis=0)
        rhs = 0.0
        for c in np.where(pc > 0)[0]:
            p = arr[:, c]/pc[c]
            xn = digit(c, t+1)
            ref_next = m.pi[:, xn]
            ref_now = m.pi[:, digit(c, t)] if t >= 1 else np.full(nS, 1/nS)
            rhs += pc[c] * (kl(p, ref_next) - kl(p, ref_now))
        worst['L1'] = max(worst['L1'], abs(lhs - rhs))

    # ---- Lemma 2 with a random sub-filtration G determined by (x_{t+1}) plus random coarsening ----
    t = rng.integers(0, T)
    # G = (x_{t+1}, f(x_{t+2:T})) with f a random coarsening -> x* = x_{t+1} measurable wrt G
    arrC, digC, _ = m.joint_s_cells([t], 1, T)   # C = full path
    # define G-label per column
    ncols = arrC.shape[1]
    coarse = rng.integers(0, 2, nX**max(T-(t+1), 0)) if T-(t+1) > 0 else None
    Glab = np.zeros(ncols, dtype=int)
    for c in range(ncols):
        xn = digC(c, t+1)
        rest = 0
        if T - (t+1) > 0:
            # index of x_{t+2:T}
            ridx = 0
            for u in range(t+2, T+1):
                ridx = ridx*nX + digC(c, u)
            rest = coarse[ridx]
        Glab[c] = xn*2 + rest
    pC = arrC.sum(axis=0)
    # LHS <D[p(s|C)||pi_{x_{t+1}}]>
    lhs = sum(pC[c]*kl(arrC[:, c]/pC[c], m.pi[:, digC(c, t+1)]) for c in np.where(pC > 0)[0])
    # I[S;C]
    ps = arrC.sum(axis=1)
    ISC = sum(pC[c]*kl(arrC[:, c]/pC[c], ps) for c in np.where(pC > 0)[0])
    # group by G
    labs = np.unique(Glab)
    ISG, DG = 0.0, 0.0
    for L in labs:
        colsL = np.where(Glab == L)[0]
        w = pC[colsL].sum()
        if w == 0: continue
        pG = arrC[:, colsL].sum(axis=1)/w
        ISG += w*kl(pG, ps)
        xn = digC(colsL[0], t+1)
        DG += w*kl(pG, m.pi[:, xn])
    worst['L2'] = max(worst['L2'], abs(lhs - (ISC - ISG + DG)))

    # ---- Lemma 3 intermediate equality:
    # <D[p(s_t,s_{t+1}|x_{t+1:T}) || p(s_t|x_{t+1:T}) K_{x_{t+1}}]> == bTE_t exactly
    for t in range(T-1):
        # pair joint with cells x_{t+1:T}
        Mj = m.marg([t, t+1], list(range(t+1, T+1)))  # (s_t, s_{t+1}, x_{t+1}..x_T)
        k = T - t
        A = Mj.reshape(nS, nS, nX**k)
        pcell = A.sum(axis=(0, 1))
        tot = 0.0
        for c in np.where(pcell > 0)[0]:
            xn = (c // (nX**(k-1))) % nX
            Pj = A[:, :, c]/pcell[c]              # p(s_t, s_{t+1}|cell)
            pst = Pj.sum(axis=1)
            Qj = pst[:, None] * m.Ks[xn].T        # p(s_t) K(s_{t+1}|s_t): K[s_new,s_old] -> [so,sn]
            tot += pcell[c]*kl(Pj.ravel(), Qj.ravel())
        bTE = m.I(({t+1}, set()), (set(), set(range(t+2, T+1))), ({t}, {t+1}))
        worst['L3joint'] = max(worst['L3joint'], abs(tot - bTE))
        # and data-processing: Delta_t <= joint value
        led = m.step_ledger(t)
        worst['L3dpi'] = max(worst['L3dpi'], led['Delta'] - tot)

print("worst-case gaps over 60 random feedback models (T=4):")
for k, v in worst.items():
    print(f"  {k}: {v:.3e}")
