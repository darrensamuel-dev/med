import React from 'react';
import { Outlet } from 'react-router-dom';
import { Navbar } from '../components/Navbar';

export const MainLayout: React.FC = () => {
  return (
    <div className="min-h-screen flex flex-col bg-med-bg">
      <Navbar />
      <main className="flex-1 w-full max-w-5xl mx-auto p-6 md:p-8">
        <Outlet />
      </main>
    </div>
  );
};