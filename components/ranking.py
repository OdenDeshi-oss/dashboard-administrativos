"""ranking.py - Ranking de preguntas Likert."""
import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import textwrap
from core.metrics import promedio_por_pregunta, ranking_mejor_peor

AZUL_DARK  = "#000064"
AZUL_LIGHT = "#1a1a8a"
AMARILLO   = "#FFB239"

def _wrap(text: str, width: int = 55) -> str:
    return "<br>".join(textwrap.wrap(text, width))

def render_ranking(df_enc: pd.DataFrame) -> None:
    st.markdown('<p class="section-title">🏆 Ranking de satisfacción por pregunta</p>', unsafe_allow_html=True)
    st.markdown(
        '<p style="color:#c8c8e0; font-size:0.9rem; margin:-8px 0 12px;">'
        'Promedio de respuestas (escala 1 a 5) para cada pregunta de la encuesta de clima laboral. '
        'Permite identificar qué aspectos del trabajo son mejor y peor valorados por el equipo.</p>',
        unsafe_allow_html=True,
    )
    mejor, peor = ranking_mejor_peor(df_enc)
    c1, c2 = st.columns(2)
    with c1: st.success(f"🥇 **Mejor:** {mejor['Pregunta']} — **{mejor['Promedio']:.2f}**")
    with c2: st.error(f"🥉 **Peor:** {peor['Pregunta']} — **{peor['Promedio']:.2f}**")

    df_prom = promedio_por_pregunta(df_enc).sort_values("Promedio", ascending=True)
    max_prom = df_prom["Promedio"].max()
    colors = [AMARILLO if p == max_prom else AZUL_LIGHT for p in df_prom["Promedio"]]

    etiquetas_y = [_wrap(q) for q in df_prom["Columna original"]]

    fig = go.Figure(go.Bar(
        x=df_prom["Promedio"], y=etiquetas_y, orientation="h",
        text=[f"  {p:.2f}" for p in df_prom["Promedio"]],
        textposition="outside", textfont=dict(color="#333333", size=13),
        marker_color=colors, marker_line=dict(width=1, color=AZUL_DARK),
        cliponaxis=False,
        hovertemplate="<b>%{x:.2f} / 5</b><extra></extra>",
    ))
    fig.update_layout(
        height=max(520, len(df_prom) * 42 + 60),
        margin=dict(t=10, b=40, l=10, r=90),
        plot_bgcolor="#FFFFFF", paper_bgcolor="#FFFFFF",
        xaxis=dict(range=[0, 5.8], tickfont=dict(color="#888", size=11),
                   gridcolor="#ECECEC", zeroline=False,
                   title="Promedio (1-5)", title_font=dict(color="#888", size=12)),
        yaxis=dict(tickfont=dict(color="#333", size=12), gridcolor="rgba(0,0,0,0)"),
        bargap=0.3,
        hoverlabel=dict(bgcolor="white", font_size=13, font_color="#111"),
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    with st.expander("📋 Tabla de promedios", expanded=False):
        st.dataframe(
            df_prom[["Pregunta", "Columna original", "Promedio", "Respuestas"]]
            .rename(columns={"Columna original": "Pregunta completa"})
            .sort_values("Promedio", ascending=False),
            hide_index=True, use_container_width=True)
