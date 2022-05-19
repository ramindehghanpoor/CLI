from typing import TextIO


class SearchSQOutput:
    seq: str
    closest: str
    accuracy: str

    def __init__(self, seq: str, closest: str, accuracy: str):
        """

        :param seq: Name of the sequence
        :type seq: str
        :param closest: Name of the closest protein family
        :type closest: str
        :param accuracy: Accuracy
        :type accuracy: str
        """
        self.seq = seq
        self.closest = closest
        self.accuracy = accuracy

    def to_stdout(self):
        print('The closest protein family to ' + self.seq + ' is ' + self.closest + ' with average accuracy: ' + self.accuracy)

    # Not currently implemented in other modules
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
                outf.write('The closest protein family to ' + self.seq + ' is ' + self.closest + ' with average accuracy: ' + self.accuracy + '\n')
            else:
                outf.write(self.seq + ',' + self.closest + ',' + self.accuracy + '\n')
