import React, { useState } from 'react';
import { useApp } from '../../context/AppContext';
import { Bookmark, Plus, Trash2, MapPin, Building, Search, ArrowRight } from 'lucide-react';
import { fetchPincodeDetails } from '../../services/api';

export const SavedLocations: React.FC = () => {
  const { savedLocations, addSavedLocation, removeSavedLocation, refreshWeather, t } = useApp();

  const [newPincode, setNewPincode] = useState('');
  const [newLabel, setNewLabel] = useState('Custom');
  const [isAdding, setIsAdding] = useState(false);
  const [errorMsg, setErrorMsg] = useState('');

  const handleAdd = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newPincode.trim()) return;

    setIsAdding(true);
    setErrorMsg('');
    try {
      const pinData = await fetchPincodeDetails(newPincode.trim());
      addSavedLocation({
        label: newLabel,
        pincode: pinData.pincode,
        name: pinData.office_name,
        district: pinData.district,
        state: pinData.state,
        latitude: pinData.latitude || 22.5726,
        longitude: pinData.longitude || 88.3639
      });
      setNewPincode('');
    } catch (err: any) {
      setErrorMsg(err.message || 'Could not resolve PIN code.');
    } finally {
      setIsAdding(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="glass-panel rounded-3xl p-6 border border-slate-200 dark:border-slate-800 flex items-center justify-between transition-colors">
        <div className="flex items-center space-x-3">
          <div className="p-2.5 rounded-2xl bg-saffron-500/10 text-saffron-600 dark:text-saffron-500 border border-saffron-500/20">
            <Bookmark className="w-6 h-6" />
          </div>
          <div>
            <h2 className="text-xl font-bold text-slate-900 dark:text-white">{t('savedPlaces')}</h2>
            <p className="text-xs text-slate-500 dark:text-slate-400">Quick Access Places (Home, Office, Farm, College)</p>
          </div>
        </div>
      </div>

      {/* Add New Location Form */}
      <form onSubmit={handleAdd} className="glass-panel rounded-3xl p-4 md:p-6 border border-slate-200 dark:border-slate-800 space-y-4 transition-colors">
        <h3 className="font-bold text-sm text-slate-900 dark:text-white flex items-center gap-2">
          <Plus className="w-4 h-4 text-saffron-500" />
          <span>{t('addLocation')}</span>
        </h3>

        <div className="flex flex-col sm:flex-row gap-3">
          <input
            type="text"
            value={newPincode}
            onChange={(e) => setNewPincode(e.target.value)}
            placeholder="Enter 6-digit PIN Code (e.g. 110001)..."
            className="flex-1 bg-slate-100 dark:bg-slate-900 border border-slate-300 dark:border-slate-700 rounded-xl px-4 py-2.5 text-xs text-slate-900 dark:text-white placeholder-slate-400 dark:placeholder-slate-500 focus:outline-none focus:border-saffron-500"
          />

          <select
            value={newLabel}
            onChange={(e) => setNewLabel(e.target.value)}
            className="bg-slate-100 dark:bg-slate-900 border border-slate-300 dark:border-slate-700 rounded-xl px-4 py-2.5 text-xs text-slate-800 dark:text-slate-200 focus:outline-none focus:border-saffron-500 cursor-pointer"
          >
            <option value="Home">Home</option>
            <option value="Office">Office</option>
            <option value="Farm">Farm</option>
            <option value="College">College</option>
            <option value="Custom">Custom</option>
          </select>

          <button
            type="submit"
            disabled={isAdding || !newPincode.trim()}
            className="px-6 py-2.5 bg-saffron-500 hover:bg-saffron-600 disabled:opacity-50 text-white font-bold rounded-xl text-xs shadow-lg shadow-saffron-500/20 transition-all shrink-0"
          >
            {isAdding ? 'Resolving...' : 'Add Place'}
          </button>
        </div>

        {errorMsg && <p className="text-xs text-red-500 dark:text-red-400 font-semibold">{errorMsg}</p>}
      </form>

      {/* Saved Locations Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {savedLocations.map((loc) => (
          <div
            key={loc.id}
            className="glass-panel rounded-3xl p-6 border border-slate-200 dark:border-slate-800 space-y-4 hover:border-slate-300 dark:hover:border-slate-700 transition-all flex flex-col justify-between"
          >
            <div className="flex items-start justify-between">
              <div className="flex items-center space-x-3">
                <div className="p-2.5 rounded-2xl bg-slate-100 dark:bg-slate-800 text-saffron-600 dark:text-saffron-400 border border-slate-200 dark:border-slate-700">
                  <Building className="w-5 h-5" />
                </div>
                <div>
                  <span className="text-[10px] font-extrabold px-2 py-0.5 rounded bg-saffron-500/20 text-saffron-700 dark:text-saffron-400 uppercase tracking-wider block w-fit mb-0.5">
                    {loc.label}
                  </span>
                  <h3 className="font-bold text-base text-slate-900 dark:text-white">{loc.name}</h3>
                  <p className="text-xs text-slate-500 dark:text-slate-400">
                    {loc.district}, {loc.state} (PIN {loc.pincode})
                  </p>
                </div>
              </div>

              <button
                onClick={() => removeSavedLocation(loc.id)}
                className="p-2 rounded-xl text-slate-400 hover:text-red-500 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
                title="Remove location"
              >
                <Trash2 className="w-4 h-4" />
              </button>
            </div>

            <button
              onClick={() => refreshWeather(loc.pincode, loc.latitude, loc.longitude)}
              className="w-full py-2 bg-slate-100 dark:bg-slate-900 hover:bg-slate-200 dark:hover:bg-slate-800 text-slate-700 dark:text-slate-200 hover:text-saffron-600 dark:hover:text-saffron-400 border border-slate-200 dark:border-slate-800 rounded-xl text-xs font-semibold flex items-center justify-center space-x-2 transition-colors"
            >
              <span>View Weather for {loc.name}</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
          </div>
        ))}
      </div>
    </div>
  );
};
