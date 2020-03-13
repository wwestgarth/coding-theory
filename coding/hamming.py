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

    def _convert_data_to_bits(self, data):
        """
        Convert the given vector from the basis into a bit-representations
        """
        position = self.basis.index(data)
        return self.decimal_to_binary(position).rjust(self.max_bit_len, '0')

    def __init__(self, basis):
        # Store basis
        self.basis = basis[:]

        # Calculate bit length
        self.max_bit_len = len(self.decimal_to_binary(len(basis) -1))

        self._map_data_to_bits = dict()
        self._map_bits_to_data = dict()

        # Create double map
        for basis_vector in self.basis:
            as_bits = self._convert_data_to_bits(basis_vector)
            self._map_data_to_bits[basis_vector] = as_bits
            self._map_bits_to_data[as_bits] = basis_vector


    def bits_to_data(self, bits):
        """
        Lookup given bits in map to return their value in the `basis'
        """
        return self._map_bits_to_data[bits]

    def data_to_bits(self, data):
        """
        Lookup given data in map to return their value in as bits
        """
        return self._map_data_to_bits[data]


class Code:
    """
    Class to bit-ify a stream from a given basis into a code which
    """

    def _closest_basis_vector(self, unknown_vector):
        """
        Return the closest basis vector to the given unknown vector
        """

        # Order basis by hamming distance to unknown
        basis = list(self._hammed_basis)
        hamming_distances = [(basis_vector, distance(basis_vector, unknown_vector)) for basis_vector in basis]
        hamming_distances.sort(key=lambda x: x[1])

        closest = hamming_distances[0]

        # If the distance is not less than the hamming distance, the closest basis vector
        # is ambiguous
        if closest[1] < self.hamming_distance:
            return closest[0]

        return None

    def _expand(self, bits):
        """
        Expand each bit to achieve desired hamming distance
        """
        return "".join([x*self.hamming_distance for x in bits])

    def _reduce(self, bits):
        """
        Reduce all expanded bits to restore original bit-basis
        """
        closest = bits

        if bits in self._hammed_basis:
            pass
        elif not self._attempt_recovery:
            return None
        else:
            closest = self._closest_basis_vector(bits)
            if not closest:
                return None

        reduced = []
        for i in range(0, len(closest), self.hamming_distance):
            reduced.append(closest[i])
        return "".join(reduced)

    def __init__(self, basis, hamming_distance=1, attempt_recovery=False):

        if hamming_distance < 1:
            raise ValueError

        self.codex = Codex(basis)
        self.hamming_distance = hamming_distance
        self._hammed_basis = {self._expand(self.codex.data_to_bits(x)) for x in basis}
        self._attempt_recovery = attempt_recovery

    def encode(self, input_steam):
        """
        Convert the given stream into bits with defined hamming-distance
        """
        bit_stream = [self.codex.data_to_bits(x) for x in input_steam]
        bit_stream = [self._expand(x) for x in bit_stream]
        return "".join(bit_stream)

    def decode(self, bit_steam):
        """
        Convert the given bit_stream back into its original form
        """
        split_stream = wrap(bit_steam, self.hamming_distance*self.codex.max_bit_len)
        split_stream = [self._reduce(x) for x in split_stream]
        return [self.codex.bits_to_data(x) if x else None for x in split_stream]

    def set_attempt_recovery(self, new_value):
        """
        Toggle the attempt_recovery option
        """
        old_value = self._attempt_recovery
        self._attempt_recovery = new_value
        return old_value
