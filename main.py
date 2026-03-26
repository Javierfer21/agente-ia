import os
from dotenv import load_dotenv

# Esto debe ir arriba del todo, antes de los imports de 'core'
load_dotenv()

# import sys
# sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from crewai import Crew, Process
from core.agents import analista_arquitectura
from core.tasks import tarea_evaluacion_tecnica

class AgenciaInteligencia:
    def __init__(self):
        # Instanciamos los componentes
        self.agente = analista_arquitectura()
        
    def ejecutar_analisis(self, requerimientos_cliente):
        # Definimos la tarea con el input dinámico
        tarea = tarea_evaluacion_tecnica(self.agente, requerimientos_cliente)
        
        # Configurando el equipo (Crew)
        equipo = Crew(
            agents=[self.agente],
            tasks=[tarea],
            process=Process.sequential,
            verbose=True
        )
        
        return equipo.kickoff()

if __name__ == "__main__":
    contexto_demo = """
    Necesitamos migrar nuestra plataforma de e-commerce a una arquitectura de microservicios. 
    Actualmente usamos una base de datos SQL centralizada que sufre picos de carga. 
    Buscamos integrar una solución de búsqueda semántica y agentes de atención al cliente.
    """
    
    print("\n--- Iniciando Proceso de Análisis de Arquitectura ---\n")
    
    orquestador = AgenciaInteligencia()
    resultado = orquestador.ejecutar_analisis(contexto_demo)
    
    print("\n--- Informe Final Generado ---\n")
    print(resultado)