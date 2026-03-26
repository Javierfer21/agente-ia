import streamlit as st
from dotenv import load_dotenv
from main import stream_agente_arquitectura, get_graph

load_dotenv()

st.set_page_config(
    page_title="Equipo de Arquitectura Cloud",
    page_icon="🏗️",
    layout="wide",
)

# ── Cachear el grafo compilado ─────────────────────────────────────────────────
@st.cache_resource
def cargar_grafo():
    try:
        return get_graph()
    except Exception:
        return None

grafo = cargar_grafo()

# ── Cabecera ───────────────────────────────────────────────────────────────────
st.title("🏗️ Equipo de Arquitectura Cloud")

st.chat_message("assistant").markdown("""
Bienvenido. Este sistema ejecuta un equipo real de **4 agentes IA independientes** con LangGraph:

| Agente | Rol | Herramientas |
|--------|-----|--------------|
| 🏗️ **Arquitecto Senior** | Diseña la infraestructura cloud | Estimación AWS, patrones, SLA |
| 🔒 **Ingeniero de Seguridad** | Audita y define controles | OWASP, checklist CIS, normativas |
| 💰 **Consultor FinOps** | Calcula costos y optimizaciones | Precios AWS, Spot, Savings Plans |
| 📝 **Editor Técnico** | Consolida el informe ejecutivo | — |

Cada agente usa un **ciclo ReAct real**: razona → llama herramientas → observa resultados → repite hasta tener suficiente información.
""")

if not grafo:
    st.error("⚠️ No se pudo construir el grafo. Verifica que `GROQ_API_KEY` esté configurada.")
    st.code("GROQ_API_KEY = 'gsk_...'", language="toml")
    st.info("En Streamlit Cloud: Settings → Secrets → añade la clave.")
    st.stop()

# ── Input ──────────────────────────────────────────────────────────────────────
EJEMPLO = (
    "Somos una clínica privada en España con 3 sedes. Queremos digitalizar la gestión de historiales "
    "médicos de 80.000 pacientes, actualmente en papel y Excel. Necesitamos una aplicación web para "
    "que los médicos accedan desde cualquier sede, con disponibilidad 24/7. Manejamos datos de salud "
    "sensibles y debemos cumplir con GDPR y la normativa española de protección de datos sanitarios. "
    "Esperamos unos 200 usuarios concurrentes en horas pico."
)

if "proyecto_texto" not in st.session_state:
    st.session_state.proyecto_texto = ""

if st.button("💡 Usar ejemplo de prueba", use_container_width=False):
    st.session_state.proyecto_texto = EJEMPLO

proyecto = st.text_area(
    "📋 Describe tu proyecto:",
    value=st.session_state.proyecto_texto,
    placeholder=(
        "Ej: Migrar e-commerce Magento con 50k productos, 10k usuarios diarios y picos en Black Friday "
        "a AWS. Alta disponibilidad requerida. Cumplimiento PCI-DSS para pagos con tarjeta."
    ),
    height=160,
)

with st.expander("⚙️ Opciones avanzadas"):
    col1, col2 = st.columns(2)
    with col1:
        st.selectbox("Modelo:", ["llama-3.3-70b-versatile", "llama-3.1-8b-instant"], index=0)
    with col2:
        st.slider("Temperatura:", 0.0, 1.0, 0.1, 0.05)

# ── Ejecución ──────────────────────────────────────────────────────────────────
if st.button("🚀 Ejecutar análisis multi-agente", type="primary", use_container_width=True):
    if not proyecto or len(proyecto.strip()) < 20:
        st.warning("⚠️ Describe el proyecto con más detalle (mínimo 20 caracteres).")
        st.stop()

    st.markdown("---")
    st.markdown("## 🤖 Progreso de los agentes")

    # Widgets de estado por agente
    status_arquitecto = st.status("🏗️ Arquitecto Senior — analizando...", state="running", expanded=True)
    status_seguridad  = st.status("🔒 Ingeniero de Seguridad — en espera", state="running", expanded=False)
    status_finops     = st.status("💰 Consultor FinOps — en espera",       state="running", expanded=False)
    status_editor     = st.status("📝 Editor Técnico — en espera",          state="running", expanded=False)

    # Placeholders para mostrar el output de cada agente en tiempo real
    out_arquitecto = st.empty()
    out_seguridad  = st.empty()
    out_finops     = st.empty()
    out_editor     = st.empty()

    informe_final = ""

    try:
        for nodo, actualizaciones in stream_agente_arquitectura(proyecto.strip()):

            if nodo == "arquitecto" and "arquitectura_output" in actualizaciones:
                contenido = actualizaciones["arquitectura_output"]
                status_arquitecto.update(
                    label="🏗️ Arquitecto Senior — ✅ completado",
                    state="complete", expanded=False
                )
                with out_arquitecto.expander("Ver análisis del Arquitecto", expanded=False):
                    st.markdown(contenido)
                status_seguridad.update(label="🔒 Ingeniero de Seguridad — analizando...", expanded=True)

            elif nodo == "seguridad" and "seguridad_output" in actualizaciones:
                contenido = actualizaciones["seguridad_output"]
                status_seguridad.update(
                    label="🔒 Ingeniero de Seguridad — ✅ completado",
                    state="complete", expanded=False
                )
                with out_seguridad.expander("Ver análisis de Seguridad", expanded=False):
                    st.markdown(contenido)
                status_finops.update(label="💰 Consultor FinOps — analizando...", expanded=True)

            elif nodo == "finops" and "finops_output" in actualizaciones:
                contenido = actualizaciones["finops_output"]
                status_finops.update(
                    label="💰 Consultor FinOps — ✅ completado",
                    state="complete", expanded=False
                )
                with out_finops.expander("Ver análisis FinOps", expanded=False):
                    st.markdown(contenido)
                status_editor.update(label="📝 Editor Técnico — consolidando...", expanded=True)

            elif nodo == "editor" and "informe_final" in actualizaciones:
                informe_final = actualizaciones["informe_final"]
                status_editor.update(
                    label="📝 Editor Técnico — ✅ completado",
                    state="complete", expanded=False
                )

    except Exception as e:
        st.error(f"❌ Error durante la ejecución: {str(e)}")
        st.exception(e)
        st.stop()

    # ── Resultado final ────────────────────────────────────────────────────────
    if informe_final:
        st.success("✅ Todos los agentes completaron su análisis.")
        st.markdown("---")
        st.markdown("## 📊 Informe Final Consolidado")
        st.markdown(informe_final)

        st.download_button(
            label="📥 Descargar informe (.md)",
            data=informe_final,
            file_name="informe_arquitectura_cloud.md",
            mime="text/markdown",
            use_container_width=True,
        )

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("ℹ️ Sistema")
    st.markdown("""
    **Motor:** LangGraph + Groq
    **Modelo:** Llama 3 70B
    **Agentes:** 4 independientes
    **Herramientas:** 9 (3 por agente)
    **Patrón:** ReAct (reason + act)
    """)
    st.markdown("---")
    if grafo:
        st.success("🟢 Grafo multi-agente listo")
    else:
        st.error("🔴 Error en el grafo")

    st.markdown("---")
    st.markdown("""
    **Flujo de colaboración:**
    ```
    Arquitecto
        ↓
    Seguridad (lee arquitectura)
        ↓
    FinOps (lee arquitectura)
        ↓
    Editor (consolida todo)
    ```
    """)
