import streamlit as st
import os
from main import ejecutar_agente_arquitectura

# Configuración de la página
st.set_page_config(
    page_title="Agente de Arquitectura Cloud",
    page_icon="🏗️",
    layout="wide"
)

# Título y descripción
st.title("🏗️ Agente de Arquitectura Cloud")
st.markdown("""
    Este agente de IA analiza tus necesidades de proyecto y recomienda 
    la mejor arquitectura cloud para tu caso de uso.
""")

# Input del usuario
contexto = st.text_area(
    "Describe tu proyecto:",
    placeholder="Ej: Queremos migrar un e-commerce de un servidor físico a AWS para escalar...",
    height=150
)

# Botón de ejecución
if st.button("🔍 Analizar Arquitectura", type="primary"):
    if not contexto:
        st.warning("⚠️ Por favor, describe tu proyecto primero.")
    else:
        with st.spinner("El agente está analizando tu caso..."):
            try:
                resultado = ejecutar_agente_arquitectura(contexto)
                st.success("✅ Análisis completado")
                st.markdown("### 📋 Resultado:")
                st.markdown(resultado)
            except Exception as e:
                st.error(f"❌ Error durante el análisis: {str(e)}")
                st.exception(e)

# Sidebar con info
with st.sidebar:
    st.header("ℹ️ Información")
    st.markdown("""
    **Versión:** 1.0.0  
    **Motor:** CrewAI + Groq  
    **Modelo:** Llama3/Mixtral
    """)
    
    # Configuración de API Key
    if not os.getenv("GROQ_API_KEY"):
        st.warning("⚠️ GROQ_API_KEY no configurada")
        groq_key = st.text_input("Groq API Key:", type="password")
        if groq_key:
            os.environ["GROQ_API_KEY"] = groq_key
            st.success("✅ API Key configurada")