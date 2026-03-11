# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Dashboard de Clima Laboral para el personal administrativo de **Limtek Servicios Integrales**, construido con Streamlit. Visualiza resultados de encuestas (escala Likert + NPS) y los cruza con un inventario de empleados por área.

## Commands

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar el dashboard
streamlit run app.py

# Ejecutar apuntando a un puerto específico
streamlit run app.py --server.port 8502
```

Los datos viven en `data/encuesta.xlsx` y `data/inventario.xlsx`. Ambos archivos deben existir para que la app inicie.

## Architecture

### Data flow

```
data/encuesta.xlsx   →  load_encuesta()  →  df_enc_raw
data/inventario.xlsx →  load_inventario() →  df_inv_raw
         ↓
   Sidebar filter (Área)
         ↓
apply_encuesta_filters / apply_inventario_filters
         ↓
   df_enc / df_inv  →  render_* components
```

`app.py` es el único punto de entrada. Carga datos con `@st.cache_data`, aplica filtros y delega el renderizado a los componentes.

### Layers

| Capa | Ubicación | Responsabilidad |
|------|-----------|-----------------|
| Config & constantes | `core/mappings.py` | Nombres de columnas, escalas Likert, lista de preguntas (`LIKERT_QUESTIONS`), columnas NPS y preguntas abiertas |
| Filtros | `core/filters.py` | Filtrar DataFrames por área |
| Métricas | `core/metrics.py` | Promedios Likert, índice de satisfacción Top-2-Box, NPS (escala 0-10) |
| Análisis de texto | `core/text_analysis.py` | Clasificación de respuestas abiertas por bloques conceptuales (keyword matching) |
| Componentes UI | `components/` | Cada archivo renderiza una sección del dashboard |

### Components

- `kpis.py` — 6 métricas globales + detalle NPS (promotores/pasivos/detractores)
- `cumplimiento.py` — Tabla/gráfico de participación por área; con filtro activo muestra solo esa área
- `ranking.py` — Ranking de preguntas Likert de mejor a peor
- `likert.py` — Distribución detallada por pregunta Likert
- `extras.py` — Preguntas de opción múltiple (medios, talleres, capacitación, Vive Bien)
- `text_block.py` — Preguntas abiertas: bloques conceptuales + respuestas individuales agrupadas

### Key conventions

- **Columnas del Excel**: los nombres exactos de columnas están centralizados en `core/mappings.py`. Si cambian las columnas del Excel, solo se actualiza allí.
- **Escalas**: cada pregunta en `LIKERT_QUESTIONS` declara su escala (`"acuerdo"` o `"frecuencia"`); `get_scale_map()` devuelve el diccionario correspondiente.
- **Colores corporativos**: azul `#000064`, amarillo `#FFB239`. Definidos como CSS variables en `app.py` y como constantes locales en los componentes que generan gráficos Plotly.
- **Gráficos**: todos usan Plotly (`plotly.graph_objects`), con `plot_bgcolor`/`paper_bgcolor` blancos para contraste con el fondo oscuro del dashboard.
- **Texto sin acento**: `core/text_analysis._strip_accents()` normaliza texto antes de buscar keywords; los keywords en `BLOQUES_DESTACAR`/`BLOQUES_MEJORAR` deben escribirse sin tildes.
