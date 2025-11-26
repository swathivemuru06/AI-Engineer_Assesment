# src/tests/test_rag_pdf.py
import pytest
from rag_pdf import PDFRAG
import os
from fpdf import FPDF
from config import settings

def test_ingest_and_query(tmp_path):
    # create tiny PDF
    p = tmp_path / "t.pdf"
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Hello from test PDF about LangChain and FAISS.", ln=True)
    pdf.output(str(p))

    rag = PDFRAG(persist=False)
    count = rag.ingest_pdf(str(p))
    assert count >= 1
    res = rag.query("LangChain")
    assert any("LangChain" in r or "langchain" in r.lower() for r in res)
