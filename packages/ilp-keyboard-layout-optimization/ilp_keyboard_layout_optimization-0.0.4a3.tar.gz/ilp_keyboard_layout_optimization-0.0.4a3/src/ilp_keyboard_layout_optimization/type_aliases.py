"""This module contains type aliases for type hints and thus more convenient coding"""

__all__ = [
    "Bigram",
    "Char",
    "CharPosPair",
    "CharPosQuadruple",
    "CharTuple",
    "Col",
    "LinCosts",
    "LinVars",
    "Mod",
    "Pos",
    "PosPair",
    "PosTuple",
    "ProbDict",
    "QuadCosts",
    "QuadVars",
    "Row",
    "Side",
]

from collections import defaultdict
from enum import auto, Enum
from typing import NamedTuple

Char = str
"""A (special) character"""


class Side(Enum):
    """Side of a position, i.e. if usually reached with the left or the right hand"""

    LEFT = auto()
    RIGHT = auto()


class Mod(Enum):
    """Modifier keys needed to reach a position"""

    NONE = 0
    SHIFT = 1
    UPPER = 3
    LOWER = 4
    NAV = 2


class Col(Enum):
    """Column of a position"""

    OUTERMOST = 0
    PINKY = 1
    RING = 2
    MIDDLE = 3
    INDEX = 4
    INNERMOST = 5


class Row(Enum):
    """Column of a position"""

    UPPER = 0
    HOME = 1
    LOWER = 2


class Pos(NamedTuple):
    """A position including side, modifiers, column and row"""

    side: Side
    mod: Mod
    col: Col
    row: Row


CharPosPair = tuple[Char, Pos]
"""A pair of a (special) character and a position"""
Bigram = str
"""A length-two string of (special) characters"""
PosPair = tuple[Pos, Pos]
"""A tuple of two positions"""
CharTuple = tuple[Char, ...]
"""A tuple of several (special) characters"""
PosTuple = tuple[Pos, ...]
"""A tuple of several positions"""
LinCosts = dict[CharPosPair, float]
"""A dictionary assigning costs to (special) character bigrams"""
CharPosQuadruple = tuple[Char, Char, Pos, Pos]
"""A four-tuple: two (special) characters and their respective positions"""
QuadCosts = dict[CharPosQuadruple, float]
"""A dictionary assigning costs to (special) character, position quadruples"""
LinVars = dict[CharPosPair, bool]
"""A dictionary of binary decisions of assigning (special) characters to positions"""
QuadVars = dict[CharPosQuadruple, bool]
"""A dictionary of binary vars assigning two (special) characters to two positions"""
ProbDict = defaultdict[Char | Bigram, float]
"""A dictionary of probabilities, defaulting to zero"""
