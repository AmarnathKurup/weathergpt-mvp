"use client";

import { useEffect, useState } from "react";
import { api, ApiError } from "@/lib/api";
import type { CurrentWeather } from "@/lib/types";
import { useLocation } from "@/lib/location-context";
import { weatherEmoji } from "@/lib/format";

export default function CurrentWeatherCard() {
  const { location } = useLocation();
  const [data, setData] = useState<CurrentWeather | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!location) return;
    let cancelled = false;
    setLoading(true);
    setError(null);
    api
      .currentWeather({ lat: location.lat, lon: location.lon })
      .then((res) => {
        if (!cancelled) setData(res);
      })
      .catch((e) => {
        if (!cancelled) setError(e instanceof ApiError ? e.message : "Failed to load weather");
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });
    return () => {
      cancelled = true;
    };
  }, [location]);

  if (loading) {
    return (
      <div className="rounded-2xl bg-gradient-to-br from-sky-500 to-sky-700 text-white p-6 animate-pulse h-48" />
    );
  }

  if (error) {
    return (
      <div className="rounded-2xl bg-red-50 border border-red-200 text-red-700 p-6">
        <p className="font-medium">Couldn&apos;t load current weather</p>
        <p className="text-sm mt-1">{error}</p>
      </div>
    );
  }

  if (!data) return null;

  return (
    <div className="rounded-2xl bg-gradient-to-br from-sky-500 to-sky-700 text-white p-6 shadow-lg">
      <div className="flex items-start justify-between">
        <div>
          <p className="text-sm opacity-80">{data.location}</p>
          <p className="text-5xl font-bold mt-1">
            {data.temperature_c !== null && data.temperature_c !== undefined
              ? `${Math.round(data.temperature_c)}°C`
              : "—"}
          </p>
          <p className="text-sm mt-1 opacity-90">{data.condition}</p>
          <p className="text-xs mt-1 opacity-70">
            Feels like{" "}
            {data.apparent_temperature_c !== null && data.apparent_temperature_c !== undefined
              ? `${Math.round(data.apparent_temperature_c)}°C`
              : "—"}
          </p>
        </div>
        <div className="text-6xl">{weatherEmoji(data.weather_code, data.is_day)}</div>
      </div>
      <div className="grid grid-cols-3 gap-3 mt-6 text-sm">
        <div className="bg-white/10 rounded-lg p-2 text-center">
          <p className="opacity-70 text-xs">Humidity</p>
          <p className="font-semibold">{data.humidity_pct ?? "—"}%</p>
        </div>
        <div className="bg-white/10 rounded-lg p-2 text-center">
          <p className="opacity-70 text-xs">Wind</p>
          <p className="font-semibold">
            {data.wind_speed_kmh !== null && data.wind_speed_kmh !== undefined
              ? `${Math.round(data.wind_speed_kmh)} km/h`
              : "—"}
          </p>
        </div>
        <div className="bg-white/10 rounded-lg p-2 text-center">
          <p className="opacity-70 text-xs">Rain</p>
          <p className="font-semibold">{data.precipitation_mm ?? 0} mm</p>
        </div>
      </div>
    </div>
  );
}
