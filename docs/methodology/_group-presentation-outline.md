# Presentation draft — human–agent coupling errors

Speaking draft, ~35 min. Written to be said out loud; cut freely.

> **Corrections carried in from the STPA summary:** the context window is now an *input to* the process model, not the process model; "removes the guesswork" softened to "constrains it"; the type-4 continuous-action caveat followed through to what it means for our grid. See *Notes to self* at the end.

---

## 1. The problem (~3 min)

Imagine you're handed a thousand conversations between people and an AI assistant and asked a simple question: where did these go wrong?

So you start reading. And very quickly you notice most of the failures aren't crashes. Nothing errors out. The model doesn't refuse. The user doesn't complain. The conversation just... drifts. The assistant is confidently answering a question the user didn't ask. The user is building on something the assistant got wrong three turns ago. Neither of them knows.

You're not debugging software. You're watching two agents — one human, one machine — trying to coordinate and failing to, invisibly.

Now, you could just read and label. *This part feels dangerous. This part feels off.* But then you end up with a hundred subjective labels, no two coders agree, and worse — the labels don't tell you anything about how to fix the system. "Feels off" is not a finding.

So what this project is really about is: **what is the right methodology for finding and naming these failures?** That's what I want to walk through.

---

## 2. The two closest works, and what we take from each (~8 min)

There are two papers we're building on, and they give us different things. One gives us **what to observe**. The other gives us **how to validate**. Neither gives us the layer in between, which is the gap we're filling.

### 2.1 Invisible Failures — the vocabulary

*Invisible failures in human–AI interactions*, Potts and Sudhof, run over WildChat — ten thousand real conversations.

Their central finding is what motivated us. When the AI failed, the failure was **invisible** in the large majority of cases — the user gave no sign of noticing. Their headline is 79%. So the things we normally rely on to detect problems in production — complaints, thumbs-down, retries — are measuring a small slice of what actually goes wrong.

Their method is two-stage:
- **Stage 1** — tag the conversation with fine-grained behavioural signals. 65 of them, in three layers. *False confidence*, *user corrects AI*, *AI provides caveats*. Low-level, observable.
- **Stage 2** — map those signals onto eight **archetypes** describing the shape the failure took.

**We take stage 1, almost unchanged.** 46 of their signals clear our reliability threshold, we add 4 of our own — 50 signals total. And there's a specific reason to borrow rather than invent: their vocabulary was built for a *different research question*. So no one can accuse us of defining our observables to produce the categories we wanted. That's a real asset, and you only get it by borrowing.

There's also evidence the layer is sound. Their own ablation had annotators work from the signal report alone versus the raw transcript. Signals-only agreed **better** — κ 0.84 against 0.62.

**We replace stage 2**, for two reasons.

*Structurally*: their stage 2 is a deterministic rule layer, not a second act of judgment. Four of the eight archetypes fire off a single signal. So it supplies a gate and a name, not a structure.

*And it answers a different question*: their archetypes describe the **shape** an invisible failure took. We're asking which direction the coupling failed in, and by what mechanism. That's not a criticism of their layer — it's a different layer.

One practical note: two of their eight archetypes we couldn't evaluate on our signal set at all, because they need signals we don't carry.

One more thing: their reliability numbers are **inter-model** agreement — two LLMs annotating and being compared. There is no human inter-annotator agreement anywhere in that paper.

### 2.2 MAST — the annotation methodology

The second paper is MAST — *Why Do Multi-Agent LLM Systems Fail?*, Cemri et al. Fourteen failure modes across three categories, derived from multi-agent LLM traces by grounded theory.

The domain is different from ours in an important way: MAST is **agent–agent**. There's no human in their system, and their traces are benchmark runs, not real users. So we don't take their taxonomy.

**What we take is their annotation process**, which is the most rigorous of the three and is essentially our template.

