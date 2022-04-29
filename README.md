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

* `-n11`

    [optional] The file name of the first new latent space. Provide a new protein family latent space to compare it with one of the existing protein families or with the second new latent space. The file should contain 30 floats, each float in a separate line.

* `-n12`

    [optional] The file name of the second new latent space. Provide a new protein family latent space to compare it with one of the existing protein families or with the first new latent space. The file should contain 30 floats, each float in a separate line.

### Searching

Find the closest family to a new protein sequence

    search [-h] [-names SHOW_NAMES_BOOL] [-m DISTANCE_METRIC] [-p P_NORM] [-nl1 NL1] [-ns NS]

#### Arguments

* `-names`

    Boolean, Show available protein family names

* `-m`

    [optional] Distance metric. Default: euclidean

* `-p`

    [optional] Scalar, The p-norm to apply for Minkowski, weighted and unweighted. Default: 2

* `-n11`

    The file name of a new latent space. Provide a new protein family latent space. The closest protein family to this new latent space will be shown.

* `-ns`

    The name of the file containing a protein sequence. Provide a protein sequence to get the closest protein family for this sequence.

## Available metrics

*euclidean (default)*, minkowski, cityblock, sqeuclidean, cosine, correlation, hamming, jaccard, chebyshev, canberra, braycurtis, yule, dice, kulsinski, rogerstanimoto, russellrao, sokalmichener, sokalsneath