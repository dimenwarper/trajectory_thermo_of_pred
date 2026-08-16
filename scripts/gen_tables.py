"""Regenerate tables for manuscript v2: hybrid r-sweep (Table 2 of v2) and
feedback g-sweep with oracular/Cor6 columns (Table 5 of v2)."""
import io, contextlib
import numpy as np
with contextlib.redirect_stdout(io.StringIO()):
    import item1_hybrid as I1   # gives three_phase; suppress its sweeps
from engine import kl, TwoStroke, jump_kernel

# ---- Table: hybrid bound, r sweep, three-phase HMM T=8, eta=.1, J=2
print("TABLE hybrid (three-phase HMM, T=8, eta=0.1, slip=0.05, J=2):")
print("r | bW | Scry | SStill | hyb1 | hybF")
for r in [0.3, 0.5, 0.7, 0.9, 1.0]:
    m = I1.three_phase(r=r); T = m.T; W = m.W_diss()
    Scry = sum(m.cryptic(t) for t in range(T))
    SStill = sum(m.Nk(t,1) for t in range(T))
    etas = [m.dobrushin(x) for x in range(m.nX)]
    hyb1 = 0.0; hybF = 0.0
    for t in range(T):
        Jm = m.marg([t],[t+1]); px = Jm.sum(axis=0)
        for x in np.where(px>0)[0]:
            fac = (1-etas[x]) if t <= T-2 else 1.0
            hyb1 += fac*px[x]*kl(Jm[:,x]/px[x], m.pi[:,x])
        if t <= T-2:
            cells = m._post_cells(t)
            hybF += sum(w*(1-etas[xn])*kl(p, m.pi[:,xn]) for w,p,xn in cells)
        else:
            hybF += m.step_ledger(t)['R']
    print(f"{r:.2f} | {W:.3f} | {Scry:.3f} | {SStill:.3f} | {Scry+hyb1:.3f} | {Scry+hybF:.3f}")

# ---- Table: feedback g-sweep with oracular column
# Copy-feedback environment: x_{t+1} = s_t w.p. g, else x flips w.p. 0.3.
# Two states, E=[[0,J],[J,0]], J=1.5, T=6, jump kernel r.
def copy_model(g, r, T=6, J=1.5, flip=0.3):
    nS = nX = 2
    E = np.array([[0.0,J],[J,0.0]])
    Z = np.exp(-E).sum(axis=0); pi = np.exp(-E)/Z
    Ks = jump_kernel(pi, r)
    rho0 = np.full(nS, 0.5)
    base = np.array([[1-flip, flip],[flip, 1-flip]])  # [xnew, xold]
    Tk = np.zeros((nX, nX, nS))
    for xo in range(nX):
        for s in range(nS):
            for xn in range(nX):
                Tk[xn, xo, s] = g*(1.0 if xn==s else 0.0) + (1-g)*base[xn,xo]
    return TwoStroke(nS, nX, T, E, Ks, rho0, [Tk]*(T-1))

print("\nTABLE feedback oracular (copy env, T=6, J=1.5, flip=0.3):")
print("g | r | bW | Scry | SPhi | SbTE | Sorac | I0 | Thm5bnd | Cor5bnd | Cor6bnd | -T_SX")
for g in [0.0, 0.3, 0.7, 0.95]:
    for r in [0.5, 1.0]:
        m = copy_model(g, r); T = m.T; W = m.W_diss()
        Scry = sum(m.cryptic(t) for t in range(T))
        led = [m.step_ledger(t) for t in range(T-1)]
        SPhi = sum(l['Phi'] for l in led)
        SbTE = sum(l['bTE'] for l in led)
        Sorac = sum(m.I(({t+1},set()), (set(), set(range(t+2,T+1))), (set(),{t+1}))
                    for t in range(T-1))
        I0 = m.I(({0},set()), (set(), set(range(1,T+1))))
        # Cor5 kinetic constant
        pmin = m.pi.min()
        M = max(np.log(1/r), np.log(r+(1-r)/pmin)) if r < 1 else 0.0
        Cor5 = Scry - sum(l['bTE'] + M*np.sqrt(2*max(l['bTE'],0.0)) for l in led) - I0
        thm5 = Scry - SPhi - I0
        Cor6 = Scry - Sorac - I0
        TSX = sum(m.I(({t},set()), (set(),{t+1}), (set(), set(range(1,t+1))))
                  for t in range(T))
        print(f"{g:.2f} | {r:.1f} | {W:+.3f} | {Scry:.3f} | {SPhi:.3f} | {SbTE:.3f} | "
              f"{Sorac:.3f} | {I0:.3f} | {thm5:+.3f} | {Cor5:+.3f} | {Cor6:+.3f} | {-TSX:+.3f}")
