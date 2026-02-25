"""
mappings.py - Constantes, columnas y mapeos para encuesta administrativa.
"""

# ── Columna de filtro ────────────────────────────────────────
COL_AREA_ENC = "Área"
COL_AREA_INV = "AREA"

# ── Escalas ──────────────────────────────────────────────────
ESCALA_ACUERDO = {
    "Totalmente de acuerdo": 5,
    "Parcialmente de acuerdo": 4,
    "Neutral": 3,
    "Parcialmente en desacuerdo": 2,
    "Totalmente en desacuerdo": 1,
}

ESCALA_FRECUENCIA = {
    "Siempre": 5,
    "Casi siempre": 4,
    "A veces": 3,
    "Casi nunca": 2,
    "Nunca": 1,
}


def get_scale_map(scale_type: str) -> dict:
    return ESCALA_FRECUENCIA if scale_type == "frecuencia" else ESCALA_ACUERDO


# ── Preguntas Likert ─────────────────────────────────────────
LIKERT_QUESTIONS = [
    {
        "key": "Ambiente de trabajo",
        "col": "Me siento a gusto con el ambiente de trabajo que se genera en mi equipo.",
        "scale": "acuerdo",
    },
    {
        "key": "Actitud positiva",
        "col": "En mi entorno de trabajo mantenemos una actitud positiva centrándonos en las soluciones más que en los problemas.",
        "scale": "acuerdo",
    },
    {
        "key": "Innovación",
        "col": "Busco innovar y nuevas formas de hacer mejor mi trabajo.",
        "scale": "frecuencia",
    },
    {
        "key": "Diálogo con jefe",
        "col": "Dialogo con mi jefe directo sobre la calidad de mi trabajo y cómo podría mejorar.",
        "scale": "frecuencia",
    },
    {
        "key": "Reconocimiento",
        "col": "Siento que mi trabajo es reconocido por mi jefe directo.",
        "scale": "frecuencia",
    },
    {
        "key": "Soporte compañeros",
        "col": "Mis compañeros de área me dan soporte cuando lo necesito.",
        "scale": "frecuencia",
    },
    {
        "key": "Trabajo en equipo",
        "col": "Mi jefe directo fomenta el trabajo en equipo y colaboración entre todos.",
        "scale": "acuerdo",
    },
    {
        "key": "Bienestar personal",
        "col": "Mi jefe directo se preocupa por mi bienestar personal.",
        "scale": "acuerdo",
    },
    {
        "key": "Motivación",
        "col": "Me siento motivado a dar lo mejor de mí y hacer un buen trabajo",
        "scale": "acuerdo",
    },
    {
        "key": "Confianza en jefe",
        "col": "Mi jefe directo me otorga la confianza para acudir a él ante cualquier problema que afecte mi trabajo.",
        "scale": "acuerdo",
    },
    {
        "key": "Compromiso compañeros",
        "col": "Mis compañeros están comprometidos a hacer un trabajo de gran calidad.",
        "scale": "acuerdo",
    },
    {
        "key": "Soporte entre áreas",
        "col": "Cuando lo necesito, el resto de áreas de Limtek me brinda el soporte e información que requiero para hacer bien mi trabajo",
        "scale": "acuerdo",
    },
    {
        "key": "Orgullo Limtek",
        "col": "Me siento orgulloso de trabajar en Limtek",
        "scale": "acuerdo",
    },
    {
        "key": "Recomendaría servicios",
        "col": "Recomendaría los servicios que ofrece Limtek",
        "scale": "acuerdo",
    },
    {
        "key": "Impacto en clientes",
        "col": "Mi trabajo impacta directa o indirectamente en la satisfacción de nuestros clientes.",
        "scale": "acuerdo",
    },
]

# ── NPS (escala 0-10 tradicional) ────────────────────────────
COL_NPS = " ¿Qué tan probable es que recomiendes a Limtek como un lugar de trabajo a tus amigos o familiares?"

# ── Limtek buen lugar ────────────────────────────────────────
COL_BUEN_LUGAR = "Considero a Limtek como un buen lugar para trabajar"

# ── Preguntas abiertas ───────────────────────────────────────
COL_DESTACAR = "¿Qué destacas de Limtek al considerarlo un buen lugar para trabajar?"
COL_MEJORAR = "¿Qué tendría que mejorar Limtek para que lo consideres un buen lugar para trabajar?"

# ── Preguntas extra ──────────────────────────────────────────
COL_MEDIOS = "¿Por cual medio te gustaría recibir las novedades de Limtek? marca máximo 2 opciones"
COL_TALLERES_APORTE = "¿Consideras que los talleres realizados en nuestro Programa de Formación Transversal han aportado a tu crecimiento profesional?Por ejemplo: Creatividad en Movimiento, Canva, tu aliado en presentaciones, etc."
COL_TALLERES_MEJOR = "De los talleres del Programa de Formación en que has participado, ¿Cuál consideras que te ha aportado más?"
COL_TIPO_CAPACITACION = "¿Qué tipo de capacitación prefieres o consideras que es mejor para tu aprendizaje?"
COL_VIVE_BIEN = "¿Cuál ha sido la actividad del programa Vive Bien, que más te ha gustado? Marca máximo 3 opciones"
COL_ACTIVIDAD_FAV = "¿Cuál ha sido la actividad que más te ha gustado?"
