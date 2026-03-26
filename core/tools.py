import json
from typing import Optional
from langchain_core.tools import tool


# ═══════════════════════════════════════════════════════════════════════════════
# HERRAMIENTAS DEL ARQUITECTO
# ═══════════════════════════════════════════════════════════════════════════════

@tool
def estimar_componentes_aws(requisitos: str) -> str:
    """Analiza un texto de requisitos y devuelve una lista de servicios AWS recomendados
    con justificación técnica para cada uno."""
    req = requisitos.lower()
    servicios = []

    if any(k in req for k in ["web", "api", "http", "rest", "frontend"]):
        servicios.append({"servicio": "Application Load Balancer", "razon": "Balanceo de carga HTTP/HTTPS con SSL termination y health checks"})
        servicios.append({"servicio": "ECS Fargate", "razon": "Contenedores sin gestión de servidores, escala automática"})

    if any(k in req for k in ["base de datos", "database", "sql", "postgres", "mysql", "datos"]):
        servicios.append({"servicio": "RDS Aurora Serverless v2", "razon": "Auto-scaling de capacidad, Multi-AZ nativo, compatible MySQL/Postgres"})

    if any(k in req for k in ["escal", "tráfico", "pico", "spike", "usuarios", "black friday"]):
        servicios.append({"servicio": "Auto Scaling Group", "razon": "Escala horizontal automática por métricas de CPU/peticiones"})
        servicios.append({"servicio": "CloudFront", "razon": "CDN global con 400+ PoPs para reducir latencia y carga en origen"})

    if any(k in req for k in ["cache", "redis", "velocidad", "latencia", "rendimiento"]):
        servicios.append({"servicio": "ElastiCache Redis", "razon": "Capa de caché en memoria para latencia <1ms en sesiones y catálogo"})

    if any(k in req for k in ["archivo", "imagen", "storage", "almacenam", "video", "s3"]):
        servicios.append({"servicio": "S3 + CloudFront", "razon": "Almacenamiento ilimitado de objetos con distribución CDN global"})

    if any(k in req for k in ["microservicio", "servicio independiente", "desacoplado"]):
        servicios.append({"servicio": "EKS (Kubernetes)", "razon": "Orquestación de microservicios con service discovery nativo"})
        servicios.append({"servicio": "SQS + SNS", "razon": "Mensajería asíncrona para desacoplar servicios"})

    if any(k in req for k in ["event", "cola", "mensaje", "stream", "kafka"]):
        servicios.append({"servicio": "Amazon EventBridge", "razon": "Bus de eventos serverless para arquitectura event-driven"})
        servicios.append({"servicio": "SQS FIFO", "razon": "Cola de mensajes con orden garantizado y exactly-once delivery"})

    if not servicios:
        servicios = [
            {"servicio": "EC2 t3.medium + Auto Scaling", "razon": "Cómputo de propósito general con escalado reactivo"},
            {"servicio": "RDS PostgreSQL Multi-AZ", "razon": "Base de datos relacional con alta disponibilidad"},
            {"servicio": "Application Load Balancer", "razon": "Punto de entrada único con health checks"},
        ]

    return json.dumps({"servicios_recomendados": servicios}, ensure_ascii=False, indent=2)


