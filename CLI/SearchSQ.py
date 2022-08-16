import os
import urllib.request
from pathlib import Path
from typing import TextIO, List
from zipfile import ZipFile
import keras
import numpy as np
import pandas as pd
from .utils import aa_letters
from .utils.data_loaders import to_one_hot
from .load_files import s_length, load_sequence
from .SearchSQOutput import SearchSQOutput
from tqdm import tqdm
import silence_tensorflow.auto

networks_path_name: str = 'Trained_networks/'
networks_path: Path = Path(networks_path_name)
networks_url: str = 'https://github.com/cfogel/Trained_networks/releases/download/Trained_networks/Trained_networks.zip'
downloaded_filename: str = 'downloaded_file.zip'

# Flag to disable progress bars
no_pbar: bool = False

# get the sequence length for each protein family that we have
seq_lengths: pd.DataFrame = pd.read_csv(s_length, usecols=['name', 'size'])
aa_key: dict = {l: i for i, l in enumerate(aa_letters)}


def get_AA(n):
    """ Get Amino Acid letter from the one hot encoded version of it

    """
    return list(aa_key.keys())[list(aa_key.values()).index(n)]


class DownloadProgressBar(tqdm):
    def update_to(self, b: int = 1, bsize: int = 1, tsize: int = None):
        """

        Parameters
        ----------
        b : int
        bsize : int
        tsize : int
        """
        if tsize is not None:
            self.total = tsize
        self.update(b * bsize - self.n)


def download_url(url: str, output_path: str):
    """

    Parameters
    ----------
    url : str
        URL to download
    output_path : str
        Filename
    """
    t: DownloadProgressBar
    with DownloadProgressBar(unit='B', unit_scale=True, miniters=1, desc=url.split('/')[-1], disable=no_pbar) as t:
        urllib.request.urlretrieve(url, filename=output_path, reporthook=t.update_to)


def check_files():
    """ If the trained network files don't already exist, download them

    """
    if not networks_path.exists():
        download_url(networks_url, downloaded_filename)
        zf: ZipFile
        with ZipFile(downloaded_filename) as zf:
            for member in tqdm(zf.infolist(), desc='Extracting', leave=False, disable=no_pbar):
                zf.extract(member, networks_path)
        os.remove(downloaded_filename)


def find_networks(slen: int) -> pd.DataFrame:
    """

    Parameters
    ----------
    slen : int
        The minimum sequence length

    Returns
    -------
    pandas.core.frame.DataFrame
        Families longer than slen with trained network data
    """
    filteredseq: pd.DataFrame = seq_lengths.query('size >= @slen')
    havefile: pd.Series = filteredseq['name'].map(lambda x: (networks_path / (x + '.json')).exists())
    networks: pd.DataFrame = filteredseq[havefile]
    return networks


class SearchSQ:

    seq: str
    lseq: str
    sequence_length: int
    result: SearchSQOutput

    def __init__(self, seq: str):
        """

        Parameters
        ----------
        seq : str
            Filename of sequence
        """
        check_files()
        self.seq = seq
        self.lseq = load_sequence(self.seq)
        self.sequence_length = len(self.lseq)
        self.result = self.do_search()

    def do_search(self) -> SearchSQOutput:
        """ Find best matching protein family

        Returns
        -------
        SearchSQOutput
        """
        network_list = find_networks(self.sequence_length)
        max_acc: float = 0
        chosen_family: str = 'none'

        for family in tqdm(network_list.itertuples(), total=network_list.shape[0], disable=no_pbar):
            test_seq: str = self.lseq
            jfile: TextIO
            with open(networks_path / (family.name + '.json')) as jfile:
                model_json = jfile.read()
            loaded_model: keras.Model = keras.models.model_from_json(model_json)
            loaded_model.load_weights(networks_path / (family.name + '_weights.h5'))

            test_seq = test_seq.center(int(family.size), '-')
            seq_length: int = len(test_seq)

            # use the one hot encoded version of the protein sequence
            single_msa_seq: List[str] = [test_seq]
            x_test: np.ndarray = to_one_hot(single_msa_seq)
            x_test = x_test.reshape((len(x_test), np.prod(x_test.shape[1:])))

            # reconstruct the new protein sequence with the network
            a = loaded_model.predict(x_test, steps=1)
            a = a.reshape(len(single_msa_seq), seq_length, 21)

            # x is the reconstructed sequence
            x: np.ndarray = np.vectorize(get_AA)(np.argmax(a, axis=-1))
            x: list = np.array(x).tolist()
            k: int
            for k in range(0, len(x)):
                x[k] = ''.join(x[k])
            count: int = 0

            # find the reconstruction accuracy
            j: int
            xlen = len(x[0])
            for j in range(0, xlen):
                if x[0][j] == single_msa_seq[0][j]:
                    count = count + 1
            acc: float = count / xlen

            if acc > max_acc:
                max_acc = acc
                chosen_family = family.name

        return SearchSQOutput(self.seq, chosen_family, str(max_acc))
