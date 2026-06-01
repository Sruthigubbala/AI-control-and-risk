import numpy as np

class MockVectorDB:
    """
    Simulates a production vector database instance (e.g., Pinecone or Milvus) 
    as outlined in Week 3 of the project timeline.
    """
    def __init__(self, embedding_dim=384):
        self.embedding_dim = embedding_dim
        self.vector_storage = {}
        self.metadata_storage = {}

    def insert_contract_segment(self, segment_id: str, embedding: np.ndarray, metadata: dict):
        """Stores a vector and its contextual metadata."""
        self.vector_storage[segment_id] = embedding
        self.metadata_storage[segment_id] = metadata

    def query_similarity(self, query_embedding: np.ndarray, top_k=2):
        """Performs a cosine similarity search comparison across stored vectors."""
        scores = []
        for seg_id, vec in self.vector_storage.items():
            # Simple cosine similarity calculation: (A dot B) / (||A|| * ||B||)
            dot_product = np.dot(query_embedding, vec)
            norm_a = np.linalg.norm(query_embedding)
            norm_b = np.linalg.norm(vec)
            similarity = dot_product / (norm_a * norm_b) if norm_a and norm_b else 0.0
            
            scores.append((seg_id, similarity, self.metadata_storage[seg_id]))
            
        # Sort descending by match score
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:top_k]

if __name__ == "__main__":
    print("Initializing Week 3 Contract Vector Search Database...")
    np.random.seed(101)
    
    # Initialize the store
    vdb = MockVectorDB(embedding_dim=6)
    
    # Insert mock contract elements
    vdb.insert_contract_segment(
        segment_id="chunk_1",
        embedding=np.array([0.1, 0.8, 0.9, 0.0, 0.1, 0.2], dtype=np.float32),
        metadata={"text": "Termination clause: Requires 30 days written notice.", "risk": "High"}
    )
    vdb.insert_contract_segment(
        segment_id="chunk_2",
        embedding=np.array([0.9, 0.1, 0.0, 0.8, 0.7, 0.9], dtype=np.float32),
        metadata={"text": "Governing Law: This agreement is governed by Delaware state code.", "risk": "Low"}
    )
    
    # Simulate an incoming search query vector matching closely with chunk_1
    simulated_search_query = np.array([0.15, 0.75, 0.85, 0.05, 0.1, 0.15], dtype=np.float32)
    
    print("\nExecuting semantic lookup query matching across contract repositories...")
    results = vdb.query_similarity(simulated_search_query, top_k=1)
    
    for seg_id, score, meta in results:
        print(f"\nMatch Found! ID: {seg_id} (Confidence Score: {score:.4f})")
        print(f"Extracted Text: {meta['text']}")
        print(f"Risk Classification Assessment: {meta['risk']}")