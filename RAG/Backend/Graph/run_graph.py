from RAG.Backend.Graph.build_graph import build_graph

graph=build_graph()



def run_langgraph(query: str, history: list = []):
    result = graph.invoke({
        "query": query,
        "history": history,   
        "query_map": {},
        "documents": [],
        "answer": "",
        "use_rerank": False,
        "retry_count": 0
    })
    return result