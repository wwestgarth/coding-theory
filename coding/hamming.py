from textwrap import wrap

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


class Codex:
    """
    Class that given a list of data, maps these to bit values and allows
    conversion between the two
    """

    @staticmethod
    def decimal_to_binary(dec):
        return "{0:b}".format(dec)

    def __init__(self, basis):
        # Store basis
        self.basis = basis[:]

        # Calculate bit length
        self.max_bit_len = len( self.decimal_to_binary(len(basis) -1) )

    def bits_to_data(self, bits):
        """
        Convert given bits generated from `basis' back into their true value
        """

        position = int(bits,2)
        return self.basis[position]

    def data_to_bits(self, data):
        """
        Convert the given vectory from the basis into a bit-representations
        """
        position = self.basis.index(data)
        return self.decimal_to_binary(position).rjust(self.max_bit_len,'0')

class Code:
    """
    Class to bit-ify a stream from a given basis into a code which
    """

    def _expand(self, bits):
        """
        Expand each bit to achieve desired hamming distance
        """
        return "".join([x*self.hamming_distance for x in bits])

    def _reduce(self, bits):
        """
        Reduce all expanded bits to restore original bit-basis
        """
        reduced = []
        for i in range(0, len(bits), self.hamming_distance):
            reduced.append( bits[i] )
        return "".join(reduced)

    def __init__(self, basis, hamming_distance=1):

        if hamming_distance < 1:
            raise ValueError

        self.codex = Codex(basis)
        self.hamming_distance=hamming_distance

    def encode(self, input_steam):
        """
        Convert the given stream into bits with defined hamming-distance
        """
        bit_stream = [ self.codex.data_to_bits(x) for x in input_steam ]
        bit_stream = [ self._expand(x) for x in bit_stream]
        return "".join(bit_stream)

    def decode(self, bit_steam):
        """
        Convert the given bit_stream back into its original form
        """
        split_stream = wrap(bit_steam, self.hamming_distance*self.codex.max_bit_len)
        split_stream = [self._reduce(x) for x in split_stream]
        return [self.codex.bits_to_data(x) for x in split_stream]

