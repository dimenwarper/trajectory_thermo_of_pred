"""Theorem C (NEW): without back-action, Sum_t N_{k+1}(t) <= Sum_t N_k(t) for all k.
Proof pairs g_{t+1} <= h_t by conditional DPI. Consequence: summed Still (k=1)
dominates the whole family incl. summed cryptic; the manuscript's 'pad
separation / rising profile / take the max' is impossible without feedback.
Verify per-pair inequality numerically; then search FEEDBACK models for
rising profiles (where the DPI step breaks)."""
import numpy as np
from engine import TwoStroke, jump_kernel
from smoke import random_model
from item2_pad import pad_model
from item1_hybrid import three_phase

rng = np.random.default_rng(7)

def profile(m):
    T = m.T
    return np.array([sum(m.Nk(t, k) for t in range(T)) for k in range(1, T+1)])

def pair_check(m, k):
    """max over t of g_{t+1} - h_t (should be <=0 no-feedback), plus g_1."""
    T = m.T
    def g(t):
        if t + k > T: return 0.0
        return m.I(({t}, set()), (set(), {t+k}), (set(), set(range(max(t,1), t+k))))
    def h(t):
        if t + k + 1 > T: return 0.0
        return m.I(({t}, set()), (set(), {t+k+1}), (set(), set(range(t+1, t+k+1))))
    worst = max(g(t+1) - h(t) for t in range(0, T))
    return worst, g(1)

print("=== no-feedback: verify monotone profile + per-pair DPI ===")
viol = 0
for i in range(30):
    m, _ = random_model(T=5, rng=rng, feedback=False, metro=(i % 3 == 0))
    prof = profile(m)
    mono = np.all(np.diff(prof) <= 1e-12)
    w = max(pair_check(m, k)[0] for k in range(1, m.T))
    g1 = max(pair_check(m, k)[1] for k in range(1, m.T))
    if not mono or w > 1e-12 or g1 > 1e-12: viol += 1
print(f"random no-fb models: violations {viol}/30")
for name, m in [("3-phase HMM", three_phase(r=0.7)), ("pad eta=.05 rho=1", pad_model(eta=0.05, rho=1.0))]:
    prof = profile(m)
    print(f"{name}: profile {np.round(prof, 4)} monotone={np.all(np.diff(prof) <= 1e-12)}")

print("\n=== feedback: search for rising profiles (Sum N_{k+1} > Sum N_k) ===")
best = None
for i in range(3000):
    m, _ = random_model(T=4, rng=rng, feedback=True, metro=False)
    prof = profile(m)
    rise = float(np.max(np.diff(prof)))
    cryVstill = prof[-1] - prof[0]
    if best is None or cryVstill > best[0]:
        best = (cryVstill, rise, prof, m)
print(f"max (Sum cryptic - Sum Still) over 3000 random fb models: {best[0]:.5f}")
print(f"profile of argmax: {np.round(best[2], 4)}  (max single-step rise {best[1]:.5f})")

# a designed feedback pad: environment ECHOES the system state later.
# s copies x_1 = a; env then emits x_2 = junk; x_3 = s_2 XOR c ... needs env to
# see s: with feedback T(x'|x,s) we can emit x_3 = s XOR coin, x_4 = coin reveal.
def designed_fb_pad(T=4, rho=1.0, J=3.0, r=0.9, eps=0.02):
    nS = nX = 2
    E = np.array([[0.0, J], [J, 0.0]])
    Z = np.exp(-E).sum(axis=0); pi = np.exp(-E)/Z
    Ks = jump_kernel(pi, r)
    rho0 = np.array([[0.5, 0.5], [0.5, 0.5]])       # x1 = a fair coin, no fb yet
    Tks = []
    # step to x_2: junk symbol independent
    Tks.append(np.full((2, 2, 2), 0.5))
    # step to x_3: x_3 = s_2 XOR c, c fair coin => x_3 uniform, correlated with s
    T3 = np.zeros((2, 2, 2))
    for x in range(2):
        for s in range(2):
            T3[:, x, s] = 0.5                        # c fair => x3 uniform regardless
    # to carry c we need env memory: env state IS the symbol; instead emit
    # x_3 = s XOR c with c = x_2 (junk reused as the pad key!):
    T3 = np.zeros((2, 2, 2))
    for x2 in range(2):
        for s in range(2):
            x3 = s ^ x2
            T3[x3, x2, s] = 1 - eps
            T3[1-x3, x2, s] = eps
    Tks[0] = np.full((2, 2, 2), 0.5)
    Tks.append(T3)
    # step to x_4: reveal the key x_2? env is Markov in x: x_4 sees only x_3, s_3.
    # reveal s_3 itself with prob rho (env re-echo) -> future unlocks x_3's pad
    T4 = np.zeros((2, 2, 2))
    for x3 in range(2):
        for s in range(2):
            T4[s, x3, s] += rho
            T4[:, x3, s] += (1 - rho)/2
    Tks.append(T4)
    return TwoStroke(nS, nX, T, E, Ks, rho0, Tks)

for rho in [0.0, 0.5, 1.0]:
    m = designed_fb_pad(rho=rho)
    prof = profile(m)
    print(f"designed fb-pad rho={rho}: profile {np.round(prof, 4)}  cry-Still={prof[-1]-prof[0]:+.4f}")
