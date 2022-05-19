from typing import List, TextIO
import numpy as np
import sys

if sys.version_info < (3, 9):
    # importlib.resources either doesn't exist or lacks the files()
    # function, so use the PyPI version:
    import importlib_resources
else:
    # importlib.resources has files(), so use that:
    import importlib.resources as importlib_resources

pkg = importlib_resources.files("CLI")
lspath = pkg / 'Latent_spaces'
s_length = pkg / "seq_lengths.csv"


# load data from protein family name
def load_family(fname: str) -> np.ndarray:
    """

    Parameters
    ----------
    fname : str
        The name of a protein family

    Returns
    -------
    numpy.ndarray
        The data from its latent space file
    """
    try:
        # noinspection PyTypeChecker
        return np.loadtxt(lspath / fname)
    # if a file with that name exists but isn't valid, treat it as a new filename
    except ValueError:
        load_ls_file(fname)


# load data from new latent space file
def load_ls_file(fname: str) -> np.ndarray:
    """

    Parameters
    ----------
    fname : str
        Name of a file containing latent space data

    Returns
    -------
    numpy.ndarray
        The latent space data from the file
    """
    # try to read the file
    try:
        return np.loadtxt(fname)
    # if it isn't a valid latent space, give an error and quit
    except ValueError:
        print("Invalid file: " + fname)
        print("Files should contain 30 floats, each float in a separate line.")
        exit(2)
    # if the file doesn't exist or can't be read
    except IOError as err:
        exit(err)


def load_sequence(fname: str) -> str:
    """

    Parameters
    ----------
    fname : str
        Name of a file containing a new sequence

    Returns
    -------
    str
        The new sequence
    """
    try:
        seq_file: TextIO = open(fname, "r+")
        return seq_file.read()
    # if the file doesn't exist or can't be read
    except IOError as err:
        exit(err)


def get_ls_list() -> List[str]:
    """

    Returns
    -------
    List[str]
        List of protein family filenames
    """
    ls_list: List[str] = []
    for f in lspath.iterdir():
        ls_list.append(f.name)
    return ls_list


def is_pf(fname: str) -> bool:
    """

    Parameters
    ----------
    fname : str
        Filename

    Returns
    -------
    bool
        If it's the name of a protein family
    """
    if (lspath / (fname + '.txt')).is_file():
        return True
    return False


latent_space_list: List[str] = get_ls_list()