@tool
def evaluar_patron_arquitectura(escenario: str) -> str:
    """Recomienda el patrón de arquitectura más adecuado dado un escenario de negocio.
    Retorna el patrón, sus pros, contras y servicios AWS clave."""
    esc = escenario.lower()

    if any(k in esc for k in ["microservicio", "equipo independiente", "despliegue independiente", "soa"]):
        return json.dumps({
            "patron": "Microservicios",
            "descripcion": "Servicios pequeños e independientes, cada uno con su propia base de datos",
            "pros": ["Equipos autónomos", "Escalado independiente por servicio", "Tecnologías heterogéneas", "Tolerancia a fallos parciales"],
            "contras": ["Complejidad operativa alta", "Latencia de red entre servicios", "Distributed tracing necesario", "Gestión de transacciones distribuidas"],
            "aws_clave": ["EKS/ECS", "API Gateway", "Service Mesh (AWS App Mesh)", "X-Ray para trazabilidad"]
        }, ensure_ascii=False, indent=2)

    elif any(k in esc for k in ["event", "mensaje", "cola", "stream", "asíncrono", "kafka"]):
        return json.dumps({
            "patron": "Event-Driven Architecture",
            "descripcion": "Los servicios se comunican mediante eventos, sin acoplamiento directo",
            "pros": ["Desacoplamiento total", "Alta resiliencia a fallos parciales", "Auditabilidad nativa", "Fácil añadir consumidores"],
            "contras": ["Orden de eventos no garantizado (sin FIFO)", "Idempotencia requerida en consumidores", "Debugging más complejo"],
            "aws_clave": ["EventBridge", "SQS/SNS", "Kinesis Data Streams", "Lambda como consumidor"]
        }, ensure_ascii=False, indent=2)

    elif any(k in esc for k in ["función", "serverless", "lambda", "trigger", "esporádico", "bajo tráfico"]):
        return json.dumps({
            "patron": "Serverless",
            "descripcion": "Funciones como unidad de despliegue, pago por ejecución",
            "pros": ["Cero gestión de infraestructura", "Pago por uso real", "Escala automática a millones de req/s", "Escala a cero en reposo"],
            "contras": ["Cold starts de 100-500ms", "Límite de 15 min por ejecución en Lambda", "Vendor lock-in elevado", "Debugging más difícil"],
            "aws_clave": ["Lambda", "API Gateway", "DynamoDB On-Demand", "Step Functions para orquestación"]
        }, ensure_ascii=False, indent=2)

    elif any(k in esc for k in ["migrar", "legacy", "monolito", "existente", "modernizar"]):
        return json.dumps({
            "patron": "Strangler Fig (Migración Gradual)",
            "descripcion": "Envolver el sistema legacy con nuevos servicios, reemplazando funcionalidad progresivamente",
            "pros": ["Sin big-bang rewrite", "Valor de negocio continuo durante migración", "Rollback granular por funcionalidad"],
            "contras": ["Periodo de coexistencia complejo", "Dos sistemas en producción simultáneamente", "Requiere API Gateway como facade"],
            "aws_clave": ["API Gateway como facade", "Lambda Authorizers", "DMS para migración de datos", "Route53 para corte de tráfico gradual"]
        }, ensure_ascii=False, indent=2)

    else:
        return json.dumps({
            "patron": "3-Tier Architecture",
            "descripcion": "Presentación → Lógica de negocio → Datos, con separación clara por capas",
            "pros": ["Simplicidad operativa", "Transacciones ACID nativas", "Fácil razonamiento y debugging", "Patrón probado en miles de proyectos"],
            "contras": ["Escala de todo o nada", "Deploy completo por cualquier cambio", "Posible cuello de botella en base de datos"],
            "aws_clave": ["ALB + ECS/EC2", "RDS Multi-AZ", "ElastiCache para capa de caché", "CloudFront para assets estáticos"]
        }, ensure_ascii=False, indent=2)


@tool
def calcular_sla_disponibilidad(nines: int) -> str:
    """Calcula el tiempo de inactividad permitido para un SLA dado en número de 'nines' (1-5).
    Ej: 3 = 99.9%, 4 = 99.99%, 5 = 99.999%"""
    tabla = {
        1: ("90%",     "36.5 días/año",  "72 horas/mes",   "EC2 Single-AZ"),
        2: ("99%",     "3.65 días/año",  "7.2 horas/mes",  "EC2 + RDS Single-AZ"),
        3: ("99.9%",   "8.76 horas/año", "43.8 min/mes",   "ALB + Auto Scaling + RDS Multi-AZ"),
        4: ("99.99%",  "52.6 min/año",   "4.38 min/mes",   "Multi-AZ + Route53 Health Checks + RDS Aurora Global"),
        5: ("99.999%", "5.26 min/año",   "26 seg/mes",     "Multi-Region Active-Active + Global Accelerator + Aurora Global"),
    }
    n = max(1, min(5, nines))
    pct, anual, mensual, estrategia = tabla[n]
    return json.dumps({
        "sla": pct,
        "downtime_anual": anual,
        "downtime_mensual": mensual,
        "estrategia_aws": estrategia,
        "rto_objetivo": f"< {['1h', '30min', '15min', '5min', '1min'][n-1]}",
        "rpo_objetivo": f"< {['24h', '4h', '1h', '15min', '5min'][n-1]}",
    }, ensure_ascii=False, indent=2)


# ═══════════════════════════════════════════════════════════════════════════════
# HERRAMIENTAS DEL AGENTE DE SEGURIDAD
# ═══════════════════════════════════════════════════════════════════════════════

