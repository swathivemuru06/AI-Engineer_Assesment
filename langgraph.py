# src/langgraph_pipeline.py
from llm import answer_with_context
from weather_app import fetch_weather_by_city, WeatherError
import re 
from rag_pdf import PDFRAG





# single PDFRAG instance (in-memory)
_rag_pdf = PDFRAG()
_rag_pdf.ingest_pdf("rag_doc.pdf")   # <-- add this line

def ingest_pdf(path: str) -> int:
    return _rag_pdf.ingest_pdf(path)

def decision_and_run(user_input: str) -> dict:
    """Decide if user asks weather or PDF question."""
    s = user_input.lower().strip()
    # simple heuristic for weather
    if any(tok in s for tok in ("weather", "temperature", "forecast", "rain", "sunny", "wind")):
        # try to extract "in <city>"
        m = re.search(r"in\s+([a-zA-Z\s]+)$", s)
        city = m.group(1).strip() if m else "London"
        try:
            w = fetch_weather_by_city(city)
            text = f"Current weather in {w['city']}: {w['temp']}°C, {w['weather']}. Humidity {w['humidity']}%."
            reply = answer_with_context(text, "Summarize this in a 1-2 line user-friendly message.")
            return {"mode": "weather", "response": reply, "raw": w}
        except WeatherError as e:
            return {"mode": "weather", "error": str(e)}
    else:
        # RAG path
        hits = _rag_pdf.query(user_input, k=4)
        if not hits:
            # no docs ingested
            return {"mode": "pdf", "response": "No documents ingested or nothing relevant found."}
        context = "\n\n".join(hits)
        answer = answer_with_context(context, user_input)
        return {"mode": "pdf", "response": answer, "context": hits}
