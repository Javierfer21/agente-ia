import os
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

def get_model():
    api_key = os.getenv("GROQ_API_KEY")
    
    if not api_key:
        raise ValueError("No se encontró GROQ_API_KEY en el archivo .env")

    # Cambiamos la forma de pasar el modelo para máxima compatibilidad
    return ChatGroq(
        model="llama3-70b-8192", # Usamos 'model' en lugar de 'model_name'
        groq_api_key=api_key,
        temperature=0.1
    )