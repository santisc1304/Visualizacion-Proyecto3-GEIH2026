# GUIÓN DE SUSTENTACIÓN ORAL Y MANUAL DE DEMOSTRACIÓN INTERACTIVA
## PROYECTO 3: NARRATIVA VISUAL INTEGRADA (MODALIDAD B)
### «El Mito de la Inestabilidad Independiente en Colombia (GEIH Ene–Jul 2026)»
**Asignatura:** Visualización I · Universidad Externado de Colombia  
**Docentes Evaluadoras:** Adriana Pineda – Paola Moreno  
**Expositores:** Santiago Sandoval & Sebastián Ramos  
**Duración Objetivo:** 10:00 minutos exactos (alternancia equilibrada)

---

## 1. REGLA DE ORO ANTES DE EMPEZAR A EXPONER
Las profesoras evalúan **dos cosas por igual**:
1. Que cuenten una historia clara (**El Viaje del Héroe + La Gran Idea**, sin perderse en jerga técnica innecesaria).
2. Que **muestren en vivo que las visualizaciones son realmente interactivas** (hacer clic en Power BI, mover filtros, hacer zoom y hover en Plotly, navegar en Leaflet, calcular en el Simulador). Nunca dejes una gráfica estática en pantalla mientras hablas de ella: **muévela mientras explicas**.

---

## 2. CRONÓMETRO Y REPARTO DE PANTALLAS / DIAPOSITIVAS (10 MIN)

| Tiempo | Pantalla / Estación (y Diapositiva PDF equivalente) | Quién habla | Acción clave en pantalla |
|---|---|---|---|
| **0:00 – 1:00** | **Portada + Bitácora de Vuelo** (Diap. 1–2) | Santiago | Mostrar título, autores y clic en *«Pasar a la Experiencia Digital»* → *«Despegar Avioneta»*. |
| **1:00 – 2:30** | **Estación X1 + Obstáculo 1 (`Remolino del Promedio`)** (Diap. 3–4) | Sebastián | Hover sobre el remolino, entrar con `ESPACIO` a **X1** e **interactuar en vivo con Power BI** (3 páginas y filtros). |
| **2:30 – 4:00** | **Estación X2 + Obstáculo 2 (`Kraken`)** (Diap. 5) | Santiago | Entrar a **X2 (Seaborn Raincloud)** y explicar la brecha distributiva real (`$1,20M` vs `$1,75M`, `-31,4%`). |
| **4:00 – 5:15** | **Estación X3 + Obstáculo 3 (`Bosque Escalas`)** (Diap. 6) | Sebastián | Entrar a **X3 (Ciclo de Vida Bootstrap)** y explicar el salto desde `18–24` hacia el **Corredor Dorado** (`35–54 años`). |
| **5:15 – 6:45** | **Estación X4 + Obstáculo 4 (`Cordillera`)** (Diap. 7) | Santiago | Entrar a **X4 (Mapa R `sf` + Leaflet)**, cambiar a la pestaña **Explorador Interactivo** y hacer zoom/clic en departamentos. |
| **6:45 – 8:30** | **Estación X5 + Obstáculo 5 (`Tormenta GEIH`)** (Diap. 8) | Sebastián | Entrar a **X5**, probar 2 perfiles en el **Simulador Ciudadano** y luego cambiar a **Python Plotly** para hacer hover, aislar leyenda y zoom box. |
| **8:30 – 10:00** | **Estación X6 (`Elixir y Cofre`)** (Diap. 9–10) | Ambos | Mostrar los 3 pilares ciudadanos, ética (no causalidad / sin falacia municipal), cierre y preguntas. |

---

## 3. QUÉ DECIR EN CADA PANTALLA / DIAPOSITIVA (GUIÓN DETALLADO)

### A. Pantalla 1 (Portada) y Pantalla 2 (Bitácora de Vuelo) · `[Diapositivas 1 y 2]`
**Voz: Santiago Sandoval (0:00 – 1:00)**
> «Buenos días, profesoras Adriana y Paola, y compañeros.  
> En Colombia, cuando un trabajador independiente busca crédito o estabilidad financiera escucha siempre el mismo veredicto: *“sin nómina fija, sus ingresos son impredecibles y riesgosos”*.  
> Para poner a prueba ese mito procesamos **183.911 registros oficiales de la GEIH del DANE (Enero a Julio de 2026)**, expandidos censalmente con `FEX_C18`.  
> Diseñamos nuestra entrega bajo la **Modalidad B** usando la técnica de storytelling del **Viaje del Héroe** en un mapa cartográfico 2D interactivo: vamos a pilotar la avioneta por **6 estaciones (`X1` a `X6`)** y, a medida que pasemos el cursor sobre los **5 obstáculos del mapa**, veremos los retos reales de datos que resolvimos en el camino.»  
*(Clic en **Pasar a la Experiencia Digital**, lee brevemente los controles en la Bitácora y clic en **Despegar Avioneta ✈️**).*

