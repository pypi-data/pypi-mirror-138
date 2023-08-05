import json
from logging import Logger

import kfp

from auto_ml_openai_sdk.pipeline.utils import S3Tools
from auto_ml_openai_sdk.pipeline.utils.data_classes import DataSetPaths
from auto_ml_openai_sdk.pipeline.utils.log import logging


def get_logger(name: str) -> Logger:
    """Get the logger.

    Parameters
    ----------
    name : str
        a string to identify the logger

    Returns
    -------
    Logger
        logger

    """
    log = logging.getLogger(name)
    return log


def upload_data_to_s3(local_data: DataSetPaths, upload_path: str) -> DataSetPaths:
    """Upload the data to s3.

    Parameters
    ----------
    local_data : DataSetPaths
        contains path of both training and test data
    upload_path :
        s3 path where the data will be uploaded

    Returns
    -------
    DataSetPaths
        contains path of both training and test data

    """
    s3_uploader = S3Tools()
    uploaded_data = DataSetPaths(
        upload_path + "/" + local_data.training_data_path,
        upload_path + "/" + local_data.test_data_path,
    )
    s3_uploader.upload_file(
        local_data.training_data_path, uploaded_data.training_data_path
    )
    s3_uploader.upload_file(local_data.test_data_path, uploaded_data.test_data_path)
    return uploaded_data


def get_pipeline_run(experiment_id: str, run_name: str) -> list:
    """Get the pipeline using experiment_id and run_name.

    Parameters
    ----------
    experiment_id : str
        the id of the experiment from kf
    run_name : str
        the name of the run in kf

    Returns
    -------
    list
        the list of run_id for pipelines

    """
    client = kfp.Client()
    run_list = client.list_runs(
        page_size=50, experiment_id=experiment_id, sort_by="created_at desc"
    ).runs
    return [run.id for run in run_list if run.name == run_name]


def is_pipeline_run_failed(run_id: str) -> bool:
    """Whether pipeline run failed or not.

    Parameters
    ----------
    run_id : str
        the run_id from kf

    Returns
    -------
    bool
        true if failed else false

    """
    client = kfp.Client()
    runtime_manifest = client.get_run(run_id).pipeline_runtime.workflow_manifest
    runtime_manifest_json = json.loads(runtime_manifest)
    runtime_steps = runtime_manifest_json["status"]["nodes"]
    for step in runtime_steps:
        if runtime_steps[step]["phase"] == "Failed":
            return True
    return False
