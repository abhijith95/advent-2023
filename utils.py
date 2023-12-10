def return_lines(txtFile: str) -> list[str]:
    """Function that will go through a text file and return the lines as list of string

    Parameters
    ----------
    txtFile : str
        name of the text file

    Returns
    -------
    list[str]
        lines in the text file
    """
    with open(txtFile, "r") as f:
        lines: list[str] = f.readlines()
    # we remove the new line character at the end of the lines
    lines = [line.replace("\n", "") for line in lines]
    return lines
