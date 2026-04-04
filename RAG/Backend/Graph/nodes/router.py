from RAG.Backend.services.retrieval import  decompose_query
from RAG.Backend.config import COLLECTION_NAMES

# def router(state):
#     query=state['query']
#     query_map=decompose_query(query)
#     if not query_map:
#         query_map={src:query for src in COLLECTION_NAMES}
#     use_rerank=len(query_map.keys())>1
#     print("Router output",query_map,"| use rerank",use_rerank)
#     return {
#         "query_map":query_map,
#         "use_rerank":use_rerank
#     }

from RAG.Backend.services.retrieval import decompose_query
from RAG.Backend.config import COLLECTION_NAMES
from RAG.Backend.services.llm_service import call_llm   # adjust if needed

def router(state):
    query = state["query"]

    
    prompt = f"""
    Classify the query:

    GENERAL → greetings, casual talk, personal info
    KNOWLEDGE → needs document retrieval

    Query: {query}

    Answer only: GENERAL or KNOWLEDGE
    """

    response = call_llm(prompt)
    route = response.strip().upper()

    #  If GENERAL → skip retrieval
    if route == "GENERAL":
        return {
            "route": "GENERAL",
            "query_map": {},
            "use_rerank": False
        }

    #  Existing logic (for RAG)
    query_map = decompose_query(query)
    print("the query map for this question is ",query_map)
    print(" ****** ")
    if not query_map:
        query_map = {src: query for src in COLLECTION_NAMES}

    use_rerank = len(query_map.keys()) > 1

    return {
        "route": "KNOWLEDGE",
        "query_map": query_map,
        "use_rerank": use_rerank
    }


