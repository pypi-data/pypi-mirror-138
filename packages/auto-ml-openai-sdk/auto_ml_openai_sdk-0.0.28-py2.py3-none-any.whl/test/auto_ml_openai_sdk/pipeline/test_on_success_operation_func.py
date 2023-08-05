import pytest
import requests
from mockito import mock, when

from auto_ml_openai_sdk.pipeline.components import on_success
from auto_ml_openai_sdk.pipeline.utils import PipelineInternalError


def mock_callback(status_code):
    when(requests).post(
        "https://test.com/callback",
        headers={"Content-type": "application/json", "Correlation-Id": "1234"},
        params={"isOpenaiModel": True},
        data='{"aiModelRequestId": 1, "status": "READY", "openaiModelName": "openai_model_name", '
        '"details": {"performance": [{"name": "validation_metrics", "metrics": {"accuracy": 0.9}}]}}',
        verify=False,
    ).thenReturn(mock({"status_code": status_code}))


def test_on_success_success():
    mock_callback(200)

    # apply on_success
    on_success(
        model_request_id=1,
        callback_service_url="https://test.com/callback",
        openai_model_name="openai_model_name",
        correlation_id="1234",
        evaluation_accuracy=0.9,
    )


def test_on_success_error():
    mock_callback(500)

    with pytest.raises(PipelineInternalError) as ex:
        # apply on_success
        on_success(
            model_request_id=1,
            callback_service_url="https://test.com/callback",
            openai_model_name="openai_model_name",
            correlation_id="1234",
            evaluation_accuracy=0.9,
        )
    assert (
        str(ex.value)
        == '[correlation_id=1234] failed to call back with request={"aiModelRequestId": 1, '
        '"status": "READY", "openaiModelName": "openai_model_name", '
        '"details": {"performance": [{"name": "validation_metrics", "metrics": {"accuracy": 0.9}}]}}!'
    )
