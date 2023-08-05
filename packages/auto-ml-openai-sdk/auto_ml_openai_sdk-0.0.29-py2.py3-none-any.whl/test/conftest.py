import pytest

from auto_ml_openai_sdk.pipeline.config import settings


@pytest.fixture(scope="session", autouse=True)
def set_test_settings() -> None:
    """Set test specific dynaconf configs."""
    settings.configure(FORCE_ENV_FOR_DYNACONF="testing")
