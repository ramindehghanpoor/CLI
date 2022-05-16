from scipy.spatial import distance
from .SearchLSOutput import SearchLSOutput
from .load_files import latent_space_list, load_family


class SearchLS:
    def __init__(self, ls, metric, p_norm):
        """

        :param ls: Latent space
        :type ls: CLI.LSVector.LSVector
        :param metric: Distance function
        :type metric: function
        :param p_norm: The p-norm to apply for Minkowski
        :type p_norm: int
        """
        self.ls_name = ls.ls_name
        self.ls_data = ls.ls_data
        self.metric = metric
        self.p_norm = p_norm
        self.result = self.do_search()

    def do_search(self):
        """

        :rtype: CLI.SearchLSOutput.SearchLSOutput
        """
        closest_family = "none"
        min_dist = float("inf")
        for i in range(len(latent_space_list)):
            if self.metric == distance.minkowski:
                distance_result = self.metric(self.ls_data, load_family(latent_space_list[i]), self.p_norm)
            else:
                distance_result = self.metric(self.ls_data, load_family(latent_space_list[i]))

            if distance_result < min_dist:
                min_dist = distance_result
                closest_family = latent_space_list[i]
        return SearchLSOutput(self.ls_name, self.metric.__name__, closest_family[:-4], str(min_dist))
