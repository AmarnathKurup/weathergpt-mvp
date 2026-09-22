"use client";

import { useEffect, useState } from "react";
import { api, ApiError } from "@/lib/api";
import type { AnalysisResponse } from "@/lib/types";
import { useLocation } from "@/lib/location-context";

function levelColor(level: string): { bar: string; text: string; bg: string } {
  switch (level) {
    case "Severe":
      return { bar: "bg-red-600", text: "text-red-700", bg: "bg-red-50 border-red-200" };
    case "High":
      return { bar: "bg-orange-500", text: "text-orange-700", bg: "bg-orange-50 border-orange-200" };
    case "Moderate":
      return { bar: "bg-yellow-500", text: "text-yellow-700", bg: "bg-yellow-50 border-yellow-200" };
    default:
      return { bar: "bg-emerald-500", text: "text-emerald-700", bg: "bg-emerald-50 border-emerald-200" };
  }
}

export default function RiskGauge() {
  const { location } = useLocation();
  const [data, setData] = useState<AnalysisResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!location) return;
    let cancelled = false;
    setLoading(true);
    setError(null);
    api
      .analysis({ lat: location.lat, lon: location.lon })
      .then((res) => {
        if (!cancelled) setData(res);
      })
      .catch((e) => {
        if (!cancelled) setError(e instanceof ApiError ? e.message : "Failed to load risk score");
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });
    return () => {
      cancelled = true;
    };
  }, [location]);

  if (loading) {
    return <div className="h-32 rounded-2xl bg-slate-100 animate-pulse dark:bg-slate-800" />;
  }

  if (error || !data) {
    return (
      <div className="rounded-2xl border border-red-200 bg-red-50 text-red-700 p-4 text-sm">
        Couldn&apos;t compute risk score{error ? `: ${error}` : ""}
      </div>
    );
  }

  const colors = levelColor(data.risk_level);

  return (
    <div className={`rounded-2xl border p-4 ${colors.bg}`}>
      <div className="flex items-center justify-between mb-2">
        <h3 className="font-semibold text-slate-700 dark:text-slate-200">
          🎯 Weather Risk Score
        </h3>
        <span className={`text-xs font-bold uppercase tracking-wide ${colors.text}`}>
          {data.risk_level}
        </span>
      </div>
      <div className="flex items-center gap-3">
        <span className={`text-3xl font-bold ${colors.text}`}>{data.risk_score}</span>
        <div className="flex-1 h-3 rounded-full bg-white/60 dark:bg-slate-900/40 overflow-hidden">
          <div
            className={`h-full ${colors.bar} transition-all duration-500`}
            style={{ width: `${data.risk_score}%` }}
          />
        </div>
        <span className="text-xs text-slate-400">/100</span>
      </div>
      <ul className="mt-3 flex flex-wrap gap-1.5">
        {data.risk_factors.map((f, i) => (
          <li
            key={i}
            className="text-[11px] rounded-full bg-white/70 dark:bg-slate-900/40 px-2 py-0.5 text-slate-600 dark:text-slate-300"
          >
            {f}
          </li>
        ))}
      </ul>
    </div>
  );
}
