import os

from src.vectorstore.hybrid_vector_store import HybridVectorStore
from src.loaders.pdf_loader import load_pdf
from src.loaders.txt_loader import load_txt
from src.config.settings import settings
from src.utils.text_cleaning import clear_text

def ingest_all_documents():
    store = HybridVectorStore(
        persist_path=settings.DATA_DB,
        embedding_model=settings.EMBEDDING_MODEL,
        chunk_size=settings.CHUNK_SIZE,
        chunk_overlap=settings.CHUNK_OVERLAP
    )

    for fname in os.listdir(settings.DATA_RAW):
        path = os.path.join(settings.DATA_RAW, fname)

        print(f"[INGEST] Loading: {path}")

        if fname.lower().endswith(".pdf"):
            text = load_pdf(path)
        else:
            text = load_txt(path)

        text = clear_text(text)

        chunks = store.splitter.split_text(text)
        store.add_chunks(path, chunks)

        print(f"[INGEST] Added {len(chunks)} chunks from {fname}")

    print("[INGEST] Complete.")