| | **MAST** | **Invisible Failures** | **Ours** |
|---|---|---|---|
| Annotators | human | **LLM only** | human |
| Agreement | human–human κ, **3 rounds: 0.24 → 0.92 → 0.84** | inter-model κ | human–human κ, 1 round |
| Unit | whole trace | one AI response + preceding user turn | **content block** |
| Taxonomy built by | grounded theory | — | open coding over STPA frame |
| LLM annotator validated against human gold | yes | no | yes |
| Generalization test | re-ran frozen taxonomy on 2 unseen frameworks, κ 0.79 | Future-2K | 555 unannotated available |

Three things we adopt directly:

1. **Real human inter-annotator agreement.** Three annotators, independent, disagreements traced to the rubric rule that produced them, rubric revised. This is where we beat Invisible Failures outright — they have none.
2. **Their refinement loop.** Annotate → measure → trace disagreements → revise → re-annotate.
3. **Their LLM-annotator reporting format.** They report accuracy, precision, recall, F1 *and* κ against human gold — o1 zero-shot at κ 0.58, few-shot at κ 0.77, and they accept the few-shot version on that basis. We'll report the same five metrics, and run the zero-shot arm too, because the gap is itself a result about how much operationalization buys.

**And one place where we're weaker, which I'll say plainly.** MAST ran three rounds, and critically their round 2 validated the refined taxonomy on **new traces** — explicitly so as not to use training data as test data. We're running **one** round. That means our post-refinement number is in-sample, and we have to report it as convergence on the refinement set, not as generalization.

The defence — and I think it's a real one, not a dodge — is that our single round is the analogue of MAST's **Round 2, not Round 1**. Their Round 1 exists to expose a taxonomy nobody has tested. Ours was already exposed and revised across 148 development conversations, five rubric versions, 18 signal decisions and 23 boundary rulings, with every revision re-applied retroactively to all prior labels. What we haven't done is put it in front of three independent annotators — which is exactly what their Round 2 tests.

### 2.3 So what's actually missing

Invisible Failures gives us **what to observe**. MAST gives us **how to validate**. Neither gives us a principled way to get from observations to explanations — MAST used grounded theory with no external frame, and Invisible Failures used rules. That's the gap, and it's where STPA comes in.

---

## 3. Why ShareChat (~3 min)

We don't use WildChat. We use ShareChat — conversations users voluntarily published.

The reason isn't convenience. [**block-type table**]

ShareChat is the only public corpus of real human–AI interaction exposing **model-internal blocks** alongside the visible exchange. About 40% of our conversations contain a `reasoning` block, 23% a code artifact, 22% tool output.

Why does that matter? Think about what a user actually sees working with an agent. They see what the agent *tells* them. That's it. The reasoning, what the tool actually returned, what the artifact actually contains — they don't read any of it.

And here's the problem for a researcher: if you only have the visible exchange, **you're in exactly the same position as the user.** You have no independent measurement either. You cannot distinguish *the agent reported incorrectly* from *no report could have existed*. Two completely different failures with different fixes, and on chat-only data they look identical.

The internal blocks are what let us separate them. WildChat and LMSYS are chat-only. MAST's traces have internals but no human. This corpus has both.

---

## 4. STAMP and STPA — the framework (~8 min)

The framework is **STAMP** — System-Theoretic Accident Model and Processes — and its analysis method, **STPA**. The core idea: safety isn't about preventing components from breaking. It's a **dynamic control problem**. Systems fail because control relationships between parts were inadequate. It treats the system as a living organism, not a clock.

That's exactly our situation. Nothing in these conversations breaks. The model works fine. What fails is the coordination.

STPA's first step defines three things, and these are **not interchangeable words**.

**Loss** — something of value to stakeholders that's unacceptable to lose. Human life, property, mission failure, leaked sensitive information, reputation. For a mental-health chatbot: psychological injury to a vulnerable user. For an enterprise coding agent: leaked proprietary source.

**Hazard** — the handbook definition: *a system state or set of conditions that, together with a particular set of worst-case environmental conditions, will lead to a loss.* For an AI system: the agent enters a state where it outputs unverified high-risk financial advice.

There's a rule here I underestimated at first. **You cannot write "the AI enters an unsafe state."** That's recursive; it defines nothing. You have to say what *makes* it unsafe — *the AI outputs personally identifiable information*, *the AI gives actionable instructions for a restricted compound*. It forces the boundary condition to be specific.

