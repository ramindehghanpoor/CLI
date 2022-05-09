import numpy as np
import sys

if sys.version_info < (3, 9):
    # importlib.resources either doesn't exist or lacks the files()
    # function, so use the PyPI version:
    import importlib_resources
else:
    # importlib.resources has files(), so use that:
    import importlib.resources as importlib_resources


# load data from protein family name
def load_namef(fname):
    pkg = importlib_resources.files("CLI")
    lspath = pkg / 'Latent_spaces'
    return np.loadtxt(lspath / (fname + '.txt'))


# load data from new latent space file
def load_newf(fname):
    return np.loadtxt(fname)


class LSCompare:
    def __init__(self, pfnames, nfiles):
        self.names = pfnames
        self.files = nfiles
        self.ls_data = []
        self.ls_names = []
        self.load_vectors()

    def load_vectors(self):
        # we already know there are only two total
        for i in self.names:
            self.ls_data.append(load_namef(i))
            self.ls_names.append(i)
        for j in self.files:
            self.ls_data.append(load_newf(j))
            self.ls_names.append(j)
