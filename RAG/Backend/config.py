import os
from dotenv import load_dotenv
load_dotenv()
import os
import chromadb


GROQ_API_KEY=os.getenv('GROQ_API_KEY')
GOOGLE_API_KEY=os.getenv("GOOGLE_API_KEY")

CHROMA_DB_PATH = os.path.join(os.getcwd(), "my_local_db")

MODEL_NAME="llama-3.3-70b-versatile"

COLLECTION_NAMES = {
    "logs": "logs_collection",
    "docs": "docs_collection",
    "metrics": "metrics_collection",
    "alerts": "alerts_collection",
}


def get_chroma_client():
    return chromadb.PersistentClient(path=CHROMA_DB_PATH)
