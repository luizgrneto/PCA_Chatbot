import os

class Settings:
    DATA_RAW = "data/raw"
    DATA_DB = "app/vectorstore/db"
    CHUNK_SIZE = 1000
    CHUNK_OVERLAP = 200
    EMBEDDING_MODEL = "all-MiniLM-L6-v2"

settings = Settings()
