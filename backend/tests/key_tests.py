import pytest
from collections import Counter
import re
from services import is_valid_udprn, key_count, distinct_key_count, get_overlap_count, calculate_overlap_product

def test_is_valid_udprn():
    # This test ensures that only valid keys (8 digits, and not "") are added to the key arrays 
    assert is_valid_udprn("12345678") is True
    assert is_valid_udprn("00000000") is True
    assert is_valid_udprn("1234") is False
    assert is_valid_udprn("abcdefgh") is False
    assert is_valid_udprn("1234567a") is False
    assert is_valid_udprn("") is False

def test_key_count():
    two_keys = ['1', '2']
    four_keys = ['1', '2', '3', '4']
    assert key_count(two_keys, four_keys) == (2, 4)
    assert key_count([], []) == (0, 0)

def test_distinct_key_count():
    two_distinct_keys = ['4', '5', '5']
    three_distinct_keys = ['1', '2', '3', '3']
    assert distinct_key_count(two_distinct_keys, three_distinct_keys) == (2, 3)
    assert distinct_key_count([], []) == (0, 0)

def test_get_overlap_count():
    f1 = ['1', '2', '3', '3']
    f2 = ['3', '4', '5', '3']
    assert get_overlap_count(f1, f2) == 1  # Only '3' overlaps
    assert get_overlap_count(['1'], ['2']) == 0
    assert get_overlap_count([], []) == 0

def test_calculate_overlap_product():
    f1 = ['1', '2', '3', '3']  
    f2 = ['3', '3', '4', '5']  
    # Overlap key: '3', with counts 2 and 2 => 4
    assert calculate_overlap_product(f1, f2) == 4

    f1 = ['1', '1', '2', '2', '2']
    f2 = ['1', '2', '2', '3']
    # Overlap keys: 
    # '1' -> 2 *1 = 2, 
    # '2' -> 3 *2 = 6, 
    # ... total = 8
    assert calculate_overlap_product(f1, f2) == 8

    # No overlap
    assert calculate_overlap_product(['1'], ['2']) == 0

    # Empty lists
    assert calculate_overlap_product([], []) == 0

def test_functions_integration():
    # Simulate two files:
    file1_keys = ['12345678', '23456789', '34567890', '12345678']
    file2_keys = ['23456789', '12345678', '12345678', '45678901']

    # Key counts
    assert key_count(file1_keys, file2_keys) == (4, 4)

    # Distinct counts
    assert distinct_key_count(file1_keys, file2_keys) == (3, 3)

    # Overlap count (distinct keys)
    assert get_overlap_count(file1_keys, file2_keys) == 2  # '12345678' and '23456789'

    # Overlap product:
    # Counts in file1: '12345678' = 2, '23456789' = 1
    # Counts in file2: '12345678' = 2, '23456789' = 1
    # Product: (2*2) + (1*1) = 4 + 1 = 5
    assert calculate_overlap_product(file1_keys, file2_keys) == 5