@tool
def generar_checklist_seguridad(contexto: str) -> str:
    """Genera un checklist de controles de seguridad según el contexto del sistema."""
    checklist = {
        "IAM y Control de Acceso": [
            "Principio de mínimo privilegio en todos los roles IAM",
            "MFA obligatorio para usuarios con acceso a consola AWS",
            "Rotar access keys cada 90 días (automatizable con Secrets Manager)",
            "Usar IAM Roles para EC2/ECS/Lambda — nunca access keys embebidas",
            "AWS Organizations + SCPs para control multi-cuenta",
        ],
        "Protección de Red": [
            "VPC con subredes públicas y privadas (bases de datos siempre en privada)",
            "Security Groups con reglas restrictivas (deny-all por defecto)",
            "NACLs como segunda capa de defensa en subredes sensibles",
            "VPC Flow Logs habilitados en todas las subredes para auditoría forense",
            "AWS WAF delante de ALB/API Gateway con reglas OWASP Core Rule Set",
        ],
        "Protección de Datos": [
            "Cifrado en reposo con KMS Customer Managed Keys (CMK)",
            "TLS 1.2+ (preferiblemente 1.3) para todo tráfico en tránsito",
            "S3 Block Public Access habilitado a nivel de cuenta",
            "RDS con cifrado habilitado y snapshots cifrados automáticamente",
            "AWS Macie para detección de PII y datos sensibles en S3",
        ],
        "Monitoreo y Detección": [
            "CloudTrail activo en todas las regiones con log file validation",
            "GuardDuty habilitado (detección de amenazas con ML)",
            "AWS Config Rules para detectar desviaciones de baseline",
            "SecurityHub para vista consolidada de hallazgos (score CIS/FSBP)",
            "Alertas CloudWatch para acciones privilegiadas (root login, cambios IAM)",
        ],
    }

    ctx = contexto.lower()
    if any(k in ctx for k in ["pci", "tarjeta", "pago", "card"]):
        checklist["PCI-DSS Específico"] = [
            "Segmentación de red para entorno de titular de tarjeta (CDE)",
            "Logs inmutables por mínimo 1 año (S3 Object Lock WORM)",
            "Penetration testing anual obligatorio",
            "AWS Shield Advanced para protección DDoS en entornos de pago",
        ]

    if any(k in ctx for k in ["gdpr", "datos personales", "usuarios europeos", "eu", "europa"]):
        checklist["GDPR Específico"] = [
            "Data Processing Agreement (DPA) firmado con AWS",
            "Registros de tratamiento de datos (Art. 30)",
            "Mecanismo de borrado por solicitud (derecho al olvido)",
            "Transferencias internacionales mediante SCCs o AWS Data Boundary",
        ]

    return json.dumps(checklist, ensure_ascii=False, indent=2)


@tool
def identificar_vulnerabilidades_comunes(tipo_sistema: str) -> str:
    """Identifica vulnerabilidades OWASP y riesgos comunes para un tipo de sistema.
    Tipos reconocidos: api, ecommerce, microservicios, legacy, saas, mobile"""
    vulnerabilidades = {
        "api": [
            "OWASP API1:2023 — Broken Object Level Authorization (BOLA/IDOR)",
            "OWASP API3:2023 — Broken Object Property Level Authorization",
            "Inyección SQL/NoSQL en parámetros de query y cuerpo de petición",
            "JWT sin rotación de secretos ni validación de audiencia",
            "Rate limiting ausente → abuso de endpoints costosos",
        ],
        "ecommerce": [
            "OWASP A03:2021 — Injection (SQLi en búsquedas y filtros de catálogo)",
            "OWASP A07:2021 — Authentication failures en checkout y recuperación de cuenta",
            "Skimming de tarjetas via scripts maliciosos en frontend (Magecart)",
            "Race conditions en gestión de inventario y cupones de descuento",
            "SSRF en funcionalidades de importación de productos (URLs externas)",
        ],
        "microservicios": [
            "Comunicación inter-servicio sin mTLS (lateral movement si un servicio es comprometido)",
            "SSRF entre servicios internos via headers mal validados",
            "Secretos en variables de entorno en texto plano (usar Secrets Manager)",
            "Ausencia de circuit breaker → cascada de fallos en alta disponibilidad",
            "Imágenes Docker con vulnerabilidades de base OS (usar ECR Image Scanning)",
        ],
        "legacy": [
            "Credenciales hardcodeadas en archivos de configuración y código fuente",
            "Ausencia de logs de auditoría para acciones privilegiadas",
            "Dependencias desactualizadas con CVEs conocidos (OWASP A06:2021)",
            "Comunicación en texto plano entre componentes internos",
            "Gestión de sesiones sin tokens CSRF ni expiración adecuada",
        ],
    }

    tipo = tipo_sistema.lower()
    key = "api"
    if any(k in tipo for k in ["ecommerce", "tienda", "shop", "magento", "woocommerce"]):
        key = "ecommerce"
    elif any(k in tipo for k in ["microservicio", "microserv", "kubernetes", "eks"]):
        key = "microservicios"
    elif any(k in tipo for k in ["legacy", "cobol", "mainframe", "antiguo", "monolito"]):
        key = "legacy"

    return json.dumps({
        "tipo_sistema": tipo_sistema,
        "vulnerabilidades_criticas": vulnerabilidades[key],
        "herramienta_escaneo": "AWS Inspector v2 + ECR Image Scanning + Dependabot"
    }, ensure_ascii=False, indent=2)


