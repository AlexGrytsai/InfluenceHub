import logging
import os

from dotenv import load_dotenv
from infisical_sdk import InfisicalSDKClient
from infisicalapi_client.exceptions import NotFoundException
from pydantic.error_wrappers import ValidationError

load_dotenv()

logger = logging.getLogger("django")


class InfisicalSecretsService:
    """
    A class to handle interactions with the Infisical Secrets API.
    """
    def __init__(self):
        self.client = InfisicalSDKClient(host="https://app.infisical.com")
        self.client.auth.universal_auth.login(
            client_id=os.getenv("CLIENT_ID"),
            client_secret=os.getenv("CLIENT_SECRET"),
        )

    def get_secret(self, secret_name: str) -> str:
        try:
            secret_data = self.client.secrets.get_secret_by_name(
                secret_name=secret_name,
                project_id=os.getenv("PROJECT_ID"),
                environment_slug="dev",
                secret_path="/",
                expand_secret_references=True,
                include_imports=True,
            )
            secret = secret_data.secret.secret_value
            logger.info(
                f"Secret with name:'{secret_name}' retrieved successfully."
            )
            return secret
        except ValidationError as exp:
            logger.error(
                f"{exp}. Maybe, env values are not set. "
                f"Check .env file and try again."
            )
            return "ValidationError"
        except NotFoundException:
            logger.error(
                f"Secret with name: '{secret_name}' not found. "
                f"Check secrets name and try again."
            )
            return "Secret not found"
