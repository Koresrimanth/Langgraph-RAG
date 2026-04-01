from typing import TypedDict,List,Annotated,Dict
from typing import List,Any,Optional,Dict
import operator



class GraphState(TypedDict):
    query: str
    query_map: Dict[str, str]
    route: str
    history: List[Dict[str, Any]]
    documents: List
    answer: str
    use_rerank: bool
    retry_count: int