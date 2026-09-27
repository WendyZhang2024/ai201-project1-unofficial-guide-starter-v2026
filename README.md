# The Unofficial Guide

Name: WendyZhang2024 | Corpus: campus_life

> **This file is your submission.** Fill it in as you go — most sections get
> written during the milestone that produces them, not at the end.
>
> How the starter works, and every command you'll need, is in `RUNNING.md`.
> Leave that file alone.
>
> **Paste everything as text.** No screenshots, no video. A typed table gets
> full credit; a picture of the same table gets none.
>
> Delete these instruction blocks as you replace them. The `<!-- -->` comments
> are notes to you and don't show up when the page renders — you can leave them
> or remove them.

---

# Unit 1

## What This Does

This project builds a retrieval-augmented generation (RAG) system over the `campus_life`  corpus. It answers common student-life questions—such as declaring a major, filing a grade appeal, changing a meal plan, or exploring study-abroad options—by retrieving relevant text chunks and using a large language model to produce grounded answers. The system is evaluated against five acceptance criteria using five test questions.

## Chunking Strategy

**Chunk size:** Paragraph-based (dynamic), with a minimum merge threshold of 50 characters.
**Overlap:** 0

When I first read the `campus_life` documents, I noticed they are mostly short posts and paragraphs rather than long continuous essays. The starter's fixed 800-character window created 271 chunks with an average length of only 101 characters, and worst of all, a shortest chunk of 10 characters. These tiny fragments were isolated titles that had lost their context, making them impossible to answer questions from.

So I replaced the fixed window with a paragraph split (`\n\n`) and added a buffer to merge any paragraph shorter than 50 characters into the following text. 

I changed my mind partway through: I initially tried a 30-character threshold, but after testing, it truned out that a 31-character title (`PHYS 130 Mechanics — assessment`) still became an isolated chunk. Raising the threshold to 50 solved the issue. As a result, the total number of chunks dropped to 179, the average length increased to 154 characters, and the shortest chunk became 57 characters. This ensures every chunk is self-contained and answerable without losing context.

## Sample Chunks



**Chunk 1** — source: `admin_add_drop_deadline.txt#0` — produced by: `chunker.py::split_documents`

```
On the add/drop deadline

You can add a course through the end of the second week. Dropping is a longer window — through the end of week six — but a drop after week two shows as a W on your transcript. Nothing anywhere on the registrar's site says this plainly, and students find out from each other.
```


**Chunk 2** — source: `course_cs_340_exams.txt#1` — produced by: `chunker.py::split_documents`

```
Start the term project in week three, not week eight; everyone learns this the hard way.
```


**Chunk 3** — source: `course_phys_130_workload.txt#1` — produced by: `chunker.py::split_documents`

```
It's front-loaded — the first month is heavier than the rest, partly because you're learning the format.

```

**Chunk 4** — source: `health_center.txt#0` — produced by: `chunker.py::split_documents`

```
The health centre

Walk-in hours are 8am to 11am; everything after that is by appointment and appointments run about a week out. If something is urgent, go at 8am and wait rather than booking.

```

**Chunk 5** — source: `housing_morrow_house.txt#1` — produced by: `chunker.py::split_documents`

```
The good: cheapest housing tier by about $900 a year, and the singles are real singles.
```

## Sample Answer

<!-- One complete question and answer, pasted as text, with the source line
     visible. Milestone 4. -->

**Question:** When can you change your meal plan tier?

**Answer:** You can change your meal plan tier once, during the first ten days of the semester.
Source: admin_meal_plan_changes.txt



**My relevance cutoff:** 0.58

*   In-corpus questions (best distances): 0.372, 0.157, 0.268, 0.216, 0.234 (max = 0.372). Tested with 0.58 cutoff: correctly answered and passed the gate.
*   Out-of-scope questions (best distances): 0.787, 0.923, 0.847, 0.824, 0.877 (min = 0.787). Tested with 0.58 cutoff: correctly refused ("I don't have enough information about that").
*   There is a clean gap between 0.372 and 0.787. I chose 0.58 because it sits almost exactly in the middle of this gap (0.208 margin on the low side, 0.207 on the high side). This symmetric margin protects against both slightly harder in-scope questions (which might score higher) and slightly easier out-of-scope questions (which might score lower).
*   Caveat: This cutoff is verified against my 5 in-scope and 5 out-of-scope examples. It may need revision if boundary-straddling or ambiguously phrased questions are introduced later.

