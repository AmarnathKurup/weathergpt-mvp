import React, { useState } from 'react';
import { useApp } from '../../context/AppContext';
import {
  CloudSun,
  MapPin,
  Map as MapIcon,
  Calendar,
  AlertTriangle,
  MessageSquare,
  BarChart3,
  Bookmark,
  Settings,
  Search,
  Navigation,
  Globe,
  Sun,
  Moon,
  Volume2,
  VolumeX,
  Menu,
  X,
  ShieldAlert
} from 'lucide-react';

interface AppShellProps {
  activeTab: string;
  setActiveTab: (tab: string) => void;
  children: React.ReactNode;
}

export const AppShell: React.FC<AppShellProps> = ({ activeTab, setActiveTab, children }) => {
  const {
    settings,
    updateSettings,
    location,
    refreshWeather,
    useDeviceLocation,
    emergencyMode,
    toggleEmergencyMode,
    t
  } = useApp();

  const [searchInput, setSearchInput] = useState('');
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const navItems = [
    { id: 'home', label: t('home'), icon: CloudSun },
    { id: 'map', label: t('map'), icon: MapIcon },
    { id: 'forecast', label: t('forecast'), icon: Calendar },
    { id: 'alerts', label: t('alerts'), icon: AlertTriangle, badge: emergencyMode ? 'RED' : 'IMD' },
    { id: 'chat', label: t('weatherGpt'), icon: MessageSquare, highlight: true },
    { id: 'climate', label: t('climate'), icon: BarChart3 },
    { id: 'saved', label: t('savedLocations'), icon: Bookmark },
    { id: 'settings', label: t('settings'), icon: Settings }
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

  const handleSearchSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (searchInput.trim()) {
      refreshWeather(searchInput.trim());
      setSearchInput('');
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 dark:bg-navy-950 text-slate-900 dark:text-slate-100 flex flex-col md:flex-row transition-colors duration-200">
      {/* Sidebar - Desktop */}
      <aside className="hidden md:flex flex-col w-64 bg-white dark:bg-navy-900 border-r border-slate-200 dark:border-slate-800 p-4 shrink-0 justify-between min-h-screen sticky top-0 h-screen transition-colors duration-200">
        <div className="space-y-6">
          {/* Logo & Platform Name */}
          <div className="flex items-center space-x-3 px-2 py-1">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-saffron-500 to-amber-400 flex items-center justify-center shadow-lg shadow-saffron-500/20">
              <CloudSun className="w-6 h-6 text-navy-950 font-bold" />
            </div>
            <div>
              <h1 className="font-extrabold text-xl tracking-tight text-slate-900 dark:text-white flex items-center">
                Weather<span className="text-saffron-500">GPT</span>
              </h1>
              <span className="text-[10px] uppercase font-semibold text-slate-500 dark:text-slate-400 tracking-wider">India Weather Intelligence</span>
            </div>
          </div>

          {/* Navigation Links */}
          <nav className="space-y-1">
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = activeTab === item.id;
              return (
                <button
                  key={item.id}
                  onClick={() => setActiveTab(item.id)}
                  className={`w-full flex items-center justify-between px-3.5 py-2.5 rounded-xl font-medium text-sm transition-all ${
                    isActive
                      ? 'bg-saffron-500 text-white shadow-md shadow-saffron-500/20 font-semibold'
                      : item.highlight
                      ? 'bg-saffron-50 dark:bg-slate-800/80 text-saffron-600 dark:text-saffron-400 hover:bg-saffron-100 dark:hover:bg-slate-800 border border-saffron-500/30'
                      : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-100 hover:bg-slate-100 dark:hover:bg-slate-800/60'
                  }`}
                >
                  <div className="flex items-center space-x-3">
                    <Icon className={`w-5 h-5 ${isActive ? 'text-white' : item.highlight ? 'text-saffron-500' : 'text-slate-400'}`} />
                    <span>{item.label}</span>
                  </div>
                  {item.badge && (
                    <span className={`text-[10px] font-extrabold px-1.5 py-0.5 rounded ${
                      item.badge === 'RED' ? 'bg-red-500 text-white animate-pulse' : 'bg-slate-200 dark:bg-slate-700 text-slate-700 dark:text-slate-300'
                    }`}>
                      {item.badge}
                    </span>
                  )}
                </button>
              );
            })}
          </nav>
        </div>

        {/* Emergency Mode Switch & User Profile */}
        <div className="space-y-3 pt-4 border-t border-slate-200 dark:border-slate-800">
          <button
            onClick={toggleEmergencyMode}
            className={`w-full flex items-center justify-between px-3.5 py-2.5 rounded-xl text-xs font-bold transition-all border ${
              emergencyMode
                ? 'bg-red-50 dark:bg-red-950/80 text-red-700 dark:text-red-300 border-red-500 animate-pulse'
                : 'bg-slate-100 dark:bg-slate-900 text-slate-700 dark:text-slate-400 border-slate-200 dark:border-slate-800 hover:border-slate-300 dark:hover:border-slate-700'
            }`}
          >
            <div className="flex items-center space-x-2">
              <ShieldAlert className={`w-4 h-4 ${emergencyMode ? 'text-red-500' : 'text-slate-500'}`} />
              <span>EMERGENCY MODE</span>
            </div>
            <span className={`px-2 py-0.5 rounded text-[10px] ${emergencyMode ? 'bg-red-600 text-white' : 'bg-slate-200 dark:bg-slate-800 text-slate-700 dark:text-slate-400'}`}>
              {emergencyMode ? 'ON' : 'OFF'}
            </span>
          </button>

          <div className="px-3 py-2 rounded-xl bg-slate-100 dark:bg-slate-900/50 border border-slate-200 dark:border-slate-800 flex items-center space-x-3">
            <div className="w-8 h-8 rounded-full bg-saffron-500/20 text-saffron-600 dark:text-saffron-500 flex items-center justify-center font-bold text-xs">
              IN
            </div>
            <div className="text-xs truncate">
              <p className="font-semibold text-slate-900 dark:text-slate-200 truncate">{location.name || 'India Core'}</p>
              <p className="text-[10px] text-slate-500">PIN: {location.pincode || '700001'}</p>
            </div>
          </div>
        </div>
      </aside>

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col min-w-0">
        {/* Top Header */}
        <header className="sticky top-0 z-30 bg-white/90 dark:bg-navy-900/90 backdrop-blur-md border-b border-slate-200 dark:border-slate-800 px-4 py-3 flex items-center justify-between gap-3 transition-colors duration-200">
          {/* Mobile Logo & Menu Trigger */}
          <div className="flex items-center space-x-3 md:hidden">
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="p-2 rounded-lg bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 hover:text-slate-900 dark:hover:text-white"
            >
              {mobileMenuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
            </button>
            <div className="flex items-center space-x-2">
              <div className="w-8 h-8 rounded-lg bg-saffron-500 flex items-center justify-center">
                <CloudSun className="w-5 h-5 text-navy-950 font-bold" />
              </div>
              <span className="font-bold text-base text-slate-900 dark:text-white">Weather<span className="text-saffron-500">GPT</span></span>
            </div>
          </div>

          {/* Search Bar with PIN Code Lookup */}
          <form onSubmit={handleSearchSubmit} className="flex-1 max-w-md relative">
            <div className="relative flex items-center">
              <Search className="w-4 h-4 text-slate-400 absolute left-3 pointer-events-none" />
              <input
                type="text"
                value={searchInput}
                onChange={(e) => setSearchInput(e.target.value)}
                placeholder={t('searchPlaceholder')}
                className="w-full bg-slate-100 dark:bg-slate-900 border border-slate-200 dark:border-slate-700/80 focus:border-saffron-500 rounded-xl pl-9 pr-24 py-2 text-xs text-slate-900 dark:text-slate-100 placeholder-slate-400 dark:placeholder-slate-500 focus:outline-none transition-all"
              />
              <button
                type="button"
                onClick={useDeviceLocation}
                className="absolute right-1.5 flex items-center space-x-1 px-2.5 py-1 bg-slate-200 dark:bg-slate-800 hover:bg-slate-300 dark:hover:bg-slate-700 text-saffron-600 dark:text-saffron-400 rounded-lg text-[11px] font-medium transition-colors border border-slate-300 dark:border-slate-700"
                title="Use Geolocation"
              >
                <Navigation className="w-3 h-3" />
                <span className="hidden sm:inline">Location</span>
              </button>
            </div>
          </form>

          {/* Quick Header Controls (Language, Theme, ReadAloud) */}
          <div className="flex items-center space-x-2">
            {/* Language Dropdown */}
            <div className="relative flex items-center">
              <Globe className="w-4 h-4 text-slate-400 absolute left-2 pointer-events-none" />
              <select
                value={settings.language}
                onChange={(e) => updateSettings({ language: e.target.value })}
                className="bg-slate-100 dark:bg-slate-900 border border-slate-200 dark:border-slate-700 text-slate-800 dark:text-slate-200 text-xs rounded-xl pl-8 pr-3 py-1.5 focus:outline-none focus:border-saffron-500 font-medium cursor-pointer"
              >
                {languages.map((l) => (
                  <option key={l.code} value={l.code}>
                    {l.name}
                  </option>
                ))}
              </select>
            </div>

            {/* Theme Toggle */}
            <button
              onClick={() => updateSettings({ theme: settings.theme === 'dark' ? 'light' : 'dark' })}
              className="p-2 rounded-xl bg-slate-100 dark:bg-slate-900 border border-slate-200 dark:border-slate-700 text-slate-700 dark:text-slate-300 hover:text-saffron-500 transition-colors"
              title="Toggle Theme"
            >
              {settings.theme === 'dark' ? <Moon className="w-4 h-4" /> : <Sun className="w-4 h-4" />}
            </button>

            {/* Read Aloud Quick Switch */}
            <button
              onClick={() =>
                updateSettings({
                  accessibility: { ...settings.accessibility, readAloud: !settings.accessibility.readAloud }
                })
              }
              className={`p-2 rounded-xl border transition-colors ${
                settings.accessibility.readAloud
                  ? 'bg-saffron-500/20 border-saffron-500 text-saffron-600 dark:text-saffron-400'
                  : 'bg-slate-100 dark:bg-slate-900 border-slate-200 dark:border-slate-700 text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-200'
              }`}
              title="Toggle Read Aloud"
            >
              {settings.accessibility.readAloud ? <Volume2 className="w-4 h-4" /> : <VolumeX className="w-4 h-4" />}
            </button>
          </div>
        </header>

        {/* Mobile Navigation Menu overlay */}
        {mobileMenuOpen && (
          <div className="md:hidden bg-navy-900 border-b border-slate-800 p-4 space-y-2 animate-in slide-in-from-top duration-200">
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = activeTab === item.id;
              return (
                <button
                  key={item.id}
                  onClick={() => {
                    setActiveTab(item.id);
                    setMobileMenuOpen(false);
                  }}
                  className={`w-full flex items-center space-x-3 px-4 py-3 rounded-xl text-sm font-medium ${
                    isActive ? 'bg-saffron-500 text-white font-bold' : 'text-slate-300 hover:bg-slate-800'
                  }`}
                >
                  <Icon className="w-5 h-5" />
                  <span>{item.label}</span>
                </button>
              );
            })}
          </div>
        )}

        {/* Dynamic Page Content */}
        <main className="flex-1 p-4 md:p-6 max-w-[var(--max-content-width)] w-full mx-auto space-y-6">
          {children}
        </main>
      </div>
    </div>
  );
};
