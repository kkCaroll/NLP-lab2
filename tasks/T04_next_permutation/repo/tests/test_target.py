from seqkit import next_permutation, permutations_from


def test_next_permutation_advances_a_middle_pivot():
    assert next_permutation([1, 2, 3]) == [1, 3, 2]


def test_permutations_from_returns_successive_orders():
    assert permutations_from([1, 2, 3], 3) == [
        [1, 3, 2],
        [2, 1, 3],
        [2, 3, 1],
    ]
