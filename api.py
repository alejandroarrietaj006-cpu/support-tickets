
from flask import Flask, request, jsonify

app = Flask(__name__)

# Endpoint para devolver la URL del mapa
@app.route('/map-url', methods=['GET'])
def get_map_url():
    return jsonify({"map_url": "https://tu-mapa.com"})  # Aquí luego pondremos tu HTML con Leaflet

# Endpoint para recibir la selección del usuario
@app.route('/selection', methods=['POST'])
def capture_selection():
    data = request.json
    selected_value = data.get("selected_value")
    return jsonify({"status": "ok", "selected_value": selected_value})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

