"""cumplimiento.py - Cumplimiento y Satisfacción por área."""
import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from core.mappings import COL_AREA_ENC, COL_AREA_INV
from core.metrics import satisfaccion_por_area


AZUL_LIGHT = "#1a1a8a"
AMARILLO = "#FFB239"

def render_cumplimiento(df_enc, df_inv, df_enc_raw, df_inv_raw, sel_area):
    has_area = sel_area and sel_area != "Todos"

    # Siempre mostrar tabla de cumplimiento por área
    st.markdown('<p class="section-title">📌 Cumplimiento por Área</p>', unsafe_allow_html=True)

    if has_area:
        total_inv = len(df_inv)
        total_resp = len(df_enc)
        pct = round((total_resp / total_inv) * 100, 1) if total_inv > 0 else 0.0
        st.markdown(f"Filtro activo: **{sel_area}**")
        c1, c2, c3 = st.columns(3)
        with c1: st.metric("👥 Inventario", f"{total_inv:,}")
        with c2: st.metric("📋 Respondieron", f"{total_resp:,}")
        with c3: st.metric("📊 Cumplimiento", f"{pct}%")
        return

    # Sin filtro: tabla completa por área
    inv_c = df_inv_raw.groupby(COL_AREA_INV).size().reset_index(name="Inventario")
    inv_c.rename(columns={COL_AREA_INV: "Área"}, inplace=True)
    enc_c = df_enc_raw.groupby(COL_AREA_ENC).size().reset_index(name="Respuestas")
    enc_c.rename(columns={COL_AREA_ENC: "Área"}, inplace=True)
    m = inv_c.merge(enc_c, on="Área", how="left").fillna(0)
    m["Respuestas"] = m["Respuestas"].astype(int)
    m["% Cumplimiento"] = (m["Respuestas"] / m["Inventario"] * 100).round(1)
    m = m.sort_values("% Cumplimiento", ascending=True)

    max_pct = m["% Cumplimiento"].max()
    colors = [AMARILLO if p == max_pct else AZUL_LIGHT for p in m["% Cumplimiento"]]

    fig = go.Figure(go.Bar(
        x=m["% Cumplimiento"], y=m["Área"], orientation="h",
        text=[f"{p}% ({int(r)}/{int(i)})" for p, r, i in zip(m["% Cumplimiento"], m["Respuestas"], m["Inventario"])],
        textposition="outside", textfont=dict(color="#333", size=12),
        marker_color=colors, marker_line=dict(width=1, color="#FFF"),
        cliponaxis=False,
    ))
    fig.update_layout(
        height=max(300, len(m)*32+60), margin=dict(t=10, b=20, l=10, r=120),
        plot_bgcolor="#FFF", paper_bgcolor="#FFF",
        xaxis=dict(showticklabels=False, showgrid=False, zeroline=False,
                   range=[0, m["% Cumplimiento"].max() * 1.3]),
        yaxis=dict(tickfont=dict(color="#333", size=11), gridcolor="rgba(0,0,0,0)"),
        bargap=0.3,
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


def render_satisfaccion_por_area(df_enc_raw: pd.DataFrame, df_inv_raw: pd.DataFrame, sel_area: str) -> None:
    st.markdown('<p class="section-title">😊 Satisfacción por Área</p>', unsafe_allow_html=True)

    df_sat = satisfaccion_por_area(df_enc_raw, df_inv_raw)

    has_area = sel_area and sel_area != "Todos"
    if has_area:
        row = df_sat[df_sat["Área"] == sel_area]
        if not row.empty:
            r = row.iloc[0]
            c1, c2, c3 = st.columns(3)
            with c1: st.metric("📊 Resp. Likert", f"{int(r['Respondieron']):,}")
            with c2: st.metric("😊 Top-2-Box (≥4)", f"{int(r['Satisfechos']):,}")
            with c3: st.metric("📊 % Satisfacción", f"{r['% Satisfacción']}%")
        return

    max_pct = df_sat["% Satisfacción"].max()
    colors = [AMARILLO if p == max_pct else AZUL_LIGHT for p in df_sat["% Satisfacción"]]

    fig = go.Figure(go.Bar(
        x=df_sat["% Satisfacción"], y=df_sat["Área"], orientation="h",
        text=[f"{pct}% ({sat}/{inv})" for pct, sat, inv in zip(
            df_sat["% Satisfacción"], df_sat["Satisfechos"], df_sat["Inventario"])],
        textposition="outside", textfont=dict(color="#333", size=12),
        marker_color=colors, marker_line=dict(width=1, color="#FFF"),
        cliponaxis=False,
    ))
    fig.update_layout(
        height=max(300, len(df_sat) * 32 + 60),
        margin=dict(t=10, b=20, l=10, r=160),
        plot_bgcolor="#FFF", paper_bgcolor="#FFF",
        xaxis=dict(showticklabels=False, showgrid=False, zeroline=False,
                   range=[0, max_pct * 1.35]),
        yaxis=dict(tickfont=dict(color="#333", size=11), gridcolor="rgba(0,0,0,0)"),
        bargap=0.3,
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
