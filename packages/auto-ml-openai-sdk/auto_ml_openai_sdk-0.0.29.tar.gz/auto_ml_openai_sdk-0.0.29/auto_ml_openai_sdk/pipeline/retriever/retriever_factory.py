from auto_ml_openai_sdk.pipeline.retriever.base_retriever import BaseRetriever
from auto_ml_openai_sdk.pipeline.retriever.cloud_retriever import CloudRetriever
from auto_ml_openai_sdk.pipeline.retriever.s3_retriever import S3Retriever
from auto_ml_openai_sdk.pipeline.utils import PipelineInputError
from auto_ml_openai_sdk.pipeline.utils.log import logging


class RetrieverFactory:
    def __init__(self) -> None:
        self.log = logging.getLogger("pipeline.retriever.factory")

    def build(self, retriever_type: str) -> BaseRetriever:
        """Initialise retriever based on the type.

        Parameters
        ----------
        retriever_type : str
            to determine which retriever to return

        Returns
        -------
        BaseRetriever
            implementation of the abstract BaseRetriever

        """
        self.log.info("building {} retriever ...".format(retriever_type))
        if retriever_type == "s3":
            self.log.info("built S3Retriever!")
            return S3Retriever()
        elif retriever_type == "cloud":
            self.log.info("built CloudRetriever!")
            return CloudRetriever()
        else:
            raise PipelineInputError(
                "{} retriever is not supported!".format(retriever_type)
            )