---

### B. Vuelo hacia Estación X1 (`El Mundo Ordinario`) · `[Diapositivas 3 y 4]`
**Voz: Sebastián Ramos (1:00 – 2:30)**
1. **Antes de entrar a X1**, pasa el cursor sobre el primer obstáculo cercano (`🌀 Remolino del Promedio`):
   > «Fíjense que los obstáculos no interrumpen el vuelo con ventanas largas: al pasar el cursor encima vemos nuestro primer reto metodológico. Si usábamos el promedio simple (`$2,47M`), los ingresos extremos altos (`>$35M`) inflaban la cifra y ocultaban la realidad del trabajador típico. Por eso decidimos usar **Mediana (P50)** y rango **P25–P75** en todo el proyecto.»
2. Llega a **`X1`**, deja que se ilumine y presiona **`ESPACIO`**:
   > «Entramos a la **Estación X1**, donde nuestro protagonista consulta el **Monitor Ejecutivo en Power BI Service conectado en vivo**. El diagnóstico inicial muestra la brecha: mientras el asalariado típico gana **$1.750.000**, el independiente típico gana **$1.200.000 (-31,4%)**, con una volatilidad relativa nacional de **`CV = 1,18`** frente a **`1,07`** del asalariado. Pero quedarse con este promedio nacional es un error: miren qué pasa cuando filtramos en vivo...»  
   *(Sigue la **Guía de Power BI en la Sección 4** abajo mientras explicas!).*

---

### C. Estación X2 (`El Cruce del Umbral` — Python Seaborn Distribución) · `[Diapositiva 5]`
**Voz: Santiago Sandoval (2:30 – 4:00)**
*(Vuela hacia `X2` haciendo clic en `X2` o con las flechas, pasa un segundo el cursor sobre `🐙 Kraken del Sesgo Muestral` y abre `X2`)*:
> «En el obstáculo del Kraken resolvimos un sesgo técnico clave de la encuesta GEIH: originalmente `P6500` excluía a los trabajadores por cuenta propia, así que unificamos `INGLABO` ponderado por `FEX_C18` para recuperar a los **85.608 independientes** y compararlos justamente con **98.303 asalariados**.  
> Al abrir **X2**, cruzamos el umbral hacia **Python Seaborn**. Esta gráfica de violines y boxplots demuestra por qué los promedios mienten: los asalariados (azul) están concentrados alrededor del salario mínimo y prestaciones legales, mientras los independientes (dorado) tienen una distribución mucho más extendida. En sectores como **Educación** o **Información**, el cuartil superior (`P75`) de los independientes compite o supera al empleo formal, mientras sectores como Comercio muestran colas mucho más dispersas.»

---

### D. Estación X3 (`Las Pruebas y Aliados` — Python Seaborn Ciclo de Vida) · `[Diapositiva 6]`
**Voz: Sebastián Ramos (4:00 – 5:15)**
*(Pasa el cursor sobre `🌲 Bosque de Escalas Asimétricas` —escala logarítmica/IQR para no aplastar el gráfico— y abre `X3`)*:
> «Aquí en **X3** nos preguntamos: *¿la edad influye en la estabilidad del independiente?* Usamos **intervalos de confianza Bootstrap al 95% (1.000 réplicas)** sobre la mediana por cohorte de edad.  
> El hallazgo es clarísimo: entre los **18 y 24 años**, trabajar por cuenta propia sin red de clientes ni capital de respaldo tiene ingresos medianos muy bajos y alta fragilidad. En cambio, al consolidarse en el **Corredor Dorado (35 a 54 años, y consolidación desde los 25–34)**, el retorno mediano alcanza su máximo (por ejemplo, en **Educación 35–54 años** llega a **`$2.600.000`** con `CV = 0,76`, y en **25–34 años** es de **`$2.500.000`** con `CV = 0,74`, estabilidad alta).»

