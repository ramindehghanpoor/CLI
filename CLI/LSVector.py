import numpy
from .load_files import load_family, load_ls_file, is_pf


class LSVector:
    ls_name: str
    ls_data: numpy.ndarray

    def __init__(self, ls_name: str, ls_data: numpy.ndarray = None):
        """

        :param ls_name: Name of latent space
        :type ls_name: str
        :param ls_data: Latent space data
        :type ls_data: numpy.ndarray
        """
        self.ls_name = ls_name
        if ls_data is None:
            self.ls_data = self.load_vector()
        else:
            self.ls_data = ls_data

    def load_vector(self) -> numpy.ndarray:
        if is_pf(self.ls_name):
            return load_family(self.ls_name + '.txt')
        else:
            return load_ls_file(self.ls_name)
