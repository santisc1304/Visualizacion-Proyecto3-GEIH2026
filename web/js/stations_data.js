/**
 * Configuración del Mundo 2D del Mapa del Tesoro (3200 x 1800 px):
 * - Enlace configurable de Power BI Service publicado
 * - 6 Estaciones Principales con X Rojas (Estructura: El Viaje del Héroe) -> Se abren con ESPACIO
 * - 5 Obstáculos Cartográficos (Altercados y soluciones) -> Se revelan al pasar el cursor encima
 */

// Enlace público oficial publicado en Power BI Service para la Estación X1:
window.POWER_BI_EMBED_URL = "https://app.powerbi.com/view?r=eyJrIjoiZjc3OGE4N2UtMTI3Ni00MGJlLWI1NTItZGU4NWRiZGM5NzRlIiwidCI6IjNiOTQ0ZDlhLTEwNTEtNDY4NS1iMDlkLTlhOTVlZTJkYmQ5OSIsImMiOjR9";

window.TREASURE_WORLD_SIZE = {
  width: 3200,
  height: 1800
};

window.TREASURE_MAP_NODES = [
  {
    id: "x1",
    order: 1,
    type: "station",
    code: "X1",
    x: 310,
    y: 1410,
    shortLabel: "1. El Mundo Ordinario",
    subLabel: "Dashboard Power BI",
    heroBadge: "ETAPA 1 DEL VIAJE DEL HÉROE • EL MUNDO ORDINARIO Y EL LLAMADO",
    modalTitle: "Estación X1: El Mito de la Inestabilidad frente al Monitor Power BI",
    panelId: "panel-x1"
  },
  {
    id: "o1",
    order: 2,
    type: "obstacle",
    code: "🌀",
    icon: "🌀",
    x: 560,
    y: 1050,
    shortLabel: "Remolino del Promedio",
    subLabel: "Pasa el cursor encima",
    problemShort: "Ingresos extremos (>$35M) inflaban la media aritmética hasta $2,47M, ocultando el ingreso real típico.",
    solutionShort: "Usamos Mediana Ponderada (P50 = $1,20M), rango P25–P75 y escala logarítmica para no distorsionar la realidad."
  },
  {
    id: "x2",
    order: 3,
    type: "station",
    code: "X2",
    x: 780,
    y: 590,
    shortLabel: "2. El Cruce del Umbral",
    subLabel: "Python: Distribución",
    heroBadge: "ETAPA 2 DEL VIAJE DEL HÉROE • EL CRUCE DEL UMBRAL ESTADÍSTICO",
    modalTitle: "Estación X2: Desenmascarando el Promedio (Seaborn Raincloud)",
    panelId: "panel-x2"
  },
  {
    id: "o2",
    order: 4,
    type: "obstacle",
    code: "🐙",
    icon: "🐙",
    x: 1090,
    y: 930,
    shortLabel: "Kraken de Ponderación",
    subLabel: "Pasa el cursor encima",
    problemShort: "Calcular cifras sin expandir por FEX_C18 daba el mismo peso a un encuestado que representa a 10 personas que a uno de 1.500.",
    solutionShort: "Unificamos fórmulas ponderadas por FEX_C18 en Python y DAX (SUMX), validadas con pruebas automatizadas."
  },
  {
    id: "x3",
    order: 5,
    type: "station",
    code: "X3",
    x: 1370,
    y: 1290,
    shortLabel: "3. El Corredor Dorado",
    subLabel: "Python: Ciclo de Vida",
    heroBadge: "ETAPA 3 DEL VIAJE DEL HÉROE • LAS PRUEBAS DEL TIEMPO Y LA EXPERIENCIA",
    modalTitle: "Estación X3: El Ciclo de Vida Laboral y el Corredor Dorado (35–44 años)",
    panelId: "panel-x3"
  },
  {
    id: "o3",
    order: 6,
    type: "obstacle",
    code: "🌲",
    icon: "🌲",
    x: 1680,
    y: 860,
    shortLabel: "Bosque de la Falacia",
    subLabel: "Pasa el cursor encima",
    problemShort: "El shapefile tenía 1.121 municipios, pero la GEIH del DANE solo es estadísticamente representativa a nivel departamental.",
    solutionShort: "Disolvimos topológicamente los municipios en R (sf::st_union) a los 33 dominios oficiales en proyección EPSG:9377."
  },
  {
    id: "x4",
    order: 7,
    type: "station",
    code: "X4",
    x: 1960,
    y: 440,
    shortLabel: "4. Geografía del Riesgo",
    subLabel: "Mapas en R (sf/Leaflet)",
    heroBadge: "ETAPA 4 DEL VIAJE DEL HÉROE • LA EXPLORACIÓN DEL TERRITORIO",
    modalTitle: "Estación X4: ¿Dónde es Más Predecible Trabajar por Cuenta Propia? (R Espacial)",
    panelId: "panel-x4"
  },
  {
    id: "o4",
    order: 8,
    type: "obstacle",
    code: "🐉",
    icon: "🐉",
    x: 2260,
    y: 860,
    shortLabel: "Serpiente del Shapefile",
    subLabel: "Pasa el cursor encima",
    problemShort: "El estándar ESRI (.shp) truncó DPTO_CCDGO a DPTO_CC y los códigos como '05' perdían el cero inicial al abrirse en CSV.",
    solutionShort: "Formateamos códigos DANE a 2 dígitos con sprintf('%02d') en R y zfill(2) en Python, logrando un cruce perfecto de 33/33."
  },
  {
    id: "x5",
    order: 9,
    type: "station",
    code: "X5",
    x: 2490,
    y: 1320,
    shortLabel: "5. Oráculo Ciudadano",
    subLabel: "Simulador + Plotly",
    heroBadge: "ETAPA 5 DEL VIAJE DEL HÉROE • EL DON DEL ORÁCULO INTERACTIVO",
    modalTitle: "Estación X5: Consulta tu Propio Mapa de Riesgo (Simulador + Plotly)",
    panelId: "panel-x5"
  },
  {
    id: "o5",
    order: 10,
    type: "obstacle",
    code: "⛈️",
    icon: "⛈️",
    x: 2750,
    y: 950,
    shortLabel: "Tormenta de 7 Meses",
    subLabel: "Pasa el cursor encima",
    problemShort: "Consolidar 7 meses de GEIH sumaba 206.712 registros y cientos de códigos CIIU imposibles de cargar fluidamente en el navegador.",
    solutionShort: "Agrupamos en 11 macro-sectores ciudadanos y pre-calculamos 44 matrices ligeras en JSON para respuesta instantánea."
  },
  {
    id: "x6",
    order: 11,
    type: "station",
    code: "X6",
    x: 2920,
    y: 540,
    shortLabel: "6. El Elixir Final",
    subLabel: "Síntesis y Cofre",
    heroBadge: "ETAPA 6 DEL VIAJE DEL HÉROE • EL REGRESO CON EL ELIXIR",
    modalTitle: "Estación X6: El Regreso con el Elixir — Decisiones, Ética y Cofre del Tesoro",
    panelId: "panel-x6"
  }
];
