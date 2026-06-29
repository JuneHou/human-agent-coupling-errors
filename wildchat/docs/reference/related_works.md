# Related Work

> Draft for the ICLR submission. Companion to [`motivation.md`](motivation.md). Detailed corpus
> numbers live in [`dataset-stats.md`](dataset-stats.md), [`wildchat-vs-sharechat.md`](wildchat-vs-sharechat.md),
> and [`tau-bench-relation.md`](tau-bench-relation.md).
>
> **Citation caveat:** author/year/venue tags below are provisional anchors to known lines of work
> and **must be verified** before submission. Still cited by name only and needing exact references:
> UserBench, PrefIx, R-Judge, RiOSWorld, ERR@HRI 2.0, Gulf of Envisioning. Given the paper's own
> subject — miscalibrated confidence — we flag this explicitly rather than assert false precision.
>
> **Verified (2026-06-06; full references in [`../methodology/derivation.md`](../methodology/derivation.md) § Decision 3b):**
> MAST — Cemri et al. (2025), arXiv:2503.13657; Mylius (2025), arXiv:2506.01782; Doshi et al. (2026),
> ICSE-NIER, arXiv:2601.08012.

We position CouplingBench against five lines of work. The central distinction is that prior work
studies user intent elicitation, AI behavior legibility, general chatbot failures, tool-agent-user
task completion, or agent safety, but does not make human-factor-in-the-loop coupling errors the
primary object of annotation and detection.

## 1. Human-to-AI intent capture

### Instruction following

A first line of work studies whether AI systems correctly follow user instructions and constraints.
Instruction-following research evaluates whether models respond in ways that accurately reflect user
requests and intended behavior. Foundational work such as InstructGPT (Ouyang et al., 2022) and
instruction-following benchmarks such as IFEval (Zhou et al., 2023) focus on improving and measuring
whether models adhere to user instructions across a wide range of tasks.

These works motivate part of the Human-to-AI side of CouplingBench by emphasizing whether an AI
system correctly interprets and executes user-provided instructions. However, they primarily study
instruction adherence rather than broader interaction dynamics, and they do not focus on whether
humans can understand the agent's subsequent behavior or on discovering interaction-induced errors
from real-world traces.

### Preference learning

A related line of work studies whether AI systems can infer, represent, and adapt to human
preferences and objectives. Preference-learning and alignment research seeks to ensure that model
behavior reflects human values, goals, and desired outcomes. Foundational approaches such as RLHF
and the broader preference-learning literature focus on learning from human feedback to better align
model behavior with user intent.

More recent work extends this perspective to interactive settings. UserBench evaluates whether
agents can clarify vague or evolving user goals and uncover hidden preferences during task-oriented
interactions. PrefIx studies whether agents infer and adapt to user preferences over the course of
an interaction, including cases where agents technically complete a task but frustrate users through
excessive confirmation, opaque reasoning, or poor pacing. The Gulf of Envisioning provides a
complementary cognitive account of why users struggle to translate intended outcomes into effective
LLM prompts and to evaluate whether the resulting output satisfies their goals. Together, these
works highlight both the challenge of communicating intent to AI systems and the challenge of
ensuring that AI systems correctly interpret and act on that intent.

These works motivate the Human-to-AI side of CouplingBench. However, they primarily study whether
the agent captures the user's intent, goals, preferences, or constraints. They do not focus on
whether the human can understand the agent's subsequent behavior, nor do they treat
interaction-induced errors as a taxonomy to be discovered from real traces.

## 2. AI-to-Human legibility and attribution

### Uncertainty, calibration, and faithfulness

A second line of work studies whether humans can correctly interpret what AI systems know, how
reliable their outputs are, and whether their explanations faithfully reflect underlying reasoning.
Research on calibration and the idea that "models know what they know" examines whether model
confidence aligns with actual correctness and whether confidence signals can be used to estimate
reliability (Kadavath et al., 2022). Related work studies verbalized or expressed uncertainty,
investigating whether models can communicate uncertainty in ways that help users make appropriate
decisions (Lin et al., 2022).

A further line of work examines faithfulness: whether explanations, chain-of-thought rationales,
summaries, or retrieved-grounded responses accurately reflect the model's actual reasoning process
and supporting evidence. Recent studies have shown that chain-of-thought explanations may be
unfaithful, providing plausible rationales that do not correspond to the computation that produced
the answer (Turpin et al., 2023; Lanham et al., 2023). More broadly, faithfulness research
investigates whether model-generated explanations genuinely support user understanding or instead
create misleading impressions of competence, evidence, or reasoning.

