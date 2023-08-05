import os
from zipfile import ZipFile

import boto3
import pandas as pd
import pytest
from mockito import when
from moto import mock_s3

from auto_ml_openai_sdk.pipeline.components import data_preparation
from auto_ml_openai_sdk.pipeline.retriever import CloudRetriever
from auto_ml_openai_sdk.pipeline.utils import PipelineInputError, S3Tools
from auto_ml_openai_sdk.pipeline.utils.removal_helpers import remove_files

current_directory = os.path.dirname(os.path.realpath(__file__))


def put_data_in_s3(file_name: str, s3_path: str):
    data_path = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "mock_data",
            file_name,
        )
    )
    s3 = boto3.client("s3", region_name="us-east-1")
    s3.create_bucket(Bucket="test_bucket")
    S3Tools().upload_file(data_path, s3_path)


@mock_s3
def test_data_preparation_success_s3_retriever_needs_split():
    # putting data to mock s3
    put_data_in_s3("mock_data_good_need_split.zip", "s3://test_bucket/mock_data.zip")

    # apply data prep
    data_preparation(
        "s3://test_bucket/mock_data.zip",
        "s3",
        "openai_gpt3",
        "1234",
        "wiki_page",
        "med",
        "training_data.jsonl",
        "test_data.jsonl",
    )

    # assert
    assert sum(1 for _ in open("training_data.jsonl")) == 42
    assert sum(1 for _ in open("test_data.jsonl")) == 7

    # remove files
    remove_files(["training_data.jsonl", "test_data.jsonl"])


@mock_s3
def test_data_preparation_success_s3_retriever_no_split():
    # putting data to mock s3
    put_data_in_s3("mock_data_good_no_split.zip", "s3://test_bucket/mock_data.zip")

    # apply data prep
    data_preparation(
        "s3://test_bucket/mock_data.zip",
        "s3",
        "openai_gpt3",
        "1234",
        "wiki_page",
        "med",
        "training_data.jsonl",
        "test_data.jsonl",
    )

    # assert
    assert sum(1 for _ in open("training_data.jsonl")) == 10
    assert sum(1 for _ in open("test_data.jsonl")) == 2

    # remove files
    remove_files(["training_data.jsonl", "test_data.jsonl"])


@mock_s3
def test_data_preparation_error_s3_retriever_not_exist_in_s3():
    with pytest.raises(Exception) as ex:
        data_preparation(
            "s3://test_bucket/mock_data.zip",
            "s3",
            "openai_gpt3",
            "1234",
            "wiki_page",
            "med",
            "training_data.jsonl",
            "test_data.jsonl",
        )
    assert (
        str(ex.value) == "An error occurred (NoSuchBucket) when calling the HeadObject "
        "operation: The specified bucket does not exist"
    )


@mock_s3
def test_data_preparation_error_s3_retriever_wrong_file_name():
    # putting data to mock s3
    put_data_in_s3("mock_data_error_wrong_name.zip", "s3://test_bucket/mock_data.zip")

    with pytest.raises(PipelineInputError) as ex:
        data_preparation(
            "s3://test_bucket/mock_data.zip",
            "s3",
            "openai_gpt3",
            "1234",
            "wiki_page",
            "med",
            "training_data.jsonl",
            "test_data.jsonl",
        )
    assert str(ex.value) == "training data=training_data.csv is not in mock_data.zip !"


@mock_s3
def test_data_preparation_error_s3_retriever_not_zip_file_extension():
    # putting data to mock s3
    put_data_in_s3("mock_data_good_need_split.zip", "s3://test_bucket/mock_data.csv")

    with pytest.raises(PipelineInputError) as ex:
        data_preparation(
            "s3://test_bucket/mock_data.csv",
            "s3",
            "openai_gpt3",
            "1234",
            "wiki_page",
            "med",
            "training_data.jsonl",
            "test_data.jsonl",
        )
    assert str(ex.value) == "mock_data.csv is not a zip file!"


@mock_s3
def test_data_preparation_error_s3_retriever_not_zip_file():
    # putting data to mock s3
    put_data_in_s3("mock_data.csv", "s3://test_bucket/mock_data.zip")

    with pytest.raises(PipelineInputError) as ex:
        data_preparation(
            "s3://test_bucket/mock_data.zip",
            "s3",
            "openai_gpt3",
            "1234",
            "wiki_page",
            "med",
            "training_data.jsonl",
            "test_data.jsonl",
        )
    assert str(ex.value) == "mock_data.zip is not a zip file!"


def test_data_preparation_error_wrong_retriever_type():
    with pytest.raises(PipelineInputError) as ex:
        data_preparation(
            "s3://test_bucket/mock_data.csv",
            "wrong_drive",
            "openai_gpt3",
            "1234",
            "wiki_page",
            "med",
            "training_data.jsonl",
            "test_data.jsonl",
        )
    assert str(ex.value) == "wrong_drive retriever is not supported!"


def test_data_preparation_error_wrong_preprocessor_type():
    with pytest.raises(PipelineInputError) as ex:
        data_preparation(
            "s3://test_bucket/mock_data.csv",
            "s3",
            "wrong_preprocessor",
            "1234",
            "wiki_page",
            "med",
            "training_data.jsonl",
            "test_data.jsonl",
        )
    assert str(ex.value) == "wrong_preprocessor preprocessor is not supported!"


def test_data_preparation_success_cloud_retriever_needs_split():
    # mock cloud retrieve and download
    pd.read_csv(os.path.join(current_directory, "mock_data", "mock_data.csv")).to_csv(
        "training_data.csv", index=None
    )
    with ZipFile("mock_data.zip", "w") as zipObj:
        zipObj.write("training_data.csv")
    when(CloudRetriever).download_file("https://www.dropbox.com/blah").thenReturn(
        "mock_data.zip"
    )

    # apply data prep
    data_preparation(
        "https://www.dropbox.com/blah",
        "cloud",
        "openai_gpt3",
        "1234",
        "wiki_page",
        "med",
        "training_data.jsonl",
        "test_data.jsonl",
    )

    # assert
    assert sum(1 for _ in open("training_data.jsonl")) == 42
    assert sum(1 for _ in open("test_data.jsonl")) == 7

    # remove files
    remove_files(["training_data.jsonl", "test_data.jsonl"])
