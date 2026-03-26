from crewai import Task

def tarea_evaluacion_tecnica(agent, texto_entrada):
    return Task(
        description=f'''Realiza un análisis profundo de los siguientes requisitos: {texto_entrada}.
        Céntrate en:
        1. Componentes clave de la infraestructura.
        2. Factores determinantes para la escalabilidad.
        3. Riesgos potenciales de integración con sistemas existentes.''',
        expected_output='Un informe de evaluación técnica profesional en formato Markdown, estructurado por secciones.',
        agent=agent,
        # NUEVO: Esto creará el archivo automáticamente al terminar
        output_file='informe_arquitectura.md' 
    )