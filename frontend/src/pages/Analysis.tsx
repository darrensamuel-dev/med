import React from 'react';
import { useLocation, Link } from 'react-router-dom';
import { AnalysisResponse } from '../types';
import { Disclaimer } from '../components/Disclaimer';
import { ArrowLeft, CheckCircle2, AlertCircle } from 'lucide-react';

const MOCK_DATA: AnalysisResponse = {
  finding: "PNEUMONIA",
  confidence: 0.91,
  original_image: "https://images.unsplash.com/photo-1516549655169-df83a0774514?auto=format&fit=crop&w=400&q=80",
  heatmap: "https://images.unsplash.com/photo-1516549655169-df83a0774514?auto=format&fit=crop&w=400&q=80",
  image_evidence: "The highlighted region indicates the area that contributed most to this prediction.",
  clinical_evidence: "Patient notes mention persistent cough and fever.",
  assessment: "Doctor, consider this finding: the model detected features associated with pneumonia with 91% confidence. The highlighted region indicates the area that contributed most to this prediction.",
  openrouter_summary: null,
};

export const Analysis: React.FC = () => {
  const location = useLocation();
  const isMock = !location.state?.result;
  const data: AnalysisResponse = location.state?.result || MOCK_DATA;

  const isPneumonia = data.finding === "PNEUMONIA";

  return (
    <div className="max-w-5xl mx-auto space-y-6">
      <div className="flex items-center justify-between">
        <Link to="/" className="inline-flex items-center text-sm font-medium text-med-blue hover:underline">
          <ArrowLeft className="w-4 h-4 mr-1" /> Back to Upload
        </Link>
        {isMock && (
          <span className="bg-amber-100 text-amber-800 text-xs px-2.5 py-1 rounded font-semibold">
            Demo Placeholder Data
          </span>
        )}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 bg-white p-6 rounded-lg border border-gray-200">
        <div>
          <h3 className="text-sm font-semibold text-navy-dark mb-2">Original Chest Radiograph</h3>
          <div className="bg-black rounded overflow-hidden aspect-square flex items-center justify-center">
            <img
              src={data.original_image}
              alt="Original X-ray"
              className="w-full h-full object-contain"
            />
          </div>
        </div>

        <div>
          <h3 className="text-sm font-semibold text-navy-dark mb-2">AI Evidence / Heatmap</h3>
          <div className="bg-black rounded overflow-hidden aspect-square flex items-center justify-center">
            <img
              src={data.heatmap}
              alt="AI Grad-CAM Attribution Heatmap"
              className="w-full h-full object-contain"
            />
          </div>
          <p className="text-xs text-gray-500 mt-2 italic text-center">
            Region contributing to the model prediction (Grad-CAM). Not a clinical segmentation mask.
          </p>
        </div>
      </div>

      <div className="bg-white p-6 rounded-lg border border-gray-200 space-y-5">
        <div className="flex items-center justify-between border-b border-gray-100 pb-4">
          <div>
            <span className="text-xs font-semibold text-gray-500 uppercase tracking-wider">Classification Assessment</span>
            <div className="flex items-center space-x-2 mt-1">
              {isPneumonia ? (
                <AlertCircle className="w-6 h-6 text-red-600" />
              ) : (
                <CheckCircle2 className="w-6 h-6 text-green-600" />
              )}
              <h2 className="text-2xl font-bold text-navy-dark">{data.finding}</h2>
            </div>
          </div>
          <div className="text-right">
            <span className="text-xs font-semibold text-gray-500 uppercase tracking-wider">Prediction Confidence</span>
            <p className="text-2xl font-bold text-med-blue mt-1">
              {(data.confidence * 100).toFixed(0)}%
            </p>
          </div>
        </div>

        <div>
          <h4 className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-2">Attribution Evidence</h4>
          <ul className="space-y-2 text-sm text-navy-dark">
            <li className="flex items-start">
              <span className="text-med-blue mr-2">✓</span>
              <span><strong>Image Evidence:</strong> {data.image_evidence}</span>
            </li>
            {data.clinical_evidence && (
              <li className="flex items-start">
                <span className="text-med-blue mr-2">✓</span>
                <span><strong>Clinical Context:</strong> {data.clinical_evidence}</span>
              </li>
            )}
          </ul>
        </div>

        <div className="bg-med-lightblue border border-blue-200 rounded p-4">
          <h4 className="text-xs font-semibold text-navy-primary uppercase tracking-wider mb-1">Doctor's Consideration</h4>
          <p className="text-sm text-navy-dark leading-relaxed font-medium">
            "{data.assessment}"
          </p>
        </div>
        {data.openrouter_summary && (
          <div className="rounded border border-slate-200 bg-slate-50 p-4">
            <h4 className="mb-1 text-xs font-semibold uppercase tracking-wider text-navy-primary">
              OpenRouter summary
            </h4>
            <p className="text-sm leading-relaxed text-navy-dark">{data.openrouter_summary}</p>
          </div>
        )}
      </div>

      <Disclaimer />
    </div>
  );
};