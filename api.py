from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

@app.route("/")
def mapa():
    html = """
    <html>
    <head>
        <title>Seleccionar ubicación</title>

        <style>
            body, html {
                margin: 0; padding: 0; height: 100%;
            }

            #wrapper {
                position: relative;
                height: 500px;
            }

            #googlemap {
                width: 100%;
                height: 100%;
                filter: brightness(100%);
            }

            /* Capa Leaflet invisible igual al tamaño del mapa */
            #leaflet-overlay {
                position: absolute;
                top: 0; left: 0;
                width: 100%;
                height: 100%;
                pointer-events: auto;
            }
        </style>

        <link rel="stylesheet" href="https://unpkg.com/leaflet/dist/leaflet.css">
        <script src="https://unpkg.com/leaflet/dist/leaflet.js"></script>
    </head>

    <body>
        <h3>Haz clic sobre Google Maps para obtener la ubicación</h3>

        <div id="wrapper">
            <!-- Google Maps embed sin API key -->
            <iframe id="googlemap"
                src="https://maps.google.com/maps?q=Medellin&z=13&output=embed">
            </iframe>

            <!-- Leaflet overlay -->
            <div id="leaflet-overlay"></div>
        </div>

        <script>
            // Crear mapa Leaflet invisible encima
            var map = L.map('leaflet-overlay', {
                zoomControl: false,
                attributionControl: false
            }).setView([6.2442, -75.5812], 13);

            // Capa en blanco (solo para poder usar Leaflet)
            L.tileLayer('', {}).addTo(map);

            var marker;

            map.on("click", function(e) {
                var lat = e.latlng.lat;
                var lng = e.latlng.lng;

                console.log("Coordenadas:", lat, lng);

                if (marker) map.removeLayer(marker);
                marker = L.marker([lat, lng]).addTo(map);

                fetch('/selection', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        selected_value: { lat: lat, lng: lng }
                    })
                })
                .then(r => r.json())
                .then(data => console.log("API:", data));
            });
        </script>

    </body>
    </html>
    """

    return render_template_string(html)

@app.route('/selection', methods=['POST'])
def capture_selection():
    data = request.json
    selected_value = data.get("selected_value")
    print("Coordenadas:", selected_value)
    return jsonify({"status": "ok", "selected_value": selected_value})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

