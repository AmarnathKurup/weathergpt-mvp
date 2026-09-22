"use client";

import dynamic from "next/dynamic";
import LocationSearchBar from "@/components/LocationSearchBar";
import CommunityReports from "@/components/CommunityReports";

const WeatherMap = dynamic(() => import("@/components/WeatherMap"), {
  ssr: false,
  loading: () => (
    <div className="h-[500px] w-full rounded-2xl bg-slate-100 dark:bg-slate-800 animate-pulse" />
  ),
});

export default function MapPage() {
  return (
    <div className="flex flex-col gap-6">
      <LocationSearchBar />
      <p className="text-sm text-slate-500 dark:text-slate-400">
        Click anywhere on the map to check the weather there. 📍 markers are conditions
        reported by nearby users in the last 24 hours.
      </p>
      <WeatherMap />
      <CommunityReports />
    </div>
  );
}
