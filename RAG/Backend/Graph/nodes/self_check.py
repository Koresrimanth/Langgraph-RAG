from RAG.Backend.services.llm_service import call_llm


def self_check_node(state):
    query = state["query"]
    answer = state["answer"]
    retry_count = state.get("retry_count", 0)

    print(f"[SelfCheck] retry_count = {retry_count}")

    if retry_count >= 2:
        print("[SelfCheck] Max retries reached")
        return "end"

    prompt = f"""
    Question: {query}
    Answer: {answer}

    Is this answer correct and complete?

    Answer only YES or NO.
    """

    decision = call_llm(prompt)

    if "YES" in decision.upper():
        print("[SelfCheck] Answer accepted")
        return "end"
    else:
        print("[SelfCheck] Answer rejected → retrying")
        return "retry"