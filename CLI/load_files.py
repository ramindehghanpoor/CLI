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
def load_family(fname):
    """

    :param fname: The name of a protein family
    :type fname: str
    :return: The data from its latent space file
    :rtype: numpy.ndarray
    """
    try:
        return np.loadtxt(lspath / fname)
    # if a file with that name exists but isn't valid, treat it as a new filename
    except ValueError:
        load_ls_file(fname)


# load data from new latent space file
def load_ls_file(fname):
    """

    :param fname: Name of a file containing latent space data
    :type fname: str
    :return: The latent space data from the file
    :rtype: numpy.ndarray
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


def load_sequence(fname):
    try:
        seq_file = open(fname, "r+")
        return seq_file.read()
    # if the file doesn't exist or can't be read
    except IOError as err:
        exit(err)


def get_ls_list():
    """

    :return: List of protein family filenames
    :rtype: List[str]
    """
    ls_list = []
    for f in lspath.iterdir():
        ls_list.append(f.name)
    return ls_list


def is_pf(fname):
    """

    :param fname: Filename
    :type fname: str
    :return: If it's the name of a protein family
    :rtype: bool
    """
    if (lspath / (fname + '.txt')).is_file():
        return True
    return False


latent_space_list = get_ls_list()
