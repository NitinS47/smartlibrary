import faiss
import numpy as np
import pickle
from sentence_transformers import SentenceTransformer

class LibrarySearch:
    def __init__(self, index_path="faiss_index.pkl", data_path="book_data.pkl"):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")  # Lightweight embedding model

        # Load book data & FAISS index
        self.index_path = index_path
        self.data_path = data_path
        self.books = self.load_books()
        self.index = self.load_index()

    def load_books(self):
        """Load book titles and summaries from file."""
        try:
            with open(self.data_path, "rb") as f:
                return pickle.load(f)
        except FileNotFoundError:
            return []  # Empty if no data

    def load_index(self):
        """Load FAISS index from file."""
        try:
            with open(self.index_path, "rb") as f:
                return pickle.load(f)
        except FileNotFoundError:
            return faiss.IndexFlatL2(384)  # Create empty FAISS index (384-dim for MiniLM)

    def search_books(self, query, top_k=3):
        """Find the most relevant books based on user query."""
        if not self.books:
            return []

        # Encode query
        query_vector = self.model.encode([query]).astype("float32")

        # Search FAISS index
        distances, indices = self.index.search(query_vector, top_k)

        # Retrieve book titles and summaries
        results = [(self.books[idx]["title"], self.books[idx]["summary"]) for idx in indices[0]]
        return results

    def add_books(self, book_list):
        """Add new books to FAISS index and save them."""
        book_vectors = []
        for book in book_list:
            title, summary = book["title"], book["summary"]
            embedding = self.model.encode([summary]).astype("float32")

            # Store book info
            self.books.append({"title": title, "summary": summary})
            book_vectors.append(embedding)

        # Update FAISS index
        book_vectors = np.vstack(book_vectors)
        self.index.add(book_vectors)

        # Save updated data
        with open(self.data_path, "wb") as f:
            pickle.dump(self.books, f)
        with open(self.index_path, "wb") as f:
            pickle.dump(self.index, f)
