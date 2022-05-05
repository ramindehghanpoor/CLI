#! /usr/bin/env python

# Author: Ramin Dehghanpoor

# import libraries
import argparse
import numpy as np
import glob
import sys
from .utils.io import read_fasta
from keras.models import model_from_json
from .utils import aa_letters
from .utils.data_loaders import to_one_hot
from keras import backend as K
import pandas as pd
from .getDistance import getDistanceFunction
from .family_list import print_families

if sys.version_info < (3, 9):
    # importlib.resources either doesn't exist or lacks the files()
    # function, so use the PyPI version:
    import importlib_resources
else:
    # importlib.resources has files(), so use that:
    import importlib.resources as importlib_resources

class SearchOutput:

    def __init__(self, ls, distance_metric, closest, distance):
        self.ls = ls
        self.distance_metric = distance_metric
        self.closest = closest
        self.distance = distance
    
    def to_stdout(self):
        print('The closest protein family to ' + self.ls + ' is ' + self.closest + ' with ' + self.distance_metric + ' distance: ' + self.distance)
    
    def to_file(self, fname, ftype, mode):
        with open(fname, mode) as outf:
            if ftype == "text":
                outf.write('The closest protein family to ' + self.ls + ' is ' + self.closest + ' with ' + self.distance_metric + ' distance: ' + self.distance + '\n')
            else:
                outf.write(self.ls + ',' + self.distance_metric + ',' + self.closest + ',' + self.distance + '\n')

def new_sequence(ns):    
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
    for i in range(0, len(seq_lengths)):
        test_seq = protein_seq
        
        # skip the families with shorter protein sequence length
        if int(seq_lengths['size'][i]) < len(test_seq):
            continue

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

def run(args):
    # create package data reference object
    pkg = importlib_resources.files("CLI")
    
    # get the arguments
    
    # show names or not
    names_flag = args.show_names_bool
    
    output_filename = args.output_file
    out_format = args.output_format
    out_mode = args.output_mode

    # The p-norm to apply for Minkowski
    p_norm = args.p_norm # default is 2
    
    # new latent space
    nl1 = args.nl1 # default is ""

    # new sequence
    ns = args.ns # default is ""
    
    # set the distance metric
    distance_function = getDistanceFunction(args.distance_metric);  
    
    # when the user asks for the names of the proteins
    if names_flag:
        print_families()
        return
    
    # when the user provides a new sequence, try to reconstruct this sequence with different trained networks that we have to find the network with the highest reconstruction accuracy.
    if (ns != ""):
        new_sequence(ns)
        
    # when the user provides a new latent space and we want to find the closest latent space to that new one
    elif nl1 != "":
        #find closest
        lspath = pkg / 'Latent_spaces'
        latent_space_list = []
        for f in lspath.iterdir():
            latent_space_list.append(f.name)
        a1 = np.loadtxt(nl1)
        min_dist = float("inf")
        for j in range(0, len(latent_space_list)):
            if args.distance_metric == 'minkowski':
                distance_result = distance_function(a1, np.loadtxt(lspath / latent_space_list[j]), p_norm)
            else:
                distance_result = distance_function(a1, np.loadtxt(lspath / latent_space_list[j]))
                
            if distance_result < min_dist:
                min_dist = distance_result
                closest_family = latent_space_list[j]
        
        res = SearchOutput(nl1, str(distance_function).split()[1], closest_family[0:len(closest_family)-4], str(min_dist))
        
        if output_filename != "":
            res.to_file(output_filename, out_format, out_mode)
        
        else:
            res.to_stdout()

        return
    
    # show the usage to the user
    else:
        print(args.help_text)
        return
 
    
def main():

    metrics = ['euclidean', 'minkowski', 'cityblock', 'sqeuclidean', 'cosine', 'correlation', 'hamming', 'jaccard', 'chebyshev', 'canberra', 'braycurtis', 'yule', 'dice', 'kulsinski', 'rogerstanimoto', 'russellrao', 'sokalmichener', 'sokalsneath']
    
    parser=argparse.ArgumentParser(description='''Find the closest protein family to a new latent space or protein sequence. 
    
Available metrics: 
    euclidean, minkowski, cityblock, sqeuclidean, cosine, correlation, hamming, jaccard, chebyshev, canberra, braycurtis, yule, dice, kulsinski, rogerstanimoto, russellrao, sokalmichener, sokalsneath

To see all the available protein families, run command:
    search -names 1
            
Or you can find the closest protein family to first_new_latent_example.txt in cosine distance by running the command:
    search -nl1 first_new_latent_example.txt -m cosine

Also you can find the closest family to a new protein sequence (for example new_sequence_example.txt) by running:
    search -ns new_sequence_example.txt
    
    ''',
                                  formatter_class=argparse.RawTextHelpFormatter)
    #parser.add_argument('--argument', default=None, help=''' ''')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-names",help="Boolean, Show available protein family names" ,dest="show_names_bool", nargs='?', const=1, type=bool, default=0)
    group.add_argument("-nl1",help="The file name of a new latent space. Provide a new protein family latent space. The closest protein family to this new latent space will be shown." ,dest="nl1", type=str, default="")
    group.add_argument("-nl2",help="The file name of a new latent space. Provide a new protein family latent space. The closest protein family to this new latent space will be shown." ,dest="nl1", metavar="NL2", type=str, default="")
    group.add_argument("-ns",help="The name of the file containing a protein sequence. Provide a protein sequence to get the closest protein family for this sequence." ,dest="ns", type=str, default="")
    parser.add_argument("-m",help="[optional] Distance metric. Default: euclidean" ,dest="distance_metric", type=str, choices=metrics ,default="euclidean")
    parser.add_argument("-p",help="[optional] Scalar, The p-norm to apply for Minkowski, weighted and unweighted. Default: 2" ,dest="p_norm", type=int, default=2)
    parser.add_argument("-out",help="[optional] Output filename" ,dest="output_file", type=str, default="")
    parser.add_argument("-of",help="[optional] Output format. Default: text" ,dest="output_format", type=str, choices = ["text", "csv"], default="text")
    parser.add_argument("-om",help="[optional] Output mode. Default: a" ,dest="output_mode", type=str, choices = ['a', 'w'], default='a')

    #parser.add_argument("-V",help="ndarray The variance vector for standardized Euclidean. Default: var(vstack([XA, XB]), axis=0, ddof=1)" ,dest="variance_vector", type=np.ndarray, default='None')
    #parser.add_argument("-VI",help="ndarray The inverse of the covariance matrix for Mahalanobis. Default: inv(cov(vstack([XA, XB].T))).T" ,dest="inverse_covariance", type=np.ndarray, default='None')
    parser.set_defaults(func=run)
    args=parser.parse_args()
    args.help_text = parser.format_help()
    args.func(args)

if __name__=="__main__":
    main()