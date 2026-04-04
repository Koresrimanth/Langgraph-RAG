# from RAG.Backend.services.llm_service import call_llm


# def format_history(history):
#     formatted = []

#     for msg in history:
#         if msg["role"] == "user":
#             formatted.append(f"User: {msg['content']}")
#         elif msg["role"] == "assistant":
#             formatted.append(f"Assistant: {msg['content']}")

#     return "\n".join(formatted)

# def answer_node(state):
#     query = state["query"]
#     docs = state["documents"]
#     history = state.get("history", [])   
    
#     if not docs:
#         print("[Answer] No documents found")
#         return {
#             "answer": "I could not find enough information to answer your question."
#         }

#     # =========================
#     # 🔥 Limit context size (VERY IMPORTANT)
#     # =========================
#     # docs = docs[:5]  # keep top 5 only

#     # =========================
#     # 🧠 Build structured context
#     # =========================
#     context_parts = []
#     history_text = format_history(history)

#     for i, d in enumerate(docs):
#         source = d.get("db_source", "unknown")
#         content = d.get("content", "")

#         context_parts.append(
#             f"[Source: {source}] {content}"
#         )

#     context = "\n\n".join(context_parts)

#     # =========================
#     # 🧠 Prompt Engineering (VERY IMPORTANT)
#     # =========================
#     prompt = f"""
#     You are an expert system analyzer.

#     Use ONLY the provided context to answer the question.

#     Conversation History:
#     {history_text}
#     Context:
#     {context}

#     Question:
#     {query}

#     Instructions:
#     - Give a clear and concise answer
#     - If multiple sources are present, combine insights
#     - If root cause exists, mention it clearly
#     - Do NOT hallucinate
#     - If answer not found, say "Not enough information"

#     Answer:
#     """

#     # =========================
#     # 🤖 Call LLM
#     # =========================
#     answer = call_llm(prompt)

#     print("[Answer] Generated successfully")

#     return {
#         "answer": answer
#     }

from RAG.Backend.services.llm_service import call_llm


def format_history(history):
    if not history:
        return "No previous conversation."

    formatted = []
    # Take the last 5 to keep the prompt clean
    for msg in history[-5:]:
        # Use .lower() to ensure it matches regardless of how it's stored in DB
        role = msg.get("role", "").lower()
        content = msg.get("content", "")

        if role == "user":
            formatted.append(f"User: {content}")
        elif role in ["assistant", "bot"]:
            formatted.append(f"Assistant: {content}")

    return "\n".join(formatted)


def answer_node(state):
    query = state["query"]
    docs = state.get("documents", [])
    history = state.get("history", [])
    route = state.get("route", "KNOWLEDGE")

    history_text = format_history(history)
    print("the history we got from the postgres is",history_text)
    
    if route == "GENERAL":
        print("[Answer] General query → LLM only")

        prompt = f"""
        You are a helpful assistant.

        Conversation History:
        {history_text}

        Question:
        {query}

        Instructions:
        - Use conversation history if relevant
        - Answer naturally

        Answer:
        """

        answer = call_llm(prompt)
        print("The answer from the llm is",answer)
        return {"answer": answer,
                "retry_count": 0}

    
    if not docs:
        print("[Answer] No documents found")
        return {
            "answer": "I could not find enough information to answer your question."
        }

    context_parts = []

    for d in docs:
        source = d.get("db_source", "unknown")
        content = d.get("content", "")

        context_parts.append(f"[Source: {source}] {content}")

    context = "\n\n".join(context_parts)

    prompt = f"""
    You are an expert system analyzer.

    Use ONLY the provided context to answer the question.

    Conversation History:
    {history_text}

    Context:
    {context}

    Question:
    {query}

    Instructions:
    - Give a clear and concise answer
    - Combine insights if multiple sources
    - Do NOT hallucinate
    - If answer not found, say "Not enough information"

    Answer:
    """

    answer = call_llm(prompt)

    print("[Answer] Generated successfully")

    return {
        "answer": answer
    }