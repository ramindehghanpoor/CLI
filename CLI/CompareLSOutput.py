from typing import TextIO


class CompareLSOutput:

    a1: str
    a2: str
    distance_metric: str
    result: str

    def __init__(self, a1: str, a2: str, distance_metric: str, result: str):
        """

        :param a1: Name of the first latent space
        :type a1: str
        :param a2: Name of the second latent space
        :type a2: str
        :param distance_metric: Name of the distance function
        :type distance_metric: str
        :param result: Distance
        :type result: str
        """
        self.a1 = a1
        self.a2 = a2
        self.distance_metric = distance_metric
        self.result = result

    def to_stdout(self):
        print(self.distance_metric + ' distance between ' + self.a1 + ' and ' + self.a2 + ': ' + self.result)

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
                outf.write(self.distance_metric + ' distance between ' + self.a1 + ' and ' + self.a2 + ': ' + self.result + '\n')
            else:
                outf.write(self.a1 + ',' + self.a2 + ',' + self.distance_metric + ',' + self.result + '\n')
