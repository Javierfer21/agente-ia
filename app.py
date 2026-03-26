import streamlit as st
import os
from dotenv import load_dotenv
from main import ejecutar_agente_arquitectura
from core.model_factory import get_model

# Cargar variables de entorno
load_dotenv()

# Configuración de la página
st.set_page_config(
    page_title="Agente de Arquitectura Cloud",
    page_icon="🏗️",
    layout="wide"
)

# Inicializar el modelo de Groq
@st.cache_resource
def get_llm():
    try:
        return get_model()
    except:
        return None

def analizar_arquitectura(contexto: str) -> str:
    """Llama a la lógica multi-paso de main.py"""
    try:
        return ejecutar_agente_arquitectura(contexto)
    except Exception as e:
        return f"❌ Error en el análisis: {str(e)}"

# ============ INTERFAZ STREAMLIT ============

st.title("🏗️ Agente de Arquitectura Cloud")

# Presentación del equipo de agentes
st.chat_message("assistant").markdown("""
    👋 **¡Hola! Somos tu equipo de consultoría técnica automatizada.**
    
    Estamos aquí para ayudarte a diseñar soluciones robustas en la nube. Nuestro equipo está compuesto por:
    *   **Arquitecto Senior:** Especialista en escalabilidad y patrones de diseño.
    *   **Ingeniero de Seguridad:** Experto en blindaje y cumplimiento (DevSecOps).
    *   **Consultor FinOps:** Tu aliado para optimizar costos y maximizar el retorno.
    
    **¿Qué proyecto tienes en mente hoy?** Describe tus necesidades abajo y nos pondremos a trabajar juntos.
""")

# Verificar API Key
llm = get_llm()
if not llm:
    st.error("⚠️ **GROQ_API_KEY no configurada**")
    st.info("Ve a la configuración de tu app en Streamlit Cloud → Secrets y añade:")
    st.code("GROQ_API_KEY = 'gsk_tu_api_key_aqui'", language="toml")
    st.stop()

# Input del usuario
contexto = st.text_area(
    "📋 Describe tu proyecto:",
    placeholder="Ejemplo: Queremos migrar un e-commerce de Magento desde un servidor dedicado en España a AWS. Tenemos 50,000 productos, 10,000 usuarios diarios y picos de tráfico en Black Friday. Necesitamos alta disponibilidad y escalado automático.",
    height=180
)

# Opciones avanzadas (colapsadas)
with st.expander("⚙️ Opciones avanzadas"):
    col1, col2 = st.columns(2)
    with col1:
        modelo = st.selectbox(
            "Modelo de IA:",
            ["llama3-70b-8192", "llama3-8b-8192", "mixtral-8x7b-32768"],
            index=0
        )
    with col2:
        temperatura = st.slider("Creatividad:", 0.0, 1.0, 0.3, 0.1)

# Botón de ejecución
if st.button("🔍 Analizar Arquitectura", type="primary", use_container_width=True):
    if not contexto or len(contexto) < 20:
        st.warning("⚠️ Por favor, describe tu proyecto con más detalle (mínimo 20 caracteres).")
    else:
        with st.spinner("🏗️ El arquitecto está diseñando tu solución..."):
            resultado = analizar_arquitectura(contexto)
            
        st.success("✅ Análisis completado")
        st.markdown("---")
        st.markdown("## 📊 Resultado del Análisis")
        st.markdown(resultado)
        
        # Botón para descargar
        st.download_button(
            label="📥 Descargar informe",
            data=resultado,
            file_name="arquitectura_cloud.md",
            mime="text/markdown"
        )

# Sidebar
with st.sidebar:
    st.header("ℹ️ Sobre esta app")
    st.markdown("""
    **Versión:** 2.0.0 (Python 3.14 compatible)  
    **Motor:** LangChain + Groq  
    **Modelo:** Llama 3 / Mixtral
    
    ---
    
    **Características:**
    - ✅ Sin dependencias Rust
    - ✅ Compatible Python 3.14
    - ✅ Respuesta en segundos
    - ✅ Arquitecturas AWS/Azure/GCP
    """)
    
    st.markdown("---")
    st.markdown("**Estado del sistema:**")
    if llm:
        st.success("🟢 API de Groq conectada")
    else:
        st.error("🔴 API no configurada")