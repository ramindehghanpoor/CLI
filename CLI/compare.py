#! /usr/bin/env python

# Author: Ramin Dehghanpoor, Suman Gautam

# import libraries
import argparse
import numpy as np
import glob
from utils.io import read_fasta
from keras.models import model_from_json
from utils import aa_letters
from utils.data_loaders import to_one_hot
from keras import backend as K
import pandas as pd
from getDistance import getDistanceFunction


def run(args):
    # get the arguments
    
    # First family
    n1 = args.first_family
    n2 = args.first_family
    
    # Second family
    n2 = args.second_family
    
  
    
    #output_filename = args.output # from dest="output"

    # The p-norm to apply for Minkowski
    p_norm = args.p_norm # default is 2
    
    # first new latent space
    nl1 = args.nl1 # default is ""
    
    # second new latent space
    nl2 = args.nl2 # default is ""
    
    # new sequence
    ns = args.ns # default is ""
    
    # set the distance metric
    distance_function = getDistanceFunction(args); 
    # show the usage to the user
    if (n1 == "" and (nl1 == "" and nl2 == "")) or (n2 == "" and (nl1 == "" and nl2 == "")):
        print('usage: compare.py [-h] [-n1 FIRST_FAMILY] [-n2 SECOND_FAMILY] [-names SHOW_NAMES_BOOL] [-m DISTANCE_METRIC] [-p P_NORM] [-nl1 NL1] [-nl2 NL2] [-ns NS]')        
        print('To see help: ./compare.py -h')
        return
        
    # when the user provides two latent spaces of the proteins that we have
    elif (n1 != "") and (n2 != ""):
        a1 = np.loadtxt('Latent_spaces/'+n1+'.txt')
        a2 = np.loadtxt('Latent_spaces/'+n2+'.txt')
        
    # when the user provides one new latent space and one from the proteins that we have
    elif n1 != "":
        a1 = np.loadtxt('Latent_spaces/'+n1+'.txt')
        if nl1 != "":
            a2 = np.loadtxt(nl1)
        else:
            a2 = np.loadtxt(nl2)
            
    elif n2 != "":
        a2 = np.loadtxt('Latent_spaces/'+n2+'.txt')
        if nl1 != "":
            a1 = np.loadtxt(nl1)
        else:
            a1 = np.loadtxt(nl2)
        
    
    # when the user provides two new latent spaces
    else:
        a1 = np.loadtxt(nl1)
        a2 = np.loadtxt(nl2)

    # find distance between two vectors a1 and a2
    if (ns == ""):
        print(str(distance_function).split()[1] + ' distance: ' + str(distance_function(a1, a2)))

        
    
    
def main():
    parser=argparse.ArgumentParser(description='''Find the distance between fingerprints of two protein families. 
    
Available metrics: 
    euclidean, minkowski, cityblock, sqeuclidean, cosine, correlation, hamming, jaccard, chebyshev, canberra, braycurtis, yule, dice, kulsinski, rogerstanimoto, russellrao, sokalmichener, sokalsneath
       
As an example you can find the Euclidean distance between two families ATKA_ATKC and CDSA_RSEP by running the command:
    ./compare.py -n1 ATKA_ATKC -n2 CDSA_RSEP
    
    
Or if you want to find the cosine distance between two new latent spaces stored at first_new_latent_example.txt and second_new_latent_example.txt, you can run the command:
    ./compare.py -nl1 first_new_latent_example.txt -nl2 second_new_latent_example.txt -m cityblock
    
    ''',
                                  formatter_class=argparse.RawTextHelpFormatter)
    #parser.add_argument('--argument', default=None, help=''' ''')
    parser.add_argument("-n1",help="First family's name" ,dest="first_family", type=str, default="")
    parser.add_argument("-n2",help="Second family's name" ,dest="second_family", type=str, default="")
    parser.add_argument("-names",help="Boolean, Show available protein family names" ,dest="show_names_bool", type=bool, default=0)
    #parser.add_argument("-out",help="fastq output filename" ,dest="output", type=str, required=True)
    parser.add_argument("-m",help="[optional] Distance metric. Default: euclidean" ,dest="distance_metric", type=str, default="euclidean")
    parser.add_argument("-p",help="[optional] Scalar, The p-norm to apply for Minkowski, weighted and unweighted. Default: 2" ,dest="p_norm", type=int, default=2)
    parser.add_argument("-nl1",help="[optional] The file name of the first new latent space. Provide a new protein family latent space to compare it with one of the existing protein families or with the second new latent space. The file should contain 30 floats, each float in a separate line. If only one of the nl1 and nl2 provided, the closest protein family to this new latent space will be shown." ,dest="nl1", type=str, default="")
    parser.add_argument("-nl2",help="[optional] The file name of the second new latent space. Provide a new protein family latent space to compare it with one of the existing protein families or with the first new latent space. The file should contain 30 floats, each float in a separate line. If only one of the nl1 and nl2 provided, the closest protein family to this new latent space will be shown." ,dest="nl2", type=str, default="")
    parser.add_argument("-ns",help="[optional] The name of the file containing a protein sequence. Provide a protein sequence to get the closest protein family for this sequence." ,dest="ns", type=str, default="")
    #parser.add_argument("-V",help="ndarray The variance vector for standardized Euclidean. Default: var(vstack([XA, XB]), axis=0, ddof=1)" ,dest="variance_vector", type=np.ndarray, default='None')
    #parser.add_argument("-VI",help="ndarray The inverse of the covariance matrix for Mahalanobis. Default: inv(cov(vstack([XA, XB].T))).T" ,dest="inverse_covariance", type=np.ndarray, default='None')
    parser.set_defaults(func=run)
    args=parser.parse_args()
    args.func(args)

if __name__=="__main__":
    main()