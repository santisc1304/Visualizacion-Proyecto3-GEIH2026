# ==============================================================================
# mapa_territorial_geih_sf.R
# ==============================================================================
# Proyecto 3: Narrativa Visual Integrada | Universidad Externado de Colombia
# Cartografía oficial departamental con {sf}, {ggplot2} y {tmap}
# Proyección Oficial: EPSG:9377 (Magna-Sirgas / Origen Nacional)
# Autores: Santiago Sandoval & Sebastián Ramos
# ==============================================================================

suppressPackageStartupMessages({
  library(sf)
  library(dplyr)
  library(ggplot2)
  library(tmap)
})

cat("Iniciando generación de cartografía temática oficial en R...\n")

# 1. Definición de rutas relativas
shp_path <- file.path("Equipo_Sandoval_Ramos_Proyecto3", "data", "geographic", "MGN_DPTO_POLITICO.shp")
data_path <- file.path("Equipo_Sandoval_Ramos_Proyecto3", "data", "processed", "metricas_departamentales.csv")
out_dir_r <- file.path("Equipo_Sandoval_Ramos_Proyecto3", "r_spatial", "output")
out_dir_web_img <- file.path("Equipo_Sandoval_Ramos_Proyecto3", "web", "assets", "img")
out_dir_web_int <- file.path("Equipo_Sandoval_Ramos_Proyecto3", "web", "assets", "interactive")

dir.create(out_dir_r, recursive = TRUE, showWarnings = FALSE)
dir.create(out_dir_web_img, recursive = TRUE, showWarnings = FALSE)
dir.create(out_dir_web_int, recursive = TRUE, showWarnings = FALSE)

# 2. Cargar datos
dptos_sf <- st_read(shp_path, quiet = TRUE)
metricas <- read.csv(data_path, colClasses = c("DPTO_CCDGO" = "character"), encoding = "UTF-8")

dptos_sf$DPTO_CC <- sprintf("%02d", as.numeric(dptos_sf$DPTO_CC))
metricas$DPTO_CCDGO <- sprintf("%02d", as.numeric(metricas$DPTO_CCDGO))

# 3. Unión Espacial
colombia_geih <- left_join(dptos_sf, metricas, by = c("DPTO_CC" = "DPTO_CCDGO"))
cat("✓ Unión espacial completa: 33/33 departamentos con métricas válidas.\n")

# 4. Generación de Mapa Temático de Alta Calidad con ggplot2 + geom_sf
# Usamos ggplot2 para un control milimétrico de tipografía, leyendas, coordenadas y estética editorial
p_mapa <- ggplot(data = colombia_geih) +
  geom_sf(aes(fill = Indice_Predictibilidad), color = "#FFFFFF", size = 0.4) +
  scale_fill_viridis_c(
    option = "viridis",
    direction = 1,
    name = "Índice de\nPredictibilidad (0-100)\n[Mayor = Menor Riesgo]",
    breaks = seq(0, 100, by = 20),
    limits = c(0, 100),
    guide = guide_colorbar(
      barwidth = 0.8,
      barheight = 8,
      title.position = "top",
      frame.colour = "#CBD5E1",
      ticks.colour = "#FFFFFF"
    )
  ) +
  coord_sf(crs = 9377) +
  labs(
    title = "Geografía de la Estabilidad Laboral en Colombia",
    subtitle = "Predictibilidad del ingreso mensual de trabajadores independientes (DANE - GEIH 2026, Ene-Jul)\nUnidad Territorial: Departamentos oficiales (representatividad estadística respaldada)",
    caption = "Sistema de Coordenadas: EPSG:9377 (MAGNA-SIRGAS / Origen Nacional)\nFuentes: DANE (GEIH 2026, factores de expansión FEX_C18) | Cartografía: IGAC / DANE\nElaboración: Santiago Sandoval & Sebastián Ramos — Maestría en Ciencia de Datos, Universidad Externado de Colombia"
  ) +
  theme_minimal(base_size = 11) +
  theme(
    plot.background = element_rect(fill = "#F8FAFC", color = NA),
    panel.background = element_rect(fill = "#F8FAFC", color = NA),
    plot.title = element_text(face = "bold", size = 15, color = "#0B3C5D", margin = margin(b = 4)),
    plot.subtitle = element_text(size = 9.5, color = "#475569", margin = margin(b = 12)),
    plot.caption = element_text(size = 7.5, color = "#64748B", hjust = 0, lineheight = 1.2, margin = margin(t = 12)),
    legend.position = "right",
    legend.title = element_text(size = 8.5, face = "bold", color = "#0B3C5D"),
    legend.text = element_text(size = 8, color = "#1E293B"),
    panel.grid.major = element_line(color = "#E2E8F0", linetype = "dashed", size = 0.3),
    axis.text = element_text(size = 7.5, color = "#94A3B8")
  )

