"""
text_analysis.py - Análisis de texto con bloques conceptuales por keywords.
"""

import pandas as pd
import unicodedata

# ── Bloques para "¿Qué destacas?" ───────────────────────────
BLOQUES_DESTACAR: dict[str, list[str]] = {
    "Ambiente laboral": [
        "ambiente", "clima", "laboral", "compañerismo", "companerismo",
        "trato", "respeto", "equipo", "familia",
    ],
    "Oportunidad de crecimiento": [
        "crecimiento", "oportunidad", "oportunidades", "desarrollo",
        "aprendizaje", "carrera", "profesional",
    ],
    "Liderazgo y confianza": [
        "jefe", "jefes", "lider", "liderazgo", "confianza",
        "apoyo", "apoyan",
    ],
    "Flexibilidad y modalidad": [
        "flexibilidad", "hibrido", "horario", "facilidades",
        "modalidad", "remoto",
    ],
    "Compromiso y valores": [
        "compromiso", "valores", "calidad", "servicio",
        "orgullo", "orgulloso",
    ],
    "Estabilidad y formalidad": [
        "estabilidad", "formal", "formalidad", "pagos",
        "puntual", "planilla",
    ],
}

# ── Bloques para "¿Qué mejorar?" ────────────────────────────
BLOQUES_MEJORAR: dict[str, list[str]] = {
    "Remuneración y beneficios": [
        "sueldo", "sueldos", "salarial", "salario", "aumento",
        "beneficios", "pagos", "alimentos", "compensacion",
    ],
    "Comunicación interna": [
        "comunicacion", "comunicación", "informacion",
        "escuchar", "dialogo",
    ],
    "Liderazgo y gestión": [
        "jefe", "lideres", "liderazgo", "gestion",
        "comprension", "comprensión",
    ],
    "Integración y trabajo en equipo": [
        "integracion", "integración", "areas", "áreas",
        "sinergia", "equipo", "colaboracion",
    ],
    "Capacitación y desarrollo": [
        "capacitacion", "capacitaciones", "desarrollo",
        "crecimiento", "oportunidad",
    ],
    "Procesos e innovación": [
        "procesos", "innovacion", "innovación", "mejorar",
        "mejora", "tecnologia", "optimizar",
    ],
}


def _strip_accents(text: str) -> str:
    nfkd = unicodedata.normalize("NFKD", text)
    return "".join(c for c in nfkd if not unicodedata.combining(c))


def _bloques_generic(
    series: pd.Series, bloques_dict: dict[str, list[str]]
) -> pd.DataFrame:
    total = len(series.dropna())
    counts = {b: 0 for b in bloques_dict}
    for text in series.dropna():
        normalized = _strip_accents(str(text).lower())
        for bloque, keywords in bloques_dict.items():
            if any(kw in normalized for kw in keywords):
                counts[bloque] += 1
    rows = [
        {"Bloque": b, "Menciones": c,
         "Porcentaje (%)": round((c / total) * 100, 1) if total > 0 else 0.0}
        for b, c in counts.items()
    ]
    return pd.DataFrame(rows).sort_values("Menciones", ascending=False).reset_index(drop=True)


def _classify_generic(
    series: pd.Series, bloques_dict: dict[str, list[str]]
) -> dict[str, list[str]]:
    classified = {b: [] for b in bloques_dict}
    for text in series.dropna():
        original = str(text).strip()
        if not original:
            continue
        normalized = _strip_accents(original.lower())
        for bloque, keywords in bloques_dict.items():
            if any(kw in normalized for kw in keywords):
                classified[bloque].append(original)
    return classified


def bloques_conceptuales(series: pd.Series) -> pd.DataFrame:
    return _bloques_generic(series, BLOQUES_DESTACAR)


def bloques_conceptuales_mejorar(series: pd.Series) -> pd.DataFrame:
    return _bloques_generic(series, BLOQUES_MEJORAR)


def classify_responses_by_block(series: pd.Series) -> dict[str, list[str]]:
    return _classify_generic(series, BLOQUES_DESTACAR)


def classify_responses_mejorar(series: pd.Series) -> dict[str, list[str]]:
    return _classify_generic(series, BLOQUES_MEJORAR)
