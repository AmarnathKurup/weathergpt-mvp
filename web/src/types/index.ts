export interface LocationInfo {
  name: string;
  pincode?: string;
  district?: string;
  state?: string;
  latitude: number;
  longitude: number;
}

export interface WarningItem {
  level: 'GREEN' | 'YELLOW' | 'ORANGE' | 'RED';
  category: string;
  headline: string;
  description: string;
  issued_at?: string;
  source: string;
}

export interface ForecastHourlyItem {
  time: string;
  temperature: number;
  rain_probability: number;
  rain_mm: number;
  wind_speed: number;
  weather_code: number;
  weather_desc: string;
}

export interface ForecastDailyItem {
  date: string;
  temp_max: number;
  temp_min: number;
  rain_probability: number;
  precipitation_sum: number;
  weather_code: number;
  weather_desc: string;
  uv_index_max: number;
}

export interface WeatherSnapshot {
  location: LocationInfo;
  timestamp: string;
  temperature: number;
  feels_like: number;
  humidity: number;
  pressure: number;
  wind_speed: number;
  wind_direction: number;
  wind_gust: number;
  visibility: number;
  cloud_cover: number;
  rain: number;
  rain_probability: number;
  weather_code: number;
  weather_desc: string;
  uv_index: number;
  sunrise: string;
  sunset: string;
  warnings: WarningItem[];
  source: string;
  model: string;
  confidence: number;
}

export interface ForecastResponse {
  location: LocationInfo;
  current: WeatherSnapshot;
  hourly: ForecastHourlyItem[];
  daily: ForecastDailyItem[];
  source: string;
}

export interface PincodeDetails {
  pincode: string;
  office_name: string;
  district: string;
  state: string;
  latitude?: number;
  longitude?: number;
  circle?: string;
  region?: string;
}

export interface ExplainabilityDetails {
  temperature: number;
  rain_probability: number;
  rain_mm: number;
  wind_kmh: number;
  uv_index: number;
  weather_code: number;
  weather_desc: string;
  data_source: string;
  nwp_model: string;
  updated_at: string;
  active_warnings: WarningItem[];
  matched_rules: string[];
}

export interface ChatMessage {
  id: string;
  sender: 'user' | 'assistant';
  text: string;
  timestamp: string;
  whyDetails?: ExplainabilityDetails;
  detectedEvents?: string[];
  recommendedActions?: string[];
  weatherSnapshot?: WeatherSnapshot;
}

export interface ChatResponse {
  query: string;
  intent: string;
  language: string;
  location_name: string;
  answer: string;
  audio_url?: string;
  weather_snapshot: WeatherSnapshot;
  detected_events: string[];
  recommended_actions: string[];
  why_explainability: ExplainabilityDetails;
  confidence: number;
}

export interface SavedLocation {
  id: string;
  label: string; // Home, Office, Farm, College, Custom
  pincode: string;
  name: string;
  district: string;
  state: string;
  latitude: number;
  longitude: number;
}

export type ThemeMode = 'dark' | 'light' | 'system';
export type FontSizeSetting = 'small' | 'normal' | 'large' | 'xlarge';
export type LineSpacingSetting = 'normal' | 'comfortable' | 'expanded';
export type ContentWidthSetting = 'standard' | 'wide';
export type OccupationSetting = 'general' | 'student' | 'farmer' | 'fisherman' | 'driver' | 'delivery_worker' | 'senior_citizen';

export interface AccessibilitySettings {
  textSize: FontSizeSetting;
  lineSpacing: LineSpacingSetting;
  contentWidth: ContentWidthSetting;
  highContrast: boolean;
  reducedMotion: boolean;
  readAloud: boolean;
}

export interface AppSettings {
  theme: ThemeMode;
  language: string; // ISO 639 code ('en', 'hi', 'bn', etc.)
  accessibility: AccessibilitySettings;
  occupation: OccupationSetting;
  notificationsEnabled: boolean;
  notificationCategories: {
    severeWeather: boolean;
    rainAlerts: boolean;
    thunderstorms: boolean;
    heatwaves: boolean;
    savedLocations: boolean;
  };
}
