"""Item 3: Open Problem 2 (sign of Phi_t) and partial-relaxation feedback bound.
Theorem B (derived):  Phi_t = Delta_t + Xi_t with Xi_t = <<log(q/pi)>_{p-q}>,
|Xi_t| <= M_t sqrt(2 Delta_t)  (Pinsker + Cauchy-Schwarz over cells),
so with Lemma 3:  Phi_t <= bTE_t + M_t sqrt(2 bTE_t), giving
  bW_diss >= Sum cryptic - Sum_t [bTE_t + M_t sqrt(2 bTE_t)] - I[S_0;X_{1:T}].
For jump kernels M_t <= max(ln(1/r), ln(r + (1-r)/pi_min)).
Adversarial search: can Phi_t < 0?  Can Phi_t > bTE_t (overshoot)?"""
import numpy as np
from scipy.optimize import minimize
from engine import TwoStroke, jump_kernel, metropolis_kernel

T, nS, nX = 4, 2, 2
rng = np.random.default_rng(123)

def softmax(v):
    v = v - v.max(axis=0, keepdims=True)
    e = np.exp(v); return e / e.sum(axis=0, keepdims=True)

NP_E, NP_R0, NP_TK = nS*nX, nX*nS, (T-1)*nX*nX*nS
NPAR = NP_E + NP_R0 + NP_TK + 1

def build(theta):
    i = 0
    E = theta[i:i+NP_E].reshape(nS, nX)*2; i += NP_E
    r0 = softmax(theta[i:i+NP_R0].reshape(nX, nS)*2); i += NP_R0
    Tks = []
    for t in range(T-1):
        L = theta[i:i+nX*nX*nS].reshape(nX, nX, nS)*2; i += nX*nX*nS
        Tks.append(softmax(L))
    r = 1/(1+np.exp(-theta[i]))
    Z = np.exp(-E).sum(axis=0); pi = np.exp(-E)/Z
    Ks = jump_kernel(pi, r)
    return TwoStroke(nS, nX, T, E, Ks, r0, Tks), r

def stats(m, r):
    led = [m.step_ledger(t) for t in range(T-1)]
    minPhi = min(l['Phi'] for l in led)
    overs = max(l['Phi'] - l['bTE'] for l in led)
    # Theorem B per-step:  Phi_t <= bTE_t + M sqrt(2 bTE_t), M a-priori for jump kernel
    pimin = m.pi.min()
    Mapr = max(np.log(1/r), np.log(r + (1-r)/pimin)) if r > 0 else np.inf
    tB = max(l['Phi'] - (l['bTE'] + Mapr*np.sqrt(2*max(l['bTE'],0.0))) for l in led)
    # also with the measured (tighter) M_t
    tBm = max(l['Phi'] - (l['bTE'] + l['Mmax']*np.sqrt(2*max(l['bTE'], 0))) for l in led)
    # full bound
    W = m.W_diss()
    Scry = sum(m.cryptic(t) for t in range(T))
    I0 = m.I(({0}, set()), (set(), set(range(1, T+1))))
    bndB = Scry - sum(l['bTE'] + Mapr*np.sqrt(2*max(l['bTE'],0.0)) for l in led) - I0
    bnd4 = Scry - sum(l['Phi'] for l in led) - I0     # exact-Phi (Thm 3) bound
    return dict(minPhi=minPhi, overs=overs, tB=tB, tBm=tBm, WgapB=W-bndB, Wgap3=W-bnd4)

print("random search (8000 models, T=4, jump kernels incl. small r)...")
best_minPhi, best_overs = (np.inf, None), (-np.inf, None)
worstB = np.inf
viol3 = 0
for i in range(8000):
    th = rng.normal(size=NPAR)
    if i % 3 == 0: th[-1] = rng.normal() - 2.0   # bias toward small r sometimes
    m, r = build(th)
    st = stats(m, r)
    if st['minPhi'] < best_minPhi[0]: best_minPhi = (st['minPhi'], th.copy())
    if st['overs'] > best_overs[0]: best_overs = (st['overs'], th.copy())
    worstB = min(worstB, st['WgapB'])
    if st['tB'] > 1e-12: viol3 += 1
