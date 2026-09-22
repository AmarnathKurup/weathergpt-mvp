import type {
  AlertsResponse,
  AnalysisResponse,
  ChatMessage,
  ChatResponse,
  CommunityReport,
  CommunityReportCreate,
  CurrentWeather,
  FarmerAdvisoryResponse,
  ForecastResponse,
  GeocodeResult,
} from "./types";

const BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL?.replace(/\/$/, "") || "http://localhost:8000";

export class ApiError extends Error {
  status: number;
  constructor(message: string, status: number) {
    super(message);
    this.status = status;
    this.name = "ApiError";
  }
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  let res: Response;
  try {
    res = await fetch(`${BASE_URL}${path}`, {
      ...init,
      headers: {
        "Content-Type": "application/json",
        ...(init?.headers || {}),
      },
    });
  } catch {
    throw new ApiError(
      "Could not reach the WeatherGPT backend. Is it running on " + BASE_URL + "?",
      0
    );
  }

  if (!res.ok) {
    let detail = res.statusText;
    try {
      const body = await res.json();
      detail = body.detail || JSON.stringify(body);
    } catch {
      // ignore body parse errors
    }
    throw new ApiError(detail, res.status);
  }

  return res.json() as Promise<T>;
}

function locationQuery(params: { lat?: number; lon?: number; name?: string }) {
  const q = new URLSearchParams();
  if (params.lat !== undefined && params.lon !== undefined) {
    q.set("lat", String(params.lat));
    q.set("lon", String(params.lon));
  } else if (params.name) {
    q.set("name", params.name);
  }
  return q.toString();
}

export const api = {
  currentWeather: (params: { lat?: number; lon?: number; name?: string }) =>
    request<CurrentWeather>(`/api/weather?${locationQuery(params)}`),

  analysis: (params: { lat?: number; lon?: number; name?: string }) =>
    request<AnalysisResponse>(`/api/weather/analysis?${locationQuery(params)}`),

  forecast: (params: { lat?: number; lon?: number; name?: string; days?: number }) => {
    const q = locationQuery(params);
    const extra = params.days ? `&days=${params.days}` : "";
    return request<ForecastResponse>(`/api/forecast?${q}${extra}`);
  },

  alerts: (params: { lat?: number; lon?: number; name?: string }) =>
    request<AlertsResponse>(`/api/alerts?${locationQuery(params)}`),

  searchLocation: (q: string) =>
    request<GeocodeResult[]>(`/api/location?q=${encodeURIComponent(q)}`),

  reverseGeocode: (lat: number, lon: number) =>
    request<GeocodeResult>(`/api/location/reverse?lat=${lat}&lon=${lon}`),

  farmerAdvisory: (params: { lat?: number; lon?: number; name?: string }) =>
    request<FarmerAdvisoryResponse>(`/api/weather/farmer-advisory?${locationQuery(params)}`),

  communityReports: (params: { lat: number; lon: number; radius_km?: number }) => {
    const q = new URLSearchParams({
      lat: String(params.lat),
      lon: String(params.lon),
      radius_km: String(params.radius_km ?? 25),
    });
    return request<CommunityReport[]>(`/api/community/reports?${q.toString()}`);
  },

  createCommunityReport: (payload: CommunityReportCreate) =>
    request<CommunityReport>(`/api/community/reports`, {
      method: "POST",
      body: JSON.stringify(payload),
    }),

  chat: (payload: {
    message: string;
    history: ChatMessage[];
    lat?: number;
    lon?: number;
    location_name?: string;
    language?: string;
  }) =>
    request<ChatResponse>(`/api/chat`, {
      method: "POST",
      body: JSON.stringify(payload),
    }),
};
