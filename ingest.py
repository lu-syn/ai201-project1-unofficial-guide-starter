import os

def load_documents(folder_path):
    documents = []
    
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            filepath = os.path.join(folder_path, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                text = f.read()
            documents.append({
                "filename": filename,
                "text": text
            })
    
    return documents


def split_into_reviews(documents):
    reviews = []
    
    for doc in documents:
        chunks = doc["text"].split("---")
        
        for chunk in chunks:
            cleaned = chunk.strip()
            if len(cleaned) > 0:
                reviews.append({
                    "filename": doc["filename"],
                    "text": cleaned
                })
    
    return reviews


def chunk_reviews(reviews, chunk_size=300, overlap=50):
    chunks = []
    chunk_id = 0
    
    for review in reviews:
        text = review["text"]
        
        if len(text) <= chunk_size:
            chunks.append({
                "chunk_id": chunk_id,
                "filename": review["filename"],
                "text": text
            })
            chunk_id += 1
        else:
            start = 0
            while start < len(text):
                end = start + chunk_size
                chunks.append({
                    "chunk_id": chunk_id,
                    "filename": review["filename"],
                    "text": text[start:end]
                })
                chunk_id += 1
                start += chunk_size - overlap
    
    return chunks


# Test it
if __name__ == "__main__":
    documents = load_documents("documents")
    print(f"Loaded {len(documents)} documents")
    
    reviews = split_into_reviews(documents)
    print(f"Split into {len(reviews)} reviews")
    
    chunks = chunk_reviews(reviews)
    print(f"Created {len(chunks)} chunks")
    
    print("\n--- 5 sample chunks ---")
    for chunk in chunks[:5]:
        print(f"\nChunk {chunk['chunk_id']} | Source: {chunk['filename']}")
        print(chunk['text'])
        print("-" * 40)