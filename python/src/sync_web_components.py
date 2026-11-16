"""
Sincronizador de Componentes Modulares Web (Modalidad B — Vercel Ready)
Ensambla los componentes modulares de `web/components/` dentro de `web/index.html`
para garantizar funcionamiento tanto en servidor HTTP/Vercel como en apertura local directa.
"""
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
WEB_DIR = BASE_DIR / "web"

def main():
    c1 = (WEB_DIR / "components" / "screen_portada.html").read_text(encoding="utf-8")
    c2 = (WEB_DIR / "components" / "screen_contexto.html").read_text(encoding="utf-8")
    c3 = (WEB_DIR / "components" / "screen_mapa_juego.html").read_text(encoding="utf-8")
    c4 = (WEB_DIR / "components" / "modal_estaciones.html").read_text(encoding="utf-8")

    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>El Mito de la Inestabilidad Independiente — Expedición Interactiva (GEIH 2026)</title>
  <meta name="description" content="Experiencia Digital Jugable (El Viaje del Héroe) sobre la estabilidad del trabajo independiente en Colombia (GEIH DANE 2026). Por Santiago Sandoval y Sebastián Ramos." />
  <link rel="stylesheet" href="css/typography.css?v=20261116" />
  <link rel="stylesheet" href="css/accessibility.css?v=20261116" />
  <link rel="stylesheet" href="css/treasure_game.css?v=20261116" />
</head>
<body>
  <!-- Componente Modular 1: Pantalla de Portada -->
  <div id="slot-portada" data-component="components/screen_portada.html">
{c1}
  </div>

  <!-- Componente Modular 2: Ventana Introductoria de Contexto y Briefing -->
  <div id="slot-contexto" data-component="components/screen_contexto.html">
{c2}
  </div>

  <!-- Componente Modular 3: El Mapa del Tesoro Jugable con la Avioneta -->
  <div id="slot-mapa" data-component="components/screen_mapa_juego.html">
{c3}
  </div>

  <!-- Componente Modular 4: Modales de las 6 Estaciones (X Rojas) y 5 Obstáculos -->
  <div id="slot-modales" data-component="components/modal_estaciones.html">
{c4}
  </div>

  <!-- Módulos JavaScript Desacoplados -->
  <script src="js/data_store.js?v=20261116"></script>
  <script src="js/stations_data.js?v=20261116"></script>
  <script src="js/simulator.js?v=20261116"></script>
  <script src="js/game_engine.js?v=20261116"></script>
  <script src="js/main.js?v=20261116"></script>
</body>
</html>
"""
    (WEB_DIR / "index.html").write_text(html, encoding="utf-8")
    print(f"web/index.html sincronizado con éxito ({len(html.splitlines())} líneas).")

if __name__ == "__main__":
    main()

