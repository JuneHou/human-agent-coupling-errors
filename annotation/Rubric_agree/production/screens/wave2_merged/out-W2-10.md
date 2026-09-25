# merged screen W2-10

| Signal | Block | Role | Span | Step fired | Excluded |
|---|---|---|---|---|---|
| ai_structured_response | 3 | ai | Executive Summary - A high-level overview of the current status of these market leaders | Step 1 "(f) a line containing ' - ' (space hyphen space) with at most 50 characters before it and a non-space character after it — the 'Name - description' entry" + Step 2 "three or more of (f)" | |
| ai_offers_to_elaborate | 3 | ai | Would you like me to focus on any particular aspect of these companies in more detail? | Step 2 "the offer must be about the delivered content or topic"; Step 5 "conditional depth-offer on delivered content -> label 1" | ai_asks_followup, Step 3 "Is the offer specifically to ELABORATE content already provided? If YES -> ai_offers_to_elaborate." |
