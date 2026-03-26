import os
import re
import streamlit as st
from dotenv import load_dotenv
from main import stream_agente_arquitectura, get_graph
from core.pdf_export import markdown_a_pdf

load_dotenv()

st.set_page_config(
    page_title="Cloud Architecture Advisory",
    page_icon=None,
    layout="wide",
)

# Estilos corporativos
st.markdown("""
<style>
    /* Tipografía y fondo general */
    html, body, [class*="css"] {
        font-family: 'Inter', 'Helvetica Neue', Arial, sans-serif;
    }

    /* Título principal */
    h1 {
        font-weight: 700;
        letter-spacing: -0.5px;
        color: #0f1923;
    }

    /* Subtítulos */
    h2 {
        font-weight: 600;
        color: #0f1923;
        border-bottom: 2px solid #e2e8f0;
        padding-bottom: 8px;
        margin-top: 2rem;
    }

    h3 { font-weight: 600; color: #1e293b; }

    /* Tabla de agentes */
    table {
        width: 100%;
        border-collapse: collapse;
        font-size: 0.9rem;
    }
    th {
        background-color: #f8fafc;
        font-weight: 600;
        text-align: left;
        padding: 10px 14px;
        border-bottom: 2px solid #e2e8f0;
        color: #475569;
        text-transform: uppercase;
        font-size: 0.75rem;
        letter-spacing: 0.05em;
    }
    td { padding: 10px 14px; border-bottom: 1px solid #f1f5f9; }

    /* Botón primario — azul marino */
    .stButton > button[kind="primary"] {
        background-color: #1d3557;
        color: white;
        border: none;
        border-radius: 4px;
        font-weight: 600;
        letter-spacing: 0.03em;
        padding: 0.6rem 1.5rem;
        transition: background-color 0.15s ease;
    }
    .stButton > button[kind="primary"]:hover {
        background-color: #14253f;
        color: white;
    }

    /* Botón secundario — contorno azul marino */
    .stButton > button:not([kind="primary"]) {
        border: 1px solid #1d3557;
        border-radius: 4px;
        color: #1d3557;
        font-weight: 500;
        background-color: white;
        transition: all 0.15s ease;
    }
    .stButton > button:not([kind="primary"]):hover {
        background-color: #1d3557;
        color: white;
    }

    /* Text area */
    .stTextArea textarea {
        border-radius: 4px;
        border: 1px solid #cbd5e1;
        font-size: 0.9rem;
        line-height: 1.6;
    }
    .stTextArea textarea:focus {
        border-color: #0f172a;
        box-shadow: 0 0 0 2px rgba(15,23,42,0.1);
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #f8fafc;
        border-right: 1px solid #e2e8f0;
    }

    /* Divider */
    hr { border-color: #e2e8f0; margin: 1.5rem 0; }

    /* Ocultar el avatar del chat */
    [data-testid="chatAvatarIcon-assistant"] { display: none; }

    /* Bloque de introducción */
    [data-testid="stChatMessage"] {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 6px;
        padding: 1rem 1.5rem;
    }

    /* Download button */
    .stDownloadButton > button {
        border: 1px solid #1d3557;
        color: #1d3557;
        background-color: white;
        font-weight: 600;
        border-radius: 4px;
        transition: all 0.15s ease;
    }
    .stDownloadButton > button:hover {
        background-color: #1d3557;
        color: white;
    }

    /* Etiquetas de fuentes */
    .fuente-label {
        font-size: 0.75rem;
        color: #64748b;
        margin-top: 12px;
        margin-bottom: 4px;
    }
</style>
""", unsafe_allow_html=True)


# ── Cache del grafo ─────────────────────────────────────────────────────────────
@st.cache_resource
def cargar_grafo():
    try:
        return get_graph()
    except Exception:
        return None

grafo = cargar_grafo()


# ── Helpers ─────────────────────────────────────────────────────────────────────
def extraer_fuentes(texto: str) -> list:
    """Extrae URLs citadas como enlaces Markdown [Título](url) del texto."""
    patron = r'\[([^\]]+)\]\((https?://[^\s\)\]]+)\)'
    matches = re.findall(patron, texto)
    seen = set()
    fuentes = []
    for titulo, url in matches:
        if url not in seen:
            seen.add(url)
            fuentes.append({"titulo": titulo, "url": url})
    return fuentes


def mostrar_badges_fuentes(fuentes: list, prefijo: str):
    """Muestra las fuentes como etiquetas clickables que abren el panel lateral."""
    if not fuentes:
        return
    st.markdown(
        "<p class='fuente-label'>Fuentes consultadas — haz clic para ver el detalle en el panel lateral:</p>",
        unsafe_allow_html=True,
    )
    for i in range(0, len(fuentes), 3):
        grupo = fuentes[i:i+3]
        cols = st.columns(len(grupo))
        for j, f in enumerate(grupo):
            with cols[j]:
                label = (f["titulo"][:40] + "…") if len(f["titulo"]) > 40 else f["titulo"]
                if st.button(label, key=f"badge_{prefijo}_{i+j}", help=f["url"], use_container_width=True):
                    st.session_state.fuente_panel = f
                    st.rerun()