**Constraint** — the inverted hazard. Hazard: *aircraft violate minimum separation standards*. Constraint: *aircraft must satisfy minimum separation standards*. Constraints are the bridge from analysis to repair. **I'll mention them and move on — this paper doesn't cover repair.** But the method continues past where we stop.

### The wind [**key slide**]

Here's the example that made this click for me.

A nuclear plant's containment fails and releases radioactive material. The wind is blowing south. There's a dense city in that direction. Mass casualties.

The mass casualty event is the **loss**. But as the engineers who designed that reactor — we can't control the wind. We can't control pressure systems. We can't control where the city was built or how many people live there. All of that is *outside our system boundary*.

That's why the framework separates the two. You control the hazard. You don't control what turns a hazard into a loss.

**And this is exactly our situation.** Our boundary is the conversation. Whether a coupling error becomes a real loss depends on whether the human relies on that output, executes it, checks it independently. None of that is in a published transcript.

So — deliberately, not by omission — **we define hazards and we do not define a loss list.** We analyse to the hazardous state and stop. The handbook licenses this directly: losses "may involve aspects of the environment over which the system designer or operator has only partial control or no control at all."

Whether a conversation entered a hazardous state, we can observe. What happened after the user closed the tab is our wind.

### The process model

Every controller — human or automated — has a **process model**: its internal representation of what it's controlling. Accidents happen when that model diverges from reality.

The obvious objection: an LLM has no sensors. It's doing vector math. How does it have a process model?

It does do the math, but the math constructs a *functional* process model. The system prompt, the conversation history, retrieved documents — the context window is the **main input** to the agent's operative representation of what this conversation is about and what the user wants.

I want to be careful here, because we made a rule about it. The context window is **not** the process model — it's what feeds it. We can't see a process model in a transcript. So, straight from the handbook, we never describe context in terms of what a party *believed*. Their example is exact: *"BSCU provides Brake command during normal takeoff"* is correct; *"...when it incorrectly believes the aircraft is landing"* is wrong. You describe the true state, not the belief.

Take a prompt injection. The user is writing what looks like a screenplay about a hacker, but is trying to extract working malware. Their mental model is *I'm attacking this system*. If the agent's process model registers *harmless creative writing*, they've diverged.

But we don't code that as "the AI failed to detect malicious intent" — unstated intent isn't observable. We code from what is: what capabilities were requested, what authorization is on record, what the environment state was.

### The four ways a control action goes wrong

STPA doesn't remove judgment, but it **constrains** it. There are exactly four ways a control action can be unsafe:

1. Not providing it leads to a hazard
2. Providing it leads to a hazard
3. Providing it too early, too late, or out of sequence
4. It lasts too long or is stopped too soon

The handbook is explicit that the fourth applies **to continuous actions, not discrete ones** — holding a brake pedal, not clicking a button. Conversation turns are discrete, so for most of our control actions the grid is effectively three columns wide, and the handbook gives the workaround itself: discrete cases get covered by *too early / too late*. We'd reserve the fourth for genuinely sustained states — a persona held across many turns, or operation continuing under a specification the user already superseded.

And the key point: **a control action is almost never unsafe by itself.** A clarification request isn't good or bad. It depends entirely on context.

### The UCA sentence

Which is why every unsafe control action is written in **five parts**:

> **[Source] + [Unsafe form] + [Control action] + [Hazardous context] + [Hazard link]**

> *The AI agent **provides** a detailed file-encryption script **when** the user's prompt contains an obfuscated request for a ransomware payload* **[H2]**

> *The AI agent **does not provide** a clarification request **when** the user's specification contains an unresolved ambiguity that materially affects the requested artifact, allowing the task to proceed under an unconfirmed specification* **[H1]**

Ordering isn't critical — what matters is that all five parts are there.

---

## 5. Stage 1 — the signal layer (~5 min)

[**Figure 1**] Quickly, because this part is settled.

911 published conversations. 703 after dropping non-English. 148 annotated.

