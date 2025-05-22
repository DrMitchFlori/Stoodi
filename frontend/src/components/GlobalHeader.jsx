import React from 'react';
import { Link } from 'react-router-dom';

const GlobalHeader = () => (
  <header className="bg-primary text-white h-16 flex items-center px-4">
    <h1 className="text-xl font-semibold mr-4">LumLearn</h1>
    <nav className="space-x-4">
      <Link to="/" className="hover:underline">Dashboard</Link>
      <Link to="/tutor" className="hover:underline">Tutor</Link>
      <Link to="/library" className="hover:underline">Library</Link>
    </nav>
  </header>
);

export default GlobalHeader;
