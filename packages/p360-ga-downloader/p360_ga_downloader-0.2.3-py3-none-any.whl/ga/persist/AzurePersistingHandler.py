import os.path
import tempfile
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient

from ga.persist.FilePersistingHandler import FilePersistingHandler


class AzurePersistingHandler(FilePersistingHandler):
    """
        Musi zvladnout ukladat na azure blob storage. A to bud pres token, 
        nebo sas, popr. muze byt bez autentikace, pokud bude model namapovany, 
        ale kdo vi, jak to bude. Prozatim teda sas a token s moznosti autentikace. 
    """

    def __init__(self, location: str, account_url, credential=DefaultAzureCredential(), sas_token: str = None):
        """
        :param account_url: "https://<my-storage-account-name>.blob.core.windows.net/
        :param credential:
        :return:
        """
        super().__init__(location)
        self.account_url = account_url
        self.credential = credential
        self.sas_token = sas_token
        #
        # if sas_token:
        #     self.blob_client = BlobServiceClient.get_blob_client()
        # self.blob_client = BlobServiceClient(account_url=account_url, credential=credential)

    # @property
    # def state(self):
    #     return {}
    #
    # @state.setter
    # def state(self, state_dict: dict):
    #     pass
    #
    def write(self, blob, filename):
        with tempfile.TemporaryDirectory() as tmpdirname:
            f = os.path.basename(filename)
            blob.download_to_filename(os.path.joinpath(tmpdirname, f), checksum=None)

            blob_service_client = BlobServiceClient.from_connection_string(...)
            container_client = blob_service_client.get_container_client("xxx")

            # Upload a blob to the container
            with open(f, "rb") as data:
                container_client.upload_blob(name=filename, data=data)
