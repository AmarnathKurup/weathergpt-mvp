"use client";

import { useEffect, useState } from "react";
import { MapContainer, Marker, Popup, TileLayer, useMapEvents } from "react-leaflet";
import L from "leaflet";
import { useLocation } from "@/lib/location-context";
import { api } from "@/lib/api";
import type { CommunityReport } from "@/lib/types";

// Fix default marker icons under bundlers (Leaflet's default asset paths break with webpack)
const markerIcon = new L.Icon({
  iconUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png",
  iconRetinaUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png",
  shadowUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png",
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41],
});

// Distinct markers for crowdsourced reports, built as inline SVG divIcons so
// they don't depend on an external image URL that may not exist/load.
const CATEGORY_EMOJI: Record<string, string> = {
  Flooding: "🌊",
  Waterlogging: "💧",
  "Power Outage": "⚡",
  "Road Blocked": "🚧",
  "Heavy Rain": "🌧️",
  "Landslide Risk": "⛰️",
  "Fallen Tree": "🌳",
  Other: "📍",
};

function reportIconFor(category: string) {
  const emoji = CATEGORY_EMOJI[category] ?? "📍";
  return L.divIcon({
    className: "",
    html: `<div style="font-size:22px;line-height:1;filter:drop-shadow(0 1px 2px rgba(0,0,0,0.4))">${emoji}</div>`,
    iconSize: [24, 24],
    iconAnchor: [12, 22],
    popupAnchor: [0, -22],
  });
}

function ClickHandler() {
  const { setLocationByCoords } = useLocation();
  useMapEvents({
    click(e) {
      setLocationByCoords(e.latlng.lat, e.latlng.lng);
    },
  });
  return null;
}

function RecenterOnChange({ lat, lon }: { lat: number; lon: number }) {
  const map = useMapEvents({});
  useEffect(() => {
    map.flyTo([lat, lon], map.getZoom(), { duration: 0.8 });
  }, [lat, lon, map]);
  return null;
}

export default function WeatherMap() {
  const { location } = useLocation();
  const [reports, setReports] = useState<CommunityReport[]>([]);

  const center: [number, number] = location ? [location.lat, location.lon] : [20.5937, 78.9629];

  useEffect(() => {
    if (!location) return;
    api
      .communityReports({ lat: location.lat, lon: location.lon, radius_km: 30 })
      .then(setReports)
      .catch(() => setReports([]));
  }, [location]);

  return (
    <div className="rounded-2xl overflow-hidden border border-slate-200 dark:border-slate-700 h-[500px] w-full">
      <MapContainer center={center} zoom={7} scrollWheelZoom style={{ height: "100%", width: "100%" }}>
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        {location && (
          <>
            <Marker position={[location.lat, location.lon]} icon={markerIcon}>
              <Popup>{location.name}</Popup>
            </Marker>
            <RecenterOnChange lat={location.lat} lon={location.lon} />
          </>
        )}
        {reports.map((r) => (
          <Marker key={r.id} position={[r.lat, r.lon]} icon={reportIconFor(r.category)}>
            <Popup>
              <strong>{r.category}</strong>
              {r.note && <div>{r.note}</div>}
            </Popup>
          </Marker>
        ))}
        <ClickHandler />
      </MapContainer>
    </div>
  );
}
