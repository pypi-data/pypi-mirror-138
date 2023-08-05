from urllib.parse import urlparse

import wget

from auto_ml_openai_sdk.pipeline.retriever.base_retriever import BaseRetriever
from auto_ml_openai_sdk.pipeline.utils.log import logging


class CloudRetriever(BaseRetriever):
    def __init__(self) -> None:
        self.log = logging.getLogger("pipeline.cloudretriever")

    def retrieve(self, path: str) -> str:
        """Retrieve data from remote cloud file such as dropbox (not s3).

        Parameters
        ----------
        path : str
            Data store path in cloud

        Returns
        -------
        str
            The file name (i.e. data.csv)

        """
        self.log.info("retrieving from {} ...".format(path))
        file_name = self.download_file(path)
        self.log.info("retrieved {}!".format(file_name))
        return file_name

    def download_file(self, url: str) -> str:
        """Download a file from url.

        Parameters
        ----------
        url : str
            url of the file

        Returns
        -------
        str
            local filename

        """
        local_filename = self.get_file_name(url)
        wget.download(url, out=local_filename)
        return local_filename

    @staticmethod
    def get_file_name(path: str) -> str:
        """Get file name from cloud path.

        Parameters
        ----------
        path : str
            the cloud path

        Returns
        -------
        str
            filename

        """
        cloud_comp = urlparse(path)
        return cloud_comp.path.split("/")[-1]
