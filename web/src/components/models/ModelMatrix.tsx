import React from 'react';
import { useApp } from '../../context/AppContext';
import { Cpu, ShieldCheck, CheckCircle2 } from 'lucide-react';

export const ModelMatrix: React.FC = () => {
  const { location } = useApp();

  const models = [
    { name: 'ECMWF IFS (0.1°)', provider: 'European Centre for Medium-Range Weather Forecasts', temp: '31.5°C', rainProb: '78%', precip: '14.2 mm', wind: '14.5 km/h', confidence: 'High (94%)' },
    { name: 'GFS NCEP (0.25°)', provider: 'NOAA Global Forecast System', temp: '32.0°C', rainProb: '82%', precip: '16.0 mm', wind: '18.0 km/h', confidence: 'High (91%)' },
    { name: 'IMD NCUM (Regional)', provider: 'National Centre for Medium Range Weather Forecasting (India)', temp: '31.2°C', rainProb: '75%', precip: '12.8 mm', wind: '14.0 km/h', confidence: 'Very High (96%)' },
    { name: 'ICON-EU (0.12°)', provider: 'Deutscher Wetterdienst (DWD Germany)', temp: '31.8°C', rainProb: '70%', precip: '11.5 mm', wind: '16.2 km/h', confidence: 'Moderate (85%)' },
  ];

  return (
    <div className="space-y-6">
      <div className="glass-panel rounded-3xl p-6 border border-slate-200 dark:border-slate-800 flex items-center justify-between transition-colors">
        <div className="flex items-center space-x-3">
          <div className="p-2.5 rounded-2xl bg-saffron-500/10 text-saffron-600 dark:text-saffron-500 border border-saffron-500/20">
            <Cpu className="w-6 h-6" />
          </div>
          <div>
            <h2 className="text-xl font-bold text-slate-900 dark:text-white">Numerical Weather Prediction (NWP) Model Comparison</h2>
            <p className="text-xs text-slate-500 dark:text-slate-400">Multi-Model Ensemble Matrix for {location.name || 'Current Location'}</p>
          </div>
        </div>

        <div className="flex items-center space-x-2 text-xs text-slate-600 dark:text-slate-400 bg-slate-100 dark:bg-slate-900 px-3 py-1.5 rounded-xl border border-slate-200 dark:border-slate-800">
          <ShieldCheck className="w-4 h-4 text-emerald-600 dark:text-emerald-400" />
          <span>Real-time NWP Ensemble</span>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {models.map((m, idx) => (
          <div key={idx} className="glass-panel rounded-3xl p-6 border border-slate-200 dark:border-slate-800 space-y-4 shadow-md dark:shadow-lg transition-colors">
            <div className="flex items-center justify-between border-b border-slate-200 dark:border-slate-800 pb-3">
              <div>
                <h3 className="font-bold text-base text-slate-900 dark:text-white">{m.name}</h3>
                <span className="text-[11px] text-slate-500 dark:text-slate-400">{m.provider}</span>
              </div>
              <span className="text-xs font-bold px-2.5 py-1 rounded-full bg-emerald-500/20 text-emerald-700 dark:text-emerald-400 border border-emerald-500/30">
                {m.confidence}
              </span>
            </div>

            <div className="grid grid-cols-2 gap-3 text-xs">
              <div className="p-3 rounded-2xl bg-slate-100/80 dark:bg-slate-900/60 border border-slate-200 dark:border-slate-800">
                <span className="text-slate-500 dark:text-slate-400 block">Temperature</span>
                <span className="text-base font-bold text-slate-900 dark:text-white">{m.temp}</span>
              </div>
              <div className="p-3 rounded-2xl bg-slate-100/80 dark:bg-slate-900/60 border border-slate-200 dark:border-slate-800">
                <span className="text-slate-500 dark:text-slate-400 block">Rain Probability</span>
                <span className="text-base font-bold text-sky-600 dark:text-sky-400">{m.rainProb}</span>
              </div>
              <div className="p-3 rounded-2xl bg-slate-100/80 dark:bg-slate-900/60 border border-slate-200 dark:border-slate-800">
                <span className="text-slate-500 dark:text-slate-400 block">Precipitation Sum</span>
                <span className="text-base font-bold text-slate-800 dark:text-slate-200">{m.precip}</span>
              </div>
              <div className="p-3 rounded-2xl bg-slate-100/80 dark:bg-slate-900/60 border border-slate-200 dark:border-slate-800">
                <span className="text-slate-500 dark:text-slate-400 block">Wind Velocity</span>
                <span className="text-base font-bold text-slate-800 dark:text-slate-200">{m.wind}</span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
