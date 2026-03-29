from typing import TypedDict,List,Annotated,Dict
import operator

class GraphState(TypedDict):
    query:str
    answer:str
    documents:Annotated[List[dict],operator.add]
    use_rerank:bool
