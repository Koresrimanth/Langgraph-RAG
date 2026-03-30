from RAG.Backend.services.retrieval import  decompose_query
from RAG.Backend.config import COLLECTION_NAMES

def router(state):
    query=state['query']
    query_map=decompose_query(query)
    if not query_map:
        query_map={src:query for src in COLLECTION_NAMES}
    use_rerank=len(query_map.keys())>1
    print("Router output",query_map,"| use rerank",use_rerank)
    return {
        "query_map":query_map,
        "use_rerank":use_rerank
    }
