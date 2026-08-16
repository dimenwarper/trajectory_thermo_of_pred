"""Item 6: finite-sample estimation bias, Still vs cryptic bounds.
Exact model: three_phase HMM (T=8, binary S/X). Sample N trajectories from
exact path law; plug-in (and Miller-Madow) estimates of
  SStill = sum_t N_1(t)        (2x2(x2) tables)
  Scry   = sum_t I[S_t;X_t|X_{t+1:T}]  (conditioning dim grows to 2^7)
vs exact. 20 reps per N in {1e3,1e4,1e5}."""
import numpy as np
from engine import hmm_env_model

def three_phase(T=8, eta=0.1, slip=0.05, J=2.0, r=0.7):
    nH, nX, nS = 3, 2, 2
    Th = np.zeros((nH, nH))
    for h in range(nH):
        Th[(h+1) % nH, h] = 1 - slip; Th[h, h] = slip
    emit = np.zeros((nX, nH))
    for h in range(nH):
        b = 1 if h == 0 else 0
        emit[b, h] = 1 - eta; emit[1-b, h] = eta
    E = np.array([[0.0, J], [J, 0.0]])
    return hmm_env_model(nS, T, E, r, nH, np.full(nH,1/3), [Th]*T, [emit]*T)

m = three_phase(); T = m.T
P = m.P  # dims (s0..sT, x1..xT) = 9 s-dims + 8 x-dims, all size 2
flat = P.ravel(); flat = flat/flat.sum()
shape = P.shape; nd = len(shape)

def decode(idx):
    out = np.empty((len(idx), nd), dtype=np.int64)
    for d in range(nd-1, -1, -1):
        out[:, d] = idx % shape[d]; idx = idx // shape[d]
    return out  # cols: s0..s8, x1..x8 (x_t at col 9+t-1)

def Scol(t): return t
def Xcol(t): return 9 + t - 1  # t>=1

def H_counts(c):
    c = c[c>0].astype(float); n = c.sum()
    return np.log(n) - (c*np.log(c)).sum()/n, len(c)

def MI(cols_a, cols_b, D, mm):
    def key(cols):
        k = np.zeros(len(D), dtype=np.int64)
        for c in cols: k = k*2 + D[:, c]
        return k
    ka, kb = key(cols_a), key(cols_b); kab = ka* (2**len(cols_b)) + kb
    n = len(D)
    Ha,Ka = H_counts(np.bincount(ka)); Hb,Kb = H_counts(np.bincount(kb))
    Hab,Kab = H_counts(np.bincount(kab))
    I = Ha+Hb-Hab
    if mm: I += (Ka-1)/(2*n)+(Kb-1)/(2*n)-(Kab-1)/(2*n)
    return I

def CMI(cols_a, cols_b, cols_c, D, mm):
    # I(A;B|C) = I(A; B,C) - I(A;C)
    return MI(cols_a, cols_b+cols_c, D, mm) - MI(cols_a, cols_c, D, mm)

def estimates(D, mm):
    still = 0.0; cry = 0.0
    for t in range(T):
        i1 = MI([Scol(t)], [Xcol(t)], D, mm) if t >= 1 else 0.0
        i2 = MI([Scol(t)], [Xcol(t+1)], D, mm) if t+1 <= T else 0.0
        still += i1 - i2
        if t >= 1:
            fut = [Xcol(u) for u in range(t+1, T+1)]
            cry += CMI([Scol(t)], [Xcol(t)], fut, D, mm) if fut else MI([Scol(t)],[Xcol(t)],D,mm)
    return still, cry

exS = sum(m.Nk(t,1) for t in range(T)); exC = sum(m.cryptic(t) for t in range(T))
W = m.W_diss()
print(f"exact: bW={W:.4f}  SStill={exS:.4f}  Scry={exC:.4f}   (path cells={flat.size})")
rng = np.random.default_rng(0)
print(f"{'N':>7} {'Still hat':>16} {'bias':>8} | {'cry hat':>16} {'bias':>8} | {'cryMM hat':>16} {'bias':>8}")
for N in [1000, 10000, 100000]:
    Ss, Cs, CsM = [], [], []
    for rep in range(20):
        idx = rng.choice(flat.size, size=N, p=flat)
        D = decode(idx.copy())
        s, c = estimates(D, mm=False); Ss.append(s); Cs.append(c)
        _, cm = estimates(D, mm=True); CsM.append(cm)
    f = lambda a: (np.mean(a), np.std(a))
    (ms,ss),(mc,sc),(mm_,sm) = f(Ss), f(Cs), f(CsM)
    print(f"{N:7d} {ms:8.4f}±{ss:6.4f} {ms-exS:+8.4f} | {mc:8.4f}±{sc:6.4f} {mc-exC:+8.4f} | {mm_:8.4f}±{sm:6.4f} {mm_-exC:+8.4f}")
print("\nNote: plug-in bound-hat can EXCEED true bound and even give false 'violations'")
print("of bW >= bound if bias > slack; slack here:", round(W-exC,4))
