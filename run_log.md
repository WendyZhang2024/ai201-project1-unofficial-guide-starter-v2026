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
​```text
Students declare a major at the end of their second semester, or later if needed (admin_declaring_a_major.txt).
​```

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