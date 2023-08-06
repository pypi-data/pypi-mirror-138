from typing import Callable, Dict

import pytest
from hypothesis import given, strategies as hst
from hypothesis.strategies import composite

from ilp_keyboard_layout_optimization.data_aquisition.positions import Positions
from ilp_keyboard_layout_optimization.type_aliases import Char, Col, Mod, Pos, Row, Side
from ilp_keyboard_layout_optimization.visualize import make_layer_strs


@pytest.fixture(scope="session")
def positions():
    return Positions()


@pytest.fixture(scope="session")
def custom_positions():
    return Positions(
        (
            Pos(Side.LEFT, Mod.NONE, Col.PINKY, Row.HOME),
            Pos(Side.LEFT, Mod.NONE, Col.RING, Row.HOME),
            Pos(Side.LEFT, Mod.NONE, Col.MIDDLE, Row.HOME),
            Pos(Side.LEFT, Mod.NONE, Col.INDEX, Row.HOME),
            Pos(Side.RIGHT, Mod.NONE, Col.INDEX, Row.HOME),
            Pos(Side.RIGHT, Mod.NONE, Col.MIDDLE, Row.HOME),
            Pos(Side.RIGHT, Mod.NONE, Col.RING, Row.HOME),
            Pos(Side.RIGHT, Mod.NONE, Col.PINKY, Row.HOME),
        )
    )


@composite
def assigns(draw: Callable):
    assignments: Dict[Pos, Char] = {}
    default_positions: Positions = Positions()
    for pos in default_positions.poss:
        assignments[pos] = draw(hst.characters())
    return assignments


def test_class_positions_available():
    assert Positions


def test_init_custom_positions(custom_positions):
    assert custom_positions


def test_custom_positions_content(custom_positions):
    assert custom_positions.poss


def test_custom_positions_missing_outer_and_innermost_column(custom_positions):
    missing_poss = (
        Pos(side, mod, col, row)
        for side in Side
        for mod in Mod
        for col in (Col.INNERMOST, Col.OUTERMOST)
        for row in Row
    )
    for pos in missing_poss:
        assert pos not in custom_positions.poss


def test_custom_positions_missing_upper_and_lower_row(custom_positions):
    missing_poss = (
        Pos(side, mod, col, row)
        for side in Side
        for mod in Mod
        for col in Col
        for row in (Row.UPPER, Row.LOWER)
    )
    for pos in missing_poss:
        assert pos not in custom_positions.poss


def test_custom_positions_missing_inners_row_except_without_mods(custom_positions):
    missing_poss = (
        Pos(side, mod, col, Row.HOME)
        for side in Side
        for mod in (Mod.SHIFT, Mod.UPPER, Mod.LOWER, Mod.NAV)
        for col in (Col.INDEX, Col.MIDDLE, Col.RING, Col.PINKY)
    )
    for pos in missing_poss:
        assert pos not in custom_positions.poss


def test_custom_positions_present(custom_positions):
    poss = (
        Pos(side, Mod.NONE, col, Row.HOME)
        for side in Side
        for col in (Col.INDEX, Col.MIDDLE, Col.RING, Col.PINKY)
    )
    for pos in poss:
        assert pos in custom_positions.poss


def test_init_positions(positions):
    assert positions


def test_positions_content(positions):
    assert positions.poss


def test_positions_missing_left_outermost_column(positions):
    missing_poss = (
        Pos(Side.LEFT, mod, Col.OUTERMOST, row) for mod in Mod for row in Row
    )
    for pos in missing_poss:
        assert pos not in positions.poss


def test_positions_missing_lower_upper_row(positions):
    missing_poss = (
        Pos(side, Mod.LOWER, col, Row.UPPER) for side in Side for col in Col
    )
    for pos in missing_poss:
        assert pos not in positions.poss


def test_positions_missing_right_outermost_lower_key(positions):
    missing_poss = (Pos(Side.RIGHT, mod, Col.OUTERMOST, Row.LOWER) for mod in Mod)
    for pos in missing_poss:
        assert pos not in positions.poss


def test_positions_missing_right_outermost_upper_key(positions):
    missing_poss = (
        Pos(Side.RIGHT, mod, Col.OUTERMOST, Row.UPPER)
        for mod in (Mod.SHIFT, Mod.UPPER, Mod.NONE)
    )
    for pos in missing_poss:
        assert pos not in positions.poss


