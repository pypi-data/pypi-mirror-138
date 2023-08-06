import os
from collections import defaultdict
from typing import Callable, List
from urllib.request import urlopen

import pytest
from hypothesis import given, strategies as hst
from hypothesis.strategies import composite

from ilp_keyboard_layout_optimization.data_aquisition.chars import Chars
from ilp_keyboard_layout_optimization.data_aquisition.probabilities import CharProbs
from ilp_keyboard_layout_optimization.type_aliases import ProbDict


@pytest.fixture(scope="session")
def chars_probs():
    return CharProbs()


@composite
def probs(draw: Callable):
    numbers = defaultdict(int)
    for key in range(draw(hst.integers(min_value=1, max_value=100))):
        numbers[key] = draw(hst.integers(min_value=1))
    normalized_numbers = CharProbs.strip_and_normalize_probs(numbers)
    return normalized_numbers


@pytest.fixture(scope="session")
def default_probs():
    return defaultdict(int)


@pytest.fixture(scope="session")
def mono_url():
    return "https://hg.sr.ht/~arnebab/evolve-keyboard-layout/raw/1gramme.txt?rev=tip"


@pytest.fixture(scope="session")
def bi_url():
    return "https://hg.sr.ht/~arnebab/evolve-keyboard-layout/raw/2gramme.txt?rev=tip"


@pytest.fixture(scope="session")
def custom_chars_probs(mono_url, bi_url):
    return CharProbs(Chars("ABC"), [mono_url], [bi_url])


def test_class_attribute_mono_urls():
    assert CharProbs.MONO_URLS


def test_class_attribute_bi_urls():
    assert CharProbs.BI_URLS


def test_static_download_method():
    assert CharProbs.download_raw_to_file


def test_static_downloads_method():
    assert CharProbs.download_raw_to_files


def test_class_method_merge_probs():
    assert CharProbs._merge_probs


@given(probs(), probs())
def test_class_method_merge_probs(probs_1, probs_2):
    assert CharProbs._merge_probs(probs_1, probs_2)


@given(probs(), probs())
def test_class_method_merge_probs(probs_1, probs_2):
    assert sum(CharProbs._merge_probs(probs_1, probs_2).values()) == pytest.approx(1)


@given(probs())
def test_class_method_merge_with_default_probs(default_probs, probs_2):
    assert CharProbs._merge_probs(default_probs, probs_2)


@given(probs())
def test_class_method_merge_with_default_probs(default_probs, probs_2):
    assert sum(
        CharProbs._merge_probs(default_probs, probs_2).values()
    ) == pytest.approx(1)


def test_class_method_almost_equal_to_one():
    assert CharProbs._almost_equal_to_one


def test_class_method_normalize_probs():
    assert CharProbs.strip_and_normalize_probs


def test_class_method_strip_and_normalize_probs_sums_up_to_one():
    test_dict = {str(integer): integer for integer in range(5)}
    assert sum(CharProbs.strip_and_normalize_probs(test_dict).values()) == 1.0


def test_class_method_strip_and_normalize_probs_stripped_from_zeros():
    test_dict = {str(integer): integer for integer in range(5)}
    assert "0" not in set(CharProbs.strip_and_normalize_probs(test_dict).keys())


def test_init_attribute_chars(custom_chars_probs):
    assert custom_chars_probs.chars


def test_init_attribute_mono_urls(chars_probs):
    assert chars_probs.mono_urls


def test_init_attribute_bi_urls(chars_probs):
    assert chars_probs.bi_urls


def test_init_attribute_mono_filenames(chars_probs):
    assert chars_probs.mono_filenames


def test_init_attribute_bi_filenames(chars_probs):
    assert chars_probs.bi_filenames


def test_init_attribute_download_function(chars_probs):
    assert chars_probs.download_raw_to_file


def test_download_function_result(custom_chars_probs, bi_url):
    file = custom_chars_probs.download_raw_to_file(bi_url)
    assert os.path.exists(file)


def test_download_function_type(custom_chars_probs, bi_url):
    assert isinstance(custom_chars_probs.download_raw_to_file(bi_url), str)


def test_downloads_function_result(custom_chars_probs, bi_url, mono_url):
    files = custom_chars_probs.download_raw_to_files([bi_url, mono_url])
    for file in files:
        assert os.path.exists(file)


def test_downloads_function_type(custom_chars_probs, bi_url, mono_url):
    assert isinstance(
        custom_chars_probs.download_raw_to_files([bi_url, mono_url]), list
    )


def test_init_attribute_downloads_function(custom_chars_probs):
    assert custom_chars_probs.download_raw_to_files


def test_init_attribute_extract_monogram_data(chars_probs):
    assert chars_probs._extract_monogram_data


def test_init_attribute_extract_bigram_data(chars_probs):
    assert chars_probs._extract_bigram_data


def test_init_attribute_mono_probs(chars_probs):
    assert chars_probs.mono_probs


def test_init_attribute_bi_probs(chars_probs):
    assert chars_probs.bi_probs


def test_init_attribute_currently_processing_bigrams():
    assert CharProbs._currently_processing_bigrams


def test_init_attribute_currently_processing_bigrams_result_for_bigram(bi_url):
    assert CharProbs._currently_processing_bigrams(bi_url)


def test_init_attribute_currently_processing_bigrams_result_for_monogram(mono_url):
    assert not CharProbs._currently_processing_bigrams(mono_url)


