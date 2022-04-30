import pandas as pd

def print_families():
    print('Here is a list of protein families\' names:\n')
    family_list = pd.read_csv('seq_lengths.csv',usecols=['name']).squeeze("columns")
    print(*family_list, sep=', ')