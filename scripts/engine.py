"""Exact enumeration engine for two-stroke prediction thermodynamics.

Canonical joint array dims: (s0, s1, ..., sT, x1, ..., xT).
beta = 1 throughout; informations in nats.

Step t (t=0..T-1): quench x_t -> x_{t+1} at fixed s_t (x_0 = flat landscape E=0),
then relax s_t -> s_{t+1} under K_{x_{t+1}}.
"""
import numpy as np

LOG0 = 0.0

def xlogx(p):
    out = np.zeros_like(p)
    m = p > 0
    out[m] = p[m] * np.log(p[m])
    return out

def entropy(p):
    return -xlogx(np.asarray(p, dtype=float)).sum()

def kl(p, q):
    p = np.asarray(p, float); q = np.asarray(q, float)
    m = p > 0
    return float(np.sum(p[m] * (np.log(p[m]) - np.log(q[m]))))


class TwoStroke:
    def __init__(self, nS, nX, T, E, Ks, rho0, Tks, s0dist=None):
        """
        E    : (nS, nX) energies, beta=1. pi_x = softmax(-E[:,x]).
        Ks   : (nX, nS, nS) relaxation kernels K[x][s_new, s_old], stationary pi_x.
        rho0 : (nX, nS) p(x1 | s0). (No feedback: columns equal.)
        Tks  : list length T-1 of (nX, nX, nS): Tks[t-1][x_{t+1}, x_t, s_t].
        """
        self.nS, self.nX, self.T = nS, nX, T
        self.E = np.asarray(E, float)
        self.Ks = np.asarray(Ks, float)
        self.rho0 = np.asarray(rho0, float)
        self.Tks = [np.asarray(t, float) for t in Tks]
        self.s0dist = np.full(nS, 1.0/nS) if s0dist is None else np.asarray(s0dist, float)
        Z = np.exp(-self.E).sum(axis=0)          # (nX,)
        self.pi = np.exp(-self.E) / Z             # (nS, nX): pi[s, x]
        self.F = -np.log(Z)                       # (nX,)
        self.F_flat = -np.log(nS)
        self._build()

    def _build(self):
        nS, nX, T = self.nS, self.nX, self.T
        # build in interleaved order (s0, x1, s1, x2, s2, ...), transpose at end
        P = self.s0dist.copy()                    # dims (s0,)
        # step 0: x1 | s0 ; then s1 | s0, x1
        P = P[:, None] * self.rho0.T              # (s0, x1)
        Kb = np.moveaxis(self.Ks, 0, 1)           # (s_new, x, s_old) -> want (s_old, x, s_new)
        Kb = self.Ks.transpose(2, 0, 1)           # (s_old, x, s_new)
        # multiply K[x1][s1, s0]: arr (s0, x1) -> (s0, x1, s1)
        P = P[:, :, None] * Kb                    # broadcast (s0,x1,1)*(s0? no)
        # careful: Kb dims are (s_old, x, s_new); P dims (s0, x1). aligned: s0<->s_old, x1<->x. OK.
        for t in range(1, T):
            Tk = self.Tks[t-1]                    # (x_{t+1}, x_t, s_t)
            Tkm = Tk.transpose(1, 2, 0)           # (x_t, s_t, x_{t+1})
            P = P[..., :, :, None] * Tkm          # trailing (x_t, s_t) -> add x_{t+1}
            # relax: trailing (s_t, x_{t+1}) -> add s_{t+1} via Kb (s_old, x, s_new)
            P = P[..., :, :, None] * Kb
        # dims now: (s0, x1, s1, x2, s2, ..., xT, sT); reorder canonical
        ndim = 2*T + 1
        s_axes = [0] + [2*t + 1 + 1 for t in range(0, 0)]  # placeholder
        s_axes = [0] + [2*t for t in range(1, T+1)]        # s_t at 2t
        x_axes = [2*t - 1 for t in range(1, T+1)]          # x_t at 2t-1
        perm = s_axes + x_axes
        P = np.transpose(P, perm)
        assert abs(P.sum() - 1.0) < 1e-12
        self.P = P                                # dims (s0..sT, x1..xT)

    # ---------- generic marginals / entropies ----------
    def s_axis(self, t): return t
    def x_axis(self, t): return self.T + t        # x_t, t=1..T -> axis T+t ... careful

    def axes(self, s_list=(), x_list=()):
        return tuple(list(s_list) + [self.T + 1 + (x - 1) for x in x_list])

    def marg(self, s_list=(), x_list=()):
        keep = set(self.axes(s_list, x_list))
        drop = tuple(a for a in range(self.P.ndim) if a not in keep)
        M = self.P.sum(axis=drop)
        # result dims ordered by original axis order: s's (ascending) then x's (ascending)
        return M

    def H(self, s_list=(), x_list=()):
        return entropy(self.marg(sorted(s_list), sorted(x_list)))

    def I(self, A, B, C=({}, {})):
        """I[A;B|C], A/B/C = (set_of_s_indices, set_of_x_indices)."""
        As, Ax = set(A[0]), set(A[1]); Bs, Bx = set(B[0]), set(B[1]); Cs, Cx = set(C[0]), set(C[1])
        def h(ss, xx): return self.H(sorted(ss), sorted(xx))
        return (h(As|Cs, Ax|Cx) + h(Bs|Cs, Bx|Cx) - h(Cs, Cx) - h(As|Bs|Cs, Ax|Bx|Cx))

    # ---------- cell machinery ----------
    def joint_s_cells(self, s_list, x_lo, x_hi):
        """joint p(s_list..., x_{x_lo:x_hi}) flattened over x cells; returns
        (arr shape (nS,)*len(s_list)+(M,), digit function for x index)"""
        M = self.marg(sorted(s_list), list(range(x_lo, x_hi+1)))
        k = x_hi - x_lo + 1
        arr = M.reshape(tuple([self.nS]*len(s_list)) + (self.nX**k,))
        def digit(colidx, xt):  # value of x_{xt}
            pos = xt - x_lo
            return (colidx // (self.nX ** (k - 1 - pos))) % self.nX
        return arr, digit, k

    # ---------- physics ----------
    def W_diss(self):
        T = self.T
        w = 0.0
        # t=0: E(s0|x1) - 0
        J = self.marg([0], [1])                    # (s0, x1)
        w += np.sum(J * self.E)
        for t in range(1, T):
            J = self.marg([t], [t, t+1])           # (s_t, x_t, x_{t+1})
            w += np.einsum('sab,sb->', J, self.E) - np.einsum('sab,sa->', J, self.E)
        px = self.marg([], [T])
        dF = float(np.dot(px, self.F)) - self.F_flat
        return w - dF

    # ---------- per-step information & residual quantities ----------
    def cryptic(self, t):
        """I[S_t; X_t | X_{t+1:T}]; t=0 -> 0 (x_0 constant)."""
        if t == 0: return 0.0
        fut = set(range(t+1, self.T+1))
        return self.I(({t}, set()), (set(), {t}), (set(), fut))

    def Nk(self, t, k):
        """window nostalgia, clipped; X_0 treated as empty."""
        T = self.T
        w1 = set(range(max(t,1), min(t+k-1, T)+1))
        w2 = set(range(t+1, min(t+k, T)+1))
        i1 = self.I(({t}, set()), (set(), w1)) if w1 else 0.0
        i2 = self.I(({t}, set()), (set(), w2)) if w2 else 0.0
        return i1 - i2

    def alpha(self, t, j, bar=False):
        T = self.T
        if t + j > T: return 0.0
        cond = set(range(t+1 if bar else max(t,1), t+j))
        return self.I(({t}, set()), (set(), {t+j}), (set(), cond))

    def _post_cells(self, t):
        """cells = x_{t+1:T}: returns P(cell), p(s_t|cell), ref pi_{x_{t+1}} per cell."""
        arr, digit, k = self.joint_s_cells([t], t+1, self.T)  # (nS, M)
        pc = arr.sum(axis=0)
        cols = np.where(pc > 0)[0]
        out = []
        for c in cols:
            xnext = digit(c, t+1)
            out.append((pc[c], arr[:, c] / pc[c], xnext))
        return out

    def R(self, t):
        """R_t = <D[p(s_t|x_{t+1:T}) || pi_{x_{t+1}}]>"""
        return sum(w * kl(p, self.pi[:, xn]) for w, p, xn in self._post_cells(t))

    def Rpp(self, t):
        """R''_t = <D[p(s_t|x_{t:T}) || pi_{x_t}]>; t=0: cells x_{1:T}, ref flat."""
        if t == 0:
            arr, digit, k = self.joint_s_cells([0], 1, self.T)
            pc = arr.sum(axis=0); tot = 0.0
            for c in np.where(pc > 0)[0]:
                tot += pc[c] * kl(arr[:, c]/pc[c], np.full(self.nS, 1/self.nS))
            return tot
        arr, digit, k = self.joint_s_cells([t], t, self.T)
        pc = arr.sum(axis=0); tot = 0.0
        for c in np.where(pc > 0)[0]:
            tot += pc[c] * kl(arr[:, c]/pc[c], self.pi[:, digit(c, t)])
        return tot

    def step_ledger(self, t):
        """Returns dict with R_t, Dq = <D[q||pi]>, C_t, and (needs t<=T-1):
        Phi_t = R''_{t+1} - Dq, Delta_t, Xi_t, bTE_t, plus Q_t and Mmax."""
        cells = self._post_cells(t)
        # p(s_{t+1} | x_{t+1:T})
        arr2, digit2, _ = self.joint_s_cells([t+1], t+1, self.T)
        pc2 = arr2.sum(axis=0)
        Rt, Dq, Delta, Rpp_next, Mmax = 0.0, 0.0, 0.0, 0.0, 0.0
        idx = 0
        arr1, digit1, _ = self.joint_s_cells([t], t+1, self.T)
        pc1 = arr1.sum(axis=0)
        for c in np.where(pc1 > 0)[0]:
            w = pc1[c]
            p_st = arr1[:, c] / w
            xn = digit1(c, t+1)
            ref = self.pi[:, xn]
            q = self.Ks[xn] @ p_st
            p_next = arr2[:, c] / pc2[c]
            Rt += w * kl(p_st, ref)
            Dq += w * kl(q, ref)
            Delta += w * kl(p_next, q)
            Rpp_next += w * kl(p_next, ref)
            m = q > 0
            if np.any(m):
                Mmax = max(Mmax, float(np.max(np.abs(np.log(q[m]) - np.log(ref[m])))))
        Ct = Rt - Dq
        Phi = Rpp_next - Dq
        Xi = Phi - Delta
        # backward transfer entropy I[S_{t+1}; X_{t+2:T} | S_t, X_{t+1}]
        if t + 2 <= self.T:
            bTE = self.I(({t+1}, set()), (set(), set(range(t+2, self.T+1))),
                         ({t}, {t+1}))
        else:
            bTE = 0.0
        # one-step quench mismatch Q_t = <D[p(s_t|x_{t+1}) || pi_{x_{t+1}}]>
        Jm = self.marg([t], [t+1])   # (s_t, x_{t+1})
        px = Jm.sum(axis=0); Q = 0.0
        for x in np.where(px > 0)[0]:
            Q += px[x] * kl(Jm[:, x]/px[x], self.pi[:, x])
        return dict(R=Rt, Dq=Dq, C=Ct, Phi=Phi, Delta=Delta, Xi=Xi, bTE=bTE,
                    Rpp_next=Rpp_next, Q=Q, Mmax=Mmax)

    # ---------- dual (past) filtration ----------
    def Ppost(self, t):
        arr, digit, k = self.joint_s_cells([t], 1, t+1)
        pc = arr.sum(axis=0); tot = 0.0
        for c in np.where(pc > 0)[0]:
            tot += pc[c] * kl(arr[:, c]/pc[c], self.pi[:, digit(c, t+1)])
        return tot

    def Ppre(self, t):
        if t == 0:
            return kl(self.marg([0]), np.full(self.nS, 1/self.nS))
        arr, digit, k = self.joint_s_cells([t], 1, t)
        pc = arr.sum(axis=0); tot = 0.0
        for c in np.where(pc > 0)[0]:
            tot += pc[c] * kl(arr[:, c]/pc[c], self.pi[:, digit(c, t)])
        return tot

    def stateTE(self, t):
        """I[S_t; X_{t+1} | X_{1:t}]"""
        return self.I(({t}, set()), (set(), {t+1}), (set(), set(range(1, t+1))))

    def massey_DI(self):
        """Massey directed information sum_t I[S_{0:t}; X_{t+1} | X_{1:t}]"""
        tot = 0.0
        for t in range(0, self.T):
            tot += self.I((set(range(0, t+1)), set()), (set(), {t+1}),
                          (set(), set(range(1, t+1))))
        return tot

    def dobrushin(self, x):
        K = self.Ks[x]
        nS = self.nS
        m = 0.0
        for a in range(nS):
            for b in range(nS):
                m = max(m, 0.5*np.abs(K[:, a]-K[:, b]).sum())
        return m


# ---------- kernels & builders ----------
def jump_kernel(pi_sx, r):
    """K_x = (1-r) I + r Pi_x for each x. pi_sx: (nS,nX)."""
    nS, nX = pi_sx.shape
    Ks = np.zeros((nX, nS, nS))
    for x in range(nX):
        Ks[x] = (1-r)*np.eye(nS) + r*np.tile(pi_sx[:, x][:, None], (1, nS))
    return Ks

def metropolis_kernel(pi_sx, prop_logits):
    """Random-proposal Metropolis kernels with stationary pi_x."""
    nS, nX = pi_sx.shape
    Ks = np.zeros((nX, nS, nS))
    for x in range(nX):
        Praw = np.exp(prop_logits[x]); Praw = Praw / Praw.sum(axis=0, keepdims=True)  # (s_new,s_old)
        pi = pi_sx[:, x]
        K = np.zeros((nS, nS))
        for so in range(nS):
            for sn in range(nS):
                if sn == so: continue
                a = min(1.0, (pi[sn]*Praw[so, sn])/(pi[so]*Praw[sn, so])) if pi[so]*Praw[sn, so] > 0 else 1.0
                K[sn, so] = Praw[sn, so]*a
            K[so, so] = 1.0 - K[:, so].sum() + K[so, so]
        Ks[x] = K
    return Ks

def hmm_env_model(nS, T, E, r, nH, h0, Th, emit, Ks=None):
    """Autonomous hidden-state environment: builds equivalent TwoStroke via
    time-dependent observable kernels?  Instead: exact construction of the
    joint by first computing p(x_{1:T}) then attaching the s-chain.
    Th: list len T of (nH,nH) hidden transitions applied before each emission
    (Th[0] maps h0 dist), emit: list len T of (nX,nH) emission matrices.
    Returns a TwoStroke-like object with .P built directly."""
    nX = emit[0].shape[0]
    # p over x-paths
    alpha = h0.copy()  # (nH,)
    paths = np.ones(1)
    # we need p(x_{1:T}) as array (nX,)*T: forward with path-indexed alphas
    A = (Th[0] @ alpha)[None, :]   # (npaths=1, nH)
    PX = np.ones((1,))
    Xarrs = None
    alphas = A  # (npaths, nH) unnormalized: p(h_t, x_{1:t}=path)
    npaths = 1
    for t in range(T):
        if t > 0:
            alphas = alphas @ Th[t].T   # h_{t-1} -> h_t : new_alpha[p,h'] = sum_h Th[h',h] alpha[p,h]
        Em = emit[t]                    # (nX, nH)
        # branch on x_t
        new = np.einsum('ph,xh->pxh', alphas, Em).reshape(npaths*nX, -1)
        alphas = new
        npaths *= nX
    px = alphas.sum(axis=1)             # (nX^T,) p(x path), path index base-nX, x1 most significant
    px = px.reshape((nX,)*T)
    # attach s-chain: P[s0..sT, x1..xT] = u(s0) px(x) prod K[x_{t+1}](s_{t+1}|s_t)
    if Ks is None:
        Z = np.exp(-np.asarray(E)).sum(axis=0); pi = np.exp(-np.asarray(E))/Z
        Ks = jump_kernel(pi, r)
    model = object.__new__(TwoStroke)
    model.nS, model.nX, model.T = nS, nX, T
    model.E = np.asarray(E, float)
    Z = np.exp(-model.E).sum(axis=0)
    model.pi = np.exp(-model.E)/Z
    model.F = -np.log(Z); model.F_flat = -np.log(nS)
    model.Ks = np.asarray(Ks)
    model.s0dist = np.full(nS, 1.0/nS)
    # build P: dims (s0..sT, x1..xT)
    shape = (nS,)*(T+1) + (nX,)*T
    P = np.zeros(shape)
    # iterate: start with u(s0) px broadcast, then multiply K factors
    # do it as: P = u[s0] * px[x] * prod_t K[x_{t+1}][s_{t+1}, s_t]
    # build multiplicatively with broadcasting via einsum-free loop
    P = np.ones(shape)
    # u(s0)
    sh = [1]*(2*T+1); sh[0] = nS
    P = P * model.s0dist.reshape(sh)
    shx = [1]*(2*T+1)
    for i in range(T): shx[T+1+i] = nX
    P = P * px.reshape(shx)
    for t in range(T):
        # K[x_{t+1}][s_{t+1}, s_t]: dims s_{t+1}=axis t+1, s_t = axis t, x_{t+1} = axis T+1+t
        sh = [1]*(2*T+1); sh[t+1] = nS; sh[t] = nS; sh[T+1+t] = nX
        Karr = np.moveaxis(model.Ks, 0, -1)  # (s_new, s_old, x)
        block = np.zeros((nS, nS, nX))
        block[:] = Karr
        # reshape to broadcast: axes (t (s_old), t+1 (s_new), T+1+t (x))
        full = np.ones((nS, nS, nX))
        full = Karr  # (s_new, s_old, x)
        # target order: axis t = s_old, axis t+1 = s_new, axis T+1+t = x
        b = np.transpose(full, (1, 0, 2))  # (s_old, s_new, x)
        newshape = [1]*(2*T+1)
        newshape[t] = nS; newshape[t+1] = nS; newshape[T+1+t] = nX
        P = P * b.reshape(newshape)
    model.P = P / P.sum()
    return model
