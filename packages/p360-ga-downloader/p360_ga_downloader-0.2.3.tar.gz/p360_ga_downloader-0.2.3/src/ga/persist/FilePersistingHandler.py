import json
import logging
import os


class FilePersistingHandler:
    """
    Persisting handler for storing data into local storage. This version just manage state for each
    downloaded file
    """
    logging.getLogger(__name__).addHandler(logging.NullHandler())

    def __init__(self, location: str):
        self.location = location

    def _create_directory_if_not_exists(self, path):
        if not os.path.exists(path):
            os.makedirs(path)

    @property
    def state(self) -> dict:
        """
        Returns dict representation of state file or empty dict if not present
        Returns:
            dict:
        """
        logging.info('Loading state file..')
        state_file_path = os.path.join(self.location, 'state.json')
        self._create_directory_if_not_exists(self.location)
        if not os.path.isfile(state_file_path):
            logging.info('State file not found. First run?')
            return {}
        try:
            with open(state_file_path, 'r') \
                    as state_file:
                return json.load(state_file)
        except (OSError, IOError):
            raise ValueError(
                "State file state.json unable to read "
            )

    @state.setter
    def state(self, state_dict: dict):
        """
        Stores [state file](https://developers.keboola.com/extend/common-interface/config-file/#state-file).
        Args:
            state_dict (dict):
        """
        if not isinstance(state_dict, dict):
            raise TypeError('Dictionary expected as a state file datatype!')

        self._create_directory_if_not_exists(self.location)
        with open(os.path.join(self.location, 'state.json'), 'w+') as state_file:
            json.dump(state_dict, state_file)

    def write(self, blob, filename):
        """ Write external files to the local storage """
        download_location = os.path.join(self.location, filename)
        download_directory = os.path.dirname(download_location)

        logging.info(f'Downloading GA data to the file: ' + download_location)

        self._create_directory_if_not_exists(download_directory)
        blob.download_to_filename(download_location, checksum=None)
