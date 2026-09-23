# The Unofficial Guide

Beryl Ghany — corpus: `campus_life`

---

# Unit 1

## What This Does

This system answers plain questions about student life at a fictional university using short peer posts about housing, dining, courses, admin rules, and transit. You ask something like “is the housing lottery random?” or “how often does the shuttle run?”, and it retrieves matching posts from the `campus_life` corpus, refuses questions the documents don’t cover, and writes a short answer that cites the source file.

## Chunking Strategy

**Chunk size:** 450 characters  
**Overlap:** 80 characters

Campus_life posts average about 317 characters — mostly one to three short paragraphs where the useful fact sits in a sentence or two. The starter’s 800-character window barely split anything (88 documents → 88 chunks), which left multi-thought posts glued together. I set size to 450 so a typical post stays one chunk, and use paragraph/sentence packing in `chunker.py::split_documents` so longer posts split on real thought boundaries instead of mid-sentence. Overlap of 80 keeps a trailing sentence when a split does happen. After indexing: 91 chunks, ~306 characters average (shortest 119, longest 431).

## Sample Chunks

**Chunk 1** — source: `admin_add_drop_deadline.txt#0` — produced by: `chunker.py::split_documents`

```
On the add/drop deadline

You can add a course through the end of the second week. Dropping is a longer window — through the end of week six — but a drop after week two shows as a W on your transcript. Nothing anywhere on the registrar's site says this plainly, and students find out from each other.
```

**Chunk 2** — source: `course_biol_160_exams.txt#0` — produced by: `chunker.py::split_documents`

```
BIOL 160 Cell Biology — assessment Four unit tests and a cumulative final. Not curved. The unit tests come fast, roughly every three weeks; falling behind once is very hard to recover from.
```

**Chunk 3** — source: `course_math_220_exams.txt#0` — produced by: `chunker.py::split_documents`

```
MATH 220 Linear Algebra — assessment Two midterms and a cumulative final. Curved to a B- median. The problem sets are the course; the lectures make sense afterwards rather than during.
```

**Chunk 4** — source: `dining_the_ridgeway_cafe.txt#0` — produced by: `chunker.py::split_documents`

```
The Ridgeway Café Second-year here. Wait times: 10 to 15 minutes at 12:30, none after 2:00. The thing worth going for is the only place on campus with real espresso. The thing to know is that seating is tight; about 40 seats for a building of 900. Hours are 7:00am to 4:00pm weekdays only. Costs declining balance only, no meal swipes.
```

**Chunk 5** — source: `housing_morrow_house.txt#0` — produced by: `chunker.py::split_documents`

```
Morrow House — what it's actually like Just finished a year in this building. Built 1954, partially renovated 2008. Rooms are singles and doubles, hall bathrooms. The good: cheapest housing tier by about $900 a year, and the singles are real singles. The bad: known damp problem on the ground floor; two rooms were taken offline in 2024. Laundry costs $1.50 wash, $1.25 dry, coin or card.
```

## Sample Answer

**Question:** Is the housing lottery actually random for juniors and seniors?

**Answer:**

```
No, the housing lottery is not completely random for juniors and seniors. They are ordered by accumulated credit hours first, and ties are broken randomly. (Source: admin_housing_lottery.txt)

Sources retrieved: admin_housing_lottery.txt, admin_parking_permits.txt, advising_registration.txt, housing_innisfree_hall.txt, housing_tamsin_court.txt
```

**My relevance cutoff:** 0.55

In-corpus best distances clustered low (0.13–0.43). Out-of-scope best distances sat high (0.82–0.93). The gap between the worst in-scope hit (shuttle, 0.425) and the best out-of-scope hit (Mongolia, 0.825) is where 0.55 sits — below that, real campus questions still pass; above it, off-topic ones get refused.

| Question | In corpus? | Best distance |
|---|---|---|
| Is the housing lottery actually random for juniors and seniors? | yes | 0.127 |
| What are the lunch wait times at Kestrel Commons between 12:15 and 1:00? | yes | 0.205 |
| How much does laundry cost in Old Brewhouse, and are the machines coin-only? | yes | 0.183 |
| Until when can you declare pass/fail on a course outside your major? | yes | 0.204 |
| How often does the campus shuttle run on weekdays? | yes | 0.425 |
| What is the capital of Mongolia? | no | 0.825 |
| How do I change the oil in a diesel engine? | no | 0.934 |
| Who won the 1994 World Cup? | no | 0.886 |
| What is the recommended dosage of ibuprofen for a headache? | no | 0.844 |
| How do I write a for loop in Rust? | no | 0.896 |

## How I Used AI

**1.** I asked Cursor to pressure-test my five acceptance criteria: for each one, how would you test it using only what the sentence says? Criterion 5 originally said “answers feel grounded,” which it couldn’t turn into a check. I rewrote it as a measurable gate pass rate (4 of 5 in-corpus questions under the cutoff).

**2.** I asked for a paragraph-aware chunker from my notes (keep short posts whole; split longer ones on paragraphs/sentences with overlap). The first draft ignored overlap when packing sentences, so I added the seed-from-previous-chunk overlap logic myself and verified with `python app.py chunks -n 5`.

---

# Unit 2

<!-- Filled in next unit. -->

## Run Log — Before

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 |  |  |  |  |
| 2. Every answer names a source | 5 of 5 |  |  |  |  |
| 3. Gate stops out-of-corpus questions | 4 of 5 |  |  |  |  |
| 4. | | | | | |
| 5. | | | | | |

## Verdicts

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 |  |  |  |
| 2 |  |  |  |
| 3 |  |  |  |
| 4 |  |  |  |
| 5 |  |  |  |

## Diagnoses

## The Improvement

**What I changed:**

**Why I picked it:**

### Run Log — After

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 |  |  |  |  |
| 2. Every answer names a source | 5 of 5 |  |  |  |  |
| 3. Gate stops out-of-corpus questions | 4 of 5 |  |  |  |  |
| 4. | | | | | |
| 5. | | | | | |

**Did it help?**

## What's Still Broken

## What I'd Do Differently
