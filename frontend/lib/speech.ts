// Thin wrapper around the browser's built-in Web Speech API.
// No external service, no API key - runs entirely client-side (best support in Chrome/Edge).
// Kept intentionally simple: speech-to-text for the chat input, text-to-speech for replies.

// Maps langdetect-style codes (as returned by the backend) to BCP-47 locale
// tags the Web Speech API expects. Covers the languages WeatherGPT's backend
// already detects/translates for.
export const VOICE_LANGUAGES: { code: string; label: string; locale: string }[] = [
  { code: "en", label: "English", locale: "en-US" },
  { code: "hi", label: "Hindi", locale: "hi-IN" },
  { code: "ta", label: "Tamil", locale: "ta-IN" },
  { code: "te", label: "Telugu", locale: "te-IN" },
  { code: "kn", label: "Kannada", locale: "kn-IN" },
  { code: "ml", label: "Malayalam", locale: "ml-IN" },
  { code: "bn", label: "Bengali", locale: "bn-IN" },
  { code: "mr", label: "Marathi", locale: "mr-IN" },
  { code: "gu", label: "Gujarati", locale: "gu-IN" },
  { code: "es", label: "Spanish", locale: "es-ES" },
  { code: "fr", label: "French", locale: "fr-FR" },
];

export function localeForLangCode(code: string): string {
  const match = VOICE_LANGUAGES.find((l) => l.code === code);
  return match?.locale || "en-US";
}

// The backend returns detected_language as e.g. "hi (Hindi)" - pull the code out.
export function extractLangCode(detected: string | undefined): string {
  if (!detected) return "en";
  const code = detected.split(" ")[0].trim();
  return code || "en";
}

export function isSpeechRecognitionSupported(): boolean {
  if (typeof window === "undefined") return false;
  return Boolean(window.SpeechRecognition || window.webkitSpeechRecognition);
}

export function isSpeechSynthesisSupported(): boolean {
  return typeof window !== "undefined" && "speechSynthesis" in window;
}

interface RecognitionHandle {
  stop: () => void;
}

export function startListening(
  locale: string,
  onResult: (transcript: string) => void,
  onEnd: () => void,
  onError: (message: string) => void
): RecognitionHandle | null {
  const SpeechRecognitionCtor = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!SpeechRecognitionCtor) {
    onError("Voice input isn't supported in this browser. Try Chrome or Edge.");
    return null;
  }

  const recognition = new SpeechRecognitionCtor();
  recognition.lang = locale;
  recognition.interimResults = false;
  recognition.maxAlternatives = 1;

  recognition.onresult = (event: SpeechRecognitionEvent) => {
    const transcript = event.results[0]?.[0]?.transcript;
    if (transcript) onResult(transcript);
  };
  recognition.onerror = (event: SpeechRecognitionErrorEvent) => {
    onError(event.error === "not-allowed" ? "Microphone access was denied." : `Voice input error: ${event.error}`);
  };
  recognition.onend = () => onEnd();

  recognition.start();
  return { stop: () => recognition.stop() };
}

export function speak(text: string, locale: string): void {
  if (!isSpeechSynthesisSupported() || !text.trim()) return;
  // Cancel anything currently speaking so replies don't overlap
  window.speechSynthesis.cancel();
  const utterance = new SpeechSynthesisUtterance(text);
  utterance.lang = locale;
  const voices = window.speechSynthesis.getVoices();
  const match = voices.find((v) => v.lang === locale) || voices.find((v) => v.lang.startsWith(locale.split("-")[0]));
  if (match) utterance.voice = match;
  window.speechSynthesis.speak(utterance);
}

export function stopSpeaking(): void {
  if (isSpeechSynthesisSupported()) window.speechSynthesis.cancel();
}
