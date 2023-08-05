from dataclasses import dataclass
from enum import Enum

import pandas as pd
from dataclasses_json import LetterCase, dataclass_json


@dataclass
class DataSet:
    training_data: pd.DataFrame
    test_data: pd.DataFrame


@dataclass
class DataSetPaths:
    training_data_path: str
    test_data_path: str


class ModelRequestStatus(Enum):
    READY = "READY"
    FAILED = "FAILED"


@dataclass
class CallbackMetrics:
    accuracy: float


@dataclass
class CallbackPerformance:
    name: str
    metrics: CallbackMetrics


@dataclass
class CallbackDetails:
    performance: list[CallbackPerformance]


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class CallbackRequest:
    ai_model_request_id: int
    status: ModelRequestStatus
    openai_model_name: str = None
    details: CallbackDetails = None
