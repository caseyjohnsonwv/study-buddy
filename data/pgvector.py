from contextlib import contextmanager
from typing import Dict, List, Generator
from langchain_community.vectorstores.pgvector import PGVector
from langchain_openai import OpenAIEmbeddings
import psycopg2
import env
from .loaders import FileLoader, FileLoaderPptx


class VectorDB:
    _embedding_function = OpenAIEmbeddings(model='text-embedding-3-small', api_key=env.OPENAI_API_KEY)
    _conn_kwargs = {
        'host' : env.PGVECTOR_HOST,
        'port' : env.PGVECTOR_PORT,
        'user' : env.PGVECTOR_USERNAME,
        'password' : env.PGVECTOR_PASSWORD,
        'database' : env.PGVECTOR_DB,
    }
    _filetype_classes:Dict[str, FileLoader] = {
        'pptx' : FileLoaderPptx,
    }

    @contextmanager
    def connect(collection_name:str='default') -> Generator[psycopg2.extensions.connection, psycopg2.extensions.cursor, PGVector]:
        conn = psycopg2.connect(**VectorDB._conn_kwargs)
        cursor = conn.cursor()
        store = PGVector(
            connection_string = PGVector.connection_string_from_db_params(
                driver = 'psycopg2',
                **VectorDB._conn_kwargs,
            ),
            embedding_function=VectorDB._embedding_function,
            collection_name=collection_name
        )
        try:
            yield (conn, cursor, store)
        finally:
            conn.close()

    def index_files(course_name:str, filepaths:List[str]) -> int:
        final_split_documents = []
        for filepath in filepaths:
            filetype = filepath.split('.')[-1].lower()
            handler = VectorDB._filetype_classes[filetype]
            split_documents = handler.load_and_split(filepath)
            final_split_documents.extend(split_documents)
        with VectorDB.connect(course_name) as (conn, cursor, store):
            store.add_documents(final_split_documents)
        return len(final_split_documents)
