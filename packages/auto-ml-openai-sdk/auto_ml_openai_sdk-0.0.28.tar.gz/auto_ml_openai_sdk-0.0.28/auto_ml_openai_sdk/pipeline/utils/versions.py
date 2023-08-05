import os
import re

current_directory = os.path.dirname(os.path.realpath(__file__))


def get_auto_ml_openai_sdk_version() -> str:
    """Get the package version of the sdk from the requirements file.

    Returns
    -------
    str
        package version

    """
    with open(
        os.path.join(current_directory, "..", "..", "__init__.py"), "r"
    ) as init_file:
        for line in init_file:
            if "__version__" in line:
                sdk_package_version = re.sub(r"\s+|\"|=", "", line).replace(
                    "__version__", ""
                )
                sdk_package_version = "auto_ml_openai_sdk==" + sdk_package_version
                break
    return sdk_package_version
