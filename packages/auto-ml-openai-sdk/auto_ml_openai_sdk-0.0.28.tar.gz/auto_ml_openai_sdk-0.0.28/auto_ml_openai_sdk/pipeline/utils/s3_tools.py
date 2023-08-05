import csv
from typing import Tuple
from urllib.parse import urlparse

import boto3


class S3Tools:
    def __init__(self, cred_file: str = None):
        if cred_file:
            self.access_key, self.secret_key = self.__read_keys_from_cred_file(
                cred_file
            )
        self.access_key = ""
        self.secret_key = ""

    def download_file(self, s3_path: str, local_path: str) -> None:
        """Download a file from the s3 store to a local path.

        Parameters
        ----------
        s3_path : str
            Fully qualified S3 store path
        local_path : str
            Fully qualified local file path

        """
        session = self.get_boto3_session()
        bucket, key = self.__parse_s3_url(s3_path)
        session.client("s3").download_file(bucket, key, local_path)

    def get_boto3_session(self) -> boto3.Session:
        """Get the aws session.

        Returns
        -------
        boto3.Session
            the aws session

        """
        session = boto3.Session(
            aws_access_key_id=self.access_key, aws_secret_access_key=self.secret_key
        )
        return session

    def set_access_key(self, key: str) -> None:
        """Set access key.

        Parameters
        ----------
        key : str
            the access key

        """
        self.access_key = key

    def set_secret_key(self, key: str) -> None:
        """Set secret key.

        Parameters
        ----------
        key : str
            the secret key

        """
        self.secret_key = key

    def upload_file(self, local_path: str, s3_path: str) -> None:
        """Write a local file to the s3 store.

        Parameters
        ----------
        local_path : str
            Fully qualified local file path
        s3_path : str
            Fully qualified S3 store path

        """
        session = self.get_boto3_session()
        bucket, key = self.__parse_s3_url(s3_path)
        session.client("s3").upload_file(Filename=local_path, Bucket=bucket, Key=key)

    def __parse_s3_url(self, url: str) -> Tuple[str, str]:
        """Parse s3 url to bucket and key.

        Parameters
        ----------
        url : str
            the s3 url

        Returns
        -------
        Tuple[str, str]
            bucket ana key

        """
        s3_components = urlparse(url)
        bucket = str(s3_components.netloc)
        key = str(s3_components.path)[1:]

        return bucket, key

    def __read_keys_from_cred_file(self, cred_file: str) -> Tuple[str, str]:
        """Read keys from cred file.

        Parameters
        ----------
        cred_file : str
            the location of the cred file

        Returns
        -------
        Tuple[str, str]
            access_key ana secret_key

        """
        with open(cred_file, newline="") as csvfile:
            cred_reader = csv.reader(csvfile, delimiter=",")
            next(cred_reader)
            for row in cred_reader:
                access_key = row[2]
                secret_key = row[3]
                break
        return access_key, secret_key