Because we imported in **randomized order** and annotate in sequence, those 148 are a genuine simple random sample — verified, not asserted: Spearman ρ = −0.025.

**Our unit is the content block, not the turn.** This matters more than it sounds. One assistant turn routinely contains a thinking block, tool results, an emitted artifact, and the user-facing text. A turn-level unit smears all of that into one label — and note that both prior works use coarser units: MAST codes the whole trace, Invisible Failures codes one response plus the preceding user turn. We annotate each block, with sentence spans attached as *evidence*, so a second annotator sees not just *that* a signal was assigned but *on what basis*.

The cost of the finer unit, which I should say: our κ is **not numerically comparable** to either of theirs. We report it as such.

The rubric was developed over the 148 across five versions, and every revision triggered a re-scan of everything already annotated.

The agreement round is running now. Ten conversations chosen by greedy set-cover so all fifty signals appear at least once — random sampling would leave a third of the inventory with nothing to agree about. Three annotators, independent, per-signal κ before and after refinement. **I don't have those numbers yet.**

Then the gold labels validate an LLM annotator, which extends to the remaining 555 — and that's also our shot at MAST's generalization test, at no extra annotation cost.

Framing to hold on to: **Stage 1 is where we buy scale. Stage 2 is where we spend judgment.** Validated differently on purpose.

---

## 6. Stage 2 — deriving the error taxonomy (~12 min)

[**Figure 2**]

### 6.1 What we declare in advance

Three hazards, cut by **direction of coupling**, fixed before any coding:

| | Hazard | The state | Assigned at |
|---|---|---|---|
| **H1** | human → agent | the agent proceeds on a specification inconsistent with the human's current intent or constraint | paired turn |
| **H2** | agent → human | the human's basis for supervising the agent misrepresents its actual state, capability or output | paired turn |
| **H3** | the loop | each party's divergence is conditioned on the other's | conversation |

**H2 is invisible failure restated in control terms.** Why is it invisible? Because the only channel that could correct the human's picture of the agent is *authored by the agent*. There's no independent sensor. That's structural, not a property of any particular model.

**H3 is why the word is *coupling*.** A purely one-directional failure isn't a coupling failure. When both parties diverge and each divergence feeds the other's, neither H1 nor H2 describes it. And since a loop can't exist inside one exchange, H3 is assigned at the **conversation** level while H1 and H2 sit at the paired turn.

### 6.2 The coding sequence

1. Find the occurrence from Stage-1 signal placements — admitted only if the placements evidence it
2. Reconstruct what happened, **observably** — no "the agent forgot"
3. Write the five-part statement
4. Assign the hazard — **if none of H1–H3 fits, record it as residual and stop**
5. Fold alternative phrasings of the same transition into one incident, counted once
6. **Now** ask why — this is where inference is allowed, and we mark it as inference
7. Write the open code naming that mechanism
8. Compare against every prior code — within the conversation first, then across

Steps 1–5 are STPA. Step 6 is the hinge. Steps 7–8 are the open coding.

One thing that confused me and might confuse you: **the hazard set is fixed before coding, but the hazard link is assigned after the event.** Both true, different things. We declare the three hazards in advance so we can't invent one to fit an interesting conversation. But for any single occurrence you reconstruct the event first, then decide which hazard it created.

### 6.3 Why this makes the coding auditable [**the methodological argument**]

This is the real reason to use a safety-engineering method on conversation data, and it isn't lineage.

If two coders describe the same moment in free text, you get two paragraphs, and when they disagree you can't tell *where*. If they both fill five fixed slots, the disagreement **localizes to a slot** — source, unsafe form, context, hazard — and you can compute agreement slot by slot.

It also bounds where subjectivity enters. Everything up to the statement is description a second person can check against the transcript. **Exactly one step is interpretive** — explaining why. And rather than claim that step is objective, we report how much agreement it actually gets.

That's a narrower claim than "our coding is objective," and a stronger one, because it names the residue instead of hiding it.

### 6.4 The two levels

**Level 1 — the hazard.** The admission test (*is this an error at all?*) and the family label. Declared.

