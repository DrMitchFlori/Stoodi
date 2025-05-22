import React from 'react';
import { Link, useLocation } from 'react-router-dom';

const MobileBottomNav = () => {
  const location = useLocation();
  const items = [
    { path: '/', label: 'Dashboard' },
    { path: '/tutor', label: 'Tutor' },
    { path: '/library', label: 'Library' }
  ];

  return (
    <nav className="md:hidden fixed bottom-0 left-0 right-0 bg-white shadow-inner h-16 flex justify-around items-center">
      {items.map(item => (
        <Link
          key={item.path}
          to={item.path}
          className={location.pathname === item.path ? 'text-primary font-semibold' : 'text-gray-600'}
        >
          {item.label}
        </Link>
      ))}
    </nav>
  );
};

export default MobileBottomNav;
