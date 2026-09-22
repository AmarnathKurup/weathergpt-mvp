export interface GeocodeResult {
  name: string;
  country?: string | null;
  admin1?: string | null;
  lat: number;
  lon: number;
  timezone?: string | null;
}

export interface CurrentWeather {
  location: string;
  lat: number;
  lon: number;
  timezone?: string | null;
  temperature_c?: number | null;
  apparent_temperature_c?: number | null;
  humidity_pct?: number | null;
  wind_speed_kmh?: number | null;
  wind_direction_deg?: number | null;
  precipitation_mm?: number | null;
  weather_code?: number | null;
  condition?: string | null;
  is_day?: boolean | null;
  observed_at?: string | null;
  source: string;
}

export interface ForecastDay {
  date: string;
  temp_max_c?: number | null;
  temp_min_c?: number | null;
  precipitation_sum_mm?: number | null;
  precipitation_probability_pct?: number | null;
  wind_speed_max_kmh?: number | null;
  weather_code?: number | null;
  condition?: string | null;
  sunrise?: string | null;
  sunset?: string | null;
}

export interface ForecastHour {
  time: string;
  temperature_c?: number | null;
  precipitation_mm?: number | null;
  precipitation_probability_pct?: number | null;
  weather_code?: number | null;
  condition?: string | null;
}

export interface ForecastResponse {
  location: string;
  lat: number;
  lon: number;
  timezone?: string | null;
  daily: ForecastDay[];
  hourly: ForecastHour[];
  source: string;
}

export interface WeatherAlert {
  id: string;
  event: string;
  severity: string;
  headline: string;
  description: string;
  start?: string | null;
  end?: string | null;
  source: string;
}

export interface AlertsResponse {
  location: string;
  lat: number;
  lon: number;
  alerts: WeatherAlert[];
  generated: WeatherAlert[];
}

export interface AnalysisResponse {
  location: string;
  summary: string;
  highlights: string[];
  risk_score: number;
  risk_level: string;
  risk_factors: string[];
}

export interface CommunityReport {
  id: string;
  lat: number;
  lon: number;
  category: string;
  note?: string | null;
  location_name?: string | null;
  created_at: string;
  distance_km?: number | null;
}

export interface CommunityReportCreate {
  lat: number;
  lon: number;
  category: string;
  note?: string;
  location_name?: string;
}

export interface FarmerAdvisoryResponse {
  location: string;
  spray_advice: string;
  irrigation_advice: string;
  livestock_advice: string;
  summary: string[];
}

export interface ChatMessage {
  role: "user" | "assistant";
  content: string;
}

export interface ToolCallTrace {
  tool: string;
  arguments: Record<string, unknown>;
}

export interface LocationQuery {
  name?: string | null;
  lat?: number | null;
  lon?: number | null;
}

export interface ChatResponse {
  reply: string;
  detected_language: string;
  tool_calls: ToolCallTrace[];
  used_location?: LocationQuery | null;
}
