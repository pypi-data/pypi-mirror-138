from typing import Any

import kfp.components as comp

from auto_ml_openai_sdk.pipeline.components.operation_func import (
    data_preparation,
    evaluation,
    on_exit,
    on_success,
    training,
)


def create_op(
    func: Any, base_packages: list, base_image: str = None, extra_packages: list = None
) -> Any:
    """Convert any function to kf component.

    Parameters
    ----------
    func : Any
        a python func
    base_packages : list
        list of base package names to be installed
    base_image : str
        name of the base image
    extra_packages : str
        list of extra package names to be installed

    Returns
    -------
    Any
        kf component

    """
    packages = base_packages
    if extra_packages:
        packages.extend(extra_packages)
    if base_image and base_image.strip():
        return comp.func_to_container_op(
            func, packages_to_install=packages, base_image=base_image
        )
    else:
        return comp.func_to_container_op(func, packages_to_install=packages)


def data_preparation_op(base_image: str = None, extra_packages: list = None) -> Any:
    """Convert data preparation function to kf operation.

    Parameters
    ----------
    base_image : str
        name of the base image
    extra_packages : list
        list of package names to be installed

    Returns
    -------
    Any
        kf component

    """
    return create_op(data_preparation, ["pyspark==2.4.5"], base_image, extra_packages)


def training_op(base_image: str = None, extra_packages: list = None) -> Any:
    """Convert fine tuning function to kf operation.

    Parameters
    ----------
    base_image : str
        name of the base image
    extra_packages : list
        list of package names to be installed

    Returns
    -------
    Any
        kf component

    """
    return create_op(training, ["pyspark==2.4.5"], base_image, extra_packages)


def evaluation_op(base_image: str = None, extra_packages: list = None) -> Any:
    """Convert evaluation function to kf operation.

    Parameters
    ----------
    base_image : str
        name of the base image
    extra_packages : list
        list of package names to be installed

    Returns
    -------
    Any
        kf component

    """
    return create_op(evaluation, ["pyspark==2.4.5"], base_image, extra_packages)


def on_success_op(base_image: str = None, extra_packages: list = None) -> Any:
    """Convert on_success function to kf operation.

    Parameters
    ----------
    base_image : str
        name of the base image
    extra_packages : list
        list of package names to be installed

    Returns
    -------
    Any
        kf component

    """
    return create_op(on_success, ["pyspark==2.4.5"], base_image, extra_packages)


def on_exit_op(base_image: str = None, extra_packages: list = None) -> Any:
    """Convert on_exit function to kf operation.

    Parameters
    ----------
    base_image : str
        name of the base image
    extra_packages : list
        list of package names to be installed

    Returns
    -------
    Any
        kf component

    """
    return create_op(on_exit, ["pyspark==2.4.5"], base_image, extra_packages)
