from RAG.Backend.retrievers.base_retriever import BaseRetriever
from RAG.Backend.config import CHROMA_DB_PATH, COLLECTION_NAMES


class DocsRetriever(BaseRetriever):
    def __init__(self):
        super().__init__(collection_name=COLLECTION_NAMES["docs"])