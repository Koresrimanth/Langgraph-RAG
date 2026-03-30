from typing import TypedDict,List,Annotated,Dict
import operator



class GraphState(TypedDict):
    query: str
    query_map: Dict[str, str]
    documents: List
    answer: str
    use_rerank: bool
    retry_count: int