# ── Session state ───────────────────────────────────────────────────────────────
if "proyecto_texto" not in st.session_state:
    st.session_state.proyecto_texto = ""
if "resultados" not in st.session_state:
    st.session_state.resultados = None
if "pdf_bytes" not in st.session_state:
    st.session_state.pdf_bytes = None
if "fuente_panel" not in st.session_state:
    st.session_state.fuente_panel = None


# ── Cabecera ────────────────────────────────────────────────────────────────────
st.title("Cloud Architecture Advisory")
st.caption("Sistema de análisis multi-agente para diseño de infraestructura cloud")

st.markdown("<br>", unsafe_allow_html=True)

st.chat_message("assistant").markdown("""
Este sistema coordina un equipo de cuatro agentes especializados que colaboran de forma secuencial
para producir un informe técnico completo. Cada agente opera de forma independiente con su propio
conjunto de herramientas y ciclo de razonamiento autónomo.

| Especialista | Función | Herramientas |
|---|---|---|
| **Arquitecto Senior** | Diseño de infraestructura y selección de servicios cloud | Estimación AWS, patrones arquitectónicos, análisis de SLA, búsqueda web |
| **Ingeniero de Seguridad** | Auditoría de controles y cumplimiento normativo | Checklist CIS, análisis OWASP, marcos regulatorios, búsqueda web |
| **Consultor FinOps** | Estimación de costos y estrategia de optimización | Precios AWS, cálculo Spot, planes de ahorro, búsqueda web |
| **Editor Técnico** | Consolidación del informe ejecutivo final | — |

Describa los requisitos del proyecto en el campo inferior para iniciar el análisis.
""")

if not grafo:
    st.error("No se pudo inicializar el sistema. Verifique que GROQ_API_KEY esté configurada correctamente.")
    st.code("GROQ_API_KEY = 'gsk_...'", language="toml")
    st.info("En Streamlit Cloud: Settings > Secrets")
    st.stop()


# ── Input ───────────────────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)

EJEMPLO = (
    "Somos una clínica privada en España con 3 sedes. Queremos digitalizar la gestión de historiales "
    "médicos de 80.000 pacientes, actualmente en papel y Excel. Necesitamos una aplicación web para "
    "que los médicos accedan desde cualquier sede, con disponibilidad 24/7. Manejamos datos de salud "
    "sensibles y debemos cumplir con GDPR y la normativa española de protección de datos sanitarios. "
    "Esperamos unos 200 usuarios concurrentes en horas pico."
)

if st.button("Cargar caso de ejemplo", use_container_width=False):
    st.session_state.proyecto_texto = EJEMPLO

proyecto = st.text_area(
    "Descripción del proyecto",
    value=st.session_state.proyecto_texto,
    placeholder=(
        "Describa el proyecto con el mayor detalle posible: sector, escala, requisitos de disponibilidad, "
        "normativas aplicables, volumen de usuarios, sistema actual si lo hay..."
    ),
    height=160,
)

st.markdown("<br>", unsafe_allow_html=True)


# ── Ejecución ───────────────────────────────────────────────────────────────────
col_run, col_clear = st.columns([5, 1])
with col_run:
    run_btn = st.button("Ejecutar análisis", type="primary", use_container_width=True)
with col_clear:
    clear_btn = st.button(
        "Limpiar",
        use_container_width=True,
        disabled=(st.session_state.resultados is None),
        help="Borrar resultados y comenzar un nuevo análisis",
    )

if clear_btn:
    st.session_state.resultados = None
    st.session_state.pdf_bytes = None
    st.session_state.fuente_panel = None
    st.rerun()

