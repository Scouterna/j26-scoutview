// src/App.jsx
import React, { useState } from 'react'; // Import useState
import { useKeycloak } from '@react-keycloak/web';

function AppContent() {
  const { keycloak, initialized } = useKeycloak();
  const [apiMessage, setApiMessage] = useState(''); // State to hold API response

  if (!initialized) {
    return <div>Loading Keycloak...</div>;
  }

  const callApi = async () => {
    if (!keycloak.authenticated) {
      setApiMessage('You must be logged in to call the API.');
      return;
    }

    try {
      // Get the access token
      const token = keycloak.token;
      if (!token) {
        setApiMessage('No token found. Please log in.');
        return;
      }

      const response = await fetch('/api/userinfo', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`, // Crucial: Add the Bearer token
        },
      });

      if (response.ok) {
        const data = await response.json();
        setApiMessage(`API Response: ${JSON.stringify(data, null, 2)}`);
      } else {
        const errorText = await response.text();
        setApiMessage(`API Error: ${response.status} - ${errorText}`);
      }
    } catch (error) {
      console.error('Error calling API:', error);
      setApiMessage(`Failed to call API: ${error.message}`);
    }
  };

  return (
    <div style={{ padding: '20px', fontFamily: 'Arial, sans-serif' }}>
      <h1>React Keycloak Integration Example</h1>

      {!keycloak.authenticated && (
        <button
          onClick={() => keycloak.login()}
          style={{ padding: '10px 20px', fontSize: '16px', cursor: 'pointer' }}
        >
          Login
        </button>
      )}

      {keycloak.authenticated && (
        <div>
          <p>
            Welcome,{' '}
            <strong>{keycloak.tokenParsed?.preferred_username || 'User'}</strong>!
          </p>
          <p>You are authenticated.</p>
          <button
            onClick={() => keycloak.logout()}
            style={{
              padding: '10px 20px',
              fontSize: '16px',
              cursor: 'pointer',
              marginRight: '10px',
            }}
          >
            Logout
          </button>
          {/* <button
            onClick={() => keycloak.updateToken(70).then((refreshed) => {
              if (refreshed) {
                console.log('Token was successfully refreshed');
                alert('Token was successfully refreshed!');
              } else {
                console.log('Token is still valid, no refresh needed');
                alert('Token is still valid, no refresh needed.');
              }
            }).catch((err) => {
              console.error('Failed to refresh token', err);
              alert('Failed to refresh token: ' + err);
            })}
            style={{ padding: '10px 20px', fontSize: '16px', cursor: 'pointer', marginRight: '10px' }}
          >
            Refresh Token (if needed)
          </button> */}

          <button
            onClick={callApi}
            style={{ padding: '10px 20px', fontSize: '16px', cursor: 'pointer', backgroundColor: '#4CAF50', color: 'white', border: 'none' }}
          >
            Call userinfo API
          </button>

          {apiMessage && (
            <div style={{ marginTop: '20px', border: '1px solid #ccc', padding: '15px', backgroundColor: '#f9f9f9', borderRadius: '5px' }}>
              <h3>API Call Result:</h3>
              <pre>{apiMessage}</pre>
            </div>
          )}

          <h3>Your Token Information:</h3>
          <pre style={{ whiteSpace: 'pre-wrap', wordBreak: 'break-all', backgroundColor: '#f0f0f0', padding: '10px', borderRadius: '5px' }}>
            {JSON.stringify(keycloak.tokenParsed, null, 2)}
          </pre>
        </div>
      )}
    </div>
  );
}

export default AppContent;