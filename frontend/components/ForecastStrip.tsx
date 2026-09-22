"use client";

import { useEffect, useState } from "react";
import { api, ApiError } from "@/lib/api";
import type { ForecastResponse } from "@/lib/types";
import { useLocation } from "@/lib/location-context";
import { formatDay, weatherEmoji } from "@/lib/format";

export default function ForecastStrip() {
  const { location } = useLocation();
  const [data, setData] = useState<ForecastResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!location) return;
    let cancelled = false;
    setLoading(true);
    setError(null);
    api
      .forecast({ lat: location.lat, lon: location.lon, days: 7 })
      .then((res) => {
        if (!cancelled) setData(res);
      })
      .catch((e) => {
        if (!cancelled) setError(e instanceof ApiError ? e.message : "Failed to load forecast");
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
      <div className="grid grid-cols-3 sm:grid-cols-7 gap-2">
        {Array.from({ length: 7 }).map((_, i) => (
          <div key={i} className="h-28 rounded-xl bg-slate-100 animate-pulse dark:bg-slate-800" />
        ))}
      </div>
    );
  }

  if (error) {
    return (
      <div className="rounded-xl bg-red-50 border border-red-200 text-red-700 p-4 text-sm">
        Couldn&apos;t load forecast: {error}
      </div>
    );
  }

  if (!data) return null;

  return (
    <div>
      <h2 className="font-semibold mb-2 text-slate-700 dark:text-slate-200">7-Day Forecast</h2>
      <div className="grid grid-cols-3 sm:grid-cols-7 gap-2">
        {data.daily.map((d) => (
          <div
            key={d.date}
            className="rounded-xl border border-slate-200 dark:border-slate-700 p-3 text-center bg-white dark:bg-slate-800"
          >
            <p className="text-xs text-slate-500 dark:text-slate-400">{formatDay(d.date)}</p>
            <p className="text-2xl my-1">{weatherEmoji(d.weather_code, true)}</p>
            <p className="text-sm font-semibold">
              {d.temp_max_c !== null && d.temp_max_c !== undefined ? Math.round(d.temp_max_c) : "—"}°
            </p>
            <p className="text-xs text-slate-400">
              {d.temp_min_c !== null && d.temp_min_c !== undefined ? Math.round(d.temp_min_c) : "—"}°
            </p>
            {(d.precipitation_probability_pct ?? 0) > 0 && (
              <p className="text-[11px] text-sky-600 mt-1">
                💧{Math.round(d.precipitation_probability_pct ?? 0)}%
              </p>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
