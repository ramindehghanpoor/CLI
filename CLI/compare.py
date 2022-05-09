#! /usr/bin/env python

# Author: Ramin Dehghanpoor

# import libraries
import argparse
import numpy as np
import sys
from argparse_formatter import FlexiFormatter
from .getDistance import getDistanceFunction
from .family_list import print_families

if sys.version_info < (3, 9):
    # importlib.resources either doesn't exist or lacks the files()
    # function, so use the PyPI version:
    import importlib_resources
else:
    # importlib.resources has files(), so use that:
    import importlib.resources as importlib_resources

class CompareOutput:

    def __init__(self, a1, a2, distance_metric, result):
        self.a1 = a1
        self.a2 = a2
        self.distance_metric = distance_metric
        self.result = result
    
    def to_stdout(self):
        print(self.distance_metric + ' distance between ' + self.a1 + ' and ' + self.a2 + ': ' + self.result)
    
    def to_file(self, fname, ftype, mode):
        with open(fname, mode) as outf:
            if ftype == "text":
                outf.write(self.distance_metric + ' distance between ' + self.a1 + ' and ' + self.a2 + ': ' + self.result + '\n')
            else:
                outf.write(self.a1 + ',' + self.a2 + ',' + self.distance_metric + ',' + self.result + '\n')

def run(args):

    # create package data reference object
    pkg = importlib_resources.files("CLI")
    # Latent_spaces folder
    lspath = pkg / 'Latent_spaces'

    # get the arguments
    
    # Families
    family_list = args.families
    
    # Set to empty list if no arguments given
    if (not family_list):
        family_list = []
    
    # show names or not
    names_flag = args.show_names_bool
  
    output_filename = args.output_file
    out_format = args.output_format
    out_mode = args.output_mode

    # The p-norm to apply for Minkowski
    p_norm = args.p_norm # default is 2
    
    # New latent spaces
    ls_list = args.latent_spaces # default is ""
    
    # Set to empty list if no arguments given
    if (not ls_list):
        ls_list = []
            
    # set the distance metric
    distance_function = getDistanceFunction(args.distance_metric); 
    
    # when the user asks for the names of the proteins
    if names_flag:
        print_families()
        return
    
    # show the usage to the user
    if ((len(family_list) + len(ls_list)) != 2):
        print(args.help_text)
        return
        
    # when the user provides two latent spaces of the proteins that we have
    elif (len(family_list) == 2):
        a1 = np.loadtxt(lspath / (family_list[0]+'.txt'))
        a1_name = family_list[0]
        a2 = np.loadtxt(lspath / (family_list[1]+'.txt'))
        a2_name = family_list[1]
        
    # when the user provides one new latent space and one from the proteins that we have
    elif (len(family_list) == 1 and len(ls_list) == 1):
        a1 = np.loadtxt(lspath / (family_list[0]+'.txt'))
        a1_name = family_list[0]
        a2 = np.loadtxt(ls_list[0])
        a2_name = ls_list[0]        
    
    # when the user provides two new latent spaces
    else:
        a1 = np.loadtxt(ls_list[0])
        a1_name = ls_list[0]
        a2 = np.loadtxt(ls_list[1])
        a2_name = ls_list[1]

    # find distance between two vectors a1 and a2, create CompareOutput object
    if args.distance_metric == 'minkowski':
        distance_result = distance_function(a1, a2, p_norm)
    else:
        distance_result = distance_function(a1, a2)
        
    res = CompareOutput(a1_name, a2_name, str(distance_function).split()[1], str(distance_result))
    
    # if there's a filename, write the output to a file
    if output_filename != "":
        res.to_file(output_filename, out_format, out_mode)
    
    # otherwise print it
    else:
        res.to_stdout()

        
    
    
def main():

    metrics = ['euclidean', 'minkowski', 'cityblock', 'sqeuclidean', 'cosine', 'correlation', 'hamming', 'jaccard', 'chebyshev', 'canberra', 'braycurtis', 'yule', 'dice', 'kulsinski', 'rogerstanimoto', 'russellrao', 'sokalmichener', 'sokalsneath']
    
    parser=argparse.ArgumentParser(description='''Find the distance between fingerprints of two protein families. 
    
Available metrics: 
    euclidean, minkowski, cityblock, sqeuclidean, cosine, correlation, hamming, jaccard, chebyshev, canberra, braycurtis, yule, dice, kulsinski, rogerstanimoto, russellrao, sokalmichener, sokalsneath
       
As an example you can find the Euclidean distance between two families ATKA_ATKC and CDSA_RSEP by running the command:
    compare -n1 ATKA_ATKC -n2 CDSA_RSEP
    
    
Or if you want to find the cosine distance between two new latent spaces stored at first_new_latent_example.txt and second_new_latent_example.txt, you can run the command:
    compare -nl1 first_new_latent_example.txt -nl2 second_new_latent_example.txt -m cityblock
    
    ''',
                                  formatter_class=FlexiFormatter)
    #parser.add_argument('--argument', default=None, help=''' ''')
    parser.add_argument("-names",help="Boolean, Show available protein family names", metavar="BOOL" ,dest="show_names_bool", nargs='?', const=1, type=bool, default=0)
    parser.add_argument("-n1",help="First family's name" ,dest="families", metavar="FIRST_FAMILY", action='append', type=str)
    parser.add_argument("-n2",help="Second family's name" ,dest="families", metavar="SECOND_FAMILY", action='append', type=str)
    parser.add_argument("-nl1",help="[optional] The file name of the first new latent space. Provide a new protein family latent space to compare it with one of the existing protein families or with the second new latent space. The file should contain 30 floats, each float in a separate line." ,dest="latent_spaces", metavar="NL1", action='append', type=str)
    parser.add_argument("-nl2",help="[optional] The file name of the second new latent space. Provide a new protein family latent space to compare it with one of the existing protein families or with the first new latent space. The file should contain 30 floats, each float in a separate line." ,dest="latent_spaces", metavar="NL2", action='append', type=str)
    parser.add_argument("-m",help="[optional] Distance metric. Default: euclidean", metavar="DISTANCE_METRIC" ,dest="distance_metric", type=str, choices=metrics ,default="euclidean")
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