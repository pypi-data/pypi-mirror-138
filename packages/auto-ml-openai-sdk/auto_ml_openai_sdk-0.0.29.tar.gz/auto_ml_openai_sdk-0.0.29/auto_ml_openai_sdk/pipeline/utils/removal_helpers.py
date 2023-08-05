import os


def remove_file(path: str) -> None:
    """Remove a file.

    Parameters
    ----------
    path : str
        path of the file to delete

    """
    if os.path.exists(path):
        os.remove(path)


def remove_files(files: list) -> None:
    """Remove a list of files.

    Parameters
    ----------
    files : str
        paths of the files to delete

    """
    for file in files:
        remove_file(file)
