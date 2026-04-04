from langgraph.graph import StateGraph, END

from RAG.Backend.Graph.state import GraphState
from RAG.Backend.Graph.nodes.router import router
from RAG.Backend.Graph.nodes.retrieve import retrieve_node
from RAG.Backend.Graph.nodes.reranker import rerank_node
from RAG.Backend.Graph.nodes.answer import answer_node
from RAG.Backend.Graph.nodes.self_check import self_check_node


def build_graph():
    workflow=StateGraph(GraphState)

    #nodes
    workflow.add_node("router_node",router)
    workflow.add_node("retrieve_node",retrieve_node)
    workflow.add_node("rerank_node",rerank_node)
    workflow.add_node("answer_node",answer_node)
    
    #edges
    workflow.set_entry_point("router_node")
    #router->retrieve
    workflow.add_conditional_edges("router_node",
                                   lambda state:state["route"],
                                   {
                                       "GENERAL":"answer_node",
                                       "KNOWLEDGE": "retrieve_node"
                                   })
    

    #rerank if multi db answer

    workflow.add_conditional_edges(
        "retrieve_node",
        lambda state:"rerank_node" if state["use_rerank"] else "answer_node",
        {
            "rerank_node":"rerank_node",
            "answer_node":"answer_node"
        }
    )
    workflow.add_edge("rerank_node","answer_node")

    workflow.add_conditional_edges(
        "answer_node",self_check_node,{
            "end":END,
            "retry":"retrieve_node"
        }
    )

    graph=workflow.compile()
    
    return graph