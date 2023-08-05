from dataclasses import dataclass

import os
from azure.identity import ClientSecretCredential


@dataclass
class AzureAuthProvider:

    url = "https://{}.blob.core.windows.net".format(
        os.getenv("AZURE_STORAGE_ACCOUNT_NAME")
    )

    connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    shared_access_key = os.getenv("AZURE_STORAGE_ACCESS_KEY")
    active_directory_application_id = os.getenv("ACTIVE_DIRECTORY_APPLICATION_ID")
    active_directory_application_secret = os.getenv("ACTIVE_DIRECTORY_APPLICATION_SECRET")
    active_directory_tenant_id = os.getenv("ACTIVE_DIRECTORY_TENANT_ID")

    def auth_active_directory(self):
        # [START create_blob_service_client_oauth]
        # Get a token credential for authentication

        return ClientSecretCredential(
            self.active_directory_tenant_id,
            self.active_directory_application_id,
            self.active_directory_application_secret
        )
