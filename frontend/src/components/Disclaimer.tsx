import React from 'react';
import { ShieldAlert } from 'lucide-react';

export const Disclaimer: React.FC = () => {
  return (
    <div className="bg-amber-50 border-l-4 border-amber-600 p-4 rounded-r-md mt-6">
      <div className="flex items-start">
        <ShieldAlert className="w-5 h-5 text-amber-600 mt-0.5 mr-3 flex-shrink-0" />
        <p className="text-xs text-amber-900 leading-relaxed">
          <strong>Clinical Research Prototype:</strong> MedGuide is an AI-assisted research prototype intended to support professional review. It is not a medical diagnosis and must not replace qualified medical judgment.
        </p>
      </div>
    </div>
  );
};