import os
import chromadb
import google.generativeai as genai
from dotenv import load_dotenv
from RAG.Backend.config import get_chroma_client, GOOGLE_API_KEY

# 1. Configure Google AI
genai.configure(api_key=GOOGLE_API_KEY)

class BaseRetriever:
    def __init__(self, collection_name):
        
        self.client = get_chroma_client()
        
        self.collection = self.client.get_collection(name=collection_name)

    def get_embedding(self, text):
        """Helper to get vector from Google API"""
        response = genai.embed_content(
            model="models/gemini-embedding-2-preview", 
            content=text
        )
        return response["embedding"]

    def retrieve(self, query, k=5):
        # 1. Get the query vector using the native function
        query_vector = self.get_embedding(query)
        
        # 2. Query ChromaDB with that vector
        results = self.collection.query(
            query_embeddings=[query_vector],
            n_results=k
        )
        return results