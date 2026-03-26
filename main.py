import os
import sys

# Asegurar que el directorio actual está en el path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from dotenv import load_dotenv
from crewai import Crew, Process

# Importaciones de tus agentes y tareas
try:
    from core.agents import analista_arquitectura
    from core.tasks import tarea_evaluacion_tecnica
except ImportError as e:
    print(f"Error importando core modules: {e}")
    # Fallback: definir agentes básicos si core no existe
    from crewai import Agent, Task
    
    analista_arquitectura = Agent(
        role="Analista de Arquitectura Cloud",
        goal="Analizar y recomendar arquitecturas cloud óptimas",
        backstory="Experto en migraciones cloud con 10+ años de experiencia en AWS, Azure y GCP",
        verbose=True,
        allow_delegation=False
    )
    
    def tarea_evaluacion_tecnica(agent, contexto):
        return Task(
            description=f"Evaluar el siguiente proyecto y proponer arquitectura: {contexto}",
            agent=agent,
            expected_output="Informe técnico con recomendaciones de arquitectura cloud"
        )

# Cargar variables de entorno
load_dotenv()

def ejecutar_agente_arquitectura(contexto_proyecto):
    """
    Orquesta el proceso de análisis de arquitectura usando CrewAI.
    """
    
    # Configurar la tarea con el contexto dinámico del usuario
    tarea_personalizada = tarea_evaluacion_tecnica(analista_arquitectura, contexto_proyecto)

    # Crear el equipo (Crew)
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