---

### E. Estación X4 (`La Exploración del Territorio` — Cartografía R `sf` + Leaflet) · `[Diapositiva 7]`
**Voz: Santiago Sandoval (5:15 – 6:45)**
*(Pasa el cursor sobre `🏔️ Cordillera de Confusores` y abre `X4`)*:
> «En **X4** llevamos el análisis al territorio con **R (`sf`, `ggplot2`, `tmap/leaflet`)** en proyección oficial **`EPSG:9377`**.  
> **Decisión ética fundamental:** Respetamos estrictamente la escala **Departamental (33 entidades: 32 departamentos + Bogotá D.C.)** porque la GEIH del DANE no tiene representatividad estadística municipal; hacer un mapa municipal habría causado falacia ecológica.  
> ¿Qué descubre el mapa? **En 12 de los 33 departamentos** (tonos azules, donde `ΔCV ≤ 0`), trabajar independiente es **igual o más estable** que ser asalariado. Aparece la paradoja territorial: en departamentos con menor dispersión relativa como **Guainía (`CV = 0,49`)**, **Putumayo (`CV = 0,63`)**, **Amazonas (`CV = 0,64`)** y **Arauca (`CV = 0,64`)**, el ingreso independiente es sorprendentemente predecible; en contraste, **Boyacá (`CV = 2,66`)**, **Cundinamarca (`CV = 2,31`)**, **Antioquia (`1,30`)** y **Bogotá (`1,27`, aunque con la media más alta `$2,78M`)** concentran simultáneamente consultores muy bien pagos e informalidad de subsistencia, disparando la varianza.»  
*(Haz clic en la pestaña **🌐 Explorador Interactivo Leaflet**, haz zoom con la rueda del mouse y clic sobre Bogotá, Guainía o Boyacá para mostrar los popups en vivo).*

---

### F. Estación X5 (`El Oráculo del Ciudadano` — Simulador JS + Python Plotly) · `[Diapositiva 8]`
**Voz: Sebastián Ramos (6:45 – 8:30)**
*(Pasa el cursor sobre `⛈️ Tormenta de Microdatos GEIH` —resuelta con `verify_all_metrics.py` y JSON preagregado— y abre `X5`)*:
> «En **X5** traducimos toda la estadística en una herramienta ciudadana práctica con dos pestañas:  
> 1. Primero, en nuestra **Calculadora Ciudadana**, un trabajador no tiene que saber qué es un Coeficiente de Variación. Probemos dos casos opuestos en vivo... *(cambia selectores: Caso 1 `Educación` + `25 a 34 años` -> Estabilidad Alta, `$2.500.000`, `CV 0,74`, colchón `2 a 3 meses`; Caso 2 `Comercio` + `35 a 54 años` -> Volatilidad Elevada, `$1.000.000`, `CV 1,16`, colchón `6 meses o más`)*.  
> 2. Ahora paso a la segunda pestaña: el **Mapa Interactivo de 44 Perfiles en Python Plotly**...»  
*(Sigue la **Guía paso a paso de Plotly en la Sección 5** abajo mientras explicas).*

---

### G. Estación X6 (`El Regreso con el Elixir` — Síntesis, Ética y Cofre) · `[Diapositivas 9 y 10]`
**Voz: Santiago Sandoval & Sebastián Ramos (8:30 – 10:00)**
* **Santiago:** Resume los **3 mensajes accionables** para el ciudadano:
  1. Presupuestar siempre con la **Mediana (P50)** y usar **P25** como piso para gastos fijos (nunca con promedios inflados).
  2. Aprovechar la ventana de consolidación (**25–54 años**) y especialización sectorial para elevar predictibilidad.
  3. Ajustar el **colchón de emergencia** al nivel de riesgo del oficio (2–3 meses en perfiles estables; 6+ meses en sectores estacionales).
* **Sebastián:** Cierra con **rigor ético y reproducibilidad**:
  - Estudio puramente **descriptivo y asociativo** (no inferencia causal).
  - Respeto a representatividad DANE (`EPSG:9377`, escala departamental).
  - **Cofre de Entregables** con acceso directo a `.pbix`/`.pbip`, `.ipynb` ejecutado, `.R`/`.Rmd`, PDF de 10 diapositivas, Anexo de IA de 1 página y Diccionario metodológico verificado con `verify_all_metrics.py` (5/5 pruebas OK).

---