These works are highly relevant to the AI-to-Human side of CouplingBench because users often rely on
confidence signals, uncertainty expressions, citations, explanations, and reasoning traces to
interpret system behavior. Miscalibration, poor uncertainty communication, or unfaithful reasoning
can distort user understanding and contribute to misplaced trust or inappropriate reliance. However,
this literature primarily evaluates the correctness, reliability, or transparency of model outputs
themselves. CouplingBench instead focuses on the broader interaction dynamics between human intent,
AI interpretation, user understanding, and repair, treating uncertainty and faithfulness failures as
potential contributors to coupling errors rather than as the primary evaluation target.

### Hallucinations

Another closely related direction focuses on hallucinations, factual inaccuracies, and unsupported
generations in LLMs. Prior work studies hallucinations in open-domain generation, retrieval-augmented
systems, question answering, summarization, and tool-using agents, as well as methods for detecting
and mitigating unsupported claims. This literature generally treats hallucination as a model-output
problem, evaluating whether generated content is factually correct, grounded in evidence, or
supported by retrieved information.

Hallucinations are relevant to CouplingBench because unsupported claims can shape user beliefs,
influence downstream decisions, and trigger interaction failures. Users may accept incorrect
information, misunderstand the reliability of generated content, or fail to recognize when an agent
has exceeded the available evidence. Nevertheless, the primary goal of hallucination benchmarks is to
measure factuality and grounding. CouplingBench instead studies how hallucinations interact with
human understanding, trust, clarification, and repair within the broader human-AI interaction loop,
treating hallucinations as one possible source of coupling errors rather than the central evaluation
target.

## 3. Human-AI interaction failure taxonomies

The closest conceptual prior is Invisible Failures in Human-AI Interactions (Potts & Sudhof, 2026 —
our **direct predecessor**). It studies naturalistic human-AI conversations from WildChat and shows
that many failures are invisible to users. Its archetypes, including silent mismatch, confidence
trap, drift, partial recovery, and death spiral, demonstrate that failures often arise from
interactional dynamics rather than from model capability alone. Methodologically, this work is
important because it uses natural conversations, visible versus invisible failure labels, domain
analysis, and archetype consolidation.

CouplingBench builds on this direction but changes the target. Invisible Failures studies general
chatbot interactions. CouplingBench focuses on human-factor-in-the-loop coupling errors, first in
affordance-rich chatbot interactions and then in agent-style traces with tool-use or artifact-level
structure. We therefore do not predefine the final error types. Instead, we follow the spirit of
Invisible Failures by beginning with signal-level annotation and open coding, then consolidating
recurring failure mechanisms into a taxonomy.

ERR@HRI 2.0 is another nearby line of work. It studies LLM-powered human-robot conversation
failures, including misunderstanding user intent, premature interruption, and failures to respond. It
also annotates perceived user intention to correct a mismatch between robot behavior and user
expectation. This shows that interaction failure detection is a recognized problem in HRI, but the
setting differs from LLM-based tool-using agents and public chatbot traces.

The most recent and **closest prior work** is the common-ground benchmark of arXiv:2602.21337
(citation provisional). It does almost exactly our *theoretical* move: it grounds a **benchmark**
in Clark and Brennan's **common-ground** theory, pairs **real human** participants with an LLM,
and measures grounding behaviors (presentation, clarification, repair, acceptance) and situation
awareness in a referential communication task — and it finds the model fails to build on
clarifications or maintain task state. This is the clearest evidence that a theory-grounded,
real-human grounding benchmark is viable. It is also where we differ most sharply: the task is a
referential *communication* game with **no tool use, no actions on external state, and no
consequences**, and it is **confirmatory** (testing whether human–LLM grounding matches
human–human patterns) rather than **inducing a taxonomy** of failures. CouplingBench differs on
exactly those axes — consequential action on shared state, and an abductively discovered failure
taxonomy with cause attribution — and we reuse its grounding-act coding scheme and its
shared-view/non-shared-view (observability) manipulation as starting material.

