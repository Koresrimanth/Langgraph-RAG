
from RAG.Backend.services.reranker import rerank_results
def rerank_node(state):
    docs = state["documents"]

    # skip if small
    if not state["use_rerank"] or len(docs) <= 5:
        print("[Rerank] Skipped")
        return state

    print("[Rerank] Running optimized reranker...")

    ranked_docs = rerank_results(state["query"], docs)

    return {"documents": ranked_docs}