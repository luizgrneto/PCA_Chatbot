import uuid
import numpy as np
import chromadb

from sentence_transformers import SentenceTransformer
from rank_bm25 import BM25Okapi
from langchain_text_splitters import RecursiveCharacterTextSplitter


class HybridVectorStore:
    def __init__(
        self,
        persist_path="data/db",
        embedding_model="all-MiniLM-L6-v2",
        chunk_size=800,
        chunk_overlap=150
    ):
        self.client = chromadb.PersistentClient(path=persist_path)

        self.semantic = self.client.get_or_create_collection(
            name="semantic_store",
            metadata={"hnsw:space": "cosine"}
        )

        self.lexical = self.client.get_or_create_collection(
            name="lexical_store"
        )

        self.embedder = SentenceTransformer(embedding_model)

        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", ".", "!", "?", " ", ""]
        )

    # ---------------- LOADERS PROVIDED BY PIPELINE ---------------- #

    def add_chunks(self, path, chunks):
        """Add pre-chunked text to the store."""
        for i, chunk in enumerate(chunks):
            chunk_id = f"{path}-{i}-{uuid.uuid4().hex}"

            embedding = self.embedder.encode([chunk])[0]

            self.semantic.add(
                ids=[chunk_id],
                embeddings=[embedding],
                metadatas=[{"source": path}],
                documents=[chunk]
            )

            self.lexical.add(
                ids=[chunk_id],
                metadatas=[{"source": path}],
                documents=[chunk]
            )

    # ---------------- HYBRID SEARCH ---------------- #

    def _bm25_rank(self, query, docs):
        tokenized = [d.split() for d in docs]
        bm25 = BM25Okapi(tokenized)
        return bm25.get_scores(query.split())

    def hybrid_search(self, query, top_k=5, w_sem=0.55, w_lex=0.45):
        q_emb = self.embedder.encode([query])[0]

        sem = self.semantic.query(
            query_embeddings=[q_emb],
            n_results=top_k
        )

        ids = sem["ids"][0]
        docs = sem["documents"][0]
        distances = sem["distances"][0]

        lex_docs = self.lexical.get(ids=ids)["documents"]
        bm25_scores = self._bm25_rank(query, lex_docs)

        sem_norm = 1 - np.array(distances)
        lex_norm = (bm25_scores - np.min(bm25_scores)) / (np.ptp(bm25_scores) + 1e-6)

        final = w_sem * sem_norm + w_lex * lex_norm

        ranked = list(zip(ids, lex_docs, final))
        ranked.sort(key=lambda x: x[2], reverse=True)
        return ranked[:top_k]
