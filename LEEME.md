# PROYECTO 3: NARRATIVA VISUAL INTEGRADA (MODALIDAD B)
## «El Mito de la Inestabilidad Independiente en Colombia (GEIH Ene–Jul 2026)»
### Maestría en Ciencia de Datos / Especialización en Analítica Estratégica de Datos
**Asignatura:** Visualización I  
**Institución:** Universidad Externado de Colombia  
**Docentes Evaluadoras:** Adriana Pineda – Paola Moreno  
**Equipo Investigador:** Santiago Sandoval & Sebastián Ramos  
**Fecha de Entrega:** Noviembre de 2026  
**Modalidad Seleccionada:** Modalidad B — Experiencia Digital Guiada Web (Mapa del Tesoro 2D Jugable · Viaje del Héroe)  
**Repositorio GitHub:** https://github.com/santisc1304/Visualizacion-Proyecto3-GEIH2026  
**Power BI Service (Enlace Público en Vivo):** https://app.powerbi.com/view?r=eyJrIjoiZjc3OGE4N2UtMTI3Ni00MGJlLWI1NTItZGU4NWRiZGM5NzRlIiwidCI6IjNiOTQ0ZDlhLTEwNTEtNDY4NS1iMDlkLTlhOTVlZTJkYmQ5OSIsImMiOjR9

---

## 1. RESUMEN DEL PROYECTO Y LA GRAN IDEA

Este proyecto articula sinérgicamente **Power BI**, **Python (Seaborn y Plotly)** y **R (`sf`, `ggplot2` y `tmap`/`leaflet`)** dentro de una experiencia digital jugable 2D estructurada bajo el marco narrativo del **Viaje del Héroe**, para comunicar a una **audiencia ciudadana específica** (trabajadores independientes en Colombia y sus familias) una investigación cuantitativa sobre **183.911 microdatos oficiales** de la Gran Encuesta Integrada de Hogares (GEIH 2026, Enero a Julio) del DANE.

### La Gran Idea:
> *«El mito bancario te dice que trabajar por cuenta propia en Colombia es saltar al vacío financiero. Al sobrevolar los 183.911 registros oficiales de la GEIH 2026 descubrimos que la inestabilidad es un mito cuando se generaliza: en 12 de los 33 departamentos el ingreso independiente es igual o más estable que el asalariado, y sectores especializados con madurez laboral superan con holgura el salario formal. Conocer tu sector, tu etapa vital y tu territorio convierte la incertidumbre en autonomía.»*

---

## 2. MAPA COMPLETO DE ENTREGABLES (RÚBRICA 1–7)

