class CompareOutput:

    def __init__(self, a1, a2, distance_metric, result):
        self.a1 = a1
        self.a2 = a2
        self.distance_metric = distance_metric
        self.result = result

    def to_stdout(self):
        print(self.distance_metric + ' distance between ' + self.a1 + ' and ' + self.a2 + ': ' + self.result)

    def to_file(self, fname, ftype, mode):
        with open(fname, mode) as outf:
            if ftype == "text":
                outf.write(self.distance_metric + ' distance between ' + self.a1 + ' and ' + self.a2 + ': ' + self.result + '\n')
            else:
                outf.write(self.a1 + ',' + self.a2 + ',' + self.distance_metric + ',' + self.result + '\n')