def test_positions_missing_right_outermost_home_key(positions):
    missing_poss = (
        Pos(Side.RIGHT, mod, Col.OUTERMOST, Row.HOME) for mod in (Mod.NAV, Mod.UPPER)
    )
    for pos in missing_poss:
        assert pos not in positions.poss


def test_positions_inners(positions):
    poss = (
        Pos(side, mod, col, row)
        for side in Side
        for mod in Mod
        for col in (Col.PINKY, Col.RING, Col.MIDDLE, Col.INDEX, Col.INNERMOST)
        for row in (Row.HOME, Row.LOWER)
    )
    for pos in poss:
        assert pos in positions.poss


def test_positions_uppers(positions):
    poss = (
        Pos(side, mod, col, Row.UPPER)
        for side in Side
        for mod in (Mod.NONE, Mod.SHIFT, Mod.UPPER, Mod.NAV)
        for col in (Col.PINKY, Col.RING, Col.MIDDLE, Col.INDEX, Col.INNERMOST)
    )
    for pos in poss:
        assert pos in positions.poss


def test_positions_right_outermost_home_key(positions):
    poss = (
        Pos(Side.RIGHT, mod, Col.OUTERMOST, Row.HOME)
        for mod in (Mod.NONE, Mod.SHIFT, Mod.LOWER)
    )
    for pos in poss:
        assert pos in positions.poss


