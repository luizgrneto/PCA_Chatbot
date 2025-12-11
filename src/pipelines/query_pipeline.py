from src.vectorstore.hybrid_vector_store import HybridVectorStore
from src.config.settings import settings


def run_query(query: str, top_k=5):
    store = HybridVectorStore(
        persist_path=settings.DATA_DB,
        embedding_model=settings.EMBEDDING_MODEL
    )
    return store.hybrid_search(query, top_k=top_k)
