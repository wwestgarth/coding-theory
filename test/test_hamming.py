import pytest
from coding import hamming


@pytest.mark.parametrize("test_input, expected", [(("0101", "1010"), 4), (("1111", "1111"), 0)])
def test_hamming_distance(test_input, expected):
    assert hamming.distance(test_input[0], test_input[1]) == expected


@pytest.mark.parametrize("test_input, expected", [("000000", 0), ("11111", 5), ("10001", 2)])
def test_hamming_weight(test_input, expected):
    assert hamming.weight(test_input) == expected
	
@pytest.mark.parametrize("test_input", [[1,2,3,4], ["duck", "Goose", "Horse"], range(12,22)])
def test_code_pairwise_checks(test_input):

	code = hamming.Code(test_input)
	decoded = code.decode(code.encode(test_input))
	for pair in zip(test_input, decoded):
		assert pair[0] == pair[1] 