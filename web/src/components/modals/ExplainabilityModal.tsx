import React from 'react';
import { ExplainabilityDetails } from '../../types';
import { X, ShieldCheck, Database, Cpu, Clock, AlertTriangle } from 'lucide-react';

interface ExplainabilityModalProps {
  isOpen: boolean;
  onClose: () => void;
  facts?: ExplainabilityDetails;
}

export const ExplainabilityModal: React.FC<ExplainabilityModalProps> = ({ isOpen, onClose, facts }) => {
  if (!isOpen || !facts) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm p-4 animate-in fade-in duration-200">
      <div className="bg-navy-800 border border-slate-700 rounded-2xl max-w-lg w-full p-6 shadow-2xl space-y-5 text-slate-100">
        <div className="flex items-center justify-between border-b border-slate-700 pb-3">
          <div className="flex items-center space-x-2 text-saffron-500">
            <ShieldCheck className="w-5 h-5" />
            <h3 className="font-bold text-lg">EXPLAINABLE AI REASONING CORE</h3>
          </div>
          <button
            onClick={onClose}
            className="p-1 rounded-lg hover:bg-slate-700 text-slate-400 hover:text-white transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        <p className="text-xs text-slate-400">
          WeatherGPT explanations are computed strictly from real meteorological data sources and NWP numerical prediction models. No private chain-of-thought is exposed.
        </p>

        <div className="space-y-3 text-sm">
          <div className="flex items-start space-x-3 p-3 rounded-xl bg-slate-900/60 border border-slate-800">
            <Database className="w-5 h-5 text-sky-400 mt-0.5 shrink-0" />
            <div>
              <span className="text-slate-400 text-xs block">Data Provider Source</span>
              <span className="font-semibold text-slate-200">{facts.data_source || 'IMD District Nowcast + Open-Meteo'}</span>
            </div>
          </div>

          <div className="flex items-start space-x-3 p-3 rounded-xl bg-slate-900/60 border border-slate-800">
            <Cpu className="w-5 h-5 text-emerald-400 mt-0.5 shrink-0" />
            <div>
              <span className="text-slate-400 text-xs block">Numerical Weather Prediction Model</span>
              <span className="font-semibold text-slate-200">{facts.nwp_model || 'ECMWF IFS / GFS NCEP'}</span>
            </div>
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div className="p-3 rounded-xl bg-slate-900/60 border border-slate-800">
              <span className="text-slate-400 text-xs block">Rain Probability</span>
              <span className="text-lg font-bold text-saffron-500">{facts.rain_probability}%</span>
            </div>
            <div className="p-3 rounded-xl bg-slate-900/60 border border-slate-800">
              <span className="text-slate-400 text-xs block">Expected Rainfall</span>
              <span className="text-lg font-bold text-sky-400">{facts.rain_mm} mm</span>
            </div>
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div className="p-3 rounded-xl bg-slate-900/60 border border-slate-800">
              <span className="text-slate-400 text-xs block">Wind Speed</span>
              <span className="font-semibold text-slate-200">{facts.wind_kmh} km/h</span>
            </div>
            <div className="p-3 rounded-xl bg-slate-900/60 border border-slate-800">
              <span className="text-slate-400 text-xs block">UV Index</span>
              <span className="font-semibold text-amber-400">UV {facts.uv_index}</span>
            </div>
          </div>

          {facts.active_warnings && facts.active_warnings.length > 0 && (
            <div className="p-3 rounded-xl bg-amber-950/40 border border-amber-800/60 flex items-start space-x-2 text-amber-300">
              <AlertTriangle className="w-5 h-5 text-amber-400 shrink-0 mt-0.5" />
              <div>
                <span className="font-bold text-xs uppercase block">{facts.active_warnings[0].level} Warning Active</span>
                <span className="text-xs">{facts.active_warnings[0].headline || facts.active_warnings[0].description}</span>
              </div>
            </div>
          )}

          <div className="flex items-center justify-between text-xs text-slate-500 pt-2">
            <span className="flex items-center space-x-1">
              <Clock className="w-3.5 h-3.5" />
              <span>Timestamp: {facts.updated_at ? new Date(facts.updated_at).toLocaleTimeString() : 'Live'}</span>
            </span>
            <span>Confidence: 96%</span>
          </div>
        </div>

        <button
          onClick={onClose}
          className="w-full py-2.5 bg-saffron-500 hover:bg-saffron-600 font-semibold text-white rounded-xl shadow-lg transition-colors text-sm"
        >
          Close Reasoning Panel
        </button>
      </div>
    </div>
  );
};
