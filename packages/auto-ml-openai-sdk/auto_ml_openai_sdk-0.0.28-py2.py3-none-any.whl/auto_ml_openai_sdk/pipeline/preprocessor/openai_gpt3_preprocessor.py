from auto_ml_openai_sdk.pipeline.preprocessor.base_preprocessor import BasePreprocessor
from auto_ml_openai_sdk.pipeline.preprocessor.preprocess_utils import (
    data_shuffle,
    data_split,
)
from auto_ml_openai_sdk.pipeline.utils import PipelineInputError
from auto_ml_openai_sdk.pipeline.utils.data_classes import DataSet
from auto_ml_openai_sdk.pipeline.utils.log import logging
from auto_ml_openai_sdk.pipeline.utils.removal_helpers import remove_file, remove_files
from auto_ml_openai_sdk.pipeline.utils.zip_helpers import (
    files_in_zip,
    is_zip_file,
    unzip,
)


class OpenaiGpt3Preprocessor(BasePreprocessor):
    def __init__(self) -> None:
        self.training_data_name = "training_data.csv"
        self.test_data_name = "test_data.csv"
        self.test_data_proportion = 0.15
        self.log = logging.getLogger("pipeline.preprocessor.openaigpt3")

    def preprocess(
        self, path: str, prompt_col_name: str, completion_col_name: str
    ) -> DataSet:
        """Apply required preprocessing for openai gpt3 on the provided data.

        Parameters
        ----------
        path : str
            fully qualified compression data file local path (i.e. data.zip)
        prompt_col_name : str
            column name for prompt
        completion_col_name : str
            column name for completion

        Returns
        -------
        Dataset
            contains the path for both train and test data

        """
        if not is_zip_file(path):
            remove_file(path)
            raise PipelineInputError("{} is not a zip file!".format(path))

        zip_files = files_in_zip(path)
        if self.training_data_name not in zip_files:
            remove_file(path)
            raise PipelineInputError(
                "training data={} is not in {} !".format(self.training_data_name, path)
            )

        self.log.info("unzip {}...".format(path))
        unzip(path)
        remove_file(path)

        training_data = data_shuffle(self.training_data_name)
        if self.test_data_name in zip_files:
            test_data = data_shuffle(self.test_data_name)
        else:
            training_data, test_data = data_split(
                self.training_data_name,
                self.test_data_proportion,
                prompt_col_name,
                completion_col_name,
            )
        remove_files([self.training_data_name, self.test_data_name])

        training_data = training_data[training_data[prompt_col_name].notna()]
        test_data = test_data[test_data[prompt_col_name].notna()]

        return DataSet(training_data, test_data)
