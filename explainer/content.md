---
title: The Warmth in Remembering, an explainer
kicker: An explainer to <a href="https://github.com/dimenwarper/trajectory_thermo_of_pred">trajectory and agent-level thermodynamics of prediction</a>
hero_title: The Warmth in<br>Remembering
hero_sub: Everything that reacts to the world keeps some record of it as transient scars in its thermodynamic profile. The price for such information is paid in heat. This is a walkthrough of a <a href="https://github.com/dimenwarper/trajectory_thermo_of_pred">set of results</a> expanding on <a href="https://arxiv.org/abs/1203.3271">Still and Crook's Thermodynamics of Prediction</a>, where we work out which memories cost, which are free, and the loophole that lets you bill the world instead.
hero_src: <b>Companion to:</b> <a href="https://github.com/dimenwarper/trajectory_thermo_of_pred">"A Trajectory-Level and Agent Back-Action Identities for the Thermodynamics of Prediction"</a>
footer: This explainer compresses the technical paper. All interactive figures use data from our numeric results (Tables 1, 2, 6 and the §6 chaotic-map computations); curves between tabulated points are interpo/listenlated and marked as such. Nats, not bits, throughout, one nat ≈ 1.44 bits.
footer_fin: Fig. ledger closed · dissipation ≥ crypticity − oracularity · 2026
---

# [Entry 01 · The setup] Systems learn naturally through thermodynamics

:::lede
A thermostat tracks the temperature. A bacterium tracks the sugar gradient it swims through. Your neurons track the sentence you're reading. They all take advantage of one simple thing: becoming a record of your surroundings kind of happens automatically (even if inefficienlty at first!), because anything a changing world pushes onto an internal system ends up statistically correlated with the how the pushing happens. Correlations propagate and change the systems they interact with.
:::

But those correlations have an energy bill. To see where the bill comes from, we use the simplest possible cartoon of "a thing driven by a world,". At each tick of time, two things happen:

:::figure "FIG 1" two-stroke
<b>The two-stroke heartbeat.</b> Each time step: (1) the environment signal jumps, which instantly reshapes the system's energy landscape. That shove does <span style="color:var(--heat);font-weight:600">work</span> on the system; (2) the system relaxes one step toward the new valley, dumping <span style="color:var(--heat);font-weight:600">heat</span> into its surroundings. The environment can be anything: rhythmic, random, long-memoried. Later, even something that listens back.
:::

Some of the work pushed in is legitimately stored (the system ends up higher on the ladder of useful free energy). The rest is <span class="term hot">dissipated work</span>: energy that came in as an orderly shove and left as disorderly heat. The gist is then:

:::pull
How little heat can a system that lives in a changing world <i>possibly</i> waste and what does the answer have to do with what it remembers?
:::

# [Entry 02 · The 2012 rule] Useless memory costs heat

