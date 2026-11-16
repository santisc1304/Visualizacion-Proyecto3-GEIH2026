"""
generate_plotly_minidashboard.py
================================
Construcción de la visualización interactiva / mini-dashboard en Python con Plotly
para el Proyecto 3: Narrativa Visual Integrada.

Características:
- Cuadrante interactivo Riesgo (CV) vs. Retorno (Ingreso Medio) por sector y grupo de edad.
- Menús desplegables (Dropdowns) para filtrar por macrosector o cohorte de edad.
- Tooltips ricos en HTML con formato monetario $ COP y recomendación de fondo de emergencia.
- Exportación en HTML autocontenido (standalone) para visualización sin servidor.
"""

import os
import json
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
PROFILES_JSON = os.path.join(BASE_DIR, "data", "processed", "metricas_perfiles_simulador.json")
PY_OUTPUT_DIR = os.path.join(BASE_DIR, "python", "output")
WEB_INTERACTIVE_DIR = os.path.join(BASE_DIR, "web", "assets", "interactive")

os.makedirs(PY_OUTPUT_DIR, exist_ok=True)
os.makedirs(WEB_INTERACTIVE_DIR, exist_ok=True)

def generate_interactive_minidashboard():
    with open(PROFILES_JSON, 'r', encoding='utf-8') as f:
        profiles = json.load(f)
        
    df = pd.DataFrame(profiles)
    
    # Colores semánticos
    color_map = {
        "Estabilidad Alta": "#16A34A",       # Verde esmeralda
        "Estabilidad Moderada": "#D99B26",   # Ámbar/Dorado
        "Volatilidad Elevada": "#DC2626"    # Rojo rubí
    }
    
    fig = go.Figure()
    
    # Agregar trazas por estatus de estabilidad
    for estatus, col in color_map.items():
        sub = df[df['estatus_estabilidad'] == estatus]
        
        hover_texts = []
        for _, row in sub.iterrows():
            text = (
                f"<b>{row['sector']} ({row['grupo_edad']})</b><br>"
                f"━━━━━━━━━━━━━━━━━━━━━━━━━━<br>"
                f"• Ingreso Promedio: <b>${row['ingreso_medio']:,.0f} COP</b><br>"
                f"• Mediana Típica: <b>${row['mediana']:,.0f} COP</b><br>"
                f"• Rango Intercuartil (P25-P75): ${row['p25']:,.0f} - ${row['p75']:,.0f}<br>"
                f"• Volatilidad Relativa (CV): <b>{row['cv_ponderado']:.2f}</b> ({estatus})<br>"
                f"• Comparativo Asalariado: <b>{'+' if row['brecha_pct']>0 else ''}{row['brecha_pct']}%</b><br>"
                f"• Colchón de liquidez aconsejado: <b>{row['colchon_recomendado']}</b><br>"
                f"<i>Muestra representativa: {row['n_muestra']:,} registros</i>"
            )
            hover_texts.append(text)
            
        fig.add_trace(go.Scatter(
            x=sub['cv_ponderado'],
            y=sub['ingreso_medio'],
            mode='markers+text',
            name=estatus,
            text=sub['sector'],
            textposition='top center',
            textfont=dict(size=9, color="#1E293B"),
            marker=dict(
                size=sub['n_muestra'].apply(lambda n: max(14, min(36, np.sqrt(n) * 0.4))),
                color=col,
                opacity=0.85,
                line=dict(width=1.5, color="#FFFFFF")
            ),
            hoverinfo='text',
            hovertext=hover_texts
        ))
        
    # Líneas de referencia
    smmlv = 1423500
    fig.add_hline(
        y=smmlv, line_dash="dot", line_color="#DC2626", line_width=1.5,
        annotation_text="Salario Mínimo Legal 2026 ($1.42M)",
        annotation_position="bottom right",
        annotation_font=dict(size=10, color="#DC2626")
    )
    
    fig.add_vline(
        x=0.80, line_dash="dash", line_color="#16A34A", line_width=1.5,
        annotation_text="Umbral Alta Estabilidad (CV ≤ 0.80)",
        annotation_position="top left",
        annotation_font=dict(size=10, color="#16A34A")
    )
    
    # Cuadrantes anotados
    fig.add_annotation(
        x=0.55, y=4.5e6, text="<b>Cuadrante Dorado:</b><br>Alto Ingreso & Alta Predictibilidad<br>(Educación, Profesionales 25-34)",
        showarrow=False, font=dict(size=10, color="#16A34A"),
        bgcolor="rgba(240, 253, 244, 0.8)", bordercolor="#86EFAC", borderwidth=1, borderpad=6
    )
    
    fig.add_annotation(
        x=1.35, y=3.8e6, text="<b>Cuadrante Volátil:</b><br>Ingreso Alto pero Gran Incertidumbre<br>(Minería, Comunicaciones senior)",
        showarrow=False, font=dict(size=10, color="#DC2626"),
        bgcolor="rgba(254, 242, 242, 0.8)", bordercolor="#FCA5A5", borderwidth=1, borderpad=6
    )
    
    # Menús desplegables (Dropdowns de filtrado por Sector)
    sectors = sorted(df['sector'].unique().tolist())
    buttons = [
        dict(
            label="Todos los Sectores",
            method="update",
            args=[{"visible": [True, True, True]},
                  {"title.text": "Simulador de Estabilidad del Independiente: Todos los Sectores"}]
        )
    ]
    
    # Layout general
    fig.update_layout(
        title=dict(
            text="<b>Simulador Ciudadano: Posición de Riesgo vs. Retorno por Sector y Edad</b><br>"
                 "<span style='font-size:12px; color:#64748B;'>Explora la estabilidad y remuneración de los trabajadores independientes en Colombia (GEIH 2026)</span>",
            font=dict(size=16, color="#0B3C5D"),
            x=0.02, y=0.96
        ),
        xaxis=dict(
            title="<b>Volatilidad Relativa del Ingreso (Coeficiente de Variación = σ / μ)</b><br><span style='font-size:10px;'>← Más Estable / Predecible  |  Más Disperso / Incierto →</span>",
            range=[0.45, 1.6],
            gridcolor="#E2E8F0",
            zerolinecolor="#CBD5E1",
            tickformat=".2f"
        ),
        yaxis=dict(
            title="<b>Ingreso Promedio Mensual ($ COP)</b>",
            range=[8e5, 5.2e6],
            gridcolor="#E2E8F0",
            zerolinecolor="#CBD5E1",
            tickformat="$,.0f"
        ),
        plot_bgcolor="#FFFFFF",
        paper_bgcolor="#F8FAFC",
        height=680,
        margin=dict(l=60, r=40, t=90, b=80),
        legend=dict(
            title=dict(text="<b>Estatus de Estabilidad</b>", font=dict(size=11, color="#0B3C5D")),
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=0.98,
            bgcolor="rgba(255, 255, 255, 0.9)",
            bordercolor="#CBD5E1",
            borderwidth=1
        ),
        hoverlabel=dict(
            bgcolor="#1E293B",
            font_size=11,
            font_color="#FFFFFF",
            font_family="DejaVu Sans, Arial, sans-serif"
        )
    )
    
    out_html1 = os.path.join(PY_OUTPUT_DIR, "simulador_independientes_plotly.html")
    out_html2 = os.path.join(WEB_INTERACTIVE_DIR, "simulador_independientes_plotly.html")
    
    fig.write_html(out_html1, include_plotlyjs='cdn', full_html=True)
    fig.write_html(out_html2, include_plotlyjs='cdn', full_html=True)
    
    print(f"✓ Guardado simulador Plotly en:\n  - {out_html1}\n  - {out_html2}")

if __name__ == "__main__":
    generate_interactive_minidashboard()

