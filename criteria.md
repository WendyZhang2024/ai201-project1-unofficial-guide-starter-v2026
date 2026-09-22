# Acceptance criteria — The Unofficial Guide

Five criteria that say what "working" means for this system, written in unit 1
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. *"Retrieval works"* is an opinion. *"For at
least 4 of my 5 test questions, the top results include a chunk containing the
answer"* is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter or looser one. A reason that says something about your corpus or your
pipeline earns credit; *"80% seemed reasonable"* does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## 1. Retrieved chunks contain the answer

For at least 4 of my 5 test questions, the retrieved chunks include one that
contains the answer.

**Why this target:**
I chose 4 out of 5 instead of 5 out of 5 is because allowing one failure prevents overfitting. I chose 4 out of 5 instead of 3 out of 5 to ensure basic reliability.

---

## 2. Every answer names a source

Every answer the system produces names at least one source document.

**Why this target:**
Requiring sources allows users to verify the answer. At least 1 source is the baseline. I don't require multiple sources because some niche factual questions exist in only a single document.

---

## 3. The relevance gate stops out-of-corpus questions

When I ask a question my documents clearly don't cover, the relevance gate
stops it and the system returns "I don't have enough information about that" —
in at least 4 of 5 tries.

<!-- The five questions are the ones in `OUT_OF_SCOPE` at the bottom of
     `questions.py`, and `run_eval.py` puts them through the gate and writes
     what happened into your run log. Swap them for your own if you'd rather —
     just keep five of them, or the "4 of 5" above has nothing to be 4 of. -->

**Why this target:**
I allow 4 out of 5 instead of requiring 5 out of 5 because semantic search can sometimes slightly misjudge completely irrelevant questions, causing the relevance score to be too high and cross the threshold.

---

## 4. Something about your chunks

For at least 4 out of my 5 test questions, the retrieved chunks do not exceed 150 characters in length.



**Why this target:**
I set the target at 150 instead of a smaller number because chunks that are too short easily cut off complete sentences. Setting it at 150 avoids bringing in too much irrelevant noise while preserving complete context.


---

## 5. Your choice

For at least 4 out of my 5 test questions, the final answers must contain the keywords required by the expects field in questions.py.


**Why this target:**
I set it at 4 out of 5 instead of 5 out of 5 because LLMs have slight wording randomness when generating answers. Allowing 1 question to miss the keyword due to different phrasing is reasonable.


---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 2 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 1. Retrieved chunks contain the answer

         For at least 4 of my 5 test questions, the retrieved chunks include
         one that contains the answer.

         **Why this target:** ...

         > **Revised in unit 2:** For at least 4 of 5 questions, the top three
         > results contain the answer.
         >
         > **Why revised:** I couldn't judge "the chunks include one that
         > contains the answer" the same way twice — I scored two questions
         > differently on Monday than on Wednesday. The new version is
         > something I can actually check.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said 4 of 5 but got 2 of 5, so 2 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.

     The whole reason the originals stay visible is so someone can see what you
     said before you knew the answer.
     ───────────────────────────────────────────────────────────────────────── -->
