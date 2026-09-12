import reflex as rx
from weathergpt_app.state.app_state import AppState

def leaflet_map(height: str = "450px") -> rx.Component:
    html_map = """
    <!DOCTYPE html>
    <html>
    <head>
        <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
        <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
        <style>
            #map { width: 100%; height: 100%; min-height: 380px; border-radius: 16px; }
            .leaflet-container { background: #0F172A; }
            .info-box { background: rgba(15, 23, 42, 0.85); color: #fff; padding: 8px 12px; border-radius: 8px; font-family: sans-serif; font-size: 12px; }
        </style>
    </head>
    <body style="margin:0; padding:0; background:#0F172A;">
        <div id="map"></div>
        <script>
            var map = L.map('map').setView([22.5726, 88.3639], 6);
            L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
                attribution: '&copy; OpenStreetMap &copy; CARTO & IMD India',
                maxZoom: 18
            }).addTo(map);

            // Active Warning Zones Markers (IMD Categories)
            var stations = [
                { lat: 22.5726, lon: 88.3639, name: "Kolkata (700001)", temp: "31.5°C", status: "Orange Alert - Heavy Rain", color: "#F97316" },
                { lat: 28.6139, lon: 77.2090, name: "New Delhi (110001)", temp: "35.2°C", status: "Yellow Watch - Heat/Haze", color: "#EAB308" },
                { lat: 19.0760, lon: 72.8777, name: "Mumbai (400001)", temp: "29.8°C", status: "Red Warning - Tidal Surge", color: "#EF4444" },
                { lat: 13.0827, lon: 80.2707, name: "Chennai (600001)", temp: "33.1°C", status: "Green Normal", color: "#10B981" },
                { lat: 12.9716, lon: 77.5946, name: "Bengaluru (560001)", temp: "26.4°C", status: "Green Normal", color: "#10B981" },
                { lat: 20.2961, lon: 85.8245, name: "Bhubaneswar (751001)", temp: "30.0°C", status: "Orange Alert - Cyclone Watch", color: "#F97316" }
            ];

            stations.forEach(function(s) {
                var circle = L.circleMarker([s.lat, s.lon], {
                    color: s.color,
                    fillColor: s.color,
                    fillOpacity: 0.6,
                    radius: 12
                }).addTo(map);
                
                circle.bindPopup(
                    "<b>" + s.name + "</b><br/>" +
                    "Temp: " + s.temp + "<br/>" +
                    "IMD Status: <span style='color:" + s.color + "'>" + s.status + "</span>"
                );
            });
        </script>
    </body>
    </html>
    """
    return rx.box(
        rx.html(html_map),
        width="100%",
        height=height,
        border_radius="16px",
        overflow="hidden",
        border="1px solid rgba(255, 255, 255, 0.12)",
        box_shadow="0 8px 32px rgba(0, 0, 0, 0.5)",
    )
