import chromadb
from sentence_transformers import SentenceTransformer
from ingest import load_documents, split_into_reviews, chunk_reviews

# Load the embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Set up ChromaDB
client = chromadb.PersistentClient(path="./chroma_db")

def embed_and_store(chunks):
    collection = client.get_or_create_collection(name="professor_reviews")
    
    texts = [chunk["text"] for chunk in chunks]
    ids = [str(chunk["chunk_id"]) for chunk in chunks]
    metadatas = [{"source": chunk["filename"]} for chunk in chunks]
    embeddings = model.encode(texts).tolist()
    
    collection.add(
        documents=texts,
        embeddings=embeddings,
        metadatas=metadatas,
        ids=ids
    )
    print(f"Stored {len(chunks)} chunks in ChromaDB")

def retrieve(query, k=5):
    collection = client.get_or_create_collection(name="professor_reviews")
    query_embedding = model.encode([query]).tolist()
    
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=k
    )
    
    chunks = []
    for i in range(len(results["documents"][0])):
        chunks.append({
            "text": results["documents"][0][i],
            "source": results["metadatas"][0][i]["source"],
            "distance": results["distances"][0][i]
        })
    return chunks

# Test it
if __name__ == "__main__":
    documents = load_documents("documents")
    reviews = split_into_reviews(documents)
    chunks = chunk_reviews(reviews)
    
    embed_and_store(chunks)
    
    print("\n--- Testing retrieval ---")
    test_queries = [
        "Is Moshe Lach good for beginners?",
        "Does Miriam Briskman curve grades?",
        "Is Katherine Chuang recommended for CISC3140?"
    ]
    
    for query in test_queries:
        print(f"\nQuery: {query}")
        results = retrieve(query)
        for r in results:
            print(f"  Source: {r['source']} | Distance: {r['distance']:.3f}")
            print(f"  {r['text'][:150]}...")