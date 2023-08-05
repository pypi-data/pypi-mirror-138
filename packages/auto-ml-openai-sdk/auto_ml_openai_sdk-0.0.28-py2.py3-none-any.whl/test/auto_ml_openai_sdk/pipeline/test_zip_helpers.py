import os
import shutil
from zipfile import ZipFile

import pandas as pd

from auto_ml_openai_sdk.pipeline.utils import create_tar_archive, unzip, zip_dir


def test_unzip():
    # create a temp zip of a file
    pd.DataFrame([{"data": "a"}, {"data": "b"}]).to_csv("test_data.csv", index=None)
    with ZipFile("test_data.zip", "w") as zipObj:
        zipObj.write("test_data.csv")
    os.remove("test_data.csv")

    # unzip it
    unzip("test_data.zip")

    # assert unzip file
    assert "test_data.csv" in os.listdir("./")

    # remove unzip file
    os.remove("test_data.csv")
    os.remove("test_data.zip")


def test_zip_dir():
    # create a temp dir
    os.makedirs("test_dir", exist_ok=True)
    pd.DataFrame([{"data": "a"}, {"data": "b"}]).to_csv(
        "test_dir/test_data.csv", index=None
    )

    # zip it
    zip_dir("test_dir", "", "")

    # assert zip exists
    assert "test_dir.zip" in os.listdir("./")

    # remove zip file
    shutil.rmtree("test_dir")
    os.remove("test_dir.zip")


def test_create_tar_archive():
    # create a temp file
    pd.DataFrame([{"data": "a"}, {"data": "b"}]).to_csv("test_data.csv", index=None)

    # create tar
    create_tar_archive(["test_data.csv"], "test_tar.tar")

    # assert tared file
    assert "test_tar.tar" in os.listdir("./")

    # remove unzip file
    os.remove("test_data.csv")
    os.remove("test_tar.tar")
