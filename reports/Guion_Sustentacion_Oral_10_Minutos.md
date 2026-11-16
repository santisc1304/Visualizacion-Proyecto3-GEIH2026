# GUIÓN OFICIAL DE SUSTENTACIÓN ORAL (10 MINUTOS EXACTOS)
## PROYECTO 3: NARRATIVA VISUAL INTEGRADA
### Asignatura: Visualización I · Maestría en Ciencia de Datos · Universidad Externado de Colombia
**Docentes:** Adriana Pineda – Paola Moreno  
**Equipo Expositor:** Santiago Sandoval & Sebastián Ramos  
**Fecha de Presentación:** Noviembre de 2026  
**Modalidad Evaluada:** Modalidad B (Experiencia Digital Guiada Web + Artefactos Integrados)

---

## 1. ESTRUCTURA CRONOMÉTRICA Y MATRIZ DE ROLES (10:00 MINUTOS)

```
┌──────────────┬───────┬──────────────────────────────────────────┬──────────────────┐
│ INTERVALO    │ TIEMPO│ SECCIÓN Y CONTENIDO                      │ RESPONSABLE      │
├──────────────┼───────┼──────────────────────────────────────────┼──────────────────┤
│ 00:00 - 01:00│ 1 min │ Problemática, Audiencia y Pregunta       │ Santiago Sandoval│
│ 01:00 - 03:00│ 2 min │ Contexto (GEIH 2026) y La Gran Idea      │ Sebastián Ramos  │
│ 03:00 - 04:15│ 1.25m │ Evidencia en Python Seaborn (Fig 1 y 2)  │ Santiago Sandoval│
│ 04:15 - 05:30│ 1.25m │ Cartografía en R (sf/tmap en EPSG:9377)  │ Sebastián Ramos  │
│ 05:30 - 06:45│ 1.25m │ Demostración en Vivo: Simulador Plotly/JS│ Santiago Sandoval│
│ 06:45 - 08:00│ 1.25m │ Repositorio Power BI & DAX Ponderado     │ Sebastián Ramos  │
│ 08:00 - 10:00│ 2 min │ Síntesis, Límites Éticos y Mensaje Final │ Ambos            │
└──────────────┴───────┴──────────────────────────────────────────┴──────────────────┘
```

---

## 2. LIBRETO PASO A PASO (TRANSMISIÓN VERBAL RECOMENDADA)

### Minuto 0:00 a 1:00 | Problemática, Audiencia y Pregunta Analítica
**Voz: Santiago Sandoval**
> «Buenos días, profesoras Adriana y Paola, y compañeros.  
> En Colombia, más del 46% de los trabajadores ocupados se gana la vida de manera independiente o por cuenta propia. Son electricistas, comerciantes, diseñadores, profesionales de la salud o técnicos. Sin embargo, cuando se acercan a la ventanilla de un banco a solicitar un crédito para hacer crecer su negocio, se encuentran con una barrera infranqueable: *«Si no tiene contrato laboral indefinido y desprendible de nómina de los últimos tres meses, usted es considerado de alto riesgo»*.  
> 
> Nuestra audiencia no es 'el público general': son **los trabajadores independientes colombianos de 18 a 45 años y sus familias**, quienes sufren este estigma y necesitan comprender su realidad económica.  
> Por eso formulamos nuestra pregunta central: *¿Es realmente el trabajo independiente en Colombia un salto al vacío financiero, o existen sectores, edades y regiones donde los ingresos son tan predecibles como un sueldo fijo; y cómo puede el ciudadano usar esta evidencia para fijar precios y defender su bienestar?*»

---

### Minuto 1:00 a 3:00 | Contexto Metodológico y La Gran Idea
**Voz: Sebastián Ramos**
> «Para responder esta pregunta no improvisamos: procesamos **183.911 microdatos oficiales de la Gran Encuesta Integrada de Hogares (GEIH 2026)** recopilados entre enero y julio por el DANE, aplicando rigurosamente los factores de expansión censal `FEX_C18`.  
> 
> Al cruzar ingresos laborales y variabilidad estadística, descubrimos que tratar al independiente como un bloque homogéneo de insolvencia es un profundo error analítico. Esto nos permitió formular **La Gran Idea** que guía toda nuestra experiencia digital:  
> 
> *(Proyectando La Gran Idea en pantalla grande)*  
> **«El mito bancario te dice que ser independiente en Colombia es sinónimo de inestabilidad y alto riesgo: la evidencia oficial de más de 105.000 trabajadores demuestra que más del 40% tiene ingresos tan predecibles como los asalariados. Conocer tu sector, tu edad y tu región es tu mayor poder para fijar tarifas justas, planificar tu futuro y exigir un trato financiero digno.»**  
> 
> Para comunicar esto a la ciudadanía, elegimos la **Modalidad B**, construyendo una experiencia web interactiva modular que ahora les presentaremos en vivo.»

