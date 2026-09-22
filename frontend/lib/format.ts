export function weatherEmoji(code?: number | null, isDay?: boolean | null): string {
  if (code === null || code === undefined) return "❓";
  const day = isDay !== false;
  if (code === 0) return day ? "☀️" : "🌙";
  if (code === 1) return day ? "🌤️" : "🌙";
  if (code === 2) return "⛅";
  if (code === 3) return "☁️";
  if (code === 45 || code === 48) return "🌫️";
  if ([51, 53, 55, 56, 57].includes(code)) return "🌦️";
  if ([61, 63, 65, 66, 67, 80, 81, 82].includes(code)) return "🌧️";
  if ([71, 73, 75, 77, 85, 86].includes(code)) return "❄️";
  if ([95, 96, 99].includes(code)) return "⛈️";
  return "🌡️";
}

export function severityColor(severity: string): string {
  const s = severity.toLowerCase();
  if (s.includes("extreme") || s.includes("severe")) return "bg-red-100 text-red-800 border-red-300";
  if (s.includes("moderate")) return "bg-orange-100 text-orange-800 border-orange-300";
  if (s.includes("minor")) return "bg-yellow-100 text-yellow-800 border-yellow-300";
  return "bg-blue-100 text-blue-800 border-blue-300";
}

export function formatDay(dateStr: string): string {
  try {
    const d = new Date(dateStr);
    return d.toLocaleDateString(undefined, { weekday: "short", month: "short", day: "numeric" });
  } catch {
    return dateStr;
  }
}

export function formatTime(dateStr: string): string {
  try {
    const d = new Date(dateStr);
    return d.toLocaleTimeString(undefined, { hour: "numeric", minute: "2-digit" });
  } catch {
    return dateStr;
  }
}
