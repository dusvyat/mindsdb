import os
import chromadb

from chromadb import Settings

check_path_exists = lambda path: os.makedirs(path, exist_ok=True)


def load_chroma(chroma_settings):
    client = chromadb.Client(chroma_settings)
    return client


def get_chroma_settings(persist_directory):
    return Settings(
        chroma_db_impl="duckdb+parquet",
        persist_directory=persist_directory,
        anonymized_telemetry=False,
    )


def get_retriever(persist_directory):
    chroma_settings = get_chroma_settings(persist_directory)
    db = load_chroma(chroma_settings)
    retriever = db.as_retriever()
    return retriever