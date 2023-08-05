import json
import os

import pandas as pd
import pytest
from mockito import when

from auto_ml_openai_sdk.pipeline.components import evaluation
from auto_ml_openai_sdk.pipeline.openaigpt3 import OpenAiGpt3
from auto_ml_openai_sdk.pipeline.utils.openai_tools import OpenaiTools
from auto_ml_openai_sdk.pipeline.utils.removal_helpers import remove_files

current_directory = os.path.dirname(os.path.realpath(__file__))


def build_test_data():
    records = map(
        json.loads,
        open(os.path.join(current_directory, "mock_data", "mock_data.jsonl")),
    )
    df = pd.DataFrame.from_records(records)
    df.to_json("test_data.jsonl", orient="records", lines=True)


def test_evaluation_success():
    build_test_data()
    when(OpenaiTools).predict_generation("prompt1->", "model_name", 0.5).thenReturn(
        "this is a sample completion."
    )
    when(OpenAiGpt3).get_evaluation_accuracy("job_id").thenReturn(90.0)

    # apply try out
    res = evaluation("job_id", "model_name", "test_data.jsonl", "1234", "api_key", 0.5)

    # assert
    assert res == 90.0
    assert "training_data.jsonl" not in os.listdir("./")
    assert "test_data.jsonl" in os.listdir("./")

    # remove files
    remove_files(["test_data.jsonl"])


def test_evaluation_error():
    build_test_data()
    when(OpenaiTools).predict_generation("prompt1->", "model_name", 0.5).thenRaise(
        ValueError("boom")
    )

    with pytest.raises(ValueError) as ex:
        evaluation("job_id", "model_name", "test_data.jsonl", "1234", "api_key", 0.5)
    assert str(ex.value) == "boom"

    # assert
    assert "training_data.jsonl" not in os.listdir("./")
    assert "test_data.jsonl" in os.listdir("./")

    # remove files
    remove_files(["test_data.jsonl"])
