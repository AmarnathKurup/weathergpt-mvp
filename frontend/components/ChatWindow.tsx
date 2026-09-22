"use client";
import ReactMarkdown from "react-markdown";

import { useRef, useState, useEffect, useCallback } from "react";
import { api, ApiError } from "@/lib/api";
import type { ChatMessage, ToolCallTrace } from "@/lib/types";
import { useLocation } from "@/lib/location-context";
import {
  VOICE_LANGUAGES,
  extractLangCode,
  isSpeechRecognitionSupported,
  isSpeechSynthesisSupported,
  localeForLangCode,
  speak,
  startListening,
  stopSpeaking,
} from "@/lib/speech";

interface DisplayMessage extends ChatMessage {
  toolCalls?: ToolCallTrace[];
  detectedLanguage?: string;
  error?: boolean;
}

const SUGGESTIONS = [
  "What's the weather right now?",
  "Will it rain tomorrow?",
  "Any weather alerts I should know about?",
  "What is a heatwave and how should I prepare?",
];

export default function ChatWindow() {
  const { location } = useLocation();
  const [messages, setMessages] = useState<DisplayMessage[]>([
    {
      role: "assistant",
      content:
        "Hi! I'm WeatherGPT 🌦️ Ask me about current conditions, forecasts, or weather hazards for any location. I can also answer general meteorology questions.",
    },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [voiceLang, setVoiceLang] = useState("en");
  const [listening, setListening] = useState(false);
  const [autoSpeak, setAutoSpeak] = useState(false);
  const [voiceError, setVoiceError] = useState<string | null>(null);
  const bottomRef = useRef<HTMLDivElement>(null);
  const recognitionRef = useRef<{ stop: () => void } | null>(null);

  const voiceSupported = isSpeechRecognitionSupported();
  const ttsSupported = isSpeechSynthesisSupported();

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  // Stop any in-progress speech when the component unmounts (navigating away)
  useEffect(() => stopSpeaking, []);

  const send = useCallback(
    async (text: string, options?: { forceSpeak?: boolean }) => {
      if (!text.trim() || loading) return;
      const userMsg: DisplayMessage = { role: "user", content: text };
      const nextMessages = [...messages, userMsg];
      setMessages(nextMessages);
      setInput("");
      setLoading(true);

      try {
        const history: ChatMessage[] = nextMessages
          .filter((m) => !m.error)
          .map((m) => ({ role: m.role, content: m.content }));

        const res = await api.chat({
          message: text,
          history: history.slice(0, -1), // exclude the message we just sent, backend appends it
          lat: location?.lat,
          lon: location?.lon,
          location_name: location?.name,
        });

        setMessages((prev) => [
          ...prev,
          {
            role: "assistant",
            content: res.reply,
            toolCalls: res.tool_calls,
            detectedLanguage: res.detected_language,
          },
        ]);

        if ((autoSpeak || options?.forceSpeak) && ttsSupported) {
          const locale = localeForLangCode(extractLangCode(res.detected_language));
          speak(res.reply, locale);
        }
      } catch (e) {
        const message =
          e instanceof ApiError
            ? e.message
            : "Something went wrong talking to the WeatherGPT agent.";
        setMessages((prev) => [...prev, { role: "assistant", content: message, error: true }]);
      } finally {
        setLoading(false);
      }
    },
    [messages, loading, location, autoSpeak, ttsSupported]
  );

  function toggleListening() {
    if (listening) {
      recognitionRef.current?.stop();
      setListening(false);
      return;
    }
    setVoiceError(null);
    const handle = startListening(
      localeForLangCode(voiceLang),
      (transcript) => {
        setInput(transcript);
        setListening(false);
        // Send immediately so voice feels conversational rather than a two-step process
        send(transcript);
      },
      () => setListening(false),
      (msg) => {
        setVoiceError(msg);
        setListening(false);
      }
    );
    if (handle) {
      recognitionRef.current = handle;
      setListening(true);
    }
  }

  return (
    <div className="flex flex-col h-[600px] rounded-2xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 overflow-hidden">
      <div className="flex items-center justify-between gap-2 border-b border-slate-200 dark:border-slate-700 px-3 py-2 text-xs">
        <div className="flex items-center gap-2">
          <span className="text-slate-500 dark:text-slate-400">Voice language:</span>
          <select
            value={voiceLang}
            onChange={(e) => setVoiceLang(e.target.value)}
            className="rounded border border-slate-300 dark:border-slate-600 dark:bg-slate-800 px-1.5 py-0.5"
          >
            {VOICE_LANGUAGES.map((l) => (
              <option key={l.code} value={l.code}>
                {l.label}
              </option>
            ))}
          </select>
        </div>
        {ttsSupported && (
          <label className="flex items-center gap-1.5 cursor-pointer select-none text-slate-500 dark:text-slate-400">
            <input
              type="checkbox"
              checked={autoSpeak}
              onChange={(e) => setAutoSpeak(e.target.checked)}
            />
            🔊 Read replies aloud
          </label>
        )}
      </div>

      <div className="px-3 pt-3">
        <button
          type="button"
          onClick={() =>
            send(
              "Give me a full emergency safety briefing for my current location: all active hazards, how severe they are, and exactly what I should do right now.",
              { forceSpeak: true }
            )
          }
          disabled={loading}
          className="w-full rounded-xl bg-red-600 hover:bg-red-700 text-white text-sm font-semibold py-2.5 flex items-center justify-center gap-2 disabled:opacity-50"
        >
          🚨 Emergency Briefing {ttsSupported && "(spoken aloud)"}
        </button>
      </div>

      <div className="flex-1 overflow-y-auto p-4 space-y-3">
        {messages.map((m, i) => (
          <div key={i} className={`flex ${m.role === "user" ? "justify-end" : "justify-start"}`}>
            <div
              className={`max-w-[80%] rounded-2xl px-4 py-2 text-sm ${
                m.role === "user"
                  ? "bg-sky-600 text-white rounded-br-sm"
                  : m.error
                  ? "bg-red-50 text-red-700 border border-red-200 rounded-bl-sm"
                  : "bg-slate-100 dark:bg-slate-800 dark:text-slate-100 rounded-bl-sm"
              }`}
            >
              {m.role === "assistant" ? (
                  <div className="prose prose-sm dark:prose-invert max-w-none">
                    <ReactMarkdown>{m.content}</ReactMarkdown>
                  </div>
                ) : (
                  <span className="whitespace-pre-wrap">{m.content}</span>
                )}
              <div className="mt-2 pt-2 border-t border-slate-200 dark:border-slate-700 flex items-center justify-between gap-2 text-[11px] opacity-60">
                {m.toolCalls && m.toolCalls.length > 0 ? (
                  <span>🔧 used tools: {m.toolCalls.map((t) => t.tool).join(", ")}</span>
                ) : (
                  <span />
                )}
                {m.role === "assistant" && !m.error && ttsSupported && (
                  <button
                    type="button"
                    onClick={() =>
                      speak(m.content, localeForLangCode(extractLangCode(m.detectedLanguage)))
                    }
                    title="Read aloud"
                    className="hover:opacity-100"
                  >
                    🔊
                  </button>
                )}
              </div>
            </div>
          </div>
        ))}
        {loading && (
          <div className="flex justify-start">
            <div className="bg-slate-100 dark:bg-slate-800 rounded-2xl rounded-bl-sm px-4 py-2 text-sm animate-pulse">
              WeatherGPT is thinking...
            </div>
          </div>
        )}
        <div ref={bottomRef} />
      </div>

      {messages.length <= 1 && (
        <div className="px-4 pb-2 flex flex-wrap gap-2">
          {SUGGESTIONS.map((s) => (
            <button
              key={s}
              onClick={() => send(s)}
              className="text-xs rounded-full border border-slate-300 dark:border-slate-600 px-3 py-1 hover:bg-slate-100 dark:hover:bg-slate-800"
            >
              {s}
            </button>
          ))}
        </div>
      )}

      {voiceError && (
        <div className="px-4 pb-1 text-[11px] text-red-500">{voiceError}</div>
      )}

      <form
        onSubmit={(e) => {
          e.preventDefault();
          send(input);
        }}
        className="border-t border-slate-200 dark:border-slate-700 p-3 flex gap-2"
      >
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder={
            location ? `Ask about weather in ${location.name}...` : "Ask WeatherGPT..."
          }
          className="flex-1 rounded-lg border border-slate-300 dark:border-slate-600 dark:bg-slate-800 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-sky-500"
        />
        {voiceSupported && (
          <button
            type="button"
            onClick={toggleListening}
            title={listening ? "Stop listening" : "Speak your question"}
            className={`rounded-lg px-3 py-2 text-sm border ${
              listening
                ? "bg-red-500 text-white border-red-500 animate-pulse"
                : "border-slate-300 dark:border-slate-600 hover:bg-slate-100 dark:hover:bg-slate-800"
            }`}
          >
            🎤
          </button>
        )}
        <button
          type="submit"
          disabled={loading || !input.trim()}
          className="rounded-lg bg-sky-600 px-4 py-2 text-sm font-medium text-white hover:bg-sky-700 disabled:opacity-50"
        >
          Send
        </button>
      </form>
    </div>
  );
}
