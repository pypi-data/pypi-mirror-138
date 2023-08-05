"""Package instructions."""
import re

from setuptools import find_packages, setup

with open("README.md") as file:
    long_description = file.read()


def find_version():
    """Load version from __init__."""
    with open("auto_ml_openai_sdk/__init__.py") as file:
        version_file = file.read()
        version_match = re.search(
            r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M
        )
        if version_match:
            return version_match.group(1)


def find_requirements():
    """Load requirements from file."""
    with open("requirements/requirements.txt") as file:
        requirements = [line.strip() for line in file.readlines()]
        return requirements


setup(
    name="auto_ml_openai_sdk",
    version=find_version(),
    description="Async requests",
    long_description_content_type="text/markdown",
    long_description=long_description,
    author="alchowdhury",
    author_email="alchowdhury@expediagroup.com",
    packages=find_packages(),
    url="https://github.expedia.biz/AI/auto-ml-openai-sdk",
    package_data={"": ["*.*"]},
    include_package_data=True,
    install_requires=find_requirements(),
    python_requires=">=3.6",
)
