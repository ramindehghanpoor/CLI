from scipy.spatial import distance
from .CompareLSOutput import CompareLSOutput


class CompareLS:
    def __init__(self, vectors, metric, p_norm):
        """

        :param vectors: Two latent spaces
        :type vectors: List[CLI.LSVector.LSVector]
        :param metric: Distance function
        :type metric: function
        :param p_norm: The p-norm to apply for Minkowski
        :type p_norm: int
        """
        self.vectors = vectors
        self.metric = metric
        self.p_norm = p_norm
        self.result = self.do_compare()

    def do_compare(self):
        """

        :rtype: CompareLSOutput
        """
        # find distance between the vectors
        if self.metric == distance.minkowski:
            distance_result = self.metric(self.vectors[0].ls_data, self.vectors[1].ls_data, self.p_norm)
        else:
            distance_result = self.metric(self.vectors[0].ls_data, self.vectors[1].ls_data)

        # create CompareLSOutput object
        return CompareLSOutput(
            self.vectors[0].ls_name, self.vectors[1].ls_name, self.metric.__name__, str(distance_result))
