"""
run_local_server.py
===================
Lanzador de servidor web local para previsualizar la Experiencia Digital Guiada (Modalidad B).
Inicia un servidor HTTP ligero en Python y abre automáticamente el navegador.
"""

import http.server
import socketserver
import webbrowser
import os
import sys

PORT = 8080
WEB_DIR = os.path.join(os.path.dirname(__file__), "web")

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=WEB_DIR, **kwargs)

    def end_headers(self):
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
        self.send_header("Pragma", "no-cache")
        super().end_headers()

def main():
    print("=" * 70)
    print("INICIANDO SERVIDOR WEB LOCAL (MODALIDAD B - PROYECTO 3)")
    print("=" * 70)
    print(f"Sirviendo directorio: {WEB_DIR}")
    print(f"URL de visualización: http://localhost:{PORT}")
    print("Presiona Ctrl + C para detener el servidor.\n")
    
    # Intentar abrir el navegador
    try:
        webbrowser.open(f"http://localhost:{PORT}")
    except Exception as e:
        print(f"Aviso: Abre manualmente en tu navegador: http://localhost:{PORT}")
        
    with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n✓ Servidor detenido por el usuario.")
            sys.exit(0)

if __name__ == "__main__":
    main()

