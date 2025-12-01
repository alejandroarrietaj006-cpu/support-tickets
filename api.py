from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

@app.route("/")
def mapa():
    html = """
    <html>
    <head>
        <title>Seleccionar ubicación</title>
        <style>
            #map {
                height: 500px;
                width: 100%;
            }
        </style>

        <!-- OpenLayers -->
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/ol@v7.3.0/ol.css">
        <script src="https://cdn.jsdelivr.net/npm/ol@v7.3.0/dist/ol.js"></script>

    </head>

    <body>
        <h3>Haz clic en el mapa para seleccionar una ubicación</h3>
        <div id="map"></div>

        <script>
            // Capa Google Maps sin API key (modo "XYZ tiles")
            var googleLayer = new ol.layer.Tile({
                source: new ol.source.XYZ({
                    url: 'http://mt1.google.com/vt/lyrs=r&x={x}&y={y}&z={z}',
                })
            });

            // Crear mapa
            var map = new ol.Map({
                target: 'map',
                layers: [googleLayer],
                view: new ol.View({
                    center: ol.proj.fromLonLat([-75.5812, 6.2442]), // Medellín
                    zoom: 13
                })
            });

            var markerLayer = new ol.layer.Vector({
                source: new ol.source.Vector()
            });
            map.addLayer(markerLayer);

            // Evento clic
            map.on('click', function(evt) {
                var coord = ol.proj.toLonLat(evt.coordinate);
                var lon = coord[0];
                var lat = coord[1];

                console.log("Coordenadas:", lat, lon);

                // Borrar marcador anterior
                markerLayer.getSource().clear();

                // Crear marcador
                var feature = new ol.Feature({
                    geometry: new ol.geom.Point(evt.coordinate)
                });

                markerLayer.getSource().addFeature(feature);

                // Enviar coordenadas al backend
                fetch("/selection", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ selected_value: { lat: lat, lng: lon } })
                })
                .then(r => r.json())
                .then(data => console.log("API:", data));
            });
        </script>

    </body>
    </html>
    """

    return render_template_string(html)



@app.route("/selection", methods=["POST"])
def capture_selection():
    data = request.json
    selected = data.get("selected_value")
    print("Coordenadas:", selected)
    return jsonify({"status": "ok", "selected_value": selected})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
