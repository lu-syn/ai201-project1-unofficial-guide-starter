# The Unofficial Guide — Project 1

---

## Domain

Student reviews of CS professors at Brooklyn College, sourced from Rate My Professors. These reviews explain their experience with the professor and also give a small insight of what to expect from them. They are honest reviews and little to know sugarcoating, so one would not find any sort of reviews like these on official CUNY Brooklyn College websites or anything remotely similar.

---

## Document Sources

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
| 1 | Rate My Professors | Text file | documents/reviews_yanofsky.txt |
| 2 | Rate My Professors | Text file | documents/reviews_briskman.txt |
| 3 | Rate My Professors | Text file | documents/reviews_lach.txt |
| 4 | Rate My Professors | Text file | documents/reviews_cuevas.txt |
| 5 | Rate My Professors | Text file | documents/reviews_chuang.txt |
| 6 | Rate My Professors | Text file | documents/reviews_thurm.txt |
| 7 | Rate My Professors | Text file | documents/reviews_lowenthal.txt |
| 8 | Rate My Professors | Text file | documents/reviews_chen.txt |
| 9 | Rate My Professors | Text file | documents/reviews_taylan.txt |
| 10 | Rate My Professors | Text file | documents/reviews_samanta.txt |

---

## Chunking Strategy

**Chunk size:** 300 characters

**Overlap:** 50 characters

**Why these choices fit your documents:** Each review is pretty short. A small chunk size keeps individual reviews intact rather than merging multiple reviews into one chunk. The 50-character overlap ensures that if a review gets split at a boundary, the key context (like the professor's name or course) carries over into the next chunk. This way, no sentences or thoughts get cutoff mid-way.

**Final chunk count:** 122 chunks across 10 documents

---

## Embedding Model

**Model used:** all-MiniLM-L6-v2 via sentence-transformers (runs locally, no API key or internet required)

**Production tradeoff reflection:** The model only handles 256 tokens and would get cut off if chunk is longer.
The good thing is that it is free, local, and requires no API keys. It is good enough for this project.

---

## Grounded Generation

**System prompt grounding instruction:** "You are a helpful assistant for Brooklyn College CS students. Answer the question using ONLY the information provided in the documents below. If the documents don't contain enough information to answer, say 'I don't have enough information on that.' Always end your answer with: 'Sources: ' followed by the document names."

**How source attribution is surfaced in the response:** Source filenames are collected from the metadata of each retrieved chunk and displayed in a separate "Retrieved from" field in the Gradio UI. The LLM is also instructed to cite sources inline in its response.

---

## Evaluation Report

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | Is Katherine Chuang recommended for CISC3140? | No, reviews describe unclear expectations, outdated material, harsh grading | Correctly said Chuang is not recommended, cited low quality ratings and unclear expectations | Relevant | Accurate |
| 2 | What do students say about Moshe Lach's exams in CISC3130? | Exams are based on HW; if you do the HW you will pass | Correctly stated Lach bases quizzes and tests on HW assigned in CISC3130 | Relevant | Accurate |
| 3 | Does Miriam Briskman curve grades? | Yes, at least one CISC2210 review mentions curved final grade | Correctly said yes, Briskman curved the final grade for CISC3310 | Relevant | Accurate |
| 4 | What do students say about Lowenthal for CISC3130? | Mixed — entertaining but mumbles, gives exam questions, lenient grader | Correctly summarized mixed opinions: entertaining and gives exam questions, but also criticized for mumbling and unclear grading | Relevant | Accurate |
| 5 | Is Yanofsky a funny professor? | Yes, described as funny and enthusiastic | Correctly said yes, but noted a chunk was cut off mid-sentence ("His jokes are...") | Partially relevant | Partially accurate |

---

## Failure Case Analysis

**Question that failed:** Is Yanofsky a funny professor?

**What the system returned:** The system correctly identified Yanofsky as funny and enthusiastic, but explicitly noted that one retrieved chunk contained an incomplete sentence: "His jokes are (although the sentence is cut off)."

**Root cause (tied to a specific pipeline stage):** The failure occurred at the chunking stage. The 300-character fixed-size chunker split a review mid-sentence, creating a chunk that ended with "His jokes are" without completing the thought. When this fragment was retrieved and passed to the LLM, the model correctly identified the truncation but couldn't complete the answer. This is a chunking boundary problem since the split didn't respect sentence structure.

**What you would change to fix it:** Instead of pure character-based chunking, use sentence-aware splitting that only cuts at sentence boundaries. The NLTK or spaCy library can detect sentence ends, ensuring no chunk ever contains an incomplete sentence.

---

## Spec Reflection

**One way the spec helped you during implementation:** The planning.md chunking strategy section forced me to think about chunk size before writing any code. Because I had already decided on 300 characters with a "split on --- first" approach, the implementation was straightforward — I knew exactly what the function needed to do and could verify it was working correctly by checking that each chunk contained one review.

**One way your implementation diverged from the spec, and why:** The spec originally described pure 300-character chunking with 50-character overlap applied to the entire file. During implementation, I changed this to split on "---" first and only apply character chunking to reviews longer than 300 characters. This was a better fit for the data because reviews are naturally self-contained units — merging two reviews into one chunk would confuse retrieval and make source attribution less precise.

---

## AI Usage

**Instance 1**

- *What I gave the AI:* My Chunking Strategy and Documents sections from planning.md, along with the structure of my .txt review files
- *What it produced:* A load_and_chunk() pipeline with three functions: load_documents(), split_into_reviews(), and chunk_reviews()
- *What I changed or overrode:* The original spec described pure character chunking. After seeing the output, I kept the "split on --- first" approach because it produced cleaner, more self-contained chunks that matched individual reviews rather than merging multiple reviews together.

**Instance 2**

- *What I gave the AI:* My Retrieval Approach section from planning.md and the output of my chunking pipeline
- *What it produced:* embed_and_store() and retrieve() functions using sentence-transformers and ChromaDB, plus a generate_answer() function connecting to Groq's llama-3.3-70b
- *What I changed or overrode:* The generated grounding prompt initially just said "use the documents." I strengthened it to explicitly say "answer using ONLY the information provided" and added the instruction to say "I don't have enough information" when the answer isn't in the documents, which is critical for preventing hallucination.