One framing point motivates our use of HCI theory and guards against an easy misreading: the prior
*applications* to human–AI failure (Invisible Failures, ERR@HRI, the common-ground benchmark) are
**communication-bound** — in substrate, and even in their *definition* of failure (a failure is
"visible" only if the user reacts in text). The underlying **theories are not**: Norman's gulfs of
execution and evaluation, situation awareness, and grounding-in-joint-action are rooted in
human–automation interaction, where action, state, and consequence are central. The open problem
is therefore **empirical** — applying these action-capable theories to LLM-agent action coupling
on real-human traces — not an absence of theory. Concretely, our taxonomy backbone is: Norman's
two gulfs name the **H→AI** and **AI→H** channels; common ground (extended to joint action) defines
the **interaction** category; the grounding acts (present / clarify / accept / repair / maintain)
provide the within-interaction structure, instantiated on **both** the meaning medium (existing
chat signals) and the **action/state** medium (the agentic cells existing data cannot express).

## 4. Agent, tool-use, and multi-agent benchmarks

A fourth line of work evaluates LLM agents in tool-use or multi-agent environments. τ-bench (Yao et
al., 2024) evaluates dynamic tool-agent-user conversations under domain policies, using simulated
users and final database-state evaluation. τ²-bench (Barres et al., 2025) extends this line to a
dual-control setting where both the agent and a simulated user can use tools to modify a shared
environment. This makes τ²-bench especially relevant to the shared-control part of CouplingBench.
However, both τ-bench and τ²-bench primarily evaluate whether agents complete tasks, follow rules,
coordinate with users, or guide user actions. They do not induce a taxonomy of
human-factor-introduced interaction errors.

MAST is the closest methodological prior for trace-level taxonomy construction. It studies why
multi-agent LLM systems fail, uses expert annotators, iteratively consolidates failure modes, and
then scales evaluation with LLM-assisted annotation. CouplingBench adopts a similar methodological
pattern for agentified traces, but changes the target from agent-system failures to human-AI coupling
failures. In our setting, the goal is not to predefine all tool-trace error types. Instead, we first
collect or construct traces, manually annotate a seed set, consolidate recurring interaction
failures, and then use the stabilized codebook for scalable annotation.

## 5. Safety, risk, and domain-specific agent evaluation

Agent safety and domain-specific benchmarks motivate why coupling-error monitoring matters, but they
do not directly solve the same problem. R-Judge evaluates whether LLMs can identify safety risks from
multi-turn agent interaction records. RiOSWorld studies risks in multimodal computer-use agents,
including user-originated and environment-originated risks. These benchmarks are relevant because they
treat agent behavior as something that must be monitored during interaction, but their label spaces
center safety risk rather than human-AI coupling errors.

Other benchmarks such as WebArena and OSWorld evaluate autonomous agents in realistic web or computer
environments. PaperArena and MLR-Bench evaluate scientific or machine-learning research agents, and
healthcare-oriented oversight work studies safety mechanisms for medical agents. These works motivate
the need for reliable agents in realistic domains, but they do not study the interaction loop between
human intent, AI interpretation, user understanding, and repair as the primary source of error.

### Control-theoretic safety analysis (STPA) for AI

A distinct safety line applies system-theoretic process analysis (STPA) directly to AI, and is the
closest prior to our *theoretical* backbone, since we likewise treat the agent under feedback as a
controller. Mylius (2025) performs STPA on a frontier-AI control scenario; Doshi et al. (2026, ICSE-NIER)
use STPA to derive information-flow safety specifications for LLM tool use; related work applies it to
ML-powered systems. They differ from us in **kind**: each applies STPA as a **per-system hazard-analysis
process** that yields system-specific unsafe-control-action and loss lists for one deployment, defines
failure as stakeholder-unacceptable losses, and is produced manually without a labelled corpus. None
yields a reusable, bidirectional, oracle-grounded taxonomy of human–agent *coupling* operations — so we
**derive** our operations from STPA's primitives (control loop + UCA guidewords) rather than adopting an
existing AI STPA taxonomy. They motivate our control framing but operate at the wrong granularity (system
hazards, not interaction operations). Full comparison and reasoning:
[`../methodology/derivation.md`](../methodology/derivation.md) § Decision 3b.

## 6. Public interaction datasets

