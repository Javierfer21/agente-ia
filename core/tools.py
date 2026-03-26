import json
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
        servicios.append({"servicio": "CloudFront", "razon": "CDN global con 400+ puntos de presencia para reducir latencia y carga en origen"})

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

    return json.dumps({
        "servicios_recomendados": servicios,
        "fuentes": [
            {"descripcion": "AWS Architecture Center — catálogo oficial de patrones y servicios", "url": "https://aws.amazon.com/architecture/"},
            {"descripcion": "AWS Well-Architected Framework — guía de buenas prácticas de diseño cloud", "url": "https://aws.amazon.com/architecture/well-architected/"},
            {"descripcion": "AWS Products & Services — listado completo con documentación técnica", "url": "https://aws.amazon.com/products/"},
        ]
    }, ensure_ascii=False, indent=2)


@tool
def evaluar_patron_arquitectura(escenario: str) -> str:
    """Recomienda el patrón de arquitectura más adecuado dado un escenario de negocio.
    Retorna el patrón, sus pros, contras y servicios AWS clave."""
    esc = escenario.lower()

    fuentes = [
        {"descripcion": "Martin Fowler — Patterns of Enterprise Application Architecture", "url": "https://martinfowler.com/eaaCatalog/"},
        {"descripcion": "AWS Well-Architected Framework — Reliability Pillar", "url": "https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/welcome.html"},
        {"descripcion": "AWS Prescriptive Guidance — Architecture patterns", "url": "https://docs.aws.amazon.com/prescriptive-guidance/latest/patterns/architectural-patterns.html"},
    ]

    if any(k in esc for k in ["microservicio", "equipo independiente", "despliegue independiente", "soa"]):
        resultado = {
            "patron": "Microservicios",
            "descripcion": "Servicios pequeños e independientes, cada uno con su propia base de datos",
            "pros": ["Equipos autónomos", "Escalado independiente por servicio", "Tecnologías heterogéneas", "Tolerancia a fallos parciales"],
            "contras": ["Complejidad operativa alta", "Latencia de red entre servicios", "Distributed tracing necesario", "Gestión de transacciones distribuidas"],
            "aws_clave": ["EKS/ECS", "API Gateway", "Service Mesh (AWS App Mesh)", "X-Ray para trazabilidad"],
        }
    elif any(k in esc for k in ["event", "mensaje", "cola", "stream", "asíncrono", "kafka"]):
        resultado = {
            "patron": "Event-Driven Architecture",
            "descripcion": "Los servicios se comunican mediante eventos, sin acoplamiento directo",
            "pros": ["Desacoplamiento total", "Alta resiliencia a fallos parciales", "Auditabilidad nativa", "Fácil añadir consumidores"],
            "contras": ["Orden de eventos no garantizado (sin FIFO)", "Idempotencia requerida en consumidores", "Debugging más complejo"],
            "aws_clave": ["EventBridge", "SQS/SNS", "Kinesis Data Streams", "Lambda como consumidor"],
        }
    elif any(k in esc for k in ["función", "serverless", "lambda", "trigger", "esporádico", "bajo tráfico"]):
        resultado = {
            "patron": "Serverless",
            "descripcion": "Funciones como unidad de despliegue, pago por ejecución",
            "pros": ["Cero gestión de infraestructura", "Pago por uso real", "Escala automática a millones de req/s", "Escala a cero en reposo"],
            "contras": ["Cold starts de 100-500ms", "Límite de 15 min por ejecución en Lambda", "Vendor lock-in elevado", "Debugging más difícil"],
            "aws_clave": ["Lambda", "API Gateway", "DynamoDB On-Demand", "Step Functions para orquestación"],
        }
    elif any(k in esc for k in ["migrar", "legacy", "monolito", "existente", "modernizar"]):
        resultado = {
            "patron": "Strangler Fig (Migración Gradual)",
            "descripcion": "Envolver el sistema legacy con nuevos servicios, reemplazando funcionalidad progresivamente",
            "pros": ["Sin big-bang rewrite", "Valor de negocio continuo durante migración", "Rollback granular por funcionalidad"],
            "contras": ["Periodo de coexistencia complejo", "Dos sistemas en producción simultáneamente", "Requiere API Gateway como facade"],
            "aws_clave": ["API Gateway como facade", "Lambda Authorizers", "DMS para migración de datos", "Route53 para corte de tráfico gradual"],
        }
    else:
        resultado = {
            "patron": "3-Tier Architecture",
            "descripcion": "Presentación → Lógica de negocio → Datos, con separación clara por capas",
            "pros": ["Simplicidad operativa", "Transacciones ACID nativas", "Fácil razonamiento y debugging", "Patrón probado en miles de proyectos"],
            "contras": ["Escala de todo o nada", "Deploy completo por cualquier cambio", "Posible cuello de botella en base de datos"],
            "aws_clave": ["ALB + ECS/EC2", "RDS Multi-AZ", "ElastiCache para capa de caché", "CloudFront para assets estáticos"],
        }

    resultado["fuentes"] = fuentes
    return json.dumps(resultado, ensure_ascii=False, indent=2)


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
        "fuentes": [
            {"descripcion": "AWS Service Level Agreements — SLAs oficiales por servicio", "url": "https://aws.amazon.com/legal/service-level-agreements/"},
            {"descripcion": "AWS Whitepaper: Availability and Beyond — estrategias de resiliencia", "url": "https://docs.aws.amazon.com/whitepapers/latest/availability-and-beyond-improving-resilience/availability-and-beyond-improving-resilience.html"},
            {"descripcion": "AWS Well-Architected: Reliability Pillar — objetivos RTO/RPO", "url": "https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/welcome.html"},
        ]
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

    if any(k in ctx for k in ["gdpr", "datos personales", "salud", "médico", "paciente", "eu", "europa", "españa"]):
        checklist["GDPR / LOPDGDD Específico"] = [
            "Data Processing Agreement (DPA) firmado con AWS (disponible en AWS Artifact)",
            "Registros de actividades de tratamiento obligatorios (Art. 30 RGPD)",
            "Mecanismo de borrado por solicitud del interesado (derecho al olvido)",
            "Notificación de brecha a la AEPD en menos de 72 horas (Art. 33 RGPD)",
            "Transferencias internacionales solo mediante Cláusulas Contractuales Tipo (CCT) o AWS Data Boundary EU",
        ]

    checklist["fuentes"] = [
        {"descripcion": "CIS AWS Foundations Benchmark v2.0 — checklist de referencia para hardening AWS", "url": "https://www.cisecurity.org/benchmark/amazon_web_services"},
        {"descripcion": "AWS Security Best Practices — guía oficial de seguridad en la nube", "url": "https://aws.amazon.com/security/security-learning/?nc1=h_ls"},
        {"descripcion": "AWS Well-Architected: Security Pillar", "url": "https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/welcome.html"},
        {"descripcion": "AEPD — Agencia Española de Protección de Datos (normativa LOPDGDD)", "url": "https://www.aepd.es/"},
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
        "herramienta_escaneo": "AWS Inspector v2 + ECR Image Scanning + Dependabot",
        "fuentes": [
            {"descripcion": "OWASP Top 10:2021 — diez riesgos de seguridad más críticos en aplicaciones web", "url": "https://owasp.org/www-project-top-ten/"},
            {"descripcion": "OWASP API Security Top 10:2023 — vulnerabilidades específicas de APIs", "url": "https://owasp.org/www-project-api-security/"},
            {"descripcion": "CVE Program — base de datos pública de vulnerabilidades conocidas (MITRE)", "url": "https://www.cve.org/"},
            {"descripcion": "AWS Inspector — documentación del servicio de análisis de vulnerabilidades", "url": "https://aws.amazon.com/inspector/"},
        ]
    }, ensure_ascii=False, indent=2)


