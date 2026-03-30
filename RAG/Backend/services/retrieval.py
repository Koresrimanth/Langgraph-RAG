import json
from RAG.Backend.services.llm_service import call_llm

from RAG.Backend.retrievers.log_retriever import LogsRetriever
from RAG.Backend.retrievers.alerts_retriever import AlertsRetriever
from RAG.Backend.retrievers.docs_retriever import DocsRetriever
from RAG.Backend.retrievers.metrics_retriever import MetricsRetriever

retrievers = {
    "logs": LogsRetriever(),
    "docs": DocsRetriever(),
    "metrics": MetricsRetriever(),
    "alerts": AlertsRetriever(),
}




import json
import re

# def decompose_query(query: str):
#     # System prompt to force strictly JSON output
#     prompt = f"""
#     You are a query router. Task: Break the user query into sub-queries for specific databases.
#     Databases: [logs, docs, metrics, alerts]

#     RULES:
#     1. Output ONLY a valid JSON object.
#     2. No preamble, no explanation, no markdown backticks.
#     3. Use only the relevant keys from the database list.
#     4. If a database is not needed, do not include it.

#     User Query: "{query}"

#     Correct Output Example:
#     {{"metrics": "CPU and memory usage", "logs": "error messages"}}
#     """

#     response = call_llm(prompt)

#     try:
#         # Regex to find the JSON block if the LLM added conversational text
#         match = re.search(r'\{.*\}', response, re.DOTALL)
#         if match:
#             clean_json = match.group(0)
#             return json.loads(clean_json)
#         return {}
#     except Exception as e:
#         print(f"⚠️ JSON Parsing Error: {e} | Raw Response: {response}")
#         return {}
import re
import json

def decompose_query(query: str):
    # 1. Be very strict in the prompt
    prompt = f"""
    You are a query router. Decompose the user query into sub-queries for specific databases for the user question.
    Databases: [logs, docs, metrics, alerts]

    RULES:
    - Output ONLY a raw JSON object. 
    - NO preamble, NO explanation, NO markdown code blocks.
    - If a database is not needed, do not include it.

    User Query: "{query}"

    Example Output:
    {{"metrics": "system performance metrics", "logs": "error logs"}}
    """

    response = call_llm(prompt)
    print(response)
    try:
        # 2. Extract ONLY the JSON part using Regex (removes text before/after)
        match = re.search(r'\{.*\}', response, re.DOTALL)
        if match:
            clean_json = match.group(0)
            return json.loads(clean_json)
        return {}
    except Exception as e:
        print(f"Error parsing JSON. Raw response was: {response}")
        return {}


# def retrieve_documents(query: str):
#     all_docs = []

#     # 🔥 Step 1: Decompose using your LLM function
#     query_map = decompose_query(query)
#     # print(f"the decomposition output is {query_map}")
#     # Fallback if LLM fails to return JSON
#     if not query_map:
#         query_map = {"docs": query} 

#     # 🔥 Step 2: Retrieve per DB
#     for db_name, sub_query in query_map.items():
#         if db_name not in retrievers or not sub_query:
#             continue

#         # Get dictionary from your Native Chroma retriever
#         results = retrievers[db_name].retrieve(sub_query, k=3)
#         # print(f"The retrieved documents from {db_name}")
#         # print(results)
#         # Process the dictionary lists (documents, metadatas, ids)
#         if results['documents']:
#             for i in range(len(results['documents'])):
#                 # Create a simple structure for your final LLM prompt
#                 doc_entry = {
#                     "content": results['documents'][i],
#                     "metadata": results['metadatas'][i],
#                     "db_source": db_name,
#                     "original_sub_query": sub_query
#                 }
#                 all_docs.append(doc_entry)
#     print("thi is is th eall docs*************************************************8")
#     print(all_docs)
#     return all_docs



# def retrieve_documents(query: str):
#     all_docs = []
#     query_map = decompose_query(query)

#     for db_name, sub_query in query_map.items():
#         if db_name not in retrievers: continue
#         results = retrievers[db_name].retrieve(sub_query, k=3)

#         # Chroma returns lists of lists: [['doc1', 'doc2']]
#         if results['documents'] and len(results['documents']) > 0:
#             # results['documents'][0] is the actual list of strings
#             docs_list = results['documents'][0] 
#             meta_list = results['metadatas'][0]

#             for i in range(len(docs_list)):
#                 all_docs.append({
#                     "content": docs_list[i],  # Now this is a single string, not a list
#                     "metadata": meta_list[i],
#                     "db_source": db_name
#                 })
#     return all_docs

# def retrieve_documents(query_map: dict):
#     """
#     Retrieve documents using precomputed query_map
#     Example:
#     {
#         "metrics": "CPU usage",
#         "logs": "error logs"
#     }
#     """

#     all_docs = []

#     # safety fallback
#     if not query_map:
#         print("[Retrieve] Empty query_map, skipping retrieval")
#         return all_docs

#     for db_name, sub_query in query_map.items():

#         if db_name not in retrievers:
#             print(f"[Retrieve] Skipping unknown DB: {db_name}")
#             continue

#         if not sub_query:
#             continue

#         results = retrievers[db_name].retrieve(sub_query, k=3)

#         # Handle Chroma output
#         if results.get("documents") and len(results["documents"]) > 0:

#             docs_list = results["documents"][0]
#             meta_list = results["metadatas"][0]

#             for i in range(len(docs_list)):
#                 all_docs.append({
#                     "content": docs_list[i],
#                     "metadata": meta_list[i],
#                     "db_source": db_name,
#                     "sub_query": sub_query
#                 })

#     print(f"[Retrieve] Total docs: {len(all_docs)}")

#     return all_docs

def retrieve_documents(query_map: dict):
    all_docs = []

    for db_name, sub_query in query_map.items():

        if db_name not in retrievers:
            continue

        results = retrievers[db_name].retrieve(sub_query, k=3)

        # ✅ FIX: flatten properly
        if results.get("documents") and len(results["documents"]) > 0:

            docs_list = results["documents"][0]
            meta_list = results["metadatas"][0]

            for i in range(len(docs_list)):
                all_docs.append({
                    "content": docs_list[i],   # ✅ string
                    "metadata": meta_list[i],
                    "db_source": db_name,
                    "sub_query": sub_query
                })

    print(f"[Retrieve] Total docs: {len(all_docs)}")

    return all_docs