import React from 'react';
import { useAppContext } from '../context/AppContext';

const ProfilePage = () => {
  const { currentUser } = useAppContext();
  return (
    <div className="p-4">
      <h2 className="text-2xl font-semibold mb-4">Profile</h2>
      <p className="text-gray-700">Logged in as {currentUser.name}.</p>
    </div>
  );
};

export default ProfilePage;
