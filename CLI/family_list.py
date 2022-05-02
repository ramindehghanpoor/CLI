import pandas as pd
import importlib.resources

def print_families():
    print('Here is a list of protein families\' names:\n')
    f = importlib.resources.path("CLI", "seq_lengths.csv")
    family_list = pd.read_csv(f,usecols=['name']).squeeze("columns")

    print(*family_list, sep=', ')