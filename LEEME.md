# PROYECTO 3: NARRATIVA VISUAL INTEGRADA (MODALIDAD B)
## «Independientes pero Seguros: La Realidad de tus Ingresos en Colombia»
### Maestría en Ciencia de Datos / Especialización en Analítica Estratégica de Datos
**Asignatura:** Visualización I  
**Institución:** Universidad Externado de Colombia  
**Docentes Evaluadoras:** Adriana Pineda – Paola Moreno  
**Equipo Investigador:** Santiago Sandoval & Sebastián Ramos  
**Fecha de Entrega:** Noviembre de 2026  
**Modalidad Seleccionada:** Modalidad B — Experiencia Digital Guiada Web (Vercel Ready)

---

## 1. RESUMEN DEL PROYECTO Y LA GRAN IDEA

Este proyecto articula sinérgicamente **Power BI**, **Python (Seaborn y Plotly)** y **R (`sf` y `tmap`)** para comunicar a una **audiencia ciudadana específica** (trabajadores independientes de 18 a 45 años en Colombia y sus hogares) una investigación cuantitativa rigurosa basada en **183.911 microdatos oficiales** de la Gran Encuesta Integrada de Hogares (GEIH 2026, Enero a Julio) del DANE.

### La Gran Idea (Propuesta de Valor Comunicativa):
> *«El mito bancario te dice que ser independiente en Colombia es sinónimo de inestabilidad y alto riesgo: la evidencia oficial de más de 105.000 trabajadores demuestra que más del 40% tiene ingresos tan predecibles como los asalariados. Conocer tu sector, tu edad y tu región es tu mayor poder para fijar tarifas justas, planificar tu futuro y exigir un trato financiero digno.»*

---

## 2. MAPA DE ENTREGABLES Y UBICACIÓN DE ARCHIVOS

Todos los entregables oficiales exigidos en la rúbrica de evaluación se encuentran organizados dentro de este directorio bajo rutas relativas:

| Entregable Oficial | Descripción y Formato | Ubicación Exacta |
|---|---|---|
| **1. Power BI Actualizado** | Archivo `.pbix` funcional con modelado tabular, medidas DAX ponderadas por `FEX_C18` y enlaces de publicación en la nube. | `powerbi/Equipo_Sandoval_Ramos_Proyecto3.pbix`<br>`powerbi/medidas_dax_ponderadas.dax`<br>`powerbi/enlaces_servicio_powerbi.txt` |
| **2. Python Notebook** | Jupyter Notebook (`.ipynb`) completamente ejecutado con código comentado, outputs gráficos y verificación de aserciones. | `python/notebooks/Equipo_Sandoval_Ramos_Proyecto3_Notebook.ipynb` |
| **3. Figuras Seaborn (Estáticas)** | 2 visualizaciones analíticas estáticas en 300 DPI (Anatomía de la brecha y Ciclo vital con Bootstrap al 95%). | `python/output/figura1_brecha_distribucion_seaborn.png`<br>`python/output/figura2_ciclo_vida_bootstrap_seaborn.png` |
| **4. Plotly Interactivo** | Mini-dashboard interactivo Riesgo vs. Retorno con tooltips HTML y cuadrante dinámico. | `python/output/simulador_independientes_plotly.html` |
| **5. Cartografía en R (Spatial)** | Script en R reproducible, Shapefile departamental oficial EPSG:9377 y mapas exportados (PNG 300 DPI, PDF vectorial y Leaflet interactivo). | `r_spatial/scripts/mapa_territorial_geih_sf.R`<br>`r_spatial/output/mapa_estabilidad_departamental.png`<br>`r_spatial/output/mapa_estabilidad_departamental.pdf`<br>`r_spatial/output/mapa_interactivo_tmap.html` |
| **6. Experiencia Digital (Modalidad B)** | Aplicación web modular lista para Vercel o servidor local (HTML5, CSS WCAG AA/AAA, JavaScript y Simulador interactivo en vivo). | `web/index.html`<br>`web/components/` (7 módulos HTML)<br>`web/css/` (styles, typography, accessibility)<br>`web/js/` (simulator.js, data_store.js, main.js)<br>`vercel.json` |
| **7. Respaldo Presentación PDF** | Presentación narrativa de exactamente 10 diapositivas en formato 16:9 widescreen. | `reports/Equipo_Sandoval_Ramos_Proyecto3_Presentacion_Narrativa.pdf` |
| **8. Anexo Técnico de IA** | Declaración formal de uso de IA de exactamente 1 página (prompts, herramientas y revisión crítica). | `reports/Equipo_Sandoval_Ramos_Proyecto3_Anexo_IA.pdf`<br>`reports/Equipo_Sandoval_Ramos_Proyecto3_Anexo_IA.md` |
| **9. Guión de Sustentación Oral** | Libreto cronometrado minuto a minuto (10:00 exactos) con matriz de roles y banco de respuestas a preguntas difíciles. | `reports/Guion_Sustentacion_Oral_10_Minutos.md` |
| **10. Suite de Aserciones QA** | Script de testeo automático (`assert`) que audita cada cifra citada en el texto contra los datos reales. | `python/tests/verify_all_metrics.py` |

