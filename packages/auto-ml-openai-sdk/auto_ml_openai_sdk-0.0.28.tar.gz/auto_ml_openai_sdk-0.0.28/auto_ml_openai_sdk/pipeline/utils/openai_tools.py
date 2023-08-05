import time

import openai
import requests
from openai.openai_object import OpenAIObject

from auto_ml_openai_sdk.pipeline.components.helper import get_logger


class OpenaiTools:
    def __init__(self, openai_api_key: str) -> None:
        self.openai_api_key = openai_api_key
        openai.api_key = openai_api_key
        self.log = get_logger("pipeline.openai_tools")

    @staticmethod
    def upload_file(file_path: str, purpose: str = "fine-tune") -> OpenAIObject:
        """Upload file to openai.

        Parameters
        ----------
        file_path : str
            path of the file
        purpose : str
            purpose of uploading

        Returns
        -------
        OpenAIObject

        """
        return openai.File.create(file=open(file_path), purpose=purpose)

    @staticmethod
    def fine_tuning(
        training_file_id: str,
        validation_file_id: str,
        model: str,
        prompt_loss_weight: float,
        learning_rate_multiplier: float,
    ) -> OpenAIObject:
        """Fine-tune using training data.

        Parameters
        ----------
        training_file_id : str
            id of training file
        validation_file_id : str
            id of validation file
        model : str
            name of the model
        prompt_loss_weight : float
            prompt loss weight
        learning_rate_multiplier : float
            learning rate

        Returns
        -------
        OpenAIObject

        """
        return openai.FineTune.create(
            training_file=training_file_id,
            validation_file=validation_file_id,
            model=model,
            prompt_loss_weight=prompt_loss_weight,
            learning_rate_multiplier=learning_rate_multiplier,
        )

    @staticmethod
    def get_status(fine_tune_id: str) -> OpenAIObject:
        """Get status of a fine-tune job.

        Parameters
        ----------
        fine_tune_id : str
            id of fine tuning

        Returns
        -------
        OpenAIObject

        """
        return openai.FineTune.retrieve(fine_tune_id)

    def download_results_file(self, job_id: str) -> bytes:
        """Download the results file from openai.

        Parameters
        ----------
        job_id : str
            openai job id

        Returns
        -------
        bytes

        """
        result_file_id = openai.FineTune.retrieve(job_id).result_files[0].id
        headers = {
            "Content-type": "application/json",
            "Authorization": "Bearer " + self.openai_api_key,
        }
        response = requests.get(
            f"https://api.openai.com/v1/files/{result_file_id}/content",
            headers=headers,
        )
        if response.status_code == 200:
            return response.content

        return None

    def predict_generation(
        self, prompt: str, model_name: str, temperature: float, max_tokens: int = 65
    ) -> str:
        """Predict generation.

        Parameters
        ----------
        prompt : str
            the prompt
        model_name : str
            the name of the finetuned model
        temperature: float
            the value of temp
        max_tokens: int
            max token

        Returns
        -------
        str
            the generation

        """
        i = 0
        while i < 20:
            i += 1
            try:
                completion = openai.Completion.create(
                    model=model_name,
                    prompt=prompt,
                    max_tokens=65,
                    temperature=temperature,
                )
                return completion["choices"][0]["text"]
            except Exception as e:
                self.log.error("Error occurred when predicting: {}".format(e))
                time.sleep(i * 2)
        return ""