@tool
def estimar_nivel_cumplimiento(normativa: str) -> str:
    """Devuelve los requisitos clave y controles AWS para una normativa de seguridad.
    Normativas soportadas: GDPR, PCI-DSS, SOC2, ISO27001, HIPAA"""
    normativas = {
        "gdpr": {
            "descripcion": "Reglamento General de Protección de Datos (UE 2016/679) — transpuesto en España mediante LOPDGDD",
            "obligatorio_para": "Cualquier empresa que trate datos de ciudadanos de la UE, incluyendo todas las empresas españolas",
            "autoridad_supervisora_espana": "AEPD — Agencia Española de Protección de Datos (www.aepd.es)",
            "controles_clave": [
                "Base legal documentada para cada tratamiento (Art. 6 RGPD)",
                "Derecho al olvido implementable (borrado definitivo de datos del interesado)",
                "Notificación de brecha a la AEPD en <72 horas (Art. 33 RGPD)",
                "Data Protection Officer (DPO) obligatorio si tratamiento a gran escala o datos sensibles",
                "Privacy by Design y Privacy by Default en nuevos sistemas (Art. 25 RGPD)",
            ],
            "aws_servicios": ["Macie (detección PII)", "KMS (cifrado CMK)", "CloudTrail (auditabilidad)", "Config (compliance continuo)", "Lake Formation (control acceso datos)"],
            "fuentes": [
                {"descripcion": "Texto completo del RGPD — EUR-Lex (Diario Oficial de la UE)", "url": "https://eur-lex.europa.eu/legal-content/ES/TXT/?uri=CELEX:32016R0679"},
                {"descripcion": "AEPD — Guías y herramientas para cumplimiento RGPD en España", "url": "https://www.aepd.es/guias-y-herramientas"},
                {"descripcion": "AWS GDPR Center — DPA y recursos de cumplimiento", "url": "https://aws.amazon.com/compliance/gdpr-center/"},
            ]
        },
        "pci-dss": {
            "descripcion": "Payment Card Industry Data Security Standard v4.0",
            "obligatorio_para": "Cualquier entidad que procese, almacene o transmita datos de tarjetas de pago",
            "controles_clave": [
                "Segmentación de red para el Cardholder Data Environment (CDE)",
                "TLS 1.2+ obligatorio, prohibición de SSL/TLS antiguo",
                "Logs inmutables 12 meses, 3 meses online accesibles",
                "Penetration testing anual por QSA certificado",
                "Escaneo de vulnerabilidades trimestral (ASV aprobado)",
            ],
            "aws_servicios": ["WAF (OWASP managed rules)", "Shield Advanced", "CloudWatch Logs con S3 Object Lock", "Inspector (vuln scanning)", "Secrets Manager"],
            "fuentes": [
                {"descripcion": "PCI Security Standards Council — documentos oficiales PCI-DSS v4.0", "url": "https://www.pcisecuritystandards.org/document_library/"},
                {"descripcion": "AWS PCI DSS Compliance — guía de responsabilidad compartida", "url": "https://aws.amazon.com/compliance/pci-dss-level-1-faqs/"},
                {"descripcion": "PCI DSS Quick Reference Guide (PDF oficial)", "url": "https://www.pcisecuritystandards.org/pdfs/pci_ssc_quick_guide.pdf"},
            ]
        },
        "soc2": {
            "descripcion": "Service Organization Control 2 (AICPA Trust Services Criteria)",
            "obligatorio_para": "SaaS y proveedores de servicios con datos de clientes empresariales",
            "controles_clave": [
                "CC6 — Control de acceso lógico y físico",
                "CC7 — Monitoreo del sistema y detección de anomalías",
                "A1 — Disponibilidad según SLA comprometido",
                "PI1 — Procesamiento íntegro y preciso",
                "Evidencias auditables para cada control (automatización recomendada)",
            ],
            "aws_servicios": ["IAM Access Analyzer", "CloudWatch + Alarms", "Config Rules", "Security Hub", "AWS Audit Manager"],
            "fuentes": [
                {"descripcion": "AICPA — SOC 2 Trust Services Criteria (documentación oficial)", "url": "https://www.aicpa-cima.com/resources/landing/system-and-organization-controls-soc-suite-of-services"},
                {"descripcion": "AWS Audit Manager — automatización de evidencias para SOC 2", "url": "https://aws.amazon.com/audit-manager/"},
                {"descripcion": "AWS Artifact — acceso a informes SOC 1/2/3 de AWS (gratuito para clientes)", "url": "https://aws.amazon.com/artifact/"},
            ]
        },
        "hipaa": {
            "descripcion": "Health Insurance Portability and Accountability Act (EEUU) — referencia para proyectos con datos sanitarios",
            "obligatorio_para": "Covered Entities y Business Associates que manejan Protected Health Information (PHI)",
            "nota_espana": "En España aplica el ENS (Esquema Nacional de Seguridad) y el Art. 9 RGPD para datos de salud",
            "controles_clave": [
                "BAA (Business Associate Agreement) firmado con AWS",
                "Cifrado de PHI en reposo y en tránsito (AES-256, TLS 1.2+)",
                "Controles de acceso único por usuario (prohibido compartir credenciales)",
                "Logs de auditoría de acceso a PHI mínimo 6 años",
                "Plan de respuesta a incidentes documentado y probado",
            ],
            "aws_servicios": ["HealthLake", "KMS", "CloudTrail", "Macie", "S3 (HIPAA eligible)"],
            "fuentes": [
                {"descripcion": "HHS.gov — HIPAA Security Rule oficial (Departamento de Salud EEUU)", "url": "https://www.hhs.gov/hipaa/for-professionals/security/index.html"},
                {"descripcion": "AWS HIPAA Compliance — lista de servicios HIPAA eligible", "url": "https://aws.amazon.com/compliance/hipaa-eligible-services-reference/"},
                {"descripcion": "CCN-CERT — Esquema Nacional de Seguridad (ENS) para entidades españolas", "url": "https://www.ccn-cert.cni.es/es/series-ccn-stic/guias/guias-de-acceso-publico-ccn-stic.html"},
            ]
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
# Precios basados en región eu-west-1 (Irlanda) — la región AWS más cercana a España
# Expresados en EUR (tipo de cambio referencia: 1 USD ≈ 0,92 EUR, BCE 2025)
# ═══════════════════════════════════════════════════════════════════════════════

@tool
def estimar_costo_mensual_aws(servicios: str) -> str:
    """Estima el coste mensual aproximado en EUR de una lista de servicios AWS.
    Input: servicios separados por coma (ej: 'ECS Fargate, RDS Aurora, ALB, CloudFront').
    Precios base en eu-west-1 (Irlanda), instancias medianas para uso moderado."""
    # Precios en EUR — región eu-west-1 (Irlanda), uso estándar
    # Fuente: AWS Pricing Calculator + tipo de cambio BCE (1 USD = 0,92 EUR)
    precios_base_eur = {
        "ec2 t3.micro":            7.80,
        "ec2 t3.small":           15.59,
        "ec2 t3.medium":          31.18,
        "ec2 t3.large":           62.37,
        "ec2 m5.large":           88.55,
        "ec2 m5.xlarge":         177.10,
        "ecs fargate":            47.15,
        "eks":                   147.20,
        "rds aurora serverless":  45.22,
        "rds":                    66.35,
        "rds multi-az":          132.70,
        "elasticache redis":      25.28,
        "alb":                    22.99,
        "nat gateway":            46.45,
        "cloudfront":             15.50,
        "s3":                     23.75,
        "lambda":                  5.15,
        "api gateway":            15.50,
        "sqs":                     4.13,
        "sns":                     2.07,
        "eventbridge":             1.03,
        "waf":                    22.72,
        "shield advanced":      2760.00,
        "cloudwatch":             20.65,
        "secrets manager":         5.16,
        "kms":                     3.10,
        "guardduty":              15.48,
        "security hub":            5.16,
    }

    items = [s.strip().lower() for s in servicios.split(",")]
    desglose = []
    total = 0.0

    for item in items:
        precio_encontrado = None
        nombre_encontrado = item
        for key, precio in precios_base_eur.items():
            if key in item or all(part in item for part in key.split() if len(part) > 2):
                precio_encontrado = precio
                nombre_encontrado = key.title()
                break
        if precio_encontrado is None:
            precio_encontrado = 32.20
            nombre_encontrado = item.title() + " (estimado)"
        desglose.append({"servicio": nombre_encontrado, "eur_mes": round(precio_encontrado, 2)})
        total += precio_encontrado

    return json.dumps({
        "region": "eu-west-1 (Irlanda) — región AWS más cercana a España",
        "desglose": desglose,
        "total_mensual_eur": round(total, 2),
        "total_anual_eur": round(total * 12, 2),
        "nota": "Estimación orientativa ±30%. IVA no incluido. Usar AWS Pricing Calculator para presupuesto formal.",
        "fuentes": [
            {"descripcion": "AWS Pricing Calculator — herramienta oficial de estimación de costes", "url": "https://calculator.aws/pricing/2/home"},
            {"descripcion": "AWS EC2 Pricing eu-west-1 — precios On-Demand actualizados", "url": "https://aws.amazon.com/ec2/pricing/on-demand/"},
            {"descripcion": "AWS RDS Pricing — precios por motor y región", "url": "https://aws.amazon.com/rds/pricing/"},
            {"descripcion": "Banco Central Europeo — tipo de cambio EUR/USD de referencia", "url": "https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/index.en.html"},
        ]
    }, ensure_ascii=False, indent=2)


@tool
def calcular_ahorro_spot(tipo_instancia: str, horas_mes: int) -> str:
    """Calcula el ahorro potencial al usar instancias Spot vs On-Demand para EC2.
    tipo_instancia: familia y tamaño (ej: 'm5.large', 'c5.xlarge', 't3.medium').
    horas_mes: horas de uso esperado (720 = 24/7, 160 = horario laboral)."""
    # Precios On-Demand en EUR — eu-west-1 (Irlanda)
    precios_od_hora_eur = {
        "t3.micro":  0.0114, "t3.small":  0.0228, "t3.medium": 0.0456, "t3.large":  0.0912,
        "m5.large":  0.1070, "m5.xlarge": 0.2140, "m5.2xlarge": 0.4280,
        "c5.large":  0.0970, "c5.xlarge": 0.1940, "c5.2xlarge": 0.3880,
        "r5.large":  0.1440, "r5.xlarge": 0.2880, "r5.2xlarge": 0.5760,
    }
    descuentos_spot_familia = {
        "t3": 0.65, "m5": 0.72, "c5": 0.70, "r5": 0.68, "default": 0.65,
    }

    tipo_lower = tipo_instancia.lower().strip()
    precio_hora = precios_od_hora_eur.get(tipo_lower, 0.107)
    familia = tipo_lower.split(".")[0] if "." in tipo_lower else "default"
    descuento = descuentos_spot_familia.get(familia, descuentos_spot_familia["default"])

    costo_od    = round(precio_hora * horas_mes, 2)
    costo_spot  = round(costo_od * (1 - descuento), 2)
    ahorro_mes  = round(costo_od - costo_spot, 2)
    ahorro_anio = round(ahorro_mes * 12, 2)

    return json.dumps({
        "instancia": tipo_instancia,
        "region": "eu-west-1 (Irlanda)",
        "horas_mes": horas_mes,
        "coste_on_demand_eur_mes": costo_od,
        "coste_spot_eur_mes": costo_spot,
        "ahorro_mensual_eur": ahorro_mes,
        "ahorro_anual_eur": ahorro_anio,
        "descuento_aplicado": f"{int(descuento * 100)}%",
        "advertencia": "Las instancias Spot pueden interrumpirse con 2 minutos de aviso. Solo para cargas tolerantes a interrupciones: batch, CI/CD, procesamiento de imágenes.",
        "casos_uso_recomendados": ["Jobs de procesamiento asíncrono", "Pipelines de CI/CD", "Entornos de staging/QA", "Workers de colas SQS"],
        "fuentes": [
            {"descripcion": "AWS EC2 Spot Instances — descripción oficial y precios históricos", "url": "https://aws.amazon.com/ec2/spot/"},
            {"descripcion": "AWS Spot Instance Advisor — probabilidad de interrupción por tipo de instancia", "url": "https://aws.amazon.com/ec2/spot/instance-advisor/"},
            {"descripcion": "AWS Spot Pricing History — histórico de precios eu-west-1", "url": "https://aws.amazon.com/ec2/spot/pricing/"},
        ]
    }, ensure_ascii=False, indent=2)


@tool
def recomendar_plan_ahorro(descripcion_uso: str) -> str:
    """Recomienda la estrategia de optimización de costes AWS más adecuada según el patrón de uso.
    descripcion_uso: descripción libre del patrón (ej: '24/7 producción estable', 'tráfico variable con picos')."""
    uso = descripcion_uso.lower()

    if any(k in uso for k in ["24/7", "continuo", "siempre activo", "producción estable", "constante"]):
        resultado = {
            "recomendacion": "Savings Plans (Compute) 1 año — Sin pago anticipado",
            "ahorro_vs_od": "40-66%",
            "compromiso": "1 año, pago mensual sin coste inicial",
            "razon": "Carga base constante: el break-even con Savings Plans se alcanza a los 7-8 meses. Savings Plans de tipo Compute son flexibles entre familias, tamaños y regiones.",
            "alternativa": "Reserved Instances 3 años All-Upfront si hay certeza del tipo de instancia (hasta 72% de ahorro)",
            "pasos": [
                "1. Analizar 2 semanas de uso histórico con AWS Cost Explorer",
                "2. Identificar el baseline de cómputo (percentil 10 del uso)",
                "3. Cubrir ese baseline con Savings Plans Compute",
                "4. Cubrir picos con On-Demand",
            ],
        }
    elif any(k in uso for k in ["variable", "pico", "fluctúa", "estacional", "black friday", "evento"]):
        resultado = {
            "recomendacion": "Savings Plans (baseline) + Spot Instances (picos) + On-Demand (desbordamiento)",
            "ahorro_vs_od": "30-40% en base + hasta 72% en picos con Spot",
            "compromiso": "Savings Plans 1 año flexible, sin compromiso para Spot/OD",
            "razon": "El tráfico variable requiere flexibilidad. Savings Plans cubren el piso de consumo; Spot cubre los picos predecibles a coste mínimo.",
            "pasos": [
                "1. Calcular el 20% del pico de carga como baseline para Savings Plans",
                "2. Configurar Spot en Auto Scaling Groups con mínimo On-Demand del 20%",
                "3. Usar estrategia Capacity-Optimized para Spot (menor tasa de interrupción)",
                "4. Programar pre-calentamiento antes de eventos conocidos (Scheduled Scaling)",
            ],
        }
    else:
        resultado = {
            "recomendacion": "On-Demand + Right-Sizing mensual",
            "ahorro_vs_od": "15-25% solo con right-sizing sin compromisos adicionales",
            "compromiso": "Sin compromiso",
            "razon": "Uso impredecible: no adquirir compromisos sin datos. Optimizar primero con right-sizing y revisar en 3 meses.",
            "pasos": [
                "1. Activar AWS Compute Optimizer (gratuito)",
                "2. Aplicar recomendaciones en instancias con <40% CPU media",
                "3. Auditar y eliminar recursos huérfanos (snapshots, EIPs libres, LBs vacíos)",
                "4. Reevaluar compromisos en 90 días con datos reales de uso",
            ],
        }

    resultado["fuentes"] = [
        {"descripcion": "AWS Savings Plans — documentación oficial y calculadora de ahorro", "url": "https://aws.amazon.com/savingsplans/"},
        {"descripcion": "AWS Cost Optimization Hub — recomendaciones consolidadas de ahorro", "url": "https://aws.amazon.com/aws-cost-management/aws-cost-optimization/"},
        {"descripcion": "AWS Compute Optimizer — recomendaciones de right-sizing basadas en ML", "url": "https://aws.amazon.com/compute-optimizer/"},
        {"descripcion": "AWS Cost Explorer — análisis de uso y previsión de costes", "url": "https://aws.amazon.com/aws-cost-management/aws-cost-explorer/"},
    ]
    return json.dumps(resultado, ensure_ascii=False, indent=2)
