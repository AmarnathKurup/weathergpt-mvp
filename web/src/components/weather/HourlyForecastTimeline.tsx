import React from 'react';
import { useApp } from '../../context/AppContext';
import { CloudRain, Sun, Cloud, Wind, Thermometer } from 'lucide-react';

export const HourlyForecastTimeline: React.FC = () => {
  const { forecast, t } = useApp();

  const hourlyItems = forecast?.hourly && forecast.hourly.length > 0
    ? forecast.hourly
    : [
        { time: '14:00', temperature: 32, rain_probability: 30, rain_mm: 0, wind_speed: 12, weather_code: 1, weather_desc: 'Partly Cloudy' },
        { time: '15:00', temperature: 33, rain_probability: 40, rain_mm: 0.5, wind_speed: 14, weather_code: 2, weather_desc: 'Humid' },
        { time: '16:00', temperature: 31, rain_probability: 60, rain_mm: 3.2, wind_speed: 18, weather_code: 61, weather_desc: 'Overcast' },
        { time: '17:00', temperature: 28, rain_probability: 78, rain_mm: 14.2, wind_speed: 22, weather_code: 63, weather_desc: 'Heavy Rain' },
        { time: '18:00', temperature: 27, rain_probability: 85, rain_mm: 18.0, wind_speed: 25, weather_code: 95, weather_desc: 'Thunderstorm' },
        { time: '19:00', temperature: 26, rain_probability: 70, rain_mm: 8.5, wind_speed: 19, weather_code: 61, weather_desc: 'Moderate Rain' },
        { time: '20:00', temperature: 26, rain_probability: 40, rain_mm: 1.2, wind_speed: 15, weather_code: 3, weather_desc: 'Passing Shower' },
        { time: '21:00', temperature: 25, rain_probability: 20, rain_mm: 0, wind_speed: 10, weather_code: 1, weather_desc: 'Cloudy Breaks' },
      ];

  const getWeatherIcon = (prob: number, code: number) => {
    if (prob >= 70 || code >= 60) return <CloudRain className="w-5 h-5 text-sky-400" />;
    if (prob >= 30) return <Cloud className="w-5 h-5 text-slate-300" />;
    return <Sun className="w-5 h-5 text-amber-400" />;
  };

  return (
    <div className="glass-panel rounded-3xl p-6 border border-slate-200 dark:border-slate-800 space-y-4 transition-colors duration-200">
      <div className="flex items-center justify-between">
        <h3 className="font-bold text-base text-slate-900 dark:text-white flex items-center gap-2">
          <Thermometer className="w-4 h-4 text-saffron-500" />
          <span>{t('hourlyForecast')}</span>
        </h3>
        <span className="text-xs text-slate-500 dark:text-slate-400">Next 24 Hours</span>
      </div>

      <div className="flex space-x-3 overflow-x-auto pb-2 pt-1 scrollbar-thin">
        {hourlyItems.map((item, idx) => {
          const isPeakRain = item.rain_probability >= 75;
          return (
            <div
              key={idx}
              className={`flex-none w-24 p-3 rounded-2xl border text-center space-y-2 transition-all ${
                isPeakRain
                  ? 'bg-sky-50 dark:bg-sky-950/60 border-sky-300 dark:border-sky-500/60 shadow-md'
                  : 'bg-slate-100/80 dark:bg-slate-900/60 border-slate-200 dark:border-slate-800/80 hover:border-slate-300 dark:hover:border-slate-700'
              }`}
            >
              <span className="text-xs font-semibold text-slate-500 dark:text-slate-400 block">{item.time}</span>
              <div className="flex justify-center my-1">
                {getWeatherIcon(item.rain_probability, item.weather_code)}
              </div>
              <span className="text-base font-bold text-slate-900 dark:text-white block">{Math.round(item.temperature)}°C</span>
              <div className="text-[11px] font-semibold text-sky-600 dark:text-sky-400">
                {item.rain_probability}%
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
