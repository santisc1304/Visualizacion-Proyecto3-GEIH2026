# RELACIÓN DE FUENTES OFICIALES, DEFINICIONES DE VARIABLES Y LIMITACIONES METODOLÓGICAS
## Proyecto 3: Narrativa Visual Integrada | Universidad Externado de Colombia
**Autores:** Santiago Sandoval & Sebastián Ramos  
**Docentes:** Adriana Pineda – Paola Moreno  
**Fecha:** Noviembre de 2026  

---

## 1. FUENTES OFICIALES DE INFORMACIÓN

### 1.1. Fuente Principal (Estadística Laboral y Socioeconómica)
- **Entidad Productora:** Departamento Administrativo Nacional de Estadística (DANE) — República de Colombia.
- **Operación Estadística:** Gran Encuesta Integrada de Hogares (GEIH) — Marco Muestral Censo Nacional de Población y Vivienda (CNPV 2018).
- **Período Analizado:** Serie continua de siete (7) meses: **Enero, Febrero, Marzo, Abril, Mayo, Junio y Julio de 2026**.
- **Catálogo Oficial de Microdatos:** [Archivo Nacional de Datos (ANDA) - Catálogo 900](https://microdatos.dane.gov.co/index.php/catalog/900).
- **Módulos Integrados:**
  1. `Ocupados.CSV`: Información sobre posición ocupacional, rama de actividad económica (CIIU Rev. 4 A.C.), ingresos laborales monetarios y factores de expansión.
  2. `Características generales, seguridad social en salud y educación.CSV`: Variables demográficas básicas (sexo, edad cumplida, parentesco y nivel educativo).

### 1.2. Fuente Complementaria (Cartografía y Marco Geoestadístico)
- **Entidad Productora:** Instituto Geográfico Agustín Codazzi (IGAC) y DANE (Marco Geoestadístico Nacional - MGN).
- **Capa Utilizada:** División Político-Administrativa de Colombia a nivel Departamental (`MGN_DPTO_POLITICO.shp`, 32 departamentos y el Distrito Capital de Bogotá).
- **Sistema de Referencia de Coordenadas (CRS):** **EPSG:9377 (MAGNA-SIRGAS 2018 / Origen-Nacional)**, proyección oficial de la República de Colombia establecida mediante Resolución 471 de 2020 del IGAC.

---

## 2. DICCIONARIO Y DEFINICIONES DE VARIABLES CLAVE

| Variable en el Modelo | Código Original GEIH | Tipo | Definición Técnica y Operacionalización |
|---|---|---|---|
| **Llave Primaria de Persona** | `DIRECTORIO` + `SECUENCIA_P` + `ORDEN` + `HOGAR` | Identificador | Llave compuesta única que identifica de forma inequívoca a cada individuo encuestado dentro de su vivienda y hogar, permitiendo la unión exacta (`inner join`) entre los módulos de *Ocupados* y *Características Generales*. |
| **Ingreso Laboral Mensual** | `INGLABO` / `P6500` | Cuantitativa Continua ($ COP) | Remuneración monetaria mensual total derivada de la ocupación principal antes de descuentos de ley (para asalariados) o ganancia neta mensual de la actividad o negocio (para trabajadores por cuenta propia). Expresada en pesos colombianos corrientes de 2026. |
| **Factor de Expansión Censal** | `FEX_C18` | Ponderador Muestral | Peso estadístico asignado por el DANE a cada registro muestral. Indica a cuántas personas de la población civil no institucional residente en Colombia representa cada encuestado, calibrado con las proyecciones del CNPV 2018. |
| **Modalidad Laboral (`TipoTrabajador`)** | `P6430` | Categórica Nominal | Clasificación derivada de la posición ocupacional:<br>• **Cuenta propia (Independiente):** Código `4` (*Trabajador por cuenta propia*).<br>• **Asalariado (Dependiente):** Códigos `1` (*Obrero o empleado de empresa particular*) y `2` (*Obrero o empleado del gobierno*). |
| **Sector Económico (`SectorEconomico`)** | `RAMA2D_R4` | Categórica Nominal | Agrupación de los códigos de 2 dígitos de la Clasificación Industrial Internacional Uniforme (CIIU Rev. 4 A.C.) en 11 grandes ramas de actividad económica (Comercio, Educación, Construcción, Agropecuario, Alojamiento y comida, Industria manufacturera, Transporte, Información y comunicaciones, Servicios profesionales, Arte y entretenimiento, y Minería). |
| **Cohorte de Edad (`GrupoEdad`)** | `P6040` | Categórica Ordinal | Edad en años cumplidos agrupada en cuatro etapas del ciclo de vida laboral activo:<br>1. `18 a 24 años` (Inserción laboral juvenil)<br>2. `25 a 34 años` (Consolidación temprana / *Corredor Dorado*)<br>3. `35 a 54 años` (Madurez laboral)<br>4. `55 años o más` (Etapa sénior y transición pensional). |
| **Sexo** | `P3271` | Categórica Nominal | Sexo biológico registrado en la encuesta (`1` = Hombre, `2` = Mujer). |
| **Entidad Territorial (`DPTO`)** | `DPTO` | Geográfica (DIVIPOLA) | Código oficial de 2 dígitos de la División Político-Administrativa del DANE correspondiente a los 32 departamentos y Bogotá D.C. (`11`). |
| **Coeficiente de Variación Ponderado (`CV_Ponderado`)** | Indicador Calculado | Métrica Adimensional | Razón entre la desviación estándar poblacional ponderada y la media aritmética ponderada del ingreso ($\text{CV} = \sigma_w / \mu_w$). Mide la dispersión y volatilidad relativa del ingreso con independencia de la escala monetaria. |
| **Índice de Predictibilidad Territorial** | Indicador Calculado | Escala (0 a 100) | Transformación lineal normalizada del Coeficiente de Variación departamental ($\text{Índice} = \text{clip}\left(\frac{1.6 - \text{CV}}{1.6 - 0.4} \times 100, 0, 100\right)$), diseñada para facilitar la lectura ciudadana (donde valores cercanos a 100 indican máxima estabilidad de ingresos). |

---

## 3. TRATAMIENTO DE DATOS Y REGLAS DE DEPURACIÓN

1. **Población Objetivo:** Personas ocupadas mayores de edad ($\text{P6040} \ge 18$ años) con ingresos laborales positivos ($\text{INGLABO} > 0$), consolidando un universo analítico de **183.911 observaciones** (85.608 trabajadores independientes por cuenta propia y 98.303 asalariados), además de la submuestra de referencia del Proyecto 1 (**105.542 registros**).
2. **Manejo de Valores Faltantes y Nulos:** No se aplicaron métodos de imputación sintética sobre la variable de ingresos para no distorsionar artificialmente la varianza empírica. Los registros con ingresos no reportados o iguales a cero (como trabajadores familiares sin remuneración) fueron excluidos explícitamente del cálculo de dispersión salarial.
3. **Control de Valores Extremos en Visualización Estática:** En los gráficos de violín y densidad continua (Seaborn), el eje visual se acotó al percentil 99 ($P_{99}$) para evitar el aplastamiento gráfico ocasionado por valores atípicos extremos, conservando la totalidad de la muestra en el cálculo de medianas y cuartiles.

---

## 4. LIMITACIONES METODOLÓGICAS Y USO ÉTICO DE LA INFORMACIÓN

1. **Restricción Estricta de Representatividad Territorial (Prohibición de Extrapolación Municipal):**
   El diseño muestral probabilístico, estratificado y de conglomerados de la GEIH garantiza representatividad estadística exclusivamente a nivel **Nacional**, **Cabecera / Centros Poblados y Rural Disperso**, **Regional**, **Departamental** y para las **23 principales Ciudades y Áreas Metropolitanas**.  
   *En cumplimiento de la ética estadística, este proyecto no presenta ni respalda estimaciones a nivel municipal*, previniendo errores de muestreo severos y falacias ecológicas.
2. **Alcance Descriptivo y Ausencia de Inferencia Causal:**
   La GEIH es una encuesta transversal repetida (*repeated cross-sectional survey*), no un panel longitudinal que siga a los mismos individuos ni un experimento controlado aleatorizado. Por consiguiente, todas las comparaciones entre sectores, edades y territorios describen **asociaciones empíricas y patrones distributivos observados**, y de ningún modo deben interpretarse como relaciones de causa y efecto ni como evaluaciones de impacto de políticas públicas.
3. **Variabilidad Intra-Individual vs. Inter-Individual:**
   El Coeficiente de Variación calculado mide la heterogeneidad de ingresos *entre trabajadores de un mismo perfil* a lo largo de los 7 meses evaluados. Aunque constituye un excelente *proxy* de la incertidumbre estructural de cada oficio, las decisiones financieras individuales deben considerar también la antigüedad y la formalización contable de cada persona.