## 4. GUÍA PRÁCTICA DE INTERACCIÓN EN VIVO: POWER BI (ESTACIÓN X1)

Cuando abras la **Estación X1** frente a las profesoras, el tablero **ya está incrustado y publicado en vivo**. Haz exactamente esta secuencia de **4 movimientos en ~45 segundos** para lucir el dominio total de la interactividad:

1. **Movimiento 1 — Barra Superior de Navegación entre 3 Páginas:**
   - Señala el menú dorado arriba a la derecha dentro del Power BI: **`1. Panorama Ejecutivo` | `2. Ciclo de Vida y Brechas` | `3. Simulador Ciudadano`**.
   - Haz clic en **`2. Ciclo de Vida y Brechas`** (muestra rápidamente la matriz de calor `Sector × Grupo de Edad`, la evolución mensual `Ene–Jul 2026`, columnas de ingreso medio ponderado y el gráfico de dona `Independientes vs. Asalariados`).
   - Luego pasa a **`3. Simulador Ciudadano`** (muestra las 4 tarjetas dinámicas del semáforo de predictibilidad + la tabla completa filtrable) y regresa a **`1. Panorama Ejecutivo`**.

2. **Movimiento 2 — Cross-Filtering (Filtro Cruzado al hacer clic en una barra):**
   - En **`1. Panorama Ejecutivo`**, en la gráfica superior izquierda (*«1. Mediana de Ingreso por Sector Económico»*), **haz clic directamente sobre la barra de `Educación`** (o `Comercio`).
   - **Qué señalar en voz alta:** *«Miren cómo al tocar un solo sector, todas las tarjetas KPI arriba (`Mediana`, `CV`, `Brecha`, `Corredor Dorado`), la curva de edad a la derecha y los 33 departamentos abajo se recalculan instantáneamente solo para ese sector».*
   - Vuelve a hacer **clic en la misma barra** (o en el espacio blanco de la gráfica) para quitar el filtro.

3. **Movimiento 3 — Segmentadores Sincronizados (Slicers):**
   - Abre el menú desplegable de **`Grupo de Edad`** arriba y selecciona **`25 a 34 años`** o **`35 a 54 años`** (y si quieres, combina con **`Departamento`** = `Antioquia` o `Bogotá D.C.`).
   - Cambia a la pestaña **`3. Simulador Ciudadano`** para demostrar que **los filtros quedaron sincronizados entre páginas** (`syncGroup`): las tarjetas de **Semáforo** y **Colchón Sugerido** y la tabla ya están filtradas para esa misma persona. *(Luego limpia los filtros con el ícono de borrador de cada slicer).*

4. **Movimiento 4 — Hover Tooltips y Pantalla Completa:**
   - Pasa el cursor sobre una burbuja extrema en la gráfica 4 (*«Mapa Retorno vs. Riesgo por Sector»*) para mostrar el tooltip exacto, o usa el botón **↗ Abrir en Pantalla Completa** si deseas que la profesora vea las 3 páginas a tamaño monitor completo.

---

## 5. GUÍA PRÁCTICA DE INTERACCIÓN EN VIVO: PYTHON PLOTLY (ESTACIÓN X5)

Al entrar a **Estación X5** y pasar a la segunda pestaña (**`📈 Mapa Interactivo de 44 Perfiles (Python Plotly)`**), el gráfico muestra los **44 perfiles (`11 sectores × 4 grupos de edad`)** en el plano **Riesgo (`CV`) vs. Retorno (`Mediana COP`)**:

1. **Explicar primero la lectura visual rápida (5 seg):**
   - **Eje horizontal (X):** Volatilidad o Coeficiente de Variación (`CV`). Más a la **izquierda** = ingresos más estables y predecibles; más a la **derecha** = ingresos variables.
   - **Eje vertical (Y):** Ingreso mensual típico (**Mediana P50** en COP). Más **arriba** = mayor remuneración.
   - **Tamaño de burbuja:** Número de personas encuestadas en ese perfil dentro de la GEIH (`n_muestra`).
   - **Color / Leyenda:** Cada color distingue una cohorte de edad / nivel de estabilidad.

2. **Movimiento 1 — Tooltip Enriquecido al Pasar el Cursor (`Hover`):**
   - Mueve el puntero suavemente hacia una burbuja alta a la izquierda (**Educación 25–34 años**) y otra burbuja baja a la derecha (**Comercio o Construcción**).
   - **Qué señalar:** *«Cada punto en Plotly despliega el detalle completo: Mediana `P50`, rango `P25–P75`, brecha vs. asalariado, `CV` exacto y el tamaño muestral real del DANE».*

