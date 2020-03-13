import pytest
from itertools import product
from coding import hamming


def flip_bit(bit_string, position):
    "Given a string representation of bit, flips the bit in the given position"
    unpacked = list(bit_string)
    unpacked[position] = "1" if unpacked[position] == "0" else "0"
    return ''.join(unpacked)


@pytest.mark.parametrize("test_input, expected", [(("0101", "1010"), 4), (("1111", "1111"), 0)])
def test_hamming_distance(test_input, expected):
    """
    Test that hamming distances are correctly calculated
    """
    assert hamming.distance(test_input[0], test_input[1]) == expected


@pytest.mark.parametrize("test_input, expected", [("000000", 0), ("11111", 5), ("10001", 2)])
def test_hamming_weight(test_input, expected):
    """
    Test that hamming weights are correctly calculated
    """
    assert hamming.weight(test_input) == expected

@pytest.mark.parametrize("test_input", [[1,2,3,4], ["duck", "Goose", "Horse"], range(12,22)])
def test_code_pairwise_checks(test_input):
    """
    Test that encoding anddecoding produce returns us to the original input
    """
    code = hamming.Code(test_input, hamming_distance=3)
    decoded = code.decode(code.encode(test_input))
    for pair in zip(test_input, decoded):
        assert pair[0] == pair[1] 

@pytest.mark.parametrize("test_input, expected", [("00","000000"), ("10","111000")])
def test_codex_expansion(test_input, expected):
    """
    Test the expansion of the bit-basis 
    """
    code = hamming.Code( [1,2,3,4], hamming_distance=3)
    expanded = code._expand(test_input)
    assert expanded == expected 
    assert test_input == code._reduce(expanded)


@pytest.mark.parametrize("test_input", [1,2,3,4])
def test_code_forced_hamming(test_input):
    """
    Test that a hamming distance can be forced by bit-expansion
    """
    basis = ["1", "2", "3", "4"]
    code = hamming.Code(basis, hamming_distance=test_input)
    code_basis = [code.encode(x) for x in basis]

    cartesian_prod = [ x for x in product(code_basis, code_basis) if x[0] != x[1] ]
    for pair in cartesian_prod:
        assert hamming.distance(pair[0],pair[1]) >= test_input


def test_ruined_message():

    test_input = ["duck", "Goose", "Horse"]
    code = hamming.Code(test_input, hamming_distance=3)
    encoded = code.encode([test_input[0]])
    decoded = code.decode(flip_bit(encoded, 0))

    assert decoded[0] is None
