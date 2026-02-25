"""
Dashboard Clima Laboral — Personal Administrativo
Limtek Servicios Integrales · 2025
"""
import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(page_title="Clima Laboral · Administrativos · Limtek", layout="wide", page_icon="📊")

# ── Imports ──────────────────────────────────────────────────
from core.filters import apply_encuesta_filters, apply_inventario_filters, get_filter_options
from core.mappings import COL_DESTACAR, COL_MEJORAR
from components.kpis import render_kpis, render_nps_detail
from components.ranking import render_ranking
from components.likert import render_likert_detail
from components.extras import render_extras
from components.text_block import render_text_blocks
from components.cumplimiento import render_cumplimiento

# ── CSS Corporativo ──────────────────────────────────────────
st.markdown("""
<style>
:root {
    --azul: #000064;
    --amarillo: #FFB239;
    --gris-border: #1a1a7a;
}
.stApp, [data-testid="stAppViewContainer"] { background-color: var(--azul) !important; }
header[data-testid="stHeader"] { background-color: var(--azul) !important; }

section[data-testid="stSidebar"] {
    background-color: #000050 !important;
    border-right: 1px solid var(--gris-border) !important;
}
section[data-testid="stSidebar"] * { color: #c8c8e0 !important; }
section[data-testid="stSidebar"] .stSelectbox label { color: var(--amarillo) !important; font-weight: 600; }

[data-testid="stMetric"] {
    background: #0d0d6b; border: 1px solid var(--gris-border); border-radius: 8px; padding: 12px 16px;
}
[data-testid="stMetricLabel"] p { color: #c8c8e0 !important; font-size: 0.8rem; }
[data-testid="stMetricValue"] { color: white !important; font-weight: 700; }

.section-title {
    color: white !important; font-size: 1.25rem; font-weight: 700;
    border-bottom: 3px solid var(--amarillo); padding-bottom: 6px; margin: 24px 0 12px;
}

.text-scroll-container {
    max-height: 300px; overflow-y: auto; padding: 10px;
    background: rgba(13,13,107,0.3); border-radius: 6px;
    color: #c8c8e0; font-size: 0.88rem; line-height: 1.6;
}

div.stTabs [data-baseweb="tab-list"] button {
    color: #c8c8e0 !important; font-size: 0.85rem;
}
div.stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
    color: var(--amarillo) !important; border-bottom-color: var(--amarillo) !important;
}

.stDivider { border-color: var(--gris-border) !important; }
</style>
""", unsafe_allow_html=True)

# ── Data load ────────────────────────────────────────────────
DATA_DIR = Path(__file__).resolve().parent / "data"

@st.cache_data
def load_encuesta():
    return pd.read_excel(DATA_DIR / "encuesta.xlsx")

@st.cache_data
def load_inventario():
    df = pd.read_excel(DATA_DIR / "inventario.xlsx")
    for col in df.columns:
        if df[col].dtype == object:
            df[col] = df[col].astype(str).str.strip()
    return df

df_enc_raw = load_encuesta()
df_inv_raw = load_inventario()

# ── Header ───────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center; padding:20px 0 10px;">
    <h1 style="color:white; margin:0;">📊 Dashboard Clima Laboral</h1>
    <p style="color:#c8c8e0; font-size:1.1rem; margin:5px 0 0;">
        Limtek Servicios Integrales · Personal Administrativo · 2025
    </p>
</div>
""", unsafe_allow_html=True)

# ── Sidebar ──────────────────────────────────────────────────
st.sidebar.markdown("""
<div style="text-align:center; margin-bottom:20px;">
    <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRGa7xFnFuRMmopHsst6MCpjR2VhLYMRL_-IQ&s"
         alt="Limtek" height="40" onerror="this.style.display='none'">
</div>
""", unsafe_allow_html=True)
st.sidebar.header("🔍 Filtros")
areas = get_filter_options(df_enc_raw)
sel_area = st.sidebar.selectbox("Área", areas, index=0, key="f_area")

# ── Apply filters ────────────────────────────────────────────
df_enc = apply_encuesta_filters(df_enc_raw, sel_area)
df_inv = apply_inventario_filters(df_inv_raw, sel_area)

# ── KPIs ─────────────────────────────────────────────────────
render_kpis(df_enc, df_inv)
st.divider()

# ── Cumplimiento por área ────────────────────────────────────
render_cumplimiento(df_enc, df_inv, df_enc_raw, df_inv_raw, sel_area)
st.divider()

# ── NPS Detail ───────────────────────────────────────────────
render_nps_detail(df_enc)
st.divider()

# ── Ranking ──────────────────────────────────────────────────
render_ranking(df_enc)
st.divider()

# ── Detalle Likert ───────────────────────────────────────────
render_likert_detail(df_enc)
st.divider()

# ── Secciones extra ──────────────────────────────────────────
render_extras(df_enc)
st.divider()

# ── Preguntas abiertas ───────────────────────────────────────
render_text_blocks(df_enc, COL_DESTACAR, COL_MEJORAR)