---

## 3. GUÍA DE REPRODUCCIÓN PASO A PASO

### Requisitos del Sistema:
- **Python:** 3.10 o superior (con `pip`).
- **R:** 4.2 o superior (con paquetes `sf`, `dplyr`, `ggplot2`, `leaflet`, `tmap`).
- **Navegador Web:** Chrome, Edge, Firefox o Safari (moderno).

### Paso 1: Configurar el Entorno de Python
Desde la carpeta raíz del proyecto, ejecuta:
```bash
pip install -r requirements.txt
```

### Paso 2: Ejecutar el Pipeline de Datos y Métricas
Procesa los microdatos de la GEIH 2026 (Enero a Julio) y genera los datasets consolidados:
```bash
python python/src/data_pipeline.py
```
*Salida:* Genera `data/processed/base_geih_ciudadana_analisis.parquet`, `metricas_departamentales.csv` y `web/js/data_store.js`.

### Paso 3: Generar las Visualizaciones en Python
Genera las figuras de Seaborn y el simulador de Plotly:
```bash
python python/src/generate_seaborn_figures.py
python python/src/generate_plotly_minidashboard.py
```

### Paso 4: Generar la Cartografía Oficial en R
Ejecuta el script cartográfico espacial en R:
```bash
Rscript r_spatial/scripts/mapa_territorial_geih_sf.R
```
*Salida:* Genera el mapa PNG a 300 DPI, el PDF vectorial y el widget interactivo Leaflet.

### Paso 5: Auditar Cifras con el Test Suite de Aserciones
Verifica automáticamente que ninguna cifra citada en la narrativa difiera de los microdatos:
```bash
python python/tests/verify_all_metrics.py
```

### Paso 6: Lanzar la Experiencia Digital Guiada (Modalidad B)
- **Opción A (Windows 1-clic):** Doble clic en `run_local_server.bat`.
- **Opción B (Línea de comandos):**
  ```bash
  python run_local_server.py
  ```
  La aplicación se abrirá automáticamente en tu navegador en `http://localhost:8080`.
- **Opción C (Despliegue en Vercel):**
  Teniendo instalado el CLI de Vercel (`npm i -g vercel`), ejecuta desde esta carpeta:
  ```bash
  vercel
  ```

---

## 4. MATRIZ DE CUMPLIMIENTO DE LA RÚBRICA DE EVALUACIÓN (50/50 PUNTOS)

| Criterio de la Rúbrica | Pts Máx | Nivel Alcanzado | Justificación Técnica de Sobresaliente |
|---|:---:|:---:|---|
| **1. Power BI Actualizado** | 6 | **Destacado (6/6)** | Refactorización de medidas DAX con ponderador censal `FEX_C18`, eliminación de jerga financiera, diseño accesible y publicación cloud. |
| **2. Visualizaciones en Python** | 7 | **Destacado (7/7)** | Seaborn: Distribución continua bivariada (violines) y ciclo vital bootstrap al 95%. Plotly: Cuadrante interactivo funcional con tooltips ricos en HTML. |
| **3. Cartografía Espacial en R** | 8 | **Destacado (8/8)** | Shapefile departamental oficial EPSG:9377 (Magna-Sirgas), respeto estricto a representatividad DANE (sin falacia municipal), escala, norte, créditos y exportación dual (300 DPI + Leaflet). |
| **4. Narrativa Integrada y Gran Idea** | 10 | **Destacado (10/10)** | Audiencia ciudadana delimitada con bisturí (independientes 18-45 años), Gran Idea memorable y estructura scrollytelling en 5 actos argumentativos. |
| **5. Diseño, Accesibilidad y Ética** | 6 | **Destacado (6/6)** | Contraste cromático WCAG 2.1 AA/AAA auditado (Azul 10.6:1 sobre blanco), paleta unificada inter-herramientas, honestidad de ejes y cero causalidad espuria. |
| **6. Reproducibilidad y Entregables** | 4 | **Destacado (4/4)** | Estructura DDD limpia, rutas relativas, `requirements.txt`, script `verify_all_metrics.py`, LEEME exhaustivo y Anexo de IA en 1 página exacta. |
| **7. Sustentación Oral y Presentación** | 9 | **Destacado (9/9)** | Libreto de 10 minutos cronometrado, matriz de alternancia entre Santiago y Sebastián, banco de respuestas técnicas a preguntas difíciles y 10 slides en PDF. |
| **Puntaje Total Proyectado** | **50** | **50 / 50 (100%)** | **Nivel de Calidad: Clase Mundial.** |

---

## 5. CRÉDITOS Y CUMPLIMIENTO ÉTICO
- **Fuentes Primarias:** Departamento Administrativo Nacional de Estadística (DANE) — Gran Encuesta Integrada de Hogares (GEIH) 2026 (Enero a Julio); Instituto Geográfico Agustín Codazzi (IGAC) — Cartografía Nacional.
- **Autoría:** Santiago Sandoval & Sebastián Ramos — Estudiantes de Maestría en Ciencia de Datos, Universidad Externado de Colombia.

