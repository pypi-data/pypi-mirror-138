from itertools import permutations

import pytest

from ilp_keyboard_layout_optimization.ilp import KeyboardOptimization
from ilp_keyboard_layout_optimization.types import CharTuple


@pytest.fixture(scope="session")
def three_chars() -> CharTuple:
    return "a", "b", "c"


@pytest.fixture(scope="session")
def three_poss() -> CharTuple:
    return "left_pinky_home", "left_ring_home", "right_index_home"


# noinspection PyArgumentList
@pytest.mark.parametrize("init_params", ["something", None])
def test_keyboard_optimization_init_throw_errors(init_params):
    with pytest.raises(TypeError, match=r"__init__\(\) missing.*"):
        KeyboardOptimization(init_params)


def test_keyboard_optimization_init(three_chars, three_poss):
    KeyboardOptimization(three_chars, three_poss)


def test_keyboard_optimization_char_pos_assigns_keys(three_chars, three_poss):
    linear_keys = tuple(
        KeyboardOptimization(three_chars, three_poss).char_key_assigns_keys
    )
    assert len(linear_keys) == len(three_chars) * len(three_poss)
    for char in three_chars:
        for pos in three_poss:
            assert (char, pos) in linear_keys


def test_keyboard_optimization_quad_char_pos_assigns_keys(three_chars, three_poss):
    quadratic_keys = tuple(
        KeyboardOptimization(three_chars, three_poss).quad_char_key_assigns_keys
    )
    assert len(quadratic_keys) == len(three_chars) * (len(three_chars) - 1) * len(
        three_poss
    ) * (len(three_poss) - 1)
    for (char, char_2) in permutations(three_chars, 2):
        for (pos, pos_2) in permutations(three_poss, 2):
            assert (char, char_2, pos, pos_2) in quadratic_keys


def test_keyboard_optimization_quad_poss(three_chars, three_poss):
    quad_poss = tuple(KeyboardOptimization(three_chars, three_poss).key_pairs)
    assert len(quad_poss) == len(three_poss) * (len(three_poss) - 1)
    for pos in three_poss:
        for pos_2 in three_poss:
            if pos != pos_2:
                assert (pos, pos_2) in quad_poss