| Requisito | Entregable y Descripción | Ubicación Exacta en el Proyecto |
|---|---|---|
| **1. Power BI Actualizado y Servicio Cloud** | Proyecto modular `.pbip` de 3 páginas (tema pergamino/roble, 20 medidas DAX ponderadas por `FEX_C18` sobre `INGLABO`), respaldo `.pbix`, medidas DAX y enlace público funcional de Power BI Service. | `powerbi/Equipo_Sandoval_Ramos_Proyecto3.pbip`<br>`powerbi/Equipo_Sandoval_Ramos_Proyecto3.pbix`<br>`powerbi/medidas_dax_ponderadas.dax`<br>`powerbi/enlaces_servicio_powerbi.txt` |
| **2. Python Notebook y Plotly Interactivo** | Jupyter Notebook (`.ipynb`) comentado y ejecutado (6/6 celdas con outputs), scripts reproducibles, figuras Seaborn 300 DPI y gráfico interactivo Plotly (`simulador_independientes_plotly.html`). | `python/notebooks/Equipo_Sandoval_Ramos_Proyecto3_Notebook.ipynb`<br>`python/output/figura1_brecha_distribucion_seaborn.png`<br>`python/output/figura2_ciclo_vida_bootstrap_seaborn.png`<br>`python/output/simulador_independientes_plotly.html` |
| **3. Cartografía Espacial en R** | Scripts reproducibles `.R` y `.Rmd` bajo proyección oficial `EPSG:9377`, Shapefile DANE/IGAC (`MGN_DPTO_POLITICO.*`), mapa estático (PNG 300 DPI y PDF vectorial) y mapa interactivo Leaflet/tmap optimizado (< 1 MB). | `r_spatial/scripts/mapa_territorial_geih_sf.R`<br>`r_spatial/scripts/mapa_territorial_geih_sf.Rmd`<br>`data/geographic/MGN_DPTO_POLITICO.*`<br>`r_spatial/output/mapa_estabilidad_departamental.png`<br>`r_spatial/output/mapa_estabilidad_departamental.pdf`<br>`r_spatial/output/mapa_interactivo_tmap.html` |
| **4. Producto Narrativo Final (Modalidad B + PDF Respaldo)** | Experiencia digital guiada 2D en arquitectura web modular (Portada, Bitácora, Mapa del Tesoro 3200×1800 px con avioneta, 6 Estaciones `X1–X6` y 5 Obstáculos por hover) lista para Cloudflare/Vercel, más presentación PDF de respaldo (10 diapositivas). | `index.html`, `vercel.json`, `web/index.html`<br>`web/components/`, `web/css/`, `web/js/`<br>`reports/Equipo_Sandoval_Ramos_Proyecto3_Presentacion_Narrativa.pdf` |
| **5. Datos, Dependencias, Rutas Relativas y LEEME** | Datos procesados consolidados (`183.911` filas en Parquet y CSV UTF-8, métricas departamentales y 44 perfiles del simulador), `requirements.txt`, lanzador local (`run_local_server.bat`) y este `LEEME.md`. | `data/processed/base_geih_ciudadana_analisis.parquet`<br>`data/processed/base_geih_ciudadana_analisis.csv`<br>`data/processed/metricas_departamentales.csv`<br>`data/processed/metricas_perfiles_simulador.json`<br>`requirements.txt`, `run_local_server.bat`, `LEEME.md` |
| **6. Anexo Técnico de Uso de IA (1 Página)** | Declaración transparente de herramientas, prompts relevantes (incluyendo paleta de colores WCAG y medidas DAX ponderadas) y revisión crítica humana. | `reports/Equipo_Sandoval_Ramos_Proyecto3_Anexo_IA.pdf`<br>`reports/Equipo_Sandoval_Ramos_Proyecto3_Anexo_IA.md` |
| **7. Fuentes, Definiciones, Limitaciones y Guión** | Relación formal de fuentes DANE/IGAC, definiciones de variables, reglas de depuración, limitaciones (no causalidad, escala departamental sin extrapolación municipal) y guión completo de sustentación. | `data/raw_metadata/diccionario_variables_geih.md`<br>`reports/Guion_Sustentacion_Oral_10_Minutos.md` |

---

## 3. GUÍA DE REPRODUCCIÓN Y ACCESO

### A. Acceso Directo en la Nube / Local (Sin instalar nada)
1. **Local (1 clic en Windows):** Haz doble clic en `run_local_server.bat` (o ejecuta `python run_local_server.py`) y se abrirá `http://localhost:8080`.
2. **Despliegue Web (Cloudflare Pages / Vercel):** Conecta el repositorio `https://github.com/santisc1304/Visualizacion-Proyecto3-GEIH2026` desde la rama `main` y raíz `./` (todos los activos son menores a 25 MiB).
3. **Power BI Service en vivo:** https://app.powerbi.com/view?r=eyJrIjoiZjc3OGE4N2UtMTI3Ni00MGJlLWI1NTItZGU4NWRiZGM5NzRlIiwidCI6IjNiOTQ0ZDlhLTEwNTEtNDY4NS1iMDlkLTlhOTVlZTJkYmQ5OSIsImMiOjR9

### B. Reproducción Completa del Pipeline y Pruebas QA
```bash
pip install -r requirements.txt
python python/src/data_pipeline.py
python python/src/generate_seaborn_figures.py
python python/src/generate_plotly_minidashboard.py
python python/src/sync_web_components.py
python python/tests/verify_all_metrics.py
Rscript r_spatial/scripts/mapa_territorial_geih_sf.R
```
*(Opcional)* Para regenerar el proyecto PBIR de Power BI ejecuta `python python/src/upgrade_pbip_report.py`.

---

## 4. CRÉDITOS Y ÉTICA ESTADÍSTICA
- **Fuentes:** DANE — Gran Encuesta Integrada de Hogares (GEIH, Ene–Jul 2026, Catálogo ANDA 900); IGAC / DANE — Marco Geoestadístico Nacional (`EPSG:9377`).
- **Principios:** Cero lenguaje causal (solo asociaciones empíricas observadas), respeto estricto a representatividad departamental (sin falacia municipal) y verificación automática (`verify_all_metrics.py`, 5/5 pruebas aprobadas).
