import argparse
from typing import List

output_opt_parser: argparse.ArgumentParser = argparse.ArgumentParser(add_help=False)
output_opt_group = output_opt_parser.add_argument_group("output options")
output_opt_group.add_argument("-out", help="Output filename", dest="output_file", type=str, default="")
output_opt_group.add_argument("-of", help="Output format. Default: %(default)s", dest="output_format", type=str, choices=["text", "csv"], default="text")
output_opt_group.add_argument("-om", help="Output mode. Default: %(default)s", dest="output_mode", type=str, choices=['a', 'w'], default='a')

metrics: List[str] = ['euclidean', 'minkowski', 'cityblock', 'sqeuclidean', 'cosine',
                      'correlation', 'hamming', 'jaccard', 'chebyshev', 'canberra',
                      'braycurtis', 'yule', 'dice', 'kulsinski', 'rogerstanimoto',
                      'russellrao', 'sokalmichener', 'sokalsneath']

dist_opt_parser: argparse.ArgumentParser = argparse.ArgumentParser(add_help=False)
dist_opt_group = dist_opt_parser.add_argument_group("distance options")
dist_opt_group.add_argument("-m", help="Distance metric. Default: %(default)s", metavar="DISTANCE_METRIC", dest="distance_metric", type=str, choices=metrics, default="euclidean")
dist_opt_group.add_argument("-p", help="Scalar. The p-norm to apply for Minkowski, weighted and unweighted. Default: 2", dest="p_norm", type=int, default=2)

metrics_epilog: str = '''Available distance metrics: 
   euclidean, minkowski, cityblock, sqeuclidean, cosine, correlation, hamming, jaccard, chebyshev, canberra, braycurtis, yule, dice, kulsinski, rogerstanimoto, russellrao, sokalmichener, sokalsneath
'''
