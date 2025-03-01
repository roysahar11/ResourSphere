// This is a React-based frontend application for ResourSphere
// File: src/App.js

import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import LoginPage from './pages/LoginPage';
import Dashboard from './pages/Dashboard';
import EC2Page from './pages/EC2Page';
import S3Page from './pages/S3Page';
import DNSPage from './pages/DNSPage';
import SettingsPage from './pages/SettingsPage';
import Navbar from './components/Navbar';
import { AuthProvider, useAuth } from './contexts/AuthContext';

const darkTheme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#90caf9',
    },
    secondary: {
      main: '#f48fb1',
    },
  },
});

function ProtectedRoute({ children }) {
  const { isAuthenticated } = useAuth();
  
  if (!isAuthenticated) {
    return <Navigate to="/login" />;
  }
  
  return children;
}

function App() {
  return (
    <ThemeProvider theme={darkTheme}>
      <CssBaseline />
      <AuthProvider>
        <Router>
          <Routes>
            <Route path="/login" element={<LoginPage />} />
            <Route path="/" element={
              <ProtectedRoute>
                <Navbar />
                <Dashboard />
              </ProtectedRoute>
            } />
            <Route path="/ec2" element={
              <ProtectedRoute>
                <Navbar />
                <EC2Page />
              </ProtectedRoute>
            } />
            <Route path="/s3" element={
              <ProtectedRoute>
                <Navbar />
                <S3Page />
              </ProtectedRoute>
            } />
            <Route path="/dns" element={
              <ProtectedRoute>
                <Navbar />
                <DNSPage />
              </ProtectedRoute>
            } />
            <Route path="/settings" element={
              <ProtectedRoute>
                <Navbar />
                <SettingsPage />
              </ProtectedRoute>
            } />
          </Routes>
        </Router>
      </AuthProvider>
    </ThemeProvider>
  );
}

export default App;