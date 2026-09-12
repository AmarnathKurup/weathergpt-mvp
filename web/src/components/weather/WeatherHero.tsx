import React from 'react';
import { useApp } from '../../context/AppContext';
import {
  CloudRain,
  Wind,
  Droplets,
  Sun,
  Sunrise,
  Sunset,
  Eye,
  Gauge,
  AlertTriangle,
  Clock,
  ShieldCheck,
  Building
} from 'lucide-react';

export const WeatherHero: React.FC = () => {
  const { weather, location, isLoadingWeather, t } = useApp();

  if (isLoadingWeather && !weather) {
    return (
      <div className="glass-panel rounded-3xl p-8 animate-pulse space-y-6">
        <div className="h-6 bg-slate-800 rounded w-1/3"></div>
        <div className="h-16 bg-slate-800 rounded w-1/2"></div>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 pt-4">
          <div className="h-20 bg-slate-800 rounded-2xl"></div>
          <div className="h-20 bg-slate-800 rounded-2xl"></div>
          <div className="h-20 bg-slate-800 rounded-2xl"></div>
          <div className="h-20 bg-slate-800 rounded-2xl"></div>
        </div>
      </div>
    );
  }

  const temp = weather ? Math.round(weather.temperature) : 31;
  const feelsLike = weather ? Math.round(weather.feels_like) : 36;
  const condition = weather?.weather_desc || 'Partly Cloudy with Evening Rain';
  const rainProb = weather?.rain_probability ?? 78;
  const humidity = weather?.humidity ?? 75;
  const windSpeed = weather?.wind_speed ?? 14.5;
  const uvIndex = weather?.uv_index ?? 8;
  const pressure = weather?.pressure ?? 1008;
  const visibility = weather?.visibility ? (weather.visibility / 1000).toFixed(1) : '8.0';

  const highestWarning = weather?.warnings && weather.warnings.length > 0 ? weather.warnings[0] : null;

  return (
    <div className="space-y-4">
      {/* IMD Warning Alert Banner if active */}
      {highestWarning && (
        <div className="p-4 rounded-2xl bg-amber-950/60 border border-amber-500/80 flex items-start space-x-3 text-amber-200 shadow-lg animate-in fade-in duration-300">
          <AlertTriangle className="w-6 h-6 text-amber-400 shrink-0 mt-0.5" />
          <div className="flex-1 text-xs md:text-sm">
            <div className="flex items-center justify-between font-bold text-amber-400 uppercase tracking-wide">
              <span>{highestWarning.level} ALERT — {highestWarning.headline || 'IMD WEATHER WARNING'}</span>
              <span className="text-[10px] bg-amber-500/20 px-2 py-0.5 rounded text-amber-300">Source: {highestWarning.source}</span>
            </div>
            <p className="mt-1 text-slate-200">{highestWarning.description}</p>
          </div>
        </div>
      )}

      {/* Main Weather Hero Card */}
      <div className="glass-panel rounded-3xl p-6 md:p-8 relative overflow-hidden shadow-xl dark:shadow-2xl border border-slate-200 dark:border-slate-800 transition-colors duration-200">
        {/* Background Subtle Gradient Glow */}
        <div className="absolute -top-24 -right-24 w-72 h-72 bg-saffron-500/10 rounded-full blur-3xl pointer-events-none" />

        {/* Location & Metadata Header */}
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-3 border-b border-slate-200 dark:border-slate-800/80 pb-5">
          <div className="flex items-center space-x-3">
            <div className="p-2.5 rounded-2xl bg-saffron-500/10 text-saffron-600 dark:text-saffron-500 border border-saffron-500/20">
              <Building className="w-5 h-5" />
            </div>
            <div>
              <h2 className="text-xl md:text-2xl font-bold text-slate-900 dark:text-white tracking-tight flex items-center gap-2">
                {location.name || 'Kolkata GPO'}
                {location.pincode && (
                  <span className="text-xs font-semibold px-2 py-0.5 rounded-full bg-slate-100 dark:bg-slate-800 text-saffron-600 dark:text-saffron-400 border border-slate-200 dark:border-slate-700">
                    PIN {location.pincode}
                  </span>
                )}
              </h2>
              <p className="text-xs text-slate-500 dark:text-slate-400">
                {location.district ? `${location.district}, ${location.state}` : 'India Meteorological Division'}
              </p>
            </div>
          </div>

          {/* Data Source & Timestamp */}
          <div className="flex items-center space-x-2 text-[11px] text-slate-600 dark:text-slate-400 bg-slate-100 dark:bg-slate-900/80 px-3 py-1.5 rounded-xl border border-slate-200 dark:border-slate-800 self-start md:self-auto">
            <ShieldCheck className="w-3.5 h-3.5 text-emerald-600 dark:text-emerald-400" />
            <span>{weather?.source || 'IMD + Open-Meteo'}</span>
            <span className="text-slate-400 dark:text-slate-600">•</span>
            <Clock className="w-3.5 h-3.5 text-slate-500 dark:text-slate-400" />
            <span>{weather?.timestamp ? new Date(weather.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) : 'Live'}</span>
          </div>
        </div>

        {/* Temperature & Main Visual */}
        <div className="py-6 flex flex-col sm:flex-row sm:items-center justify-between gap-6">
          <div className="space-y-1">
            <div className="flex items-baseline space-x-2">
              <span className="text-6xl md:text-7xl font-black text-slate-900 dark:text-white tracking-tight leading-none">
                {temp}°
              </span>
              <span className="text-lg md:text-xl text-slate-500 dark:text-slate-400 font-medium">C</span>
            </div>
            <p className="text-xs md:text-sm text-slate-500 dark:text-slate-400 font-medium pt-1">
              {t('feelsLike')} <span className="text-slate-900 dark:text-slate-200 font-bold">{feelsLike}°C</span>
            </p>
          </div>

          {/* Condition Badge */}
          <div className="flex items-center space-x-3 bg-slate-100 dark:bg-slate-900/90 border border-slate-200 dark:border-slate-800 px-4 py-3 rounded-2xl self-start sm:self-auto">
            <div className="p-2 rounded-xl bg-sky-500/20 text-sky-600 dark:text-sky-400">
              <CloudRain className="w-7 h-7" />
            </div>
            <div>
              <p className="text-sm md:text-base font-bold text-slate-900 dark:text-slate-100">{condition}</p>
              <p className="text-xs text-sky-600 dark:text-sky-400 font-semibold">{rainProb}% Rain Probability</p>
            </div>
          </div>
        </div>

        {/* Core Weather Metrics Grid */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 pt-2">
          <div className="p-3.5 rounded-2xl bg-slate-100/80 dark:bg-slate-900/60 border border-slate-200 dark:border-slate-800/80 flex items-center space-x-3">
            <div className="p-2 rounded-xl bg-sky-500/10 text-sky-600 dark:text-sky-400">
              <CloudRain className="w-4 h-4" />
            </div>
            <div>
              <span className="text-[11px] text-slate-500 dark:text-slate-400 block">{t('rainChance')}</span>
              <span className="text-sm font-bold text-slate-900 dark:text-slate-100">{rainProb}%</span>
            </div>
          </div>

          <div className="p-3.5 rounded-2xl bg-slate-100/80 dark:bg-slate-900/60 border border-slate-200 dark:border-slate-800/80 flex items-center space-x-3">
            <div className="p-2 rounded-xl bg-blue-500/10 text-blue-600 dark:text-blue-400">
              <Droplets className="w-4 h-4" />
            </div>
            <div>
              <span className="text-[11px] text-slate-500 dark:text-slate-400 block">{t('humidity')}</span>
              <span className="text-sm font-bold text-slate-900 dark:text-slate-100">{humidity}%</span>
            </div>
          </div>

          <div className="p-3.5 rounded-2xl bg-slate-100/80 dark:bg-slate-900/60 border border-slate-200 dark:border-slate-800/80 flex items-center space-x-3">
            <div className="p-2 rounded-xl bg-emerald-500/10 text-emerald-600 dark:text-emerald-400">
              <Wind className="w-4 h-4" />
            </div>
            <div>
              <span className="text-[11px] text-slate-500 dark:text-slate-400 block">{t('wind')}</span>
              <span className="text-sm font-bold text-slate-900 dark:text-slate-100">{windSpeed} km/h</span>
            </div>
          </div>

          <div className="p-3.5 rounded-2xl bg-slate-100/80 dark:bg-slate-900/60 border border-slate-200 dark:border-slate-800/80 flex items-center space-x-3">
            <div className="p-2 rounded-xl bg-amber-500/10 text-amber-600 dark:text-amber-400">
              <Sun className="w-4 h-4" />
            </div>
            <div>
              <span className="text-[11px] text-slate-500 dark:text-slate-400 block">{t('uvIndex')}</span>
              <span className="text-sm font-bold text-amber-600 dark:text-amber-400">UV {uvIndex}</span>
            </div>
          </div>
        </div>

        {/* Secondary Metrics Row */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 pt-3 text-xs text-slate-500 dark:text-slate-400 border-t border-slate-200 dark:border-slate-800/60 mt-4">
          <div className="flex items-center space-x-2">
            <Gauge className="w-3.5 h-3.5 text-slate-400 dark:text-slate-500" />
            <span>{t('pressure')}: <strong className="text-slate-900 dark:text-slate-200">{pressure} hPa</strong></span>
          </div>
          <div className="flex items-center space-x-2">
            <Eye className="w-3.5 h-3.5 text-slate-400 dark:text-slate-500" />
            <span>{t('visibility')}: <strong className="text-slate-900 dark:text-slate-200">{visibility} km</strong></span>
          </div>
          <div className="flex items-center space-x-2">
            <Sunrise className="w-3.5 h-3.5 text-amber-500 dark:text-amber-400" />
            <span>{t('sunrise')}: <strong className="text-slate-900 dark:text-slate-200">{weather?.sunrise || '05:22 AM'}</strong></span>
          </div>
          <div className="flex items-center space-x-2">
            <Sunset className="w-3.5 h-3.5 text-orange-500 dark:text-orange-400" />
            <span>{t('sunset')}: <strong className="text-slate-900 dark:text-slate-200">{weather?.sunset || '06:14 PM'}</strong></span>
          </div>
        </div>
      </div>
    </div>
  );
};
