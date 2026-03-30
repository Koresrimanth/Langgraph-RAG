from RAG.Backend.Graph.build_graph import build_graph

graph=build_graph()

def run_langgraph(query:str):
    result=graph.invoke({
        "query":query,
        "query_map":{},
        "documents":[],
        "answer":"",
        "use_rerank":False,
        "retry_count":0
    })
    return result