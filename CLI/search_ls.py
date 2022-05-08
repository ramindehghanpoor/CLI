#! /usr/bin/env python

# Author: Ramin Dehghanpoor

# import libraries
import numpy as np
import sys
from .getDistance import getDistanceFunction

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

def ls_search(args):

    # create package data reference object
    pkg = importlib_resources.files("CLI")
    
    # get the arguments
    
    output_filename = args.output_file
    out_format = args.output_format
    out_mode = args.output_mode

    # The p-norm to apply for Minkowski
    p_norm = args.p_norm # default is 2
    
    # new latent space
    lat_space = args.latent_space # default is ""
    
    # set the distance metric
    distance_function = getDistanceFunction(args.distance_metric);  
    
    # when the user provides a new latent space and we want to find the closest latent space to that new one
    #find closest
    lspath = pkg / 'Latent_spaces'
    latent_space_list = []
    for f in lspath.iterdir():
        latent_space_list.append(f.name)
    ls_data = np.loadtxt(lat_space)
    min_dist = float("inf")
    for j in range(0, len(latent_space_list)):
        if args.distance_metric == 'minkowski':
            distance_result = distance_function(ls_data, np.loadtxt(lspath / latent_space_list[j]), p_norm)
        else:
            distance_result = distance_function(ls_data, np.loadtxt(lspath / latent_space_list[j]))
            
        if distance_result < min_dist:
            min_dist = distance_result
            closest_family = latent_space_list[j]
    
    res = SearchOutput(lat_space, str(distance_function).split()[1], closest_family[0:len(closest_family)-4], str(min_dist))
    
    if output_filename != "":
        res.to_file(output_filename, out_format, out_mode)
    
    else:
        res.to_stdout()
 