from typing import NamedTuple

from kfp.components import InputPath, OutputPath


def data_preparation(
    raw_data_path: str,
    retriever_type: str,
    preprocessor_type: str,
    correlation_id: str,
    prompt_col_name: str,
    completion_col_name: str,
    training_fet_path: OutputPath(str),  # type: ignore
    test_fet_path: OutputPath(str),  # type: ignore
) -> None:
    """Apply data preparation function on the data.

    Parameters
    ----------
    raw_data_path : str
        the path of the data
    retriever_type : str
        type of the retriever to use based on the data location, for example: s3, cloud
    preprocessor_type : str
        the type of preprocessor to use, example: openai_gpt3
    correlation_id : str
        an id to link everything
    prompt_col_name : str
        the name of the column in the dataframe which will be used as prompt
    completion_col_name : str
        the name of the column in the dataframe which will be used as completion
    test_fet_path : OutputPath(str)
        path where the test feature will be saved, can leave empty
    training_fet_path : OutputPath(str)
        path where the training feature will be saved, can leave empty

    """
    from auto_ml_openai_sdk.pipeline.components.helper import get_logger
    from auto_ml_openai_sdk.pipeline.preprocessor import PreprocessorFactory, save_jsonl
    from auto_ml_openai_sdk.pipeline.retriever.retriever_factory import RetrieverFactory

    log = get_logger("pipeline.components.data_preparation")
    try:
        log.info(
            "[correlation_id={}] Start the data preparation step...".format(
                correlation_id
            )
        )

        retriever_factory = RetrieverFactory()
        preprocessor_factory = PreprocessorFactory()

        retriever = retriever_factory.build(retriever_type)
        preprocessor = preprocessor_factory.build(preprocessor_type)

        compression_data = retriever.retrieve(raw_data_path)
        data = preprocessor.preprocess(
            compression_data,
            prompt_col_name=prompt_col_name,
            completion_col_name=completion_col_name,
        )

        save_jsonl(
            data.training_data, training_fet_path, prompt_col_name, completion_col_name
        )
        save_jsonl(data.test_data, test_fet_path, prompt_col_name, completion_col_name)

        log.info(
            "training_fet_path={}, test_fet_path={}".format(
                training_fet_path, test_fet_path
            )
        )

    except Exception:
        log.exception(
            "[correlation_id={}] Error happened during the data preparation step!".format(
                correlation_id
            )
        )
        raise


def training(
    training_fet_path: InputPath(str),  # type: ignore
    test_fet_path: InputPath(str),  # type: ignore
    correlation_id: str,
    openai_api_key: str,
    base_model: str = "curie",
) -> NamedTuple("model_training_output", [("job_id", str), ("model_name", str)]):  # type: ignore
    """Apply fine-tuning on the training data.

    Parameters
    ----------
    training_fet_path : InputPath(str)
        the path of the training feature
    test_fet_path : InputPath(str)
        the path of the test feature
    base_model : str
        base model for openai model
    correlation_id : str
        an id to link everything
    openai_api_key : str
        api key for openai

    Returns
    -------
    object
        the fine-tune job_id and model name

    """
    from collections import namedtuple

    from auto_ml_openai_sdk.pipeline.components.helper import get_logger
    from auto_ml_openai_sdk.pipeline.openaigpt3 import OpenAiGpt3

    log = get_logger("pipeline.components.training")
    try:
        log.info(
            "[correlation_id={}] Start the training step... training_fet_path: {}, test_fet_path = {}".format(
                correlation_id, training_fet_path, test_fet_path
            )
        )

        openai_gpt3 = OpenAiGpt3(openai_api_key)
        job_id, model_name = openai_gpt3.fine_tune(
            training_fet_path, test_fet_path, correlation_id, base_model
        )

        log.info(
            "[correlation_id={}] fine-tuned job_id = {} and model name = {}".format(
                correlation_id, job_id, model_name
            )
        )

        model_training_output = namedtuple(
            "model_training_output", ["job_id", "model_name"]
        )
        return model_training_output(job_id, model_name)

    except Exception:
        log.exception(
            "[correlation_id={}] Error happened during the training step!".format(
                correlation_id
            )
        )
        raise


