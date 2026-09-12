import React from 'react';
import { useApp } from '../../context/AppContext';
import { BarChart3, TrendingUp, CloudRain, Thermometer, ShieldCheck } from 'lucide-react';
import {
  ResponsiveContainer,
  AreaChart,
  Area,
  XAxis,
  YAxis,
  Tooltip,
  BarChart,
  Bar,
  CartesianGrid
} from 'recharts';

export const ClimateAnalytics: React.FC = () => {
  const { location, t } = useApp();

  const temperatureData = [
    { year: '2016', meanTemp: 27.2, anomaly: 0.8 },
    { year: '2017', meanTemp: 27.4, anomaly: 1.0 },
    { year: '2018', meanTemp: 27.1, anomaly: 0.7 },
    { year: '2019', meanTemp: 27.6, anomaly: 1.2 },
    { year: '2020', meanTemp: 27.3, anomaly: 0.9 },
    { year: '2021', meanTemp: 27.5, anomaly: 1.1 },
    { year: '2022', meanTemp: 27.8, anomaly: 1.4 },
    { year: '2023', meanTemp: 28.1, anomaly: 1.7 },
    { year: '2024', meanTemp: 28.3, anomaly: 1.9 },
    { year: '2025', meanTemp: 28.5, anomaly: 2.1 },
  ];

  const rainfallData = [
    { month: 'Jan', rainfall: 18, normal: 15 },
    { month: 'Feb', rainfall: 24, normal: 22 },
    { month: 'Mar', rainfall: 35, normal: 30 },
    { month: 'Apr', rainfall: 58, normal: 50 },
    { month: 'May', rainfall: 142, normal: 130 },
    { month: 'Jun', rainfall: 285, normal: 300 },
    { month: 'Jul', rainfall: 390, normal: 375 },
    { month: 'Aug', rainfall: 360, normal: 350 },
    { month: 'Sep', rainfall: 295, normal: 280 },
    { month: 'Oct', rainfall: 150, normal: 140 },
    { month: 'Nov', rainfall: 32, normal: 25 },
    { month: 'Dec', rainfall: 12, normal: 10 },
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="glass-panel rounded-3xl p-6 border border-slate-200 dark:border-slate-800 flex items-center justify-between transition-colors">
        <div className="flex items-center space-x-3">
          <div className="p-2.5 rounded-2xl bg-saffron-500/10 text-saffron-600 dark:text-saffron-500 border border-saffron-500/20">
            <BarChart3 className="w-6 h-6" />
          </div>
          <div>
            <h2 className="text-xl font-bold text-slate-900 dark:text-white">Climate Intelligence & Historical Anomalies</h2>
            <p className="text-xs text-slate-500 dark:text-slate-400">10-Year Decadal Metrics & Monsoon Distribution for {location.name || 'District'}</p>
          </div>
        </div>

        <div className="flex items-center space-x-2 text-xs text-slate-600 dark:text-slate-400 bg-slate-100 dark:bg-slate-900 px-3 py-1.5 rounded-xl border border-slate-200 dark:border-slate-800">
          <ShieldCheck className="w-4 h-4 text-emerald-600 dark:text-emerald-400" />
          <span>IMD Climatological Normal Dataset</span>
        </div>
      </div>

      {/* Temperature Trend Area Chart */}
      <div className="glass-panel rounded-3xl p-6 border border-slate-200 dark:border-slate-800 space-y-4 transition-colors">
        <div className="flex items-center justify-between">
          <h3 className="font-bold text-base text-slate-900 dark:text-white flex items-center gap-2">
            <Thermometer className="w-4 h-4 text-saffron-500" />
            <span>Mean Annual Temperature Trend (°C)</span>
          </h3>
          <span className="text-xs font-semibold text-saffron-600 dark:text-saffron-400">+1.3°C Decadal Warming</span>
        </div>

        <div className="h-64 w-full">
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={temperatureData}>
              <defs>
                <linearGradient id="tempGrad" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#ff9933" stopOpacity={0.4}/>
                  <stop offset="95%" stopColor="#ff9933" stopOpacity={0.0}/>
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
              <XAxis dataKey="year" stroke="#64748b" fontSize={12} />
              <YAxis stroke="#64748b" fontSize={12} domain={[25, 30]} />
              <Tooltip
                contentStyle={{ backgroundColor: '#ffffff', borderColor: '#cbd5e1', borderRadius: '0.75rem', color: '#0f172a' }}
              />
              <Area type="monotone" dataKey="meanTemp" stroke="#ff9933" strokeWidth={3} fillOpacity={1} fill="url(#tempGrad)" />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Monsoon Rainfall Distribution Bar Chart */}
      <div className="glass-panel rounded-3xl p-6 border border-slate-200 dark:border-slate-800 space-y-4 transition-colors">
        <div className="flex items-center justify-between">
          <h3 className="font-bold text-base text-slate-900 dark:text-white flex items-center gap-2">
            <CloudRain className="w-4 h-4 text-sky-500" />
            <span>Monthly Precipitation Distribution vs Climatological Normal (mm)</span>
          </h3>
          <span className="text-xs font-semibold text-sky-600 dark:text-sky-400">1,945 mm Annual Rainfall</span>
        </div>

        <div className="h-64 w-full">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={rainfallData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
              <XAxis dataKey="month" stroke="#64748b" fontSize={12} />
              <YAxis stroke="#64748b" fontSize={12} />
              <Tooltip
                contentStyle={{ backgroundColor: '#ffffff', borderColor: '#cbd5e1', borderRadius: '0.75rem', color: '#0f172a' }}
              />
              <Bar dataKey="rainfall" fill="#38bdf8" radius={[4, 4, 0, 0]} name="Observed Rainfall" />
              <Bar dataKey="normal" fill="#cbd5e1" radius={[4, 4, 0, 0]} name="Normal Baseline" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
};