| Question | In corpus? | Best distance |
|---|---|---|
| When do students declare a major? | Yes | 0.372 |
| How many days do you have to raise a grade appeal? | Yes | 0.157 |
| How many credit hours are required for graduation? | Yes | 0.268 |
| When can you change your meal plan tier? | Yes | 0.216 |
| When do study abroad applications open? | Yes | 0.234 |
| What is the capital of Mongolia? | No | 0.787 |
| How do I change the oil in a diesel engine? | No | 0.923 |
| Who won the 1994 World Cup? | No | 0.847 |
| What is the recommended dosage of ibuprofen? | No | 0.824 |
| How do I write a for loop in Rust? | No | 0.877 |



## How I Used AI

**1.**
I initially wrote a paragraph-based chunker (`split_documents`) but it produced a problematic 10-character isolated chunk ("On the add/drop deadline"). I asked Claude to diagnose the output. It identified that my code lacked a "heading vs. body" concept, which isolated short titles from their answers and fused multi-fact paragraphs together. Based on this diagnosis, I worked with DeepSeek to implement a buffer mechanism to merge short paragraphs into the following text. During testing, DeepSeek pointed out that a 30-character threshold still left a 31-character title isolated, so I raised the threshold to 50. This reduced my chunks from 271 to 179, increased the average length to 154 characters, and eliminated all fragments (shortest chunk became 57 characters).

**2.**
I collected best-distance scores for 5 in-scope questions (0.157–0.372) and 5 out-of-scope questions (0.787–0.923), and asked Claude where to set the cutoff. Claude pointed out the clean gap between the two groups and suggested picking 0.58 for symmetric margin (~0.2 on each side), while noting that boundary-straddling questions couldn't be validated with this sample. DeepSeek guided me to run concrete verifications: a normal question with distance 0.372 correctly passed the gate, while an out-of-scope question about the capital of Mongolia (0.787) was correctly rejected and triggered the "I don't have enough information" response. I documented this entire rationale and the caveat in my README.

**Stretch feature:** Completed. I added chunk-level distance scores to the CLI output in `app.py`. Chunks near the cutoff (0.58) are flagged with ⚠️, and rejected chunks are flagged with ❌.
Tested result: For "When do students declare a major?", top chunks scored 0.372 and 0.509 (⚠️), while the rest scored 0.589, 0.638, 0.680 (❌). For "What is the capital of Mongolia?", all 5 chunks scored 0.787–0.879 (❌) and the system correctly refused to answer.

**Evaluated but dropped:** I also considered the "Answer caching improvements" stretch feature (`--no-cache` flag). After analyzing it, I realized that for a normal user, caching is always superior (faster, cheaper, identical answer). A `--no-cache` flag is a development/debugging tool. It forces a fresh model call when I am actively changing code, so I don't accidentally test against a stale cached response. Since this adds only developer convenience (not user value) and introduces more CLI argument complexity, I decided to skip it and focus on delivering a polished relevance-scoring feature instead.

---

# Unit 2

**Stretch Feature:** I am attempting a second measured improvement.

The full run logs, verdicts, diagnoses, and the before/after improvement analysis are documented in [run_log.md](./run_log.md).

## Run Log — Before



| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunks contain the answer | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 2. Every answer names a source | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 3. The relevance gate stops out-of-corpus questions | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 4. Retrieved chunks do not exceed 150 characters | 4 of 5 | 0/5 | 0/5 | 0/5 | MISSED |
| 5. Final answers contain expected keywords | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |

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

## Verdicts

### Verdict Rationale

