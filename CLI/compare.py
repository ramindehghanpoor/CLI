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
    # Set to empty list if no arguments given
    if not family_list:
        family_list = []

    # New latent spaces
    ls_list = args.ls_file
    # Set to empty list if no arguments given
    if not ls_list:
        ls_list = []

    # Set the distance metric
    distance_function = getDistanceFunction(args.distance_metric)

    # The p-norm to apply for Minkowski
    p_norm = args.p_norm  # default is 2

    # Output arguments
    output_filename = args.output_file
    out_format = args.output_format
    out_mode = args.output_mode

    # when the user asks for the names of the proteins
    if args.show_names_bool:
        print_families(None)  # argument required in search but never used
        return

    # if there aren't two values, print help text and return
    if (len(family_list) + len(ls_list)) != 2:
        print(args.help_text)
        return

    # create LSCompare object to load vectors
    else:
        v = LSCompare(family_list, ls_list)

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
    compare -n1 ATKA_ATKC -n2 CDSA_RSEP
    
    
Or if you want to find the cosine distance between two new latent spaces stored at first_new_latent_example.txt and second_new_latent_example.txt, you can run the command:
    compare -nl1 first_new_latent_example.txt -nl2 second_new_latent_example.txt -m cityblock
    
    ''',
                                     formatter_class=FlexiFormatter)
    # parser.add_argument('--argument', default=None, help=''' ''')
    parser.add_argument("-names",
                        help="Boolean, Show available protein family names",
                        dest="show_names_bool", metavar="BOOL", nargs='?',
                        const=1, type=bool, default=0)
    parser.add_argument("-fn", "-n1", "-n2",
                        help="Protein family's name. Provide an existing protein family's name to compare it with one of the other existing protein families or a new latent space.",
                        dest="family_name", action='append', type=str)
    parser.add_argument("-ls", "-nl1", "-nl2",
                        help="The file name of a new latent space. Provide a new protein family latent space to compare it with one of the existing protein families or with the other new latent space. The file should contain 30 floats, each float in a separate line.",
                        dest="ls_file", action='append', type=str)
    parser.add_argument("-m",
                        help="[optional] Distance metric. Default: euclidean",
                        metavar="DISTANCE_METRIC", dest="distance_metric",
                        type=str, choices=metrics, default="euclidean")
    parser.add_argument("-p",
                        help="[optional] Scalar, The p-norm to apply for Minkowski, weighted and unweighted. Default: 2",
                        dest="p_norm", type=int, default=2)
    parser.add_argument("-out", help="[optional] Output filename",
                        dest="output_file", type=str, default="")
    parser.add_argument("-of", help="[optional] Output format. Default: text",
                        dest="output_format", type=str, choices=["text", "csv"],
                        default="text")
    parser.add_argument("-om", help="[optional] Output mode. Default: a",
                        dest="output_mode", type=str, choices=['a', 'w'],
                        default='a')

    # parser.add_argument("-V",help="ndarray The variance vector for standardized Euclidean. Default: var(vstack([XA, XB]), axis=0, ddof=1)" ,dest="variance_vector", type=np.ndarray, default='None')
    # parser.add_argument("-VI",help="ndarray The inverse of the covariance matrix for Mahalanobis. Default: inv(cov(vstack([XA, XB].T))).T" ,dest="inverse_covariance", type=np.ndarray, default='None')
    parser.set_defaults(func=run)
    args = parser.parse_args()
    args.help_text = parser.format_help()
    args.func(args)


if __name__ == "__main__":
    main()
