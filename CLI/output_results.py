from typing import Union
from . import CompareLSOutput, SearchLSOutput, SearchSQOutput


def output_result(res: Union[
    SearchLSOutput.SearchLSOutput, SearchSQOutput.SearchSQOutput, CompareLSOutput.CompareLSOutput], fname: str, form: str, mode: str):
    """

    :param res: Result
    :type res: Union[CompareLSOutput.CompareLSOutput, SearchLSOutput.SearchLSOutput, SearchSQOutput.SearchSQOutput]
    :param fname: Output filename
    :type fname: str
    :param form: Output format
    :type form: str
    :param mode: Output mode
    :type mode: str
    """
    if fname != "":
        res.to_file(fname, form, mode)
    else:
        res.to_stdout()
