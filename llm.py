import os
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.embeddings import OpenAIEmbeddings
from config import settings
# enable LangSmith tracing if key present
if settings.LANGSMITH_API_KEY:
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    os.environ["LANGCHAIN_API_KEY"] = settings.LANGSMITH_API_KEY

# set OPENAI_API_KEY for any library that expects it
if settings.OPENAI_API_KEY:
    os.environ["OPENAI_API_KEY"] = settings.OPENAI_API_KEY

def get_chat_llm(temperature: int=0, model: str = "gpt-4o-mini"):
    """Returns a ChatOpenAI wrapper (adjust model name as per your access)."""
    return ChatOpenAI(temperature=temperature, model=model)

def answer_with_context(context: str, question: str) -> str:
    prompt = PromptTemplate.from_template(
        """You are a helpful assistant. Use the context to answer the question concisely.
Context:
{context}

Question:
{question}

Answer:"""
    )
    llm = get_chat_llm()
    chain = LLMChain(llm=llm, prompt=prompt)
    return chain.run({"context": context, "question": question})

def get_openai_embeddings():
    return OpenAIEmbeddings()