@given(assigns())
def test_positions_with_visualization(assignments):
    layout = make_layer_strs(assignments)
    assert layout
    assert (
        "UNMODIFIED:\n    "
        f"-------------------------------------     "
        f"-------------------------------------\n    "
        f"|  ⇥  "
        f"|  {assignments[Side.LEFT, Mod.NONE, Col.PINKY, Row.UPPER]}  "
        f"|  {assignments[Side.LEFT, Mod.NONE, Col.RING, Row.UPPER]}  "
        f"|  {assignments[Side.LEFT, Mod.NONE, Col.MIDDLE, Row.UPPER]}  "
        f"|  {assignments[Side.LEFT, Mod.NONE, Col.INDEX, Row.UPPER]}  "
        f"|  {assignments[Side.LEFT, Mod.NONE, Col.INNERMOST, Row.UPPER]}  "
        f"|     "
        f"|  {assignments[Side.RIGHT, Mod.NONE, Col.INNERMOST, Row.UPPER]}  "
        f"|  {assignments[Side.RIGHT, Mod.NONE, Col.INDEX, Row.UPPER]}  "
        f"|  {assignments[Side.RIGHT, Mod.NONE, Col.MIDDLE, Row.UPPER]}  "
        f"|  {assignments[Side.RIGHT, Mod.NONE, Col.RING, Row.UPPER]}  "
        f"|  {assignments[Side.RIGHT, Mod.NONE, Col.PINKY, Row.UPPER]}  "
        f"|  ←  |\n    "
        f"-------------------------------------     "
        f"-------------------------------------\n    "
        f"|  ⎈  "
        f""
        f"|  {assignments[Side.LEFT, Mod.NONE, Col.PINKY, Row.HOME]}  "
        f"|  {assignments[Side.LEFT, Mod.NONE, Col.RING, Row.HOME]}  "
        f"|  {assignments[Side.LEFT, Mod.NONE, Col.MIDDLE, Row.HOME]}  "
        f"|  {assignments[Side.LEFT, Mod.NONE, Col.INDEX, Row.HOME]}  "
        f"|  {assignments[Side.LEFT, Mod.NONE, Col.INNERMOST, Row.HOME]}  "
        f"|     "
        f"|  {assignments[Side.RIGHT, Mod.NONE, Col.INNERMOST, Row.HOME]}  "
        f"|  {assignments[Side.RIGHT, Mod.NONE, Col.INDEX, Row.HOME]}  "
        f"|  {assignments[Side.RIGHT, Mod.NONE, Col.MIDDLE, Row.HOME]}  "
        f"|  {assignments[Side.RIGHT, Mod.NONE, Col.RING, Row.HOME]}  "
        f"|  {assignments[Side.RIGHT, Mod.NONE, Col.PINKY, Row.HOME]}  "
        f""
        f"|  {assignments[Side.RIGHT, Mod.NONE, Col.OUTERMOST, Row.HOME]}  |\n    "
        f"-------------------------------------     "
        f"-------------------------------------\n    "
        f"|  ⇧  "
        f"|  {assignments[Side.LEFT, Mod.NONE, Col.PINKY, Row.LOWER]}  "
        f"|  {assignments[Side.LEFT, Mod.NONE, Col.RING, Row.LOWER]}  "
        f"|  {assignments[Side.LEFT, Mod.NONE, Col.MIDDLE, Row.LOWER]}  "
        f"|  {assignments[Side.LEFT, Mod.NONE, Col.INDEX, Row.LOWER]}  "
        f"|  {assignments[Side.LEFT, Mod.NONE, Col.INNERMOST, Row.LOWER]}  "
        f"|     "
        f"|  {assignments[Side.RIGHT, Mod.NONE, Col.INNERMOST, Row.LOWER]}  "
        f"|  {assignments[Side.RIGHT, Mod.NONE, Col.INDEX, Row.LOWER]}  "
        f"|  {assignments[Side.RIGHT, Mod.NONE, Col.MIDDLE, Row.LOWER]}  "
        f"|  {assignments[Side.RIGHT, Mod.NONE, Col.RING, Row.LOWER]}  "
        f"|  {assignments[Side.RIGHT, Mod.NONE, Col.PINKY, Row.LOWER]}  "
        "|  ⇧  |\n    "
        f"-------------------------------------     "
        f"-------------------------------------\n    \n    "
        "SHIFT:\n    "
        f"-------------------------------------     "
        f"-------------------------------------\n    "
        f"|  ⇥  "
        f"|  {assignments[Side.LEFT, Mod.SHIFT, Col.PINKY, Row.UPPER]}  "
        f"|  {assignments[Side.LEFT, Mod.SHIFT, Col.RING, Row.UPPER]}  "
        f"|  {assignments[Side.LEFT, Mod.SHIFT, Col.MIDDLE, Row.UPPER]}  "
        f"|  {assignments[Side.LEFT, Mod.SHIFT, Col.INDEX, Row.UPPER]}  "
        f"|  {assignments[Side.LEFT, Mod.SHIFT, Col.INNERMOST, Row.UPPER]}  "
        f"|     "
        f"|  {assignments[Side.RIGHT, Mod.SHIFT, Col.INNERMOST, Row.UPPER]}  "
        f"|  {assignments[Side.RIGHT, Mod.SHIFT, Col.INDEX, Row.UPPER]}  "
        f"|  {assignments[Side.RIGHT, Mod.SHIFT, Col.MIDDLE, Row.UPPER]}  "
        f"|  {assignments[Side.RIGHT, Mod.SHIFT, Col.RING, Row.UPPER]}  "
        f"|  {assignments[Side.RIGHT, Mod.SHIFT, Col.PINKY, Row.UPPER]}  "
        f"|  ←  |\n    "
        f"-------------------------------------     "
        f"-------------------------------------\n    "
        f"|  ⎈  "
        f"|  {assignments[Side.LEFT, Mod.SHIFT, Col.PINKY, Row.HOME]}  "
        f"|  {assignments[Side.LEFT, Mod.SHIFT, Col.RING, Row.HOME]}  "
        f"|  {assignments[Side.LEFT, Mod.SHIFT, Col.MIDDLE, Row.HOME]}  "
        f"|  {assignments[Side.LEFT, Mod.SHIFT, Col.INDEX, Row.HOME]}  "
        f"|  {assignments[Side.LEFT, Mod.SHIFT, Col.INNERMOST, Row.HOME]}  "
        f"|     "
        f"|  {assignments[Side.RIGHT, Mod.SHIFT, Col.INNERMOST, Row.HOME]}  "
        f"|  {assignments[Side.RIGHT, Mod.SHIFT, Col.INDEX, Row.HOME]}  "
        f"|  {assignments[Side.RIGHT, Mod.SHIFT, Col.MIDDLE, Row.HOME]}  "
        f"|  {assignments[Side.RIGHT, Mod.SHIFT, Col.RING, Row.HOME]}  "
        f"|  {assignments[Side.RIGHT, Mod.SHIFT, Col.PINKY, Row.HOME]}  "
        f""
        f"|  {assignments[Side.RIGHT, Mod.SHIFT, Col.OUTERMOST, Row.HOME]}  |\n    "
        f"-------------------------------------     "
        f"-------------------------------------\n    "
        f"|  ⇧  "
        f"|  {assignments[Side.LEFT, Mod.SHIFT, Col.PINKY, Row.LOWER]}  "
        f"|  {assignments[Side.LEFT, Mod.SHIFT, Col.RING, Row.LOWER]}  "
        f"|  {assignments[Side.LEFT, Mod.SHIFT, Col.MIDDLE, Row.LOWER]}  "
        f"|  {assignments[Side.LEFT, Mod.SHIFT, Col.INDEX, Row.LOWER]}  "
        f"|  {assignments[Side.LEFT, Mod.SHIFT, Col.INNERMOST, Row.LOWER]}  "
        f"|     "
        f"|  {assignments[Side.RIGHT, Mod.SHIFT, Col.INNERMOST, Row.LOWER]}  "
        f"|  {assignments[Side.RIGHT, Mod.SHIFT, Col.INDEX, Row.LOWER]}  "
        f"|  {assignments[Side.RIGHT, Mod.SHIFT, Col.MIDDLE, Row.LOWER]}  "
        f"|  {assignments[Side.RIGHT, Mod.SHIFT, Col.RING, Row.LOWER]}  "
        f"|  {assignments[Side.RIGHT, Mod.SHIFT, Col.PINKY, Row.LOWER]}  "
        "|  ⇧  |\n    "
        f"-------------------------------------     "
        f"-------------------------------------\n    \n    "
        "LOWER:\n    "
        f"-------------------------------------     "
        f"-------------------------------------\n    "
        "| F1  | F2  | F3  | F4  | F5  | F6  |     | F7  | F8  | F9  | F10 | F11 "
        "| F12 |\n    "
        f"-------------------------------------     "
        f"-------------------------------------\n    "
        f"|  ⇕  "
        f"|  {assignments[Side.LEFT, Mod.LOWER, Col.PINKY, Row.HOME]}  "
        f"|  {assignments[Side.LEFT, Mod.LOWER, Col.RING, Row.HOME]}  "
        f"|  {assignments[Side.LEFT, Mod.LOWER, Col.MIDDLE, Row.HOME]}  "
        f"|  {assignments[Side.LEFT, Mod.LOWER, Col.INDEX, Row.HOME]}  "
        f"|  {assignments[Side.LEFT, Mod.LOWER, Col.INNERMOST, Row.HOME]}  "
        f"|     "
        f"|  {assignments[Side.RIGHT, Mod.LOWER, Col.INNERMOST, Row.HOME]}  "
        f"|  {assignments[Side.RIGHT, Mod.LOWER, Col.INDEX, Row.HOME]}  "
        f"|  {assignments[Side.RIGHT, Mod.LOWER, Col.MIDDLE, Row.HOME]}  "
        f"|  {assignments[Side.RIGHT, Mod.LOWER, Col.RING, Row.HOME]}  "
        f"|  {assignments[Side.RIGHT, Mod.LOWER, Col.PINKY, Row.HOME]}  "
        f""
        f"|  {assignments[Side.RIGHT, Mod.LOWER, Col.OUTERMOST, Row.HOME]}  |\n    "
        f"-------------------------------------     "
        f"-------------------------------------\n    "
        f"|  ⎇  "
        f"|  {assignments[Side.LEFT, Mod.LOWER, Col.PINKY, Row.LOWER]}  "
        f"|  {assignments[Side.LEFT, Mod.LOWER, Col.RING, Row.LOWER]}  "
        f"|  {assignments[Side.LEFT, Mod.LOWER, Col.MIDDLE, Row.LOWER]}  "
        f"|  {assignments[Side.LEFT, Mod.LOWER, Col.INDEX, Row.LOWER]}  "
        f"|  {assignments[Side.LEFT, Mod.LOWER, Col.INNERMOST, Row.LOWER]}  "
        f"|     "
        f"|  {assignments[Side.RIGHT, Mod.LOWER, Col.INNERMOST, Row.LOWER]}  "
        f"|  {assignments[Side.RIGHT, Mod.LOWER, Col.INDEX, Row.LOWER]}  "
        f"|  {assignments[Side.RIGHT, Mod.LOWER, Col.MIDDLE, Row.LOWER]}  "
        f"|  {assignments[Side.RIGHT, Mod.LOWER, Col.RING, Row.LOWER]}  "
        f"|  {assignments[Side.RIGHT, Mod.LOWER, Col.PINKY, Row.LOWER]}  "
        "|AltGr|\n    "
        f"-------------------------------------     "
        f"-------------------------------------\n    \n    "
        "UPPER:\n    "
        f"-------------------------------------     "
        f"-------------------------------------\n    "
        f"|  ⇥  "
        f"|  {assignments[Side.LEFT, Mod.UPPER, Col.PINKY, Row.UPPER]}  "
        f"|  {assignments[Side.LEFT, Mod.UPPER, Col.RING, Row.UPPER]}  "
        f"|  {assignments[Side.LEFT, Mod.UPPER, Col.MIDDLE, Row.UPPER]}  "
        f"|  {assignments[Side.LEFT, Mod.UPPER, Col.INDEX, Row.UPPER]}  "
        f"|  {assignments[Side.LEFT, Mod.UPPER, Col.INNERMOST, Row.UPPER]}  "
        f"|     "
        f"|  {assignments[Side.RIGHT, Mod.UPPER, Col.INNERMOST, Row.UPPER]}  "
        f"|  {assignments[Side.RIGHT, Mod.UPPER, Col.INDEX, Row.UPPER]}  "
        f"|  {assignments[Side.RIGHT, Mod.UPPER, Col.MIDDLE, Row.UPPER]}  "
        f"|  {assignments[Side.RIGHT, Mod.UPPER, Col.RING, Row.UPPER]}  "
        f"|  {assignments[Side.RIGHT, Mod.UPPER, Col.PINKY, Row.UPPER]}  "
        f"|  ⌦  |\n    "
        f"-------------------------------------     "
        f"-------------------------------------\n    "
        f"|  ⎈  "
        f"|  {assignments[Side.LEFT, Mod.UPPER, Col.PINKY, Row.HOME]}  "
        f"|  {assignments[Side.LEFT, Mod.UPPER, Col.RING, Row.HOME]}  "
        f"|  {assignments[Side.LEFT, Mod.UPPER, Col.MIDDLE, Row.HOME]}  "
        f"|  {assignments[Side.LEFT, Mod.UPPER, Col.INDEX, Row.HOME]}  "
        f"|  {assignments[Side.LEFT, Mod.UPPER, Col.INNERMOST, Row.HOME]}  "
        f"|     "
        f"|  {assignments[Side.RIGHT, Mod.UPPER, Col.INNERMOST, Row.HOME]}  "
        f"|  {assignments[Side.RIGHT, Mod.UPPER, Col.INDEX, Row.HOME]}  "
        f"|  {assignments[Side.RIGHT, Mod.UPPER, Col.MIDDLE, Row.HOME]}  "
        f"|  {assignments[Side.RIGHT, Mod.UPPER, Col.RING, Row.HOME]}  "
        f"|  {assignments[Side.RIGHT, Mod.UPPER, Col.PINKY, Row.HOME]}  "
        f"|  ⇕  |\n    "
        f"-------------------------------------     "
        f"-------------------------------------\n    "
        f"|  ⇧  "
        f"|  {assignments[Side.LEFT, Mod.UPPER, Col.PINKY, Row.LOWER]}  "
        f"|  {assignments[Side.LEFT, Mod.UPPER, Col.RING, Row.LOWER]}  "
        f"|  {assignments[Side.LEFT, Mod.UPPER, Col.MIDDLE, Row.LOWER]}  "
        f"|  {assignments[Side.LEFT, Mod.UPPER, Col.INDEX, Row.LOWER]}  "
        f"|  {assignments[Side.LEFT, Mod.UPPER, Col.INNERMOST, Row.LOWER]}  "
        f"|     "
        f"|  {assignments[Side.RIGHT, Mod.UPPER, Col.INNERMOST, Row.LOWER]}  "
        f"|  {assignments[Side.RIGHT, Mod.UPPER, Col.INDEX, Row.LOWER]}  "
        f"|  {assignments[Side.RIGHT, Mod.UPPER, Col.MIDDLE, Row.LOWER]}  "
        f"|  {assignments[Side.RIGHT, Mod.UPPER, Col.RING, Row.LOWER]}  "
        f"|  {assignments[Side.RIGHT, Mod.UPPER, Col.PINKY, Row.LOWER]}  "
        "|AltGr|\n    "
        f"-------------------------------------     "
        f"-------------------------------------\n    \n    "
        "NAV:\n    "
        f"-------------------------------------     "
        f"-------------------------------------\n    "
        f"|  ⇥  "
        f"|  {assignments[Side.LEFT, Mod.NAV, Col.PINKY, Row.UPPER]}  "
        f"|  {assignments[Side.LEFT, Mod.NAV, Col.RING, Row.UPPER]}  "
        f"|  {assignments[Side.LEFT, Mod.NAV, Col.MIDDLE, Row.UPPER]}  "
        f"|  {assignments[Side.LEFT, Mod.NAV, Col.INDEX, Row.UPPER]}  "
        f""
        f"|  {assignments[Side.LEFT, Mod.NAV, Col.INNERMOST, Row.UPPER]}  |     "
        f"|  {assignments[Side.RIGHT, Mod.NAV, Col.INNERMOST, Row.UPPER]}  "
        f"|  {assignments[Side.RIGHT, Mod.NAV, Col.INDEX, Row.UPPER]}  "
        f"|  {assignments[Side.RIGHT, Mod.NAV, Col.MIDDLE, Row.UPPER]}  "
        f""
        f"|  {assignments[Side.RIGHT, Mod.NAV, Col.RING, Row.UPPER]}  "
        f"|  {assignments[Side.RIGHT, Mod.NAV, Col.PINKY, Row.UPPER]}  |  ←  |\n    "
        f"-------------------------------------     "
        f"-------------------------------------\n    "
        f"|     "
        f"|  {assignments[Side.LEFT, Mod.NAV, Col.PINKY, Row.HOME]}  "
        f"|  {assignments[Side.LEFT, Mod.NAV, Col.RING, Row.HOME]}  "
        f"|  {assignments[Side.LEFT, Mod.NAV, Col.MIDDLE, Row.HOME]}  "
        f"|  {assignments[Side.LEFT, Mod.NAV, Col.INDEX, Row.HOME]}  "
        f"|  {assignments[Side.LEFT, Mod.NAV, Col.INNERMOST, Row.HOME]}  "
        f"|     "
        f"|  {assignments[Side.RIGHT, Mod.NAV, Col.INNERMOST, Row.HOME]}  "
        f"|  {assignments[Side.RIGHT, Mod.NAV, Col.INDEX, Row.HOME]}  "
        f"|  {assignments[Side.RIGHT, Mod.NAV, Col.MIDDLE, Row.HOME]}  "
        f"|  {assignments[Side.RIGHT, Mod.NAV, Col.RING, Row.HOME]}  "
        f"|  {assignments[Side.RIGHT, Mod.NAV, Col.PINKY, Row.HOME]}  "
        f"|     |\n    "
        f"-------------------------------------     "
        f"-------------------------------------\n    "
        f"|  ⇧  "
        f"|  {assignments[Side.LEFT, Mod.NAV, Col.PINKY, Row.LOWER]}  "
        f"|  {assignments[Side.LEFT, Mod.NAV, Col.RING, Row.LOWER]}  "
        f"|  {assignments[Side.LEFT, Mod.NAV, Col.MIDDLE, Row.LOWER]}  "
        f"|  {assignments[Side.LEFT, Mod.NAV, Col.INDEX, Row.LOWER]}  "
        f"|  {assignments[Side.LEFT, Mod.NAV, Col.INNERMOST, Row.LOWER]}  "
        f"|     "
        f"|  {assignments[Side.RIGHT, Mod.NAV, Col.INNERMOST, Row.LOWER]}  "
        f"|  {assignments[Side.RIGHT, Mod.NAV, Col.INDEX, Row.LOWER]}  "
        f"|  {assignments[Side.RIGHT, Mod.NAV, Col.MIDDLE, Row.LOWER]}  "
        f"|  {assignments[Side.RIGHT, Mod.NAV, Col.RING, Row.LOWER]}  "
        f"|  {assignments[Side.RIGHT, Mod.NAV, Col.PINKY, Row.LOWER]}  "
        "|  ⇧  |\n    "
        f"-------------------------------------     "
        f"-------------------------------------"
    ) in layout
