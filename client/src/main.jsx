import React from 'react';
import ReactDOM from 'react-dom/client';
import AppContent from './App.jsx';
import { ReactKeycloakProvider } from '@react-keycloak/web';
import keycloak from './keycloak.js';

const keycloakInitOptions = {
  onLoad: 'check-sso', // Can be 'login-required' or 'check-sso'
  pkceMethod: 'S256', // Recommended for SPAs
  silentCheckSsoRedirectUri: window.location.origin + '/silent-check-sso.html', // Required for silent SSO
  checkLoginIframe: true, // Enables silent token refresh
  checkLoginIframeInterval: 5, // Interval in seconds for checking session
};

ReactDOM.createRoot(document.getElementById('root')).render(
  // Important: Avoid wrapping with <React.StrictMode> directly around KeycloakProvider
  // in development, as it can cause double initialization issues with keycloak-js.
  // For production, StrictMode can be used, but ensure keycloak.init() is idempotent.
  <ReactKeycloakProvider authClient={keycloak} initOptions={keycloakInitOptions}>
    <AppContent />
  </ReactKeycloakProvider>
);