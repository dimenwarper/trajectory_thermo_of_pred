"""Item 1: hybrid bound
Theorem A (no back-action):
  bW_diss >= Sum_t cryptic_t + Sum_t (1 - eta_TV(K_{x_{t+1}})) * Q_t^{(fut)}
with the certified-computable weakening Q_t^{(1)} = <D[p(s_t|x_{t+1}) || pi_{x_{t+1}}]>.
Derivation: residual = Sum_{t<=T-2}(R_t - R''_{t+1}) + R_{T-1};
R''_{t+1} = <D[pK||piK]> <= eta_KL(K) R_t <= eta_TV(K) R_t (Dobrushin dominates
all f-divergence contraction coefficients); then R_t >= Q_t by Lemma-2 coarsening.
Test on a 3-phase hidden-cycle environment (Table-1 style), sweep r.
"""
import numpy as np
from engine import hmm_env_model, kl

def three_phase(T=8, eta=0.1, slip=0.05, J=2.0, r=0.7):
    nH, nX, nS = 3, 2, 2
    Th = np.zeros((nH, nH))
    for h in range(nH):
        Th[(h+1) % nH, h] = 1 - slip
        Th[h, h] = slip
    emit = np.zeros((nX, nH))
    for h in range(nH):
        b = 1 if h == 0 else 0
        emit[b, h] = 1 - eta
        emit[1-b, h] = eta
    E = np.array([[0.0, J], [J, 0.0]])
    h0 = np.full(nH, 1/nH)
    return hmm_env_model(nS, T, E, r, nH, h0, [Th]*T, [emit]*T)

if __name__ == "__main__":
    print(f"{'r':>5} {'bW':>8} {'Scry':>8} {'SStill':>8} {'hyb1':>8} {'hybF':>8} "
          f"{'cry/W':>7} {'hyb1/W':>7} {'hybF/W':>7} {'ok':>3}")
    for r in [0.3, 0.5, 0.7, 0.9, 0.99, 1.0]:
        m = three_phase(r=r)
        T = m.T
        W = m.W_diss()
        Scry = sum(m.cryptic(t) for t in range(T))
        SStill = sum(m.Nk(t, 1) for t in range(T))
        led = [m.step_ledger(t) for t in range(T)]
        etas = [m.dobrushin(x) for x in range(m.nX)]
        # worst-case eta over x (per-step exact would weight by realized x_{t+1};
        # use per-cell exact: (1-eta_{x+1}) inside Q's average) -> compute exact per-x Q
        hyb1 = 0.0
        hybF = 0.0  # full-R version (t<=T-2 uses (1-eta)R_t, plus R_{T-1})
        for t in range(T):
            # Q decomposed per x_{t+1}
            Jm = m.marg([t], [t+1])
            px = Jm.sum(axis=0)
            for x in np.where(px > 0)[0]:
                fac = (1 - etas[x]) if t <= T-2 else 1.0
                # for hyb1 use one-step Q always with (1-eta) except last step full
                hyb1 += fac * px[x] * kl(Jm[:, x]/px[x], m.pi[:, x])
            if t <= T-2:
                # exact-R version, per-cell eta
                cells = m._post_cells(t)
                hybF += sum(w * (1 - etas[xn]) * kl(p, m.pi[:, xn]) for w, p, xn in cells)
            else:
                hybF += led[t]['R']
        b_info = Scry
        b_hyb1 = Scry + hyb1
        b_hybF = Scry + hybF
        ok = (W - b_hybF >= -1e-12) and (W - b_hyb1 >= -1e-12)
        print(f"{r:5.2f} {W:8.4f} {Scry:8.4f} {SStill:8.4f} {b_hyb1:8.4f} {b_hybF:8.4f} "
              f"{Scry/W:7.3f} {b_hyb1/W:7.3f} {b_hybF/W:7.3f} {str(ok):>3}")

    # also sweep emission noise at fixed r
    print("\nsweep eta (r=0.7):")
    print(f"{'eta':>5} {'bW':>8} {'Scry':>8} {'hyb1/W':>7} {'hybF/W':>7}")
    for eta in [0.02, 0.1, 0.25, 0.4]:
        m = three_phase(eta=eta, r=0.7)
        T = m.T; W = m.W_diss()
        Scry = sum(m.cryptic(t) for t in range(T))
        etas = [m.dobrushin(x) for x in range(m.nX)]
        hyb1 = 0.0; hybF = 0.0
        for t in range(T):
            Jm = m.marg([t], [t+1]); px = Jm.sum(axis=0)
            for x in np.where(px > 0)[0]:
                fac = (1 - etas[x]) if t <= T-2 else 1.0
                hyb1 += fac * px[x] * kl(Jm[:, x]/px[x], m.pi[:, x])
            if t <= T-2:
                hybF += sum(w*(1-etas[xn])*kl(p, m.pi[:, xn]) for w, p, xn in m._post_cells(t))
            else:
                hybF += m.step_ledger(t)['R']
        print(f"{eta:5.2f} {W:8.4f} {Scry:8.4f} {(Scry+hyb1)/W:7.3f} {(Scry+hybF)/W:7.3f}")
