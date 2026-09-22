"use client";

import { useEffect, useState } from "react";
import { api, ApiError } from "@/lib/api";
import type { FarmerAdvisoryResponse } from "@/lib/types";
import { useLocation } from "@/lib/location-context";

export default function FarmerAdvisoryCard() {
  const { location } = useLocation();
  const [data, setData] = useState<FarmerAdvisoryResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!location) return;
    let cancelled = false;
    setLoading(true);
    setError(null);
    api
      .farmerAdvisory({ lat: location.lat, lon: location.lon })
      .then((res) => {
        if (!cancelled) setData(res);
      })
      .catch((e) => {
        if (!cancelled) setError(e instanceof ApiError ? e.message : "Failed to load advisory");
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });
    return () => {
      cancelled = true;
    };
  }, [location]);

  if (loading) {
    return <div className="h-40 rounded-2xl bg-slate-100 animate-pulse dark:bg-slate-800" />;
  }

  if (error || !data) {
    return (
      <div className="rounded-2xl border border-red-200 bg-red-50 text-red-700 p-4 text-sm">
        Couldn&apos;t load farmer advisory{error ? `: ${error}` : ""}
      </div>
    );
  }

  const rows = [
    { icon: "🧪", label: "Spraying", text: data.spray_advice },
    { icon: "💧", label: "Irrigation", text: data.irrigation_advice },
    { icon: "🐄", label: "Livestock", text: data.livestock_advice },
  ];

  return (
    <div className="rounded-2xl border border-lime-200 bg-lime-50 dark:bg-lime-950/20 dark:border-lime-900 p-4">
      <h3 className="font-semibold text-lime-800 dark:text-lime-300 mb-3">
        🌾 Farmer Advisory — {data.location}
      </h3>
      <div className="flex flex-col gap-2">
        {rows.map((r) => (
          <div key={r.label} className="flex gap-2 text-sm">
            <span>{r.icon}</span>
            <div>
              <span className="font-medium text-lime-900 dark:text-lime-200">{r.label}: </span>
              <span className="text-slate-700 dark:text-slate-300">{r.text}</span>
            </div>
          </div>
        ))}
      </div>
      <p className="text-[11px] text-lime-700/70 dark:text-lime-400/60 mt-3">
        Rule-of-thumb guidance based on forecast data — not a substitute for local
        agricultural extension advice.
      </p>
    </div>
  );
}
