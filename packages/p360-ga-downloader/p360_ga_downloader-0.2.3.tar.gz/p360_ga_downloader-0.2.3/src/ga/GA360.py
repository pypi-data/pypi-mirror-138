import google
import logging
import multiprocessing
import os
import re
import sys
import time
from datetime import datetime, timedelta
from google.cloud import bigquery, storage
from google.oauth2 import service_account

from ga.auth.GoogleAuthProvider import GoogleAuthProvider
from ga.exceptions.NotFound import NotFound
from ga.model.Dataset import Dataset
from ga.persist.FilePersistingHandler import FilePersistingHandler
from ga.utils.list_utils import split


class GA360:
    """
    GA360 is module covering the Google Analytics 360 data platform. It use several API
    to keep data jobs simple and easy.

    @version 0.1.8
    @author Datasentics a.s.
    """
    logging.getLogger(__name__).addHandler(logging.NullHandler())

    GOOGLE_COMPOSED_REQUEST_OBJECT_COUNT = 32

    def __init__(self, project_name
                 , gcp_project_id
                 , gcp_bucket_name
                 , gcp_bucket_folder
                 , gcp_dataset_id
                 , gcp_table_id
                 , gcp_service_account_key_file
                 , gcp_dataset_alias=None):

        self.project_name = project_name
        self.gcp_project_id = gcp_project_id
        self.gcp_bucket_name = gcp_bucket_name
        self.gcp_bucket_folder = gcp_bucket_folder
        self.gcp_dataset_id = gcp_dataset_id
        self.gcp_dataset_alias = gcp_dataset_alias
        self.gcp_table_id = gcp_table_id
        self.gcp_service_account_key_file = gcp_service_account_key_file

        self.credentials = service_account.Credentials.from_service_account_info(
            gcp_service_account_key_file)

    @property
    def storage(self):
        """ Google Storage Client """
        return storage.Client(credentials=self.credentials)

    @property
    def bigquery(self):
        """ Google Big Query Client """
        return bigquery.Client(credentials=self.credentials)

    @property
    def gcp_file_name_mask(self):
        """ File mask for dataset """
        return self.gcp_dataset_id + '_' + self.gcp_table_id

    @property
    def _build_extractor_job_config(self):
        """ Default extractor setting. Store data into AVRO-SNAPPY compression """
        job_config = bigquery.ExtractJobConfig()
        job_config.compression = bigquery.Compression.SNAPPY
        job_config.destination_format = bigquery.DestinationFormat.AVRO

        return job_config

    def extract_bigquery_table_to_storage(self, extractor_setting=None):
        """
        Export the BigQuery table to Google Storage.
        By default it is exported as AVRO-SNAPPY, but this setting is possible to
        overwrite by set up the @param extractor_settings. For more @see GA360._build_extractor_job_config
        """
        extractor_setting = extractor_setting if extractor_setting else self._build_extractor_job_config

        # Setting Destination path in Google Storage
        filename = self.gcp_file_name_mask + '*' + '.avro'

        destination_uri = 'gs://{}/{}/{}'.format(self.gcp_bucket_name, self.gcp_bucket_folder, filename)
        logging.info('Data are exported to the path: ' + destination_uri)

        dataset = "{}.{}".format(self.gcp_project_id, self.gcp_dataset_id)
        dataset_ref = self.bigquery.get_dataset(dataset)
        table_ref = dataset_ref.table(self.gcp_table_id)

        try:
            # Export JOB
            extract_job = self.bigquery.extract_table(
                table_ref,
                destination_uri,
                location='EU',  # Location must match that of the source table.
                job_config=extractor_setting)  # API request

            extract_job.result()  # Waits for job to complete.
            logging.info('Exported {}:{}.{} to {}'
                         .format(self.gcp_project_id, self.gcp_dataset_id, self.gcp_table_id, destination_uri))
        except google.api_core.exceptions.NotFound as nf:
            raise NotFound(nf.message)

        return filename

    def _available_blobs(self):
        """
        Retrieve list of available blobs to working with
        """
        return list(filter(lambda blob: blob.name.find(self.gcp_file_name_mask) >= 0,
                           self.storage
                           .get_bucket(self.gcp_bucket_name)
                           .list_blobs(prefix=self.gcp_bucket_folder))
                    )

    def merge_files_on_google_storage(self):
        """
        Merge google avro files (shards) into one file
        """
        logging.info(
            f"Merge all files with mask {self.gcp_file_name_mask} in the folder {self.gcp_bucket_folder}")

        # Composition allows merge only 32 objects together
        compose_chunks = split(self._available_blobs(), self.GOOGLE_COMPOSED_REQUEST_OBJECT_COUNT)
        logging.debug(f"file split into {compose_chunks}")
        paths = []

        for i, chunks in enumerate(compose_chunks):
            gcp_merged_file_name_full_path = f"{self.gcp_bucket_folder}/{self.gcp_file_name_mask}_{i}.avro"
            paths.append(gcp_merged_file_name_full_path)
            logging.info(f'Files merged into file: {gcp_merged_file_name_full_path}')

            self.storage.get_bucket(self.gcp_bucket_name) \
                .blob(gcp_merged_file_name_full_path) \
                .compose(chunks)

        return paths

    def download_file_to_location(self, filename: str, writer: FilePersistingHandler):
        """
        Download file from Google Storage to download location.

        :param writer:
        :param filename:
        :return:
        """
        _filename = ""
        for blob in self._available_blobs():
            _filename = blob.name.replace('/', '_').replace(self.gcp_bucket_folder + '_', '')
            _to_download_filename = os.path.join(self.gcp_dataset_alias, _filename)
            self._download_blob_to_location(blob, _to_download_filename, writer)

        return _filename

    def _download_blob_to_location(self, blob, filename: str, writer: FilePersistingHandler):
        try:
            writer.write(blob, filename)
            # time to retrieve file from memory to disk
            time.sleep(5)
            return blob
        except google.cloud.exceptions.NotFound:
            logging.warning(f'WARN - not possible to download file {blob.name}, file does not exists')

    def delete_files_on_google_storage(self):
        """
        Deletes a blob from Cloud Storage.
        """
        logging.info(f"Delete all files with mask {self.gcp_file_name_mask} in the folder {self.gcp_bucket_folder}")

        try:
            for blob in self._available_blobs():
                if blob.name.find(self.gcp_file_name_mask) >= 0:
                    logging.info(f'Delete file {blob.name} from {self.gcp_bucket_folder}')
                    blob.delete()
        except google.cloud.exceptions.NotFound:
            pass
            # to distracting warning, no usage for user
            # logging.warning(f'WARN - not possible to delete blobs for bucket {self.gcp_bucket_folder}')

    def bucket_cleanup(self):
        """ Bucket cleanup, its handy both before or after data manipulations to prevent duplications of data"""
        try:
            bucket = self.storage.get_bucket(self.gcp_bucket_name)
            return bucket.delete_blobs(blobs=self.gcp_bucket_folder)
        except google.cloud.exceptions.NotFound:
            pass
            # too distracting warning, no usage for user
            # logging.warning(f'WARN - not possible to delete blobs for bucket {self.gcp_bucket_folder}')


