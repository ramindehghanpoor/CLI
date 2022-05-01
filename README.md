# CLI
CLI tool for CS410 project

## Usage

### Comparing protein sequences

Find the distance between fingerprints of two protein families

    compare [-h] [-n1 FIRST_FAMILY] [-n2 SECOND_FAMILY] [-names SHOW_NAMES_BOOL] [-m DISTANCE_METRIC] [-p P_NORM] [-nl1 NL1] [-nl2 NL2]

#### Arguments

* `-n1`

    First family's name

* `-n2`

    Second family's name

* `-names`

    Boolean, Show available protein family names

* `-m`

    [optional] Distance metric. Default: euclidean

* `-p`

    [optional] Scalar, The p-norm to apply for Minkowski, weighted and unweighted. Default: 2

* `-nl1`

    [optional] The file name of the first new latent space. Provide a new protein family latent space to compare it with one of the existing protein families or with the second new latent space. The file should contain 30 floats, each float in a separate line.

* `-nl2`

    [optional] The file name of the second new latent space. Provide a new protein family latent space to compare it with one of the existing protein families or with the first new latent space. The file should contain 30 floats, each float in a separate line.

### Searching

Find the closest family to a new protein sequence

    search [-h] [-names SHOW_NAMES_BOOL] [-m DISTANCE_METRIC] [-p P_NORM] [-nl1 NL1] [-nl2 NL2] [-ns NS]

#### Arguments

* `-names`

    Boolean, Show available protein family names

* `-m`

    [optional] Distance metric. Default: euclidean

* `-p`

    [optional] Scalar, The p-norm to apply for Minkowski, weighted and unweighted. Default: 2

* `-nl1`

    The file name of a new latent space. Provide a new protein family latent space. The closest protein family to this new latent space will be shown.

* `-nl2`

    The file name of a new latent space. Provide a new protein family latent space. The closest protein family to this new latent space will be shown.

* `-ns`

    The name of the file containing a protein sequence. Provide a protein sequence to get the closest protein family for this sequence.

## Available metrics

*euclidean (default)*, minkowski, cityblock, sqeuclidean, cosine, correlation, hamming, jaccard, chebyshev, canberra, braycurtis, yule, dice, kulsinski, rogerstanimoto, russellrao, sokalmichener, sokalsneath

## Examples

To see all the available protein families, run command:

    compare -names 1
        
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
