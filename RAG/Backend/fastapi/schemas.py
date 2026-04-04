from pydantic import BaseModel
from typing import List,Any,Optional,Dict


class QueryRequest(BaseModel):
    query: str
    user_id: str
    session_id: str


class QueryResponse(BaseModel):
    query:str
    answer:str
    documents:List[dict]
    retry_count:int
