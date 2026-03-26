# Agente de Arquitectura Cloud

Sistema de consultoría técnica automatizada basado en **múltiples agentes de IA independientes** que colaboran para analizar requisitos de proyectos y producir informes profesionales de arquitectura cloud.

Construido con **LangGraph**, **LangChain** y **Groq** (Llama 3.3 70B), desplegado como aplicación web con **Streamlit**.

---

## Cómo funciona

El sistema orquesta un equipo de cuatro agentes especializados mediante un grafo de estado (LangGraph `StateGraph`). Cada agente opera de forma independiente con su propio conjunto de herramientas y ciclo de razonamiento **ReAct** (Reason + Act): el agente razona, decide qué herramienta invocar, observa el resultado y repite hasta tener suficiente información para producir su análisis.

```
Usuario
   │
   ▼
┌─────────────────────┐
│  Arquitecto Senior  │  → estimar_componentes_aws
│                     │  → evaluar_patron_arquitectura
│                     │  → calcular_sla_disponibilidad
└──────────┬──────────┘
           │ arquitectura_output
           ▼
┌─────────────────────┐
│ Ingeniero Seguridad │  → generar_checklist_seguridad
│                     │  → identificar_vulnerabilidades
│                     │  → estimar_nivel_cumplimiento
└──────────┬──────────┘
           │ seguridad_output
           ▼
┌─────────────────────┐
│  Consultor FinOps   │  → estimar_costo_mensual_aws
│                     │  → calcular_ahorro_spot
│                     │  → recomendar_plan_ahorro
└──────────┬──────────┘
           │ finops_output
           ▼
┌─────────────────────┐
│   Editor Técnico    │  Consolida los tres informes
│                     │  en documento ejecutivo Markdown
└──────────┬──────────┘
           │
           ▼
    informe_arquitectura.md
```

El estado compartido (`OrchestratorState`) fluye entre nodos: cada agente lee los outputs de los anteriores y aporta el suyo, sin acoplamiento directo entre ellos.

---

## Agentes y herramientas

### Arquitecto Senior
Diseña la infraestructura cloud basándose en los requisitos del proyecto.

| Herramienta | Descripción |
|---|---|
| `estimar_componentes_aws` | Mapea requisitos a servicios AWS concretos con justificación |
| `evaluar_patron_arquitectura` | Recomienda patrón: 3-Tier, Microservicios, Serverless, Event-Driven, Strangler Fig |
| `calcular_sla_disponibilidad` | Calcula downtime permitido, RTO/RPO y estrategia AWS según los nines requeridos |

### Ingeniero de Seguridad (DevSecOps)
Audita la arquitectura propuesta y define controles de seguridad y cumplimiento normativo.

| Herramienta | Descripción |
|---|---|
| `generar_checklist_seguridad` | Genera checklist CIS/AWS por categoría: IAM, Red, Datos, Monitoreo |
| `identificar_vulnerabilidades_comunes` | Lista vulnerabilidades OWASP aplicables al tipo de sistema |
| `estimar_nivel_cumplimiento` | Requisitos y servicios AWS para GDPR, PCI-DSS, SOC2, HIPAA |

### Consultor FinOps
Calcula costos reales y estrategias de optimización para la arquitectura definida.

| Herramienta | Descripción |
|---|---|
| `estimar_costo_mensual_aws` | Estimación USD/mes por servicio (precios us-east-1) |
| `calcular_ahorro_spot` | Calcula ahorro potencial con Spot Instances vs On-Demand |
| `recomendar_plan_ahorro` | Recomienda Savings Plans, Reserved Instances u On-Demand según el patrón de uso |

### Editor Técnico
Consolida los tres informes en un documento Markdown ejecutivo sin herramientas adicionales.

---

## Stack tecnológico

| Capa | Tecnología |
|---|---|
| Orquestación de agentes | LangGraph `StateGraph` |
| Framework LLM | LangChain + LangChain-Core |
| Modelo de lenguaje | Llama 3.3 70B Versatile (vía Groq API) |
| Interfaz web | Streamlit |
| Gestión de entorno | python-dotenv |

---

## Estructura del proyecto

```
agentic-ai/
├── app.py                  # Interfaz Streamlit con progreso por agente en tiempo real
├── main.py                 # Grafo LangGraph: nodos, edges y puntos de entrada
├── requirements.txt
├── .env                    # Variables de entorno (no incluir en git)
└── core/
    ├── __init__.py
    ├── graph_state.py      # OrchestratorState (TypedDict compartido entre agentes)
    ├── tools.py            # 9 herramientas @tool deterministas
    ├── agents.py           # Definición de agentes con create_react_agent
    └── model_factory.py    # Factory de ChatGroq
```

---

## Instalación y uso local

### Requisitos

- Python 3.10+
- Clave API de [Groq](https://console.groq.com)

### Configuración

```bash
git clone <repo-url>
cd agentic-ai

python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

Crea el archivo `.env` en la raíz del proyecto:

```env
GROQ_API_KEY=gsk_...
```

### Ejecución

**Interfaz web:**
```bash
streamlit run app.py
```

**Línea de comandos:**
```bash
python main.py
```

El informe final se guarda automáticamente en `informe_arquitectura.md`.

---

## Despliegue en Streamlit Cloud

1. Haz fork del repositorio en GitHub.
2. Conecta el repositorio en [share.streamlit.io](https://share.streamlit.io).
3. En **Settings → Secrets**, añade:
   ```toml
   GROQ_API_KEY = "gsk_..."
   ```
4. Despliega. El archivo principal es `app.py`.

---

## Ejemplo de uso

**Input:**
> Migrar e-commerce Magento con 50.000 productos y 10.000 usuarios diarios desde servidor dedicado a AWS. Alta disponibilidad requerida, picos en Black Friday. Cumplimiento PCI-DSS para pagos con tarjeta.

**Output:** Documento Markdown con:
- Resumen ejecutivo
- Arquitectura AWS propuesta (ALB + ECS Fargate + Aurora Serverless + ElastiCache + CloudFront)
- Controles de seguridad priorizados + checklist PCI-DSS
- Estimación de costos desglosada + escenario optimizado con Savings Plans
- Plan de implementación en 3 fases
- Tabla de riesgos y mitigaciones
- Próximos pasos concretos

---

## Licencia

MIT
