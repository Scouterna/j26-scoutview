import Keycloak from 'keycloak-js';

const keycloak_url = import.meta.env.DEV
  ? import.meta.env.VITE_KEYCLOAK_URL
  : window.keycloak_url;

const keycloak_realm = import.meta.env.DEV
  ? import.meta.env.VITE_KEYCLOAK_REALM
  : window.keycloak_realm;

const keycloak_client_id = import.meta.env.DEV
  ? import.meta.env.VITE_KEYCLOAK_CLIENT_ID
  : window.keycloak_client_id;

const keycloakConfig = {
  url: keycloak_url,
  realm: keycloak_realm,
  clientId: keycloak_client_id
};

const keycloak = new Keycloak(keycloakConfig);

export default keycloak;