class TimeSeries:
    """
    This class keeps time related task out of business for GA360 component.
    It helps manage time series for GA360 in correct format without polluting
    simple code of main package

    Related for GA360
    """
    time_series_log = logging.getLogger(__name__)

    FORMAT = '%Y%m%d'

    @classmethod
    def is_date(cls, date: str) -> bool:
        """"
        Check acceptable date format. Only valid format is as @cls.FORMAT
        """
        try:
            datetime.strptime(date, cls.FORMAT)
            return True
        except ValueError:
            return False

    @classmethod
    def to_date(cls, date: str) -> datetime:
        """ Convert date string into datetime by format @cls.FORMAT"""
        return datetime.strptime(str(date), cls.FORMAT)

    @classmethod
    def to_string(cls, date: datetime):
        """ Convert date into string with format @cls.FORMAT"""
        return date.strftime(cls.FORMAT)

    @classmethod
    def move_by(cls, date: datetime, days: int = 1) -> datetime:
        """
        Move date by number of @days into the future
        :param date: base date which will be moved
        :param days: number of days to move by, as default is one day
        :return: moved date
        """
        return date + timedelta(days=days)

    @classmethod
    def next_day(cls, date: datetime) -> datetime:
        """ Give a next date for passed date """
        return cls.move_by(date, days=1)

    @classmethod
    def date_from(cls, previous_date: datetime, manual_forced_date: str = None) -> datetime:
        """

        :param previous_date:
        :param manual_forced_date:
        :return:
        """
        if manual_forced_date and cls.is_date(manual_forced_date):
            cls.time_series_log.debug(f"'FROM_DATE' is forced to value '{manual_forced_date}'")
            return cls.to_date(manual_forced_date)

        cls.time_series_log.debug(f"'FROM_DATE' is set to value '{previous_date}'")
        return cls.next_day(previous_date)

    @classmethod
    def date_to(cls, latest_date: datetime, manual_forced_date: str = None) -> datetime:
        if manual_forced_date and cls.is_date(manual_forced_date):
            cls.time_series_log.debug(f"'TO_DATE' is forced to value '{manual_forced_date}'")
            return cls.to_date(manual_forced_date)

        cls.time_series_log.debug(f"'TO_DATE' is forced to value '{latest_date}'")
        return latest_date

    @classmethod
    def date_between(cls, start_date: datetime, end_date: datetime) -> list:
        """ Return list of dates between @start_date and @end_date"""
        print(start_date, end_date)
        return [start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1)]


