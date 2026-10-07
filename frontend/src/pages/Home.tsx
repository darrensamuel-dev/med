import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { UploadBox } from '../components/UploadBox';
import { Disclaimer } from '../components/Disclaimer';
import { submitAnalysis } from '../services/api';
import { Stethoscope, Loader2 } from 'lucide-react';

export const Home: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const [notes, setNotes] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();

  const handleAnalyze = async () => {
    if (!file) {
      setError("Please select a chest X-ray image to analyze.");
      return;
    }
    setError(null);
    setLoading(true);
    try {
      const result = await submitAnalysis(file, notes);
      navigate('/analysis', { state: { result } });
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Network error. Is the backend running?");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto space-y-8">
      <div className="text-center space-y-2">
        <h2 className="text-3xl font-extrabold text-navy-dark">Diagnostic Image Analysis</h2>
        <p className="text-gray-600 text-sm max-w-lg mx-auto">
          Upload an anterior-posterior or posterior-anterior chest radiograph to evaluate for pneumonia-associated radiographic patterns.
        </p>
      </div>

      <div className="bg-white p-8 rounded-2xl shadow-sm border border-gray-100 space-y-6">
        <div>
          <label className="block text-sm font-bold text-navy-dark mb-3">1. Upload Chest Radiograph</label>
          <UploadBox selectedFile={file} onFileSelect={(f) => { setFile(f); setError(null); }} />
        </div>

        <div>
          <label className="block text-sm font-bold text-navy-dark mb-3">2. Clinical Indications (Optional)</label>
          <textarea
            value={notes}
            onChange={(e) => setNotes(e.target.value)}
            rows={3}
            placeholder="e.g., 3-day persistent dry cough, documented fever 38.5°C..."
            className="w-full p-4 border border-gray-200 rounded-xl focus:ring-2 focus:ring-med-blue focus:border-transparent outline-none transition-all resize-none text-sm bg-gray-50 focus:bg-white"
          />
        </div>

        {error && (
          <div className="p-4 bg-red-50 border border-red-100 text-red-700 text-sm rounded-xl font-medium">
            {error}
          </div>
        )}

        <button
          onClick={handleAnalyze}
          disabled={loading || !file}
          className="w-full bg-med-blue hover:bg-blue-700 disabled:bg-gray-200 disabled:text-gray-400 text-white font-bold py-4 rounded-xl transition-colors flex items-center justify-center space-x-2 shadow-sm"
        >
          {loading ? (
            <>
              <Loader2 className="w-5 h-5 animate-spin" />
              <span>Processing Analysis...</span>
            </>
          ) : (
            <>
              <Stethoscope className="w-5 h-5" />
              <span>Evaluate Radiograph</span>
            </>
          )}
        </button>
      </div>

      <Disclaimer />
    </div>
  );
};