import React, { useState, useRef, useEffect } from 'react';
import { useApp } from '../../context/AppContext';
import { ChatMessage, ExplainabilityDetails } from '../../types';
import { ExplainabilityModal } from '../modals/ExplainabilityModal';
import {
  MessageSquare,
  Send,
  Mic,
  MicOff,
  Volume2,
  HelpCircle,
  Copy,
  Share2,
  Sparkles,
  Bot,
  User,
  ShieldCheck,
  Check
} from 'lucide-react';

export const WeatherGPTChat: React.FC = () => {
  const { chatHistory, sendChatQuery, speakText, location, t } = useApp();

  const [inputQuery, setInputQuery] = useState('');
  const [isListening, setIsListening] = useState(false);
  const [isSending, setIsSending] = useState(false);
  const [copiedId, setCopiedId] = useState<string | null>(null);
  const [selectedWhyFacts, setSelectedWhyFacts] = useState<ExplainabilityDetails | undefined>(undefined);
  const [isWhyModalOpen, setIsWhyModalOpen] = useState(false);

  const chatEndRef = useRef<HTMLDivElement>(null);

  const quickPrompts = [
    "Will it rain in the evening today?",
    "Do I need an umbrella for my commute?",
    "Can I travel safely tonight?",
    "Agromet advisory for crops in this district",
    "Compare Kolkata and Delhi weather"
  ];

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [chatHistory]);

  const handleSend = async (e?: React.FormEvent) => {
    if (e) e.preventDefault();
    if (!inputQuery.trim() || isSending) return;

    const query = inputQuery.trim();
    setInputQuery('');
    setIsSending(true);
    try {
      await sendChatQuery(query);
    } finally {
      setIsSending(false);
    }
  };

  const handleVoiceCapture = () => {
    const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
    if (!SpeechRecognition) {
      alert('Speech recognition is not supported in your browser.');
      return;
    }

    if (isListening) {
      setIsListening(false);
      return;
    }

    const recognition = new SpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.lang = 'en-IN';

    recognition.onstart = () => setIsListening(true);
    recognition.onend = () => setIsListening(false);
    recognition.onerror = () => setIsListening(false);
    recognition.onresult = (event: any) => {
      const transcript = event.results[0][0].transcript;
      setInputQuery(transcript);
    };

    recognition.start();
  };

  const handleCopyText = (id: string, text: string) => {
    navigator.clipboard.writeText(text);
    setCopiedId(id);
    setTimeout(() => setCopiedId(null), 2000);
  };

  const openWhyModal = (facts?: ExplainabilityDetails) => {
    if (facts) {
      setSelectedWhyFacts(facts);
      setIsWhyModalOpen(true);
    }
  };

  return (
    <div className="glass-panel rounded-3xl p-4 md:p-6 border border-slate-200 dark:border-slate-800 flex flex-col h-[calc(100vh-140px)] min-h-[500px] transition-colors duration-200">
      {/* Header */}
      <div className="flex items-center justify-between border-b border-slate-200 dark:border-slate-800 pb-4 shrink-0">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 rounded-2xl bg-gradient-to-tr from-saffron-500 to-amber-400 flex items-center justify-center shadow-lg shadow-saffron-500/20">
            <Bot className="w-6 h-6 text-navy-950 font-bold" />
          </div>
          <div>
            <h2 className="font-bold text-lg text-slate-900 dark:text-white flex items-center gap-2">
              WeatherGPT Intelligence Assistant
              <span className="text-[10px] font-extrabold px-2 py-0.5 rounded-full bg-emerald-500/20 text-emerald-700 dark:text-emerald-400 border border-emerald-500/30">
                LIVE AI
              </span>
            </h2>
            <p className="text-xs text-slate-500 dark:text-slate-400">Context: {location.name || 'India meteorological pipeline'}</p>
          </div>
        </div>
      </div>

      {/* Messages Scroll Area */}
      <div className="flex-1 overflow-y-auto py-4 space-y-4 pr-1 scrollbar-thin">
        {chatHistory.map((msg) => {
          const isUser = msg.sender === 'user';
          return (
            <div
              key={msg.id}
              className={`flex items-start space-x-3 ${isUser ? 'flex-row-reverse space-x-reverse' : ''}`}
            >
              <div
                className={`w-8 h-8 rounded-xl flex items-center justify-center shrink-0 font-bold text-xs ${
                  isUser ? 'bg-saffron-500 text-white' : 'bg-slate-200 dark:bg-slate-800 text-saffron-600 dark:text-saffron-400 border border-slate-300 dark:border-slate-700'
                }`}
              >
                {isUser ? <User className="w-4 h-4" /> : <Bot className="w-4 h-4" />}
              </div>

              <div className={`max-w-[85%] sm:max-w-[75%] space-y-2`}>
                <div
                  className={`p-4 rounded-2xl text-sm leading-relaxed ${
                    isUser
                      ? 'bg-saffron-500 text-white font-medium rounded-tr-none shadow-lg shadow-saffron-500/10'
                      : 'bg-slate-100 dark:bg-slate-900/90 text-slate-900 dark:text-slate-100 border border-slate-200 dark:border-slate-800 rounded-tl-none shadow-md'
                  }`}
                >
                  <p className="whitespace-pre-wrap">{msg.text}</p>

                  {/* Actions for Assistant Messages */}
                  {!isUser && (
                    <div className="pt-3 border-t border-slate-200 dark:border-slate-800/80 mt-3 flex flex-wrap items-center justify-between gap-2 text-xs">
                      <div className="flex items-center space-x-2">
                        {msg.whyDetails && (
                          <button
                            onClick={() => openWhyModal(msg.whyDetails)}
                            className="flex items-center space-x-1 px-2.5 py-1 bg-saffron-500/15 hover:bg-saffron-500/25 text-saffron-600 dark:text-saffron-400 border border-saffron-500/30 rounded-lg font-semibold transition-colors"
                          >
                            <HelpCircle className="w-3.5 h-3.5" />
                            <span>Why?</span>
                          </button>
                        )}
                        <button
                          onClick={() => speakText(msg.text)}
                          className="flex items-center space-x-1 px-2.5 py-1 bg-slate-200 dark:bg-slate-800 hover:bg-slate-300 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-300 rounded-lg transition-colors border border-slate-300 dark:border-slate-700"
                        >
                          <Volume2 className="w-3.5 h-3.5 text-sky-600 dark:text-sky-400" />
                          <span>Read</span>
                        </button>
                      </div>

                      <div className="flex items-center space-x-2 text-slate-500 dark:text-slate-400">
                        <button
                          onClick={() => handleCopyText(msg.id, msg.text)}
                          className="p-1 hover:text-slate-900 dark:hover:text-white transition-colors"
                          title="Copy message"
                        >
                          {copiedId === msg.id ? <Check className="w-3.5 h-3.5 text-emerald-600 dark:text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
                        </button>
                        <button
                          onClick={() => navigator.share && navigator.share({ text: msg.text })}
                          className="p-1 hover:text-slate-900 dark:hover:text-white transition-colors"
                          title="Share"
                        >
                          <Share2 className="w-3.5 h-3.5" />
                        </button>
                      </div>
                    </div>
                  )}
                </div>

                <span className={`text-[10px] text-slate-500 block ${isUser ? 'text-right' : 'text-left'}`}>
                  {msg.timestamp}
                </span>
              </div>
            </div>
          );
        })}
        <div ref={chatEndRef} />
      </div>

      {/* Quick Contextual Prompts Pills */}
      <div className="py-2 flex items-center space-x-2 overflow-x-auto scrollbar-none shrink-0 border-t border-slate-200 dark:border-slate-800/80">
        <Sparkles className="w-4 h-4 text-saffron-500 shrink-0" />
        {quickPrompts.map((prompt, idx) => (
          <button
            key={idx}
            onClick={() => setInputQuery(prompt)}
            className="flex-none px-3 py-1 bg-slate-100 dark:bg-slate-900 hover:bg-slate-200 dark:hover:bg-slate-800 border border-slate-200 dark:border-slate-800 hover:border-slate-300 dark:hover:border-slate-700 rounded-full text-xs text-slate-700 dark:text-slate-300 hover:text-saffron-600 dark:hover:text-saffron-400 transition-colors whitespace-nowrap"
          >
            {prompt}
          </button>
        ))}
      </div>

      {/* Query Form Input */}
      <form onSubmit={handleSend} className="pt-2 shrink-0 flex items-center space-x-2">
        <div className="relative flex-1 flex items-center">
          <input
            type="text"
            value={inputQuery}
            onChange={(e) => setInputQuery(e.target.value)}
            placeholder={t('askPlaceholder')}
            className="w-full bg-slate-100 dark:bg-slate-900 border border-slate-300 dark:border-slate-700 focus:border-saffron-500 rounded-2xl pl-4 pr-12 py-3 text-sm text-slate-900 dark:text-white placeholder-slate-400 dark:placeholder-slate-500 focus:outline-none transition-all shadow-inner"
          />
          <button
            type="button"
            onClick={handleVoiceCapture}
            className={`absolute right-2 p-2 rounded-xl transition-colors ${
              isListening
                ? 'bg-red-500 text-white animate-pulse'
                : 'bg-slate-200 dark:bg-slate-800 text-slate-600 dark:text-slate-400 hover:text-saffron-600 dark:hover:text-saffron-400 border border-slate-300 dark:border-slate-700'
            }`}
            title="Voice input"
          >
            {isListening ? <MicOff className="w-4 h-4" /> : <Mic className="w-4 h-4" />}
          </button>
        </div>

        <button
          type="submit"
          disabled={!inputQuery.trim() || isSending}
          className="px-5 py-3 bg-saffron-500 hover:bg-saffron-600 disabled:opacity-50 disabled:cursor-not-allowed text-white font-bold rounded-2xl shadow-lg shadow-saffron-500/20 flex items-center space-x-2 transition-all shrink-0"
        >
          <span>{t('send')}</span>
          <Send className="w-4 h-4" />
        </button>
      </form>

      {/* Explainability Reasoning Modal */}
      <ExplainabilityModal
        isOpen={isWhyModalOpen}
        onClose={() => setIsWhyModalOpen(false)}
        facts={selectedWhyFacts}
      />
    </div>
  );
};
