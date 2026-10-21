from pathmont import join_path, resolve_under


def test_join_path_keeps_the_base_for_a_leading_slash_part():
    assert join_path("data", "/reports/q1.csv") == "data/reports/q1.csv"


def test_resolve_under_keeps_the_root_for_a_leading_slash_part():
    assert resolve_under("data", "/etc/passwd") == "data/etc/passwd"
