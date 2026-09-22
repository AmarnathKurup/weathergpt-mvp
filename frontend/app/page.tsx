"use client";

import { useState } from "react";
import LocationSearchBar from "@/components/LocationSearchBar";
import CurrentWeatherCard from "@/components/CurrentWeatherCard";
import ForecastStrip from "@/components/ForecastStrip";
import AlertsPanel from "@/components/AlertsPanel";
import RiskGauge from "@/components/RiskGauge";
import FarmerAdvisoryCard from "@/components/FarmerAdvisoryCard";

export default function DashboardPage() {
  const [farmerMode, setFarmerMode] = useState(false);

  return (
    <div className="flex flex-col gap-6">
      <LocationSearchBar />

      <div className="flex justify-end">
        <label className="flex items-center gap-2 text-sm cursor-pointer select-none rounded-full border border-slate-300 dark:border-slate-600 px-3 py-1.5 hover:bg-slate-100 dark:hover:bg-slate-800">
          <input
            type="checkbox"
            checked={farmerMode}
            onChange={(e) => setFarmerMode(e.target.checked)}
          />
          🌾 Farmer Mode
        </label>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-1 flex flex-col gap-6">
          <CurrentWeatherCard />
          <RiskGauge />
        </div>
        <div className="lg:col-span-2 flex flex-col gap-6">
          <ForecastStrip />
          <AlertsPanel />
          {farmerMode && <FarmerAdvisoryCard />}
        </div>
      </div>
    </div>
  );
}
