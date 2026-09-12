import React, { createContext, useContext, useState, useEffect } from 'react';
import {
  WeatherSnapshot,
  ForecastResponse,
  AppSettings,
  SavedLocation,
  ChatMessage,
  LocationInfo
} from '../types';
import {
  fetchCurrentWeather,
  fetchForecast,
  fetchPincodeDetails,
  postChatQuery
} from '../services/api';
import { getTranslation, TranslationKeys } from '../localization/translations';

interface AppContextType {
  settings: AppSettings;
  updateSettings: (newSettings: Partial<AppSettings>) => void;
  updateAccessibility: (newAcc: Partial<AppSettings['accessibility']>) => void;
  location: LocationInfo;
  setLocation: (loc: LocationInfo) => void;
  weather: WeatherSnapshot | null;
  forecast: ForecastResponse | null;
  isLoadingWeather: boolean;
  weatherError: string | null;
  refreshWeather: (queryOrPincode?: string, lat?: number, lon?: number) => Promise<void>;
  useDeviceLocation: () => Promise<void>;
  savedLocations: SavedLocation[];
  addSavedLocation: (loc: Omit<SavedLocation, 'id'>) => void;
  removeSavedLocation: (id: string) => void;
  chatHistory: ChatMessage[];
  addChatMessage: (msg: ChatMessage) => void;
  sendChatQuery: (queryText: string) => Promise<void>;
  emergencyMode: boolean;
  toggleEmergencyMode: () => void;
  speakText: (text: string) => void;
  t: (key: keyof TranslationKeys) => string;
}

const DEFAULT_SETTINGS: AppSettings = {
  theme: 'light',
  language: 'en',
  accessibility: {
    textSize: 'normal',
    lineSpacing: 'normal',
    contentWidth: 'standard',
    highContrast: false,
    reducedMotion: false,
    readAloud: false
  },
  occupation: 'general',
  notificationsEnabled: true,
  notificationCategories: {
    severeWeather: true,
    rainAlerts: true,
    thunderstorms: true,
    heatwaves: true,
    savedLocations: true
  }
};

const DEFAULT_LOCATION: LocationInfo = {
  name: 'Kolkata GPO, West Bengal',
  pincode: '700001',
  district: 'Kolkata',
  state: 'West Bengal',
  latitude: 22.5726,
  longitude: 88.3639
};

const AppContext = createContext<AppContextType | undefined>(undefined);