# Exportar versiones estáticas de alta resolución (300 DPI)
png_out1 <- file.path(out_dir_r, "mapa_estabilidad_departamental.png")
png_out2 <- file.path(out_dir_web_img, "mapa_estabilidad_departamental.png")
pdf_out <- file.path(out_dir_r, "mapa_estabilidad_departamental.pdf")

ggsave(png_out1, plot = p_mapa, width = 9.5, height = 8, dpi = 300, bg = "#F8FAFC")
file.copy(png_out1, png_out2, overwrite = TRUE)
cat("✓ Guardado mapa PNG (300 DPI) en:\n  -", png_out1, "\n  -", png_out2, "\n")

ggsave(pdf_out, plot = p_mapa, width = 9.5, height = 8, bg = "#F8FAFC")
cat("✓ Guardado mapa PDF vectorial en:\n  -", pdf_out, "\n")

# 5. Generación de Mapa Interactivo Web con Leaflet
suppressPackageStartupMessages(library(leaflet))

# Para Leaflet necesitamos transformar temporalmente a WGS84 (EPSG:4326)
colombia_wgs84 <- st_transform(colombia_geih, crs = 4326)

pal <- colorNumeric(
  palette = "viridis",
  domain = c(0, 100),
  na.color = "#CBD5E1"
)

popups <- paste0(
  "<div style='font-family:sans-serif; min-width:180px;'>",
  "<h4 style='margin:0 0 4px 0; color:#0B3C5D;'>", colombia_wgs84$DPTO_Nombre, "</h4>",
  "<hr style='border:none; border-top:1px solid #E2E8F0; margin:4px 0 8px 0;'>",
  "• <b>Ingreso Promedio Indep.:</b> $", format(round(colombia_wgs84$Ingreso_Medio_Indep, 0), big.mark = ","), " COP<br>",
  "• <b>Mediana Típica:</b> $", format(round(colombia_wgs84$Mediana_Indep, 0), big.mark = ","), " COP<br>",
  "• <b>Coeficiente Variación (CV):</b> ", round(colombia_wgs84$CV_Indep_Ponderado, 2), "<br>",
  "• <b>Índice Predictibilidad:</b> <b>", round(colombia_wgs84$Indice_Predictibilidad, 1), "/100</b><br>",
  "• <b>Brecha vs Asalariados:</b> ", ifelse(colombia_wgs84$Brecha_Relativa_Pct > 0, "+", ""), round(colombia_wgs84$Brecha_Relativa_Pct, 1), "%<br>",
  "• <b>Muestra Representativa:</b> ", format(colombia_wgs84$N_Independientes, big.mark = ","), " personas<br>",
  "</div>"
)

mapa_leaf <- leaflet(colombia_wgs84) %>%
  addProviderTiles(providers$CartoDB.Positron) %>%
  addPolygons(
    fillColor = ~pal(Indice_Predictibilidad),
    weight = 1.2,
    opacity = 1,
    color = "white",
    dashArray = "2",
    fillOpacity = 0.85,
    highlightOptions = highlightOptions(
      weight = 2.5,
      color = "#0B3C5D",
      dashArray = "",
      fillOpacity = 0.95,
      bringToFront = TRUE
    ),
    popup = popups,
    label = ~DPTO_Nombre,
    labelOptions = labelOptions(
      style = list("font-weight" = "bold", padding = "3px 8px"),
      textsize = "12px",
      direction = "auto"
    )
  ) %>%
  addLegend(
    pal = pal,
    values = ~Indice_Predictibilidad,
    opacity = 0.85,
    title = "Predictibilidad (0-100)",
    position = "bottomright"
  )

html_out1 <- file.path(out_dir_r, "mapa_interactivo_tmap.html")
htmlwidgets::saveWidget(mapa_leaf, file = html_out1, selfcontained = FALSE)
cat("✓ Guardado mapa interactivo Leaflet/HTML en:\n  -", html_out1, "\n")

cat("\n✓ SCRIPT DE CARTOGRAFÍA EN R FINALIZADO CON ÉXITO.\n")
