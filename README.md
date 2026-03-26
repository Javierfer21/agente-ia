# 🤖 Consultor de Arquitectura con Agentes de IA

Este proyecto es un sistema de **IA Generativa Agéntica** diseñado para analizar requerimientos técnicos complejos y proponer arquitecturas de software escalables. Utiliza **LangChain (LCEL)** para la orquestación del flujo de trabajo y **Groq** para una inferencia de alta velocidad con modelos **Llama 3**.

## 🚀 Características
* **Equipo de Agentes Virtuales:** Flujo de trabajo secuencial con roles de Arquitectura, Seguridad y FinOps.
* **Orquestación con LangChain:** Uso de cadenas (Chains) para un control preciso del contexto y la generación de informes.
* **Interfaz Web:** Despliegue interactivo mediante **Streamlit**.
* **Baja Latencia:** Integración con la API de **Groq** para respuestas casi instantáneas.
* **Seguridad:** Gestión de variables de entorno para proteger credenciales sensibles.

## 🛠️ Stack Tecnológico
* **Lenguaje:** Python 3.10+
* **Framework:** LangChain (LCEL)
* **LLM:** Llama 3.1 (vía Groq)
* **Interfaz:** Streamlit
* **Entorno:** Virtualenv con soporte para `.env`

## 📂 Estructura del Proyecto
```text
agentic-ai/
├── core/
│   ├── agents.py       # Definición de agentes y sus LLMs
│   └── tasks.py        # Configuración de tareas y outputs
├── app.py              # Interfaz de usuario (Streamlit)
├── main.py             # Lógica principal y orquestación
[cite_start]├── .env                # Variables de entorno (no incluido en git) [cite: 2]
└── requirements.txt    # Dependencias del proyecto