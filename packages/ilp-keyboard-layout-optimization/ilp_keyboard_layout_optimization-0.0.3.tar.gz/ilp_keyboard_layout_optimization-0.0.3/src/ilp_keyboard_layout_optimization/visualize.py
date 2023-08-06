from typing import Dict

from ilp_keyboard_layout_optimization.type_aliases import (
    Char,
    Col,
    Mod,
    Pos,
    PosTuple,
    Row,
    Side,
)


def make_layer_strs(poss: Dict[PosTuple, Char]):
    """Create UNICODE string of the different layers"""
    home_str = """
    UNMODIFIED:
    -------------------------------------     -------------------------------------
    |  ⇥  |  {}  |  {}  |  {}  |  {}  |  {}  |     |  {}  |  {}  |  {}  |  {}  |  {}  |  ←  |
    -------------------------------------     -------------------------------------
    |  ⎈  |  {}  |  {}  |  {}  |  {}  |  {}  |     |  {}  |  {}  |  {}  |  {}  |  {}  |  {}  |
    -------------------------------------     -------------------------------------
    |  ⇧  |  {}  |  {}  |  {}  |  {}  |  {}  |     |  {}  |  {}  |  {}  |  {}  |  {}  |  ⇧  |
    -------------------------------------     -------------------------------------
    """
    shifted_str = """
    SHIFT:
    -------------------------------------     -------------------------------------
    |  ⇥  |  {}  |  {}  |  {}  |  {}  |  {}  |     |  {}  |  {}  |  {}  |  {}  |  {}  |  ←  |
    -------------------------------------     -------------------------------------
    |  ⎈  |  {}  |  {}  |  {}  |  {}  |  {}  |     |  {}  |  {}  |  {}  |  {}  |  {}  |  {}  |
    -------------------------------------     -------------------------------------
    |  ⇧  |  {}  |  {}  |  {}  |  {}  |  {}  |     |  {}  |  {}  |  {}  |  {}  |  {}  |  ⇧  |
    -------------------------------------     -------------------------------------
    """
    lowered_str = """
    LOWER:
    -------------------------------------     -------------------------------------
    | F1  | F2  | F3  | F4  | F5  | F6  |     | F7  | F8  | F9  | F10 | F11 | F12 |
    -------------------------------------     -------------------------------------
    |  ⇕  |  {}  |  {}  |  {}  |  {}  |  {}  |     |  {}  |  {}  |  {}  |  {}  |  {}  |  {}  |
    -------------------------------------     -------------------------------------
    |  ⎇  |  {}  |  {}  |  {}  |  {}  |  {}  |     |  {}  |  {}  |  {}  |  {}  |  {}  |AltGr|
    -------------------------------------     -------------------------------------
    """
    raised_str = """
    UPPER:
    -------------------------------------     -------------------------------------
    |  ⇥  |  {}  |  {}  |  {}  |  {}  |  {}  |     |  {}  |  {}  |  {}  |  {}  |  {}  |  ⌦  |
    -------------------------------------     -------------------------------------
    |  ⎈  |  {}  |  {}  |  {}  |  {}  |  {}  |     |  {}  |  {}  |  {}  |  {}  |  {}  |  ⇕  |
    -------------------------------------     -------------------------------------
    |  ⇧  |  {}  |  {}  |  {}  |  {}  |  {}  |     |  {}  |  {}  |  {}  |  {}  |  {}  |AltGr|
    -------------------------------------     -------------------------------------
    """
    nav_str = """
    NAV:
    -------------------------------------     -------------------------------------
    |  ⇥  |  {}  |  {}  |  {}  |  {}  |  {}  |     |  {}  |  {}  |  {}  |  {}  |  {}  |  ←  |
    -------------------------------------     -------------------------------------
    |     |  {}  |  {}  |  {}  |  {}  |  {}  |     |  {}  |  {}  |  {}  |  {}  |  {}  |     |
    -------------------------------------     -------------------------------------
    |  ⇧  |  {}  |  {}  |  {}  |  {}  |  {}  |     |  {}  |  {}  |  {}  |  {}  |  {}  |  ⇧  |
    -------------------------------------     -------------------------------------
    """
    return (
        home_str.format(
            poss.get((Side.LEFT, Mod.NONE, Col.PINKY, Row.UPPER), " "),
            poss.get((Side.LEFT, Mod.NONE, Col.RING, Row.UPPER), " "),
            poss.get((Side.LEFT, Mod.NONE, Col.MIDDLE, Row.UPPER), " "),
            poss.get((Side.LEFT, Mod.NONE, Col.INDEX, Row.UPPER), " "),
            poss.get((Side.LEFT, Mod.NONE, Col.INNERMOST, Row.UPPER), " "),
            poss.get((Side.RIGHT, Mod.NONE, Col.INNERMOST, Row.UPPER), " "),
            poss.get((Side.RIGHT, Mod.NONE, Col.INDEX, Row.UPPER), " "),
            poss.get((Side.RIGHT, Mod.NONE, Col.MIDDLE, Row.UPPER), " "),
            poss.get((Side.RIGHT, Mod.NONE, Col.RING, Row.UPPER), " "),
            poss.get((Side.RIGHT, Mod.NONE, Col.PINKY, Row.UPPER), " "),
            poss.get((Side.LEFT, Mod.NONE, Col.PINKY, Row.HOME), " "),
            poss.get((Side.LEFT, Mod.NONE, Col.RING, Row.HOME), " "),
            poss.get((Side.LEFT, Mod.NONE, Col.MIDDLE, Row.HOME), " "),
            poss.get((Side.LEFT, Mod.NONE, Col.INDEX, Row.HOME), " "),
            poss.get((Side.LEFT, Mod.NONE, Col.INNERMOST, Row.HOME), " "),
            poss.get((Side.RIGHT, Mod.NONE, Col.INNERMOST, Row.HOME), " "),
            poss.get((Side.RIGHT, Mod.NONE, Col.INDEX, Row.HOME), " "),
            poss.get((Side.RIGHT, Mod.NONE, Col.MIDDLE, Row.HOME), " "),
            poss.get((Side.RIGHT, Mod.NONE, Col.RING, Row.HOME), " "),
            poss.get((Side.RIGHT, Mod.NONE, Col.PINKY, Row.HOME), " "),
            poss.get((Side.RIGHT, Mod.NONE, Col.OUTERMOST, Row.HOME), " "),
            poss.get((Side.LEFT, Mod.NONE, Col.PINKY, Row.LOWER), " "),
            poss.get((Side.LEFT, Mod.NONE, Col.RING, Row.LOWER), " "),
            poss.get((Side.LEFT, Mod.NONE, Col.MIDDLE, Row.LOWER), " "),
            poss.get((Side.LEFT, Mod.NONE, Col.INDEX, Row.LOWER), " "),
            poss.get((Side.LEFT, Mod.NONE, Col.INNERMOST, Row.LOWER), " "),
            poss.get((Side.RIGHT, Mod.NONE, Col.INNERMOST, Row.LOWER), " "),
            poss.get((Side.RIGHT, Mod.NONE, Col.INDEX, Row.LOWER), " "),
            poss.get((Side.RIGHT, Mod.NONE, Col.MIDDLE, Row.LOWER), " "),
            poss.get((Side.RIGHT, Mod.NONE, Col.RING, Row.LOWER), " "),
            poss.get((Side.RIGHT, Mod.NONE, Col.PINKY, Row.LOWER), " "),
        )
        + shifted_str.format(
            poss.get((Side.LEFT, Mod.SHIFT, Col.PINKY, Row.UPPER), " "),
            poss.get((Side.LEFT, Mod.SHIFT, Col.RING, Row.UPPER), " "),
            poss.get((Side.LEFT, Mod.SHIFT, Col.MIDDLE, Row.UPPER), " "),
            poss.get((Side.LEFT, Mod.SHIFT, Col.INDEX, Row.UPPER), " "),
            poss.get((Side.LEFT, Mod.SHIFT, Col.INNERMOST, Row.UPPER), " "),
            poss.get((Side.RIGHT, Mod.SHIFT, Col.INNERMOST, Row.UPPER), " "),
            poss.get((Side.RIGHT, Mod.SHIFT, Col.INDEX, Row.UPPER), " "),
            poss.get((Side.RIGHT, Mod.SHIFT, Col.MIDDLE, Row.UPPER), " "),
            poss.get((Side.RIGHT, Mod.SHIFT, Col.RING, Row.UPPER), " "),
            poss.get((Side.RIGHT, Mod.SHIFT, Col.PINKY, Row.UPPER), " "),
            poss.get((Side.LEFT, Mod.SHIFT, Col.PINKY, Row.HOME), " "),
            poss.get((Side.LEFT, Mod.SHIFT, Col.RING, Row.HOME), " "),
            poss.get((Side.LEFT, Mod.SHIFT, Col.MIDDLE, Row.HOME), " "),
            poss.get((Side.LEFT, Mod.SHIFT, Col.INDEX, Row.HOME), " "),
            poss.get((Side.LEFT, Mod.SHIFT, Col.INNERMOST, Row.HOME), " "),
            poss.get((Side.RIGHT, Mod.SHIFT, Col.INNERMOST, Row.HOME), " "),
            poss.get((Side.RIGHT, Mod.SHIFT, Col.INDEX, Row.HOME), " "),
            poss.get((Side.RIGHT, Mod.SHIFT, Col.MIDDLE, Row.HOME), " "),
            poss.get((Side.RIGHT, Mod.SHIFT, Col.RING, Row.HOME), " "),
            poss.get((Side.RIGHT, Mod.SHIFT, Col.PINKY, Row.HOME), " "),
            poss.get((Side.RIGHT, Mod.SHIFT, Col.OUTERMOST, Row.HOME), " "),
            poss.get((Side.LEFT, Mod.SHIFT, Col.PINKY, Row.LOWER), " "),
            poss.get((Side.LEFT, Mod.SHIFT, Col.RING, Row.LOWER), " "),
            poss.get((Side.LEFT, Mod.SHIFT, Col.MIDDLE, Row.LOWER), " "),
            poss.get((Side.LEFT, Mod.SHIFT, Col.INDEX, Row.LOWER), " "),
            poss.get((Side.LEFT, Mod.SHIFT, Col.INNERMOST, Row.LOWER), " "),
            poss.get((Side.RIGHT, Mod.SHIFT, Col.INNERMOST, Row.LOWER), " "),
            poss.get((Side.RIGHT, Mod.SHIFT, Col.INDEX, Row.LOWER), " "),
            poss.get((Side.RIGHT, Mod.SHIFT, Col.MIDDLE, Row.LOWER), " "),
            poss.get((Side.RIGHT, Mod.SHIFT, Col.RING, Row.LOWER), " "),
            poss.get((Side.RIGHT, Mod.SHIFT, Col.PINKY, Row.LOWER), " "),
        )
        + lowered_str.format(
            poss.get((Side.LEFT, Mod.LOWER, Col.PINKY, Row.HOME), " "),
            poss.get((Side.LEFT, Mod.LOWER, Col.RING, Row.HOME), " "),
            poss.get((Side.LEFT, Mod.LOWER, Col.MIDDLE, Row.HOME), " "),
            poss.get((Side.LEFT, Mod.LOWER, Col.INDEX, Row.HOME), " "),
            poss.get((Side.LEFT, Mod.LOWER, Col.INNERMOST, Row.HOME), " "),
            poss.get((Side.RIGHT, Mod.LOWER, Col.INNERMOST, Row.HOME), " "),
            poss.get((Side.RIGHT, Mod.LOWER, Col.INDEX, Row.HOME), " "),
            poss.get((Side.RIGHT, Mod.LOWER, Col.MIDDLE, Row.HOME), " "),
            poss.get((Side.RIGHT, Mod.LOWER, Col.RING, Row.HOME), " "),
            poss.get((Side.RIGHT, Mod.LOWER, Col.PINKY, Row.HOME), " "),
            poss.get((Side.RIGHT, Mod.LOWER, Col.OUTERMOST, Row.HOME), " "),
            poss.get((Side.LEFT, Mod.LOWER, Col.PINKY, Row.LOWER), " "),
            poss.get((Side.LEFT, Mod.LOWER, Col.RING, Row.LOWER), " "),
            poss.get((Side.LEFT, Mod.LOWER, Col.MIDDLE, Row.LOWER), " "),
            poss.get((Side.LEFT, Mod.LOWER, Col.INDEX, Row.LOWER), " "),
            poss.get((Side.LEFT, Mod.LOWER, Col.INNERMOST, Row.LOWER), " "),
            poss.get((Side.RIGHT, Mod.LOWER, Col.INNERMOST, Row.LOWER), " "),
            poss.get((Side.RIGHT, Mod.LOWER, Col.INDEX, Row.LOWER), " "),
            poss.get((Side.RIGHT, Mod.LOWER, Col.MIDDLE, Row.LOWER), " "),
            poss.get((Side.RIGHT, Mod.LOWER, Col.RING, Row.LOWER), " "),
            poss.get((Side.RIGHT, Mod.LOWER, Col.PINKY, Row.LOWER), " "),
        )
        + raised_str.format(
            poss.get((Side.LEFT, Mod.UPPER, Col.PINKY, Row.UPPER), " "),
            poss.get((Side.LEFT, Mod.UPPER, Col.RING, Row.UPPER), " "),
            poss.get((Side.LEFT, Mod.UPPER, Col.MIDDLE, Row.UPPER), " "),
            poss.get((Side.LEFT, Mod.UPPER, Col.INDEX, Row.UPPER), " "),
            poss.get((Side.LEFT, Mod.UPPER, Col.INNERMOST, Row.UPPER), " "),
            poss.get((Side.RIGHT, Mod.UPPER, Col.INNERMOST, Row.UPPER), " "),
            poss.get((Side.RIGHT, Mod.UPPER, Col.INDEX, Row.UPPER), " "),
            poss.get((Side.RIGHT, Mod.UPPER, Col.MIDDLE, Row.UPPER), " "),
            poss.get((Side.RIGHT, Mod.UPPER, Col.RING, Row.UPPER), " "),
            poss.get((Side.RIGHT, Mod.UPPER, Col.PINKY, Row.UPPER), " "),
            poss.get((Side.LEFT, Mod.UPPER, Col.PINKY, Row.HOME), " "),
            poss.get((Side.LEFT, Mod.UPPER, Col.RING, Row.HOME), " "),
            poss.get((Side.LEFT, Mod.UPPER, Col.MIDDLE, Row.HOME), " "),
            poss.get((Side.LEFT, Mod.UPPER, Col.INDEX, Row.HOME), " "),
            poss.get((Side.LEFT, Mod.UPPER, Col.INNERMOST, Row.HOME), " "),
            poss.get((Side.RIGHT, Mod.UPPER, Col.INNERMOST, Row.HOME), " "),
            poss.get((Side.RIGHT, Mod.UPPER, Col.INDEX, Row.HOME), " "),
            poss.get((Side.RIGHT, Mod.UPPER, Col.MIDDLE, Row.HOME), " "),
            poss.get((Side.RIGHT, Mod.UPPER, Col.RING, Row.HOME), " "),
            poss.get((Side.RIGHT, Mod.UPPER, Col.PINKY, Row.HOME), " "),
            poss.get((Side.LEFT, Mod.UPPER, Col.PINKY, Row.LOWER), " "),
            poss.get((Side.LEFT, Mod.UPPER, Col.RING, Row.LOWER), " "),
            poss.get((Side.LEFT, Mod.UPPER, Col.MIDDLE, Row.LOWER), " "),
            poss.get((Side.LEFT, Mod.UPPER, Col.INDEX, Row.LOWER), " "),
            poss.get((Side.LEFT, Mod.UPPER, Col.INNERMOST, Row.LOWER), " "),
            poss.get((Side.RIGHT, Mod.UPPER, Col.INNERMOST, Row.LOWER), " "),
            poss.get((Side.RIGHT, Mod.UPPER, Col.INDEX, Row.LOWER), " "),
            poss.get((Side.RIGHT, Mod.UPPER, Col.MIDDLE, Row.LOWER), " "),
            poss.get((Side.RIGHT, Mod.UPPER, Col.RING, Row.LOWER), " "),
            poss.get((Side.RIGHT, Mod.UPPER, Col.PINKY, Row.LOWER), " "),
        )
        + nav_str.format(
            poss.get((Side.LEFT, Mod.NAV, Col.PINKY, Row.UPPER), " "),
            poss.get((Side.LEFT, Mod.NAV, Col.RING, Row.UPPER), " "),
            poss.get((Side.LEFT, Mod.NAV, Col.MIDDLE, Row.UPPER), " "),
            poss.get((Side.LEFT, Mod.NAV, Col.INDEX, Row.UPPER), " "),
            poss.get((Side.LEFT, Mod.NAV, Col.INNERMOST, Row.UPPER), " "),
            poss.get((Side.RIGHT, Mod.NAV, Col.INNERMOST, Row.UPPER), " "),
            poss.get((Side.RIGHT, Mod.NAV, Col.INDEX, Row.UPPER), " "),
            poss.get((Side.RIGHT, Mod.NAV, Col.MIDDLE, Row.UPPER), " "),
            poss.get((Side.RIGHT, Mod.NAV, Col.RING, Row.UPPER), " "),
            poss.get((Side.RIGHT, Mod.NAV, Col.PINKY, Row.UPPER), " "),
            poss.get((Side.LEFT, Mod.NAV, Col.PINKY, Row.HOME), " "),
            poss.get((Side.LEFT, Mod.NAV, Col.RING, Row.HOME), " "),
            poss.get((Side.LEFT, Mod.NAV, Col.MIDDLE, Row.HOME), " "),
            poss.get((Side.LEFT, Mod.NAV, Col.INDEX, Row.HOME), " "),
            poss.get((Side.LEFT, Mod.NAV, Col.INNERMOST, Row.HOME), " "),
            poss.get((Side.RIGHT, Mod.NAV, Col.INNERMOST, Row.HOME), " "),
            poss.get((Side.RIGHT, Mod.NAV, Col.INDEX, Row.HOME), " "),
            poss.get((Side.RIGHT, Mod.NAV, Col.MIDDLE, Row.HOME), " "),
            poss.get((Side.RIGHT, Mod.NAV, Col.RING, Row.HOME), " "),
            poss.get((Side.RIGHT, Mod.NAV, Col.PINKY, Row.HOME), " "),
            poss.get((Side.LEFT, Mod.NAV, Col.PINKY, Row.LOWER), " "),
            poss.get((Side.LEFT, Mod.NAV, Col.RING, Row.LOWER), " "),
            poss.get((Side.LEFT, Mod.NAV, Col.MIDDLE, Row.LOWER), " "),
            poss.get((Side.LEFT, Mod.NAV, Col.INDEX, Row.LOWER), " "),
            poss.get((Side.LEFT, Mod.NAV, Col.INNERMOST, Row.LOWER), " "),
            poss.get((Side.RIGHT, Mod.NAV, Col.INNERMOST, Row.LOWER), " "),
            poss.get((Side.RIGHT, Mod.NAV, Col.INDEX, Row.LOWER), " "),
            poss.get((Side.RIGHT, Mod.NAV, Col.MIDDLE, Row.LOWER), " "),
            poss.get((Side.RIGHT, Mod.NAV, Col.RING, Row.LOWER), " "),
            poss.get((Side.RIGHT, Mod.NAV, Col.PINKY, Row.LOWER), " "),
        )
    )