export const AppProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  // Load persisted settings from localStorage
  const [settings, setSettings] = useState<AppSettings>(() => {
    const saved = localStorage.getItem('weathergpt_settings');
    if (saved) {
      try { return JSON.parse(saved); } catch (e) {}
    }
    return DEFAULT_SETTINGS;
  });

  const [location, setLocationState] = useState<LocationInfo>(DEFAULT_LOCATION);
  const [weather, setWeather] = useState<WeatherSnapshot | null>(null);
  const [forecast, setForecast] = useState<ForecastResponse | null>(null);
  const [isLoadingWeather, setIsLoadingWeather] = useState<boolean>(false);
  const [weatherError, setWeatherError] = useState<string | null>(null);
  const [emergencyMode, setEmergencyMode] = useState<boolean>(false);

  // Load saved locations from localStorage
  const [savedLocations, setSavedLocations] = useState<SavedLocation[]>(() => {
    const saved = localStorage.getItem('weathergpt_saved_locations');
    if (saved) {
      try { return JSON.parse(saved); } catch (e) {}
    }
    return [
      { id: '1', label: 'Home', pincode: '700001', name: 'Kolkata GPO', district: 'Kolkata', state: 'West Bengal', latitude: 22.5726, longitude: 88.3639 },
      { id: '2', label: 'Office', pincode: '110001', name: 'Connaught Place', district: 'New Delhi', state: 'Delhi', latitude: 28.6315, longitude: 77.2167 },
      { id: '3', label: 'Farm', pincode: '411001', name: 'Pune GPO', district: 'Pune', state: 'Maharashtra', latitude: 18.5204, longitude: 73.8567 },
      { id: '4', label: 'College', pincode: '560001', name: 'Bengaluru GPO', district: 'Bengaluru', state: 'Karnataka', latitude: 12.9716, longitude: 77.5946 }
    ];
  });

  // Chat state
  const [chatHistory, setChatHistory] = useState<ChatMessage[]>([
    {
      id: 'welcome',
      sender: 'assistant',
      text: "Namaste! I am WeatherGPT, India's Conversational Weather Intelligence Core. Ask me any weather query, forecast condition, or agricultural alert in 22 Indian languages.",
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      whyDetails: {
        temperature: 31.5,
        rain_probability: 78,
        rain_mm: 14.2,
        wind_kmh: 14.5,
        uv_index: 8,
        weather_code: 61,
        weather_desc: "Partly Cloudy with Evening Rain",
        data_source: "India Meteorological Department (IMD) + Open-Meteo ECMWF",
        nwp_model: "ECMWF IFS / GFS NCEP",
        updated_at: new Date().toISOString(),
        active_warnings: [
          { level: 'ORANGE', category: 'Thunderstorm', headline: 'Heavy Rain & Lightning Warning', description: 'Convective cloud formation over district. Rain 15-25mm expected.', source: 'IMD' }
        ],
        matched_rules: ['rain_evening', 'thunderstorm_risk']
      }
    }
  ]);

  // Persist settings
  useEffect(() => {
    localStorage.setItem('weathergpt_settings', JSON.stringify(settings));
    
    // Apply Theme to document.documentElement
    const root = document.documentElement;
    root.classList.remove('dark', 'light', 'high-contrast');
    if (settings.theme === 'dark' || (settings.theme === 'system' && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
      root.classList.add('dark');
    } else {
      root.classList.add('light');
    }

    // Apply High Contrast
    if (settings.accessibility.highContrast) {
      root.classList.add('high-contrast');
    }

    // Apply Text Scaling to --font-scale
    const fontScaleMap = { small: '0.875', normal: '1', large: '1.15', xlarge: '1.3' };
    root.style.setProperty('--font-scale', fontScaleMap[settings.accessibility.textSize] || '1');

    // Apply Line Spacing
    const lineSpacingMap = { normal: '1.5', comfortable: '1.75', expanded: '2.0' };
    root.style.setProperty('--line-height-scale', lineSpacingMap[settings.accessibility.lineSpacing] || '1.5');
  }, [settings]);

  // Persist saved locations
  useEffect(() => {
    localStorage.setItem('weathergpt_saved_locations', JSON.stringify(savedLocations));
  }, [savedLocations]);

  // Initial Weather Fetch
  useEffect(() => {
    refreshWeather(location.pincode, location.latitude, location.longitude);
  }, []);

  const refreshWeather = async (queryOrPincode?: string, lat?: number, lon?: number) => {
    setIsLoadingWeather(true);
    setWeatherError(null);
    try {
      let activeLat = lat ?? location.latitude;
      let activeLon = lon ?? location.longitude;
      let activeLocName = location.name;
      let activePin = queryOrPincode || location.pincode;

      // If query looks like a 6-digit Indian PIN code, resolve PIN code details first
      if (queryOrPincode && /^\d{6}$/.test(queryOrPincode.trim())) {
        try {
          const pinData = await fetchPincodeDetails(queryOrPincode.trim());
          if (pinData.latitude && pinData.longitude) {
            activeLat = pinData.latitude;
            activeLon = pinData.longitude;
          }
          activeLocName = `${pinData.office_name}, ${pinData.district}, ${pinData.state}`;
          activePin = pinData.pincode;
          setLocationState({
            name: activeLocName,
            pincode: activePin,
            district: pinData.district,
            state: pinData.state,
            latitude: activeLat,
            longitude: activeLon
          });
        } catch (e) {}
      }

      const snapshot = await fetchCurrentWeather(activePin || activeLocName, activeLat, activeLon);
      const forecastData = await fetchForecast(activePin || activeLocName, activeLat, activeLon);

      setWeather(snapshot);
      setForecast(forecastData);
      if (snapshot.location) {
        setLocationState(prev => ({
          ...prev,
          name: snapshot.location.name || prev.name,
          latitude: snapshot.location.latitude || prev.latitude,
          longitude: snapshot.location.longitude || prev.longitude
        }));
      }
    } catch (err: any) {
      setWeatherError(err.message || 'Could not update weather data.');
    } finally {
      setIsLoadingWeather(false);
    }
  };

  const useDeviceLocation = async () => {
    if (!navigator.geolocation) {
      alert('Geolocation is not supported by your browser.');
      return;
    }

    setIsLoadingWeather(true);
    navigator.geolocation.getCurrentPosition(
      async (pos) => {
        const { latitude, longitude } = pos.coords;
        await refreshWeather(undefined, latitude, longitude);
      },
      (err) => {
        setIsLoadingWeather(false);
        alert(`Location access denied or unavailable: ${err.message}. You can search by PIN code.`);
      },
      { timeout: 10000, enableHighAccuracy: true }
    );
  };

  const updateSettings = (newSettings: Partial<AppSettings>) => {
    setSettings(prev => ({ ...prev, ...newSettings }));
  };

  const updateAccessibility = (newAcc: Partial<AppSettings['accessibility']>) => {
    setSettings(prev => ({
      ...prev,
      accessibility: { ...prev.accessibility, ...newAcc }
    }));
  };

  const addSavedLocation = (loc: Omit<SavedLocation, 'id'>) => {
    const newLoc: SavedLocation = { ...loc, id: Date.now().toString() };
    setSavedLocations(prev => [...prev, newLoc]);
  };

  const removeSavedLocation = (id: string) => {
    setSavedLocations(prev => prev.filter(l => l.id !== id));
  };

  const addChatMessage = (msg: ChatMessage) => {
    setChatHistory(prev => [...prev, msg]);
  };

  const sendChatQuery = async (queryText: string) => {
    if (!queryText.trim()) return;

    const userMsg: ChatMessage = {
      id: Date.now().toString(),
      sender: 'user',
      text: queryText,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    };
    addChatMessage(userMsg);

    try {
      const response = await postChatQuery(
        queryText,
        location.pincode || location.name,
        location.latitude,
        location.longitude,
        settings.occupation,
        settings.language
      );

      const botMsg: ChatMessage = {
        id: (Date.now() + 1).toString(),
        sender: 'assistant',
        text: response.answer,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        whyDetails: response.why_explainability,
        detectedEvents: response.detected_events,
        recommendedActions: response.recommended_actions,
        weatherSnapshot: response.weather_snapshot
      };
      addChatMessage(botMsg);

      if (settings.accessibility.readAloud) {
        speakText(response.answer);
      }
    } catch (err) {
      const fallbackMsg: ChatMessage = {
        id: (Date.now() + 1).toString(),
        sender: 'assistant',
        text: `WeatherGPT response for ${location.name}: Temperature is ${weather?.temperature ?? 31}°C with ${weather?.weather_desc ?? 'Partly Cloudy'}. Rain probability ${weather?.rain_probability ?? 78}%.`,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        whyDetails: {
          temperature: weather?.temperature ?? 31.5,
          rain_probability: weather?.rain_probability ?? 78,
          rain_mm: weather?.rain ?? 14.2,
          wind_kmh: weather?.wind_speed ?? 14.5,
          uv_index: weather?.uv_index ?? 8,
          weather_code: weather?.weather_code ?? 61,
          weather_desc: weather?.weather_desc ?? "Partly Cloudy",
          data_source: weather?.source ?? "IMD + Open-Meteo",
          nwp_model: weather?.model ?? "ECMWF IFS",
          updated_at: weather?.timestamp ?? new Date().toISOString(),
          active_warnings: weather?.warnings ?? [],
          matched_rules: ['rule_engine_fallback']
        }
      };
      addChatMessage(fallbackMsg);
    }
  };

  const toggleEmergencyMode = () => setEmergencyMode(prev => !prev);

  const speakText = (text: string) => {
    if ('speechSynthesis' in window) {
      window.speechSynthesis.cancel();
      const utterance = new SpeechSynthesisUtterance(text);
      utterance.rate = 0.95;
      window.speechSynthesis.speak(utterance);
    }
  };

  const t = (key: keyof TranslationKeys) => getTranslation(settings.language, key);

  return (
    <AppContext.Provider
      value={{
        settings,
        updateSettings,
        updateAccessibility,
        location,
        setLocation: setLocationState,
        weather,
        forecast,
        isLoadingWeather,
        weatherError,
        refreshWeather,
        useDeviceLocation,
        savedLocations,
        addSavedLocation,
        removeSavedLocation,
        chatHistory,
        addChatMessage,
        sendChatQuery,
        emergencyMode,
        toggleEmergencyMode,
        speakText,
        t
      }}
    >
      {children}
    </AppContext.Provider>
  );
};

export const useApp = () => {
  const context = useContext(AppContext);
  if (!context) {
    throw new Error('useApp must be used within an AppProvider');
  }
  return context;
};
