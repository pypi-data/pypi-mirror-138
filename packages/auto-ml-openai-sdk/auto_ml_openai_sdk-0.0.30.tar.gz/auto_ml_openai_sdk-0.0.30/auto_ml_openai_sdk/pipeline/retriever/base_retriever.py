import typing
from abc import ABC, abstractmethod


class BaseRetriever(ABC):
    @typing.no_type_check
    @abstractmethod
    def retrieve(self, path: str) -> str:
        """Abstract method for retrieve.

        Parameters
        ----------
        path : str
            Fully qualified data store path (i.e. s3://store/data.csv)

        Returns
        -------
        str
            The file name (i.e. data.csv)

        """
        raise NotImplementedError()