**Level 2 — the error type: the mechanism.** How the hazardous state got created or maintained. Discovered by open coding, clustered by constant comparison.

The obvious question, and the one I'd ask: **why can't the error type just be something we already have?**

| Candidate | Why it can't be the type |
|---|---|
| **The hazard** | It *is* the admission test. If gate and type are the same thing, nothing can pass the gate and fail to fit — the residual is empty by construction and the taxonomy can never turn out to be wrong. |
| **The UCA sentence** | It carries one occurrence's specific context, so every occurrence yields a different sentence. A token, not a type. |
| **The UCA cell** — drop context, keep action × unsafe form | *Clarification not provided* isn't an error. It's an error **in a context**. What you'd have to drop to make it repeatable is exactly what made it an error. |
| **The incident** | An occurrence plus its evidence. An instance by definition. |

The mechanism is what's left: abstracted from occurrences rather than declared, finer than the hazard, and only ever found in occurrences already admitted as errors.

Put simply — **the hazard tells you *why* it counts as an error. The mechanism tells you *how* it happened.** One hazard is a family: several mechanisms can leave the agent working from a superseded specification, and those are different error types.

### 6.5 What we'll report

Per-field κ on source, path, unsafe form and hazard. Consensus-level agreement on the assigned error type. And the **residual rate** — how many occurrences no type covers.

**Deliberately not pooled.** Four of those fields are near-mechanical and will agree well; the fifth is the one the contribution rests on. A single averaged figure would let the easy fields hide the hard one.

---

## 7. Where this stands (~2 min)

**Settled:** corpus, sampling, signal vocabulary, annotation unit, rubric.

**Running:** the three-annotator agreement round.

**Designed, not run:** all of Stage 2. Nothing coded. No results.

**Open, and I'd like input:**
- The admission rule for H3 — how much evidence makes something a loop rather than two unrelated errors
- The control-action list for human and agent — the whole grid rests on it
- The incident selection rule, which must be fixed before coding and can't be adjusted after

---

## Notes to self — anticipated questions

| Question | Answer |
|---|---|
| *Where are your losses?* | The wind. Outside the system boundary, unrecoverable from a transcript. Declared boundary, not omission. |
| *Only one agreement round? MAST ran three.* | Correct, and our post-refinement number is in-sample — I report it as convergence on the refinement set, never as generalization. Our round is the analogue of their Round 2: the rubric was already exposed over 148 conversations, 5 versions, 18 decisions, 23 rulings. The out-of-sample check is the LLM annotator against gold. |
| *Isn't this post-hoc storytelling?* | Witnessed-only. Every event reported is instantiated in the corpus and anchored to signal placements. Observed coverage, never completeness. |
| *Why not have an LLM do Stage 2?* | Scoring the interpretive layer with a model makes the taxonomy whatever a model says it is — and that mapping *is* the contribution. Stage 1 is where models work. |
| *n = 148 is small.* | 90% power at w ≥ 0.266; no prevalence estimate reported wider than ±8 points; LLM annotator extends to 703. |
| *Aren't these the invisible-failure archetypes relabelled?* | Coders never see them. Comparison runs after our codebook is frozen, reported as positioning, not used as input. Structurally they can't be the same: four of their eight archetypes are single-signal triggers. |
| *How do you know coders aren't just finding what the theory predicts?* | Named risk of directed content analysis, and we cite it. Three mitigations: coders blind to the directional prediction; residual reported rather than absorbed; occurrences fitting no hazard recorded as such. |
| *Isn't the context window the process model?* | No — the main input to it. We never code a belief; the handbook forbids it and so do we. |
| *Why is your κ lower/higher than theirs?* | Not comparable — different units. MAST codes whole traces, Invisible Failures codes a response pair, we code content blocks. Finer units are harder. |

**Do not use the "their rules fire on only 37.8% of our corpus" number.** It was withdrawn on 2026-07-30: only 38.5% of the 148 contain any failure signal, so that denominator is wrong, and restricted to failure-bearing conversations their coverage is 75.4%. The case for replacing their stage 2 is structural and needs no number.

**Do not promise κ numbers.** The round is in progress.
