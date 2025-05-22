import React, { useEffect } from 'react';

const Toast = ({ message, onClose }) => {
  useEffect(() => {
    const timer = setTimeout(onClose, 3000);
    return () => clearTimeout(timer);
  }, [onClose]);

  return (
    <div className="bg-gray-900 text-white px-4 py-2 rounded shadow">
      {message}
    </div>
  );
};

export default Toast;