print(f"  min Phi_t found: {best_minPhi[0]:.6f}")
print(f"  max (Phi_t - bTE_t) found: {best_overs[0]:.6f}")
print(f"  Theorem-B per-step violations: {viol3}/8000; worst full-bound slack: {worstB:.4f}")

def polish(th0, obj, sign):
    f = lambda th: sign*getattr_stats(th, obj)
    def getattr_stats(th, key):
        try:
            m, r = build(th)
            return stats(m, r)[key]
        except Exception:
            return 1e3*sign
    res = minimize(lambda th: sign*getattr_stats(th, obj), th0, method='Nelder-Mead',
                   options=dict(maxiter=1500, xatol=1e-8, fatol=1e-12))
    return getattr_stats(res.x, obj), res.x

v1, th1 = polish(best_minPhi[1], 'minPhi', +1)
print(f"  polished min Phi_t: {v1:.8f}")
v2, th2 = polish(best_overs[1], 'overs', -1)
print(f"  polished max (Phi_t - bTE_t): {v2:.8f}")
if v2 > 1e-9:
    m, r = build(th2)
    led = [m.step_ledger(t) for t in range(T-1)]
    t = int(np.argmax([l['Phi'] - l['bTE'] for l in led]))
    l = led[t]
    print(f"  OVERSHOOT WITNESS at r={r:.4f}, step {t}: Phi={l['Phi']:.5f} "
          f"bTE={l['bTE']:.5f} Delta={l['Delta']:.5f} Xi={l['Xi']:.5f} M={l['Mmax']:.3f}")
    print(f"  Theorem-B cap bTE+M*sqrt(2bTE) = {l['bTE']+l['Mmax']*np.sqrt(2*max(l['bTE'],0.0)):.5f}")
if v1 < -1e-9:
    m, r = build(th1)
    led = [m.step_ledger(t) for t in range(T-1)]
    t = int(np.argmin([l['Phi'] for l in led]))
    l = led[t]
    print(f"  NEGATIVE-PHI WITNESS at r={r:.4f}, step {t}: Phi={l['Phi']:.6f} "
          f"Delta={l['Delta']:.6f} Xi={l['Xi']:.6f} bTE={l['bTE']:.6f}")

# Metropolis-kernel variant (breaks the jump-kernel structure)
print("\nMetropolis-kernel search (4000 models)...")
NPAR2 = NP_E + NP_R0 + NP_TK + nX*nS*nS
def build2(theta):
    i = 0
    E = theta[i:i+NP_E].reshape(nS, nX)*2; i += NP_E
    r0 = softmax(theta[i:i+NP_R0].reshape(nX, nS)*2); i += NP_R0
    Tks = []
    for t in range(T-1):
        L = theta[i:i+nX*nX*nS].reshape(nX, nX, nS)*2; i += nX*nX*nS
        Tks.append(softmax(L))
    prop = theta[i:].reshape(nX, nS, nS)
    Z = np.exp(-E).sum(axis=0); pi = np.exp(-E)/Z
    Ks = metropolis_kernel(pi, prop)
    return TwoStroke(nS, nX, T, E, Ks, r0, Tks)
mn, mo = np.inf, -np.inf
th_mn = th_mo = None
for i in range(4000):
    th = rng.normal(size=NPAR2)
    m = build2(th)
    led = [m.step_ledger(t) for t in range(T-1)]
    a = min(l['Phi'] for l in led); b = max(l['Phi'] - l['bTE'] for l in led)
    if a < mn: mn, th_mn = a, th.copy()
    if b > mo: mo, th_mo = b, th.copy()
print(f"  min Phi_t = {mn:.6f}, max (Phi_t - bTE_t) = {mo:.6f}")
def polish2(th0, key, sign):
    def val(th):
        try:
            m = build2(th)
            led = [m.step_ledger(t) for t in range(T-1)]
            return (min(l['Phi'] for l in led) if key == 'minPhi'
                    else max(l['Phi'] - l['bTE'] for l in led))
        except Exception:
            return 1e3*sign
    res = minimize(lambda th: sign*val(th), th0, method='Nelder-Mead',
                   options=dict(maxiter=1500))
    return val(res.x)
print(f"  polished min Phi_t (metro): {polish2(th_mn, 'minPhi', +1):.8f}")
print(f"  polished max overshoot (metro): {polish2(th_mo, 'overs', -1):.8f}")