In a landmark [paper](https://arxiv.org/abs/1203.3271) by Still, Sivak, Bell and Crooks proved that if a system is physically pushed around by an external signal, its internal state <span class="mth">S</span> inevitably carries information about the signal. They split that information in two:

:::raw
<p style="margin-bottom:.6em"><strong style="color:var(--free)">The predictive part</strong>: bits about the current signal that are still useful for anticipating the <em>next</em> one.</p>
<p><strong style="color:var(--heat)">The nostalgic part</strong>: bits about the current signal that will be useless one tick from now. Memory for memory's sake.</p>
:::

:::figure "FIG 2" nostalgia
<b>Nostalgia = memory − predictive power.</b> The Still bound: dissipated work per step is at least <span class="mth">k<tspan style="font-size:.8em">B</tspan>T</span> × nostalgia. Clinging to the past, if the past won't help you with the future, is physically expensive. A perfect predictor, i.e. remembering only what forecasts, can in principle run cool.
:::

That result launched a small field. But it also left two itches that we set out to scratch. <strong>First:</strong> "useful for the next tick of the clock" is a strangely short horizon. What about signals whose patterns only make sense over long stretches? Second, when you actually compute the bound, it typically explains only a small sliver of the heat a real system wastes. Where's the rest?

# [Entry 03 · The exact identity] The cost of information what never repeats

:::lede
Not all correlations in the world are predictive of its future. The system pays a cost for the memories it keeps that are never repeated.
:::

Consider what the system's state knows about the present signal. Some of that information will be repeated, and the future of the signal will reveal it whether or not the system bothered to remember. And some of it is <em>gone</em>: the signal's entire future, watched to the end of time, would never disclose it again. We call that second kind <span class="term hot">cryptic information</span> what the state stores about the present that the future never brings up abain.

:::figure "FIG 3" cryptic
<b>The green part is thermodynamically free</b> — whether or not the system ever "uses" it — because the world's own future is a backup copy. Only the <b>red, cryptic part</b> shows up as heat. In symbols: cryptic information is <span class="mth">I[S<tspan style="font-size:.75em">t</tspan> ; x<tspan style="font-size:.75em">t</tspan> | future]</span>, the state's knowledge of now <em>given</em> the whole future.
:::

This results in a simple equality:

:::ledger Ledger · Theorem 1 | exact, always
debit | Cryptic information, summed over all steps | secrets the future never repeats | DEBIT
debit | A "residual" of leftover terms | this is where the rest of the story hides | DEBIT / CREDIT
total | = Total dissipated work (in units of k<sub>B</sub>T) | | EXACT
:::

When the system does not affect the future of the external signal (that is, non-agentic), the residual is provably ≥ 0, so you get a clean law: <strong>dissipation ≥ total cryptic information.</strong> The heat results only for that which never repeats. This residual behaves differently depending on the assumptions of the system.

:::aside Why this generalizes the Still inequality
If the signal happens to be Markovian, "what the future reveals" collapses to "what the next symbol reveals," and this new law reduces exactly to the Still nostalgia bound. The new statement is what nostalgia <em>wanted</em> to be for worlds with tangled memories.
:::

# [Entry 04 · A family of relationships] How far into the future should you peek?

Between "compare against the next temporal step" (Still bound) and "compare against the entire future" (the cryptic bound above) sits a whole family: judge the system's memory against a sliding <strong>window of the next <span class="mth">k</span> symbols</strong>. Every window width gives a valid heat bound. So which is best? Bigger windows are more forgiving, so maybe their bounds are tighter?

<strong>Actually the opposite.</strong> Summed over a whole trajectory, the bounds only get <em>weaker</em> as the window grows. The humble one-step Still bound is the tightest member of the entire family, always, for any system that's not agentic. It's the <em>shape</em> of the curve, which turns out to be a diagnostic instrument. Try it:

:::widget window
:::

Read the shapes as follows:

<strong>The cliff tells you the world's memory span.</strong> The echo world repeats each symbol three ticks later; its profile plummets exactly at width 3 — the moment the window becomes long enough to catch the repeat, most of the "secret" stops being secret. Flatness onset reads off the world's memory order.

<strong>A rising profile should be impossible.</strong> The monotone theorem says summed profiles can only fall — <em>if the system never acts on the world</em>. So if you ever measure a rising one, you've caught the environment red-handed: it is reacting to the system (and your system needs to be agentic). It is a feedback detector of sorts, via statistics. (Hold that thought for Entry 06.)

# [Entry 05 · The missing heat] Where's the other seventy percent?

:::lede
Across every regime we test, the information bounds — the Still bound or our cryptic bound — account for only <strong>4–30%</strong> of the heat actually wasted.
:::

The missing heat due to bound laxness has nothing to do with the signal or the memory. It's, however, a property of system itself: how completely it relaxes each step. A system that only slumps partway down each new valley leaves stored stress that dissipates later, and no amount of informational cleverness prices it. Is there a quantity that can describe this internal dynamic? Yes! Each thermal bath gets a coefficient (the <em>[Dobrushin coefficient](https://www.researchgate.net/publication/265436392_A_generalization_of_Dobrushin_coefficient)</em> — roughly, "what fraction of the way to equilibrium does one step take you?"), and adding that one system constant to the ledger recovers <strong>74–100%</strong> of the bill.

:::widget hybrid
:::

This prices in kinetic cost, which does not appear in the Stills and other such bounds. The missing dissipation belongs to the behavior of the system itself. At complete relaxation (<span class="mth">r = 1</span>), the hybrid bound isn't a bound at all: it's exact!.

# [Entry 06 · The loophole] What if the system is agentic?

:::lede
Everything so far assumed the world ignores the system. But real agents — ants, engineers, language models with scratchpads — <em>act</em>. And the moment the environment starts responding to the system, an interesting loophole appears inside the dissipation.
:::

An ant doesn't remember the route to food. It lays pheromones - it <strong>writes its memory into the world</strong> - and later reads it back off the trail. You do the same with sticky notes, filenames, and the arrangement of objects on your desk. In biology this is called <em>stigmergy</em>. We prove this trick has an exact thermodynamic value.

:::figure "FIG 4" stigmergy
<b>Stigmergy, priced.</b> The discount's exact currency is <b>oracular information</b>: what the agent's state tells about the world's <em>future</em> beyond what the current observation already shows. A purely passive observer has zero of it (its state is just a digest of the past). An agent that stamps its memory into the world has plenty. Each nat of it is worth one nat off the cryptic charge.
:::

With feedback switched on, the residual acquires a per-step penalty, and we prove two things about it: the penalty <strong>never flips sign</strong> (verified against 12,000 adversarially optimized models trying to break it — minimum found: exactly zero), and it is <em>exactly</em> the oracular information minus a harmless defect. Dropping the defect gives our headline inequality, valid at any relaxation speed:

:::ledger Ledger · the master account | Corollary 6
debit | Hidden (cryptic) state information | secrets held internally, summed over time | + DEBIT
credit | Oracular state information | memory the world's future re-exposes for you | − CREDIT
credit | Initial coding cost | what the starting state already encoded | − CREDIT
total | ≤ Dissipated work | | THE LAW
:::

:::pull
An agent pays for memory either by dissipating it <i>or by writing it into the world's future.</i>
:::

When the credits exceed the debits in the heat bill, the bound goes <em>negative</em>!: the system can extract net work, running on the order it previously stamped into its surroundings. Our tables realize this regime explicitly. Watch it happen:

:::widget feedback
:::

:::aside A trap we defuse
A tempting shortcut, swap the exact penalty for a familiar quantity called backward transfer entropy, turns out to produce an <em>invalid</em> "law" whenever relaxation is incomplete. We exhibit explicit counterexamples where the fake bound exceeds the true dissipation, then show the correct oracular version quietly becomes the shortcut in the complete-relaxation limit.
:::

# [Entry 07 · Relationship to directed information] A connection with communication theory

Consider Maxwell's demon: here information is a <strong>resource</strong>, where a feedback controller uses what it knows to extract work. It has its own second law, written in a quantity sometimes called <em>[directed information](https://pmc.ncbi.nlm.nih.gov/articles/PMC5104982/)</em>.

We show that directed information and our oracle information are sort of the same thing. Theorem 1's equation contains a free choice: condition the bookkeeping on the signal's <em>future</em>, or on its <em>past</em>. Future-facing gives "prediction pays" (the cryptic part of the identity). Past-facing gives "action pays back", and turns out it reduces, exactly, to the classic directed-information. The two split a single conserved total of information between system and world.

:::figure "FIG 5" duality plain
<b>Two vantage points, one relationship.</b> "Memory as liability" and "information as resource" turn out to be the same accounting, read left-to-right versus right-to-left, splitting one conserved total (the Massey–Kim conservation law, verified in our models to machine precision).
:::

# [Entry 08 · So what] Why you might care

Unfortunately this does not affect your GPU bill (real chips run astronomically above these fundamental floors!). But the results perhaps do yield some intuitinos:

### ML systems can design for cryptic or oracle information

The right "memory penalty" for a neural architecture having a recurrent state isn't a generic bottleneck that squeezes useful and useless bits alike, but rather the <strong>cryptic</strong> part only. That is, you should directly and surgically penalize what the state holds that the future would never repeat. For agents, the regularizer refines further to <em>cryptic minus oracular</em>: writing state into the environment (a scratchpad, a file) is a legitimate 1:1 substitute for internal retention.

### For the small and the hot

In molecular machines, e.g. analog and stochastic computing, the feedback bound is a design law valid at any speed, and the one-number hardware correction prices the rest of the bill.

:::ledger Closing the books | the account in one line
debit | Crypticity — informtion the world never repeats | | DEBIT
debit | Mismatch cost — hardware relaxing off-target | | DEBIT
credit | Feedback discount — memory exported to the future | | CREDIT
zero | Boundary terms | | ≥ 0
total | = Dissipation.| | ■
:::

The original Still bound stated that <em>a memory that doesn't predict must burn.</em> The amendment here is: <strong>only the unpredictable burns, but you can cool it off by acting on the world</strong>
