import pandas as pd
import sys

if sys.version_info < (3, 9):
    # importlib.resources either doesn't exist or lacks the files()
    # function, so use the PyPI version:
    import importlib_resources
else:
    # importlib.resources has files(), so use that:
    import importlib.resources as importlib_resources

def print_families():
    print('Here is a list of protein families\' names:\n')
    pkg = importlib_resources.files("CLI")
    f = pkg / "seq_lengths.csv"
    family_list = pd.read_csv(f,usecols=['name']).squeeze("columns")

    print(*family_list, sep=', ')