@tool
def estimar_nivel_cumplimiento(normativa: str) -> str:
    """Devuelve los requisitos clave y controles AWS para una normativa de seguridad.
    Normativas soportadas: GDPR, PCI-DSS, SOC2, ISO27001, HIPAA"""
    normativas = {
        "gdpr": {
            "descripcion": "Reglamento General de Protección de Datos (UE 2016/679)",
            "obligatorio_para": "Cualquier empresa que trate datos de ciudadanos de la UE",
            "controles_clave": [
                "Base legal documentada para cada tratamiento (Art. 6)",
                "Derecho al olvido implementable (borrado definitivo de datos)",
                "Notificación de brecha en <72 horas a autoridad supervisora",
                "Data Protection Officer (DPO) si tratamiento a gran escala",
                "Privacy by Design en nuevos sistemas",
            ],
            "aws_servicios": ["Macie (detección PII)", "KMS (cifrado)", "CloudTrail (auditabilidad)", "Config (compliance continuo)", "Lake Formation (control acceso datos)"],
            "aws_programa": "AWS GDPR Center + DPA disponible en aws.amazon.com/compliance/gdpr-center"
        },
        "pci-dss": {
            "descripcion": "Payment Card Industry Data Security Standard v4.0",
            "obligatorio_para": "Cualquier entidad que procese, almacene o transmita datos de tarjetas",
            "controles_clave": [
                "Segmentación de red para el Cardholder Data Environment (CDE)",
                "TLS 1.2+ obligatorio, prohibición de SSL/TLS antiguo",
                "Logs inmutables 12 meses, 3 meses online accesibles",
                "Penetration testing anual por QSA certificado",
                "Escaneo de vulnerabilidades trimestral (ASV approved)",
            ],
            "aws_servicios": ["WAF (OWASP managed rules)", "Shield Advanced", "CloudWatch Logs con S3 Object Lock", "Inspector (vuln scanning)", "Secrets Manager (gestión de claves)"],
            "aws_programa": "AWS es QSA-certified PCI DSS Level 1 Service Provider"
        },
        "soc2": {
            "descripcion": "Service Organization Control 2 (AICPA Trust Services Criteria)",
            "obligatorio_para": "SaaS y proveedores de servicios con datos de clientes empresariales",
            "controles_clave": [
                "CC6 — Control de acceso lógico y físico",
                "CC7 — Monitoreo del sistema y detección de anomalías",
                "A1 — Disponibilidad según SLA comprometido",
                "PI1 — Procesamiento íntegro y preciso",
                "Evidencias auditables para cada control (automation recomendada)",
            ],
            "aws_servicios": ["IAM Access Analyzer", "CloudWatch + Alarms", "Config Rules", "Security Hub", "AWS Audit Manager"],
            "aws_programa": "SOC 1/2/3 reports disponibles en AWS Artifact (gratuito para clientes)"
        },
        "hipaa": {
            "descripcion": "Health Insurance Portability and Accountability Act (EEUU)",
            "obligatorio_para": "Covered Entities y Business Associates que manejan PHI",
            "controles_clave": [
                "BAA (Business Associate Agreement) firmado con AWS",
                "Cifrado de PHI en reposo y en tránsito (AES-256, TLS 1.2+)",
                "Controles de acceso único por usuario (no compartir credenciales)",
                "Logs de auditoría de acceso a PHI mínimo 6 años",
                "Plan de respuesta a incidentes documentado y probado",
            ],
            "aws_servicios": ["HealthLake", "KMS", "CloudTrail", "Macie", "S3 (HIPAA eligible)"],
            "aws_programa": "AWS HIPAA Compliance Program — lista de servicios HIPAA eligible en aws.amazon.com/compliance/hipaa-eligible-services-reference"
        },
    }

    key = normativa.lower().replace(" ", "-").replace("_", "-")
    if key not in normativas:
        return json.dumps({
            "error": f"Normativa '{normativa}' no encontrada.",
            "normativas_disponibles": list(normativas.keys())
        }, ensure_ascii=False)

    return json.dumps(normativas[key], ensure_ascii=False, indent=2)


