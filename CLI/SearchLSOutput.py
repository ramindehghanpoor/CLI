from typing import TextIO


class SearchLSOutput:

    ls: str
    distance_metric: str
    closest: str
    distance: str

    def __init__(self, ls: str, distance_metric: str, closest: str, distance: str):
        """

        :param ls: Name of the latent space
        :type ls: str
        :param distance_metric: Name of the distance function
        :type distance_metric: str
        :param closest: Name of the closest protein family
        :type closest: str
        :param distance: Distance from the closest protein family
        :type distance: str
        """
        self.ls = ls
        self.distance_metric = distance_metric
        self.closest = closest
        self.distance = distance

    def to_stdout(self):
        print('The closest protein family to ' + self.ls + ' is ' + self.closest + ' with ' + self.distance_metric + ' distance: ' + self.distance)

    def to_file(self, fname: str, ftype: str, mode: str):
        """

        :param fname: Output filename
        :type fname: str
        :param ftype: Output format
        :type ftype: str
        :param mode: Output mode
        :type mode: str
        """
        outf: TextIO
        with open(fname, mode) as outf:
            if ftype == "text":
                outf.write('The closest protein family to ' + self.ls + ' is ' + self.closest + ' with ' + self.distance_metric + ' distance: ' + self.distance + '\n')
            else:
                outf.write(self.ls + ',' + self.distance_metric + ',' + self.closest + ',' + self.distance + '\n')
