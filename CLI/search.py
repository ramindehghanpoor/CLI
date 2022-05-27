import argparse
from argparse_formatter import FlexiFormatter
from .search_seq import seq_search
from .family_list import print_families
from .search_lat import ls_search
from . import output_opt_parser, dist_opt_parser, metrics_epilog

lat_help: str = "Provide a new protein family latent space. The closest protein family to this new latent space will be shown."
seq_help: str = "Provide a protein sequence to get the closest protein family for this sequence."


def main():
    parser: argparse.ArgumentParser = argparse.ArgumentParser(description='Find the closest protein family to a new latent space or protein sequence.',
                                                              formatter_class=FlexiFormatter)
    subparsers = parser.add_subparsers(dest='command', title='subcommands', metavar="{lat,seq,list names}")
    parser_ls: argparse.ArgumentParser = subparsers.add_parser('lat', help=lat_help, parents=[output_opt_parser, dist_opt_parser], formatter_class=FlexiFormatter, epilog=metrics_epilog)
    parser_ls.add_argument('latent_space', metavar="filename", help="The file name of a new latent space.", type=str, nargs='+')

    parser_seq: argparse.ArgumentParser = subparsers.add_parser('seq', help=seq_help, parents=[output_opt_parser])
    parser_seq.add_argument('sequence', metavar="filename", help="The name of the file containing a protein sequence.", type=str, nargs='+')

    parser_names: argparse.ArgumentParser = subparsers.add_parser('list names', aliases=['list'], help="Show available protein family names")
    parser_names.add_argument('names', nargs='?', help=argparse.SUPPRESS)
    parser_ls.set_defaults(func=ls_search)
    parser_seq.set_defaults(func=seq_search)
    parser_names.set_defaults(func=print_families)
    args: argparse.Namespace = parser.parse_args()
    # print help text if nothing is selected
    if args.command is None:
        parser.print_help()
    else:
        args.func(args)


if __name__ == "__main__":
    main()
