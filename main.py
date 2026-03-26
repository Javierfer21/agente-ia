import os
import sys

# Streamlit no encontraba la carpeta 'core' y lo estoy forzando desde aquí
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from dotenv import load_dotenv
from crewai import Crew, Process

# Importaciones de tus agentes y tareas
from core.agents import analista_arquitectura
from core.tasks import tarea_evaluacion_tecnica

# Cargo las variables de entorno (Local lee .env, Cloud lee 'Secrets')
load_dotenv()

def ejecutar_agente_arquitectura(contexto_proyecto):
    """
    Orquesta el proceso de análisis de arquitectura usando CrewAI.
    """
    
    # Configuro la tarea con el contexto dinámico del usuario
    tarea_personalizada = tarea_evaluacion_tecnica(analista_arquitectura, contexto_proyecto)

    # Crea0 el equipo (Crew)
    crew = Crew(
        agents=[analista_arquitectura],
        tasks=[tarea_personalizada],
        process=Process.sequential,
        verbose=True
    )


    resultado = crew.kickoff()
    return resultado

if __name__ == "__main__":
    # Prueba rápida de ejecución local
    test_context = "Queremos migrar un e-commerce de un servidor físico a AWS para escalar."
    print(ejecutar_agente_arquitectura(test_context))