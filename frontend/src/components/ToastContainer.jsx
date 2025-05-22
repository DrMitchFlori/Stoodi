import React, { useState, useCallback } from 'react';
import Toast from './Toast';

let idCounter = 0;

const ToastContainer = () => {
  const [toasts, setToasts] = useState([]);

  const addToast = useCallback((message) => {
    setToasts((prev) => [...prev, { id: idCounter++, message }]);
  }, []);

  const removeToast = useCallback((id) => {
    setToasts((prev) => prev.filter((t) => t.id !== id));
  }, []);

  return (
    <div className="fixed top-4 right-4 space-y-2 z-50">
      {toasts.map((toast) => (
        <Toast key={toast.id} message={toast.message} onClose={() => removeToast(toast.id)} />
      ))}
    </div>
  );
};

export default ToastContainer;
