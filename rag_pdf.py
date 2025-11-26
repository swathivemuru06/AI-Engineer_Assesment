# src/rag_pdf.py
from typing import List
from pypdf import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from llm import get_openai_embeddings
import os
from config import settings

class PDFRAG:
    def __init__(self, index_path: str = settings.FAISS_INDEX_PATH, persist: bool = settings.PERSIST_FAISS):
        self.emb = get_openai_embeddings()
        self.index_path = index_path
        self.persist = persist
        self.store = None
        # try load if present
        if persist and os.path.exists(index_path):
            try:
                self.store = FAISS.load_local(index_path, self.emb)
            except Exception:
                self.store = None

    def ingest_pdf(self, pdf_path: str, chunk_size: int = 1000, chunk_overlap: int = 200) -> int:
        reader = PdfReader(pdf_path)
        full_text = []
        for page in reader.pages:
            text = page.extract_text() or ""
            if text.strip():
                full_text.append(text)
        joined = "\n\n".join(full_text)
        splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        docs = splitter.split_text(joined)
        if not docs:
            return 0
        # create FAISS from texts
        self.store = FAISS.from_texts(docs, self.emb)
        if self.persist:
            self.store.save_local(self.index_path)
        return len(docs)

    def query(self, q: str, k: int = 4) -> List[str]:
        if not self.store:
            return []
        docs_and_scores = self.store.similarity_search_with_score(q, k=k)
        # return only text parts (first element of tuple is Document)
        results = [doc.page_content for doc, score in docs_and_scores]
        return results
