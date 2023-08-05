import typing
from abc import ABC, abstractmethod

from auto_ml_openai_sdk.pipeline.utils.data_classes import DataSet


class BasePreprocessor(ABC):
    @typing.no_type_check
    @abstractmethod
    def preprocess(
        self, path, prompt_col_name: str, completion_col_name: str
    ) -> DataSet:
        """Abstract method for preprocessing.

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
        raise NotImplementedError()
