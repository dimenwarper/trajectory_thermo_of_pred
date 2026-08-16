"""Item 8: (a) Massey weakening: sum_t I[S_t;X_{t+1}|X_{1:t}] <= DI(S->X)
(monotonicity of CMI in the first argument), hence bW >= -DI(S->X).
(b) Numerical-discovery battery: how does Sum_t bTE_t relate to directed
informations?  Test candidate identities on random feedback models."""
import numpy as np
from smoke import random_model

rng = np.random.default_rng(5)

def battery(m):
    T = m.T
    d = {}
    ste = sum(m.stateTE(t) for t in range(T))
    DI = m.massey_DI()
    d['sumStateTE'] = ste
    d['MasseyDI_StoX'] = DI
    # reverse-delayed Massey X->S: sum_t I[X_{1:t+1}; S_{t+1} | S_{0:t}]
    DIxs = sum(m.I((set(), set(range(1, t+2))), ({t+1}, set()), (set(range(0, t+1)), set()))
               for t in range(T))
    d['MasseyDI_XtoS_delay'] = DIxs
    d['Itotal'] = m.I((set(range(0, T+1)), set()), (set(), set(range(1, T+1))))
    d['conservation_gap'] = d['Itotal'] - (DI + DIxs) - m.I(({0}, set()), (set(), set()))
    # bTE variants
    c0 = sum(m.step_ledger(t)['bTE'] for t in range(T-1))
    d['sum_bTE'] = c0
    c1 = sum(m.I(({t+1}, set()), (set(), set(range(t+2, T+1))), (set(range(0, t+1)), {t+1}))
             for t in range(T-1))
    d['sum_bTE_histS'] = c1
    c2 = sum(m.I(({t+1}, set()), (set(), set(range(t+2, T+1))),
                 (set(range(0, t+1)), set(range(1, t+2)))) for t in range(T-1))
    d['sum_bTE_histSX'] = c2
    # time-reversed Massey S->X on reversed sequences:
    # rev X: (X_T,...,X_1), rev S: (S_T,...,S_0); DI(revS->revX) =
    # sum_u I[S_{T:T-u}; X_{T-u} | X_{T:T-u+1}] ... build explicitly
    rev = 0.0
    for u in range(1, T+1):
        xt = T - u + 1            # target symbol going backwards: X_T, X_{T-1},...
        Scond = set(range(xt, T+1))       # states S_{xt..T} (those 'before' in reversed order, aligned)
        Xcond = set(range(xt+1, T+1))
        rev += m.I((Scond, set()), (set(), {xt}), (set(), Xcond))
    d['revMassey_StoX'] = rev
    # sum of Phi (for reference) and Sum I[S_{t+1};fut|X_{t+1}] (Corollary E cap)
    d['sum_Phi'] = sum(m.step_ledger(t)['Phi'] for t in range(T-1))
    d['sum_capE'] = sum(m.I(({t+1}, set()), (set(), set(range(t+2, T+1))), (set(), {t+1}))
                        for t in range(T-1))
    return d

keys = None
vals = []
worst_ineq = -np.inf
for i in range(60):
    m, _ = random_model(T=4, rng=rng, feedback=True, metro=(i % 4 == 0))
    d = battery(m)
    if keys is None: keys = list(d.keys())
    vals.append([d[k] for k in keys])
    worst_ineq = max(worst_ineq, d['sumStateTE'] - d['MasseyDI_StoX'])
V = np.array(vals)
print("means over 60 random feedback models:")
for j, k in enumerate(keys):
    print(f"  {k:22s} mean={V[:, j].mean():8.4f}  sd={V[:, j].std():.4f}")
print(f"\nsum stateTE <= Massey DI: worst violation {worst_ineq:.2e}")
print(f"Massey conservation gap (Itotal - DI_SX - DI_XS_delay): "
      f"max|.| = {np.abs(V[:, keys.index('conservation_gap')]).max():.2e}")

# pairwise equality detection
print("\nexact equalities / inequalities detected (tol 1e-10):")
import itertools
for a, b in itertools.combinations(range(len(keys)), 2):
    diff = V[:, a] - V[:, b]
    if np.abs(diff).max() < 1e-10:
        print(f"  {keys[a]} == {keys[b]}")
    elif diff.max() < 1e-12:
        print(f"  {keys[a]} <= {keys[b]}  (always, margin {-diff.max():.1e}..{-diff.min():.1e})")
    elif diff.min() > -1e-12:
        print(f"  {keys[a]} >= {keys[b]}  (always)")