def test_init_attribute_bi_probs_type(custom_chars_probs):
    assert isinstance(custom_chars_probs.bi_probs, ProbDict.__origin__)


def test_init_attribute_mono_probs_type(custom_chars_probs):
    assert isinstance(custom_chars_probs.mono_probs, ProbDict.__origin__)


def test_init_attribute_bi_probs_sum_up_to_one(custom_chars_probs):
    assert sum(custom_chars_probs.bi_probs.values()) == pytest.approx(1)


def test_init_attribute_mono_probs_sum_up_to_one(custom_chars_probs):
    assert sum(custom_chars_probs.mono_probs.values()) == pytest.approx(1)


def test_init_attribute_chars_type(custom_chars_probs):
    assert custom_chars_probs.chars


def test_init_attribute_extract_derechar_monos(chars_probs):
    filename = [
        filename
        for filename in chars_probs.mono_filenames
        if "DeReChar-v-uni-204-a-c-2018-02-28-1.0.csv" in filename
    ][0]
    assert isinstance(
        chars_probs._extract_derechar_monos(filename), ProbDict.__origin__
    )


def test_init_attribute_extract_derechar_sum_up_to_one(chars_probs):
    filename = [
        filename
        for filename in chars_probs.mono_filenames
        if "DeReChar-v-uni-204-a-c-2018-02-28-1.0.csv" in filename
    ][0]
    assert sum(chars_probs._extract_derechar_monos(filename).values()) == pytest.approx(
        1
    )


def test_init_attribute_extract_arnes_monos(chars_probs):
    assert chars_probs._extract_arnes_probs


@pytest.mark.parametrize(
    "basename", ["1-gramme.15.txt", "1-gramme.wiki.txt", "1gramme.txt"]
)
def test_init_attribute_extract_arnes_monos_type(basename, chars_probs):
    filename = [
        filename for filename in chars_probs.mono_filenames if basename in filename
    ][0]
    assert isinstance(chars_probs._extract_arnes_probs(filename), ProbDict.__origin__)


@pytest.mark.parametrize(
    "basename", ["1-gramme.15.txt", "1-gramme.wiki.txt", "1gramme.txt"]
)
def test_init_attribute_extract_arnes_monos_sum_up_to_one(basename, chars_probs):
    filename = [
        filename for filename in chars_probs.mono_filenames if basename in filename
    ][0]
    assert sum(chars_probs._extract_arnes_probs(filename).values()) == pytest.approx(1)


def test_init_default_monogram_file_download(chars_probs):
    compare_files_contents_to_http_responses(
        chars_probs.mono_filenames, chars_probs.mono_urls
    )


def compare_files_contents_to_http_responses(filenames: List[str], urls: List[str]):
    for filename in filenames:
        assert os.path.exists(filename)
    for url, filename in zip(urls, filenames):
        with urlopen(url) as response, open(filename) as file:
            assert file.read() == response.read().decode().replace("\r\n", "\n")


def test_init_custom_monogram_file_download(custom_chars_probs):
    compare_files_contents_to_http_responses(
        custom_chars_probs.mono_filenames, custom_chars_probs.mono_urls
    )


def test_init_default_bigram_file_download(chars_probs):
    compare_files_contents_to_http_responses(
        chars_probs.bi_filenames, chars_probs.bi_urls
    )


def test_init_custom_bigram_file_download(custom_chars_probs):
    compare_files_contents_to_http_responses(
        custom_chars_probs.bi_filenames, custom_chars_probs.bi_urls
    )


def test_init_extract_monogram_data(chars_probs):
    assert chars_probs._extract_monogram_data()


def test_init_extract_bigram_data(custom_chars_probs):
    assert custom_chars_probs._extract_bigram_data()


def test_init_custom_bigram_data(custom_chars_probs):
    bi_probs = custom_chars_probs.bi_probs
    assert (
        "AA" in bi_probs
        and "AB" in bi_probs
        and "BB" in bi_probs
        and "BA" in bi_probs
        and "AC" in bi_probs
        and "BC" in bi_probs
        and "CC" in bi_probs
        and "CA" in bi_probs
        and "CB" in bi_probs
    )


def test_init_custom_monogram_data(custom_chars_probs):
    mono_probs = custom_chars_probs.mono_probs
    assert "A" in mono_probs and "B" in mono_probs and "C" in mono_probs


def test_almost_equal_to_one_too_big():
    assert not CharProbs._almost_equal_to_one(1.00000001)


def test_almost_equal_to_one_too_small():
    assert not CharProbs._almost_equal_to_one(0.99999999)


def test_almost_equal_to_one_just_as_small():
    assert CharProbs._almost_equal_to_one(0.999999999)


def test_almost_equal_to_one_just_as_big():
    assert CharProbs._almost_equal_to_one(1.000000001)


def test_attr_is_replace_char():
    assert CharProbs._is_replace_char


def test_attr_is_replace_char():
    assert CharProbs._should_be_bigram_but_is_not


@given(hst.characters())
def test_attr_is_replace_char(bi_url, char):
    assert CharProbs._should_be_bigram_but_is_not(char, bi_url)


@given(hst.text(min_size=2, max_size=10))
def test_attr_is_replace_char(bi_url, chars):
    assert not CharProbs._should_be_bigram_but_is_not(chars, bi_url)


def test_is_replace_char():
    assert CharProbs._is_replace_char(chr(65533))


@given(hst.characters())
def test_is_not_replace_char(char):
    assert not CharProbs._is_replace_char(char)
