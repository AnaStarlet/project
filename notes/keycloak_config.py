import os
from keycloak import KeycloakOpenID, KeycloakAdmin

KEYCLOAK_SERVER_URL = os.getenv("KEYCLOAK_SERVER_URL", "http://localhost:8080")
KEYCLOAK_REALM = os.getenv("KEYCLOAK_REALM", "notes-realm")
KEYCLOAK_CLIENT_ID = os.getenv("KEYCLOAK_CLIENT_ID", "notes-client")
KEYCLOAK_CLIENT_SECRET = os.getenv("KEYCLOAK_CLIENT_SECRET", "your-client-secret")

keycloak_openid = KeycloakOpenID(
    server_url=KEYCLOAK_SERVER_URL,
    client_id=KEYCLOAK_CLIENT_ID,
    realm_name=KEYCLOAK_REALM,
    client_secret_key=KEYCLOAK_CLIENT_SECRET
)

def get_keycloak_user_info(token: str):
    try:
        userinfo = keycloak_openid.userinfo(token)
        return userinfo
    except Exception as e:
        return None


def validate_keycloak_token(token: str):
    try:
        token_info = keycloak_openid.introspect(token)
        return token_info.get('active', False)
    except Exception as e:
        return False


def create_keycloak_user(username: str, email: str, password: str):
    admin = KeycloakAdmin(
        server_url=KEYCLOAK_SERVER_URL,
        username="admin",
        password="admin123",
        realm_name=KEYCLOAK_REALM,
        client_id=KEYCLOAK_CLIENT_ID,
        client_secret_key=KEYCLOAK_CLIENT_SECRET,
        verify=True
    )

    user = {
        "username": username,
        "email": email,
        "enabled": True,
        "emailVerified": False,
        "credentials": [{
            "type": "password",
            "value": password,
            "temporary": False
        }]
    }

    user_id = admin.create_user(user)
    return user_id