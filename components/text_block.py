"""text_block.py - Bloques conceptuales para preguntas abiertas."""
import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from core.text_analysis import (bloques_conceptuales, bloques_conceptuales_mejorar,
                                 classify_responses_by_block, classify_responses_mejorar)

AZUL_LIGHT = "#1a1a8a"
AMARILLO = "#FFB239"
BLANCO = "#FFFFFF"

def _render_bloques_section(series, title, emoji, bloques_fn, classify_fn):
    st.markdown(f'<p class="section-title">{emoji} {title}</p>', unsafe_allow_html=True)
    df_b = bloques_fn(series)
    total = int(series.dropna().shape[0])
    if df_b.empty or total == 0:
        st.info("Sin datos."); return

    c1, c2 = st.columns(2)
    with c1: st.metric("🏆 Bloque más mencionado", df_b.iloc[0]["Bloque"])
    with c2: st.metric("💬 Total respuestas", f"{total:,}")

    df_plot = df_b.sort_values("Menciones", ascending=True)
    max_m = df_plot["Menciones"].max()
    colors = [AMARILLO if m == max_m else AZUL_LIGHT for m in df_plot["Menciones"]]

    fig = go.Figure(go.Bar(
        x=df_plot["Menciones"], y=df_plot["Bloque"], orientation="h",
        text=[f"  {int(m)}  ({p}%)" for m, p in zip(df_plot["Menciones"], df_plot["Porcentaje (%)"])],
        textposition="outside", textfont=dict(color="#333", size=13),
        marker_color=colors, marker_line=dict(width=1, color="#FFF"),
        cliponaxis=False,
    ))
    max_m_val = df_plot["Menciones"].max()
    fig.update_layout(
        height=330, margin=dict(t=10, b=20, l=10, r=110),
        plot_bgcolor="#FFF", paper_bgcolor="#FFF",
        xaxis=dict(showticklabels=False, showgrid=False, zeroline=False,
                   range=[0, max_m_val * 1.35]),
        yaxis=dict(tickfont=dict(color="#333", size=12), gridcolor="rgba(0,0,0,0)"),
        bargap=0.3,
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    classified = classify_fn(series)
    with st.expander("📂 TEXTO ORIGINAL CLASIFICADO POR BLOQUE", expanded=False):
        ordered = df_b["Bloque"].tolist()
        tabs = st.tabs([f"{b} ({len(classified.get(b,[]))})" for b in ordered])
        for tab, b in zip(tabs, ordered):
            with tab:
                resps = classified.get(b, [])
                st.markdown(f"**{b}** — {len(resps)} respuestas")
                if not resps: st.caption("Sin respuestas."); continue
                html = "".join(f"<p>• {r}</p>" for r in resps)
                st.markdown(f'<div class="text-scroll-container">{html}</div>', unsafe_allow_html=True)

def render_text_blocks(df_enc, col_destacar, col_mejorar):
    _render_bloques_section(df_enc[col_destacar], "¿Qué destacas de Limtek?", "🌟",
                            bloques_conceptuales, classify_responses_by_block)
    st.divider()
    _render_bloques_section(df_enc[col_mejorar], "¿Qué tendría que mejorar Limtek?", "🔧",
                            bloques_conceptuales_mejorar, classify_responses_mejorar)