class Ga360Builder:

    def __init__(self):
        self.__project = ""
        self.__dataset_id_list = {}
        self.__dataset_list = []
        self.__bucket_folder = self.__bucket_name = ""
        self.__table_name = ""

        self.__multiprocessing = False
        self.__number_of_processors = multiprocessing.cpu_count()

        self.__persisting_handler = None
        self.__service_key = None
        self.__auth = None

    def project(self, project_id):
        self.__project = project_id
        return self

    def bucket(self, bucket_name, bucket_folder):
        self.__bucket_name = bucket_name
        self.__bucket_folder = bucket_folder
        return self

    def dataset(self, dataset_id):
        """
        Datasets setter. This accept several types of input
            <li>str: single dataset id</li>
            <li>list[str]: list of ids for several datasets</li>
            <li>dict[str, str]: key of dict is dataset alias, @see example section</li>

        @example: I assume, that input look like {'alias': dataset_id}, where alias is name of
        folder, where files will be downloaded and dataset_id is id of downloaded dataset
        """

        # case 1. single values
        if isinstance(dataset_id, str):
            self.__dataset_list.append(Dataset(dataset_id, ""))
            print("str")
            return self

        # case 2. list of single values
        if isinstance(dataset_id, list):
            print(f"list {dataset_id}")
            self.__dataset_list.extend([Dataset(d, "") for d in dataset_id])

        # case 3 dict {alias: }
        if isinstance(dataset_id, dict):
            self.__dataset_list.extend([Dataset(d, a) for a, d in dataset_id.items()])

        return self

    def table(self, table_name):
        self.__table_name = table_name
        return self

    def service_key(self, service_key: dict):
        """ @deprecated since 20.10.2021 """
        self.__service_key = service_key
        return self

    def multiprocessing(self, is_active=True, number_of_processors=multiprocessing.cpu_count()):
        self.__multiprocessing = is_active
        self.__number_of_processors = number_of_processors
        return self

    def persist(self, persisting_handle: FilePersistingHandler):
        self.__persisting_handler = persisting_handle
        return self

    def auth(self, file: str = None,
             private_key: str = None, private_key_id: str = None,
             client_id: str = None, client_email: str = None):

        self.__auth = (
            GoogleAuthProvider.from_json(file) if file
            else GoogleAuthProvider(project_id=self.__project, private_key=private_key,
                                    private_key_id=private_key_id,
                                    client_id=client_id, client_email=client_email)
        )
        return self

    def __validate(self):
        pass

    def build(self, force=False):
        force or self.__validate()

        # validate before
        return self.GA360Handler(
            self.__project
            , self.__dataset_list
            , self.__bucket_name
            , self.__bucket_folder
            # since 20.10.2021, for backward compatibility
            , self.__auth.service_key if not self.__service_key else self.__service_key
            , self.__persisting_handler)

    class GA360Handler:

        def __init__(self, project_id: str, dataset: list, bucket_name: str, bucket_folder: str,
                     service_key, persisting_handler):
            self.gcp_project_id = project_id
            self.gcp_ga_datasets = dataset
            self.gcp_bucket_name = bucket_name
            self.gcp_bucket_folder = bucket_folder
            self.gcp_service_account_key_file = service_key
            self.persisting_handler = persisting_handler
            self.state = self.persisting_handler.state

        def ga360_extractor(self, gcp_ga360_session_table_id, gcp_dataset_id, gcp_dataset_alias=None) -> GA360:
            """ Build GA360 extractor for session """
            return GA360(
                self.gcp_project_id
                , self.gcp_project_id
                , self.gcp_bucket_name
                , self.gcp_bucket_folder
                , gcp_dataset_id
                , gcp_ga360_session_table_id
                , self.gcp_service_account_key_file
                , gcp_dataset_alias
            )

        def last_date_in_stored_dataset(self, gcp_dataset_id):
            """
            Explore state file for latest processing date for given dataset
            :param gcp_dataset_id:
            :return:
            """
            state = self.persisting_handler.state
            return state.get(gcp_dataset_id)['date'] if state.get(gcp_dataset_id) \
                else TimeSeries.to_string(TimeSeries.move_by(datetime.now(), days=-20))

        def job_sequence_for_dataset(self, extractor: GA360):
            """
            Sequence of tasks for reaching out files from Google Analytics Storage
            :param extractor:
            :return:
            """

            try:
                # 1. Exporting Google BigQuery table to Google Storage
                extractor.extract_bigquery_table_to_storage()

                # 2. Create package for download, omitted due large file limitation
                # exported_tbl_filename_list = extractor.merge_files_on_google_storage()
                # for exported_tbl_filename in exported_tbl_filename_list:

                # 3. download files from remote to local
                extractor.download_file_to_location(None, writer=self.persisting_handler)

                # 5. drop files from remote location
                extractor.delete_files_on_google_storage()
                logging.info('DONE - Deleting files on Google Storage')

                # return exported_tbl_filename
            except NotFound as notFound:
                logging.warning(f'{notFound.message}. Skip for now.')
            except AssertionError as error:
                logging.error(
                    f'ERROR: Unexpected error during exporting table stage: {extractor.gcp_table_id}')
            finally:
                extractor.delete_files_on_google_storage()
                logging.info('Not downloaded, only deleted.')

        def fetch_daily_dataset(self, gcp_dataset: Dataset, pointer_date: datetime):
            """
            Download daily dump for given dataset and date
            """

            ga_sessions_table_suffix = TimeSeries.to_string(pointer_date)
            logging.info(
                'Processing table for date: ' + ga_sessions_table_suffix)

            # creating path to a BigQuery table 'projectId.dataset.tablename specific for GA360
            gcp_ga360_session_table_id = "ga_sessions_" + ga_sessions_table_suffix

            return self.job_sequence_for_dataset(
                extractor=self.ga360_extractor(gcp_ga360_session_table_id, gcp_dataset.id, gcp_dataset.alias)
            )

        def fetch_latest_and_cleanup(self, days_back=None):
            self.fetch_latest(days_back)
            self.cleanup()

        def fetch_and_cleanup(self, period_date_from_manual=None, period_date_to_manual=None):
            self.fetch(period_date_from_manual, period_date_to_manual)
            self.cleanup()

        def fetch_latest(self, days_back=None):
            """
            Perform extraction process. It does download all data newer than @param days_back days.
            f.e. it usable, when you are interest into all data no older than 14 days inc.

            :example GA360(...).fetch_latest(days_back = 14)
            :param days_back:
            :return:
            """
            from_date = TimeSeries.move_by(datetime.now(), days=-days_back)
            return self.fetch(period_date_from_manual=TimeSeries.to_string(from_date))

        def fetch(self, period_date_from_manual=None, period_date_to_manual=None):
            """
            Perform extraction process
            :return:
            """

            # start with empty bucket folder for prevent duplication of data
            self.cleanup()

            # latest data, which can be extracted from GA is -1 day old, so
            # yesterday date works as limiter for latest dataset available
            yesterday_date = TimeSeries.move_by(datetime.now(), days=-1)
            ga_sessions_table_suffix = TimeSeries.to_string(yesterday_date)

            logging.debug('GA Session date: ' + str(ga_sessions_table_suffix) + ' will be used.')

            # @memo note, that parallelism can be applied even here, but heavy part is extracting so
            # better have more threads in network ops than just counting time series
            for dataset in self.gcp_ga_datasets:
                # Load will start by the next day of the last processed date (if set manually then use manual setting)
                start_date = self.last_date_in_stored_dataset(dataset.id)
                period_date_from = TimeSeries.date_from(TimeSeries.to_date(start_date), period_date_from_manual)
                logging.debug(f"Start date for dataset {dataset.id} is set to {period_date_from}")

                # Load will end by the yesterday (if set manually then use manual setting)
                period_date_to = TimeSeries.date_to(yesterday_date, period_date_to_manual)

                with multiprocessing.Pool(multiprocessing.cpu_count()) as pool:
                    time_series_to_download = TimeSeries.date_between(period_date_from, period_date_to)
                    gcp_dataset_for_each_process = [dataset] * len(time_series_to_download)

                    processed_dates = (list(pool.starmap(
                        self.fetch_daily_dataset,
                        zip(gcp_dataset_for_each_process, time_series_to_download)
                    )))

                    # remove None values from list and make a new one with dates only
                    processed_dates = list(filter(None, processed_dates))

                if processed_dates:
                    last_date_string = TimeSeries.to_date(max([re.split('_|\.', x)[-2] for x in processed_dates])) \
                        .strftime(TimeSeries.FORMAT)
                    self.state.update({dataset.id: {"date": last_date_string}})

            # write updated state file
            logging.debug(f"Writing up state file with content: {self.state}")
            self.persisting_handler.state = self.state

        def cleanup(self):
            """ Drop all generated files from google storage """
            self.ga360_extractor(None, None).bucket_cleanup()
