---
title: The Price of Remembering — an interactive explainer
kicker: An interactive explainer · thermodynamics of prediction
hero_title: The Price of<br>Remembering
hero_sub: Every thing that reacts to the world keeps a record of it — and physics charges rent for records, paid in heat. A layman's walk through our 2026 paper, where we work out <em>exactly</em> which memories cost, which are free, and the loophole that lets you bill the world instead.
hero_src: <b>Companion to our paper:</b> "A Trajectory-Level Identity for the Thermodynamics of Prediction, With and Without Back-Action" (2026). This page simplifies aggressively; every number in the interactive figures comes from our machine-verified tables.
footer: This explainer compresses our technical paper into pictures; the paper itself is precise where this page waves hands. All interactive figures use our published, exactly-enumerated tables (Tables 1, 2, 6 and the §6 chaotic-map computations); curves between tabulated points are interpolated and marked as such. Nats, not bits, throughout — one nat ≈ 1.44 bits.
footer_fin: Fig. ledger closed · dissipation ≥ crypticity − oracularity · 2026
---

# [Entry 01 · The setup] A world that pushes, a system that settles

:::lede
A thermostat tracks the temperature. A bacterium tracks the sugar gradient it swims through. Your neurons track the sentence you're reading. None of them chose to become records of their surroundings — it happens automatically, because anything a changing world pushes on ends up statistically correlated with the pushing.
:::

Statistical physics has a striking thing to say about this: <strong>those correlations have an energy bill.</strong> To see where the bill comes from, we use the simplest possible cartoon of "a thing driven by a world," borrowed from a famous 2012 result. Time ticks in steps. At each tick, two things happen:

:::figure "FIG 1" two-stroke
<b>The two-stroke heartbeat.</b> Each time step: (1) the environment signal jumps, which instantly reshapes the system's energy landscape — that shove does <span style="color:var(--heat);font-weight:600">work</span> on the system; (2) the system relaxes one step toward the new valley, dumping <span style="color:var(--heat);font-weight:600">heat</span> into its surroundings. The environment can be anything: rhythmic, random, long-memoried — later, even something that listens back.
:::

Some of the work pushed in is legitimately stored (the system ends up higher on the ladder of useful free energy). The rest is <span class="term hot">dissipated work</span> — energy that came in as an orderly shove and left as disorderly heat. Wasted. The whole game of this subject is:

:::pull
How little heat can a system that lives in a changing world <i>possibly</i> waste — and what does the answer have to do with what it remembers?
:::

# [Entry 02 · The 2012 rule] Useless memory costs heat

In 2012, Still, Sivak, Bell and Crooks proved something lovely. Because the system is physically pushed around by the signal, its internal state <span class="mth">S</span> inevitably carries information about the signal. Split that information in two:

:::raw
<p style="margin-bottom:.6em"><strong style="color:var(--free)">The predictive part</strong> — bits about the current signal that are still useful for anticipating the <em>next</em> one.</p>
<p><strong style="color:var(--heat)">The nostalgic part</strong> — bits about the current signal that will be useless one tick from now. Memory for memory's sake.</p>
:::

:::figure "FIG 2" nostalgia
<b>Nostalgia = memory − predictive power.</b> The 2012 bound: dissipated work per step is at least <span class="mth">k<tspan style="font-size:.8em">B</tspan>T</span> × nostalgia. Clinging to the past, if the past won't help you with the future, is physically expensive. A perfect predictor — remembering only what forecasts — can in principle run cool.
:::

That result launched a small field. But it also left two itches that we set out to scratch. <strong>First:</strong> "useful for the next tick" is a strangely short horizon — what about signals whose patterns only make sense over long stretches? <strong>Second, and more embarrassing:</strong> when you actually compute the bound, it typically explains only a small sliver of the heat a real system wastes. Where's the rest?

# [Entry 03 · The exact identity] Only secrets cost

:::lede
Our first move is to stop asking "is this memory useful to <em>me</em>?" and start asking "will the <em>world itself</em> ever repeat it?"
:::

