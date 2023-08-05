from urllib.parse import urlparse

from auto_ml_openai_sdk.pipeline.retriever.base_retriever import BaseRetriever
from auto_ml_openai_sdk.pipeline.utils import S3Tools
from auto_ml_openai_sdk.pipeline.utils.log import logging


class S3Retriever(BaseRetriever):
    def __init__(self, cred_file: str = None) -> None:
        self.log = logging.getLogger("pipeline.s3retriever")
        self.s3_tools = S3Tools(cred_file)

    def retrieve(self, path: str) -> str:
        """Retrieve data from remote s3 file.

        Parameters
        ----------
        path : str
            Fully qualified data store path (i.e. s3://store/data.csv)

        Returns
        -------
        str
            The file name (i.e. data.csv)

        """
        self.log.info("retrieving from {} ...".format(path))
        file_name = self.get_file_name(path)
        self.s3_tools.download_file(path, file_name)
        self.log.info("retrieved {}!".format(file_name))
        return file_name

    @staticmethod
    def get_file_name(path: str) -> str:
        """Get file name from s3 path.

        Parameters
        ----------
        path : str
            the s3 path

        Returns
        -------
        str
            filename

        """
        s3_comp = urlparse(path)
        return s3_comp.path.split("/")[-1]
