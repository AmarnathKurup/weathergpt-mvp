import React from 'react';
import { useApp } from '../../context/AppContext';
import { Calendar, CloudRain, Sun, Cloud, AlertCircle } from 'lucide-react';

export const DailyForecastList: React.FC = () => {
  const { forecast, t } = useApp();

  const dailyItems = forecast?.daily && forecast.daily.length > 0
    ? forecast.daily
    : [
        { date: 'Today', temp_max: 33, temp_min: 26, rain_probability: 78, precipitation_sum: 15.2, weather_code: 63, weather_desc: 'Thunderstorm Evening', uv_index_max: 8.5 },
        { date: 'Tomorrow', temp_max: 32, temp_min: 25, rain_probability: 65, precipitation_sum: 8.4, weather_code: 61, weather_desc: 'Moderate Rain', uv_index_max: 7.0 },
        { date: 'Thursday', temp_max: 34, temp_min: 27, rain_probability: 30, precipitation_sum: 1.2, weather_code: 2, weather_desc: 'Partly Sunny', uv_index_max: 9.0 },
        { date: 'Friday', temp_max: 35, temp_min: 28, rain_probability: 20, precipitation_sum: 0, weather_code: 1, weather_desc: 'Hot & Humid', uv_index_max: 9.5 },
        { date: 'Saturday', temp_max: 31, temp_min: 26, rain_probability: 80, precipitation_sum: 22.0, weather_code: 95, weather_desc: 'Heavy Monsoonal Rain', uv_index_max: 6.0 },
        { date: 'Sunday', temp_max: 30, temp_min: 25, rain_probability: 70, precipitation_sum: 12.0, weather_code: 61, weather_desc: 'Scattered Showers', uv_index_max: 6.5 },
        { date: 'Monday', temp_max: 32, temp_min: 26, rain_probability: 40, precipitation_sum: 3.5, weather_code: 2, weather_desc: 'Cloudy Breaks', uv_index_max: 8.0 }
      ];

  const getWeatherIcon = (prob: number) => {
    if (prob >= 70) return <CloudRain className="w-5 h-5 text-sky-400" />;
    if (prob >= 40) return <Cloud className="w-5 h-5 text-slate-300" />;
    return <Sun className="w-5 h-5 text-amber-400" />;
  };

  return (
    <div className="glass-panel rounded-3xl p-6 border border-slate-200 dark:border-slate-800 space-y-4 transition-colors duration-200">
      <div className="flex items-center justify-between">
        <h3 className="font-bold text-base text-slate-900 dark:text-white flex items-center gap-2">
          <Calendar className="w-4 h-4 text-saffron-500" />
          <span>{t('dailyForecast')}</span>
        </h3>
        <span className="text-xs text-slate-500 dark:text-slate-400">7-Day Horizon</span>
      </div>

      <div className="space-y-2.5">
        {dailyItems.map((item, idx) => (
          <div
            key={idx}
            className="flex items-center justify-between p-3.5 rounded-2xl bg-slate-100/80 dark:bg-slate-900/60 border border-slate-200 dark:border-slate-800/80 hover:border-slate-300 dark:hover:border-slate-700 transition-colors"
          >
            <div className="w-28 flex items-center space-x-2">
              {getWeatherIcon(item.rain_probability)}
              <span className="font-bold text-sm text-slate-900 dark:text-slate-100">{item.date}</span>
            </div>

            <div className="flex-1 px-4 hidden sm:block">
              <span className="text-xs text-slate-500 dark:text-slate-400 block truncate">{item.weather_desc}</span>
            </div>

            <div className="w-24 text-right">
              <span className="text-xs font-semibold text-sky-600 dark:text-sky-400">{item.rain_probability}% Rain</span>
            </div>

            <div className="w-32 flex items-center justify-end space-x-2 font-bold text-sm">
              <span className="text-slate-900 dark:text-slate-100">{Math.round(item.temp_max)}°</span>
              <div className="w-12 h-1.5 rounded-full bg-slate-200 dark:bg-slate-800 overflow-hidden hidden xs:block">
                <div
                  className="h-full bg-gradient-to-r from-sky-400 to-saffron-500 rounded-full"
                  style={{ width: `${Math.min(100, Math.max(20, item.temp_max * 2.5))}%` }}
                />
              </div>
              <span className="text-slate-400 dark:text-slate-500 text-xs">{Math.round(item.temp_min)}°</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
