import requests

from auto_ml_openai_sdk.pipeline.components.helper import get_logger
from auto_ml_openai_sdk.pipeline.utils import CallbackRequest, PipelineInternalError


class CallbackClient:
    def __init__(self, base_url: str) -> None:
        self.log = get_logger("pipeline.callback.client")
        self.base_url = base_url
        self.correlation_id_header_key = "Correlation-Id"

    def callback(self, callback_request: CallbackRequest, correlation_id: str) -> None:
        """Call auto-mltd-svc callback endpoint.

        Parameters
        ----------
        callback_request : CallbackRequest
            the request obj for callback
        correlation_id : str
            an id to link everything

        """
        headers = self.create_headers(correlation_id)
        params = self.create_params()
        response = requests.post(
            self.base_url,
            headers=headers,
            params=params,  # type: ignore
            data=callback_request.to_json(),  # type: ignore
            verify=False,
        )
        if response.status_code == 200:
            self.log.info(
                "[correlation_id={}] call back with request={} succeeds!".format(
                    correlation_id, callback_request.to_json()  # type: ignore
                )
            )
        else:
            raise PipelineInternalError(
                "[correlation_id={}] failed to call back with request={}!".format(
                    correlation_id, callback_request.to_json()  # type: ignore
                )
            )

    def create_headers(self, correlation_id: str) -> object:
        """Create headers for callback endpoint.

        Parameters
        ----------
        correlation_id : str
            an id to link everything

        Returns
        -------
        object
            headers object

        """
        headers = {
            "Content-type": "application/json",
            self.correlation_id_header_key: correlation_id,
        }
        return headers

    @staticmethod
    def create_params() -> object:
        """Create params for callback endpoint.

        Returns
        -------
        object
            params object

        """
        params = {"isOpenaiModel": True}
        return params
