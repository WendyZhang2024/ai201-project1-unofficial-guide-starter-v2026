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

<!-- These sections get ADDED to what's already above. Don't delete or rewrite
     unit 1 — the point is that someone can see what you said before you knew
     how it went. -->

## Run Log — Before

<!-- Your five criteria, three runs each. `python run_eval.py --label before`
     runs the questions, puts the OUT_OF_SCOPE ones through the gate, and
     writes it all into results/ for you. Targets come from criteria.md; the
     verdict column is your call.

     Criterion 3 is measured in one deterministic pass rather than three, so
     the same number goes in all three run columns. That's correct, not lazy.

     Milestone 1. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 |  |  |  |  |
| 2. Every answer names a source | 5 of 5 |  |  |  |  |
| 3. Gate stops out-of-corpus questions | 4 of 5 |  |  |  |  |
| 4. | | | | | |
| 5. | | | | | |

<!-- Underneath, paste the REAL output for each criterion from one of your
     runs — the actual text your system produced, not a description of it.
     Name the file and function that produced it. -->

## Verdicts

<!-- MET or MISSED for each of the five, against the target you wrote last
     unit — not a new one. Plus a sentence on how you decided. That sentence
     matters most where it was close.

     If your target said 4 of 5 and your runs came out 4, 3, 4, that's a MISS.
     The target has to hold, not show up occasionally.

     Milestone 2. -->

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 |  |  |  |
| 2 |  |  |  |
| 3 |  |  |  |
| 4 |  |  |  |
| 5 |  |  |  |

## Diagnoses

<!-- For each miss: which stage caused it, and how. The stage alone isn't
     enough — you need the mechanism.

     Not a diagnosis: "Question 3 didn't work."
     A diagnosis:     "Question 3 asks about laundry costs. The answer is in
                       one sentence that got split across two chunks, so
                       neither chunk on its own contains it."

     The five stages: loading → chunking → embedding → retrieval → generation.

     Look for a pattern. If three misses all ask about numbers, that's one
     problem, not three.

     Missed nothing? Say so, then say honestly whether your targets were set
     low, and which one you'd tighten and to what.

     Milestone 3. -->

## The Improvement

**What I changed:**

**Why I picked it:**

<!-- Connect it to a specific diagnosis above in one sentence. If you can't,
     you picked a fix because it sounded impressive. -->

### Run Log — After

<!-- Same format, same five criteria, three runs each.
     `python run_eval.py --label after` -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 |  |  |  |  |
| 2. Every answer names a source | 5 of 5 |  |  |  |  |
| 3. Gate stops out-of-corpus questions | 4 of 5 |  |  |  |  |
| 4. | | | | | |
| 5. | | | | | |

**Did it help?**

<!-- Say plainly whether it did, and how you know. If it made things worse,
     say that — a change that backfired, honestly reported, earns full credit
     and is more interesting than one that worked. What matters is that you can
     tell.

     Milestone 4. -->

## What's Still Broken

<!-- For each criterion still missed after your fix: what you'd do about it,
     and why you stopped where you did.

     "I ran out of time" is fine if it's true. Pretending nothing is left is
     not.

     Milestone 5. -->

## What I'd Do Differently

<!-- Knowing what you know now — which of your five criteria would you write
     differently, and why?

     Milestone 5. -->
