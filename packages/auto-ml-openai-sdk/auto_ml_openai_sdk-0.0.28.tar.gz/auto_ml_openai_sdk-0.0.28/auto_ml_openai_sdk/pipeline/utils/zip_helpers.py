import shutil
import tarfile
from zipfile import ZipFile


def files_in_zip(path: str) -> list:
    """Get files inside the zip.

    Parameters
    ----------
    path : str
        path of the zip file

    Returns
    -------
    list
        list of files inside zip

    """
    return ZipFile(path).namelist()


def is_zip_file(path: str) -> bool:
    """Check a zip file.

    Parameters
    ----------
    path : str
        path of the zip file

    Returns
    -------
    bool
        whether zip or not

    """
    if path.endswith(".zip"):
        try:
            test_res = ZipFile(path).testzip()
            return test_res is None
        except Exception:
            return False
    return False


def unzip(file_name: str, output_path: str = None) -> None:
    """Unzip and save a file.

    Parameters
    ----------
    file_name : str
        path of the zip file
    output_path : str
        path where will be saved after unzipping

    """
    shutil.unpack_archive(file_name, output_path)


def zip_dir(output_file_name: str, root_dir: str, base_dir: str) -> None:
    """Zip a directory.

    Parameters
    ----------
    output_file_name : str
        name of the output file
    root_dir : str
        path of root dir
    base_dir : str
        path of base dir

    """
    shutil.make_archive(
        output_file_name, "zip", root_dir="./" + root_dir, base_dir="./" + base_dir
    )


def create_tar_archive(files: list, tar_path: str) -> None:
    """Create tar archive.

    Parameters
    ----------
    files : list
        list of files to add in tar
    tar_path : str
        path of tar

    """
    with tarfile.open(tar_path, "w:gz") as tar:
        for file in files:
            tar.add(file)
