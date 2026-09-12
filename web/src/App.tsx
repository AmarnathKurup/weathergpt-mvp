import React, { useState } from 'react';
import { AppProvider } from './context/AppContext';
import { AppShell } from './components/layout/AppShell';
import { WeatherHero } from './components/weather/WeatherHero';
import { HourlyForecastTimeline } from './components/weather/HourlyForecastTimeline';
import { DailyForecastList } from './components/weather/DailyForecastList';
import { WeatherGPTChat } from './components/chat/WeatherGPTChat';
import { GISMap } from './components/map/GISMap';
import { AlertCenter } from './components/alerts/AlertCenter';
import { ClimateAnalytics } from './components/climate/ClimateAnalytics';
import { ModelMatrix } from './components/models/ModelMatrix';
import { SavedLocations } from './components/locations/SavedLocations';
import { SettingsPanel } from './components/settings/SettingsPanel';

export const MainContent: React.FC = () => {
  const [activeTab, setActiveTab] = useState<string>('home');

  const renderActiveTab = () => {
    switch (activeTab) {
      case 'home':
        return (
          <div className="space-y-6">
            <WeatherHero />
            <HourlyForecastTimeline />
            <DailyForecastList />
          </div>
        );
      case 'map':
        return <GISMap />;
      case 'forecast':
        return (
          <div className="space-y-6">
            <DailyForecastList />
            <HourlyForecastTimeline />
            <ModelMatrix />
          </div>
        );
      case 'alerts':
        return <AlertCenter />;
      case 'chat':
        return <WeatherGPTChat />;
      case 'climate':
        return <ClimateAnalytics />;
      case 'saved':
        return <SavedLocations />;
      case 'settings':
        return <SettingsPanel />;
      default:
        return (
          <div className="space-y-6">
            <WeatherHero />
            <HourlyForecastTimeline />
          </div>
        );
    }
  };

  return (
    <AppShell activeTab={activeTab} setActiveTab={setActiveTab}>
      {renderActiveTab()}
    </AppShell>
  );
};

export function App() {
  return (
    <AppProvider>
      <MainContent />
    </AppProvider>
  );
}

export default App;