Here is the reframe. Look at everything the system's state knows about the present signal. Some of that information will be broadcast again anyway — the future of the signal will reveal it, whether or not the system bothered to remember. And some of it is <em>gone</em>: the signal's entire future, watched to the end of time, would never disclose it again. We call that second kind <span class="term hot">cryptic information</span> — what the state stores about the present that the future never tells.

:::figure "FIG 3" cryptic
<b>The green part is thermodynamically free</b> — whether or not the system ever "uses" it — because the world's own future is a backup copy. Only the <b>red, cryptic part</b> shows up on the heat bill. In symbols: cryptic information is <span class="mth">I[S<tspan style="font-size:.75em">t</tspan> ; x<tspan style="font-size:.75em">t</tspan> | future]</span>, the state's knowledge of now <em>given</em> the whole future.
:::

And now the punchline — not an inequality but an <em>equality</em>, our Theorem 1, valid for any environment whatsoever, even one the system talks back to:

:::ledger Ledger · Theorem 1 | exact, always
debit | Cryptic information, summed over all steps | secrets the future never repeats | DEBIT
debit | A "residual" of leftover terms | this is where the rest of the story hides | DEBIT / CREDIT
total | = Total dissipated work (in units of k<sub>B</sub>T) | | EXACT
:::

When the environment doesn't listen back, the residual is provably ≥ 0, so you get a clean law: <strong>dissipation ≥ total cryptic information.</strong> The heat bill only ever charges you for secrets. Everything we do from here on is, quite literally, an audit of that residual line.

:::aside Why this generalizes 2012
If the signal happens to be memoryless-simple (Markov), "what the future reveals" collapses to "what the next symbol reveals," and this new law reduces exactly to the 2012 nostalgia bound. The new statement is what nostalgia <em>wanted</em> to be for worlds with long, tangled memories.
:::

# [Entry 04 · A family of laws] How far into the future should you peek?

Between "compare against the next tick" (2012) and "compare against the entire future" (cryptic) sits a whole family: judge the system's memory against a sliding <strong>window of the next <span class="mth">k</span> symbols</strong>. Every window width gives a valid heat bound. So which is best? Bigger windows are more forgiving — surely their bounds are tighter?

<strong>No — and we prove it's the opposite.</strong> Summed over a whole trajectory, the bounds only get <em>weaker</em> as the window grows. The humble one-step 2012 bound is the tightest member of the entire family, always, for any world that doesn't listen back. The value of the family isn't a better number. It's the <em>shape</em> of the curve, which turns out to be a diagnostic instrument. Try it:

:::widget window
:::

Read the shapes like a doctor reads an EKG:

<strong>The cliff tells you the world's memory span.</strong> The echo world repeats each symbol three ticks later; its profile plummets exactly at width 3 — the moment the window becomes long enough to catch the repeat, most of the "secret" stops being secret. Flatness onset reads off the world's memory order.

<strong>A rising profile should be impossible.</strong> The monotone theorem says summed profiles can only fall — <em>if the world is autonomous</em>. So if you ever measure a rising one, you've caught the environment red-handed: it is reacting to the system. <strong>A feedback detector made of pure statistics</strong>, no thermometer required. (Hold that thought for Entry 07.)

# [Entry 05 · The missing heat] Where's the other seventy percent?

:::lede
Here's the embarrassment mentioned earlier, now with numbers: across every regime we test, information bounds — old or new — account for only <strong>4–30%</strong> of the heat actually wasted. For a "law of physics," that's a lot of unexplained bill.
:::

Our answer reframes the whole complaint. The missing heat has nothing to do with the signal or the memory. It's a property of <strong>the hardware</strong>: how completely the system relaxes each step. A system that only slumps partway down each new valley leaves stored stress that dissipates later, and no amount of informational cleverness prices it — but <em>one single number</em> does. Each thermal bath gets a coefficient (the <em>Dobrushin coefficient</em> — roughly, "what fraction of the way to equilibrium does one step take you?"), and adding that one hardware constant to the ledger recovers <strong>74–100%</strong> of the bill.

