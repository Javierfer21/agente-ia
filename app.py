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
| **Arquitecto Senior** | Diseño de infraestructura y selección de servicios cloud | Estimación AWS, patrones arquitectónicos, análisis de SLA |
| **Ingeniero de Seguridad** | Auditoría de controles y cumplimiento normativo | Checklist CIS, análisis OWASP, marcos regulatorios |
| **Consultor FinOps** | Estimación de costos y estrategia de optimización | Precios AWS, cálculo Spot, planes de ahorro |
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

if "proyecto_texto" not in st.session_state:
    st.session_state.proyecto_texto = ""

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

with st.expander("Configuración avanzada"):
    col1, col2 = st.columns(2)
    with col1:
        st.selectbox("Modelo de lenguaje", ["llama-3.3-70b-versatile", "llama-3.1-8b-instant"], index=0)
    with col2:
        st.slider("Temperatura", 0.0, 1.0, 0.1, 0.05)

st.markdown("<br>", unsafe_allow_html=True)


# ── Ejecución ───────────────────────────────────────────────────────────────────
if st.button("Ejecutar análisis", type="primary", use_container_width=True):
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

    informe_final = ""

    try:
        for nodo, actualizaciones in stream_agente_arquitectura(proyecto.strip()):

            if nodo == "arquitecto" and "arquitectura_output" in actualizaciones:
                slot_arquitecto.markdown(actualizaciones["arquitectura_output"])
                status_arquitecto.update(
                    label="Arquitecto Senior — completado",
                    state="complete", expanded=False
                )
                status_seguridad.update(
                    label="Ingeniero de Seguridad — en proceso",
                    expanded=True
                )

            elif nodo == "seguridad" and "seguridad_output" in actualizaciones:
                slot_seguridad.markdown(actualizaciones["seguridad_output"])
                status_seguridad.update(
                    label="Ingeniero de Seguridad — completado",
                    state="complete", expanded=False
                )
                status_finops.update(
                    label="Consultor FinOps — en proceso",
                    expanded=True
                )

            elif nodo == "finops" and "finops_output" in actualizaciones:
                slot_finops.markdown(actualizaciones["finops_output"])
                status_finops.update(
                    label="Consultor FinOps — completado",
                    state="complete", expanded=False
                )
                status_editor.update(
                    label="Editor Técnico — consolidando informe",
                    expanded=True
                )

            elif nodo == "editor" and "informe_final" in actualizaciones:
                informe_final = actualizaciones["informe_final"]
                slot_editor.markdown(informe_final)
                status_editor.update(
                    label="Editor Técnico — completado",
                    state="complete", expanded=False
                )

    except Exception as e:
        st.error(f"Error durante la ejecución: {str(e)}")
        st.exception(e)
        st.stop()

    if informe_final:
        st.success("Análisis completado. Los cuatro agentes han finalizado su trabajo.")
        st.markdown("---")
        st.markdown("## Informe Final")
        st.markdown(informe_final)

        with st.spinner("Generando PDF..."):
            pdf_bytes = markdown_a_pdf(informe_final)

        st.download_button(
            label="Descargar informe (.pdf)",
            data=pdf_bytes,
            file_name="informe_arquitectura_cloud.pdf",
            mime="application/pdf",
            use_container_width=True,
        )


# ── Sidebar ─────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### Sistema")
    st.markdown("""
    | | |
    |---|---|
    | Motor | LangGraph + Groq |
    | Modelo | Llama 3.3 70B |
    | Agentes | 4 especializados |
    | Herramientas | 9 (3 por agente) |
    | Razonamiento | ReAct |
    """)

    st.markdown("---")

    if grafo:
        st.success("Sistema operativo")
    else:
        st.error("Error de inicialización")

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
