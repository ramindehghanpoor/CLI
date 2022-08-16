import sys
import argparse
from typing import List
from .SearchSQOutput import SearchSQOutput
from .output_results import output_result

debug = True


def seq_search(args: argparse.Namespace):
    """

    Parameters
    ----------
    args : argparse.Namespace
    """
    # get the arguments
    sequences: List[str] = args.sequence
    output_filename: str = args.output_file
    out_format: str = args.output_format
    out_mode: str = args.output_mode
    if sys.version_info[:2] == (3, 7) and ('32 bit' not in sys.version):
        # don't import function and dependencies if you don't need to
        if debug:
            from .SearchSQ import SearchSQ
            ns: str
            for ns in sequences:
                res: SearchSQOutput = SearchSQ(ns).result
                output_result(res, output_filename, out_format, out_mode)
        else:
            try:
                from .SearchSQ import SearchSQ
                ns: str
                for ns in sequences:
                    res: SearchSQOutput = SearchSQ(ns).result
                    output_result(res, output_filename, out_format, out_mode)
            except Exception as err:
                print("Error")
                exit(err)

    else:
        print("Sequence searches only supported on 64-bit Python 3.7")
