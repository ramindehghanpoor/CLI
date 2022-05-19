import numpy
from .load_files import load_family, load_ls_file, is_pf


class LSVector:
    ls_name: str
    ls_data: numpy.ndarray

    def __init__(self, ls_name: str, ls_data: numpy.ndarray = None):
        """

        Parameters
        ----------
        ls_name : str
            Name of latent space
        ls_data : ls_data: numpy.ndarray
            Latent space data
        """
        self.ls_name = ls_name
        if ls_data is None:
            self.ls_data = self.load_vector()
        else:
            self.ls_data = ls_data

    def load_vector(self) -> numpy.ndarray:
        """ Loads data if only ls_name was given

        Loads the latent space data of a protein family if one matches, otherwise it's treated as a filename

        Returns
        -------
        numpy.ndarray
        """
        if is_pf(self.ls_name):
            return load_family(self.ls_name + '.txt')
        else:
            return load_ls_file(self.ls_name)
