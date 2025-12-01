
<!DOCTYPE html>
<html>
<head>
    <title>Seleccionar ubicación en Google Maps</title>
    <style>
        #map { height: 500px; width: 100%; }
    </style>
    <!-- Carga la librería de Google Maps -->
    <script src="https://maps.googleapis.com/mapsU_API_KEY</script>
</head>
<body>
    <h3>Haz clic en el mapa para seleccionar una ubicación</h3>
    <div id="map"></div>

    <script>
        function initMap() {
            // Inicializa el mapa centrado en La Dorada
            var map = new google.maps.Map(document.getElementById('map'), {
                center: {lat: 5.45, lng: -74.67},
                zoom: 13
            });

            var marker;

            // Evento al hacer clic en el mapa
            map.addListener('click', function(event) {
                var lat = event.latLng.lat();
                var lng = event.latLng.lng();

                // Coloca un marcador en la ubicación seleccionada
                if (marker) {
                    marker.setMap(null);
                }
                marker = new google.maps.Marker({
                    position: event.latLng,
                    map: map
                });

                alert("Seleccionaste: " + lat + ", " + lng);

                // Envía las coordenadas a tu API Flask
                fetch('https://prueba-api-laz2.onrender.com/selection', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({selected_value: {lat: lat, lng: lng}})
                })
                .then(response => response.json())
                .then(data => console.log("Respuesta API:", data))
                .catch(error => console.error("Error:", error));
            });
        }

        // Inicializa el mapa cuando cargue la página
        window.onload = initMap;
    </script>
</body>
</html>
