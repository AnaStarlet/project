import os
from keycloak import KeycloakAdmin, KeycloakOpenID
from keycloak.exceptions import KeycloakAuthenticationError, KeycloakGetError
from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from typing import Optional

KEYCLOAK_URL = os.getenv("KEYCLOAK_URL", "http://localhost:8080")
KEYCLOAK_REALM = os.getenv("KEYCLOAK_REALM", "notes")
KEYCLOAK_CLIENT_ID = os.getenv("KEYCLOAK_CLIENT_ID", "notes client")
KEYCLOAK_CLIENT_SECRET = os.getenv("KEYCLOAK_CLIENT_SECRET", "")

keycloak_openid = KeycloakOpenID(
    server_url=KEYCLOAK_URL,
    client_id=KEYCLOAK_CLIENT_ID,
    realm_name=KEYCLOAK_REALM,
    client_secret_key=KEYCLOAK_CLIENT_SECRET
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_keycloak_admin():
    admin = KeycloakAdmin(
        server_url=KEYCLOAK_URL,
        username="admin",
        password="admin",
        realm_name="master",
        client_id="admin-cli",
        verify=True
    )
    admin.realm_name = KEYCLOAK_REALM
    return admin


def verify_token(token: str):
    try:
        token_info = keycloak_openid.introspect(token)
        if not token_info.get("active", False):
            return None
        return token_info
    except Exception as e:
        return None


def get_current_user(token: str = Depends(oauth2_scheme)):
    token_info = verify_token(token)
    if not token_info:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        user_info = keycloak_openid.userinfo(token)
        return {
            "id": token_info.get("sub"),
            "username": user_info.get("preferred_username"),
            "email": user_info.get("email"),
            "roles": token_info.get("realm_access", {}).get("roles", [])
        }
    except Exception:
        return {
            "id": token_info.get("sub"),
            "username": token_info.get("preferred_username"),
            "email": token_info.get("email"),
            "roles": token_info.get("realm_access", {}).get("roles", [])
        }


def get_user_info(token: str):
    try:
        user_info = keycloak_openid.userinfo(token)
        return user_info
    except Exception:
        return None


def logout(token: str):
    try:
        keycloak_openid.logout(token)
        return True
    except Exception:
        return False


def refresh_token(refresh_token: str):
    try:
        token = keycloak_openid.refresh_token(refresh_token)
        return token
    except Exception:
        return None