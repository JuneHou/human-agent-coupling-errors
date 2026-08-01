# Task 120 Review — special-case ruling: `under_delivered` vs the "many continue" pattern

> Task id **120**, conv `claude.ai/share/251d5d41-de4c-4573-903c-161569cd46c8`,
> topic `computer_programming`, platform `claude`, **n_turns = 19**.
> WASM/WebGL procedural-shader-generator debugging spiral (sliders don't work → repeated
> "confident fix", user pastes shader-compile errors, many "continue" installments).

## The question logged here
Does the **repeated "continue" / long chunked delivery** pattern warrant `under_delivered`?
**No.** In Jun's ground-truth annotation `under_delivered` fires **exactly once**, and not for the continues.

## Ruling

### 1. `under_delivered` fires on b12 — narrated-but-undelivered artifact (NOT the continues)
- b12 (ai) delivers only the **"Fixed Rust Implementation (src/lib.rs)"** artifact (b11), but its fix
  instructions tell the user to *"Replace static/main.js with the improved code from the
  **'Updated JavaScript with Error Handling'** artifact"* — **an artifact never produced that turn.**
- Trigger = a **named/promised deliverable that fell short**, per `under_delivered` code block_note
  ("implements less than the specification required"). Span sits on the "…with Error Handling artifact.
  Rebuild and Run… These changes should fix the shader compilation errors" region.
- Contrast [[feedback-narrated-artifact-is-false-confidence]] (task 89): a code artifact merely *absent
  from the lossy export* does **not** establish non-delivery — hold at 0 and verify against rendered
  source. Here the JS artifact was **genuinely never generated**, and the pattern (referencing
  nonexistent "Updated/Improved JavaScript" artifacts) **recurs across the conversation**, so Jun
  judged real under-delivery.

### 2. The "many continue"s do NOT trigger `under_delivered`
- Length-limit truncation of a long installment → `ai_malfunction` (mechanical cutoff), never
  `under_delivered`. A "continue" that nets forward content → `conversation_advanced` on the ai turn.
- Regenerate-from-scratch after "continue" is **not** `repetition` (R6).

### 3. Related distinctions confirmed in Jun's slate (context, not re-adjudicated)
- **"Confident fix that doesn't resolve, same approach reapplied"** → `conversation_stalled`
  (b12, b18, b42), not advanced. Turns that genuinely shift approach → `conversation_advanced`
  (b15 float-formatting fix, b22 minimal-example pivot, b54 specific error fix).
- **First error-paste of a bug** = `user_corrects_ai` (b13, b16, b43); **nth "still doesn't work / same"
  repeat** = `user_repeats_request` (b19, b43, b49).

## Takeaway (logged to memory)
`under_delivered` = a **named deliverable/requirement not actually delivered** — including an artifact
the turn *references but never produced*. It is **not** triggered by chunked/continue delivery or
truncation. See [[feedback-unfollowed-instruction-is-under-delivered]].
