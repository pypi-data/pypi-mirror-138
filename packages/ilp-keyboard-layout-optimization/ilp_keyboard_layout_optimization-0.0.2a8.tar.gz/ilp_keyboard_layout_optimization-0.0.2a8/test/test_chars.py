from typing import Iterable, List

from hypothesis import given, settings, strategies as hst

from src.ilp_keyboard_layout_optimization.data_aquisition.chars import (
    Chars,
)
from src.ilp_keyboard_layout_optimization.type_aliases import CharTuple


def test_chars_init():
    assert Chars()


def test_chars_chars_type():
    assert isinstance(Chars().chars, str)


def test_chars_monos_type():
    assert isinstance(Chars().monos, CharTuple.__origin__)


@given(hst.lists(hst.characters(), min_size=1))
@settings(deadline=None)
def test_chars_input_tuple(char_tuple):
    assert Chars(tuple(char_tuple)).chars == "".join(char_tuple)


@given(hst.text(min_size=1))
def test_chars_input_str(char_string):
    assert Chars(char_string).chars == char_string


@given(hst.text(min_size=1))
def test_chars_input_tuple_equals_input_str(char_string):
    char_tuple = Chars._str2char_tuple(char_string)
    assert Chars(char_string).chars == Chars(char_tuple).chars


@given(hst.text(min_size=1))
def test_chars_input_str(char_string):
    assert Chars(char_string).chars == char_string


def test_chars_default():
    all_test_chars = list(Chars().chars)
    basic_latin = _get_unicode_chars(range(0x0021, 0x007F))
    latin_1_supp = _get_unicode_chars(
        (0x00C4, 0x00D6, 0x00DC, 0x00E4, 0x00F6, 0x00FC, 0x00DF)
    )
    general_punc = _get_unicode_chars((0x2013, 0x2026))
    extended_alphabet = basic_latin + latin_1_supp + general_punc
    for char in extended_alphabet:
        assert char in all_test_chars
        all_test_chars.remove(char)
    assert not all_test_chars


def _get_unicode_chars(code_point_range: Iterable) -> List[str]:
    return [chr(char) for char in code_point_range]


def test_chars_monograms():
    assert Chars().monos


def test_chars_monograms_multiple_times():
    test_chars = Chars()
    first_time_monos = test_chars.monos
    second_time_monos = test_chars.monos
    assert first_time_monos == second_time_monos


@given(hst.lists(hst.characters(), min_size=3))
def test_chars_monograms_after_resetting(char_tuple):
    first_test_chars = Chars(char_tuple)
    assert first_test_chars.monos == tuple(char_tuple)
    first_test_chars.chars = char_tuple[1:-1]
    assert first_test_chars.monos == tuple(char_tuple[1:-1])


def test_chars_bigrams():
    assert Chars().bis


def test_chars_bigrams_length():
    for bigram in Chars().bis:
        assert len(bigram) == 2


def test_bigrams_default():
    all_test_bigrams = list(Chars("1234").bis)
    actual_bigrams = (
        "11",
        "12",
        "21",
        "13",
        "31",
        "14",
        "41",
        "22",
        "23",
        "32",
        "24",
        "42",
        "33",
        "34",
        "44",
        "43",
    )
    for bigram in actual_bigrams:
        assert bigram in all_test_bigrams
        all_test_bigrams.remove(bigram)
    assert not all_test_bigrams


def test_chars_bigrams_multiple_times():
    test_chars = Chars()
    first_time_bis = test_chars.bis
    second_time_bis = test_chars.bis
    assert first_time_bis == second_time_bis


def test_chars_bigrams_after_resetting():
    test_chars = Chars("12")
    first_bigram_list = list(test_chars.bis)
    first_actual_bigrams = (
        "11",
        "12",
        "21",
        "22",
    )
    for bigram in first_actual_bigrams:
        assert bigram in first_bigram_list
        first_bigram_list.remove(bigram)
    assert not first_bigram_list
    test_chars.chars = "23"
    second_bigram_list = list(test_chars.bis)
    second_actual_bigrams = (
        "22",
        "23",
        "32",
        "33",
    )
    for bigram in second_actual_bigrams:
        assert bigram in second_bigram_list
        second_bigram_list.remove(bigram)
    assert not second_bigram_list
