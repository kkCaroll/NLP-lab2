from rankkit import top_k


def test_top_k_returns_the_requested_number_of_values():
    assert top_k([5, 3, 9, 1], 2) == [9, 5]


def test_top_k_preserves_the_order_of_equal_scores():
    scores = [("ana", 7), ("bo", 9), ("cy", 7), ("dee", 5)]
    assert top_k(scores, 2, key=lambda entry: entry[1]) == [("bo", 9), ("ana", 7)]
