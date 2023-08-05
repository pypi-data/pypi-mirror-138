from auto_ml_openai_sdk.pipeline.preprocessor import BasePreprocessor
from auto_ml_openai_sdk.pipeline.preprocessor.openai_gpt3_preprocessor import (
    OpenaiGpt3Preprocessor,
)
from auto_ml_openai_sdk.pipeline.utils import PipelineInputError
from auto_ml_openai_sdk.pipeline.utils.log import logging


class PreprocessorFactory:
    def __init__(self) -> None:
        self.log = logging.getLogger("pipeline.preprocessor.factory")

    def build(self, preprocessor_type: str) -> BasePreprocessor:
        """Initialise preprocessor based on the type.

        Parameters
        ----------
        preprocessor_type : str
            to determine which preprocessor to return

        Returns
        -------
        BasePreprocessor
            implementation of the abstract BasePreprocessor

        """
        self.log.info("building {} preprocessor ...".format(preprocessor_type))
        if preprocessor_type == "openai_gpt3":
            self.log.info("built openai_gpt3 preprocessor!")
            return OpenaiGpt3Preprocessor()
        else:
            raise PipelineInputError(
                "{} preprocessor is not supported!".format(preprocessor_type)
            )
