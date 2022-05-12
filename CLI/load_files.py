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
    return np.loadtxt(lspath / fname)


# load data from new latent space file
def load_ls_file(fname):
    return np.loadtxt(fname)


def get_ls_list():
    ls_list = []
    for f in lspath.iterdir():
        ls_list.append(f.name)
    return ls_list


def is_pf(fname):
    if (lspath / (fname + '.txt')).is_file():
        return True
    return False


latent_space_list = get_ls_list()
