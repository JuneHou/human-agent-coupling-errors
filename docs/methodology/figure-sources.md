# Figure sources

Mermaid source for the two Method-section figures. Captions live with the figures in `paper/methods.md` (§3.2, §3.3). Rendered: the published artifact. Convert to TikZ for submission.

## Figure 1 — Stage 1

```mermaid
flowchart LR
    A["703 conversations"]
    B["148 sampled"]
    C["555 held out"]
    D["Human annotation<br/>and rubric development"]
    E["Agreement round<br/>3 annotators"]
    F["Frozen rubric<br/>148 gold labels"]
    G["LLM annotator<br/>validated on gold"]
    H["Signal layer<br/>703 conversations"]

    A -- random --> B
    A --> C
    B --> D --> E --> F --> G --> H
    C --> G
    E -. refine .-> D
```

## Figure 2 — Stage 2

```mermaid
flowchart TD
    A["Signal layer"]
    L["<b>Hazards — declared in advance</b><br/>H1 human to agent<br/>H2 agent to human<br/>H3 the loop"]
    HZ["<b>Hazard — a state of the joint work</b><br/><b>H1</b> the agent proceeds on a specification inconsistent<br/>with the human's current intent or constraint (paired turn)<br/><b>H2</b> the human's basis for supervising the agent<br/>misrepresents its actual state or output (paired turn)<br/><b>H3</b> each party's divergence is conditioned on the<br/>other's (conversation)"]
    B["Control actions<br/>human and agent"]
    C["Coupling events<br/>control · feedback · execution"]
    U["<b>Unsafe control action — five parts</b><br/>source · unsafe type · control action<br/>· context · <b>hazard</b><br/><i>the hazard is assigned per occurrence;</i><br/><i>the context is the true state, never a belief</i>"]
    D["Why the event occurred"]

    subgraph OUTER["Open coding - taxonomy development"]
        E["Cluster mechanisms"]
        F{"Ending<br/>conditions met?"}
        E --> F
    end

    G["Held-out validation"]
    H["Coupling-error taxonomy"]

    A --> C
    L -- "what counts as an error" --> C
    B --> C
    C -- "grouped into incidents" --> D --> E
    L --- HZ
    C --- U
    F -- no --> E
    F -- yes --> G --> H

    classDef legend fill:#FFFFFF,stroke:#8A93A0,stroke-dasharray: 4 3,color:#12181F
    class U legend
    class HZ legend
    classDef out fill:#DCE8F5,stroke:#2F5D8C,stroke-width:2px,color:#12181F
    class H out
```
