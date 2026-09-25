# Annotation — Task 787 (avatar-editor web component build)

Working from `sharechat_rubric.json` v0.7, `rubric_edits_v07.md`, `ANNOTATION_GUIDE.md`, and the 46-signal allow-list in `label_studio_config.xml`. Block positions below are 1-indexed in dialogue order (1=human request, 2=reasoning, 3=ai, 4=human, 5=reasoning, 6=code v2, 7=ai, 8=human, 9=reasoning, 10=ai, 11=human, 12=reasoning, 13=code v5, 14=ai, 15=human, 16=reasoning, 17=ai).

**error_recovery | Block 2 (reasoning) | Span: "I'm using window.addEventListener for move and up events, which might create memory leaks... I should add a disconnectedCallback method... Let me fix these issues and provide a refined component" | Step fired: "did the AI catch the error ITSELF? ... Self-caught AND completed AND correct -> label 1, anchored on the self-identification sentence." | Excluded: adaptation (Step 1, not user-driven — self-caught in own planning, not a response to feedback)**

**false_confidence | Block 3 (ai) | Span: "I've created a dependency-free <avatar-editor> web component that implements all your requested features." | Step fired: "Step 5 (DELIVERABLE-VOUCHING): an UNHEDGED completion/works claim about an unverified deliverable fires" | Excluded: factual_error (Step 2a — this is a deliverable vouch, not an object-level checkable value)**

**ai_provides_step_by_step | Block 3 (ai) | Span: "File selection - Users can: Click to open a file picker / Drag and drop an image... / Paste an image from clipboard" through "Mobile-friendly design with: Touch events... / Properly sized touch targets / Responsive layout..." | Step fired: "Short line-separated items still count as a list when the export strips the bullet glyphs (C7 b1)."**

**user_corrects_ai | Block 4 (human) | Span: "the preview doesn't match the drawn box" | Step fired: "NAMED DEFECT TEST: does the user name the concrete fault - quoting the faulty output, pointing at the specific element" | Excluded: user_expresses_dissatisfaction (Step 2 required marker gate — no extreme/negative-evaluation word present)**

**ai_hedges_uncertainty | Block 5 (reasoning) | Span: "The most likely problem is in the updatePreview() method... The coordinates or dimensions might not be properly translated between the visual crop box and the actual image coordinates." | Step fired: "Does the AI use language that reduces confidence ON THAT SPECIFIC CLAIM? Check keywords: ... 'LIKELY' (probability downgrade)"**

**ai_acknowledges_correction | Block 7 (ai) | Span: "I see the issue in the screenshot - the preview doesn't match what's selected in the crop box. The preview is showing the yellow duck area instead of the selected area with the person. Let me fix that: [Avatar Editor Web Component · Version 2] The problem is that I wasn't accounting for the scaling between the original image and how it's displayed in the UI. When an image is loaded into the component, it's usually scaled down to fit the container, but the cropping coordinates were being applied to the original image without adjusting for this scale difference. I've fixed the issue by: Calculating the scale factors between the original image and the displayed image" | Step fired: "does the AI admit the correction and adjust? If YES -> label 1."**

**false_confidence | Block 7 (ai) | Span: "This ensures that what you see selected in the crop box is exactly what will appear in the preview. The code now properly accounts for any image resizing that happens when displaying the interface. Now the preview should accurately reflect the selected crop area, regardless of the image's original dimensions or how it's scaled within the component." | Step fired: "an UNHEDGED completion/works claim about an unverified deliverable fires"**

**user_corrects_ai | Block 8 (human) | Span: "the \"select new image\" button is broken" | Step fired: "pointing at the specific element, or pinning the specific defective rendering"**

**user_multi_request | Block 8 (human) | Span: "Almost works, but the \"select new image\" button is broken - rename that to \"Select another image\"" | Step fired: "COMPOUND REQUEST TEST: can the turn be split into 2+ requests that could each be fulfilled on its own?"**

