from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.graph import StateGraph, START, END

from core.graph_state import OrchestratorState
from core.model_factory import get_model
from core.agents import (
    build_arquitecto_agent,
    build_seguridad_agent,
    build_finops_agent,
    build_editor_agent,
)

load_dotenv()

# ── Nodos del grafo ────────────────────────────────────────────────────────────

def nodo_arquitecto(state: OrchestratorState) -> dict:
    """Agente Arquitecto: diseña la arquitectura cloud usando herramientas AWS."""
    llm = get_model()
    agente = build_arquitecto_agent(llm)

    resultado = agente.invoke({
        "messages": [
            HumanMessage(content=f"Diseña la arquitectura cloud para este proyecto:\n\n{state['proyecto']}")
        ]
    })

    output = resultado["messages"][-1].content
    return {
        "arquitectura_output": output,
        "active_agent": "seguridad",
        "messages": [AIMessage(content=f"[ARQUITECTO] Análisis completado.")],
    }


def nodo_seguridad(state: OrchestratorState) -> dict:
    """Agente de Seguridad: audita la arquitectura y define controles de seguridad."""
    llm = get_model()
    agente = build_seguridad_agent(llm)

    resultado = agente.invoke({
        "messages": [
            HumanMessage(content=(
                f"Contexto del proyecto:\n{state['proyecto']}\n\n"
                f"Arquitectura ya definida por el Arquitecto Senior:\n{state['arquitectura_output']}\n\n"
                f"Realiza el análisis de seguridad completo para esta arquitectura."
            ))
        ]
    })

    output = resultado["messages"][-1].content
    return {
        "seguridad_output": output,
        "active_agent": "finops",
        "messages": [AIMessage(content=f"[SEGURIDAD] Análisis completado.")],
    }


def nodo_finops(state: OrchestratorState) -> dict:
    """Agente FinOps: calcula costos y estrategias de optimización."""
    llm = get_model()
    agente = build_finops_agent(llm)

    resultado = agente.invoke({
        "messages": [
            HumanMessage(content=(
                f"Contexto del proyecto:\n{state['proyecto']}\n\n"
                f"Arquitectura propuesta:\n{state['arquitectura_output']}\n\n"
                f"Realiza el análisis completo de costos FinOps para esta arquitectura."
            ))
        ]
    })

    output = resultado["messages"][-1].content
    return {
        "finops_output": output,
        "active_agent": "editor",
        "messages": [AIMessage(content=f"[FINOPS] Análisis completado.")],
    }


def nodo_editor(state: OrchestratorState) -> dict:
    """Agente Editor: consolida los tres informes en un documento ejecutivo final."""
    llm = get_model()
    agente = build_editor_agent(llm)

    resultado = agente.invoke({
        "messages": [
            HumanMessage(content=(
                f"Consolida estos tres informes de expertos en el documento final:\n\n"
                f"--- INFORME DEL ARQUITECTO SENIOR ---\n{state['arquitectura_output']}\n\n"
                f"--- INFORME DEL INGENIERO DE SEGURIDAD ---\n{state['seguridad_output']}\n\n"
                f"--- INFORME DEL CONSULTOR FINOPS ---\n{state['finops_output']}"
            ))
        ]
    })

    informe = resultado["messages"][-1].content

    with open("informe_arquitectura.md", "w", encoding="utf-8") as f:
        f.write(informe)

    return {
        "informe_final": informe,
        "active_agent": "done",
        "messages": [AIMessage(content=f"[EDITOR] Informe consolidado.")],
    }


# ── Construcción del grafo ─────────────────────────────────────────────────────

def build_graph():
    """Construye y compila el grafo orquestador multi-agente."""
    workflow = StateGraph(OrchestratorState)

    workflow.add_node("arquitecto", nodo_arquitecto)
    workflow.add_node("seguridad",  nodo_seguridad)
    workflow.add_node("finops",     nodo_finops)
    workflow.add_node("editor",     nodo_editor)

    workflow.add_edge(START,        "arquitecto")
    workflow.add_edge("arquitecto", "seguridad")
    workflow.add_edge("seguridad",  "finops")
    workflow.add_edge("finops",     "editor")
    workflow.add_edge("editor",     END)

    return workflow.compile()


# Grafo compilado una sola vez (evita reconstruirlo en cada llamada)
_graph = None

def get_graph():
    global _graph
    if _graph is None:
        _graph = build_graph()
    return _graph


# ── Puntos de entrada públicos ─────────────────────────────────────────────────

def ejecutar_agente_arquitectura(proyecto: str) -> str:
    """Ejecuta el pipeline multi-agente y retorna el informe final."""
    grafo = get_graph()
    estado_final = grafo.invoke({
        "proyecto": proyecto,
        "messages": [],
        "arquitectura_output": "",
        "seguridad_output": "",
        "finops_output": "",
        "informe_final": "",
        "active_agent": "arquitecto",
    })
    return estado_final["informe_final"]


def stream_agente_arquitectura(proyecto: str):
    """Generador que emite (nombre_nodo, actualizaciones_estado) a medida que cada agente termina."""
    grafo = get_graph()
    estado_inicial = {
        "proyecto": proyecto,
        "messages": [],
        "arquitectura_output": "",
        "seguridad_output": "",
        "finops_output": "",
        "informe_final": "",
        "active_agent": "arquitecto",
    }
    for chunk in grafo.stream(estado_inicial, stream_mode="updates"):
        for nodo, actualizaciones in chunk.items():
            yield nodo, actualizaciones


# ── Ejecución directa ──────────────────────────────────────────────────────────

if __name__ == "__main__":
    test_proyecto = (
        "Queremos migrar un e-commerce de Magento con 50,000 productos y 10,000 usuarios "
        "diarios desde un servidor dedicado en España a AWS. Necesitamos alta disponibilidad, "
        "escalado automático para picos de Black Friday y cumplir PCI-DSS para pagos con tarjeta."
    )
    print("Iniciando análisis multi-agente con LangGraph...\n")
    for nodo, updates in stream_agente_arquitectura(test_proyecto):
        print(f"✅ Agente '{nodo}' completado.")
    print("\nInforme guardado en informe_arquitectura.md")
