#! /usr/bin/env python

# Author: Ramin Dehghanpoor

# import libraries
import argparse
import sys
from argparse_formatter import FlexiFormatter
from .family_list import print_families
from .search_ls import ls_search


def seq_search(args):
    new_sequence = args.sequence
    if sys.version_info[:3] == (3, 7, 6):
        # don't import function and dependencies if you don't need to
        from .new_sequence import ns_search
        ns_search(new_sequence)
    else:
        print('sequence searches only available with python 3.7.6')


def main():
    metrics = ['euclidean', 'minkowski', 'cityblock', 'sqeuclidean', 'cosine',
               'correlation', 'hamming', 'jaccard', 'chebyshev', 'canberra',
               'braycurtis', 'yule', 'dice', 'kulsinski', 'rogerstanimoto',
               'russellrao', 'sokalmichener', 'sokalsneath']

    parser = argparse.ArgumentParser(description='''Find the closest protein family to a new latent space or protein sequence. 
    
Available metrics: 
    euclidean, minkowski, cityblock, sqeuclidean, cosine, correlation, hamming, jaccard, chebyshev, canberra, braycurtis, yule, dice, kulsinski, rogerstanimoto, russellrao, sokalmichener, sokalsneath

To see all the available protein families, run command:
    search names
            
Or you can find the closest protein family to first_new_latent_example.txt in cosine distance by running the command:
    search lat first_new_latent_example.txt -m cosine

Also you can find the closest family to a new protein sequence (for example new_sequence_example.txt) by running:
    search seq new_sequence_example.txt
    
    ''',
                                  formatter_class=FlexiFormatter)
    subparsers = parser.add_subparsers(dest='command')
    parser_ls = subparsers.add_parser('lat', help="Provide a new protein family latent space. The closest protein family to this new latent space will be shown.")
    parser_ls.add_argument('latent_space', metavar="filename", help="The file name of a new latent space.", type=str, nargs='+')
    parser_ls.add_argument("-m", help="[optional] Distance metric. Default: euclidean", metavar="DISTANCE_METRIC", dest="distance_metric", type=str, choices=metrics, default="euclidean")
    parser_ls.add_argument("-p", help="[optional] Scalar, The p-norm to apply for Minkowski, weighted and unweighted. Default: 2", dest="p_norm", type=int, default=2)
    parser_ls.add_argument("-out", help="[optional] Output filename", dest="output_file", type=str, default="")
    parser_ls.add_argument("-of", help="[optional] Output format. Default: text", dest="output_format", type=str, choices=["text", "csv"], default="text")
    parser_ls.add_argument("-om", help="[optional] Output mode. Default: a", dest="output_mode", type=str, choices=['a', 'w'], default='a')

    parser_seq = subparsers.add_parser('seq', help="Provide a protein sequence to get the closest protein family for this sequence.")
    parser_seq.add_argument('sequence', metavar="filename", help="The name of the file containing a protein sequence.", type=str, nargs='+')

    parser_names = subparsers.add_parser('names', help="Show available protein family names")

    parser_ls.set_defaults(func=ls_search)
    parser_seq.set_defaults(func=seq_search)
    parser_names.set_defaults(func=print_families)
    args = parser.parse_args()
    # print help text if nothing is selected
    if args.command is None:
        parser.print_help()
    else:
        args.func(args)

    # #parser.add_argument("-V",help="ndarray The variance vector for standardized Euclidean. Default: var(vstack([XA, XB]), axis=0, ddof=1)" ,dest="variance_vector", type=np.ndarray, default='None')
    # #parser.add_argument("-VI",help="ndarray The inverse of the covariance matrix for Mahalanobis. Default: inv(cov(vstack([XA, XB].T))).T" ,dest="inverse_covariance", type=np.ndarray, default='None')
    # args.help_text = parser.format_help()


if __name__ == "__main__":
    main()
