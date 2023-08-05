from auto_ml_openai_sdk.pipeline.utils import get_auto_ml_openai_sdk_version


def test_version():
    sdk_package_version = get_auto_ml_openai_sdk_version()
    assert "auto_ml_openai_sdk==" in sdk_package_version
