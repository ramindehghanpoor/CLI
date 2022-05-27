import argparse
from typing import List, Callable
from argparse_formatter import FlexiFormatter
from .CompareLSOutput import CompareLSOutput
from .get_metric import get_distance_function
from .family_list import print_families
from .LSVector import LSVector
from .CompareLS import CompareLS
from . import output_opt_parser, dist_opt_parser, metrics_epilog
from .output_results import output_result

family_help: str = "Protein family's name. Provide an existing protein family's name or the file name of a new latent space. Files should contain 30 floats, each float in a separate line."

compare_usage: str = '''%(prog)s [-h] <protein_family> <protein_family> [output_options] [distance_options]
                    list names'''


def run(args: argparse.Namespace):
    """

    Parameters
    ----------
    args : argparse.Namespace
        Argparse arguments
    """
    # Get the arguments

    # Families
    family_list: List[str] = args.family_name

    # Set the distance metric
    distance_metric: str = args.distance_metric
    distance_function: Callable = get_distance_function(distance_metric)

    # The p-norm to apply for Minkowski
    p_norm: int = args.p_norm  # default is 2

    # Output arguments
    output_filename: str = args.output_file
    out_format: str = args.output_format
    out_mode: str = args.output_mode

    # List protein family names
    if family_list == ['list', 'names']:
        print_families(None)  # argument required in search but never used
        return

    else:
        # turn names into objects containing data
        v: List[LSVector] = [LSVector(family_list[0]), LSVector(family_list[1])]

    # find distance between the vectors, create CompareOutput object
    res: CompareLSOutput = CompareLS(v, distance_function, p_norm).result
    output_result(res, output_filename, out_format, out_mode)


def main():
    parser: argparse.ArgumentParser = argparse.ArgumentParser(usage=compare_usage, description='Find the distance between fingerprints of two protein families.',
                                                              formatter_class=FlexiFormatter, parents=[output_opt_parser, dist_opt_parser], epilog=metrics_epilog)
    parser.add_argument("family_name", help=family_help, metavar="protein_family", nargs=2, type=str)
    parser.add_argument("ln", metavar='list names', nargs=argparse.SUPPRESS, help="Show available protein family names")

    parser.set_defaults(func=run)
    args: argparse.Namespace = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
