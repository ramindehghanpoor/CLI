from .load_files import load_family, load_ls_file


class LSCompare:
    def __init__(self, pfnames, nfiles):
        self.names = pfnames
        self.files = nfiles
        self.ls_data = []
        self.ls_names = []
        self.load_vectors()

    def load_vectors(self):
        # we already know there are only two total
        for i in self.names:
            self.ls_data.append(load_family(i + '.txt'))
            self.ls_names.append(i)
        for j in self.files:
            self.ls_data.append(load_ls_file(j))
            self.ls_names.append(j)