- **Criterion 1 (MET):** Target was 4 of 5. My run log shows that all five test questions retrieved chunks containing the answer (5/5 across three runs), which exceeds the target.
- **Criterion 2 (MET):** Target was 5 of 5. Every generated answer explicitly cited its source document in the text, which meets the strict requirement.
- **Criterion 3 (MET):** Target was 4 of 5. The gate deterministically refused all five out-of-corpus questions (5/5), exceeding the target.
- **Criterion 4 (MISSED):** Target was 4 of 5. I measured the retrieved chunks for each question and found that in every one of the 5 test questions, at least one of the 5 retrieved chunks exceeded 150 characters — meaning 0 of 5 questions had all their chunks within the limit (0/5 across three runs). The target was not met. This is a genuine miss, not a broken criterion — the 150-character check was fully measurable using `check_chunks.py`, so no revision was made. The number stays as recorded and will be diagnosed and addressed as an improvement target.
- **Criterion 5 (MET):** Target was 4 of 5. I checked the `expects` field in `questions.py` and confirmed all five answers contained their required keywords (5/5), exceeding the target.

### Revision Notes
No revisions were made. All criteria were measurable and measurable in a consistent manner.

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 | Retrieved chunks contain the answer (target: 4 of 5) | MET | Across all three runs, every one of the 5 test questions produced an answer stating the correct fact (e.g. "fifteen days," "120 credit hours"), consistent across runs — 5/5 each time, above the 4/5 target. |
| 2 | Every answer names a source (target: 5 of 5) | MET | Checked each of the 15 answers (5 questions × 3 runs) for a literal filename or `Source:` line; every single one included it, with no exceptions. |
| 3 | The relevance gate stops out-of-corpus questions (target: 4 of 5) | MET | Ran the 5 `OUT_OF_SCOPE` questions once through `run_eval.py::check_out_of_scope`; all 5 best-distances exceeded the 0.58 threshold, so the gate refused all 5. Measured once since retrieval and the gate are deterministic — the same 5/5 applies to all three run columns. |
| 4 |  Measured actual retrieved chunk lengths with `check_chunks.py`. In every one of the 5 test questions, at least one of the 5 retrieved chunks exceeded 150 characters, so 0 of 5 questions had all their chunks within the limit — well short of the 4 of 5 target. |
| 5 | Final answers contain expected keywords (target: 4 of 5) | MET | Compared each answer's text against the `expects` field in `questions.py` for all 5 questions across all 3 runs; the required keyword (e.g. "second semester," "October") appeared verbatim in every case — 5/5 each run. |

## Diagnoses

### Criterion 4 MISSED (Target: 4 of 5, Result: 0 of 5)
- **Failed stage:** Chunking (`chunker.py::split_documents`)
- **Mechanism:** The current strategy splits strictly on paragraph breaks (`\n\n`) and only merges chunks smaller than 50 characters, which has no upper bound. Any paragraph that happens to be long in the source text becomes one long chunk untouched. This explains the wide, inconsistent chunk lengths observed (74–300 characters across the same question): short paragraphs get merged up, but long paragraphs are never split down. Since this is a property of the splitting logic itself rather than any single document, it affects all 5 test questions the same way rather than five separate failures.

## The Improvement

**What I changed:** Replaced `chunker.py::split_documents` with a sentence-aware splitter that enforces a 150-character maximum chunk size.

**Why I picked it:** The diagnosis pointed directly at the chunking stage (`chunker.py::split_documents`) lacking an upper bound on paragraph length, which directly caused Criterion 4 to fail (0/5).

### Run Log — After



| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunks contain the answer | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 2. Every answer names a source | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 3. The relevance gate stops out-of-corpus questions | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 4. Retrieved chunks do not exceed 150 characters | 4 of 5 | 3/5 | 3/5 | 3/5 | MISSED |
| 5. Final answers contain expected keywords | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |

**Did it help?**

Yes, partially.

***Comparison based on the numbers from both run logs:***