:::widget hybrid
:::

Notice the moral inversion. The standard critique was "information bounds are loose, hence weak." Our version: information terms were never <em>supposed</em> to price the kinetic cost — the missing dissipation belongs to the machine, not the message, and a single kernel constant settles it. At complete relaxation (<span class="mth">r = 1</span>), the hybrid bound isn't a bound at all: it's <em>exact</em>.

# [Entry 06 · A field test] A heat meter for chaos

Does the window profile actually measure anything real? We point the instrument at the hardest kind of world: <strong>deterministic chaos, watched through a blurry lens.</strong> Imagine a chaotic map (the "skew tent map" — stretch the interval, fold it back) that you observe with only finite precision, say the first few binary digits. Then compute the window profile <em>exactly</em>, no sampling.

Three clean signatures fall out:

:::widget chaos
:::

<strong>1 · The profile rises here</strong> — a sigmoid, the mirror image of the echo world's cliff. For short windows, chaos hasn't yet amplified microscopic differences past your lens's resolution, so nothing looks secret. <strong>2 · The knee sits exactly where chaos eats your decimal places:</strong> at window width <span class="mth">k* ≈ ln(1/precision) / λ</span>, where <span class="mth">λ</span> is the Lyapunov exponent — the map's stretching rate. Sharper memory pushes the knee right, by precisely the predicted amount. <strong>3 · The plateau equals the map's information-destruction rate</strong> (its "folding entropy" — for these maps, exactly <span class="mth">λ</span>). Our computed value: 0.5622 nats against a true 0.5623.

:::pull
A calorimeter, plus this bookkeeping, becomes a <i>chaos meter</i>: the heat ledger reads out how fast the world is destroying information.
:::

