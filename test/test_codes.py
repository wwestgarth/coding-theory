"""
Test set for the Code class
"""

from itertools import product
import pytest

from coding import codes
from coding import hamming
from coding import exceptions

# pylint: disable=protected-access

def flip_bit(bit_string, position):
    "Given a string representation of bit, flips the bit in the given position"
    unpacked = list(bit_string)
    unpacked[position] = "1" if unpacked[position] == "0" else "0"
    return ''.join(unpacked)


@pytest.mark.parametrize("test_input", [[1, 2, 3, 4],
                                        ["duck", "Goose", "Horse"],
                                        list(range(12, 22))])
def test_code_pairwise_checks(test_input):
    """
    Test that encoding anddecoding produce returns us to the original input
    """
    code = codes.Code(test_input, hamming_distance=3)
    decoded = code.decode(code.encode(test_input))
    for pair in zip(test_input, decoded):
        assert pair[0] == pair[1]


@pytest.mark.parametrize("test_input, expected", [("00", "000000"), ("10", "111000")])
def test_codex_expansion(test_input, expected):
    """
    Test the expansion of the bit-basis
    """
    code = codes.Code([1, 2, 3, 4], hamming_distance=3)
    expanded = code._expand(test_input)
    assert expanded == expected
    assert test_input == code._reduce(expanded)


@pytest.mark.parametrize("test_input", [1, 2, 3, 4])
def test_code_forced_hamming(test_input):
    """
    Test that a hamming distance can be forced by bit-expansion
    """
    basis = ["1", "2", "3", "4"]
    code = codes.Code(basis, hamming_distance=test_input)
    code_basis = [code.encode([x]) for x in basis]

    cartesian_prod = [x for x in product(code_basis, code_basis) if x[0] != x[1]]
    for pair in cartesian_prod:
        assert hamming.distance(pair[0], pair[1]) >= test_input


def test_ruined_message():
    """
    Test that a message with a flipped bit returns None for that particular piece of data
    """
    test_input = ["duck", "Goose", "Horse"]
    code = codes.Code(test_input, hamming_distance=3)
    encoded = code.encode([test_input[0]])
    decoded = code.decode(flip_bit(encoded, 0))

    assert decoded[0] is None
    code.set_attempt_recovery(True)
    decoded = code.decode(flip_bit(encoded, 0))
    assert decoded[0] == test_input[0]

def test_recovery_toggle():
    """
    Test that the attempt_recovery option can be toggled
    """
    test_input = ["duck", "Goose", "Horse"]
    code = codes.Code(test_input, hamming_distance=3)
    assert not code.set_attempt_recovery(True)
    assert code.set_attempt_recovery(False)
    assert not code.set_attempt_recovery(False)


def test_closet_basis():
    """
    Test that the attempt_recovery option can be toggled
    """
    test_input = ["duck", "Goose", "Horse"]
    code = codes.Code(test_input, hamming_distance=3)
    encoded = code.encode([test_input[0]])
    assert code._closest_basis_vector(flip_bit(encoded, 0)) == encoded


def test_not_in_basis():
    """
    Test that the appropriate error is raised when asked to encode an element
    that is not in the codes' basis
    """
    basis = ["duck", "Goose", "Horse"]
    code = codes.Code(basis, hamming_distance=3)

    with pytest.raises(exceptions.ValueNotInBasis):
        code.encode(["human"])
