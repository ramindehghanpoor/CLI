# CLI

### Software Info:

Software Name: CompBio Lab  
Software Version: v0.2  
PyPI: https://pypi.org/project/compbiolab-CLI/

### Overview

Our goal for this project is to read a new input sequence and find the protein family in which it belongs to by comparing it with existing sequences in the database. We can also read two different inputs sequences and compare them to find the similarities between the two. The program can be downloaded from PyPI (Python Package Index) and will have a Command Line Interface.

1. Find the distance between fingerprints of two protein families using different metrics (Euclidean, Minkowski, Cityblock, Sqeuclidean, Cosine, etc.)

2. Find the closest family to a new protein sequence

## Installation

    1. Install Python 3.7 or above. (https://www.python.org/downloads/)  
    2. Open up Command Prompt. (Windows Key + R → Type cmd → Enter)
    3. In Command Prompt, type pip install compbiolab-CLI.

## Usage

### Comparing protein sequences

Find the distance between fingerprints of two protein families

    compare [-h] [-names BOOL] [-n1 FIRST_FAMILY] [-n2 SECOND_FAMILY] [-nl1 NL1] [-nl2 NL2] [-m DISTANCE_METRIC] [-p P_NORM] [-out OUTPUT_FILE] [-of OUTPUT_FORMAT] [-om OUTPUT_MODE]

#### Arguments

* `-names`

    Boolean, Show available protein family names

* `-fn`, `-n1`, `-n2`

    Protein family's name. Provide an existing protein family's name to compare it with one of the other existing protein families or a new latent space.
	
* `-ls`, `-nl1`, `-nl2`

    The file name of a new latent space. Provide a new protein family latent space to compare it with one of the existing protein families or with the other new latent space. The file should contain 30 floats, each float in a separate line.

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

    search [-h] [-names SHOW_NAMES_BOOL] [-m DISTANCE_METRIC] [-p P_NORM] [-nl1 NL1] [-ns NS] [-out OUTPUT_FILE] [-of OUTPUT_FORMAT] [-om OUTPUT_MODE]

#### Arguments

* `-names`

    Boolean, Show available protein family names

* `-lat`, `-nl1`

    The file name of a new latent space. Provide a new protein family latent space. The closest protein family to this new latent space will be shown.

* `-seq`, `-ns`

    The name of the file containing a protein sequence. Provide a protein sequence to get the closest protein family for this sequence.

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

## Available metrics

*euclidean (default)*, minkowski, cityblock, sqeuclidean, cosine, correlation, hamming, jaccard, chebyshev, canberra, braycurtis, yule, dice, kulsinski, rogerstanimoto, russellrao, sokalmichener, sokalsneath

## Examples

To see all the available protein families, run command:

    compare -names
        
You can find the Euclidean distance between two families ATKA_ATKC and CDSA_RSEP by running the command:

    compare -n1 ATKA_ATKC -n2 CDSA_RSEP
    
If you want to find the Cityblock distance between ATKA_ATKC and a new latent space stored at second_new_latent_example.txt, you can run the command:

    compare -n1 ATKA_ATKC -nl2 second_new_latent_example.txt -m cityblock
    
If you want to find the cosine distance between two new latent spaces stored at first_new_latent_example.txt and second_new_latent_example.txt, you can run the command:

    compare -nl1 first_new_latent_example.txt -nl2 second_new_latent_example.txt -m cityblock

---

You can find the closest protein family to first_new_latent_example.txt in cosine distance by running the command:

    search -nl1 first_new_latent_example.txt -m cosine
    
You can find the closest family to a new protein sequence (for example new_sequence_example.txt) by running:

    search -ns new_sequence_example.txt