- **Criterion 4:** Before = 0/5 (MISSED). After = 3/5 (MISSED). The chunking change partially improved the result, increasing the score from 0/5 to 3/5. It fixed the issue for 3 out of 5 questions, but two questions (declare a major, study abroad) still have a single chunk at 160 characters, falling short of the 4/5 target.
- **Criterion 1:** Before = 5/5 (MET). After = 5/5 (MET). The smaller chunks did not harm retrieval accuracy. Best distances also decreased (e.g., declare a major went from 0.37 to 0.19), consistent with smaller, more topically-focused chunks producing embeddings closer to the question — though this is a side effect of chunk size, not a separate improvement to retrieval itself.
- **Other Criteria:** Criteria 2, 3, and 5 remained at 5/5 (MET). No regressions were observed.

**Conclusion:** The improvement directly addressed the diagnosed failure and moved Criterion 4 from 0/5 to 3/5. However, it did not fully meet the 4/5 target because two chunks remained slightly over the 150-character limit, each corresponding to a single source sentence longer than the target itself. No other criteria were negatively affected by the change. The change is considered a partial success.

## What's Still Broken

**Criterion 4 (Retrieved chunks do not exceed 150 characters):**
- **Status:** Still missed after the fix (score improved from 0/5 to 3/5, but the target remains 4/5).
- **What I'd do about it:** The root cause is fixed, but there are two edge cases where a chunk still reached 160 characters (specifically in the questions "When do students declare a major?" and "When do study abroad applications open?"). This is likely due to a single sentence exceeding 150 characters, though I have not verified whether a buffer-merging edge case also contributes. To fix this, I would add a secondary fallback: if a single sentence still exceeds the limit, force-split it at the nearest comma rather than hard-cutting at the character count — a hard cut risks severing a word mid-token, while a comma-split at least respects a natural clause boundary. I would also lower `target_size` from 150 to 140 to create a small safety margin.
- **Why I stopped here:** The primary structural flaw (no upper bound on chunk length) was diagnosed and fixed, moving the result from 0/5 to 3/5 and drastically improving retrieval precision (best distance for the "declare a major" question dropped from 0.37 to 0.19). The remaining fix is small and well-defined, but I prioritized verifying and documenting the improvement I'd already made — including rebuilding the index and re-running the full evaluation — over chasing the last two edge cases, given the time remaining in this unit.

## What I'd Do Differently

**Regarding the criteria:**
Knowing what I know now, I would rewrite Criterion 4 to be more flexible regarding natural language boundaries. Instead of requiring strict compliance for 4 out of 5 questions ("all chunks must be ≤ 150 characters"), I would specify a target like: "For at least 4 out of 5 questions, the average chunk length must be ≤ 150 characters, with no single chunk exceeding 200 characters." This still enforces the spirit of the short-chunk requirement but tolerates the fact that a single grammatical sentence occasionally runs slightly over 150 characters. A strict hard limit risks cutting sentences in half and losing the context Criterion 1 depends on. This also reflects something I didn't anticipate when I wrote the original criterion in Unit 1: I hadn't yet seen how much natural sentence length varies across a real corpus, so the 150-character target was set before I had evidence to calibrate it against.

**Regarding the pipeline:**
I would also rebuild the index immediately after modifying the chunking logic in the future — I initially forgot this step and had to run `python app.py index` after `check_chunks.py` kept returning stale, unchanged lengths despite my code edits.

## How I Used AI

In this unit, I used AI (specifically Deepseek and Claude) to assist with diagnosing the failed criterion. After my initial testing showed Criterion 4 failed (0/5), I shared the relevant `chunker.py` logic and the raw measurement data with the AI to assist in tracing the failure.

The AI traced the failure to the chunking stage: my original logic only merged small paragraphs together but completely lacked an upper bound to split long paragraphs. It also pointed out that this was likely one root cause affecting all 5 questions rather than five separate failures, since the mechanism was the same across all of them. I verified this independently by reading the code myself and running `check_chunks.py` to measure the actual chunk lengths before accepting the diagnosis.

I also used AI to help draft a sentence-aware splitting strategy using `re.split`. But I was responsible for integrating the fix into my codebase, rebuilding the vector index (`python ingest.py`), running the full evaluation (`run_eval.py --label after`), and accurately reporting the resulting data (0/5 to 3/5), including the fact that the fix did not fully reach the 4/5 target.