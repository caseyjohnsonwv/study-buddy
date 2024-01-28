import glob
import os
import re
from typing import List, Tuple
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.docstore.document import Document
from langchain_community.vectorstores.faiss import FAISS
from langchain_openai import OpenAIEmbeddings
from pptx import Presentation
import env

class VectorDB:
    course_name = None
    _course_path = None
    _embeddings = None
    _vectorstore = None

    def __init__(self, course_name:str, force_recreate:bool=False) -> None:
        self.course_name = course_name
        self._course_path = os.path.normpath(os.path.join('courses', course_name.strip().upper()))
        self._embeddings = OpenAIEmbeddings(model='text-embedding-ada-002', api_key=env.OPENAI_API_KEY, organization=env.OPENAI_ORG_ID)
        # try to load from existing file
        if os.path.exists(os.path.join(self._course_path, 'index.faiss')) and not force_recreate:
            print(f"Loading existing index from {self._course_path}")
            self._vectorstore = FAISS.load_local(self._course_path, self._embeddings, index_name='index')
        else:
            print(f"Generating new embeddings from {self._course_path}")
            # otherwise, crawl course materials directory
            pptx_glob_expr = os.path.normpath(os.path.join(self._course_path, '*', '*.pptx'))
            pptx_docs = self._load_pptx_docs(pptx_glob_expr)
            # then create vectorstore from loaded documents
            self._vectorstore = FAISS.from_documents(pptx_docs, self._embeddings)
            self._vectorstore.save_local(self._course_path, index_name='index')
        
    def _load_pptx_docs(self, pptx_glob_expr:str) -> List[Document]:
        documents = []
        # load documents from pptx files
        for f in glob.glob(pptx_glob_expr):
            prs = Presentation(f)
            filename, directory = os.path.basename(f), os.path.dirname(f)
            for n,slide in enumerate(prs.slides):
                slide_texts = []
                # get all text from the slides themselves
                for shape in slide.shapes:
                    if hasattr(shape, 'text'):
                        slide_text_cleaned = re.sub('\s+', ' ', shape.text)
                        slide_texts.append(slide_text_cleaned)
                # also grab presenter's notes if available
                slide_notes = slide.notes_slide.notes_text_frame.text
                slide_notes_cleaned = re.sub('\s+', ' ', slide_notes)
                slide_texts.append(slide_notes_cleaned)
                full_slide_text = ' '.join(slide_texts)
                # convert slide to document for embedding
                slide_document = Document(page_content=full_slide_text, metadata={'filename':filename, 'directory':directory, 'slide_number':n+1})
                documents.append(slide_document)
        # split documents with text splitter
        text_splitter = RecursiveCharacterTextSplitter(separators=['\s+'], is_separator_regex=True, keep_separator=True, chunk_size=500, chunk_overlap=0)
        docs = text_splitter.split_documents(documents)
        # return list of documents ready for embedding
        return docs    

    def search(self, phrase:str, k:int=5, metadata_filter:dict={}) -> List[Tuple[Document, float]]:
        return self._vectorstore.similarity_search_with_score(phrase, k=k, filter=metadata_filter)
