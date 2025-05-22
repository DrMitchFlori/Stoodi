import React, { createContext, useContext, useState, useEffect } from 'react';

const AppContext = createContext();

export const AppProvider = ({ children }) => {
  const [currentUser, setCurrentUser] = useState({ name: 'Student' });
  const [notifications, setNotifications] = useState([]);
  const [isOffline, setIsOffline] = useState(false);
  const [toasts, setToasts] = useState([]);

  const addToast = (message) => {
    setToasts((prev) => [...prev, { id: Date.now(), message }]);
  };

  const removeToast = (id) => {
    setToasts((prev) => prev.filter((t) => t.id !== id));
  };

  useEffect(() => {
    const handleOffline = () => setIsOffline(true);
    const handleOnline = () => setIsOffline(false);
    window.addEventListener('offline', handleOffline);
    window.addEventListener('online', handleOnline);
    return () => {
      window.removeEventListener('offline', handleOffline);
      window.removeEventListener('online', handleOnline);
    };
  }, []);

  return (
    <AppContext.Provider
      value={{ currentUser, notifications, isOffline, toasts, addToast, removeToast }}
    >
      {children}
    </AppContext.Provider>
  );
};

export const useAppContext = () => useContext(AppContext);