---

### Minuto 3:00 a 4:15 | Evidencia en Python Seaborn: Distribución y Ciclo de Vida
**Voz: Santiago Sandoval**
> *(Navegando a la sección 'La Evidencia' en la web app)*  
> «Aquí en nuestra experiencia digital, el ciudadano se encuentra con dos visualizaciones analíticas estáticas en Seaborn diseñadas bajo el principio de alto contraste WCAG:  
> 1. En la **Figura 1**, los violines de densidad demuestran que mientras los asalariados (en azul marino) están rígidamente concentrados en el salario mínimo, los independientes (en dorado) presentan una gran riqueza distributiva. En sectores como Educación (con ingreso medio de $4.04M y CV de 0,71) y Comercio, el 25% superior de los independientes gana significativamente más que los asalariados formales del mismo sector. Además, en Alojamiento y Comida el CV es de apenas 0,59, el más bajo de la economía.  
> 2. En la **Figura 2**, mediante estimación bootstrap al 95% de confianza, identificamos el **'Corredor Dorado' de los 25 a los 34 años**: 30.132 personas que alcanzan un ingreso promedio de $2,27M con un CV de 0,80, desmintiendo que solo la vejez otorgue predictibilidad.»

---

### Minuto 4:15 a 5:30 | Cartografía en R: La Paradoja de las Metrópolis
**Voz: Sebastián Ramos**
> *(Desplazándose al mapa interactivo y proyectando el mapa R en EPSG:9377)*  
> «Al pasar al territorio en R utilizando `{sf}` y `{tmap}`, encontramos un hallazgo fascinante: **La Paradoja de las Grandes Metrópolis**.  
> El sentido común sugeriría que vivir en Bogotá ofrece mayor estabilidad. Los datos revelan lo contrario: aunque Bogotá D.C. lidera el ingreso medio del país ($3,52M COP), registra simultáneamente **el coeficiente de variación más alto de toda Colombia: 1,26**. Similar volatilidad extrema ocurre en Atlántico (1,14) y Valle del Cauca (1,09).  
> 
> En cambio, la estabilidad no está en las capitales densas, sino en departamentos intermedios como Putumayo (CV = 0,47), Amazonas (0,57), San Andrés (0,63) y Risaralda (0,80).  
> **Nota de rigor ético:** Nuestro mapa respeta estrictamente el marco muestral del DANE a nivel departamental; no extrapolamos a municipios porque la GEIH no tiene representatividad municipal, evitando incurrir en falacia ecológica.»

---

### Minuto 5:30 a 6:45 | Demostración en Vivo: El Simulador Ciudadano Interactivo
**Voz: Santiago Sandoval**
> *(Interactuando en vivo con los selectores del simulador en la web)*  
> «Queríamos que el ciudadano no fuera un espectador pasivo, sino que pudiera diagnosticar su propio oficio.  
> Observemos en vivo: si soy una diseñadora o comerciante independiente de 28 años en Risaralda:  
> - Selecciono *Comercio*, *25 a 34 años* y *Risaralda*.  
> - El simulador calcula al instante: mi mediana típica es de **$1.800.000 COP**, mi predictibilidad es **Alta (CV = 0,80)**, y el sistema me aconseja un colchón de reserva de **3 a 5 meses**.  
> - Además, en el cuadrante interactivo de Plotly que tenemos integrado abajo, puedo hacer zoom, filtrar por sector y ver exactamente en qué percentil se ubica mi actividad económica.»

---

### Minuto 6:45 a 8:00 | Integración con Power BI Service y DAX Ponderado
**Voz: Sebastián Ramos**
> *(Mostrando la sección Power BI y el enlace al servicio)*  
> «Para el analista o ciudadano que requiere exploración profunda, conservamos e integramos el dashboard de Power BI del Proyecto 1, pero completamente evolucionado:  
> 1. **DAX Ponderado:** Refactorizamos las medidas en DAX para multiplicar cada observación por el ponderador `FEX_C18`, garantizando que la varianza y el ingreso medio representen a los 23 millones de colombianos en edad productiva.  
> 2. **Lenguaje Ciudadano:** Cambiamos los KPIs corporativos por preguntas directas: *¿Cuánto se gana típicamente?* y *¿Qué tan predecible es mes a mes?*.  
> 3. El dashboard está disponible en Power BI Service institucional y empaquetado en el archivo `.pbix` de la entrega.»

---

