"""likert.py - Detalle por pregunta Likert. Barras verticales, KPI al costado."""
import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from core.metrics import distribucion_pregunta, promedio_por_pregunta

COLOR_MAP = {5: "#000064", 4: "#3355AA", 3: "#A0A0B0", 2: "#E8943A", 1: "#CC4444"}
ETIQUETAS_CORTAS = {
    5: "Totalmente<br>de acuerdo", 4: "Parcialmente<br>de acuerdo", 3: "Neutral",
    2: "Parcialmente<br>en desacuerdo", 1: "Totalmente<br>en desacuerdo",
}
AMARILLO = "#FFB239"
AZUL = "#000064"
BLANCO = "#FFFFFF"

def render_likert_detail(df_enc: pd.DataFrame) -> None:
    st.markdown('<p class="section-title">📊 Detalle por pregunta Likert</p>', unsafe_allow_html=True)
    df_prom = promedio_por_pregunta(df_enc)

    for _, row in df_prom.iterrows():
        key, col_orig, prom, n = row["Pregunta"], row["Columna original"], row["Promedio"], row["Respuestas"]
        # Top-2 Box per question
        from core.mappings import get_scale_map, LIKERT_QUESTIONS
        q_def = next((q for q in LIKERT_QUESTIONS if q["key"] == key), None)
        if q_def:
            scale_map = get_scale_map(q_def["scale"])
            vals = df_enc[q_def["col"]].map(scale_map).dropna()
            top2 = int((vals >= 4).sum())
            pct_satisf = round((top2 / len(vals)) * 100, 1) if len(vals) > 0 else 0.0
        else:
            pct_satisf = round((prom / 5) * 100, 1)

        st.markdown(f"""<div style="background:rgba(13,13,107,0.6); border:1px solid #1a1a7a;
            border-left:4px solid {AMARILLO}; border-radius:6px; padding:10px 16px; margin:24px 0 4px 0;">
            <span style="color:{BLANCO}; font-weight:600; font-size:1.05rem;">{key}</span>
        </div><p style="color:#c8c8e0; font-size:0.95rem; margin:2px 0 10px 0;">{col_orig}</p>""",
            unsafe_allow_html=True)

        dist = distribucion_pregunta(df_enc, key)
        if dist.empty:
            st.info("Sin datos."); continue

        col_chart, col_kpi = st.columns([3, 1])
        with col_chart:
            orden = [5, 4, 3, 2, 1]
            dist_map = dict(zip(dist["Valor"].astype(int), zip(dist["Frecuencia"], dist["Porcentaje"])))
            freqs, colors, labels, texts = [], [], [], []
            for v in orden:
                if v in dist_map and dist_map[v][0] > 0:
                    f, p = dist_map[v]
                    freqs.append(int(f)); colors.append(COLOR_MAP[v])
                    labels.append(ETIQUETAS_CORTAS[v])
                    texts.append(f"<b>{int(f)}</b> ({round(p,1)}%)")
            max_freq = max(freqs) if freqs else 1

            fig = go.Figure(go.Bar(
                x=labels, y=freqs, text=texts, textposition="outside",
                textfont=dict(color="#333", size=13), marker_color=colors,
                marker_line=dict(width=1, color="#FFF"), cliponaxis=False,
            ))
            fig.update_layout(
                height=340, margin=dict(t=50, b=10, l=10, r=10),
                plot_bgcolor="#FFF", paper_bgcolor="#FFF",
                xaxis=dict(tickfont=dict(color="#333", size=10), showgrid=False, zeroline=False, fixedrange=True),
                yaxis=dict(showticklabels=False, showgrid=False, zeroline=False, fixedrange=True,
                           range=[0, max_freq * 1.32]),
                bargap=0.25, uniformtext=dict(minsize=11, mode="show"),
            )
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False}, key=f"likert_{key}")

        with col_kpi:
            st.markdown(f"""<div style="background:#FFF; box-shadow:0 1px 4px rgba(0,0,0,0.12);
                border:1px solid #E0E0E0; border-radius:10px; padding:20px 16px; text-align:center; margin-top:10px;">
                <p style="color:#555; font-size:0.78rem; margin:0 0 4px; text-transform:uppercase;">Promedio</p>
                <p style="color:#002B7F; font-size:2.6rem; font-weight:700; margin:0; line-height:1.1;">{prom:.2f}</p>
                <p style="color:#666; font-size:0.85rem; margin:2px 0 12px;">de 5.00</p>
                <hr style="border:none; border-top:1px solid #ECECEC; margin:8px 0;">
                <p style="color:#555; font-size:0.75rem; margin:0 0 2px; text-transform:uppercase;">Satisfacción (Top-2)</p>
                <p style="color:{AMARILLO}; font-size:1.6rem; font-weight:700; margin:0;">{pct_satisf}%</p>
                <hr style="border:none; border-top:1px solid #ECECEC; margin:8px 0;">
                <p style="color:#555; font-size:0.75rem; margin:0 0 2px; text-transform:uppercase;">Respuestas</p>
                <p style="color:#333; font-size:1.3rem; font-weight:600; margin:0;">{n:,}</p>
            </div>""", unsafe_allow_html=True)
