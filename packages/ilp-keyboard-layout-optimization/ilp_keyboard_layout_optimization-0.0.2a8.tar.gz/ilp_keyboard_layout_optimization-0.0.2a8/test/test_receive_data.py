import os
from urllib.request import urlopen

import pytest

from src.ilp_keyboard_layout_optimization.receive_data import CharProbs


@pytest.fixture
def characters_count():
    return CharProbs()


@pytest.fixture()
def characters_count_custom():
    return CharProbs(
        ("A", "B", "C"),
        "http://www.ids-mannheim.de/fileadmin/kl/derewo/"
        "DeReChar-v-uni-204-a-c-2018-02-28-1.0.csv",
        "http://practicalcryptography.com/media/cryptanalysis/files/"
        "german_bigrams.txt",
    )


def test_init_attribute_chars(characters_count_custom):
    assert characters_count_custom.chars


def test_init_attribute_mono_url(characters_count):
    assert characters_count.mono_url


def test_init_attribute_bi_url(characters_count):
    assert characters_count.bi_url


def test_init_attribute_mono_filename(characters_count):
    assert characters_count.mono_filename


def test_init_attribute_bi_filename(characters_count):
    assert characters_count.bi_filename


def test_init_attribute_download_function(characters_count):
    assert characters_count.download_raw_to_file


def test_init_attribute_extract_monogram_data(characters_count):
    assert characters_count._extract_monogram_data


def test_init_attribute_extract_bigram_data(characters_count):
    assert characters_count._extract_bigram_data


def test_init_attribute_mono_probs(characters_count):
    assert characters_count.mono_probs


def test_init_attribute_bi_probs(characters_count):
    assert characters_count.bi_probs


def test_init_default_monogram_file_download(characters_count):
    assert os.path.exists(characters_count.mono_filename)
    with urlopen(characters_count.mono_url) as response, open(
        characters_count.mono_filename
    ) as file:
        assert file.read() == response.read().decode()


def test_init_custom_monogram_file_download(characters_count_custom):
    with urlopen(characters_count_custom.mono_url) as response, open(
        characters_count_custom.mono_filename
    ) as file:
        assert file.read() == response.read().decode()


def test_init_default_bigram_file_download(characters_count):
    assert os.path.exists(characters_count.bi_filename)
    with urlopen(characters_count.bi_url) as response, open(
        characters_count.bi_filename
    ) as file:
        assert file.read() == response.read().decode()


def test_init_extract_monogram_data(characters_count):
    assert characters_count._extract_monogram_data()


def test_init_extract_bigram_data(characters_count):
    assert characters_count._extract_bigram_data()


def test_init_custom_bigram_data(characters_count_custom):
    assert (
        "AA" in characters_count_custom.bi_probs
        and "AB" in characters_count_custom.bi_probs.keys()
        and "BB" in characters_count_custom.bi_probs
        and "BA" in characters_count_custom.bi_probs
        and "AC" in characters_count_custom.bi_probs
        and "BC" in characters_count_custom.bi_probs
        and "CC" in characters_count_custom.bi_probs
        and "CA" in characters_count_custom.bi_probs
        and "CB" in characters_count_custom.bi_probs
    )
