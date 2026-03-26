import streamlit as st
from main import AgenciaInteligencia

st.title("🤖 Consultor de Arquitectura AI")
st.markdown("Introduce los requisitos de tu sistema para recibir un análisis detallado.")

# Cuadro de texto para el usuario
user_input = st.text_area("Requerimientos del cliente:", placeholder="Ej: Necesito migrar mi SQL a microservicios...")

if st.button("Generar Informe"):
    if user_input:
        with st.spinner("Los agentes están trabajando..."):
            orquestador = AgenciaInteligencia()
            resultado = orquestador.ejecutar_analisis(user_input)
            st.success("¡Informe generado!")
            st.markdown(resultado)
    else:
        st.warning("Por favor, escribe algo primero.")