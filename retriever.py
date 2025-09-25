# retriever.py
from sentence_transformers import SentenceTransformer
import faiss
import pickle
from rank_bm25 import BM25Okapi
from pathlib import Path
import numpy as np

INDEX_DIR = Path("vectorstore")
EMBED_MODEL = "all-MiniLM-L6-v2"

class Retriever:
    def __init__(self):
        # load FAISS index and metadata
        self.index = faiss.read_index(str(INDEX_DIR/"faiss.index"))
        with open(INDEX_DIR/"meta.pkl","rb") as f:
            self.meta = pickle.load(f)
        # embedding model for query embeddings
        self.emb = SentenceTransformer(EMBED_MODEL)

        # prepare BM25 over full corpus (list of token lists)
        corpus = [m['text'].split() for m in self.meta]
        self.bm25 = BM25Okapi(corpus)

    def _normalize(self, arr):
        arr = np.array(arr, dtype=float)
        if arr.size == 0:
            return arr
        minv = arr.min()
        maxv = arr.max()
        if maxv - minv > 0:
            return (arr - minv) / (maxv - minv)
        return np.zeros_like(arr)

    def retrieve(self, query, top_k=5, rerank_topk=10, alpha=0.6):
        """
        Retrieve documents using FAISS, then re-rank candidates with BM25.
        - query: user query string
        - top_k: final number of results to return
        - rerank_topk: number of FAISS candidates to consider for re-ranking
        - alpha: weight for FAISS (semantic) in combined score (0..1)
        Returns: list of meta dicts (same structure as self.meta) with optional 'combined_score'
        """
        # 1) encode query and FAISS search
        q_emb = self.emb.encode([query], convert_to_numpy=True)
        D, I = self.index.search(q_emb, rerank_topk)  # D: distances, I: indices
        distances = D[0] if len(D) > 0 else np.array([])
        indices = I[0] if len(I) > 0 else np.array([])

        # collect valid candidates (keep original index mapping)
        candidates = []
        faiss_scores = []
        candidate_indices = []
        for dist, idx in zip(distances, indices):
            if idx < len(self.meta):
                candidate_indices.append(idx)
                # convert L2 distance to a similarity-like score (higher = better)
                faiss_scores.append(1.0 / (1.0 + float(dist)))
                candidates.append(self.meta[idx])

        if not candidates:
            return []

        # 2) BM25 scores for the full corpus, then pick scores for candidate indices
        q_tokens = query.split()
        bm25_all_scores = self.bm25.get_scores(q_tokens)  # array length == len(self.meta)
        bm25_scores = np.array([float(bm25_all_scores[idx]) for idx in candidate_indices], dtype=float)

        # 3) Normalize both score arrays to [0,1]
        n_faiss = self._normalize(np.array(faiss_scores))
        n_bm25 = self._normalize(bm25_scores)

        # 4) Combine scores
        combined = alpha * n_faiss + (1.0 - alpha) * n_bm25

        # 5) Sort candidates by combined score descending
        order = np.argsort(-combined)
        reranked = []
        for i in order[:top_k]:
            hit = candidates[i].copy()
            hit['combined_score'] = float(combined[i])
            # optional debug fields (remove if you want)
            hit['_faiss_score'] = float(faiss_scores[i])
            hit['_bm25_score'] = float(bm25_scores[i])
            reranked.append(hit)

        return reranked
