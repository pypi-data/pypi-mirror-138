import os

import pandas as pd
import pytest
from mockito import when

from auto_ml_openai_sdk.pipeline.components import training
from auto_ml_openai_sdk.pipeline.utils import PipelineInternalError
from auto_ml_openai_sdk.pipeline.utils.openai_tools import OpenaiTools
from auto_ml_openai_sdk.pipeline.utils.removal_helpers import remove_files

current_directory = os.path.dirname(os.path.realpath(__file__))


class DotDict(dict):
    """dot.notation access to dictionary attributes"""

    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


def build_train_test_data():
    pd.read_csv(os.path.join(current_directory, "mock_data", "mock_data.csv")).to_json(
        "training_data.jsonl"
    )
    pd.read_csv(os.path.join(current_directory, "mock_data", "mock_data.csv")).to_json(
        "test_data.jsonl"
    )


def mock_openai(is_error: bool = False):
    when(OpenaiTools).upload_file("training_data.jsonl").thenReturn(
        DotDict({"id": "training_data_id"})
    )
    when(OpenaiTools).upload_file("test_data.jsonl").thenReturn(
        DotDict({"id": "test_data_id"})
    )
    when(OpenaiTools).fine_tuning(
        "training_data_id", "test_data_id", "curie", 0.1, 0.1
    ).thenReturn(DotDict({"id": "fine_tuning_id"}))
    when(OpenaiTools).get_status("fine_tuning_id").thenReturn(
        DotDict(
            {
                "id": "fine_tuning_id",
                "status": "succeeded" if not is_error else "failed",
                "events": [
                    DotDict(
                        {"level": "info", "created_at": 1640259393, "message": "blah"}
                    )
                ],
                "fine_tuned_model": "fine_tuned_model_id",
            }
        )
    )


def test_training_success():
    build_train_test_data()
    mock_openai(False)

    # apply training
    res = training("training_data.jsonl", "test_data.jsonl", "1234", "api_key", "curie")

    # assert
    assert res[0] == "fine_tuning_id"
    assert res[1] == "fine_tuned_model_id"
    assert "training_data.jsonl" in os.listdir("./")
    assert "test_data.jsonl" in os.listdir("./")

    # remove files
    remove_files(["training_data.jsonl", "test_data.jsonl"])


def test_training_error():
    build_train_test_data()
    mock_openai(True)

    with pytest.raises(PipelineInternalError) as ex:
        training("training_data.jsonl", "test_data.jsonl", "1234", "api_key", "curie")

    # assert
    assert (
        str(ex.value)
        == "[correlation_id=1234] fine_tune_job (id=fine_tuning_id) failed"
    )
    assert "training_data.jsonl" in os.listdir("./")
    assert "test_data.jsonl" in os.listdir("./")

    # remove files
    remove_files(["training_data.jsonl", "test_data.jsonl"])
