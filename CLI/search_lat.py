#! /usr/bin/env python

# Author: Ramin Dehghanpoor

# import libraries
from .get_metric import get_distance_function
from .SearchLS import SearchLS
from .output_results import output_result
from .LSVector import LSVector


def ls_search(args):

    # get the arguments
    output_filename = args.output_file
    out_format = args.output_format
    out_mode = args.output_mode
    p_norm = args.p_norm  # The p-norm to apply for Minkowski - default is 2
    lat_spaces = args.latent_space
    
    # set the distance metric
    distance_function = get_distance_function(args.distance_metric)
    
    # find the closest latent space
    for lat_space in lat_spaces:
        v = LSVector(lat_space)
        res = SearchLS(v, distance_function, p_norm).result
        output_result(res, output_filename, out_format, out_mode)