# ═══════════════════════════════════════════════════════════════════════════════
# HERRAMIENTAS DEL AGENTE FINOPS
# ═══════════════════════════════════════════════════════════════════════════════

@tool
def estimar_costo_mensual_aws(servicios: str) -> str:
    """Estima el costo mensual aproximado en USD de una lista de servicios AWS.
    Input: servicios separados por coma (ej: 'ECS Fargate, RDS Aurora, ALB, CloudFront').
    Precios base en us-east-1, instancias medianas para 10k usuarios/día."""
    precios_base = {
        "ec2 t3.micro":           8.47,
        "ec2 t3.small":          16.94,
        "ec2 t3.medium":         33.87,
        "ec2 t3.large":          67.74,
        "ec2 m5.large":          87.60,
        "ec2 m5.xlarge":        175.20,
        "ecs fargate":           45.00,
        "eks":                  144.00,
        "rds aurora serverless":  43.80,
        "rds":                   64.22,
        "rds multi-az":         128.44,
        "elasticache redis":     24.48,
        "alb":                   22.27,
        "nat gateway":           45.00,
        "cloudfront":            15.00,
        "s3":                    23.00,
        "lambda":                 5.00,
        "api gateway":           15.00,
        "sqs":                    4.00,
        "sns":                    2.00,
        "eventbridge":            1.00,
        "waf":                   22.00,
        "shield advanced":     3000.00,
        "cloudwatch":            20.00,
        "secrets manager":        5.00,
        "kms":                    3.00,
        "guardduty":             15.00,
        "security hub":           5.00,
    }

    items = [s.strip().lower() for s in servicios.split(",")]
    desglose = []
    total = 0.0

    for item in items:
        precio_encontrado = None
        nombre_encontrado = item
        for key, precio in precios_base.items():
            if key in item or all(part in item for part in key.split() if len(part) > 2):
                precio_encontrado = precio
                nombre_encontrado = key.title()
                break
        if precio_encontrado is None:
            precio_encontrado = 35.0
            nombre_encontrado = item.title() + " (estimado)"
        desglose.append({"servicio": nombre_encontrado, "usd_mes": round(precio_encontrado, 2)})
        total += precio_encontrado

    return json.dumps({
        "desglose": desglose,
        "total_mensual_usd": round(total, 2),
        "total_anual_usd": round(total * 12, 2),
        "nota": "Estimación ±30%. Precios us-east-1, uso moderado. Usar AWS Pricing Calculator para presupuesto formal.",
    }, ensure_ascii=False, indent=2)


