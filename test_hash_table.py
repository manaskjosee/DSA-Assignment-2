"""
test_hash_table.py
-------------------
Minimal sanity tests (no external test framework needed).
Run with:  python3 test_hash_table.py
"""

from hash_table import DivisionHashTable, linear_search

SONG_IDS = [105, 210, 315, 420, 525, 630, 735, 840]


def test_hash_function():
    ht = DivisionHashTable(10)
    assert ht.h(105) == 5
    assert ht.h(210) == 0
    print("test_hash_function: PASS")


def test_insert_and_collisions():
    ht = DivisionHashTable(10)
    ht.build(SONG_IDS)
    assert ht.collision_count() == 6
    assert ht.load_factor() == 0.8
    assert ht.non_empty_buckets() == 2
    print("test_insert_and_collisions: PASS")


def test_search_found():
    ht = DivisionHashTable(10)
    ht.build(SONG_IDS)
    result = ht.search(630)
    assert result.found is True
    assert result.comparisons == 3
    print("test_search_found: PASS")


def test_search_not_found():
    ht = DivisionHashTable(10)
    ht.build(SONG_IDS)
    result = ht.search(999)
    assert result.found is False
    print("test_search_not_found: PASS")


def test_linear_search():
    result = linear_search(SONG_IDS, 735)
    assert result.found is True
    assert result.comparisons == 7
    print("test_linear_search: PASS")


def test_prime_table_no_collisions():
    ht = DivisionHashTable(11)
    ht.build(SONG_IDS)
    assert ht.collision_count() == 0
    print("test_prime_table_no_collisions: PASS")


if __name__ == "__main__":
    test_hash_function()
    test_insert_and_collisions()
    test_search_found()
    test_search_not_found()
    test_linear_search()
    test_prime_table_no_collisions()
    print("\nAll tests passed.")
