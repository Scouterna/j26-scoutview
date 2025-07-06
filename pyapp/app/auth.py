import os

import httpx
from async_lru import alru_cache
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JOSEError, jwt

from .config import get_settings  # Import get_settings
from .models import User

AUTH_DISABLED = os.getenv("AUTH_DISABLED", "false").lower() == "true"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token", auto_error=not AUTH_DISABLED)


@alru_cache(maxsize=1)
async def get_keycloak_jwks():
    """
    Fetches and caches Keycloak's JSON Web Key Set (JWKS) using an async HTTP client.
    The result is cached to avoid repeated network calls.
    """
    settings = get_settings()
    # Construct the OIDC discovery URL
    discovery_url = f"{settings.keycloak_url}/realms/{settings.keycloak_realm}/.well-known/openid-configuration"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(discovery_url)
            response.raise_for_status()  # Raise an exception for HTTP errors
            discovery_data = response.json()
            jwks_uri = discovery_data.get("jwks_uri")
            if not jwks_uri:
                raise ValueError("JWKS URI not found in OIDC discovery document.")

            jwks_response = await client.get(jwks_uri)
            jwks_response.raise_for_status()
            return jwks_response.json()
    except httpx.RequestError as e:
        raise RuntimeError(f"Failed to fetch Keycloak JWKS: {e}") from e
    except ValueError as e:
        raise RuntimeError(f"Invalid Keycloak OIDC configuration: {e}") from e


async def get_active_user(token: str = Depends(oauth2_scheme)) -> User:
    """
    Validates a Keycloak issued JWT token and returns the active user.
    """
    if not token and AUTH_DISABLED:
        # For development/testing when auth is disabled, return a default user with admin role
        return User(username="dev@scouterna.se", roles=["admin"])

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        settings = get_settings()
        jwks = await get_keycloak_jwks()

        # Decode and validate the token
        # audience (aud) should be the client_id configured in Keycloak
        # issuer (iss) should be the Keycloak realm URL
        decoded_token = jwt.decode(
            token,
            jwks,
            algorithms=["RS256"],  # Keycloak typically uses RS256
            # audience=settings.keycloak_client_id,
            audience="account",
            issuer=f"{settings.keycloak_url}/realms/{settings.keycloak_realm}",
        )

        username = decoded_token.get("preferred_username", decoded_token.get("email"))
        if username is None:
            raise credentials_exception

        # Extract roles
        roles = []
        # Prioritize client-specific roles if available
        client_resource_access = decoded_token.get("resource_access", {}).get(settings.keycloak_client_id, {})
        if client_resource_access and "roles" in client_resource_access:
            roles.extend(client_resource_access["roles"])
        else:
            # Fallback to realm roles
            realm_access = decoded_token.get("realm_access", {})
            if realm_access and "roles" in realm_access:
                roles.extend(realm_access["roles"])

        return User(username=username, roles=roles)

    except JOSEError as e:
        # This catches various JWT errors (e.g., invalid signature, expired token, invalid audience/issuer)
        print(f"JWT validation error: {e}")  # Log the error for debugging
        raise credentials_exception
    except RuntimeError as e:
        # This catches errors during JWKS fetching or invalid Keycloak config
        print(f"Keycloak configuration error: {e}")  # Log the error for debugging
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server configuration error: Could not fetch Keycloak public keys.",
        )
    except Exception as e:
        # Catch any other unexpected errors
        print(f"An unexpected error occurred during authentication: {e}")
        raise credentials_exception
