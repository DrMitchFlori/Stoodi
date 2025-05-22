import React from 'react';
import { HashRouter, Routes, Route } from 'react-router-dom';
import { AppProvider } from './context/AppContext';
import GlobalHeader from './components/GlobalHeader';
import MobileBottomNav from './components/MobileBottomNav';
import ToastContainer from './components/ToastContainer';
import LandingDashboardPage from './pages/LandingDashboardPage';
import TutorChatWorkspacePage from './pages/TutorChatWorkspacePage';
import LibraryPage from './pages/LibraryPage';
import NotificationsPage from './pages/NotificationsPage';
import ProfilePage from './pages/ProfilePage';

const AppRoutes = () => (
  <Routes>
    <Route path="/" element={<LandingDashboardPage />} />
    <Route path="/tutor" element={<TutorChatWorkspacePage />} />
    <Route path="/library" element={<LibraryPage />} />
    <Route path="/notifications" element={<NotificationsPage />} />
    <Route path="/profile" element={<ProfilePage />} />
    <Route path="*" element={<div className="p-4">Page Not Found</div>} />
  </Routes>
);

const App = () => (
  <HashRouter>
    <AppProvider>
      <div className="flex flex-col min-h-screen">
        <GlobalHeader />
        <main className="flex-grow">
          <AppRoutes />
        </main>
        <ToastContainer />
        <MobileBottomNav />
      </div>
    </AppProvider>
  </HashRouter>
);

export default App;
