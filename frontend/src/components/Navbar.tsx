import React from 'react';
import { Link } from 'react-router-dom';
import { Activity } from 'lucide-react';

export const Navbar: React.FC = () => {
  return (
    <header className="bg-navy-primary text-white shadow-md">
      <div className="max-w-5xl mx-auto px-6 py-4 flex items-center justify-between">
        <Link to="/" className="flex items-center space-x-3 group">
          <div className="bg-med-blue p-2 rounded-lg group-hover:bg-blue-600 transition">
            <Activity className="w-5 h-5 text-white" />
          </div>
          <div>
            <h1 className="font-bold text-lg leading-tight tracking-wide">MedGuide</h1>
            <p className="text-[11px] text-blue-200 font-medium uppercase tracking-wider">Clinical Second Opinion</p>
          </div>
        </Link>
        <nav className="flex space-x-6 text-sm font-medium">
          <Link to="/" className="text-gray-300 hover:text-white transition">Upload & Analysis</Link>
          <Link to="/analysis" className="text-gray-300 hover:text-white transition">View Case</Link>
        </nav>
      </div>
    </header>
  );
};