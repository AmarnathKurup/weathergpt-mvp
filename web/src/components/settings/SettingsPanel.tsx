import React from 'react';
import { useApp } from '../../context/AppContext';
import {
  Settings as SettingsIcon,
  Sun,
  Moon,
  Monitor,
  Globe,
  Type,
  Maximize2,
  Volume2,
  Bell,
  UserCheck,
  ShieldCheck,
  Check
} from 'lucide-react';
import { FontSizeSetting, LineSpacingSetting, OccupationSetting } from '../../types';

export const SettingsPanel: React.FC = () => {
  const { settings, updateSettings, updateAccessibility, t } = useApp();

  const fontSizes: { id: FontSizeSetting; label: string }[] = [
    { id: 'small', label: 'Small (87.5%)' },
    { id: 'normal', label: 'Normal (100%)' },
    { id: 'large', label: 'Large (115%)' },
    { id: 'xlarge', label: 'Extra Large (130%)' }
  ];

  const lineSpacings: { id: LineSpacingSetting; label: string }[] = [
    { id: 'normal', label: 'Normal' },
    { id: 'comfortable', label: 'Comfortable' },
    { id: 'expanded', label: 'Expanded' }
  ];

  const occupations: { id: OccupationSetting; label: string }[] = [
    { id: 'general', label: 'General Public' },
    { id: 'student', label: '🎓 Student / Youth' },
    { id: 'farmer', label: '🌾 Farmer / Agriculture' },
    { id: 'fisherman', label: '⛵ Fisherman / Coastal Work' },
    { id: 'driver', label: '🚗 Driver / Logistics' },
    { id: 'delivery_worker', label: '🛵 Delivery Partner' },
    { id: 'senior_citizen', label: '👴 Senior Citizen' }
  ];

  const languages = [
    { code: 'en', name: 'English' },
    { code: 'hi', name: 'हिन्दी (Hindi)' },
    { code: 'bn', name: 'বাংলা (Bengali)' },
    { code: 'ta', name: 'தமிழ் (Tamil)' },
    { code: 'te', name: 'తెలుగు (Telugu)' },
    { code: 'mr', name: 'मराठी (Marathi)' },
    { code: 'gu', name: 'ગુજરાતી (Gujarati)' },
    { code: 'kn', name: 'ಕನ್ನಡ (Kannada)' },
    { code: 'ml', name: 'മലയാളം (Malayalam)' },
    { code: 'or', name: 'ଓଡ଼ିଆ (Odia)' },
    { code: 'pa', name: 'ਪੰਜਾਬੀ (Punjabi)' },
    { code: 'ur', name: 'اردو (Urdu)' }
  ];

  return (
    <div className="space-y-6 max-w-4xl mx-auto">
      {/* Header */}
      <div className="glass-panel rounded-3xl p-6 border border-slate-200 dark:border-slate-800 flex items-center justify-between transition-colors">
        <div className="flex items-center space-x-3">
          <div className="p-2.5 rounded-2xl bg-saffron-500/10 text-saffron-600 dark:text-saffron-500 border border-saffron-500/20">
            <SettingsIcon className="w-6 h-6" />
          </div>
          <div>
            <h2 className="text-xl font-bold text-slate-900 dark:text-white">{t('settings')}</h2>
            <p className="text-xs text-slate-500 dark:text-slate-400">System Preferences, Localization & Accessibility Engine</p>
          </div>
        </div>
      </div>

      {/* 1. Theme System */}
      <div className="glass-panel rounded-3xl p-6 border border-slate-200 dark:border-slate-800 space-y-4 transition-colors">
        <h3 className="font-bold text-sm text-slate-900 dark:text-white flex items-center gap-2">
          <Sun className="w-4 h-4 text-saffron-500" />
          <span>{t('appearance')}</span>
        </h3>

        <div className="grid grid-cols-3 gap-3">
          <button
            onClick={() => updateSettings({ theme: 'system' })}
            className={`p-4 rounded-2xl border flex flex-col items-center space-y-2 transition-all ${
              settings.theme === 'system'
                ? 'bg-saffron-500/15 border-saffron-500 text-saffron-600 dark:text-saffron-400 font-bold'
                : 'bg-slate-100 dark:bg-slate-900/60 border-slate-200 dark:border-slate-800 text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-200'
            }`}
          >
            <Monitor className="w-5 h-5" />
            <span className="text-xs">{t('themeSystem')}</span>
          </button>

          <button
            onClick={() => updateSettings({ theme: 'light' })}
            className={`p-4 rounded-2xl border flex flex-col items-center space-y-2 transition-all ${
              settings.theme === 'light'
                ? 'bg-saffron-500/15 border-saffron-500 text-saffron-600 dark:text-saffron-400 font-bold'
                : 'bg-slate-100 dark:bg-slate-900/60 border-slate-200 dark:border-slate-800 text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-200'
            }`}
          >
            <Sun className="w-5 h-5" />
            <span className="text-xs">{t('themeLight')}</span>
          </button>

          <button
            onClick={() => updateSettings({ theme: 'dark' })}
            className={`p-4 rounded-2xl border flex flex-col items-center space-y-2 transition-all ${
              settings.theme === 'dark'
                ? 'bg-saffron-500/15 border-saffron-500 text-saffron-600 dark:text-saffron-400 font-bold'
                : 'bg-slate-100 dark:bg-slate-900/60 border-slate-200 dark:border-slate-800 text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-200'
            }`}
          >
            <Moon className="w-5 h-5" />
            <span className="text-xs">{t('themeDark')}</span>
          </button>
        </div>
      </div>

      {/* 2. Accessibility Controls */}
      <div className="glass-panel rounded-3xl p-6 border border-slate-200 dark:border-slate-800 space-y-6 transition-colors">
        <h3 className="font-bold text-sm text-slate-900 dark:text-white flex items-center gap-2">
          <Type className="w-4 h-4 text-saffron-500" />
          <span>{t('accessibility')}</span>
        </h3>

        {/* Text Scaling */}
        <div className="space-y-2">
          <span className="text-xs font-semibold text-slate-700 dark:text-slate-300 block">{t('textSize')} (Global Font Scale)</span>
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-2">
            {fontSizes.map((f) => (
              <button
                key={f.id}
                onClick={() => updateAccessibility({ textSize: f.id })}
                className={`py-2.5 px-3 rounded-xl border text-xs font-semibold transition-all ${
                  settings.accessibility.textSize === f.id
                    ? 'bg-saffron-500 text-white border-saffron-500 shadow-md shadow-saffron-500/20'
                    : 'bg-slate-100 dark:bg-slate-900 border-slate-200 dark:border-slate-800 text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white'
                }`}
              >
                {f.label}
              </button>
            ))}
          </div>
        </div>

        {/* Line Spacing */}
        <div className="space-y-2">
          <span className="text-xs font-semibold text-slate-700 dark:text-slate-300 block">{t('lineSpacing')}</span>
          <div className="grid grid-cols-3 gap-2">
            {lineSpacings.map((l) => (
              <button
                key={l.id}
                onClick={() => updateAccessibility({ lineSpacing: l.id })}
                className={`py-2.5 px-3 rounded-xl border text-xs font-semibold transition-all ${
                  settings.accessibility.lineSpacing === l.id
                    ? 'bg-saffron-500 text-white border-saffron-500'
                    : 'bg-slate-100 dark:bg-slate-900 border-slate-200 dark:border-slate-800 text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white'
                }`}
              >
                {l.label}
              </button>
            ))}
          </div>
        </div>

        {/* High Contrast & Read Aloud Switches */}
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-2">
          <div className="p-4 rounded-2xl bg-slate-100 dark:bg-slate-900/60 border border-slate-200 dark:border-slate-800 flex items-center justify-between">
            <div>
              <span className="text-xs font-bold text-slate-900 dark:text-white block">{t('highContrast')}</span>
              <span className="text-[11px] text-slate-500 dark:text-slate-400">Pure black/white high contrast</span>
            </div>
            <button
              onClick={() => updateAccessibility({ highContrast: !settings.accessibility.highContrast })}
              className={`w-12 h-6 rounded-full transition-colors relative p-1 ${
                settings.accessibility.highContrast ? 'bg-saffron-500' : 'bg-slate-300 dark:bg-slate-800'
              }`}
            >
              <div
                className={`w-4 h-4 rounded-full bg-white transition-transform ${
                  settings.accessibility.highContrast ? 'translate-x-6' : 'translate-x-0'
                }`}
              />
            </button>
          </div>

          <div className="p-4 rounded-2xl bg-slate-100 dark:bg-slate-900/60 border border-slate-200 dark:border-slate-800 flex items-center justify-between">
            <div>
              <span className="text-xs font-bold text-slate-900 dark:text-white block">{t('readAloud')}</span>
              <span className="text-[11px] text-slate-500 dark:text-slate-400">Auto voice synthesis for AI answers</span>
            </div>
            <button
              onClick={() => updateAccessibility({ readAloud: !settings.accessibility.readAloud })}
              className={`w-12 h-6 rounded-full transition-colors relative p-1 ${
                settings.accessibility.readAloud ? 'bg-saffron-500' : 'bg-slate-300 dark:bg-slate-800'
              }`}
            >
              <div
                className={`w-4 h-4 rounded-full bg-white transition-transform ${
                  settings.accessibility.readAloud ? 'translate-x-6' : 'translate-x-0'
                }`}
              />
            </button>
          </div>
        </div>
      </div>

      {/* 3. Occupation Profile */}
      <div className="glass-panel rounded-3xl p-6 border border-slate-200 dark:border-slate-800 space-y-4 transition-colors">
        <h3 className="font-bold text-sm text-slate-900 dark:text-white flex items-center gap-2">
          <UserCheck className="w-4 h-4 text-saffron-500" />
          <span>{t('occupation')}</span>
        </h3>

        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-2">
          {occupations.map((o) => (
            <button
              key={o.id}
              onClick={() => updateSettings({ occupation: o.id })}
              className={`p-3 rounded-2xl border text-left text-xs font-semibold transition-all ${
                settings.occupation === o.id
                  ? 'bg-saffron-500/20 border-saffron-500 text-saffron-700 dark:text-saffron-400'
                  : 'bg-slate-100 dark:bg-slate-900/60 border-slate-200 dark:border-slate-800 text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-200'
              }`}
            >
              {o.label}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
};
