# Author: Ramin Dehghanpoor

from scipy.spatial import distance


def get_distance_function(distance_metric):
    """

    :param distance_metric: Distance metric
    :type distance_metric: str
    :return: The distance function
    :rtype: function
    """
    # distance metric

    # set the distance metric
    if distance_metric == 'minkowski':
        distance_function = distance.minkowski
    elif distance_metric == 'cityblock':
        distance_function = distance.cityblock
    elif distance_metric == 'sqeuclidean':
        distance_function = distance.sqeuclidean
    elif distance_metric == 'cosine':
        distance_function = distance.cosine
    elif distance_metric == 'correlation':
        distance_function = distance.correlation
    elif distance_metric == 'hamming':
        distance_function = distance.hamming
    elif distance_metric == 'jaccard':
        distance_function = distance.jaccard
    elif distance_metric == 'chebyshev':
        distance_function = distance.chebyshev
    elif distance_metric == 'canberra':
        distance_function = distance.canberra
    elif distance_metric == 'braycurtis':
        distance_function = distance.braycurtis
    elif distance_metric == 'yule':
        distance_function = distance.yule
    elif distance_metric == 'dice':
        distance_function = distance.dice
    elif distance_metric == 'kulsinski':
        distance_function = distance.kulsinski
    elif distance_metric == 'rogerstanimoto':
        distance_function = distance.rogerstanimoto
    elif distance_metric == 'russellrao':
        distance_function = distance.russellrao
    elif distance_metric == 'sokalmichener':
        distance_function = distance.sokalmichener
    elif distance_metric == 'sokalsneath':
        distance_function = distance.sokalsneath
    else:
        distance_function = distance.euclidean
    return distance_function
