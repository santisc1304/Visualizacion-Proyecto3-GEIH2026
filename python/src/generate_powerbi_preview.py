"""
Generador de Vista Ejecutiva de Alta Resolución (300 DPI) del Dashboard Power BI
para mostrar en la Estación X1 cuando no hay enlace web en vivo de Power BI Service.
Corrige márgenes laterales y colisiones de etiquetas.
"""
import json
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.patches as patches

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data" / "processed"
OUT_IMG = BASE_DIR / "web" / "assets" / "img" / "powerbi_dashboard_ejecutivo.png"

def main():
    dptos = pd.read_csv(DATA_DIR / "metricas_departamentales.csv")
    with open(DATA_DIR / "metricas_perfiles_simulador.json", "r", encoding="utf-8") as f:
        profiles = json.load(f)

    plt.rcParams["font.sans-serif"] = "DejaVu Sans"
    plt.rcParams["axes.edgecolor"] = "#D4AF72"
    plt.rcParams["axes.linewidth"] = 0.9

    fig = plt.figure(figsize=(17, 9.8), dpi=300, facecolor="#FBF4E3")
    gs = gridspec.GridSpec(
        3, 3,
        figure=fig,
        height_ratios=[0.82, 1.58, 1.58],
        width_ratios=[1.15, 1.0, 1.05],
        hspace=0.42,
        wspace=0.34,
        left=0.19, right=0.965, top=0.875, bottom=0.075
    )

    # Barra Superior estilo Power BI Ejecutivo armonizada
    header_ax = fig.add_axes([0.0, 0.905, 1.0, 0.095], facecolor="#2A1808")
    header_ax.set_xticks([])
    header_ax.set_yticks([])
    for s in header_ax.spines.values():
        s.set_visible(False)
    header_ax.text(
        0.025, 0.62,
        "POWER BI  |  MONITOR EJECUTIVO: ESTABILIDAD DEL TRABAJO INDEPENDIENTE EN COLOMBIA (GEIH 2026)",
        color="#FDE68A", fontsize=13.0, fontweight="bold", va="center"
    )
    header_ax.text(
        0.025, 0.24,
        "Corte: Enero - Julio 2026  •  Muestra: 183.911 adultos ocupados  •  Ponderación Censal: FEX_C18 (DANE)  •  S. Sandoval & S. Ramos",
        color="#F6E6C2", fontsize=9.2, va="center"
    )
    header_ax.text(
        0.975, 0.50,
        "FILTRO ACTIVO: Nacional (33 Dptos)  |  Edad >= 18",
        color="#2A1808", fontsize=9.0, fontweight="bold", va="center", ha="right",
        bbox=dict(boxstyle="round,pad=0.45", facecolor="#F59E0B", edgecolor="#FDE047", lw=1.2)
    )

    # Fila 1: 4 Tarjetas KPI (ocupando desde el borde izquierdo real para verse balanceadas)
    kpi_band = fig.add_axes([0.025, 0.745, 0.94, 0.13], facecolor="none")
    kpi_band.set_xticks([])
    kpi_band.set_yticks([])
    for s in kpi_band.spines.values():
        s.set_visible(False)

    gs_kpis = gridspec.GridSpecFromSubplotSpec(1, 4, subplot_spec=gs[0, :], wspace=0.14)
    # Posicionar KPIs manualmente en fig para alinearse de 0.025 a 0.965 sin dejar hueco izquierdo
    kpis = [
        ("MEDIANA CUENTA PROPIA", "$1.200.000 COP", "-31.4% vs. Asalariados ($1.75M)", "#D97706"),
        ("VOLATILIDAD INDEPENDIENTE (CV)", "1.182 (118.2%)", "+11.2 pts más disperso que formal (1.07)", "#DC2626"),
        ("CORREDOR DORADO (35-44 AÑOS)", "$1.400.000 COP", "Etapa de máxima estabilidad y retorno", "#16A34A"),
        ("TERRITORIOS ESTABLES (ΔCV <= 0)", "12 de 33 Dptos.", "Regiones donde independiente es más estable", "#0B3C5D"),
    ]
    kpi_w = 0.224
    kpi_gap = 0.014
    for idx, (title, val, sub, accent) in enumerate(kpis):
        x0 = 0.025 + idx * (kpi_w + kpi_gap)
        ax_k = fig.add_axes([x0, 0.755, kpi_w, 0.115], facecolor="#FFFDF9")
        ax_k.set_xticks([])
        ax_k.set_yticks([])
        for s in ax_k.spines.values():
            s.set_color("#D4AF72")
            s.set_linewidth(1.1)
        rect = patches.Rectangle((0, 0), 0.032, 1, transform=ax_k.transAxes, color=accent, clip_on=False)
        ax_k.add_patch(rect)
        ax_k.text(0.075, 0.77, title, fontsize=8.3, fontweight="bold", color="#784B16", transform=ax_k.transAxes)
        ax_k.text(0.075, 0.43, val, fontsize=15.0, fontweight="bold", color="#2A1808", transform=ax_k.transAxes)
        ax_k.text(0.075, 0.14, sub, fontsize=8.0, fontweight="bold", color=accent, transform=ax_k.transAxes)

    # Ocultar fila 0 de gs porque ya dibujamos las 4 KPIs perfectamente alineadas al ancho total
    for c in range(3):
        ax_dummy = fig.add_subplot(gs[0, c])
        ax_dummy.set_visible(False)

    # Panel 1 (Fila 1, Col 0-1): Ingreso por Macro-Sector (Cohorte 35 a 54 años)
    ax1 = fig.add_subplot(gs[1, 0:2], facecolor="#FFFDF9")
    sectores_map = {}
    for p in profiles:
        if p["grupo_edad"] == "35 a 54 años":
            sectores_map[p["sector"]] = (
                p["mediana"] / 1e6,
                p["ingreso_medio_asalariado"] / 1e6,
                p["cv_ponderado"]
            )
    short_names = {
        "Información y comunicaciones": "Información y comunic.",
        "Servicios profesionales e inmobiliarios": "Servicios prof. e inmob.",
        "Servicios profesionales e inmo": "Servicios prof. e inmob.",
        "Transporte y almacenamiento": "Transporte y almacen.",
        "Arte y entretenimiento": "Arte y entretenimiento",
        "Industria manufacturera": "Industria manufacturera",
        "Alojamiento y comida": "Alojamiento y comida",
    }
    sec_df = pd.DataFrame([
        {"sector": k, "label": short_names.get(k, k), "indep": v[0], "asal": v[1], "cv": v[2]}
        for k, v in sectores_map.items()
    ]).sort_values("indep", ascending=True)

    y_pos = np.arange(len(sec_df))
    h = 0.36
    ax1.barh(y_pos - h/2, sec_df["indep"], height=h, color="#D97706", label="Cuenta Propia (Mediana)")
    ax1.barh(y_pos + h/2, sec_df["asal"], height=h, color="#0B3C5D", label="Referencia Asalariado")
    ax1.set_yticks(y_pos)
    ax1.set_yticklabels(sec_df["label"], fontsize=8.5, fontweight="bold", color="#2A1808")
    ax1.set_xlabel("Ingreso Mensual (Millones COP)", fontsize=8.5, color="#4A2E0F")
    ax1.set_title("1. Ingreso por Sector Económico (Cohorte 35-54 años)", fontsize=10.5, fontweight="bold", color="#2A1808", loc="left", pad=8)
    ax1.legend(loc="lower right", fontsize=8.2, frameon=True, facecolor="#FBF4E3", edgecolor="#D4AF72")
    ax1.grid(axis="x", linestyle="--", alpha=0.5, color="#D4AF72")
    for i, (v_i, v_a) in enumerate(zip(sec_df["indep"], sec_df["asal"])):
        ax1.text(v_i + 0.05, i - h/2, f"${v_i:.2f}M", va="center", fontsize=7.5, color="#92400E", fontweight="bold")
        ax1.text(v_a + 0.05, i + h/2, f"${v_a:.2f}M", va="center", fontsize=7.5, color="#0B3C5D", fontweight="bold")
    ax1.set_xlim(0, max(sec_df["asal"].max(), sec_df["indep"].max()) * 1.17)

    # Panel 2 (Fila 1, Col 2): Curva del Ciclo de Vida
    ax2 = fig.add_subplot(gs[1, 2], facecolor="#FFFDF9")
    edades_order = ["18 a 24 años", "25 a 34 años", "35 a 54 años", "55 años o más"]
    edades_order = [e for e in edades_order if any(p["grupo_edad"] == e for p in profiles)]
    edad_indep, edad_asal = [], []
    for ed in edades_order:
        sub = [p for p in profiles if p["grupo_edad"] == ed]
        edad_indep.append(np.median([x["mediana"] for x in sub]) / 1e6)
        edad_asal.append(np.median([x["ingreso_medio_asalariado"] for x in sub]) / 1e6)

    x_ed = np.arange(len(edades_order))
    ax2.plot(x_ed, edad_asal, marker="o", linewidth=2.6, color="#0B3C5D", label="Referencia Asalariado")
    ax2.plot(x_ed, edad_indep, marker="s", linewidth=2.6, color="#D97706", label="Cuenta Propia (Mediana)")
    if len(edades_order) >= 3:
        ax2.axvspan(1.65, 2.35, color="#16A34A", alpha=0.14, label="Corredor Dorado")
    ax2.set_xticks(x_ed)
    ax2.set_xticklabels(["18-24", "25-34", "35-54", "55+"], fontsize=8.5, fontweight="bold", color="#2A1808")
    ax2.set_ylabel("Millones COP", fontsize=8.5, color="#4A2E0F")
    ax2.set_title("2. Trayectoria por Ciclo de Vida", fontsize=10.5, fontweight="bold", color="#2A1808", loc="left", pad=8)
    ax2.grid(True, linestyle="--", alpha=0.5, color="#D4AF72")
    ax2.legend(loc="upper left", fontsize=7.6, frameon=True, facecolor="#FBF4E3", edgecolor="#D4AF72")
    ax2.set_ylim(0.5, max(edad_asal) * 1.15)

    # Panel 3 (Fila 2, Col 0-1): Ranking Departamental de Volatilidad
    ax3 = fig.add_subplot(gs[2, 0:2], facecolor="#FFFDF9")
    dptos_clean = dptos.dropna(subset=["CV_Indep_Ponderado"]).sort_values("CV_Indep_Ponderado")
    extremos = pd.concat([dptos_clean.head(6), dptos_clean.tail(6)])
    colors_dpto = ["#0B3C5D" if v <= 0.95 else ("#D97706" if v <= 1.15 else "#DC2626") for v in extremos["CV_Indep_Ponderado"]]
    y_d = np.arange(len(extremos))
    ax3.barh(y_d, extremos["CV_Indep_Ponderado"], color=colors_dpto, height=0.62)
    ax3.axvline(1.07, color="#2A1808", linewidth=1.3, linestyle="--", label="Ref. Nacional Asalariado (CV = 1.07)")
    ax3.set_yticks(y_d)
    ax3.set_yticklabels(extremos["DPTO_Nombre"], fontsize=8.5, fontweight="bold", color="#2A1808")
    ax3.set_xlabel("Volatilidad del Ingreso Independiente (Coeficiente de Variación Ponderado)", fontsize=8.5, color="#4A2E0F")
    ax3.set_title("3. Extremos Territoriales: Más Estables (Azul) vs. Más Volátiles (Rojo)", fontsize=10.5, fontweight="bold", color="#2A1808", loc="left", pad=8)
    ax3.grid(axis="x", linestyle="--", alpha=0.5, color="#D4AF72")
    ax3.legend(loc="lower right", fontsize=8.0, frameon=True, facecolor="#FBF4E3", edgecolor="#D4AF72")
    for i, v in enumerate(extremos["CV_Indep_Ponderado"]):
        ax3.text(v + 0.02, i, f"{v:.2f}", va="center", ha="left", fontsize=7.8, fontweight="bold", color="#2A1808")
    ax3.set_xlim(0, extremos["CV_Indep_Ponderado"].max() * 1.15)

    # Panel 4 (Fila 2, Col 2): Mapa de Cuadrantes sin colisiones de texto
    ax4 = fig.add_subplot(gs[2, 2], facecolor="#FFFDF9")
    ax4.scatter(sec_df["cv"], sec_df["indep"], s=105, c="#D97706", edgecolors="#2A1808", linewidth=1.4, zorder=4)
    offsets = {
        "Educación": (6, -4),
        "Información": (-48, -14),
        "Arte": (6, 5),
        "Construcción": (-34, 8),
        "Transporte": (7, 5),
        "Minería": (7, -8),
        "Comercio": (-38, 12),
        "Servicios": (4, -15),
        "Industria": (-8, 11),
        "Alojamiento": (-40, -13),
        "Agropecuario": (8, -11),
    }
    for _, row in sec_df.iterrows():
        short_lbl = row["sector"].split(" ")[0].replace(",", "")
        dx, dy = offsets.get(short_lbl, (5, 5))
        ax4.annotate(
            short_lbl,
            (row["cv"], row["indep"]),
            xytext=(dx, dy),
            textcoords="offset points",
            fontsize=7.3,
            fontweight="bold",
            color="#2A1808",
            arrowprops=dict(arrowstyle="-", color="#94A3B8", lw=0.6)
        )
    ax4.axhline(sec_df["indep"].median(), color="#784B16", linestyle=":", linewidth=1.0)
    ax4.axvline(sec_df["cv"].median(), color="#784B16", linestyle=":", linewidth=1.0)
    ax4.set_xlabel("Volatilidad del Sector (CV)", fontsize=8.5, color="#4A2E0F")
    ax4.set_ylabel("Mediana Independiente ($ M)", fontsize=8.5, color="#4A2E0F")
    ax4.set_title("4. Mapa Retorno vs. Riesgo", fontsize=10.5, fontweight="bold", color="#2A1808", loc="left", pad=8)
    ax4.grid(True, linestyle="--", alpha=0.5, color="#D4AF72")
    ax4.set_xlim(0.65, sec_df["cv"].max() + 0.15)
    ax4.set_ylim(0.55, sec_df["indep"].max() + 0.30)

    OUT_IMG.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT_IMG, dpi=300)
    plt.close(fig)
    print(f"Vista ejecutiva Power BI guardada en: {OUT_IMG}")

if __name__ == "__main__":
    main()
