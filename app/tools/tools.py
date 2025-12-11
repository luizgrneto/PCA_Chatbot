from datetime import datetime

from src.vectorstore.hybrid_vector_store import HybridVectorStore
from src.config.settings import settings


def get_current_date() -> dict:
    """
    Get the current date in the format YYYY-MM-DD
    """
    return {"current_date": datetime.now().strftime("%Y-%m-%d")}

def get_context_from_rag(question: str) -> str:
    """Recupera documentos importantes em forma de contexto, baseado em uma pergunta."""

    store = HybridVectorStore(
        persist_path=settings.DATA_DB,
        embedding_model=settings.EMBEDDING_MODEL
        )

    docs = store.hybrid_search(question, top_k=5)
    context = "\n\n".join([d[1] for d in docs])

    return context
