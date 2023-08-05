from test.auto_ml_openai_sdk.pipeline.test_training_operation_func import DotDict

import kfp
import pytest
import requests
from mockito import mock, when

from auto_ml_openai_sdk.pipeline.components import on_exit
from auto_ml_openai_sdk.pipeline.utils import PipelineInternalError

client = mock()


def mock_get_runs(
    mocked_client: object, experiment_id: str, run_name: str, is_success: bool
):
    when(kfp).Client().thenReturn(mocked_client)
    if is_success:
        when(mocked_client).list_runs(
            page_size=50, experiment_id=experiment_id, sort_by="created_at desc"
        ).thenReturn(
            DotDict(
                {
                    "runs": [
                        DotDict({"id": "run_id_1", "name": run_name}),
                        DotDict({"id": "run_id_2", "name": "run_name-2"}),
                    ]
                }
            )
        )
    else:
        when(mocked_client).list_runs(
            page_size=50, experiment_id=experiment_id, sort_by="created_at desc"
        ).thenReturn(DotDict({"runs": []}))


def mock_run_status(mocked_client: object, run_id: str, is_failed: bool):
    when(kfp).Client().thenReturn(mocked_client)

    phase = "Failed" if is_failed else "Ready"
    when(mocked_client).get_run(run_id).thenReturn(
        DotDict(
            {
                "pipeline_runtime": DotDict(
                    {
                        "workflow_manifest": """{
                                                       "status":{
                                                          "nodes":{
                                                            "step-1": {
                                                                "phase": "Ready"
                                                            },
                                                            "step-2": {
                                                                "phase": \""""
                        + phase
                        + """\"
                                                            }
                                                          }
                                                       }
                                                    }"""
                    }
                )
            }
        )
    )


def mock_callback(status_code):
    when(requests).post(
        "https://test.com/callback",
        headers={"Content-type": "application/json", "Correlation-Id": "1234"},
        params={"isOpenaiModel": True},
        data='{"aiModelRequestId": 1, "status": "FAILED", "openaiModelName": null, "details": null}',
        verify=False,
    ).thenReturn(mock({"status_code": status_code}))


def test_on_exit_success():
    mock_get_runs(client, "exp-1", "run_name", True)
    mock_run_status(client, "run_id_1", True)
    mock_callback(200)

    # apply on_exit
    on_exit(
        model_request_id=1,
        callback_service_url="https://test.com/callback",
        experiment_id="exp-1",
        run_name="run_name",
        correlation_id="1234",
    )


def test_on_exit_error_callback():
    mock_get_runs(client, "exp-1", "run_name", True)
    mock_run_status(client, "run_id_1", True)
    mock_callback(500)

    with pytest.raises(PipelineInternalError) as ex:
        # apply on_exit
        on_exit(
            model_request_id=1,
            callback_service_url="https://test.com/callback",
            experiment_id="exp-1",
            run_name="run_name",
            correlation_id="1234",
        )
    assert (
        str(ex.value)
        == '[correlation_id=1234] failed to call back with request={"aiModelRequestId": 1, '
        '"status": "FAILED", "openaiModelName": null, '
        '"details": null}!'
    )


def test_on_exit_error_no_pipeline():
    mock_get_runs(client, "exp-1", "run_name", False)

    with pytest.raises(PipelineInternalError) as ex:
        # apply on_exit
        on_exit(
            model_request_id=1,
            callback_service_url="https://test.com/callback",
            experiment_id="exp-1",
            run_name="run_name",
            correlation_id="1234",
        )
    assert str(ex.value) == "no run=run_name under experiment=exp-1"


def test_on_exit_error_run_failed():
    mock_get_runs(client, "exp-1", "run_name", True)
    mock_run_status(client, "run_id_1", False)

    on_exit(
        model_request_id=1,
        callback_service_url="https://test.com/callback",
        experiment_id="exp-1",
        run_name="run_name",
        correlation_id="1234",
    )
