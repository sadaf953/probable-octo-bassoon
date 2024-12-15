import chromadb
from sentence_transformers import SentenceTransformer
import pandas as pd

class MTechVectorStore:
    def __init__(self, data_source='mtech_programs.csv'):
        """
        Initialize vector store for M.Tech program data
        
        Args:
            data_source (str): Path to CSV file with program data
        """
        self.client = chromadb.Client()
        self.collection = self.client.create_collection("mtech_programs")
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
        self.data = pd.read_csv(data_source)

    def create_embeddings(self):
        """
        Create vector embeddings for program descriptions
        """
        for index, row in self.data.iterrows():
            # Combine relevant text for embedding
            text = f"{row['university']} {row['name']} {row['duration']}"
            
            # Generate embedding
            embedding = self.embedder.encode(text).tolist()
            
            # Add to Chroma vector store
            self.collection.add(
                embeddings=[embedding],
                documents=[text],
                ids=[f"program_{index}"]
            )

    def query_programs(self, query, top_k=5):
        """
        Query vector store for similar M.Tech programs
        
        Args:
            query (str): Search query
            top_k (int): Number of results to return
        
        Returns:
            List of matching programs
        """
        query_embedding = self.embedder.encode(query).tolist()
        
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )
        
        return results

def main():
    # Initialize vector store
    vector_store = MTechVectorStore()
    
    # Create embeddings
    vector_store.create_embeddings()
    
    # Example query
    query = "AI and Machine Learning specialization"
    results = vector_store.query_programs(query)
    
    print("Top matching programs:")
    for result in results['documents'][0]:
        print(result)

if __name__ == "__main__":
    main()
