#! /usr/bin/env python

# Author: Ramin Dehghanpoor

# import libraries
from tqdm import trange
from .SearchOutput import SearchOutput
from .getDistance import getDistanceFunction
from .load_files import load_ls_file, latent_space_list, load_family

# Flag to disable progress bars
no_pbar = False


def ls_search(args):

    # get the arguments
    output_filename = args.output_file
    out_format = args.output_format
    out_mode = args.output_mode
    p_norm = args.p_norm  # The p-norm to apply for Minkowski - default is 2
    lat_spaces = args.latent_space
    
    # set the distance metric
    distance_function = getDistanceFunction(args.distance_metric)
    
    # find the closest latent space
    for lat_space in lat_spaces:
        ls_data = load_ls_file(lat_space)
        min_dist = float("inf")
        for j in trange(0, len(latent_space_list), total=len(latent_space_list), leave=False, disable=no_pbar):
            if args.distance_metric == 'minkowski':
                distance_result = distance_function(ls_data, load_family(latent_space_list[j]), p_norm)
            else:
                distance_result = distance_function(ls_data, load_family(latent_space_list[j]))

            if distance_result < min_dist:
                min_dist = distance_result
                closest_family = latent_space_list[j]

        res = SearchOutput(lat_space, str(distance_function).split()[1], closest_family[0:len(closest_family) - 4], str(min_dist))

        if output_filename != "":
            res.to_file(output_filename, out_format, out_mode)

        else:
            res.to_stdout()
