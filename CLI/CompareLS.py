from typing import List
from numpy import double
from pandas.compat.numpy import function
from scipy.spatial import distance
import CLI
from .CompareLSOutput import CompareLSOutput
from .LSVector import LSVector


class CompareLS:
    vectors: List[LSVector]
    metric: function
    p_norm: int
    result: CompareLSOutput

    def __init__(self, vectors: List[CLI.LSVector.LSVector], metric: function, p_norm: int):
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

    def do_compare(self) -> CLI.CompareLSOutput.CompareLSOutput:
        """

        :return: Result of the comparison
        :rtype: CLI.CompareLSOutput.CompareLSOutput
        """
        # find distance between the vectors
        if self.metric == distance.minkowski:
            distance_result: double = self.metric(self.vectors[0].ls_data, self.vectors[1].ls_data, self.p_norm)
        else:
            distance_result = self.metric(self.vectors[0].ls_data, self.vectors[1].ls_data)

        # create CompareLSOutput object
        return CompareLSOutput(
            self.vectors[0].ls_name, self.vectors[1].ls_name, self.metric.__name__, str(distance_result))
