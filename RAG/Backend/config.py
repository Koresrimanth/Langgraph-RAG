import os
from dotenv import load_dotenv
load_dotenv()
import os
import chromadb
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


GROQ_API_KEY=os.getenv('GROQ_API_KEY')
GOOGLE_API_KEY=os.getenv("GOOGLE_API_KEY")
host=os.getenv('host')
database=os.getenv('database')
password=os.getenv('password')
port=os.getenv("port")
user=os.getenv("user")

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




DATABASE_URL = f"postgresql://{user}:{password}@localhost:5432/postgres"
engine = create_engine(
    DATABASE_URL,
    pool_size=20,
    max_overflow=10
)

SessionLocal = sessionmaker(bind=engine)

