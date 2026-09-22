import type { Metadata } from "next";
import "./globals.css";
import "leaflet/dist/leaflet.css";
import { LocationProvider } from "@/lib/location-context";
import NavBar from "@/components/NavBar";

export const metadata: Metadata = {
  title: "WeatherGPT — Local MVP",
  description: "An AI-powered weather dashboard, map, and chat assistant.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className="h-full antialiased">
      <body className="min-h-full flex flex-col bg-slate-50 text-slate-900 dark:bg-slate-950 dark:text-slate-100">
        <LocationProvider>
          <NavBar />
          <main className="flex-1 w-full max-w-6xl mx-auto px-4 py-6">{children}</main>
          <footer className="text-center text-xs text-slate-400 py-4">
            WeatherGPT MVP · data from Open-Meteo, NOAA/NWS · AI by Groq
          </footer>
        </LocationProvider>
      </body>
    </html>
  );
}
