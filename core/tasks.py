from langchain.prompts import ChatPromptTemplate

def get_architecture_prompts():
    """Define los prompts de LangChain para cada etapa del análisis."""
    
    evaluacion_template = ChatPromptTemplate.from_messages([
        ("system", "{system_prompt}"),
        ("human", "Analiza estos requisitos: {proyecto}. Céntrate en: 1. Infraestructura, 2. Escalabilidad, 3. Riesgos.")
    ])

    seguridad_template = ChatPromptTemplate.from_messages([
        ("system", "{system_prompt}"),
        ("human", "Basado en este diseño de arquitectura: {arquitectura_previa}, define controles de seguridad y cumplimiento.")
    ])

    costos_template = ChatPromptTemplate.from_messages([
        ("system", "{system_prompt}"),
        ("human", "Para este proyecto: {proyecto} y este diseño: {arquitectura_previa}, estima costos y estrategias de ahorro.")
    ])

    final_template = ChatPromptTemplate.from_messages([
        ("system", "Eres un Editor Técnico Senior."),
        ("human", "Consolida los siguientes informes en un documento Markdown profesional:\n\nARQUITECTURA:\n{arquitectura}\n\nSEGURIDAD:\n{seguridad}\n\nCOSTOS:\n{costos}")
    ])

    return (
        evaluacion_template, 
        seguridad_template, 
        costos_template,
        final_template
    )