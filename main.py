import os
import sys
from dotenv import load_dotenv
from core.model_factory import get_model
from core.agents import get_agent_personas
from core.tasks import get_architecture_prompts

# Asegurar que el directorio actual está en el path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

load_dotenv()

def ejecutar_agente_arquitectura(contexto_proyecto):
    """
    Orquesta el flujo de análisis usando LangChain (LCEL).
    """
    llm = get_model()
    personas = get_agent_personas()
    p_eval, p_seg, p_cost, p_final = get_architecture_prompts()

    # 1. Análisis de Arquitectura
    chain_arch = p_eval | llm
    res_arch = chain_arch.invoke({
        "system_prompt": personas["arquitecto"]["system"],
        "proyecto": contexto_proyecto
    })

    # 2. Análisis de Seguridad (usa el resultado del anterior)
    chain_seg = p_seg | llm
    res_seg = chain_seg.invoke({
        "system_prompt": personas["seguridad"]["system"],
        "arquitectura_previa": res_arch.content
    })

    # 3. Análisis de Costos
    chain_cost = p_cost | llm
    res_cost = chain_cost.invoke({
        "system_prompt": personas["finops"]["system"],
        "proyecto": contexto_proyecto,
        "arquitectura_previa": res_arch.content
    })

    # 4. Consolidación Final
    chain_final = p_final | llm
    informe_final = chain_final.invoke({
        "arquitectura": res_arch.content,
        "seguridad": res_seg.content,
        "costos": res_cost.content
    })

    # Guardar reporte (CrewAI lo hacía solo, en LangChain lo manejamos nosotros)
    with open("informe_arquitectura.md", "w", encoding="utf-8") as f:
        f.write(informe_final.content)
    
    return informe_final.content

if __name__ == "__main__":
    test_context = "Queremos migrar un e-commerce de un servidor físico a AWS para escalar."
    print("Generando informe técnico con LangChain...")
    resultado = ejecutar_agente_arquitectura(test_context)
    print(resultado)