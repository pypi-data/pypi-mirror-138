"""This module contains the class providing a unified interface for character sets"""

__all__ = ["Chars"]

import string
from itertools import product
from typing import Optional, Tuple, Union

from ..type_aliases import Bigram, CharTuple


class Chars:
    """A unified interface to a collection of characters and corresponding bigrams

    Parameters
    ----------
    chars : str or CharTupel, optional
        A string of concatenated (special) characters or a CharTupel of single
        characters, that are supposed to be considered. Defaults to the most common
        letters, numbers and punctuation in German texts.
    """

    _chars: str
    _monos: CharTuple
    _bis: Tuple[Bigram]

    def __init__(self, chars: Optional[Union[str, CharTuple]] = None):
        if chars is None:
            self._chars = (
                string.ascii_lowercase
                + string.ascii_uppercase
                + string.digits
                + string.punctuation
                + "üöäÜÖÄß–…"
            )
        else:
            self.chars = chars

    @property
    def chars(self) -> str:
        return self._chars

    @chars.setter
    def chars(self, chars: Union[str, CharTuple]):
        if isinstance(chars, str):
            self._chars = chars
        else:  # isinstance(chars, CharTuple):
            self._chars = "".join(char for char in chars)
        try:
            del self._monos
        except AttributeError:
            pass
        try:
            del self._bis
        except AttributeError:
            pass

    @property
    def monos(self) -> CharTuple:
        try:
            return self._monos
        except AttributeError:
            self._monos = self._str2char_tuple(self.chars)
            return self._monos

    @staticmethod
    def _str2char_tuple(char_str: str) -> CharTuple:
        return tuple(char for char in char_str)

    @property
    def bis(self):
        try:
            return self._bis
        except AttributeError:
            self._bis = tuple(
                "".join(bigram_tuple) for bigram_tuple in product(self.chars, repeat=2)
            )
            return self._bis
