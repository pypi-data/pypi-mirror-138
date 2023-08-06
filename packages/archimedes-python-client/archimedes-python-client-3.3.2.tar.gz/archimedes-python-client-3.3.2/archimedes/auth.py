import os

import msal

from .configuration import api_config
from .token_cache import token_cache

SCOPES = [
    f"api://{api_config.aad_app_client_id}/.default",
]


class NoneAuth(Exception):
    """User not logged in. Please log in using `arcl auth login <organization_id>"""

    pass


class ArchimedesAuth:
    def __init__(self):
        self.app = self.build_msal_app(api_config.client_id, cache=token_cache)

    def get_access_token_silent(self):
        # We now check the cache to see
        # whether we already have some accounts that the end user already used to sign in before.
        accounts = self.app.get_accounts()
        if not accounts:
            return None

        chosen = accounts[0]
        result = self.app.acquire_token_silent(SCOPES, account=chosen)

        if result is None or "access_token" not in result:
            raise NoneAuth(
                "User not logged in. Please log in using `arcl auth login <organization_id>`."
            )

        return result.get("access_token")

    @staticmethod
    def build_msal_app(client_id, cache=None):
        return msal.PublicClientApplication(
            client_id,
            authority=api_config.authority,
            token_cache=cache,
        )


class ArchimedesConfidentialAuth:
    def __init__(self, client_id, client_credential, authority):
        self.app = self.build_confidential_msal_app(client_id, client_credential, authority)

    def get_access_token_silent(self):
        result = self.app.acquire_token_for_client(SCOPES)

        if result is None or "access_token" not in result:
            raise NoneAuth(
                "Authentication failed. Please make sure that AZURE_AD_APP_ID, AZURE_AD_APP_CLIENT_CREDENTIAL and "
                "AZURE_AD_TENANT_ID are properly configured."
            )

        return result.get("access_token")

    @staticmethod
    def build_confidential_msal_app(client_id, client_credential, authority):
        return msal.ConfidentialClientApplication(
            client_id=client_id,
            client_credential=client_credential,
            authority=authority
        )


archimedes_auth = None
use_app_authentication = os.getenv("USE_APP_AUTHENTICATION", "false").strip().lower() not in ["false", "f", "0"]
is_local = not use_app_authentication
if is_local:
    archimedes_auth = ArchimedesAuth()
else:
    azure_ad_client_id = os.getenv("AZURE_AD_APP_ID")
    azure_ad_client_credential = os.getenv("AZURE_AD_APP_CLIENT_CREDENTIAL")
    azure_ad_tenant_id = os.getenv("AZURE_AD_TENANT_ID")
    azure_ad_authority = f"https://login.microsoftonline.com/{azure_ad_tenant_id}"
    archimedes_auth = ArchimedesConfidentialAuth(azure_ad_client_id, azure_ad_client_credential, azure_ad_authority)
