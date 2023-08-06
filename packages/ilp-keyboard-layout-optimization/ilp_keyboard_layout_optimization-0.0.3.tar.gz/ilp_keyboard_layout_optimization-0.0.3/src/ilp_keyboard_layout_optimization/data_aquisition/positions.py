from dataclasses import dataclass
from itertools import product

from ..type_aliases import Col, Mod, Pos, PosTuple, Row, Side


@dataclass
class Positions:
    """An instance provides a tuple of relevant positions on our Corne keyboard

    Attributes
    ----------
    poss : PosTuple
        the relevant positions to assign chars to on our Corne keyboard
    """

    poss: PosTuple

    def __init__(self):
        poss = set(
            product(
                Side,
                Mod,
                (Col.PINKY, Col.RING, Col.MIDDLE, Col.INDEX, Col.INNERMOST),
                Row,
            )
        )
        for mod in (Mod.SHIFT, Mod.NONE, Mod.LOWER):
            poss.add(Pos(Side.RIGHT, mod, Col.OUTERMOST, Row.HOME))
        for col in (Col.PINKY, Col.RING, Col.MIDDLE, Col.INDEX, Col.INNERMOST):
            for side in Side:
                poss.remove(Pos(side, Mod.LOWER, col, Row.UPPER))
        self.poss = tuple(poss)
