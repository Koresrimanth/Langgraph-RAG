from RAG.Backend.services.retrieval import retrieve_documents



def retrieve_node(state):

    query_map = state["query_map"]

    docs = retrieve_documents(query_map)

    return {
        "documents": docs,
        "retry_count": state.get("retry_count", 0) + 1
    }
