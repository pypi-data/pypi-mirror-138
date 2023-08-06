from ilp_keyboard_layout_optimization.costs import FreqTuple
from ilp_keyboard_layout_optimization.type_aliases import (
    Bigram,
    Char,
    CharPosPair,
    CharPosQuadruple,
    CharTuple,
    Pos,
    PosPair,
    PosTuple,
    LinCosts,
    LinVars,
    QuadCosts,
    QuadVars,
)


def test_freq_tuple():

    assert FreqTuple == tuple[float, ...]


def test_char():
    assert Char == str


def test_key():
    assert Pos == str


def test_char_key_pair():
    assert CharPosPair == tuple[Char, Pos]


def test_bigram():
    assert Bigram == str


def test_pos_pair():
    assert PosPair == tuple[Pos, Pos]


def test_lin_costs():
    assert LinCosts == dict[CharPosPair, float]


def test_char_tuple():
    assert CharTuple == tuple[Char, ...]


def test_pos_tuple():
    assert PosTuple == tuple[Pos, ...]


def test_lin_vars():
    assert LinVars == dict[CharPosPair, bool]


def test_quad_pos_quadruple():
    assert CharPosQuadruple == tuple[Char, Pos, Char, Pos]


def test_quad_costs():
    assert QuadCosts == dict[CharPosQuadruple, float]


def test_quad_vars():
    assert QuadVars == dict[CharPosQuadruple, bool]
