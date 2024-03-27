import os
from data.pgvector import VectorDB

test_files = [os.path.normpath('./courses/HMG6228/Week 4/Emerging Legal Issues - Jan 2023.pptx')]

db = VectorDB()
num_docs = db.index_files(test_files)
print(num_docs)
