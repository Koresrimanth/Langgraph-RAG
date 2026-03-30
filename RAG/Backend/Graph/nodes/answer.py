from RAG.Backend.services.llm_service import call_llm


def answer_node(state):
    query = state["query"]
    docs = state["documents"]

    # =========================
    # ⚠️ Safety: handle empty docs
    # =========================
    if not docs:
        print("[Answer] No documents found")
        return {
            "answer": "I could not find enough information to answer your question."
        }

    # =========================
    # 🔥 Limit context size (VERY IMPORTANT)
    # =========================
    # docs = docs[:5]  # keep top 5 only

    # =========================
    # 🧠 Build structured context
    # =========================
    context_parts = []

    for i, d in enumerate(docs):
        source = d.get("db_source", "unknown")
        content = d.get("content", "")

        context_parts.append(
            f"[Source: {source}] {content}"
        )

    context = "\n\n".join(context_parts)

    # =========================
    # 🧠 Prompt Engineering (VERY IMPORTANT)
    # =========================
    prompt = f"""
    You are an expert system analyzer.

    Use ONLY the provided context to answer the question.

    Context:
    {context}

    Question:
    {query}

    Instructions:
    - Give a clear and concise answer
    - If multiple sources are present, combine insights
    - If root cause exists, mention it clearly
    - Do NOT hallucinate
    - If answer not found, say "Not enough information"

    Answer:
    """

    # =========================
    # 🤖 Call LLM
    # =========================
    answer = call_llm(prompt)

    print("[Answer] Generated successfully")

    return {
        "answer": answer
    }