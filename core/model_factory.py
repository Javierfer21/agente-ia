import os
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()


def get_model(model_name: str = "llama3-70b-8192", temperature: float = 0.1) -> ChatGroq:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY no encontrada en el archivo .env")

    return ChatGroq(
        model=model_name,
        groq_api_key=api_key,
        temperature=temperature,
    )
