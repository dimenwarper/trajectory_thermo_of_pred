"""Item 2: physically instantiate the one-time-pad separation.
Environment (T=6, two rounds of 3 symbols): hidden bits (a,b) fresh each round.
  t=1,4: 'A' symbol carrying a (flipped w.p. eta)   -> coupled landscape (J)
  t=2,5: 'C' symbol carrying a XOR b (exact)        -> flat landscape
  t=3,6: 'B' symbol carrying b w.p. rho, else coin  -> flat landscape
Alphabet x in {A0,A1,C0,C1,B0,B1} = {0..5}.
System: 2 states, jump-kernel relaxation r. It copies 'a' during the A stroke
and then holds it (imperfectly, decay (1-r) per step) through the C stroke.
At the C step: I[S;X_t] ~ I[a; a^b] = 0 (Still blind), but conditioned on the
future B symbol (which reveals b w.p. rho) the pad unlocks: cryptic > 0.
"""
import numpy as np
from engine import hmm_env_model

def pad_model(T=6, eta=0.1, rho=1.0, J=2.5, r=0.5):
    nH = 4   # (a,b)
    nX, nS = 6, 2
    h0 = np.full(nH, 1/nH)
    def hbits(h): return h >> 1, h & 1
    Th_hold = np.eye(nH)
    Th_new = np.full((nH, nH), 1/nH)      # resample both bits
    Ths, emits = [], []
    for t in range(1, T+1):
        ph = (t-1) % 3   # 0=A,1=C,2=B
        Ths.append(Th_new if ph == 0 else Th_hold)
        Em = np.zeros((nX, nH))
        for h in range(nH):
            a, b = hbits(h)
            if ph == 0:
                Em[0 + (a ^ 1), h] += eta      # A with flipped bit
                Em[0 + a, h] += 1 - eta
            elif ph == 1:
                Em[2 + (a ^ b), h] = 1.0
            else:
                Em[4 + b, h] += rho
                Em[4 + 0, h] += (1 - rho)/2
                Em[4 + 1, h] += (1 - rho)/2
        emits.append(Em)
    E = np.zeros((nS, nX))
    E[:, 0] = [0.0, J]   # A0 favors s=0
    E[:, 1] = [J, 0.0]   # A1 favors s=1
    # C*, B* flat
    return hmm_env_model(nS, T, E, r, nH, h0, Ths, emits)

hdr = f"{'eta':>5} {'rho':>5} {'bW':>7} {'S_k1':>7} {'S_kT':>7} {'bestS':>7} {'k*':>3} {'winner':>8}"
if __name__ == "__main__":
    print(hdr)
    rows = []
    for eta in [0.05, 0.2]:
        for rho in [0.0, 0.25, 0.5, 0.75, 1.0]:
            m = pad_model(eta=eta, rho=rho)
            T = m.T
            W = m.W_diss()
            Ssum = {}
            for k in range(1, T+1):
                Ssum[k] = sum(m.Nk(t, k) for t in range(T))
            kstar = max(Ssum, key=Ssum.get)
            win = 'cryptic' if Ssum[T] > Ssum[1] + 1e-12 else ('Still' if Ssum[1] > Ssum[T] + 1e-12 else 'tie')
            print(f"{eta:5.2f} {rho:5.2f} {W:7.4f} {Ssum[1]:7.4f} {Ssum[T]:7.4f} "
                  f"{Ssum[kstar]:7.4f} {kstar:3d} {win:>8}")
            rows.append((eta, rho, W, Ssum))

    # detailed per-step decomposition at the extreme point to show the mechanism
    m = pad_model(eta=0.05, rho=1.0)
    T = m.T
    print("\nper-step (eta=0.05, rho=1.0):  t : N_1(t)  N_T(t)=cryptic")
    for t in range(1, T+1 - 0):
        if t >= T: break
    for t in range(T):
        print(f"  t={t}: Still={m.Nk(t,1):7.4f}  cryptic={m.cryptic(t):7.4f}")
    # sanity: full profile at that point
    print("\nSum_t N_k profile (eta=.05, rho=1):",
          [round(sum(m.Nk(t, k) for t in range(T)), 4) for k in range(1, T+1)])
