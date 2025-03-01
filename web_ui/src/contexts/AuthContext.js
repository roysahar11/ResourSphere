// File: src/contexts/AuthContext.js

import React, { createContext, useContext, useState, useEffect } from 'react';
import api from '../services/api';

const AuthContext = createContext();

export function useAuth() {
  return useContext(AuthContext);
}

export function AuthProvider({ children }) {
  const [currentUser, setCurrentUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('token'));
  const [userPermissions, setUserPermissions] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check if token exists and is valid
    if (token) {
      // Set the token in the API service
      api.setToken(token);
      
      // Try to get user permissions to verify token is valid
      api.getUserPermissions()
        .then(permissions => {
          setUserPermissions(permissions);
          setCurrentUser(localStorage.getItem('username'));
        })
        .catch(() => {
          // If token is invalid, clear it
          logout();
        })
        .finally(() => {
          setLoading(false);
        });
    } else {
      setLoading(false);
    }
  }, [token]);

  const login = async (username, password) => {
    try {
      const response = await api.login(username, password);
      const { access_token, user_permissions, expires_at_utc } = response;
      
      localStorage.setItem('token', access_token);
      localStorage.setItem('username', username);
      localStorage.setItem('tokenExpiry', expires_at_utc);
      
      setToken(access_token);
      setCurrentUser(username);
      setUserPermissions(user_permissions);
      
      return true;
    } catch (error) {
      console.error('Login failed:', error);
      return false;
    }
  };

  const logout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('username');
    localStorage.removeItem('tokenExpiry');
    setToken(null);
    setCurrentUser(null);
    setUserPermissions(null);
  };

  const value = {
    currentUser,
    userPermissions,
    isAuthenticated: !!currentUser,
    login,
    logout,
  };

  return (
    <AuthContext.Provider value={value}>
      {!loading && children}
    </AuthContext.Provider>
  );
}