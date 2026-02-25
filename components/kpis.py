"""kpis.py - KPIs principales + NPS detalle."""
import streamlit as st
import pandas as pd
from core.metrics import promedio_general, indice_satisfaccion, calcular_nps

AMARILLO = "#FFB239"

def render_kpis(df_enc: pd.DataFrame, df_inv: pd.DataFrame) -> None:
    total_enc = len(df_enc)
    total_inv = len(df_inv)
    part = round((total_enc / total_inv) * 100, 1) if total_inv > 0 else 0.0
    prom = promedio_general(df_enc)
    satisf = indice_satisfaccion(df_enc)
    nps_data = calcular_nps(df_enc)

    c1, c2, c3, c4, c5, c6 = st.columns(6)
    with c1: st.metric("📋 Respuestas", f"{total_enc:,}")
    with c2: st.metric("👥 Inventario", f"{total_inv:,}")
    with c3: st.metric("📊 Participación", f"{part}%")
    with c4: st.metric("⭐ Prom. Likert", f"{prom}/5")
    with c5: st.metric("😊 Satisfacción", f"{satisf}%")
    with c6: st.metric("🎯 NPS", f"{nps_data['nps']:+.1f}")

def render_nps_detail(df_enc: pd.DataFrame) -> None:
    st.markdown('<p class="section-title">🎯 Detalle NPS (Escala 0-10)</p>', unsafe_allow_html=True)
    nps = calcular_nps(df_enc)
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric("🟢 Promotores (9-10)", f"{nps['promotores']} ({nps['pct_pro']}%)")
    with c2: st.metric("🟡 Pasivos (7-8)", f"{nps['pasivos']} ({nps['pct_pas']}%)")
    with c3: st.metric("🔴 Detractores (0-6)", f"{nps['detractores']} ({nps['pct_det']}%)")
    with c4:
        color = "#22c55e" if nps["nps"] > 50 else AMARILLO if nps["nps"] > 0 else "#ef4444"
        st.markdown(
            f"""<div style="background:#FFFFFF; border-radius:10px; padding:16px; text-align:center; border:1px solid #E0E0E0;">
                <p style="color:#555; font-size:0.75rem; margin:0; text-transform:uppercase;">NPS Score</p>
                <p style="color:{color}; font-size:2.2rem; font-weight:700; margin:0;">{nps['nps']:+.1f}</p>
            </div>""", unsafe_allow_html=True)
