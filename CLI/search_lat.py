#! /usr/bin/env python

# Author: Ramin Dehghanpoor

# import libraries
from .get_metric import get_distance_function
from .SearchLS import SearchLS


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
        res = SearchLS(lat_space, distance_function, p_norm).result

        # if there's a filename, write the output to a file
        if output_filename != "":
            res.to_file(output_filename, out_format, out_mode)

        # otherwise print it
        else:
            res.to_stdout()
