"""This module contains type aliases for type hints and thus more convenient coding"""

__all__ = [
    "Bigram",
    "Char",
    "CharPosPair",
    "CharPosQuadruple",
    "CharSet",
    "CharTuple",
    "LinCosts",
    "LinVars",
    "Pos",
    "PosPair",
    "PosTuple",
    "QuadCosts",
    "QuadVars",
]

Char = str
"""A (special) character"""
Pos = str
"""A position"""
CharPosPair = tuple[Char, Pos]
"""A pair of a (special) character and a position"""
Bigram = str
"""A length-two string of (special) characters"""
PosPair = tuple[Pos, Pos]
"""A tuple of two positions"""
CharTuple = tuple[Char, ...]
"""A tuple of several (special) characters"""
CharSet = set[Char]
"""A set of several (special) characters"""
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
