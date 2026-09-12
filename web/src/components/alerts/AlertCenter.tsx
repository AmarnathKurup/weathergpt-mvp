import React, { useState } from 'react';
import { useApp } from '../../context/AppContext';
import { WarningItem } from '../../types';
import { ShieldAlert, AlertTriangle, ShieldCheck, Info, Filter, Bell, MapPin, Clock } from 'lucide-react';

export const AlertCenter: React.FC = () => {
  const { weather, location, emergencyMode, toggleEmergencyMode, t } = useApp();
  const [filterSeverity, setFilterSeverity] = useState<string>('ALL');

  const activeWarnings: WarningItem[] = weather?.warnings && weather.warnings.length > 0
    ? weather.warnings
    : [
        {
          level: 'ORANGE',
          category: 'Thunderstorm & Lightning',
          headline: 'IMD Orange Alert — Heavy Rainfall & Severe Thunderstorm Warning',
          description: 'Convective cloud cluster developing over district. Rainfall expected 15-25mm/hr accompanied by squally winds 40-50 km/h and intense cloud-to-ground lightning activity between 17:00 and 20:00 IST.',
          issued_at: '2026-09-02T14:30:00IST',
          source: 'India Meteorological Department (IMD) Kolkata Division'
        },
        {
          level: 'YELLOW',
          category: 'Heavy Rainfall Watch',
          headline: 'IMD Yellow Watch — Monsoonal Heavy Rainfall Spell',
          description: 'Active monsoonal trough passing over Gangetic West Bengal. Isolated heavy precipitation expected across low-lying coastal districts.',
          issued_at: '2026-09-02T12:00:00IST',
          source: 'IMD Regional Meteorological Centre'
        }
      ];

  const filteredWarnings = activeWarnings.filter(w => {
    if (filterSeverity === 'ALL') return true;
    return w.level === filterSeverity;
  });

  const getSeverityBadgeClass = (level: string) => {
    switch (level.toUpperCase()) {
      case 'RED':
        return 'bg-red-500/20 text-red-400 border-red-500/50';
      case 'ORANGE':
        return 'bg-saffron-500/20 text-saffron-400 border-saffron-500/50';
      case 'YELLOW':
        return 'bg-amber-500/20 text-amber-300 border-amber-500/50';
      default:
        return 'bg-emerald-500/20 text-emerald-400 border-emerald-500/50';
    }
  };

  const getRecommendedAction = (category: string) => {
    if (category.includes('Thunderstorm') || category.includes('Lightning')) {
      return 'Stay indoors. Avoid open fields, metal structures, and tall trees during lightning activity.';
    }
    if (category.includes('Heat') || category.includes('High Temp')) {
      return 'Drink plenty of water. Avoid outdoor exposure during peak heat hours (12:00–15:00 IST).';
    }
    return 'Exercise caution while travelling. Monitor local IMD weather bulletins.';
  };

  return (
    <div className="space-y-6">
      {/* Header Banner */}
      <div className={`p-6 rounded-3xl border transition-all ${
        emergencyMode
          ? 'bg-red-900/90 border-red-500 shadow-2xl animate-pulse text-white'
          : 'glass-panel border-slate-200 dark:border-slate-800'
      }`}>
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div className="flex items-center space-x-4">
            <div className={`w-12 h-12 rounded-2xl flex items-center justify-center font-bold shadow-lg ${
              emergencyMode ? 'bg-red-600 text-white' : 'bg-saffron-500/20 text-saffron-600 dark:text-saffron-500 border border-saffron-500/30'
            }`}>
              <ShieldAlert className="w-7 h-7" />
            </div>
            <div>
              <h2 className="text-xl md:text-2xl font-bold text-slate-900 dark:text-white tracking-tight">
                IMD Emergency Warning Center
              </h2>
              <p className="text-xs text-slate-500 dark:text-slate-400">
                Official Warnings & Severe Weather Intelligence for {location.name || 'India'}
              </p>
            </div>
          </div>

          <button
            onClick={toggleEmergencyMode}
            className={`px-5 py-2.5 rounded-2xl font-extrabold text-xs tracking-wider uppercase transition-all shadow-lg border ${
              emergencyMode
                ? 'bg-red-600 hover:bg-red-700 text-white border-red-400 shadow-red-600/30'
                : 'bg-slate-100 dark:bg-slate-900 hover:bg-slate-200 dark:hover:bg-slate-800 text-saffron-600 dark:text-saffron-400 border-saffron-500/40'
            }`}
          >
            {emergencyMode ? 'DEACTIVATE EMERGENCY MODE' : 'ACTIVATE EMERGENCY INTELLIGENCE'}
          </button>
        </div>
      </div>

      {/* Filter Tabs */}
      <div className="flex items-center justify-between bg-slate-100 dark:bg-slate-900/80 p-2 rounded-2xl border border-slate-200 dark:border-slate-800 text-xs transition-colors">
        <div className="flex items-center space-x-2">
          <Filter className="w-4 h-4 text-slate-400 ml-2" />
          <span className="text-slate-500 dark:text-slate-400 font-semibold hidden sm:inline">Filter Severity:</span>
          <button
            onClick={() => setFilterSeverity('ALL')}
            className={`px-3 py-1.5 rounded-xl font-bold transition-colors ${
              filterSeverity === 'ALL' ? 'bg-slate-800 text-white dark:bg-slate-700' : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-200'
            }`}
          >
            All Warnings ({activeWarnings.length})
          </button>
          <button
            onClick={() => setFilterSeverity('RED')}
            className={`px-3 py-1.5 rounded-xl font-bold transition-colors ${
              filterSeverity === 'RED' ? 'bg-red-500 text-white' : 'text-red-600 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-950/40'
            }`}
          >
            RED Alert
          </button>
          <button
            onClick={() => setFilterSeverity('ORANGE')}
            className={`px-3 py-1.5 rounded-xl font-bold transition-colors ${
              filterSeverity === 'ORANGE' ? 'bg-saffron-500 text-white' : 'text-saffron-600 dark:text-saffron-400 hover:bg-saffron-50 dark:hover:bg-saffron-950/40'
            }`}
          >
            ORANGE Alert
          </button>
        </div>

        <span className="text-[11px] text-slate-400 mr-2">Authoritative Source: IMD</span>
      </div>

      {/* Warning Cards List */}
      <div className="space-y-4">
        {filteredWarnings.map((warn, idx) => (
          <div
            key={idx}
            className="glass-panel rounded-3xl p-6 border border-slate-200 dark:border-slate-800 space-y-4 relative overflow-hidden shadow-md dark:shadow-xl transition-colors"
          >
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-200 dark:border-slate-800/80 pb-3">
              <div className="flex items-center space-x-3">
                <span className={`px-3 py-1 rounded-xl text-xs font-black tracking-wider uppercase border ${getSeverityBadgeClass(warn.level)}`}>
                  {warn.level} ALERT
                </span>
                <h3 className="font-bold text-base text-slate-900 dark:text-white">{warn.category}</h3>
              </div>

              <div className="flex items-center space-x-2 text-xs text-slate-500 dark:text-slate-400">
                <Clock className="w-3.5 h-3.5" />
                <span>Issued: {warn.issued_at ? new Date(warn.issued_at).toLocaleTimeString() : 'Recent'}</span>
              </div>
            </div>

            <h4 className="font-semibold text-sm text-saffron-600 dark:text-saffron-400">{warn.headline}</h4>
            <p className="text-xs md:text-sm text-slate-700 dark:text-slate-300 leading-relaxed">{warn.description}</p>

            {/* Recommended Action Box */}
            <div className="p-4 rounded-2xl bg-slate-100 dark:bg-slate-900/90 border border-slate-200 dark:border-slate-800 space-y-1">
              <span className="text-xs font-bold text-emerald-600 dark:text-emerald-400 uppercase tracking-wider block">
                RECOMMENDED SAFETY ACTION
              </span>
              <p className="text-xs text-slate-800 dark:text-slate-200">{getRecommendedAction(warn.category)}</p>
            </div>

            <div className="flex items-center justify-between text-[11px] text-slate-500 dark:text-slate-400 pt-1">
              <span className="flex items-center space-x-1">
                <MapPin className="w-3.5 h-3.5 text-slate-400" />
                <span>Affected Location: {location.name || 'District Wide'}</span>
              </span>
              <span>Source: {warn.source}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
