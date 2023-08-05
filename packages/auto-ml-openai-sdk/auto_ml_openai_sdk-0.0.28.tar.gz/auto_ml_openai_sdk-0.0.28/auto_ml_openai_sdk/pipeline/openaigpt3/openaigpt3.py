import time
from datetime import datetime
from io import StringIO
from typing import Tuple

import numpy as np
import pandas as pd

from auto_ml_openai_sdk.pipeline.utils import PipelineInternalError
from auto_ml_openai_sdk.pipeline.utils.formatter import clean_generation_prediction
from auto_ml_openai_sdk.pipeline.utils.log import logging
from auto_ml_openai_sdk.pipeline.utils.openai_tools import OpenaiTools


class OpenAiGpt3:
    def __init__(self, openai_api_key: str) -> None:
        self.openai_tools = OpenaiTools(openai_api_key)
        self.log = logging.getLogger("pipeline.openaigpt3.openaigpt3")

    def fine_tune(
        self,
        training_data_path: str,
        test_data_path: str,
        correlation_id: str,
        base_model: str = "curie",
    ) -> Tuple[str, str]:
        """Apply fine-tuning on the training data.

        Parameters
        ----------
        training_data_path : str
            the path of the training data
        test_data_path : str
            the path of the test data
        base_model : str
            base model for openai model
        correlation_id : str
            an id to link everything

        Returns
        -------
        Tuple[str, str]
            job_id, model_name

        """
        train_file = self.openai_tools.upload_file(training_data_path)
        self.log.info(
            "[correlation_id={}] train_file.id: {}".format(
                correlation_id, train_file.id
            )
        )
        valid_file = self.openai_tools.upload_file(test_data_path)
        self.log.info(
            "[correlation_id={}] valid_file.id: {}".format(
                correlation_id, valid_file.id
            )
        )
        ft_job = self.openai_tools.fine_tuning(
            train_file.id, valid_file.id, base_model, 0.1, 0.1
        )
        self.log.info(
            "[correlation_id={}] fine_tune_job.id: {}".format(correlation_id, ft_job.id)
        )

        ft_job_id = ft_job.id

        seen_events = set()
        while True:
            ft_job = self.openai_tools.get_status(ft_job_id)
            events = ft_job.events
            for event in events:
                event_str = (
                    f"[{event.level}:{datetime.fromtimestamp(event.created_at)}]"
                    f" {event.message}"
                )
                if event_str not in seen_events:
                    self.log.info(
                        "[correlation_id={}] fine_tune_job (id={}) status update: {}".format(
                            correlation_id, ft_job.id, event_str
                        )
                    )
                    seen_events.add(event_str)

            status = ft_job.status
            if status == "running" or status == "pending":
                time.sleep(30)
            else:
                break

        if status == "failed":
            raise PipelineInternalError(
                "[correlation_id={}] fine_tune_job (id={}) failed".format(
                    correlation_id, ft_job.id
                )
            )

        assert status == "succeeded"
        self.log.info(
            "[correlation_id={}] fine_tune_job (id={}) succeed. model_name={}".format(
                correlation_id, ft_job.id, ft_job.fine_tuned_model
            )
        )
        return ft_job_id, ft_job.fine_tuned_model

    def predict(self, model_name: str, prompt: str, temperature: float) -> str:
        """Predict and clean generation.

        Parameters
        ----------
        model_name : str
            the name of the fine-tuned model
        prompt : str
            the prompt
        temperature : float
            the value of the temperature

        Returns
        -------
        str
            the completion or generation

        """
        return clean_generation_prediction(
            self.openai_tools.predict_generation(prompt, model_name, temperature)
        )

    def get_evaluation_accuracy(self, job_id: str) -> float:
        """Get the evaluation result.

        Parameters
        ----------
        job_id : str
            finetune job id

        Returns
        -------
        float
            validation token accuracy

        """
        bytes_data = self.openai_tools.download_results_file(job_id)
        results_df = pd.read_csv(StringIO(str(bytes_data, "utf-8")))
        res = results_df["validation_token_accuracy"]
        nan_idx = np.isnan(res)
        return list(res[~nan_idx])[-1]
