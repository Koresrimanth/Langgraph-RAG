# from sentence_transformers import CrossEncoder

# # 1. Load a lightweight reranker model
# reranker_model = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')

# def rerank_results(original_query, retrieved_docs, top_n=5):
#     # 'retrieved_docs' is the list of dictionaries from your 'all_docs'
#     if not retrieved_docs:
#         return []

#     # 2. Prepare pairs: (Original User Query, Document Content)
#     # This ensures everything is ranked against the FULL intent
#     pairs = [[original_query, doc['content']] for doc in retrieved_docs]
    
#     # 3. Predict relevance scores
#     scores = reranker_model.predict(pairs)
    
#     # 4. Attach scores and sort
#     for i, score in enumerate(scores):
#         retrieved_docs[i]['rerank_score'] = float(score)
    
#     # Sort descending (highest score first)
#     reranked_docs = sorted(retrieved_docs, key=lambda x: x['rerank_score'], reverse=True)
    
#     return reranked_docs[:top_n]

# # --- Usage in your Test Script ---
# # all_docs = retrieve_documents("What are the metrics and logs for today?")
# # final_context = rerank_results("What are the metrics and logs for today?", all_docs)

from sentence_transformers import CrossEncoder
import numpy as np

# 
reranker_model = CrossEncoder(
    # 'cross-encoder/ms-marco-MiniLM-L-6-v2',
    'cross-encoder/ms-marco-TinyBERT-L-2-v2',
    device='cpu'   # change to 'cuda' if GPU
)


def rerank_results(query, docs, top_n=5):
    if not docs:
        return []

    # 🔥 limit docs BEFORE scoring
    docs = docs[:15]

    # prepare inputs
    pairs = [(query, d["content"]) for d in docs]

    # 🔥 batch prediction (faster)
    scores = reranker_model.predict(
        pairs,
        batch_size=8,
        show_progress_bar=True
    )

    # convert to numpy
    scores = np.array(scores)

    # sort indices
    top_indices = np.argsort(-scores)[:top_n]

    reranked = []
    for idx in top_indices:
        doc = docs[idx]
        doc["rerank_score"] = float(scores[idx])
        reranked.append(doc)

    return reranked
