import React, { useState } from 'react';
import { MapContainer, TileLayer, Marker, Popup, CircleMarker, useMap } from 'react-leaflet';
import L from 'leaflet';
import { useApp } from '../../context/AppContext';
import { Layers, MapPin, Navigation, Eye, Droplets, Thermometer, Wind } from 'lucide-react';

// Fix Leaflet marker icon URL issue in React bundlers
delete (L.Icon.Default.prototype as any)._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
  iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png'
});

const MapRecenter: React.FC<{ lat: number; lon: number }> = ({ lat, lon }) => {
  const map = useMap();
  React.useEffect(() => {
    map.setView([lat, lon], map.getZoom());
  }, [lat, lon, map]);
  return null;
};

export const GISMap: React.FC = () => {
  const { location, weather, useDeviceLocation, settings, t } = useApp();

  const [activeLayer, setActiveLayer] = useState<'temp' | 'rain' | 'wind'>('rain');
  const [mapTileStyle, setMapTileStyle] = useState<'dark' | 'streets' | 'satellite'>(
    settings.theme === 'dark' ? 'dark' : 'streets'
  );

  const lat = location.latitude || 22.5726;
  const lon = location.longitude || 88.3639;

  // Major Indian Automated Weather Stations (AWS)
  const weatherStations = [
    { name: 'Kolkata (Alipore AWS)', lat: 22.5326, lon: 88.3267, temp: 31.5, rainProb: 78, status: 'Orange Warning' },
    { name: 'Delhi (Safdarjung AWS)', lat: 28.5849, lon: 77.2075, temp: 38.2, rainProb: 10, status: 'Heatwave Watch' },
    { name: 'Mumbai (Santacruz AWS)', lat: 19.0883, lon: 72.8617, temp: 30.4, rainProb: 85, status: 'Heavy Rain Warning' },
    { name: 'Bengaluru (HAL AWS)', lat: 12.9567, lon: 77.6625, temp: 26.2, rainProb: 20, status: 'Normal' },
    { name: 'Chennai (Meenambakkam AWS)', lat: 12.9900, lon: 80.1694, temp: 35.1, rainProb: 15, status: 'Normal' },
    { name: 'Guwahati (Borjhar AWS)', lat: 26.1061, lon: 91.5859, temp: 29.8, rainProb: 60, status: 'Yellow Warning' },
    { name: 'Ahmedabad (IMD AWS)', lat: 23.0734, lon: 72.6266, temp: 39.5, rainProb: 5, status: 'Heatwave Alert' },
  ];

  const tileUrls = {
    dark: 'https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png',
    streets: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
    satellite: 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}'
  };

  return (
    <div className="glass-panel rounded-3xl p-4 md:p-6 border border-slate-200 dark:border-slate-800 space-y-4 flex flex-col h-[calc(100vh-140px)] min-h-[550px] transition-colors duration-200">
      {/* Top Map Controls Header */}
      <div className="flex flex-wrap items-center justify-between gap-3 border-b border-slate-200 dark:border-slate-800 pb-3 shrink-0">
        <div className="flex items-center space-x-3">
          <div className="p-2.5 rounded-2xl bg-saffron-500/10 text-saffron-600 dark:text-saffron-500 border border-saffron-500/20">
            <Layers className="w-5 h-5" />
          </div>
          <div>
            <h2 className="font-bold text-base md:text-lg text-slate-900 dark:text-white">India GIS Weather Map</h2>
            <p className="text-xs text-slate-500 dark:text-slate-400">Live Doppler Radar & IMD Station Synoptic Grid</p>
          </div>
        </div>

        {/* Layer Controls & Tile Switchers */}
        <div className="flex flex-wrap items-center gap-2">
          <div className="flex items-center bg-slate-100 dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl p-1 text-xs">
            <button
              onClick={() => setActiveLayer('rain')}
              className={`px-3 py-1 rounded-lg font-semibold transition-colors ${
                activeLayer === 'rain' ? 'bg-sky-500 text-white' : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-200'
              }`}
            >
              Rainfall Overlay
            </button>
            <button
              onClick={() => setActiveLayer('temp')}
              className={`px-3 py-1 rounded-lg font-semibold transition-colors ${
                activeLayer === 'temp' ? 'bg-saffron-500 text-white' : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-200'
              }`}
            >
              Temperature
            </button>
            <button
              onClick={() => setActiveLayer('wind')}
              className={`px-3 py-1 rounded-lg font-semibold transition-colors ${
                activeLayer === 'wind' ? 'bg-emerald-500 text-white' : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-200'
              }`}
            >
              Wind Speed
            </button>
          </div>

          <div className="flex items-center bg-slate-100 dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl p-1 text-xs">
            <button
              onClick={() => setMapTileStyle('dark')}
              className={`px-2.5 py-1 rounded-lg font-semibold ${
                mapTileStyle === 'dark' ? 'bg-slate-800 text-white' : 'text-slate-600 dark:text-slate-400'
              }`}
            >
              Dark
            </button>
            <button
              onClick={() => setMapTileStyle('streets')}
              className={`px-2.5 py-1 rounded-lg font-semibold ${
                mapTileStyle === 'streets' ? 'bg-slate-800 text-white' : 'text-slate-600 dark:text-slate-400'
              }`}
            >
              Streets
            </button>
            <button
              onClick={() => setMapTileStyle('satellite')}
              className={`px-2.5 py-1 rounded-lg font-semibold ${
                mapTileStyle === 'satellite' ? 'bg-slate-800 text-white' : 'text-slate-600 dark:text-slate-400'
              }`}
            >
              Satellite
            </button>
          </div>

          <button
            onClick={useDeviceLocation}
            className="p-2 rounded-xl bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-saffron-600 dark:text-saffron-400 border border-slate-200 dark:border-slate-700 transition-colors"
            title="Recenter to my location"
          >
            <Navigation className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* Map Display Container */}
      <div className="flex-1 relative rounded-2xl overflow-hidden border border-slate-800">
        <MapContainer center={[lat, lon]} zoom={6} scrollWheelZoom={true} className="w-full h-full">
          <TileLayer
            attribution='&copy; <a href="https://carto.com/">CARTO</a> & OpenStreetMap'
            url={tileUrls[mapTileStyle]}
          />
          <MapRecenter lat={lat} lon={lon} />

          {/* Current Active Location Marker */}
          <Marker position={[lat, lon]}>
            <Popup>
              <div className="p-1 space-y-1 text-slate-100">
                <h4 className="font-bold text-sm text-saffron-400">{location.name}</h4>
                <p className="text-xs text-slate-300">Temp: <strong>{weather?.temperature ?? 31.5}°C</strong></p>
                <p className="text-xs text-slate-300">Rain Prob: <strong>{weather?.rain_probability ?? 78}%</strong></p>
                <p className="text-xs text-slate-300">Condition: {weather?.weather_desc ?? 'Partly Cloudy'}</p>
              </div>
            </Popup>
          </Marker>

          {/* IMD AWS Weather Stations Grid */}
          {weatherStations.map((station, idx) => (
            <CircleMarker
              key={idx}
              center={[station.lat, station.lon]}
              radius={8}
              pathOptions={{
                color: station.status.includes('Orange') || station.status.includes('Heavy') ? '#f97316' : station.status.includes('Heatwave') ? '#ef4444' : '#10b981',
                fillColor: station.status.includes('Orange') || station.status.includes('Heavy') ? '#f97316' : station.status.includes('Heatwave') ? '#ef4444' : '#10b981',
                fillOpacity: 0.6
              }}
            >
              <Popup>
                <div className="p-1 text-slate-100 space-y-1">
                  <h4 className="font-bold text-xs text-white">{station.name}</h4>
                  <p className="text-[11px] text-slate-300">Temperature: <strong>{station.temp}°C</strong></p>
                  <p className="text-[11px] text-slate-300">Rain Prob: <strong>{station.rainProb}%</strong></p>
                  <p className="text-[11px] font-bold text-amber-400">{station.status}</p>
                </div>
              </Popup>
            </CircleMarker>
          ))}
        </MapContainer>

        {/* Overlay Map Legend */}
        <div className="absolute bottom-4 left-4 z-[400] bg-white/95 dark:bg-navy-900/90 backdrop-blur-md border border-slate-200 dark:border-slate-800 p-3 rounded-2xl text-xs space-y-2 shadow-xl max-w-xs transition-colors">
          <span className="font-bold text-slate-800 dark:text-slate-200 block text-[11px] uppercase tracking-wider">
            {activeLayer === 'rain' ? 'Rainfall Intensity (mm/h)' : activeLayer === 'temp' ? 'Temperature Scale (°C)' : 'Wind Velocity'}
          </span>
          <div className="flex items-center space-x-1.5 text-[10px] text-slate-300">
            <span className="w-3 h-3 rounded-full bg-emerald-500 inline-block"></span>
            <span>Normal</span>
            <span className="w-3 h-3 rounded-full bg-amber-400 inline-block ml-2"></span>
            <span>Moderate / Watch</span>
            <span className="w-3 h-3 rounded-full bg-saffron-500 inline-block ml-2"></span>
            <span>Heavy Alert</span>
            <span className="w-3 h-3 rounded-full bg-red-500 inline-block ml-2"></span>
            <span>Severe</span>
          </div>
        </div>
      </div>
    </div>
  );
};
