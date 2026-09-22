"use client";

import { useState } from "react";
import { useLocation } from "@/lib/location-context";

export default function LocationSearchBar() {
  const { location, loading, error, setLocationByName, useBrowserLocation } = useLocation();
  const [query, setQuery] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (query.trim()) {
      setLocationByName(query.trim());
    }
  };

  return (
    <div className="flex flex-col gap-2 w-full">
      <form onSubmit={handleSubmit} className="flex gap-2 w-full">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Search a city, e.g. Mumbai, Delhi, Kochi..."
          className="flex-1 rounded-lg border border-slate-300 px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-sky-500 dark:bg-slate-800 dark:border-slate-600"
        />
        <button
          type="submit"
          disabled={loading}
          className="rounded-lg bg-sky-600 px-4 py-2 text-sm font-medium text-white hover:bg-sky-700 disabled:opacity-50"
        >
          Search
        </button>
        <button
          type="button"
          onClick={useBrowserLocation}
          disabled={loading}
          title="Use my current location"
          className="rounded-lg border border-slate-300 px-3 py-2 text-sm hover:bg-slate-100 disabled:opacity-50 dark:border-slate-600 dark:hover:bg-slate-800"
        >
          📍
        </button>
      </form>
      <div className="flex items-center justify-between text-xs text-slate-500 dark:text-slate-400">
        <span>
          {loading
            ? "Locating..."
            : location
            ? `Showing: ${location.name} (${location.lat.toFixed(2)}, ${location.lon.toFixed(2)})`
            : "No location selected"}
        </span>
        {error && <span className="text-red-500">{error}</span>}
      </div>
    </div>
  );
}
