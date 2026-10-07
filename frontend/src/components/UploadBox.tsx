import React, { useRef } from 'react';
import { Upload, FileCheck } from 'lucide-react';

interface UploadBoxProps {
  selectedFile: File | null;
  onFileSelect: (file: File) => void;
}

export const UploadBox: React.FC<UploadBoxProps> = ({ selectedFile, onFileSelect }) => {
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleDragOver = (e: React.DragEvent) => e.preventDefault();

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const file = e.dataTransfer.files[0];
      if (file.type === 'image/jpeg' || file.type === 'image/png') onFileSelect(file);
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) onFileSelect(e.target.files[0]);
  };

  return (
    <div
      onDragOver={handleDragOver}
      onDrop={handleDrop}
      onClick={() => fileInputRef.current?.click()}
      className="group border-2 border-dashed border-gray-300 hover:border-med-blue bg-gray-50 hover:bg-med-lightblue rounded-xl p-10 text-center cursor-pointer transition-all duration-200 flex flex-col items-center justify-center min-h-[240px]"
    >
      {/* THIS CLASS HIDES THE DEFAULT BROWSER INPUT */}
      <input
        type="file"
        ref={fileInputRef}
        onChange={handleFileChange}
        accept=".jpg,.jpeg,.png,image/jpeg,image/png"
        className="hidden" 
      />
      
      {selectedFile ? (
        <div className="flex flex-col items-center space-y-2">
          <div className="bg-green-100 p-3 rounded-full">
            <FileCheck className="w-8 h-8 text-green-600" />
          </div>
          <span className="font-semibold text-navy-dark">{selectedFile.name}</span>
          <span className="text-sm text-gray-500">{(selectedFile.size / 1024).toFixed(1)} KB</span>
          <span className="text-sm text-med-blue font-medium mt-2 group-hover:underline">Click to change image</span>
        </div>
      ) : (
        <div className="flex flex-col items-center space-y-3">
          <div className="bg-white p-4 rounded-full shadow-sm border border-gray-100 group-hover:border-blue-200 transition">
            <Upload className="w-8 h-8 text-med-blue" />
          </div>
          <div>
            <p className="text-base font-semibold text-navy-dark">Click to upload or drag and drop</p>
            <p className="text-sm text-gray-500 mt-1">JPEG or PNG (max. 10MB)</p>
          </div>
        </div>
      )}
    </div>
  );
};