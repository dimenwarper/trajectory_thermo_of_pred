"""Item 5b: skew baker's map (invertible) Monte Carlo.
Map on unit square, a=0.6:
  u<a:  (u/a, a*v)         else: ((u-a)/(1-a), a+(1-a)*v)
lambda_u = H(a) = 0.673 nats. Observable X_t from state at time t.
S = coarse bin of (u0,v0), 2^p bins per axis.
N_k = I[S; W_{0:k-1}] - I[S; W_{1:k}]  (words as ints).
Degenerate obs: x=[u>=0.5] (constant along stable/v direction -> genericity fails,
 expect N_k -> lambda like tent map, no embedding closure).
Generic obs:    x=[frac(u+0.618*v)>=0.5] (mixes u,v -> S recoverable from word,
 expect N_k -> ~0 beyond embedding window).
Plug-in MI with Miller-Madow, half-sample stability."""
import numpy as np

rng = np.random.default_rng(7)
a = 0.6
lam = -(a*np.log(a)+(1-a)*np.log(1-a))
N = 10_000_000
KMAX = 14
p = 6  # 64 bins per axis -> 4096 S cells

u = rng.random(N); v = rng.random(N)
S = (np.floor(u*(1<<p)).astype(np.int64)*(1<<p) + np.floor(v*(1<<p)).astype(np.int64))

def step(u, v):
    m = u < a
    un = np.where(m, u/a, (u-a)/(1-a))
    vn = np.where(m, a*v, a+(1-a)*v)
    return un, vn

def obs_deg(u, v):  return (u >= 0.5).astype(np.int64)
def obs_gen(u, v):  return (np.mod(u+0.618*v, 1.0) >= 0.5).astype(np.int64)

def MI_mm(A, B):
    """plug-in MI + Miller-Madow correction, A,B int arrays"""
    ja, ia = np.unique(A, return_inverse=True)
    jb, ib = np.unique(B, return_inverse=True)
    nj = len(ja)*len(jb)
    joint = np.bincount(ia*len(jb)+ib, minlength=nj).astype(float)
    joint /= joint.sum()
    pa = np.bincount(ia, minlength=len(ja)).astype(float); pa/=pa.sum()
    pb = np.bincount(ib, minlength=len(jb)).astype(float); pb/=pb.sum()
    def H(q):
        q = q[q>0]; return -(q*np.log(q)).sum()
    Ka = (pa>0).sum(); Kb=(pb>0).sum(); Kj=(joint>0).sum()
    n = len(A)
    mm = (Ka-1)/(2*n) + (Kb-1)/(2*n) - (Kj-1)/(2*n)
    return H(pa)+H(pb)-H(joint) + mm

def run(obs, label):
    uu, vv = u.copy(), v.copy()
    words = np.zeros(N, dtype=np.int64)   # W_{0:k-1}
    x0 = obs(uu, vv)                      # word bit at t=0
    print(f"\n== {label} ==  (lam={lam:.4f})")
    xs = [x0]
    Nk = []
    for k in range(1, KMAX+1):
        # advance to get x_{k-1} if needed
        while len(xs) < k+1:  # need bits 0..k (k+1 bits so word W_{1:k} available)
            uu, vv = step(uu, vv)
            xs.append(obs(uu, vv))
        W0 = xs[0].copy()
        for j in range(1, k):  W0 = W0*2 + xs[j]
        W1 = xs[1].copy()
        for j in range(2, k+1): W1 = W1*2 + xs[j]
        I0 = MI_mm(S, W0); I1 = MI_mm(S, W1)
        # half-sample stability
        h = N//2
        I0h = MI_mm(S[:h], W0[:h]); I1h = MI_mm(S[:h], W1[:h])
        nk = I0-I1; nkh = I0h-I1h
        Nk.append(nk)
        print(f" k={k:2d}  I[S;W0k]={I0:7.4f}  I[S;W1k]={I1:7.4f}  N_k={nk:7.4f}  (half: {nkh:7.4f}, d={abs(nk-nkh):.4f})")
    return np.array(Nk)

nk_d = run(obs_deg, "DEGENERATE x=[u>=0.5] (constant along v)")
nk_g = run(obs_gen, "GENERIC x=[frac(u+0.618v)>=0.5]")
print("\nSummary: deg tail mean(k=10..14) =", nk_d[9:].mean().round(4),
      " vs lam =", lam.round(4))
print("         gen tail mean(k=10..14) =", nk_g[9:].mean().round(4))
print("         gen peak =", nk_g.max().round(4), "at k =", int(nk_g.argmax()+1))
