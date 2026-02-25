"""
filters.py - Filtros por Área para encuesta e inventario administrativo.
"""

import pandas as pd
from core.mappings import COL_AREA_ENC, COL_AREA_INV


def apply_encuesta_filters(df: pd.DataFrame, area: str | None) -> pd.DataFrame:
    out = df.copy()
    if area and area != "Todos":
        out = out[out[COL_AREA_ENC] == area]
    return out


def apply_inventario_filters(df: pd.DataFrame, area: str | None) -> pd.DataFrame:
    out = df.copy()
    if area and area != "Todos":
        out = out[out[COL_AREA_INV] == area]
    return out


def get_filter_options(df_enc: pd.DataFrame) -> list[str]:
    areas = sorted(df_enc[COL_AREA_ENC].dropna().unique())
    return ["Todos"] + areas
