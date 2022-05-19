# CLI

### Table Of Contents

- [Table of Contents](#table-of-contents)
- [Software Info](#software-info)
- [Overview](#overview)
- [Installation](#installation)
- [Usage](#usage)
    - [Comparing protein sequences](#comparing-protein-sequences)
        - [Comparing Arguments](#comparing-arguments)
    - [Searching](#searching)
        - [Searching Arguments](#searching-arguments)
- [Available Metrics](#available-metrics)
- [Examples](#examples)

### Software Info:

Software Name: CompBioLab CLI  
Latest Software Version: v0.3.3  
PyPI: https://pypi.org/project/compbiolab-CLI/

### Overview

Our goal for this project is to read a new input sequence and find the protein family which it belongs in by comparing it with existing sequences in the database. In addition to finding the closest family for a new sequence, our search application can also accept an autoencoded fingerprint and see which family is the best match using a variety of different metrics.

Our compare application allows different protein families to be compared directly using different distance functions.  It accepts the names of families already in the database, but it can also accept files containing data from new latent spaces. 

The program can be downloaded from PyPI (the Python Package Index), and it has a Command Line Interface.

## Installation

1. Install [Python 3.7 or above](https://www.python.org/downloads/) 
2. Open a terminal. (On Windows, Windows Key + R → Type cmd → Enter)
3. Type `pip install compbiolab-CLI`

## Usage

### Comparing protein sequences

Find the distance between fingerprints of two protein families

    compare [-h] <protein_family> <protein_family> [-m DISTANCE_METRIC] [-p P_NORM] [-out OUTPUT_FILE] [-of OUTPUT_FORMAT] [-om OUTPUT_MODE]

#### Comparing Arguments

* `protein_family`

  Protein family's name. Provide an existing protein family's name or the file name of a new latent space. Files should contain 30 floats, each float in a separate line.

* `-m`

    [optional] Distance metric. Default: euclidean

* `-p`

    [optional] Scalar, The p-norm to apply for Minkowski, weighted and unweighted. Default: 2

* `-out`

	[optional] Output filename

* `-of`

	[optional] Output format, text or csv. Default: text

* `-om`

	[optional] Output mode, a[ppend] or w[rite]. Default: a

### Searching

Find the closest family to a new protein sequence

    search [-h] names
		    lat <latent space> [-m DISTANCE_METRIC] [-p P_NORM] [-out OUTPUT_FILE] [-of OUTPUT_FORMAT] [-om OUTPUT_MODE]
		    seq <sequence> [-out OUTPUT_FILE] [-of OUTPUT_FORMAT] [-om OUTPUT_MODE]

#### Searching Arguments

* `names`

    Show available protein family names

* `lat <filename> [options]`

    Provide the file name of one or more new protein family latent spaces. The closest protein family to these new latent spaces will be shown.

    * `-m`

        [optional] Distance metric. Default: euclidean

    * `-p`

        [optional] Scalar, The p-norm to apply for Minkowski, weighted and unweighted. Default: 2

    * `-out`

        [optional] Output filename

    * `-of`

        [optional] Output format, text or csv. Default: text

    * `-om`

        [optional] Output mode, a[ppend] or w[rite]. Default: a

* `seq <filename> [options]`

    Provide the name of one or more files containing a protein sequence to get the closest protein families for those sequences.

	* `-out`

	  [optional] Output filename

	* `-of`

	  [optional] Output format, text or csv. Default: text

	* `-om`

	  [optional] Output mode, a[ppend] or w[rite]. Default: a

## Available metrics

*euclidean (default)*, minkowski, cityblock, sqeuclidean, cosine, correlation, hamming, jaccard, chebyshev, canberra, braycurtis, yule, dice, kulsinski, rogerstanimoto, russellrao, sokalmichener, sokalsneath

## Examples

To see all the available protein families, run command:

    compare list names
        
You can find the Euclidean distance between two families ATKA_ATKC and CDSA_RSEP by running the command:

    compare ATKA_ATKC CDSA_RSEP

![example-1](https://user-images.githubusercontent.com/1418557/169188051-77bf99a9-2427-4d9a-b6a9-536d81fa0a73.png)

    
If you want to find the Cityblock distance between ATKA_ATKC and a new latent space stored at second_new_latent_example.txt, you can run the command:

    compare ATKA_ATKC second_new_latent_example.txt -m cityblock

![example-2](https://user-images.githubusercontent.com/1418557/169188080-8f53426f-b754-4f40-8e0e-396f842ebfa1.png)

    
If you want to find the cosine distance between two new latent spaces stored at first_new_latent_example.txt and second_new_latent_example.txt, you can run the command:

    compare first_new_latent_example.txt second_new_latent_example.txt -m cosine

![example-3](https://user-images.githubusercontent.com/1418557/169188109-0b55b0a1-869a-4dad-be19-bcc6012ddd86.png)


---

You can find the closest protein family to first_new_latent_example.txt in cosine distance by running the command:

    search lat first_new_latent_example.txt -m cosine

![example-4](https://user-images.githubusercontent.com/1418557/169188127-06af9faa-81b7-489a-b87b-82ef9b1b4129.png)

    
You can find the closest family to a new protein sequence (for example new_sequence_example.txt) by running:

    search seq new_sequence_example.txt

![example-5](https://user-images.githubusercontent.com/1418557/169188138-add1c6be-50a8-482b-9ad1-c9c4f463de45.png)

