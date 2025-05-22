import React from 'react';
import Toast from './Toast';
import { useAppContext } from '../context/AppContext';

const ToastContainer = () => {
  const { toasts, removeToast } = useAppContext();

  return (
    <div className="fixed top-4 right-4 space-y-2 z-50">
      {toasts.map((toast) => (
        <Toast key={toast.id} message={toast.message} onClose={() => removeToast(toast.id)} />
      ))}
    </div>
  );
};

export default ToastContainer;
