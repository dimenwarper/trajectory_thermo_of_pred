import numpy as np
from engine import TwoStroke, jump_kernel, metropolis_kernel, kl

rng = np.random.default_rng(0)

def random_model(T=4, nS=2, nX=2, r=None, feedback=True, metro=False, rng=rng):
    E = rng.uniform(-2, 2, (nS, nX))
    Z = np.exp(-E).sum(axis=0); pi = np.exp(-E)/Z
    if r is None: r = rng.uniform(0.2, 0.95)
    if metro:
        Ks = metropolis_kernel(pi, rng.uniform(-1, 1, (nX, nS, nS)))
    else:
        Ks = jump_kernel(pi, r)
    def stoch(shape, ax=0):
        A = rng.uniform(0.05, 1, shape); return A/A.sum(axis=ax, keepdims=True)
    rho0 = stoch((nX, nS))
    if not feedback:
        rho0 = np.tile(rho0[:, :1], (1, nS))
    Tks = []
    for t in range(T-1):
        Tk = stoch((nX, nX, nS))
        if not feedback:
            Tk = np.tile(Tk[:, :, :1], (1, 1, nS))
        Tks.append(Tk)
    return TwoStroke(nS, nX, T, E, Ks, rho0, Tks), r

def check(m, label):
    T = m.T
    W = m.W_diss()
    cry = [m.cryptic(t) for t in range(T)]
    led = [m.step_ledger(t) for t in range(T)]
    Rs = [l['R'] for l in led]
    Rpps = [m.Rpp(t) for t in range(T)]
    gap1 = W - (sum(cry) + sum(Rs) - sum(Rpps))
    # Theorem-3 ledger: W = sum cry + sum_{t<=T-2}(C_t - Phi_t) + R_{T-1} - R''_0
    CmP = sum(led[t]['C'] - led[t]['Phi'] for t in range(T-1))
    gap3 = W - (sum(cry) + CmP + Rs[T-1] - Rpps[0])
    # R''_0 = I[S_0; X_{1:T}]
    I0 = m.I(({0}, set()), (set(), set(range(1, T+1))))
    gapR0 = Rpps[0] - I0
    # bookkeeping of Rpp_next vs Rpp(t+1)
    gapRpp = max(abs(led[t]['Rpp_next'] - Rpps[t+1]) for t in range(T-1))
    # Lemma 3: Delta_t <= bTE_t
    lem3 = max(led[t]['Delta'] - led[t]['bTE'] for t in range(T-1))
    # Theorem 4 dual identity
    Ppost = [m.Ppost(t) for t in range(T)]
    Ppre = [m.Ppre(t) for t in range(T)]
    ste = [m.stateTE(t) for t in range(T)]
    gap4 = W - (-sum(ste) + sum(Ppost) - sum(Ppre))
    resid4 = sum(Ppost) - sum(Ppre)
    # per-pair contraction of dual residuals: Ppre_{t+1} <= Ppost_t
    dualpair = max(Ppre[t+1] - Ppost[t] for t in range(T-1))
    # Corollary 3 duality (no feedback only)
    print(f"{label}: gap1={gap1:.2e} gap3={gap3:.2e} R0-I0={gapR0:.2e} "
          f"Rppnext={gapRpp:.2e} lem3max={lem3:.2e} gap4={gap4:.2e} "
          f"resid4={resid4:.3f} dualpair_max={dualpair:.2e} W={W:.3f}")
    return dict(W=W, cry=cry, led=led)

if __name__ == "__main__":
    for i in range(4):
        m, r = random_model(feedback=True, metro=(i % 2 == 1))
        check(m, f"fb  model {i} (metro={i%2==1})")
    for i in range(2):
        m, r = random_model(feedback=False)
        d = check(m, f"nofb model {i}")
        # no feedback: Phi_t = 0, residual pairing R''_{t+1} <= R_t
        led = d['led']; T = m.T
        print("   max|Phi| (should be ~0):", max(abs(l['Phi']) for l in led[:T-1]),
              " min C_t:", min(l['C'] for l in led[:T-1]))
        # Corollary 3 learning duality
        W = d['W']
        lhs = sum(d['cry'])
        fut = lambda t: set(range(t+1, T+1))
        anticip = sum(m.I(({t+1}, set()), (set(), fut(t))) - m.I(({t}, set()), (set(), fut(t)))
                      for t in range(T-1))
        # doc: sum_t (I[S_{t+1};X_{t+1:T}] - I[S_t;X_{t+1:T}]) - I[S_T;X_T]
        anticip2 = sum(m.I(({t+1}, set()), (set(), set(range(t+1, T+1)))) -
                       m.I(({t}, set()), (set(), set(range(t+1, T+1)))) for t in range(T))
        dual_gap = lhs - (anticip2 - m.I(({T}, set()), (set(), {T})))
        print("   Corollary-3 telescoping gap:", f"{dual_gap:.2e}")
