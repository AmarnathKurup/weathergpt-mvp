"use client";

import { useEffect, useState } from "react";
import { api, ApiError } from "@/lib/api";
import type { AlertsResponse } from "@/lib/types";
import { useLocation } from "@/lib/location-context";
import { severityColor } from "@/lib/format";

export default function AlertsPanel() {
  const { location } = useLocation();
  const [data, setData] = useState<AlertsResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!location) return;
    let cancelled = false;
    setLoading(true);
    setError(null);
    api
      .alerts({ lat: location.lat, lon: location.lon })
      .then((res) => {
        if (!cancelled) setData(res);
      })
      .catch((e) => {
        if (!cancelled) setError(e instanceof ApiError ? e.message : "Failed to load alerts");
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });
    return () => {
      cancelled = true;
    };
  }, [location]);

  if (loading) {
    return <div className="h-24 rounded-xl bg-slate-100 animate-pulse dark:bg-slate-800" />;
  }

  if (error) {
    return (
      <div className="rounded-xl bg-red-50 border border-red-200 text-red-700 p-4 text-sm">
        Couldn&apos;t load alerts: {error}
      </div>
    );
  }

  const all = [...(data?.alerts ?? []), ...(data?.generated ?? [])];

  return (
    <div>
      <h2 className="font-semibold mb-2 text-slate-700 dark:text-slate-200">
        Alerts &amp; Hazards
      </h2>
      {all.length === 0 ? (
        <div className="rounded-xl border border-emerald-200 bg-emerald-50 text-emerald-800 p-4 text-sm">
          ✅ No active weather alerts for this location right now.
        </div>
      ) : (
        <div className="flex flex-col gap-2">
          {all.map((a) => (
            <div
              key={a.id}
              className={`rounded-xl border p-3 text-sm ${severityColor(a.severity)}`}
            >
              <div className="flex items-center justify-between gap-2">
                <p className="font-semibold">
                  ⚠️ {a.event} <span className="font-normal opacity-70">· {a.severity}</span>
                </p>
                <span className="text-[10px] uppercase tracking-wide opacity-60">{a.source}</span>
              </div>
              <p className="mt-1">{a.headline}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
