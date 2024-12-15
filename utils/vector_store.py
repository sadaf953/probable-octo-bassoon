import chromadb
from sentence_transformers import SentenceTransformer
import pandas as pd
import os

class MTechVectorStore:
    def __init__(self, data_source='mtech_programs.csv', collection_name="mtech_programs"):
        """Initializes vector store for M.Tech program data."""
        self.client = chromadb.Client()
        self.collection_name = collection_name
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
        self.data_source = data_source
        self.collection = self._load_or_create_collection()


    def _load_or_create_collection(self):
        """Loads the collection if it exists, creates it otherwise."""
        try:
            collection = self.client.get_collection(name=self.collection_name)
            print(f"Loaded existing collection: {self.collection_name}")
            return collection
        except Exception as e:
            print(f"Collection '{self.collection_name}' not found. Creating a new one.")
            self._create_embeddings() # Create embeddings if collection doesn't exist
            collection = self.client.get_collection(name=self.collection_name)
            return collection



    def _create_embeddings(self):
        """Creates vector embeddings and adds them to the collection."""
        try:
            self.data = pd.read_csv(self.data_source)
        except FileNotFoundError:
            raise FileNotFoundError(f"Data file not found at: {self.data_source}")

        embeddings = []
        documents = []
        ids = []

        for index, row in self.data.iterrows():
            text = f"{row['university']} {row['name']} {row['duration']}"  #Combine relevant text
            embedding = self.embedder.encode(text).tolist()
            embeddings.append(embedding)
            documents.append(text)
            ids.append(f"program_{index}")

        self.client.create_collection(name=self.collection_name)
        self.collection = self.client.get_collection(name=self.collection_name) #Get the collection
        self.collection.add(embeddings=embeddings, documents=documents, ids=ids)
        print(f"Embeddings created and added to collection: {self.collection_name}")

    def query_programs(self, query, top_k=5):
        """Queries vector store for similar M.Tech programs."""
        query_embedding = self.embedder.encode(query).tolist()
        results = self.collection.query(query_embeddings=[query_embedding], n_results=top_k)
        return results

#Remove the main function - it is only for testing
#This class is now ready to be used in your main application.
