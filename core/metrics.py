"""
metrics.py - KPIs, NPS tradicional (0-10), promedios Likert.
"""

import pandas as pd
import numpy as np
from core.mappings import LIKERT_QUESTIONS, get_scale_map, COL_NPS


def promedio_por_pregunta(df_enc: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for q in LIKERT_QUESTIONS:
        scale_map = get_scale_map(q["scale"])
        vals = df_enc[q["col"]].map(scale_map).dropna()
        rows.append({
            "Pregunta": q["key"],
            "Columna original": q["col"],
            "Promedio": round(vals.mean(), 2) if len(vals) > 0 else 0.0,
            "Respuestas": len(vals),
        })
    return pd.DataFrame(rows).sort_values("Promedio", ascending=False).reset_index(drop=True)


def distribucion_pregunta(df_enc: pd.DataFrame, key: str) -> pd.DataFrame:
    q = next((q for q in LIKERT_QUESTIONS if q["key"] == key), None)
    if q is None:
        return pd.DataFrame()
    scale_map = get_scale_map(q["scale"])
    vals = df_enc[q["col"]].map(scale_map).dropna()
    total = len(vals)
    if total == 0:
        return pd.DataFrame()
    dist = vals.value_counts().reset_index()
    dist.columns = ["Valor", "Frecuencia"]
    dist["Porcentaje"] = round((dist["Frecuencia"] / total) * 100, 1)
    return dist.sort_values("Valor", ascending=False).reset_index(drop=True)


def ranking_mejor_peor(df_enc: pd.DataFrame) -> tuple[dict, dict]:
    df_prom = promedio_por_pregunta(df_enc)
    mejor = df_prom.iloc[0].to_dict()
    peor = df_prom.iloc[-1].to_dict()
    return mejor, peor


def promedio_general(df_enc: pd.DataFrame) -> float:
    all_vals = []
    for q in LIKERT_QUESTIONS:
        scale_map = get_scale_map(q["scale"])
        vals = df_enc[q["col"]].map(scale_map).dropna().tolist()
        all_vals.extend(vals)
    return round(np.mean(all_vals), 2) if all_vals else 0.0


def indice_satisfaccion(df_enc: pd.DataFrame) -> float:
    """Top-2 Box: % de respuestas que son 4 o 5."""
    all_vals = []
    for q in LIKERT_QUESTIONS:
        scale_map = get_scale_map(q["scale"])
        vals = df_enc[q["col"]].map(scale_map).dropna().tolist()
        all_vals.extend(vals)
    if not all_vals:
        return 0.0
    top2 = sum(1 for v in all_vals if int(v) >= 4)
    return round((top2 / len(all_vals)) * 100, 1)


def satisfaccion_por_area(df_enc_raw: pd.DataFrame, df_inv_raw: pd.DataFrame) -> pd.DataFrame:
    """Personas satisfechas (promedio Likert ≥4) vs inventario por área."""
    from core.mappings import COL_AREA_ENC, COL_AREA_INV
    # Calcular promedio Likert por persona
    scores = []
    for _, row in df_enc_raw.iterrows():
        vals = []
        for q in LIKERT_QUESTIONS:
            scale_map = get_scale_map(q["scale"])
            v = scale_map.get(row[q["col"]])
            if v is not None:
                vals.append(v)
        prom = np.mean(vals) if vals else None
        scores.append({"Área": row[COL_AREA_ENC], "prom": prom})
    df_scores = pd.DataFrame(scores).dropna(subset=["prom"])

    # Inventario por área
    inv_c = df_inv_raw.groupby(COL_AREA_INV).size().reset_index(name="Inventario")
    inv_c.rename(columns={COL_AREA_INV: "Área"}, inplace=True)

    rows = []
    for area, group in df_scores.groupby("Área"):
        satisfechos = int((group["prom"] >= 4).sum())
        n_respondieron = len(group)
        inventario = int(inv_c.loc[inv_c["Área"] == area, "Inventario"].values[0]) if area in inv_c["Área"].values else n_respondieron
        pct = round((satisfechos / inventario) * 100, 1) if inventario > 0 else 0.0
        rows.append({"Área": area, "Satisfechos": satisfechos,
                     "Respondieron": n_respondieron, "Inventario": inventario,
                     "% Satisfacción": pct})
    return pd.DataFrame(rows).sort_values("% Satisfacción", ascending=True).reset_index(drop=True)


def calcular_nps(df_enc: pd.DataFrame) -> dict:
    """NPS tradicional escala 0-10."""
    vals = df_enc[COL_NPS].dropna()
    total = len(vals)
    if total == 0:
        return {"promotores": 0, "pasivos": 0, "detractores": 0,
                "pct_pro": 0, "pct_pas": 0, "pct_det": 0, "nps": 0, "total": 0}
    promotores = int((vals >= 9).sum())
    pasivos = int(((vals >= 7) & (vals <= 8)).sum())
    detractores = int((vals <= 6).sum())
    nps = round((promotores - detractores) / total * 100, 1)
    return {
        "promotores": promotores,
        "pasivos": pasivos,
        "detractores": detractores,
        "pct_pro": round(promotores / total * 100, 1),
        "pct_pas": round(pasivos / total * 100, 1),
        "pct_det": round(detractores / total * 100, 1),
        "nps": nps,
        "total": total,
    }
