"""Item 5a: exact (interval-arithmetic) horizon profiles for quantized chaos.
Skew tent map f(z)=z/a (z<a), (1-z)/(1-a) (else); Lebesgue invariant;
Lyapunov exponent lambda = H(a) = -a ln a - (1-a) ln(1-a) = KS entropy.
Observable: m-bit quantization X_t = floor(2^m f^t(z)).  State: delta-bin of z_0.
All entropies computed EXACTLY from interval lengths (piecewise-linear map =>
symbol partitions are finite unions of intervals).
Tests: (i) N_k asymptote = folding entropy = lambda; (ii) alpha-bar support
knee at k* ~ (ln(1/delta))/lambda; (iii) presence/absence of an embedding
shoulder for this non-invertible (Regime III) system."""
import numpy as np

def profiles(a=0.6, m=2, p_delta=10, K=14):
    lam = -(a*np.log(a) + (1-a)*np.log(1-a))
    # breakpoints: union over j<=K of f^{-j}(m-grid), plus delta-grid
    grid = np.arange(0, 2**m + 1) / 2**m
    pts = [grid.copy()]
    cur = grid.copy()
    for j in range(K):
        cur = np.concatenate([a*cur, 1 - (1-a)*cur])
        pts.append(cur)
    B = np.concatenate(pts + [np.arange(0, 2**p_delta + 1)/2**p_delta])
    B = np.unique(np.clip(B, 0, 1))
    mid = 0.5*(B[:-1] + B[1:])
    L = np.diff(B)
    # forward words
    z = mid.copy()
    words = np.zeros((len(mid), K+1), dtype=np.int64)
    for t in range(K+1):
        words[:, t] = np.minimum((z * 2**m).astype(np.int64), 2**m - 1)
        z = np.where(z < a, z/a, (1-z)/(1-a))
    zbin = np.minimum((mid * 2**p_delta).astype(np.int64), 2**p_delta - 1)

    def Hof(codes):
        # entropy of the partition labeled by integer codes, lengths L
        order = np.argsort(codes, kind='stable')
        c = codes[order]; l = L[order]
        cuts = np.nonzero(np.diff(c))[0] + 1
        sums = np.add.reduceat(l, np.concatenate([[0], cuts]))
        s = sums[sums > 0]
        return float(-(s*np.log(s)).sum())

    def code(cols, withz=False):
        c = np.zeros(len(mid), dtype=np.int64)
        for j in cols:
            c = c*(2**m) + words[:, j]
        if withz:
            c = c*(2**p_delta) + zbin
        return c

    Hz = p_delta*np.log(2)
    out = {}
    Nk, abar = [], []
    for k in range(1, K+1):
        w0 = list(range(0, k)); w1 = list(range(1, k+1))
        I0 = Hof(code(w0)) + Hz - Hof(code(w0, True))
        I1 = Hof(code(w1)) + Hz - Hof(code(w1, True))
        Nk.append(I0 - I1)
        # abar_k = I[Z; X_k | X_{1:k-1}]
        wc = list(range(1, k))
        Hc = Hof(code(wc)) if wc else 0.0
        Hcz = Hof(code(wc, True)) if wc else Hz
        Hck = Hof(code(wc + [k]))
        Hckz = Hof(code(wc + [k], True))
        abar.append((Hcz - Hz) + Hck - Hc - (Hckz - Hz) - 0.0)
        # I[Z;X_k|X_{1:k-1}] = H(Xk|cond) - H(Xk|cond,Z)
        abar[-1] = (Hck - Hc) - (Hckz - Hcz)
    return lam, np.array(Nk), np.array(abar)

print("=== skew tent, exact interval computation ===")
for a in (0.6, 0.75):
    for m in (1, 2):
        for p in (6, 10, 14):
            K = min(16, p + 6)
            lam, Nk, ab = profiles(a=a, m=m, p_delta=p, K=K)
            kstar_pred = p*np.log(2)/lam
            # measured knee: first k where abar_k < 0.05*abar_1
            idx = np.where(ab < 0.05*max(ab[0], 1e-12))[0]
            kmeas = (idx[0]+1) if len(idx) else np.nan
            print(f"a={a} m={m} delta=2^-{p} lam={lam:.3f} pred k*~{kstar_pred:4.1f} "
                  f"meas~{kmeas}  N_last={Nk[-1]:.3f}")
            if m == 2 and p == 10:
                print("   N_k   :", np.round(Nk, 3))
                print("   abar_k:", np.round(ab, 3))
