from dotenv import load_dotenv
load_dotenv()

import os
OPENAI_API_KEY = os.environ['OPENAI_API_KEY']
PGVECTOR_HOST = os.environ['PGVECTOR_HOST']
PGVECTOR_PORT = os.environ['PGVECTOR_PORT']
PGVECTOR_USERNAME = os.environ['PGVECTOR_USERNAME']
PGVECTOR_PASSWORD = os.environ['PGVECTOR_PASSWORD']
PGVECTOR_DB = os.getenv('PGVECTOR_DB') or 'pgvector'
SERVER_HOST = os.getenv('SERVER_HOST') or '0.0.0.0'
SERVER_PORT = int(os.getenv('SERVER_PORT') or '80')