### Minuto 8:00 a 10:00 | Síntesis, Límites Éticos y Mensaje Ciudadano
**Voces Alternadas: Santiago Sandoval & Sebastián Ramos**
> **Santiago (1 min):**  
> «Concluimos con cuatro acciones prácticas que todo trabajador independiente en Colombia puede aplicar hoy:  
> 1. **Cotizar con base en percentiles:** Fijar tarifas considerando el rango P50-P75 para cubrir seguridad social.  
> 2. **Ajustar el colchón al riesgo:** Quien trabaje en sectores volátiles como Arte o Minería debe reservar mínimo 6 meses de gastos; en sectores estables como Alimentos o Educación, 3 meses bastan.  
> 3. **Negociar con datos:** Exigir inclusión financiera demostrando que la estabilidad no es monopolio de la nómina.»  
> 
> **Sebastián (1 min):**  
> «Por último, declaramos nuestras **limitaciones éticas**: este estudio es descriptivo y asociativo; no afirma causalidad. Todos nuestros entregables son 100% reproducibles: incluimos un test suite en Python (`verify_all_metrics.py`) que comprueba automáticamente que cada número citado coincide sin error con la base oficial, y el Anexo de IA documenta de forma transparente cada herramienta y prompt empleado.  
> Muchísimas gracias. Quedamos atentos a sus preguntas y comentarios.»

---

## 3. BANCO DEFENSIVO DE PREGUNTAS DIFÍCILES (PROFESORAS ADRIANA Y PAOLA)

### P1: «¿Por qué decidieron no hacer el mapa a nivel municipal en R?»
> **Respuesta Técnica:**  
> «Hacer un mapa municipal con la GEIH habría sido un error metodológico grave. El DANE diseña la muestra de la GEIH para tener representatividad estadística exclusivamente a nivel Nacional, Regional (5 regiones), Departamental (32 departamentos + Bogotá D.C.) y para 23 Ciudades Capitales y Áreas Metropolitanas. Los 1.121 municipios no tienen tamaño de muestra suficiente; desagregar a ese nivel generaría estimaciones con errores de muestreo inaceptables y falacia ecológica. Por eso proyectamos estrictamente a nivel departamental bajo el sistema oficial EPSG:9377 (Magna-Sirgas Origen Nacional).»

### P2: «¿Cómo calcularon la varianza y el Coeficiente de Variación ponderado en DAX?»
> **Respuesta Técnica:**  
> «No utilizamos un simple `STDEV.P` sobre filas crudas. En DAX formulamos:  
> 1. `Ingreso_Medio_Ponderado = DIVIDE(SUMX(Tabla, INGLABO * FEX_C18), SUM(FEX_C18))`  
> 2. `Varianza_Ponderada = DIVIDE(SUMX(Tabla, FEX_C18 * (INGLABO - [Ingreso_Medio_Ponderado])^2), SUM(FEX_C18))`  
> 3. `CV_Ponderado = DIVIDE(SQRT([Varianza_Ponderada]), [Ingreso_Medio_Ponderado])`  
> Esto garantiza que cada persona en la muestra aporte el peso censal real que representa en la población colombiana.»

### P3: «¿Por qué en Modalidad B eligieron una arquitectura HTML modular en lugar de Streamlit directo?»
> **Respuesta Técnica:**  
> «La guía oficial establece la Modalidad B como una 'experiencia digital guiada, por ejemplo en Streamlit', dejando abierta la tecnología. Elegimos una arquitectura web nativa modular (HTML5 semántico, CSS auditado en accesibilidad y JavaScript ES6) porque ofrece tres ventajas cruciales de clase mundial:  
> 1. Permite un despliegue instantáneo sin servidor en plataformas de alto rendimiento como Vercel o GitHub Pages.  
> 2. Es 100% accesible (cumple WCAG 2.1 AA/AAA verificado matemáticamente y soporte para lectores de pantalla).  
> 3. Permite la integración nativa fluida de los widgets interactivos de Leaflet (R) y Plotly (Python) sin la sobrecarga ni los reinicios de estado típicos de Streamlit. Además, incluimos un lanzador local en Python (`run_local_server.py`) que permite ejecutarla con un solo clic en cualquier computador sin instalar nada adicional.»

### P4: «¿Cómo verificaron que las visualizaciones sean accesibles para daltónicos?»
> **Respuesta Técnica:**  
> «Diseñamos un sistema cromático semántico unificado compartido por Power BI, Seaborn, Plotly y R: Azul Marino (`#0B3C5D`) para categorías de referencia y Asalariados, y Dorado/Ámbar Cálido (`#D99B26`) para Independientes. Esta combinación se probó en simuladores Coblis y ColorBrewer, confirmando que es fisiológicamente distinguishable bajo Deuteranopía, Protanopía y Tritanopía. El contraste del azul sobre fondo blanco es de 10.6:1 (superando con holgura el umbral AAA de 7.0:1 de la W3C).»