if run_btn:
    if not proyecto or len(proyecto.strip()) < 20:
        st.warning("Por favor, describa el proyecto con mayor detalle antes de continuar.")
        st.stop()

    st.markdown("---")
    st.markdown("## Progreso del análisis")

    with st.status("Arquitecto Senior — en proceso", state="running", expanded=True) as status_arquitecto:
        slot_arquitecto = st.empty()

    with st.status("Ingeniero de Seguridad — en espera", state="running", expanded=False) as status_seguridad:
        slot_seguridad = st.empty()

    with st.status("Consultor FinOps — en espera", state="running", expanded=False) as status_finops:
        slot_finops = st.empty()

    with st.status("Editor Técnico — en espera", state="running", expanded=False) as status_editor:
        slot_editor = st.empty()

    _arquitectura = ""
    _seguridad = ""
    _finops = ""
    _informe = ""

    try:
        for nodo, actualizaciones in stream_agente_arquitectura(proyecto.strip()):

            if nodo == "arquitecto" and "arquitectura_output" in actualizaciones:
                _arquitectura = actualizaciones["arquitectura_output"]
                slot_arquitecto.markdown(_arquitectura)
                status_arquitecto.update(
                    label="Arquitecto Senior — completado",
                    state="complete", expanded=False
                )
                status_seguridad.update(
                    label="Ingeniero de Seguridad — en proceso",
                    expanded=True
                )

            elif nodo == "seguridad" and "seguridad_output" in actualizaciones:
                _seguridad = actualizaciones["seguridad_output"]
                slot_seguridad.markdown(_seguridad)
                status_seguridad.update(
                    label="Ingeniero de Seguridad — completado",
                    state="complete", expanded=False
                )
                status_finops.update(
                    label="Consultor FinOps — en proceso",
                    expanded=True
                )

            elif nodo == "finops" and "finops_output" in actualizaciones:
                _finops = actualizaciones["finops_output"]
                slot_finops.markdown(_finops)
                status_finops.update(
                    label="Consultor FinOps — completado",
                    state="complete", expanded=False
                )
                status_editor.update(
                    label="Editor Técnico — consolidando informe",
                    expanded=True
                )

            elif nodo == "editor" and "informe_final" in actualizaciones:
                _informe = actualizaciones["informe_final"]
                slot_editor.markdown(_informe)
                status_editor.update(
                    label="Editor Técnico — completado",
                    state="complete", expanded=False
                )

    except Exception as e:
        st.error(f"Error durante la ejecución: {str(e)}")
        st.exception(e)
        st.stop()

    if _informe:
        st.session_state.resultados = {
            "arquitecto": _arquitectura,
            "seguridad": _seguridad,
            "finops": _finops,
            "informe": _informe,
        }
        st.session_state.pdf_bytes = None  # Forzar regeneración del PDF


# ── Resultados persistentes ──────────────────────────────────────────────────────
if st.session_state.resultados:
    r = st.session_state.resultados

    st.markdown("---")
    st.success("Análisis completado. Los cuatro agentes han finalizado su trabajo.")
    st.markdown("## Resultados del análisis")

    tab_informe, tab_arq, tab_seg, tab_fin = st.tabs([
        "Informe Final", "Arquitecto Senior", "Ingeniero de Seguridad", "Consultor FinOps"
    ])

    with tab_informe:
        st.markdown(r["informe"])
        mostrar_badges_fuentes(extraer_fuentes(r["informe"]), "inf")
        st.markdown("<br>", unsafe_allow_html=True)
        if st.session_state.pdf_bytes is None:
            with st.spinner("Generando PDF..."):
                st.session_state.pdf_bytes = markdown_a_pdf(r["informe"])
        st.download_button(
            label="Descargar informe (.pdf)",
            data=st.session_state.pdf_bytes,
            file_name="informe_arquitectura_cloud.pdf",
            mime="application/pdf",
            use_container_width=True,
        )

    with tab_arq:
        st.markdown(r["arquitecto"])
        mostrar_badges_fuentes(extraer_fuentes(r["arquitecto"]), "arq")

    with tab_seg:
        st.markdown(r["seguridad"])
        mostrar_badges_fuentes(extraer_fuentes(r["seguridad"]), "seg")

    with tab_fin:
        st.markdown(r["finops"])
        mostrar_badges_fuentes(extraer_fuentes(r["finops"]), "fin")


# ── Sidebar ─────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### Sistema")
    tavily_activo = bool(os.getenv("TAVILY_API_KEY"))
    st.markdown(f"""
    | | |
    |---|---|
    | Motor | LangGraph + Groq |
    | Modelo | Llama 3.3 70B |
    | Agentes | 4 especializados |
    | Herramientas | 9 + búsqueda web |
    | Búsqueda web | {"Activa" if tavily_activo else "No configurada"} |
    | Razonamiento | ReAct |
    """)

    st.markdown("---")

    if grafo:
        st.success("Sistema operativo")
    else:
        st.error("Error de inicialización")

    if not tavily_activo:
        st.warning(
            "**Búsqueda web no configurada.**\n\n"
            "Añade `TAVILY_API_KEY` en los secretos de Streamlit Cloud para que los agentes "
            "consulten precios y datos en tiempo real."
        )

    st.markdown("---")
    st.markdown("**Flujo de trabajo**")
    st.markdown("""
    ```
    Arquitecto Senior
         |
    Ingeniero de Seguridad
         |
    Consultor FinOps
         |
    Editor Técnico
         |
    Informe ejecutivo
    ```
    """)
    st.caption("Cada agente recibe el output de los anteriores como contexto.")

    # ── Panel de fuente seleccionada ─────────────────────────────────────────────
    if st.session_state.get("fuente_panel"):
        fuente = st.session_state.fuente_panel
        st.markdown("---")
        st.markdown("### Fuente consultada")
        st.markdown(f"**{fuente['titulo']}**")
        st.markdown(
            f"<p style='font-size:0.75rem;word-break:break-all;color:#475569;'>{fuente['url']}</p>",
            unsafe_allow_html=True,
        )
        st.link_button("Abrir fuente completa", fuente["url"], use_container_width=True)
        if st.button("Cerrar panel", key="cerrar_fuente_panel", use_container_width=True):
            st.session_state.fuente_panel = None
            st.rerun()
