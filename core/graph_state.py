from typing import Annotated, TypedDict
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage


class OrchestratorState(TypedDict):
    proyecto: str
    messages: Annotated[list[BaseMessage], add_messages]
    arquitectura_output: str
    seguridad_output: str
    finops_output: str
    informe_final: str
    active_agent: str
