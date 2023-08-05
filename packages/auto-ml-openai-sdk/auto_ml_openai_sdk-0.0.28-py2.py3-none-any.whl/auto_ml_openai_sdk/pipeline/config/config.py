import os
import sys

from dynaconf import Dynaconf

current_directory = os.path.dirname(os.path.realpath(__file__))
settings_file = os.path.join(current_directory, "settings.toml")

if os.path.exists(settings_file):
    settings = Dynaconf(
        settings_files=[settings_file],
    )
    settings.configure(FORCE_ENV_FOR_DYNACONF="default")
else:
    sys.exit("settings.toml was not found")


def get_config_value(key: str) -> str:
    """Get dynaconf value for a key.

    Parameters
    ----------
    key : str
        key to look for in the config

    Returns
    -------
    str
        the value for the key in the config

    """
    env = settings.FORCE_ENV_FOR_DYNACONF

    if env == "default":
        return settings.default[key]
    elif env == "testing":
        return settings.testing[key]
    else:
        sys.exit("invalid config env provided")
