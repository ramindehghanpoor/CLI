from .load_files import load_family, load_ls_file, is_pf


class LSVectors:
    def __init__(self, pfnames):
        """

        :type pfnames: List[str]
        """
        self.names = pfnames
        self.ls_data = []
        self.ls_names = []
        self.load_vectors()

    def load_vectors(self):
        for ls in self.names:
            self.ls_names.append(ls)
            if is_pf(ls):
                self.ls_data.append(load_family(ls + '.txt'))
            else:
                self.ls_data.append(load_ls_file(ls))
