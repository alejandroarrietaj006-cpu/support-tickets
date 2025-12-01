import json
import os
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

SAVE_FILE = "ubicacion.json"


def guardar_ubicacion(data):
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f)


def leer_ubicacion():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            return json.load(f)
    return None


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

        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/ol@v7.3.0/ol.css">
        <script src="https://cdn.jsdelivr.net/npm/ol@v7.3.0/dist/ol.js"></script>
    </head>

    <body>
        <h3>Haz clic en el mapa para seleccionar una ubicación</h3>
        <div id="map"></div>

        <script>
            var googleLayer = new ol.layer.Tile({
                source: new ol.source.XYZ({
                    url: 'http://mt1.google.com/vt/lyrs=r&x={x}&y={y}&z={z}'
                })
            });

            var map = new ol.Map({
                target: 'map',
                layers: [googleLayer],
                view: new ol.View({
                    center: ol.proj.fromLonLat([-75.5812, 6.2442]),
                    zoom: 13
                })
            });

            var markerLayer = new ol.layer.Vector({
                source: new ol.source.Vector()
            });
            map.addLayer(markerLayer);

            map.on('click', function(evt) {
                var coord = ol.proj.toLonLat(evt.coordinate);
                var lon = coord[0];
                var lat = coord[1];

                console.log("Coordenadas:", lat, lon);

                markerLayer.getSource().clear();

                var feature = new ol.Feature({
                    geometry: new ol.geom.Point(evt.coordinate)
                });
                markerLayer.getSource().addFeature(feature);

                fetch("/selection", {
                    method: "POST",
                    headers: {"Content-Type": "application/json"},
                    body: JSON.stringify({lat: lat, lng: lon})
                })
                .then(r => r.json())
                .then(data => console.log("Guardado:", data));
            });
        </script>
    </body>
    </html>
    """

    return render_template_string(html)


@app.route("/selection", methods=["POST"])
def capture_selection():
    data = request.json
    guardar_ubicacion(data)
    print("Ubicación guardada:", data)
    return jsonify({"status": "ok", "saved": data})


@app.route("/ultima_ubicacion", methods=["GET"])
def ultima_ubicacion():
    data = leer_ubicacion()
    return jsonify({"ultima_ubicacion": data})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
