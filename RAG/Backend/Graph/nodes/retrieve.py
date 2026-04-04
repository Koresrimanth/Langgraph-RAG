from RAG.Backend.services.retrieval import retrieve_documents



def retrieve_node(state):

    query_map = state["query_map"]
    print("sending the query_map to retriever")
    docs = retrieve_documents(query_map)
    print("the number of docs retrieved",docs)
    return {
        "documents": docs,
        "retry_count": state.get("retry_count", 0) + 1
    }
