import os
from groq import Groq
from dotenv import load_dotenv
from retrieve import retrieve

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_answer(query):
    # Step 1: Retrieve relevant chunks
    chunks = retrieve(query, k=5)
    
    # Step 2: Build context from chunks
    context = ""
    sources = []
    for chunk in chunks:
        context += f"\n---\n{chunk['text']}"
        if chunk['source'] not in sources:
            sources.append(chunk['source'])
    
    # Step 3: Build grounded prompt
    prompt = f"""You are a helpful assistant for Brooklyn College CS students.
Answer the question using ONLY the information provided in the documents below.
If the documents don't contain enough information to answer, say "I don't have enough information on that."
Always end your answer with: "Sources: " followed by the document names.

Documents:
{context}

Question: {query}

Answer:"""

    # Step 4: Call Groq
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    
    answer = response.choices[0].message.content
    
    return {
        "answer": answer,
        "sources": sources
    }

# Test it
if __name__ == "__main__":
    test_queries = [
        "Is Moshe Lach good for beginners?",
        "Does Miriam Briskman curve grades?",
        "Is Katherine Chuang recommended for CISC3140?"
    ]
    
    for query in test_queries:
        print(f"\nQuestion: {query}")
        result = generate_answer(query)
        print(f"Answer: {result['answer']}")
        print("-" * 50)