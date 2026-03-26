from crewai import Agent

def analista_arquitectura():
    return Agent(
        role='Especialista Senior en Arquitectura de Soliciones',
        goal='Identificar patrones de diseño y requisitos de integración a partir de memorias técnicas.',
        backstory='''Eres un arquitecto de soluciones con amplia trayectoria en la modernización de sistemas complejos. 
        Tu fuerte es detectar cuellos de botella de escalabilidad y puntos críticos de integración.''',
        allow_delegation=False,
        verbose=True,
        # ACTUALIZACIÓN: Usamos el modelo Llama 3.3, que es el estándar actual en Groq
        llm="groq/llama-3.1-8b-instant" 
    )