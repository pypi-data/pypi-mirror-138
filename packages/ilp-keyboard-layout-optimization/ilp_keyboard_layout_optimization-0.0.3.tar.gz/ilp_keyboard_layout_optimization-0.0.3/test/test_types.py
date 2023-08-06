from collections import defaultdict
from enum import EnumMeta

from ilp_keyboard_layout_optimization.costs import FreqTuple
from ilp_keyboard_layout_optimization.type_aliases import (
    Bigram,
    Char,
    CharPosPair,
    CharPosQuadruple,
    CharTuple,
    Col,
    LinCosts,
    LinVars,
    Mod,
    Pos,
    PosPair,
    PosTuple,
    ProbDict,
    QuadCosts,
    QuadVars,
    Row,
    Side,
)


def test_freq_tuple():

    assert FreqTuple == tuple[float, ...]


def test_char():
    assert Char == str


def test_pos():
    assert issubclass(Pos, tuple)


def test_pos_row():
    assert "row" in Pos._fields


def test_pos_mod():
    assert "mod" in Pos._fields


def test_pos_side():
    assert "side" in Pos._fields


def test_pos_col():
    assert "col" in Pos._fields


def test_char_pos_pair():
    assert CharPosPair == tuple[Char, Pos]


def test_bigram():
    assert Bigram == str


def test_col():
    assert isinstance(Col, EnumMeta)


def test_col_outermost():
    assert Col.OUTERMOST


def test_col_pinky():
    assert Col.PINKY


def test_col_ring():
    assert Col.RING


def test_col_middle():
    assert Col.MIDDLE


def test_col_index():
    assert Col.INDEX


def test_col_innermost():
    assert Col.INNERMOST


def test_col_innermost_minus_index():
    assert Col.INNERMOST.value - Col.INDEX.value == 1


def test_col_innermost_minus_middle():
    assert Col.INNERMOST.value - Col.MIDDLE.value == 2


def test_col_innermost_minus_ring():
    assert Col.INNERMOST.value - Col.RING.value == 3


def test_col_innermost_minus_pinky():
    assert Col.INNERMOST.value - Col.PINKY.value == 4


def test_col_innermost_minus_outermost():
    assert Col.INNERMOST.value - Col.OUTERMOST.value == 5


def test_mod():
    assert isinstance(Mod, EnumMeta)


def test_mod_none():
    assert Mod.NONE


def test_mod_shift():
    assert Mod.SHIFT


def test_mod_upper():
    assert Mod.UPPER


def test_mod_lower():
    assert Mod.LOWER


def test_mod_nav():
    assert Mod.NAV


def test_mod_none_equals_zero():
    assert Mod.NONE.value == 0


def test_mod_nav_equals_two():
    assert Mod.NAV.value == 2


def test_row():
    assert isinstance(Row, EnumMeta)


def test_row_upper():
    assert Row.UPPER


def test_row_lower():
    assert Row.LOWER


def test_row_home():
    assert Row.HOME


def test_row_lower_minus_home():
    assert Row.LOWER.value - Row.HOME.value == 1


def test_row_lower_minus_home():
    assert Row.LOWER.value - Row.UPPER.value == 2


def test_side():
    assert isinstance(Side, EnumMeta)


def test_side_left():
    assert Side.LEFT


def test_side_right():
    assert Side.RIGHT


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
    assert CharPosQuadruple == tuple[Char, Char, Pos, Pos]


def test_quad_costs():
    assert QuadCosts == dict[CharPosQuadruple, float]


def test_quad_vars():
    assert QuadVars == dict[CharPosQuadruple, bool]


def test_prob_dict():
    assert ProbDict == defaultdict[Char | Bigram, float]
