def output_result(res, fname, form, mode):
    if fname != "":
        res.to_file(fname, form, mode)
    else:
        res.to_stdout()
