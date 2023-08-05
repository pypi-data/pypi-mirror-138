import json
import os
from dataclasses import dataclass

from ga.exceptions.InvalidConfigurationException import InvalidConfigurationException


@dataclass
class GoogleAuthProvider:
    """ Provides the information for flawless connection to the google services """

    project_id: str
    private_key: str
    private_key_id: str
    client_id: str
    client_email: str

    @staticmethod
    def from_json(path: str):
        """
        Load Service Key for Google platform auth from json file

        :param path: Path to the json file containing the service key
        :return: GoogleAuthProvider
        :raise InvalidConfigurationException when service key is in invalid format or
            required fields ('project_id', 'private_key', 'private_key_id', 'client_id', 'client_email') missing
        :raise FileNotFoundError when file containing the service key is not available or nonexists
        """
        if not os.path.exists(path):
            raise FileNotFoundError( "The path {} cannot be found on the filesystem".format(path) )

        required_keys = ('project_id', 'private_key', 'private_key_id', 'client_id', 'client_email')
        with open(path, 'r') as service_key:
            service_key_json = json.load(service_key)
            if not all(k in service_key_json for k in required_keys):
                raise InvalidConfigurationException("Provided service key is invalid")

            return GoogleAuthProvider(
                project_id=service_key_json.get('project_id'),
                private_key=service_key_json.get('private_key'), private_key_id=service_key_json.get('private_key_id'),
                client_id=service_key_json.get('client_id'), client_email=service_key_json.get('client_email')
            )

    @property
    def service_key(self):
        return {
            "type": "service_account",
            "project_id": self.project_id,
            "private_key_id": self.private_key_id,
            "private_key": self.private_key,
            "client_email": self.client_email,
            "client_id": self.client_id,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_x509_cert_url": f"https://www.googleapis.com/robot/v1/metadata/x509/{self.client_email}"
        }
