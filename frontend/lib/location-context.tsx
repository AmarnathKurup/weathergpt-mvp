"use client";

import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
  type ReactNode,
} from "react";
import { api } from "./api";

export interface SelectedLocation {
  name: string;
  lat: number;
  lon: number;
}

interface LocationContextValue {
  location: SelectedLocation | null;
  loading: boolean;
  error: string | null;
  setLocationByCoords: (lat: number, lon: number, name?: string) => Promise<void>;
  setLocationByName: (name: string) => Promise<void>;
  useBrowserLocation: () => void;
}

const DEFAULT_LOCATION: SelectedLocation = {
  name: "Thiruvananthapuram",
  lat: 8.5241,
  lon: 76.9366,
};

const LocationContext = createContext<LocationContextValue | null>(null);

export function LocationProvider({ children }: { children: ReactNode }) {
  const [location, setLocation] = useState<SelectedLocation | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const setLocationByCoords = useCallback(async (lat: number, lon: number, name?: string) => {
    setLoading(true);
    setError(null);
    try {
      if (name) {
        setLocation({ name, lat, lon });
      } else {
        const resolved = await api.reverseGeocode(lat, lon);
        setLocation({ name: resolved.name, lat, lon });
      }
    } catch {
      setLocation({ name: `${lat.toFixed(2)}, ${lon.toFixed(2)}`, lat, lon });
    } finally {
      setLoading(false);
    }
  }, []);

  const setLocationByName = useCallback(async (name: string) => {
    setLoading(true);
    setError(null);
    try {
      const results = await api.searchLocation(name);
      if (results.length === 0) {
        setError(`No location found for "${name}"`);
        return;
      }
      const first = results[0];
      setLocation({ name: first.name, lat: first.lat, lon: first.lon });
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to search location");
    } finally {
      setLoading(false);
    }
  }, []);

  const useBrowserLocation = useCallback(() => {
    if (!navigator.geolocation) {
      setError("Geolocation is not supported by your browser");
      return;
    }
    setLoading(true);
    navigator.geolocation.getCurrentPosition(
      async (pos) => {
        await setLocationByCoords(pos.coords.latitude, pos.coords.longitude);
      },
      () => {
        setError("Could not access your location - using default");
        setLoading(false);
      },
      { timeout: 8000 }
    );
  }, [setLocationByCoords]);

  useEffect(() => {
    setLocation(DEFAULT_LOCATION);
  }, []);

  const value = useMemo(
    () => ({ location, loading, error, setLocationByCoords, setLocationByName, useBrowserLocation }),
    [location, loading, error, setLocationByCoords, setLocationByName, useBrowserLocation]
  );

  return <LocationContext.Provider value={value}>{children}</LocationContext.Provider>;
}

export function useLocation() {
  const ctx = useContext(LocationContext);
  if (!ctx) throw new Error("useLocation must be used within LocationProvider");
  return ctx;
}