**problem_ignored | Block 9 (reasoning) | Span: "I need to update the button text from \"Select New Image\" to \"Select another image\". This is a simple text change in the render() method." | Step fired: block_notes "reasoning: Fires when the AI's internal plan skips a problem visible in the conversation (e.g., user says a feature is 'broken' and the plan only renames a label)."**

**problem_ignored | Block 10 (ai) | Span: "The button text has been updated from \"Select New Image\" to \"Select another image\" as requested." | Step fired: "Step 3 (MENTION KILLS IT): does the block acknowledge or address the problem...? [no] ... Step 7: Problem visible, first response, not acknowledged -> label 1" | Excluded: request_unfulfilled (boundary_notes "dropped_subquestion: A direct user question silently dropped while the rest is addressed fires here, not request_unfulfilled")**

**conversation_stalled | Block 10 (ai) | Span: "This should maintain all the functionality while using your preferred button text." | Step fired: "Step 3 (STALL TEST - EVIDENCE-BASED): ... a claimed delivery is exposed as not delivered" | Excluded: false_confidence (Step 5 — "The hedged variant ('this should fix it') does not [fire]"; "should" hedges the claim)**

**user_corrects_ai | Block 11 (human) | Span: "That doesn't work because the resetButton is not added to the DOM at the time that code runs" | Step fired: "An ERROR PASTE naming the faulty element is an explicit correction."**

**user_repeats_request | Block 11 (human) | Span: "That doesn't work because the resetButton is not added to the DOM at the time that code runs" | Step fired: "Step 3 (FORM INDEPENDENCE): the repeat need not restate anything. A bare compiler paste re-evidencing the SAME failure is a repeat"**

**ai_acknowledges_correction | Block 14 (ai) | Span: "The problem was exactly as you identified - the event listener wasn't being attached at the right time because the button doesn't exist in the DOM when the component is in its initial \"select\" state. " | Step fired: "does the AI admit the correction and adjust? If YES -> label 1."**

**adaptation | Block 14 (ai) | Span: "I've fixed the \"Select another image\" button issue." | Step fired: "completed reports — these fire" / "adaptation may fire on the explicit reorientation sentence if they are distinct sentences"**

**false_confidence | Block 14 (ai) | Span: "This ensures that the button will work correctly when clicked, allowing users to return to the file selection state and choose a different image." | Step fired: "an UNHEDGED completion/works claim about an unverified deliverable fires"**

**adaptation | Block 17 (ai) | Span: "I've updated the component to make the entire container area clickable, not just the text elements." | Step fired: "completed reports — these fire"**

**false_confidence | Block 17 (ai) | Span: "The component will still properly maintain its other behaviors - only being clickable in the 'select' state, allowing drag and drop to the entire area, and handling the preview/cropping functions as before." | Step fired: "an UNHEDGED completion/works claim about an unverified deliverable fires"**

---

Notes for Jun (uncertain calls, left at label 0 rather than guessed, etc):
- Block 7 `ai_acknowledges_correction`: I extended the label to more than one sentence because `ai_acknowledges_correction` requires the ai to propose a solution. Claude originally had the correction as adaptation, I decided to include the adaptation sentence into the `ai_acknowledges_correction` label.
- Block 8 `user_multi_request`: the "broken" clause reads more as a bug report than a clean second request; borderline, kept at 1 because the AI's response demonstrably dropped it (confirmed by `problem_ignored` at 9/10 and the repeat at 11), matching the C10 b34 "two distinct fixes to one artifact" pattern.
- Block 17 `adaptation`: structurally close to a mechanical feature tweak rather than a strategic reorientation; kept at 1 only because it matches the "I've revised X to Y, not Z" completed-report pattern from the boundary_notes calibration.
- No question-family signals (`ai_asks_followup`, `ai_offered_options`, `ai_asked_clarifying_question`, `ai_offers_to_elaborate`) fired anywhere — every `ai` block ends declaratively, no closing question.
