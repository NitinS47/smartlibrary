import faiss
import numpy as np
import pickle
from sentence_transformers import SentenceTransformer

# Load book data
with open("book_data.pkl", "rb") as f:
    books = pickle.load(f)

# Load SentenceTransformer model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Convert book summaries into embeddings
book_vectors = np.array([model.encode(book["summary"]) for book in books]).astype("float32")

# Initialize FAISS index
index = faiss.IndexFlatL2(384)  # 384 dimensions for MiniLM model
index.add(book_vectors)

# Save FAISS index
with open("faiss_index.pkl", "wb") as f:
    pickle.dump(index, f)

print("✅ faiss_index.pkl created successfully!")
