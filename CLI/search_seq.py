import sys
from .output_results import output_result


def seq_search(args):
    if sys.version == '3.7.6 (default, Jan  8 2020, 19:59:22) \n[GCC 7.3.0]':
        # don't import function and dependencies if you don't need to
        from .SearchSQ import SearchSQ
        for ns in args.sequence:
            try:
                res = SearchSQ(ns).result
            except Exception as err:
                print("Error")
                exit(err)
            else:
                output_result(res, args.output_file, args.output_format, args.output_mode)

    else:
        errormessage = "Sequence searches not supported on this python version."
        url = "https://github.com/cfogel/CLI/raw/main/compbiolab-cli.yml"
        dowloadmessage = "See " + url + " for the system requirements to use this feature."
        print(errormessage)
        print(dowloadmessage)