:::aside A subtle correction to folklore
You might expect that for <em>reversible</em> chaos (like the baker's map, which folds but never truly destroys), long enough windows would drive the profile to zero — the future should eventually reveal everything. We show this fails: future observations resolve the <em>stretching</em> direction of chaos but carry exponentially fading news about the <em>squeezing</em> direction. Watching only forward in time, some of the past stays cryptic forever. Closing the gap would need windows that look both ways — an open problem we leave flagged.
:::

# [Entry 07 · The loophole] Write it into the world

:::lede
Everything so far assumed the world ignores you. But real agents — ants, engineers, language models with scratchpads — <em>act</em>. And the moment the environment starts responding to the system, a remarkable loophole opens in the heat bill.
:::

An ant doesn't remember the route to food. It lays pheromone — it <strong>writes its memory into the world</strong>, and later reads it back off the trail. You do the same with sticky notes, filenames, and the arrangement of objects on your desk. Biologists call it <em>stigmergy</em>. We prove this trick has an exact thermodynamic value.

:::figure "FIG 4" stigmergy
<b>Stigmergy, priced.</b> The discount's exact currency is <b>oracular information</b>: what the agent's state tells about the world's <em>future</em> beyond what the current observation already shows. A purely passive observer has zero of it (its state is just a digest of the past). An agent that stamps its memory into the world has plenty — and each nat of it is worth one nat off the cryptic charge.
:::

With feedback switched on, the residual acquires a per-step penalty, and we prove two crucial things about it: the penalty <strong>never flips sign</strong> (verified against 12,000 adversarially optimized models trying to break it — minimum found: exactly zero), and it is <em>exactly</em> the oracular information minus a harmless defect. Dropping the defect gives our headline inequality, valid at any relaxation speed:

:::ledger Ledger · the master account | Corollary 6
debit | Hidden (cryptic) state information | secrets held internally, summed over time | + DEBIT
credit | Oracular state information | memory the world's future re-exposes for you | − CREDIT
credit | Initial coding cost | what the starting state already encoded | − CREDIT
total | ≤ Dissipated work | | THE LAW
:::

:::pull
An agent pays for memory by dissipating it — <i>or by writing it into the world's future.</i>
:::

And when the credits exceed the debits, the bound goes <em>negative</em>: the system can extract net work, running on the order it previously stamped into its surroundings. Our tables realize this regime explicitly. Watch it happen:

:::widget feedback
:::

:::aside A trap we defuse
A tempting shortcut — swap the exact penalty for a familiar quantity called backward transfer entropy — turns out to produce an <em>invalid</em> "law" whenever relaxation is incomplete. We exhibit explicit counterexamples where the fake bound exceeds the true dissipation, then show the correct oracular version quietly becomes the shortcut in the complete-relaxation limit. The moral: in this subject, plausible substitutions need proofs.
:::

# [Entry 08 · The mirror] One ledger, two readings

There has long been a <em>second</em> tradition of information thermodynamics, descending from Maxwell's demon: information as a <strong>resource</strong>, where a feedback controller uses what it knows to extract work. It has its own second law, written in a quantity called <em>directed information</em>. Two literatures, two laws — prediction costs versus feedback profits.

Our final structural result: <strong>they are the same identity.</strong> Theorem 1's equation contains a free choice — condition the bookkeeping on the signal's <em>future</em>, or on its <em>past</em>. Future-facing gives "prediction pays" (the cryptic law). Past-facing gives "action pays back" — and reduces, exactly, to the classic directed-information second law. The two split a single conserved total of information between system and world.

:::figure "FIG 5" duality plain
<b>Two σ-algebra choices in one decomposition.</b> "Memory as liability" and "information as resource" turn out to be the same accounting, read left-to-right versus right-to-left, splitting one conserved total (the Massey–Kim conservation law — verified in our models to machine precision).
:::

# [Entry 09 · Due diligence] Trust, but enumerate

A habit we insisted on throughout: every identity and inequality is <strong>machine-verified</strong>, not by simulation but by exact enumeration of the entire joint probability of every possible history. Identities check out to fourteen–sixteen decimal places. The sign of the feedback penalty survived a deliberate 12,000-model adversarial search built to break it. The bounds hold even in the strange regimes where net work is being extracted.

We also tuck in a practitioner's warning: if you try to <em>estimate</em> these quantities from finite recorded data, the future-conditioned terms are far hungrier for samples than the one-step ones, and naive estimates can err on the flattering side — an estimated heat floor is not a certificate. Building estimators that are guaranteed one-sided is one we leave open.

# [Entry 10 · Beyond physics] Why you might care

Honestly: not because of your GPU bill. Real chips run astronomically above these fundamental floors. The interesting transfers are structural — strip the temperature off, and the identity is a statement about <em>representation</em>:

### For machine learning

The right "memory penalty" for a recurrent state isn't a generic bottleneck that squeezes useful and useless bits alike — it's the <strong>cryptic</strong> part only: penalize what the state holds that the future context wouldn't reveal anyway. For agents, the regularizer refines further to <em>cryptic minus oracular</em>: writing state into the environment (a scratchpad, a file) is a legitimate 1:1 substitute for internal retention, and the theorem guarantees the credit can never overdraw.

### For systems engineers

The ledger reads like a cache-eviction policy: an entry is safe to evict if it's non-cryptic given what you're keeping plus what's about to arrive — or if you've exported it to a persistent substrate the future computation will read. The physics and the systems folklore agree, now with an exact exchange rate.

### For the small and the hot

Where temperature is literal — molecular machines, analog and stochastic computing — the feedback bound is a design law valid at any speed, and the one-number hardware correction prices the rest of the bill.

:::ledger Closing the books | the account in one line
debit | Crypticity — secrets the world never repeats | | DEBIT
debit | Mismatch cost — hardware relaxing off-target | | DEBIT
credit | Feedback discount — memory exported to the future | | CREDIT
zero | Boundary terms | | ≥ 0
total | = Dissipation. Every entry proven, every sign certified. | | ■
:::

The 2012 slogan was <em>a memory that doesn't predict must burn.</em> The 2026 amendment is gentler and stranger: <strong>only secrets burn — and a secret told to the world stops being a secret.</strong>
