import sys
import argparse
from .SearchSQOutput import SearchSQOutput
from .output_results import output_result


def seq_search(args: argparse.Namespace):
    if sys.version_info[:3] == (3, 7, 6):
        # don't import function and dependencies if you don't need to
        from .SearchSQ import SearchSQ
        ns: str
        for ns in args.sequence:
            try:
                res: SearchSQOutput = SearchSQ(ns).result
            except Exception as err:
                print("Error")
                exit(err)
            else:
                output_result(res, args.output_file, args.output_format, args.output_mode)

    else:
        print('sequence searches only available with python 3.7.6')
