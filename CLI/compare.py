#! /usr/bin/env python

# Author: Ramin Dehghanpoor

# import libraries
import argparse
from argparse_formatter import FlexiFormatter
from .CompareOutput import CompareOutput
from .getDistance import getDistanceFunction
from .family_list import print_families
from .LSCompare import LSCompare


def run(args):
    # Get the arguments

    # Families
    family_list = args.family_name

    # Set the distance metric
    distance_function = getDistanceFunction(args.distance_metric)

    # The p-norm to apply for Minkowski
    p_norm = args.p_norm  # default is 2

    # Output arguments
    output_filename = args.output_file
    out_format = args.output_format
    out_mode = args.output_mode

    # when the user asks for the names of the proteins
    if family_list == ['list', 'names']:
        print_families(None)  # argument required in search but never used
        return

    else:
        v = LSCompare(family_list)

    # find distance between the vectors, create CompareOutput object
    if args.distance_metric == 'minkowski':
        distance_result = distance_function(v.ls_data[0], v.ls_data[1], p_norm)
    else:
        distance_result = distance_function(v.ls_data[0], v.ls_data[1])

    res = CompareOutput(v.ls_names[0], v.ls_names[1], str(distance_function).split()[1],
                        str(distance_result))

    # if there's a filename, write the output to a file
    if output_filename != "":
        res.to_file(output_filename, out_format, out_mode)

    # otherwise print it
    else:
        res.to_stdout()


def main():
    metrics = ['euclidean', 'minkowski', 'cityblock', 'sqeuclidean', 'cosine',
               'correlation', 'hamming', 'jaccard', 'chebyshev', 'canberra',
               'braycurtis', 'yule', 'dice', 'kulsinski', 'rogerstanimoto',
               'russellrao', 'sokalmichener', 'sokalsneath']

    parser = argparse.ArgumentParser(description='''Find the distance between fingerprints of two protein families. 
    
Available metrics: 
    euclidean, minkowski, cityblock, sqeuclidean, cosine, correlation, hamming, jaccard, chebyshev, canberra, braycurtis, yule, dice, kulsinski, rogerstanimoto, russellrao, sokalmichener, sokalsneath
       
As an example you can find the Euclidean distance between two families ATKA_ATKC and CDSA_RSEP by running the command:
    compare ATKA_ATKC CDSA_RSEP
    
    
Or if you want to find the cosine distance between two new latent spaces stored at first_new_latent_example.txt and second_new_latent_example.txt, you can run the command:
    compare first_new_latent_example.txt second_new_latent_example.txt -m cityblock
    
    
To show all available protein family names, run the command:
    compare list names
    
    ''',
                                     formatter_class=FlexiFormatter)
    # parser.add_argument('--argument', default=None, help=''' ''')
    parser.add_argument("family_name", help="Protein family's name. Provide an existing protein family's name or the file name of a new latent space. Files should contain 30 floats, each float in a separate line.", metavar="protein_family", nargs=2, type=str)
    parser.add_argument("-m", help="Distance metric. Default: euclidean", metavar="DISTANCE_METRIC", dest="distance_metric", type=str, choices=metrics, default="euclidean")
    parser.add_argument("-p", help="Scalar, The p-norm to apply for Minkowski, weighted and unweighted. Default: 2", dest="p_norm", type=int, default=2)
    parser.add_argument("-out", help="Output filename", dest="output_file", type=str, default="")
    parser.add_argument("-of", help="Output format. Default: text", dest="output_format", type=str, choices=["text", "csv"], default="text")
    parser.add_argument("-om", help="Output mode. Default: a", dest="output_mode", type=str, choices=['a', 'w'], default='a')

    # parser.add_argument("-V",help="ndarray The variance vector for standardized Euclidean. Default: var(vstack([XA, XB]), axis=0, ddof=1)" ,dest="variance_vector", type=np.ndarray, default='None')
    # parser.add_argument("-VI",help="ndarray The inverse of the covariance matrix for Mahalanobis. Default: inv(cov(vstack([XA, XB].T))).T" ,dest="inverse_covariance", type=np.ndarray, default='None')
    parser.set_defaults(func=run)
    args = parser.parse_args()
    args.help_text = parser.format_help()
    args.func(args)


if __name__ == "__main__":
    main()
