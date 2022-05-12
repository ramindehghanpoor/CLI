class SearchSQOutput:

    def __init__(self, seq, closest, accuracy):
        self.seq = seq
        self.closest = closest
        self.accuracy = accuracy

    def to_stdout(self):
        print('The closest protein family to ' + self.seq + ' is ' + self.closest + ' with average accuracy: ' + self.accuracy)

    # Not currently implemented in other modules
    def to_file(self, fname, ftype, mode):
        with open(fname, mode) as outf:
            if ftype == "text":
                outf.write('The closest protein family to ' + self.seq + ' is ' + self.closest + ' with average accuracy: ' + self.accuracy + '\n')
            else:
                outf.write(self.seq + ',' + self.closest + ',' + self.accuracy + '\n')
