CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS embeddings (
  id SERIAL PRIMARY KEY,
  embedding vector,
  metadata JSON,
  created_at TIMESTAMPTZ DEFAULT NOW()
);
