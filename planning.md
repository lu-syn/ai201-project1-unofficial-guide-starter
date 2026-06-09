# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

Student reviews of CS professors at Brooklyn College, sourced from Rate My Professors. These reviews explain their experience with the professor and also give a small insight of what to expect from them. They are honest reviews and little to know sugarcoating, so one would not find any sort of reviews like these on official CUNY Brooklyn College websites or anything remotely similar.

---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

| # |       Source       |          Description         |         URL or location        |
|---|--------------------|------------------------------|--------------------------------|
| 1  |Rate My Professors |Reviews for Noson Yanofsky    |documents/reviews_yanofsky.txt  |
| 2  |Rate My Professors |Reviews for Miriam Briskman   |documents/reviews_briskman.txt  |
| 3  |Rate My Professors |Reviews for Moshe Lach        |documents/reviews_lach.txt      |
| 4  |Rate My Professors |Reviews for Carlos Cuevas     |documents/reviews_cuevas.txt    |
| 5  |Rate My Professors |Reviews for Katherine Chuang  |documents/reviews_chuang.txt    |
| 6  |Rate My Professors |Reviews for Joseph Thurm      |documents/reviews_thurm.txt     |
| 7  |Rate My Professors |Reviews for Moshe Lowenthal   |documents/reviews_lowenthal.txt |
| 8  |Rate My Professors |Reviews for Hui Chen          |documents/reviews_chen.txt      |
| 9  |Rate My Professors |Reviews for Basak Taylan      |documents/reviews_taylan.txt    |
| 10 |Rate My Professors |Reviews for Priyanka Samanta  |documents/reviews_samanta.txt   |

---

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size:** 300 characters

**Overlap:** 50 characters

**Reasoning:**Each review is pretty short. A small chunk size keeps individual reviews intact rather than merging multiple reviews into one chunk. The 50-character overlap ensures that if a review gets split at a boundary, the key context (like the professor's name or course) carries over into the next chunk. This way, no sentences or thoughts get cutoff mid-way.

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:****Embedding model:** all-MiniLM-L6-v2 via sentence-transformers (runs locally, no API key or internet required)

**Top-k:**5

**Production tradeoff reflection:**The model only handles 256 tokens and would get cut off if chunk is longer.
The good thing is that it is free, local, and requires no API keys. It is good enough for this project.

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 |Is Katherine Chuang recommended for CISC3140? |No, students say she is unclear about exam expectations, spends time on trivial material, and refuses to cover topics in depth. One student called it confusing and recommended against it. |
| 2 |What do students say about Moshe Lach's exams in CISC3130? |Exams are based on the homework he assigns. If you do the HW and study it, you will pass. |
| 3 |Does Miriam Briskman curve grades? |Yes, at least one review for CISC2210 mentions she curved the final grade. |
| 4 |What do students say about Lowenthal for 3130? | Mixed reviews, some say he gives you the exam questions and is entertaining, is unorganized, and you will learn nothing but still pass. |
| 5 |Is Yanofsky a funny professor? |Yes, students describe him as funny and enthusiastic about what he teaches. |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1. A query may ask for "Lowenthal" and "CISC3130" and it might cut off numbers between 3130 depending on the chunks. So it won't be as consistent with giving accurate answers.

2. The model again handles 256 tokens which is about 200 characters. So the answers given might be cut off if the chunk is longer.

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->


     Document Ingestion => Chunking        => Embedding + Vector Store    => Retrieval  => Generation
     (.txt files in        (split on "---",  (sentence-transformers,         (ChromaDB,    (Groq API,
     documents/ folder)    then 300 char     all-MiniLM-L6-v2,               top-k=5)      llama-3.3-70b,
                           limit with 50     ChromaDB local storage)                       cited answer)
                           char overlap)

---

## AI Tool Plan

<!-- For each part of the pipeline below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, which requirements)
     - What you expect it to produce
     - How you'll verify the output matches your spec

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Chunking Strategy section and ask it to implement chunk_text()
     with my specified chunk size and overlap" is a plan. -->

**Milestone 3 — Ingestion and chunking:**
- I'll use Claude as the AI tool.
- I'll give it my Chunking Strategy and Documents sections from planning.md as input.
- I expect it to produce a load_and_chunk() function that reads all .txt files from the documents/ folder, splits each file on "---" to get individual reviews, and applies 300-character chunking with 50-character overlap only if a review exceeds 300 characters. Each chunk should be a dict with text, source filename, and chunk_id.
- I'll verify by printing the first 5 chunks and confirming no chunk exceeds 300 characters and that each chunk contains a professor name.

**Milestone 4 — Embedding and retrieval:**
- I'll use Claude as the AI tool.
- I'll give it my Retrieval Approach section from planning.md as input.
- I expect it to produce an embed_and_store() function using sentence-transformers and ChromaDB, and a retrieve() function that takes a query string and returns the top 5 most relevant chunks with their source filenames.
- I'll verify by running 2-3 of my evaluation questions and checking that the returned chunks are actually about the professor mentioned in the query.

**Milestone 5 — Generation and interface:**
- I'll use Claude as the AI tool.
- I'll give it the full planning.md as input.
- I expect it to produce a generate_answer() function that takes a query and retrieved chunks, sends them to Groq's llama-3.3-70b, and returns a grounded answer that only uses information from the retrieved chunks and always includes which source file the answer came from.
- I'll verify by checking that no answer includes information not present in the retrieved chunks.
