"""extras.py - Secciones extra: Medios, Talleres, Capacitación, Vive Bien, Actividad favorita."""
import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from collections import Counter
from core.mappings import (COL_MEDIOS, COL_TALLERES_APORTE, COL_TALLERES_MEJOR,
                           COL_TIPO_CAPACITACION, COL_VIVE_BIEN, COL_ACTIVIDAD_FAV)

AZUL_LIGHT = "#1a1a8a"
AMARILLO = "#FFB239"
BLANCO = "#FFFFFF"


def _bar_chart(labels, values, title_key, height=280):
    max_v = max(values) if values else 1
    total = sum(values)
    colors = [AMARILLO if v == max_v else AZUL_LIGHT for v in values]
    texts = [f"<b>{v}</b> ({round(v/total*100,1)}%)" for v in values]
    fig = go.Figure(go.Bar(
        x=values, y=labels, orientation="h", text=texts,
        textposition="outside", textfont=dict(color="#333", size=12),
        marker_color=colors, marker_line=dict(width=1, color="#FFF"),
        cliponaxis=False,
    ))
    fig.update_layout(
        height=height, margin=dict(t=10, b=20, l=10, r=120),
        plot_bgcolor="#FFF", paper_bgcolor="#FFF",
        xaxis=dict(showticklabels=False, showgrid=False, zeroline=False,
                   range=[0, max_v * 1.35]),
        yaxis=dict(tickfont=dict(color="#333", size=11), gridcolor="rgba(0,0,0,0)"),
        bargap=0.3,
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False}, key=f"extra_{title_key}")


def _section_title(emoji, text):
    st.markdown(f"""<div style="background:rgba(13,13,107,0.6); border:1px solid #1a1a7a;
        border-left:4px solid {AMARILLO}; border-radius:6px; padding:8px 14px; margin:8px 0;">
        <span style="color:{BLANCO}; font-weight:600; font-size:0.95rem;">{emoji} {text}</span>
    </div>""", unsafe_allow_html=True)


def render_extras(df_enc: pd.DataFrame) -> None:
    st.markdown('<p class="section-title">📋 Secciones Adicionales</p>', unsafe_allow_html=True)

    # ── 1. Medios de comunicación (multi-select con \n) ──────
    _section_title("📨", "¿Por cuál medio te gustaría recibir novedades de Limtek?")
    mc = Counter()
    for val in df_enc[COL_MEDIOS].dropna():
        for item in str(val).split('\n'):
            mc[item.strip()] += 1
    sorted_mc = mc.most_common()
    _bar_chart([k for k,_ in reversed(sorted_mc)], [v for _,v in reversed(sorted_mc)], "medios", 260)

    st.divider()

    # ── 2. Talleres (2 gráficos lado a lado) ─────────────────
    _section_title("🎓", "Programa de Formación Transversal")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**¿Aportaron a tu crecimiento profesional?**")
        ta = df_enc[COL_TALLERES_APORTE].value_counts()
        _bar_chart(list(reversed(ta.index.tolist())), list(reversed(ta.values.tolist())), "talleres_aporte", 220)
    with col2:
        st.markdown("**¿Cuál taller te aportó más?**")
        tm = df_enc[COL_TALLERES_MEJOR].value_counts()
        short = [l[:35] + "..." if len(l) > 35 else l for l in tm.index]
        _bar_chart(list(reversed(short)), list(reversed(tm.values.tolist())), "talleres_mejor", 280)

    st.divider()

    # ── 3. Tipo de capacitación preferida ────────────────────
    _section_title("📚", "Tipo de capacitación preferida")
    tc = df_enc[COL_TIPO_CAPACITACION].value_counts()
    short_tc = [l.split("(")[0].strip() if "(" in l else l for l in tc.index]
    _bar_chart(list(reversed(short_tc)), list(reversed(tc.values.tolist())), "tipo_cap", 240)

    st.divider()

    # ── 4. Vive Bien (multi-select con ;) ────────────────────
    _section_title("🎉", "Actividades del programa Vive Bien")
    vb = Counter()
    for val in df_enc[COL_VIVE_BIEN].dropna():
        for item in str(val).split(';'):
            vb[item.strip()] += 1
    sorted_vb = vb.most_common()
    _bar_chart([k for k,_ in reversed(sorted_vb)], [v for _,v in reversed(sorted_vb)], "vive_bien", 260)

    st.divider()

    # ── 5. Actividad favorita (barras horizontales) ─────────
    _section_title("⭐", "Actividad que más te ha gustado")
    af = df_enc[COL_ACTIVIDAD_FAV].fillna("No participó").replace("", "No participó").value_counts()
    af = af.rename(index={"No participé": "No participó"})
    if af.empty:
        st.info("Sin datos."); return
    _bar_chart(list(reversed(af.index.tolist())), list(reversed(af.values.tolist())), "act_fav", max(260, len(af) * 38))
