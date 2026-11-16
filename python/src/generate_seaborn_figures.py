"""
generate_seaborn_figures.py
===========================
Generación de las 2 visualizaciones estáticas analíticas en Python con Seaborn
para el Proyecto 3: Narrativa Visual Integrada.

Cumplimiento estricto de:
- Data-Ink Ratio de Tufte y jerarquía visual de Few.
- Títulos de hallazgo analítico ("Takeaway titles").
- Paleta semántica accesible WCAG AA/AAA (Azul #0B3C5D vs Dorado #D99B26).
- Exportación en alta resolución (300 DPI) para reporte y plataforma web.
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
PARQUET_PATH = os.path.join(BASE_DIR, "data", "processed", "base_geih_ciudadana_analisis.parquet")
PY_OUTPUT_DIR = os.path.join(BASE_DIR, "python", "output")
WEB_IMG_DIR = os.path.join(BASE_DIR, "web", "assets", "img")

os.makedirs(PY_OUTPUT_DIR, exist_ok=True)
os.makedirs(WEB_IMG_DIR, exist_ok=True)

# Configuración de estilo global
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#CBD5E1'
plt.rcParams['axes.linewidth'] = 0.8
plt.rcParams['grid.color'] = '#E2E8F0'
plt.rcParams['grid.linestyle'] = '--'
plt.rcParams['grid.alpha'] = 0.7

COLOR_ASALARIADO = "#0B3C5D"   # Azul institucional oscuro (WCAG AAA)
COLOR_INDEPENDIENTE = "#D99B26" # Dorado/Ámbar cálido (WCAG AA)
COLOR_TEXT_DARK = "#1E293B"     # Carbón pizarra
COLOR_TEXT_MUTED = "#64748B"    # Gris texto secundario

def load_data():
    df = pd.read_parquet(PARQUET_PATH)
    # Filtrar sectores con volumen estadísticamente robusto (> 1000 registros)
    sectores_clave = [
        "Comercio", "Agropecuario", "Construcción",
        "Alojamiento y comida", "Industria manufacturera", "Educación"
    ]
    df_filtered = df[df['SectorEconomico'].isin(sectores_clave)].copy()
    # Acotar ingreso al percentil 99 para evitar distorsiones por valores atípicos extremos
    p99 = df_filtered['INGLABO'].quantile(0.99)
    df_filtered = df_filtered[df_filtered['INGLABO'] <= p99]
    return df_filtered

def generate_figure1_distribution(df):
    """
    Figura 1: Distribución continua y asimetría salarial (Violin Plot con Boxplot integrado)
    """
    fig, ax = plt.subplots(figsize=(12, 7), dpi=300)
    fig.patch.set_facecolor('#F8FAFC')
    ax.set_facecolor('#FFFFFF')
    
    palette = {"Asalariado": COLOR_ASALARIADO, "Cuenta propia": COLOR_INDEPENDIENTE}
    
    order = ["Educación", "Industria manufacturera", "Construcción", "Comercio", "Agropecuario", "Alojamiento y comida"]
    
    sns.violinplot(
        data=df,
        x="SectorEconomico",
        y="INGLABO",
        hue="TipoTrabajador",
        split=True,
        inner="quart",
        palette=palette,
        order=order,
        cut=0,
        linewidth=1.2,
        ax=ax
    )
    
    # Formateo de ejes
    ax.set_title("Anatomía de la Brecha Salarial: La Heterogeneidad Interna del Trabajo Independiente",
                 fontsize=14, fontweight='bold', color=COLOR_TEXT_DARK, pad=18, loc='left')
    ax.text(0, 1.02, "Distribución de densidad continua e ingresos intercuartiles (P25, P50, P75) en millones de pesos colombianos (COP)",
            transform=ax.transAxes, fontsize=10, color=COLOR_TEXT_MUTED)
    
    ax.set_xlabel("Sector Económico de Actividad", fontsize=11, fontweight='semibold', color=COLOR_TEXT_DARK, labelpad=10)
    ax.set_ylabel("Ingreso Laboral Mensual ($ COP)", fontsize=11, fontweight='semibold', color=COLOR_TEXT_DARK, labelpad=10)
    
    # Formatear eje Y en millones
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: f"${x/1e6:.1f}M"))
    ax.set_ylim(0, 8.5e6)
    
    # Línea de referencia SMMLV 2026 (~$1.423.500 COP)
    smmlv = 1423500
    ax.axhline(smmlv, color="#DC2626", linestyle=":", linewidth=1.2, alpha=0.85)
    ax.text(5.4, smmlv + 120000, "SMMLV Legal ($1.42M)", color="#DC2626", fontsize=8.5, fontweight='bold', ha='right')
    
    # Anotación preatentiva editorial
    ax.annotate(
        "En Educación y Comercio, el 25% superior de los independientes\nsupera holgadamente el ingreso medio de los asalariados",
        xy=(0.2, 4.8e6), xytext=(0.8, 6.8e6),
        arrowprops=dict(facecolor=COLOR_TEXT_DARK, shrink=0.08, width=1, headwidth=6),
        fontsize=9, fontweight='semibold', color=COLOR_TEXT_DARK,
        bbox=dict(boxstyle="round,pad=0.5", facecolor="#FEF3C7", edgecolor="#D99B26", alpha=0.95)
    )
    
    # Leyenda limpia
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles=handles, labels=["Asalariado (Fijo)", "Cuenta propia (Independiente)"],
              title="Modalidad Laboral", title_fontsize='9', fontsize='9', loc='upper right', framealpha=0.95)
    
    plt.tight_layout()
    
    p1_path = os.path.join(PY_OUTPUT_DIR, "figura1_brecha_distribucion_seaborn.png")
    w1_path = os.path.join(WEB_IMG_DIR, "figura1_brecha_distribucion_seaborn.png")
    plt.savefig(p1_path, dpi=300, facecolor=fig.get_facecolor(), bbox_inches='tight')
    plt.savefig(w1_path, dpi=300, facecolor=fig.get_facecolor(), bbox_inches='tight')
    plt.close()
    print(f"✓ Guardada Figura 1 Seaborn en:\n  - {p1_path}\n  - {w1_path}")

def generate_figure2_lifecycle(df):
    """
    Figura 2: El 'Corredor Dorado' del Ciclo de Vida Laboral (Bootstrap 95% CI)
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6), dpi=300, gridspec_kw={'width_ratios': [1.1, 1]})
    fig.patch.set_facecolor('#F8FAFC')
    ax1.set_facecolor('#FFFFFF')
    ax2.set_facecolor('#FFFFFF')
    
    order_ages = ["18 a 24 años", "25 a 34 años", "35 a 54 años", "55 años o más"]
    palette = {"Asalariado": COLOR_ASALARIADO, "Cuenta propia": COLOR_INDEPENDIENTE}
    
    # Panel 1: Ingreso Mediano con Intervalos de Confianza al 95%
    sns.pointplot(
        data=df,
        x="GrupoEdad",
        y="INGLABO",
        hue="TipoTrabajador",
        estimator=np.median,
        errorbar=('ci', 95),
        n_boot=1000,
        palette=palette,
        order=order_ages,
        markers=["o", "s"],
        linestyles=["-", "--"],
        capsize=0.15,
        ax=ax1
    )
    
    ax1.set_title("Nivel de Ingreso Mediano por Ciclo Vital", fontsize=12, fontweight='bold', color=COLOR_TEXT_DARK, pad=12)
    ax1.set_xlabel("Cohorte de Edad", fontsize=10, fontweight='semibold', color=COLOR_TEXT_DARK)
    ax1.set_ylabel("Ingreso Mediano Mensual ($ COP)", fontsize=10, fontweight='semibold', color=COLOR_TEXT_DARK)
    ax1.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: f"${x/1e6:.1f}M"))
    ax1.grid(True, linestyle="--", alpha=0.5)
    
    # Panel 2: Coeficiente de Variación (CV) por Cohorte de Edad
    # Calculamos CV explícito para cada cohorte
    cv_data = []
    for age in order_ages:
        for tipo in ["Asalariado", "Cuenta propia"]:
            sub = df[(df['GrupoEdad'] == age) & (df['TipoTrabajador'] == tipo)]
            if len(sub) > 0:
                cv = sub['INGLABO'].std() / sub['INGLABO'].mean()
                cv_data.append({"GrupoEdad": age, "TipoTrabajador": tipo, "CV": cv})
    df_cv = pd.DataFrame(cv_data)
    
    sns.barplot(
        data=df_cv,
        x="GrupoEdad",
        y="CV",
        hue="TipoTrabajador",
        palette=palette,
        order=order_ages,
        ax=ax2
    )
    
    ax2.set_title("Volatilidad Relativa del Ingreso (Coeficiente de Variación)", fontsize=12, fontweight='bold', color=COLOR_TEXT_DARK, pad=12)
    ax2.set_xlabel("Cohorte de Edad", fontsize=10, fontweight='semibold', color=COLOR_TEXT_DARK)
    ax2.set_ylabel("Coeficiente de Variación (CV = σ / μ)", fontsize=10, fontweight='semibold', color=COLOR_TEXT_DARK)
    ax2.set_ylim(0, 1.4)
    ax2.grid(True, linestyle="--", alpha=0.5)
    
    # Línea umbral de estabilidad
    ax2.axhline(0.80, color="#16A34A", linestyle=":", linewidth=1.2)
    ax2.text(3.4, 0.82, "Umbral Alta Predictibilidad (CV ≤ 0.80)", color="#16A34A", fontsize=8, fontweight='bold', ha='right')
    
    # Título superior del canvas integrado
    fig.suptitle("El 'Corredor Dorado' del Independiente: La Juventud como Ancla y la Madurez como Divergencia",
                 fontsize=14, fontweight='bold', color=COLOR_TEXT_DARK, y=1.02)
    
    # Sombrear el Corredor Dorado (25 a 34 años)
    ax1.axvspan(0.7, 1.3, color="#FEF3C7", alpha=0.4, label="Corredor Dorado (25-34 años)")
    ax2.axvspan(0.7, 1.3, color="#FEF3C7", alpha=0.4)
    
    ax1.legend(loc='upper left', fontsize='9', title="Modalidad")
    ax2.legend().remove()
    
    plt.tight_layout()
    
    p2_path = os.path.join(PY_OUTPUT_DIR, "figura2_ciclo_vida_bootstrap_seaborn.png")
    w2_path = os.path.join(WEB_IMG_DIR, "figura2_ciclo_vida_bootstrap_seaborn.png")
    plt.savefig(p2_path, dpi=300, facecolor=fig.get_facecolor(), bbox_inches='tight')
    plt.savefig(w2_path, dpi=300, facecolor=fig.get_facecolor(), bbox_inches='tight')
    plt.close()
    print(f"✓ Guardada Figura 2 Seaborn en:\n  - {p2_path}\n  - {w2_path}")

if __name__ == "__main__":
    print("Iniciando generación de figuras Seaborn...")
    df = load_data()
    generate_figure1_distribution(df)
    generate_figure2_lifecycle(df)
    print("✓ Figuras Seaborn generadas exitosamente.")