def evaluation(
    job_id: str,
    model_name: str,
    test_fet_path: InputPath(str),  # type: ignore
    correlation_id: str,
    openai_api_key: str,
    temperature: float = 0.5,
) -> float:
    """Evaluate fine-tuned/trained model.

    Parameters
    ----------
    job_id : str
        id of the fine-tune job
    model_name : str
        name of the fine-tuned model
    test_fet_path : InputPath(str)
        the path of the test data
    correlation_id : str
        an id to link everything
    temperature : float
        the temperature value
    openai_api_key : str
        api key for openai

    Returns
    -------
    float
        evaluation accuracy

    """
    import json

    import pandas as pd

    from auto_ml_openai_sdk.pipeline.components.helper import get_logger
    from auto_ml_openai_sdk.pipeline.openaigpt3 import OpenAiGpt3

    log = get_logger("pipeline.components.evaluation")
    try:
        log.info(
            "[correlation_id={}] Start the evaluation step...".format(correlation_id)
        )

        records = map(json.loads, open(test_fet_path))
        df = pd.DataFrame.from_records(records)

        openai_gpt3 = OpenAiGpt3(openai_api_key)
        if len(df) > 0:
            prompt = df.iloc[0].prompt

            log.info("[correlation_id={}] prompt = {}".format(correlation_id, prompt))

            completion = openai_gpt3.predict(model_name, prompt, temperature)

            log.info(
                "[correlation_id={}] completion = {}".format(correlation_id, completion)
            )
        else:
            log.info(
                "[correlation_id={}] no prompt found to predict".format(correlation_id)
            )

        evaluation_accuracy = openai_gpt3.get_evaluation_accuracy(job_id)
        log.info(
            "[correlation_id={}] evaluation_accuracy = {}".format(
                correlation_id, evaluation_accuracy
            )
        )
        return evaluation_accuracy

    except Exception:
        log.exception(
            "[correlation_id={}] Error happened during the evaluation step!".format(
                correlation_id
            )
        )
        raise


def on_success(
    model_request_id: int,
    callback_service_url: str,
    openai_model_name: str,
    correlation_id: str,
    evaluation_accuracy: float,
) -> None:
    """Perform callback on success.

    Parameters
    ----------
    model_request_id : int
        request id of the model
    callback_service_url : str
        url of the callback service
    openai_model_name : str
        model name from open ai
    correlation_id : str
        an id to link everything
    evaluation_accuracy : float
        the accuracy of the evaluation

    """
    from auto_ml_openai_sdk.pipeline.clients.callback_client import CallbackClient
    from auto_ml_openai_sdk.pipeline.components.helper import get_logger
    from auto_ml_openai_sdk.pipeline.utils import (
        CallbackDetails,
        CallbackMetrics,
        CallbackPerformance,
        CallbackRequest,
        ModelRequestStatus,
    )

    log = get_logger("pipeline.components.on.success")
    try:
        log.info(
            "[correlation_id={}] Start to callback with the successful pipeline run details...".format(
                correlation_id
            )
        )

        callback_request = CallbackRequest(
            ai_model_request_id=int(model_request_id),
            openai_model_name=openai_model_name,
            status=ModelRequestStatus.READY,
            details=CallbackDetails(
                performance=[
                    CallbackPerformance(
                        name="validation_metrics",
                        metrics=CallbackMetrics(accuracy=evaluation_accuracy),
                    )
                ]
            ),
        )
        callback_client = CallbackClient(callback_service_url)
        callback_client.callback(callback_request, correlation_id)

    except Exception:
        log.exception(
            "[correlation_id={}] Error happened during the on_success step!".format(
                correlation_id
            )
        )
        raise


def on_exit(
    model_request_id: int,
    callback_service_url: str,
    experiment_id: str,
    run_name: str,
    correlation_id: str,
) -> None:
    """Perform callback on exit.

    Parameters
    ----------
    experiment_id : str
        id of the experiment in kf
    run_name : str
        run name in kf
    model_request_id : int
        request id of the model
    callback_service_url : str
        url of the callback service
    correlation_id : str
        an id to link everything

    """
    from auto_ml_openai_sdk.pipeline.clients.callback_client import CallbackClient
    from auto_ml_openai_sdk.pipeline.components.helper import (
        get_logger,
        get_pipeline_run,
        is_pipeline_run_failed,
    )
    from auto_ml_openai_sdk.pipeline.utils import (
        CallbackRequest,
        ModelRequestStatus,
        PipelineInternalError,
    )

    log = get_logger("pipeline.components.on.exit")
    try:
        run = get_pipeline_run(experiment_id, run_name)
        if not run:
            raise PipelineInternalError(
                "no run={} under experiment={}".format(run_name, experiment_id)
            )
        if is_pipeline_run_failed(run[0]):
            log.info(
                "[correlation_id={}] Start to callback with the failed pipeline run details...".format(
                    correlation_id
                )
            )
            callback_request = CallbackRequest(
                ai_model_request_id=int(model_request_id),
                status=ModelRequestStatus.FAILED,
            )
            callback_client = CallbackClient(callback_service_url)
            callback_client.callback(callback_request, correlation_id)

    except Exception:
        log.exception(
            "[correlation_id={}] Error happened during the on_exit step!".format(
                correlation_id
            )
        )
        raise