@tool
def calcular_ahorro_spot(tipo_instancia: str, horas_mes: int) -> str:
    """Calcula el ahorro potencial al usar instancias Spot vs On-Demand para EC2.
    tipo_instancia: familia y tamaño (ej: 'm5.large', 'c5.xlarge', 't3.medium').
    horas_mes: horas de uso esperado (720 = 24/7, 160 = horario laboral)."""
    precios_od_hora = {
        "t3.micro": 0.0104, "t3.small": 0.0208, "t3.medium": 0.0416, "t3.large": 0.0832,
        "m5.large": 0.096,  "m5.xlarge": 0.192,  "m5.2xlarge": 0.384,
        "c5.large": 0.085,  "c5.xlarge": 0.170,  "c5.2xlarge": 0.340,
        "r5.large": 0.126,  "r5.xlarge": 0.252,  "r5.2xlarge": 0.504,
    }
    descuentos_spot_familia = {
        "t3": 0.65, "m5": 0.72, "c5": 0.70, "r5": 0.68, "default": 0.65,
    }

    tipo_lower = tipo_instancia.lower().strip()
    precio_hora = precios_od_hora.get(tipo_lower, 0.096)
    familia = tipo_lower.split(".")[0] if "." in tipo_lower else "default"
    descuento = descuentos_spot_familia.get(familia, descuentos_spot_familia["default"])

    costo_od    = round(precio_hora * horas_mes, 2)
    costo_spot  = round(costo_od * (1 - descuento), 2)
    ahorro_mes  = round(costo_od - costo_spot, 2)
    ahorro_anio = round(ahorro_mes * 12, 2)

    return json.dumps({
        "instancia": tipo_instancia,
        "horas_mes": horas_mes,
        "costo_on_demand_usd_mes": costo_od,
        "costo_spot_usd_mes": costo_spot,
        "ahorro_mensual_usd": ahorro_mes,
        "ahorro_anual_usd": ahorro_anio,
        "descuento_aplicado": f"{int(descuento * 100)}%",
        "advertencia": "Spot puede interrumpirse con 2 min de aviso. Solo para cargas tolerantes a fallos: batch, CI/CD, procesamiento de imágenes.",
        "casos_uso_recomendados": ["Jobs de procesamiento asíncrono", "Pipelines de CI/CD", "Entornos de staging/QA", "Workers de colas SQS"],
    }, ensure_ascii=False, indent=2)


@tool
def recomendar_plan_ahorro(descripcion_uso: str) -> str:
    """Recomienda la estrategia de compromiso de costos AWS más adecuada según el patrón de uso.
    descripcion_uso: descripción libre del patrón (ej: '24/7 producción estable', 'tráfico variable con picos', 'solo horario laboral')."""
    uso = descripcion_uso.lower()

    if any(k in uso for k in ["24/7", "continuo", "siempre activo", "producción estable", "constante"]):
        return json.dumps({
            "recomendacion": "Savings Plans (Compute) 1 año — No Upfront",
            "ahorro_vs_od": "40-66%",
            "compromiso": "1 año, pago mensual sin pago anticipado",
            "razon": "Carga base constante: el break-even con Savings Plans se alcanza a los 7-8 meses",
            "alternativa": "Reserved Instances 3 años All-Upfront si hay certeza del tamaño de instancia (hasta 72% ahorro)",
            "pasos": [
                "1. Analizar 2 semanas de uso con AWS Cost Explorer",
                "2. Identificar el baseline de cómputo (percentil 10 del uso)",
                "3. Cubrir ese baseline con Savings Plans",
                "4. Cubrir picos con On-Demand",
            ]
        }, ensure_ascii=False, indent=2)

    elif any(k in uso for k in ["variable", "pico", "fluctúa", "estacional", "black friday", "evento"]):
        return json.dumps({
            "recomendacion": "Savings Plans (baseline) + Spot Instances (picos) + On-Demand (overflow)",
            "ahorro_vs_od": "30-40% base + hasta 72% en picos con Spot",
            "compromiso": "Savings Plans 1 año flexible, sin compromiso para Spot/OD",
            "razon": "Tráfico variable requiere flexibilidad. Savings Plans cubren el piso, Spot los picos predecibles",
            "pasos": [
                "1. Calcular el 20% del pico como baseline para Savings Plans",
                "2. Configurar Spot en Auto Scaling Groups con capacidad mínima On-Demand (20%)",
                "3. Usar Capacity-Optimized allocation strategy para Spot",
                "4. Pre-warming programado antes de eventos conocidos (scheduled scaling)",
            ]
        }, ensure_ascii=False, indent=2)

    else:
        return json.dumps({
            "recomendacion": "On-Demand + Right-Sizing mensual",
            "ahorro_vs_od": "15-25% solo con right-sizing",
            "compromiso": "Sin compromiso",
            "razon": "Uso impredecible: no comprometer capacidad. Optimizar con right-sizing primero",
            "pasos": [
                "1. Activar AWS Compute Optimizer (gratuito)",
                "2. Aplicar recomendaciones de right-sizing en instancias con <40% CPU promedio",
                "3. Revisar y eliminar recursos huérfanos (snapshots, EIPs sin usar, LBs vacíos)",
                "4. Reevaluar compromisos en 3 meses con datos reales",
            ]
        }, ensure_ascii=False, indent=2)
