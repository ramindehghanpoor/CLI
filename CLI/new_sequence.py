import numpy as np
import glob
import urllib.request
import os
from pathlib import Path
from keras.models import model_from_json
from .utils import aa_letters
from .utils.data_loaders import to_one_hot
from keras import backend as K
import pandas as pd
from tqdm import tqdm, trange
from zipfile import ZipFile
import importlib_resources #new_sequence only called w/ python 3.7.6

class DownloadProgressBar(tqdm):
    def update_to(self, b=1, bsize=1, tsize=None):
        if tsize is not None:
            self.total = tsize
        self.update(b * bsize - self.n)

def download_url(url, output_path):
    with DownloadProgressBar(unit='B', unit_scale=True, miniters=1, desc=url.split('/')[-1]) as t:
        urllib.request.urlretrieve(url, filename=output_path, reporthook=t.update_to)

def ns_search(ns):
    
    # if the trained network files don't already exist, download them
    if (not Path('Trained_networks').exists()):
        download_url('https://github.com/cfogel/Trained_networks/releases/download/Trained_networks/Trained_networks.zip', 'downloaded_file.zip')
        with ZipFile('downloaded_file.zip') as zf:
            for member in tqdm(zf.infolist(), desc='Extracting', leave=False):
                zf.extract(member, 'Trained_networks')
        os.remove('downloaded_file.zip')

    #
    # Currently needs to be run from folder with Trained_networks directory in it
    #
    
    protein_seq_file = open(ns,"r+")
    protein_seq = protein_seq_file.read()
    
    # list of all the trained networks. Each trained network belongs to a specific family
    networks_list = glob.glob('Trained_networks/*.h5')

    # get Amino Acid letter from the one hot encoded version of it
    def get_AA(n):
        return list(aa_key.keys())[list(aa_key.values()).index(n)]
    aa_key = {l: i for i, l in enumerate(aa_letters)}

    max_acc = 0
    chosen_family = 'none'

    # get the sequence length for each protein family that we have
    pkg = importlib_resources.files("CLI")
    f = pkg / "seq_lengths.csv"
    seq_lengths = pd.read_csv(f,usecols=['name', 'size'])

    # loop over all the trained networks and find the one with highest reconstruction accuracy
    for i in trange(0, len(seq_lengths), total=len(seq_lengths), leave=False):
        test_seq = protein_seq
        
        # skip the families with shorter protein sequence length
        if int(seq_lengths['size'][i]) < len(test_seq):
            continue

        # Not all families in sequence_lengths are in Trained_networks
        
        if Path('Trained_networks/' + seq_lengths['name'][i] + '.json').exists():
        
            # load the trained network
            json_file = open('Trained_networks/' + seq_lengths['name'][i] + '.json', 'r')
            loaded_model_json = json_file.read()
            json_file.close()
            loaded_model = model_from_json(loaded_model_json)

            #load weights into new model
            loaded_model.load_weights('Trained_networks/' + seq_lengths['name'][i] + '_weights.h5')
            
            #new_encoder = loaded_model.layers[1]
            #if int(loaded_model.layers[0].input_shape[1]/21) < len(test_seq):
            #    continue

            # add left and right gaps to get the same size sequence as the sequences used for training this network
            left_gaps = int((int(seq_lengths['size'][i]) - len(test_seq))/2)
            right_gaps = int(seq_lengths['size'][i]) - len(test_seq) - left_gaps
            test_seq = (left_gaps*'-') + test_seq + (right_gaps*'-')
            seq_length = len(test_seq)

            # use the one hot encoded version of the protein sequence
            single_msa_seq = [test_seq]
            x_test = to_one_hot(single_msa_seq)
            y_test = K.argmax(x_test, axis=-1)
            x_test = x_test.reshape((len(x_test), np.prod(x_test.shape[1:])))

            # reconstruct the new protein sequence with the network
            a = loaded_model.predict(x_test, steps = 1)
            a = a.reshape(len(single_msa_seq),seq_length,21)
            
            # x is the reconstructed sequence
            x = np.vectorize(get_AA)(np.argmax(a, axis=-1))
            x = np.array(x).tolist()
            for k in range(0, len(x)):
                x[k] = ''.join(x[k])
            count = 0
            
            # find the reconstruction accuracy
            for j in range(0, len(x[0])):
                if x[0][j] == single_msa_seq[0][j]:
                    count = count + 1
            acc = count / len(x[0])
            
            # update the max accuracy and the chosen family name
            if acc > max_acc:
                max_acc = acc
                chosen_family = seq_lengths['name'][i]
    print('The closest protein family is ' + chosen_family + ' with average accuracy of ' + str(max_acc))
    return
