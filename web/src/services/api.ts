import {
  WeatherSnapshot,
  ForecastResponse,
  PincodeDetails,
  ChatResponse,
  WarningItem
} from '../types';

const BASE_URL = '/api/v1';

export async function fetchCurrentWeather(location?: string, lat?: number, lon?: number): Promise<WeatherSnapshot> {
  const params = new URLSearchParams();
  if (location) params.append('location', location);
  if (lat !== undefined && lat !== null) params.append('lat', lat.toString());
  if (lon !== undefined && lon !== null) params.append('lon', lon.toString());

  const res = await fetch(`${BASE_URL}/weather/current?${params.toString()}`);
  if (!res.ok) {
    throw new Error(`Failed to fetch current weather: ${res.statusText}`);
  }
  return res.json();
}

export async function fetchForecast(location?: string, lat?: number, lon?: number): Promise<ForecastResponse> {
  const params = new URLSearchParams();
  if (location) params.append('location', location);
  if (lat !== undefined && lat !== null) params.append('lat', lat.toString());
  if (lon !== undefined && lon !== null) params.append('lon', lon.toString());

  const res = await fetch(`${BASE_URL}/weather/forecast?${params.toString()}`);
  if (!res.ok) {
    throw new Error(`Failed to fetch forecast: ${res.statusText}`);
  }
  return res.json();
}

export async function fetchPincodeDetails(pin: string): Promise<PincodeDetails> {
  const res = await fetch(`${BASE_URL}/location/pincode/${pin}`);
  if (!res.ok) {
    throw new Error(`Pincode ${pin} not found in India Post directory.`);
  }
  return res.json();
}

export async function searchLocations(query: string): Promise<PincodeDetails[]> {
  const res = await fetch(`${BASE_URL}/location/search?q=${encodeURIComponent(query)}`);
  if (!res.ok) {
    return [];
  }
  return res.json();
}

export async function resolveLocation(query?: string, lat?: number, lon?: number) {
  const params = new URLSearchParams();
  if (query) params.append('q', query);
  if (lat !== undefined && lat !== null) params.append('lat', lat.toString());
  if (lon !== undefined && lon !== null) params.append('lon', lon.toString());

  const res = await fetch(`${BASE_URL}/location/resolve?${params.toString()}`);
  if (!res.ok) {
    throw new Error('Could not resolve location.');
  }
  return res.json();
}

export async function fetchWarnings(location?: string, lat?: number, lon?: number) {
  const params = new URLSearchParams();
  if (location) params.append('location', location);
  if (lat !== undefined && lat !== null) params.append('lat', lat.toString());
  if (lon !== undefined && lon !== null) params.append('lon', lon.toString());

  const res = await fetch(`${BASE_URL}/warnings?${params.toString()}`);
  if (!res.ok) {
    throw new Error('Failed to fetch warnings.');
  }
  return res.json();
}

export async function postChatQuery(
  query: string,
  location?: string,
  latitude?: number,
  longitude?: number,
  occupation: string = 'general',
  language: string = 'en'
): Promise<ChatResponse> {
  const res = await fetch(`${BASE_URL}/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      query,
      location,
      latitude,
      longitude,
      occupation,
      language
    })
  });

  if (!res.ok) {
    throw new Error('Failed to process WeatherGPT chat query.');
  }
  return res.json();
}

export async function fetchSupportedLanguages() {
  const res = await fetch(`${BASE_URL}/language/supported`);
  if (!res.ok) {
    throw new Error('Failed to fetch languages.');
  }
  return res.json();
}

export async function translateText(text: string, targetLanguage: string, sourceLanguage: string = 'en') {
  const res = await fetch(`${BASE_URL}/language/translate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      text,
      target_language: targetLanguage,
      source_language: sourceLanguage
    })
  });

  if (!res.ok) {
    throw new Error('Failed to translate text.');
  }
  return res.json();
}

export async function fetchClimateTrend(location: string = 'Kolkata') {
  const res = await fetch(`${BASE_URL}/climate/trend?location=${encodeURIComponent(location)}`);
  if (!res.ok) {
    throw new Error('Failed to fetch climate trend.');
  }
  return res.json();
}
