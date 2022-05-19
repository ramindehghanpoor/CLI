def output_result(res, fname, form, mode):
    """

    :param res: Result
    :type res: Union[CLI.CompareLSOutput.CompareLSOutput, CLI.SearchLSOutput.SearchLSOutput, CLI.SearchSQOutput.SearchSQOutput]
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
