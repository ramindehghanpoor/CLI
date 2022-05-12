import sys


def seq_search(args):
    if sys.version_info[:3] == (3, 7, 6):
        # don't import function and dependencies if you don't need to
        from .SearchSQ import SearchSQ
        for ns in args.sequence:
            res = SearchSQ(ns).result
            res.to_stdout()
    else:
        print('sequence searches only available with python 3.7.6')
