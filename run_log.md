### Before Run Log

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunks contain the answer | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 2. Every answer names a source | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 3. The relevance gate stops out-of-corpus questions | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 4. Retrieved chunks do not exceed 150 characters | 4 of 5 | 0/5 | 0/5 | 0/5 | MISSED |
| 5. Final answers contain expected keywords | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |

## Real output for each criterion

### Criterion 1 Real Output
Produced by `generate.py::answer_from_chunks` (via `run_eval.py::run_once`).
​```text
Students declare a major at the end of their second semester, or later if needed (admin_declaring_a_major.txt).
​```

### Criterion 2 Real Output
Produced by `generate.py::answer_from_chunks` (via `run_eval.py::run_once`).
```text
You can change your meal plan tier once, during the first ten days of the semester.
Source: admin_meal_plan_changes.txt
```

### Criterion 3 Real Output
Produced by `run_eval.py::check_out_of_scope`.

| Out-of-scope question | Best distance | Gate |
|---|---|---|
| What is the capital of Mongolia? | 0.787 | refused |
| How do I change the oil in a diesel engine? | 0.923 | refused |
| Who won the 1994 World Cup? | 0.847 | refused |
| What is the recommended dosage of ibuprofen for a headache? | 0.824 | refused |
| How do I write a for loop in Rust? | 0.877 | refused |

-> gate refused 5 of 5

### Criterion 4 Real Output
Produced by `check_chunks.py` (chunks retrieved via `store.py::search`).
​```text
Question: When do students declare a major?
  Chunk 1 length: 274 chars
  Chunk 2 length: 259 chars
  Chunk 3 length: 282 chars
  Chunk 4 length: 300 chars
  Chunk 5 length: 74 chars
​```

### Criterion 5 Real Output
Produced by `generate.py::answer_from_chunks` (via `run_eval.py::run_once`).
​```text
You have fifteen days from the grade posting to raise a grade appeal (admin_grade_appeals.txt).
​```

## Verdict Rationale

- **Criterion 1 (MET):** Target was 4 of 5. My run log shows that all five test questions retrieved chunks containing the answer (5/5 across three runs), which exceeds the target.
- **Criterion 2 (MET):** Target was 5 of 5. Every generated answer explicitly cited its source document in the text, which meets the strict requirement.
- **Criterion 3 (MET):** Target was 4 of 5. The gate deterministically refused all five out-of-corpus questions (5/5), exceeding the target.
- **Criterion 4 (MISSED):** Target was 4 of 5. I measured the retrieved chunks for each question and found that in every one of the 5 test questions, at least one of the 5 retrieved chunks exceeded 150 characters — meaning 0 of 5 questions had all their chunks within the limit (0/5 across three runs). The target was not met. This is a genuine miss, not a broken criterion — the 150-character check was fully measurable using `check_chunks.py`, so no revision was made. The number stays as recorded and will be diagnosed and addressed as an improvement target.
- **Criterion 5 (MET):** Target was 4 of 5. I checked the `expects` field in `questions.py` and confirmed all five answers contained their required keywords (5/5), exceeding the target.

## Revision Notes
No revisions were made. All criteria were measurable and measurable in a consistent manner.

## Diagnoses

### Criterion 4 MISSED (Target: 4 of 5, Result: 0 of 5)
- **Failed stage:** Chunking (`chunker.py::split_documents`)
- **Mechanism:** The current strategy splits strictly on paragraph breaks (`\n\n`) and only merges chunks smaller than 50 characters, which has no upper bound. Any paragraph that happens to be long in the source text becomes one long chunk untouched. This explains the wide, inconsistent chunk lengths observed (74–300 characters across the same question): short paragraphs get merged up, but long paragraphs are never split down. Since this is a property of the splitting logic itself rather than any single document, it affects all 5 test questions the same way rather than five separate failures.

## Improvement

- **Change made:** Replaced `chunker.py::split_documents` with a sentence-aware splitter that enforces a 150-character maximum chunk size.
- **Failure it was meant to fix:** Criterion 4 (Retrieved chunks do not exceed 150 characters), diagnosed as caused by the chunking stage lacking an upper bound on paragraph length.

### After Run Log

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunks contain the answer | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 2. Every answer names a source | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 3. The relevance gate stops out-of-corpus questions | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 4. Retrieved chunks do not exceed 150 characters | 4 of 5 | 3/5 | 3/5 | 3/5 | MISSED |
| 5. Final answers contain expected keywords | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |

### Criterion 4 — real output (the chunks still over the limit)

Produced by `chunker.py::split_documents` (via `store.py::search`), from `check_chunks.py`.

The two questions that still have one oversized chunk each — "When do students declare a major?" and "When do study abroad applications open?" — both have a chunk at exactly 160 characters. Both correspond to single sentences from the source documents that are themselves longer than 150 characters, so the sentence-level splitter has nowhere left to cut without breaking a sentence in half:

```text
Chunk length: 160 chars
```

### Did the change help?

**Comparison based on the numbers from both run logs:**

- **Criterion 4:** Before = 0/5 (MISSED). After = 3/5 (MISSED). The chunking change partially improved the result, increasing the score from 0/5 to 3/5. It fixed the issue for 3 out of 5 questions, but two questions (declare a major, study abroad) still have a single chunk at 160 characters, falling short of the 4/5 target.
- **Criterion 1:** Before = 5/5 (MET). After = 5/5 (MET). The smaller chunks did not harm retrieval accuracy. Best distances also decreased (e.g., declare a major went from 0.37 to 0.19), consistent with smaller, more topically-focused chunks producing embeddings closer to the question — though this is a side effect of chunk size, not a separate improvement to retrieval itself.
- **Other Criteria:** Criteria 2, 3, and 5 remained at 5/5 (MET). No regressions were observed.

**Conclusion:** The improvement directly addressed the diagnosed failure and moved Criterion 4 from 0/5 to 3/5. However, it did not fully meet the 4/5 target because two chunks remained slightly over the 150-character limit, each corresponding to a single source sentence longer than the target itself. No other criteria were negatively affected by the change. The change is considered a partial success.