CouplingBench also builds on public human-AI interaction datasets. WildChat provides large-scale
naturalistic ChatGPT conversations and serves as the source for Invisible Failures. ShareChat is
especially relevant because it preserves cross-platform affordances from ChatGPT, Claude, Gemini,
Grok, and Perplexity, including source links, reasoning traces, and code artifacts. ShareChat is not
an error benchmark. Its analyses focus on platform-mediated usage patterns, conversation completeness,
source grounding, and temporal dynamics. For CouplingBench, this makes ShareChat a useful substrate
for discovering how platform affordances shape coupling errors, such as misplaced trust in citations,
misunderstanding of code artifacts, or overinterpretation of visible reasoning.

We empirically characterized these corpora to test whether any off-the-shelf data supports a
coupling-failure benchmark. WildChat (**837,989 conversations**; mean 2.34 turns; 2023–2024 GPT-3.5/4)
carries the predecessor's annotations, and we **reproduced its ~79%-invisible headline** (78.9% of
62,557 failures), validating the schema and join. ShareChat (**129,584 conversations / ~1.2M
messages**) uniquely carries `thinking` traces, but **effectively Claude-only** (911 conversations) —
a small, qualitative AI→H disclosure probe, not a prevalence substrate. Neither corpus has tool
actions, shared state, or consequences. The adequacy gap is summarized below; full numbers are in the
companion docs.

| Corpus | H→AI | AI→H | Coupling (interaction) | Action / consequence | Real human |
|---|:--:|:--:|:--:|:--:|:--:|
| WildChat | ✓ | ◐ | ◐ | ✗ | ✓ |
| ShareChat | ◐ | ✓ (thinking, Claude-only) | ◐ | ✗ | ✓ |
| τ-/τ²-bench | ◐ | ◐ | ✓ (τ² dual-control) | ✓ | ✗ (simulated) |

No single corpus has **action/consequence *and* a real human *and* both channels** — the empirical
justification for collecting a new benchmark, most economically by taking a τ²-bench-style
dual-control environment and **swapping the simulated user for a real human**.

## 7. Summary of the gap

Existing work covers important pieces of the human-AI loop. UserBench, PrefIx, and the Gulf of
Envisioning emphasize the Human-to-AI channel. Calibration, uncertainty, faithfulness, and
hallucination work emphasize the AI-to-Human channel. Invisible Failures and ERR@HRI 2.0 study
interactional failures in chatbot and human-robot conversations. τ-bench, τ²-bench, MAST, R-Judge,
and RiOSWorld study tool-use, multi-agent failure, or safety-risk monitoring. CouplingBench targets
the seam between these directions. It studies failures that become visible only when we jointly
analyze user intent, AI interpretation, AI output or action, human understanding, and repair. The
result is a benchmark for detecting and analyzing human-factor-in-the-loop coupling errors rather
than standalone user errors or standalone agent errors.

## 8. Differentiation (the one table reviewers will read)

| Line of work | Both channels | Coupling (interaction) | Repair | Agentic (action+consequence) | Real human | Reusable benchmark + repair model |
|---|:--:|:--:|:--:|:--:|:--:|:--:|
| Instruction following / preference (H→AI) | ✗ | ✗ | ✗ | ◐ | ✗ | ✓ |
| Calibration / faithfulness / hallucination (AI→H) | ✗ | ✗ | ✗ | ✗ | ✗ | ✓ |
| Interaction taxonomies (Invisible Failures, ERR@HRI) | ✓ | ✓ | ◐ | ✗ | ✓ | ◐ (chat, tagger) |
| Common-ground benchmark (2602.21337) | ✓ | ✓ | ◐ | ✗ | ✓ | ✓ (grounding metrics) |
| Agent benchmarks (τ/τ²/WebArena/MAST) | ◐ | ✗ (τ² ◐) | ✗ | ✓ | ✗ (simulated) | ✓ (task / agent-failure) |
| Safety / risk (R-Judge, RiOSWorld) | ◐ | ✗ | ✗ | ✓ | ◐ | ✓ (safety label) |
| **Ours (CouplingBench)** | **✓** | **✓** | **✓** | **✓** | **✓** | **✓** |

The common-ground benchmark (2602.21337) is the closest — checked on every column **except agentic
action+consequence**, and confirmatory rather than taxonomy-inducing. Ours is the only row checked
across **coupling × repair × agentic × real-human × reusable artifact**, with an **abductively
discovered** failure taxonomy — the precise, defensible gap.
