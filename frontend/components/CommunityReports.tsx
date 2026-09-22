"use client";

import { useEffect, useState, useCallback } from "react";
import { api, ApiError } from "@/lib/api";
import type { CommunityReport } from "@/lib/types";
import { useLocation } from "@/lib/location-context";

const CATEGORIES = [
  "Flooding",
  "Waterlogging",
  "Power Outage",
  "Road Blocked",
  "Heavy Rain",
  "Landslide Risk",
  "Fallen Tree",
  "Other",
];

const CATEGORY_ICON: Record<string, string> = {
  Flooding: "🌊",
  Waterlogging: "💧",
  "Power Outage": "⚡",
  "Road Blocked": "🚧",
  "Heavy Rain": "🌧️",
  "Landslide Risk": "⛰️",
  "Fallen Tree": "🌳",
  Other: "📍",
};

function timeAgo(iso: string): string {
  const diffMs = Date.now() - new Date(iso).getTime();
  const mins = Math.floor(diffMs / 60000);
  if (mins < 1) return "just now";
  if (mins < 60) return `${mins}m ago`;
  const hrs = Math.floor(mins / 60);
  return `${hrs}h ago`;
}

export default function CommunityReports() {
  const { location } = useLocation();
  const [reports, setReports] = useState<CommunityReport[]>([]);
  const [showForm, setShowForm] = useState(false);
  const [category, setCategory] = useState(CATEGORIES[0]);
  const [note, setNote] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const loadReports = useCallback(() => {
    if (!location) return;
    api
      .communityReports({ lat: location.lat, lon: location.lon, radius_km: 30 })
      .then(setReports)
      .catch(() => {
        // Non-critical - fail silently, the feed just stays empty
      });
  }, [location]);

  useEffect(() => {
    loadReports();
  }, [loadReports]);

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    if (!location) return;
    setSubmitting(true);
    setError(null);
    try {
      await api.createCommunityReport({
        lat: location.lat,
        lon: location.lon,
        category,
        note: note.trim() || undefined,
        location_name: location.name,
      });
      setNote("");
      setShowForm(false);
      loadReports();
    } catch (e) {
      setError(e instanceof ApiError ? e.message : "Failed to submit report");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div className="rounded-2xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 p-4">
      <div className="flex items-center justify-between mb-3">
        <h3 className="font-semibold text-slate-700 dark:text-slate-200">
          📢 Ground Reports Nearby
        </h3>
        <button
          onClick={() => setShowForm((v) => !v)}
          className="text-xs rounded-full bg-sky-600 text-white px-3 py-1.5 hover:bg-sky-700"
        >
          {showForm ? "Cancel" : "+ Report Condition"}
        </button>
      </div>

      {showForm && (
        <form onSubmit={submit} className="mb-4 flex flex-col gap-2 border-b border-slate-200 dark:border-slate-700 pb-4">
          <select
            value={category}
            onChange={(e) => setCategory(e.target.value)}
            className="rounded-lg border border-slate-300 dark:border-slate-600 dark:bg-slate-800 px-3 py-2 text-sm"
          >
            {CATEGORIES.map((c) => (
              <option key={c} value={c}>
                {CATEGORY_ICON[c]} {c}
              </option>
            ))}
          </select>
          <input
            value={note}
            onChange={(e) => setNote(e.target.value)}
            placeholder="Optional note (e.g. 'knee-deep near the bus stand')"
            maxLength={280}
            className="rounded-lg border border-slate-300 dark:border-slate-600 dark:bg-slate-800 px-3 py-2 text-sm"
          />
          {error && <p className="text-xs text-red-500">{error}</p>}
          <button
            type="submit"
            disabled={submitting || !location}
            className="rounded-lg bg-sky-600 text-white px-3 py-2 text-sm font-medium hover:bg-sky-700 disabled:opacity-50"
          >
            {submitting ? "Submitting..." : `Submit for ${location?.name ?? "current location"}`}
          </button>
          <p className="text-[11px] text-slate-400">
            Reports are visible to everyone nearby and expire after 24 hours.
          </p>
        </form>
      )}

      {reports.length === 0 ? (
        <p className="text-sm text-slate-400">No reports nearby in the last 24 hours.</p>
      ) : (
        <ul className="flex flex-col gap-2">
          {reports.map((r) => (
            <li
              key={r.id}
              className="flex items-start gap-2 text-sm rounded-lg bg-slate-50 dark:bg-slate-800 px-3 py-2"
            >
              <span>{CATEGORY_ICON[r.category] ?? "📍"}</span>
              <div className="flex-1">
                <div className="flex items-center justify-between gap-2">
                  <span className="font-medium">{r.category}</span>
                  <span className="text-[11px] text-slate-400">
                    {r.distance_km != null ? `${r.distance_km} km · ` : ""}
                    {timeAgo(r.created_at)}
                  </span>
                </div>
                {r.note && <p className="text-slate-500 dark:text-slate-400">{r.note}</p>}
              </div>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
