from dataclasses import dataclass
from itertools import product
from typing import Optional

from ..type_aliases import Col, Mod, Pos, PosTuple, Row, Side


@dataclass
class Positions:
    """An instance provides a tuple of relevant positions on our Corne keyboard

    Parameters
    ----------
    poss : PosTuple, optional
        the relevant positions to assign chars to, defaults to
        all actually available positions on our Corne keyboard
    Attributes
    ----------
    poss : PosTuple
        the relevant positions to assign chars to
    """

    poss: PosTuple

    def __init__(self, poss: Optional[PosTuple] = None):
        if poss is None:
            poss_set = set(
                product(
                    Side,
                    Mod,
                    (Col.PINKY, Col.RING, Col.MIDDLE, Col.INDEX, Col.INNERMOST),
                    Row,
                )
            )
            for mod in (Mod.SHIFT, Mod.NONE, Mod.LOWER):
                poss_set.add(Pos(Side.RIGHT, mod, Col.OUTERMOST, Row.HOME))
            for col in (Col.PINKY, Col.RING, Col.MIDDLE, Col.INDEX, Col.INNERMOST):
                for side in Side:
                    poss_set.remove(Pos(side, Mod.LOWER, col, Row.UPPER))
            poss = tuple(poss_set)
        self.poss = poss
