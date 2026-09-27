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