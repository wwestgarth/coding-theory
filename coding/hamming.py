

def distance(code1, code2):
    """
    Return the Hamming distance for the given strings. Raises an exception if input are not strings
    or are not of equal length.
    """
    if type(code1) != str or type(code2) != str:
        raise TypeError
    if len(code1) != len(code2):
        raise ValueError

    diffs = [x for x in zip(code1, code2) if x[0] != x[1]]
    return len(diffs)


def weight(code):
    """
    Return the Hamming weight for the given string
    """
    if type(code) != str:
        raise TypeError
    identity = "0"*len(code)
    return distance(identity, code)