3. **Movimiento 2 — Aislar Cohortes desde la Leyenda (`Clic` vs `Doble Clic`):**
   - **Truco estrella:** Haz **doble clic** sobre una categoría en la leyenda derecha (por ejemplo, **`25 a 34 años`** o **`35 a 54 años`**). Eso oculta todas las demás edades y deja **solo esa etapa del ciclo de vida** en pantalla, demostrando visualmente qué sectores forman el Corredor Dorado!
   - Haz **un solo clic** sobre otra cohorte para superponer ambas y compararlas directamente (ej. comparar `18 a 24 años` vs `35 a 54 años`).
   - Vuelve a hacer **doble clic** en la leyenda para restaurar los 44 puntos.

4. **Movimiento 3 — Zoom Box sobre la Zona Densa y Reset:**
   - Arrastra con el mouse formando un rectángulo (**Zoom Box**, herramienta activa por defecto) sobre las burbujas agrupadas entre `$600k` y `$1,5M` para despejar el solapamiento y leer claramente sectores populares como `Comercio`, `Alojamiento y comida`, `Transporte` y `Agropecuario`.
   - Haz **doble clic en cualquier espacio vacío del gráfico** (o clic en el ícono de casita **Reset axes** arriba a la derecha) para regresar al panorama completo de los 44 perfiles.

---

## 6. GUÍA RÁPIDA: MAPA LEAFLET EN R (ESTACIÓN X4)
En **Estación X4 → Pestaña 2 (`🌐 Explorador Interactivo Leaflet`)**:
1. Haz zoom con la rueda del mouse hacia el sur/oriente (**Guainía**, **Putumayo**, **Amazonas** — tonos azules/estables) y luego hacia el centro andino (**Bogotá D.C.**, **Boyacá**, **Cundinamarca**, **Antioquia** — tonos rojos/alta dispersión).
2. Haz **clic** sobre dos departamentos contrastantes para abrir su popup exacto (`Mediana Indep.`, `Mediana Asal.`, `CV Indep.`, `Brecha %`, `Índice de Predictibilidad`).

---

## 7. BANCO DEFENSIVO DE PREGUNTAS DIFÍCILES DE LAS PROFESORAS

1. **«¿Por qué el mapa de R llega hasta Departamentos y no a Municipios?»**
   > *Respuesta:* El marco muestral probabilístico de la GEIH del DANE tiene representatividad estadística garantizada a nivel Nacional, Regional, Departamental (33 dominios) y 23 Ciudades/Áreas Metropolitanas, **no para los 1.121 municipios**. Mapear municipios con la GEIH violaría el diseño muestral y produciría falacia ecológica. Usamos proyección oficial **EPSG:9377 (MAGNA-SIRGAS Origen Nacional)**.
2. **«¿Por qué cambiaron `P6500` por `INGLABO` ponderado por `FEX_C18`?»**
   > *Respuesta:* En la GEIH del DANE, `P6500` corresponde a ingreso de asalariados y viene nulo para trabajadores por cuenta propia (cuya ganancia se consolida en `INGLABO`). Al conectar el modelo semántico `.pbip` y Python a `INGLABO` ponderado por el factor de expansión censal `FEX_C18`, recuperamos los `85.608` independientes reales y garantizamos inferencia poblacional fiel.
3. **«¿Se puede afirmar que cambiar de sector o cumplir 35 años *causa* estabilidad?»**
   > *Respuesta:* No. La GEIH es un corte transversal repetido, no un experimento ni un panel longitudinal. Todos nuestros hallazgos describen **asociaciones empíricas y distribuciones observadas**, nunca relaciones causales.
4. **«¿Por qué eligieron HTML modular en Modalidad B en vez de Streamlit?»**
   > *Respuesta:* La rúbrica admite experiencias digitales guiadas interactivas ("por ejemplo en Streamlit"). La arquitectura modular HTML/CSS/JS nos permitió integrar de forma fluida el mapa 2D del Viaje del Héroe, el Power BI Service publicado en vivo, el mapa Leaflet de R, el cuadrante Plotly y la Calculadora Ciudadana con despliegue instantáneo en Cloudflare/Vercel y cumplimiento de contraste WCAG.
