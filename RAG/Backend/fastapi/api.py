from fastapi import FastAPI,HTTPException
import time
import asyncio
from RAG.Backend.Graph.run_graph import run_langgraph
from RAG.Backend.fastapi.schemas import QueryRequest,QueryResponse
app=FastAPI()
from RAG.Backend.msg_db.msg_db_conn import save_message,get_last_message

@app.get("/")
def home():
    return {"message":"API is working"}

@app.post("/query",response_model=QueryResponse)
async def query_rag(request:QueryRequest):
    start_time=time.time()
    user_id = request.user_id
    session_id = request.session_id
    query = request.query
    try:
        history=get_last_message(user_id,session_id) or []
        loop=asyncio.get_event_loop()
        result=await loop.run_in_executor(
            None,
            run_langgraph,
            request.query,
            history
        )
        latency=round(time.time()-start_time,2)
        print("query time:",latency)
        
        save_message(user_id,session_id,"user",query)
        print("saved user query to postgres")
        save_message(user_id,session_id,"assistant",result.get("answer", ""))
        print("saved user Answer to postgres")
        return {
            "query": request.query,
            "answer": result.get("answer", ""),
            "documents": result.get("documents", []),
            "retry_count": result.get("retry_count", 0)
        }

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500,detail="Interal server error")

