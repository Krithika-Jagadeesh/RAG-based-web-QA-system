import numpy as np

def retrieve_top_k(query, index, chunks, model, k=3):
    query_vec = model.encode([query])
    _, indices = index.search(np.array(query_vec), k)
    return [chunks[i] for i in indices[0]]