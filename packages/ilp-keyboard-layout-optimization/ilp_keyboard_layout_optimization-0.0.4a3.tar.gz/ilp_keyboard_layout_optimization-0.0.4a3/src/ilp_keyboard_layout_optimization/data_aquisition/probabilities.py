"""This module contains a class representing (special) character counts"""

__all__ = ["CharProbs"]

import csv
import os
from collections import defaultdict
from os.path import abspath, basename
from typing import List, Optional
from urllib.parse import urlparse
from urllib.request import urlopen

from .chars import Chars
from ..type_aliases import Bigram, Char, ProbDict


class CharProbs:
    """Instances represent all relevant (special) character probabilities

    Parameters
    ----------
    chars : Chars
        the set of characters to consider
    mono_urls : str
        download URLs for the monogram probabilities including their file name
    bi_urls : str
        download URLs for the bigram probabilities including their file name
    """

    MONO_URLS: List[str] = [
        "http://www.ids-mannheim.de/fileadmin/kl/derewo/"
        "DeReChar-v-uni-204-a-c-2018-02-28-1.0.csv",
        "https://hg.sr.ht/~arnebab/evolve-keyboard-layout/raw/"
        "1-gramme.15.txt?rev=tip",
        "https://hg.sr.ht/~arnebab/evolve-keyboard-layout/raw/"
        "1-gramme.wiki.txt?rev=tip",
        "https://hg.sr.ht/~arnebab/evolve-keyboard-layout/raw/1gramme.txt?rev=tip",
    ]

    BI_URLS: List[str] = [
        "https://hg.sr.ht/~arnebab/evolve-keyboard-layout/raw/2-gramme.15.txt?rev=tip",
        "https://hg.sr.ht/~arnebab/evolve-keyboard-layout/raw/"
        "2-gramme.wiki.txt?rev=tip",
        "https://hg.sr.ht/~arnebab/evolve-keyboard-layout/raw/2gramme.txt?rev=tip",
    ]

    def __init__(
        self,
        chars: Chars = None,
        mono_urls: List[str] = None,
        bi_urls: List[str] = None,
    ):
        self.chars: Optional[str] = None if chars is None else chars.chars
        self._no_char_restr = self.chars is None
        self.mono_urls: List[str] = self.MONO_URLS if mono_urls is None else mono_urls
        self.bi_urls: List[str] = self.BI_URLS if bi_urls is None else bi_urls
        self.mono_filenames: List[str] = self.download_raw_to_files(self.mono_urls)
        self.bi_filenames: List[str] = self.download_raw_to_files(self.bi_urls)
        self._mono_probs = self._extract_monogram_data()
        self._bi_probs = self._extract_bigram_data()

    @staticmethod
    def download_raw_to_file(url: str, overwrite: bool = False) -> str:
        """Download raw data from a URL

        Parameters
        ----------
        url : str
            download URL including file name
        overwrite : bool
            if True a present file gets replaced by the specified file, otherwise
            (default) local file stays and does not get replaced

        Returns
        -------
        str
            file name of the raw data on disc extracted from the URL
        """
        filename = abspath(basename(urlparse(url).path))
        if overwrite or not os.path.exists(filename):
            with urlopen(url) as response, open(filename, "wb") as out_file:
                downloaded_raw_data = response.read()
                out_file.write(downloaded_raw_data)
        return filename

    @staticmethod
    def download_raw_to_files(urls: List[str]) -> List[str]:
        """Download raw data from a URLs

        Parameters
        ----------
        urls : list of str
            download URLs including file names

        Returns
        -------
        list of str
            files name of the raw data on disc extracted from the URLs
        """
        filenames = []
        for url in urls:
            filenames.append(CharProbs.download_raw_to_file(url))
        return filenames

    def _extract_monogram_data(self) -> ProbDict:
        mono_probs = defaultdict(float)
        for mono_filename in self.mono_filenames:
            new_mono_probs = defaultdict(float)
            match basename(mono_filename):
                case "DeReChar-v-uni-204-a-c-2018-02-28-1.0.csv":
                    new_mono_probs = self._extract_derechar_monos(mono_filename)
                case "1-gramme.15.txt" | "1-gramme.wiki.txt" | "1gramme.txt":
                    new_mono_probs = self._extract_arnes_probs(mono_filename)
            mono_probs = CharProbs._merge_probs(mono_probs, new_mono_probs)
        return mono_probs

    def _extract_derechar_monos(self, filename: str) -> ProbDict:
        chars_left_to_find = Chars(self.chars)
        with open(filename, encoding="UTF-8") as mono_csv_file:
            mono_csv_dialect: str = "derechar"
            csv.register_dialect(
                mono_csv_dialect, delimiter="	", quoting=csv.QUOTE_NONE
            )
            reader = csv.DictReader(
                mono_csv_file,
                fieldnames=[
                    "probability",
                    "absolute_count",
                    "hexadecimal Unicode code point",
                    "decimal value corresponding to the code",
                    "unicode general category",
                    "glyph",
                    "name of the symbol",
                    "unicode block designation",
                ],
                dialect=mono_csv_dialect,
            )
            total_sum: float = 0.0
            mono_probs_per_hex_code: ProbDict = defaultdict(float)
            for row in reader:
                try:
                    probability = float(row["probability"])
                except ValueError:
                    continue
                assert probability
                if self._no_char_restr or row["glyph"] in self.chars:
                    mono_probs_per_hex_code[
                        row["hexadecimal Unicode code point"]
                    ] = probability
                    assert mono_probs_per_hex_code[
                        row["hexadecimal Unicode code point"]
                    ] == float(row["probability"])
                    total_sum += probability
                    if chars_left_to_find is not None:
                        chars_left_to_find.remove(row["glyph"])
                assert total_sum == sum(mono_probs_per_hex_code.values())
                if chars_left_to_find is not None and not chars_left_to_find.chars:
                    break
        if self._no_char_restr:
            assert CharProbs._almost_equal_to_one(total_sum)
            assert len(mono_probs_per_hex_code) == reader.line_num - 2
            del mono_probs_per_hex_code[""]
            assert len(mono_probs_per_hex_code) == reader.line_num - 3
        else:
            assert total_sum <= 1.0
            assert len(mono_probs_per_hex_code) == len(self.chars)
        mono_probs_per_hex_code = CharProbs.strip_and_normalize_probs(
            mono_probs_per_hex_code
        )
        assert CharProbs._almost_equal_to_one(sum(mono_probs_per_hex_code.values()))
        mono_probs: ProbDict = defaultdict(float)
        for code, prob in mono_probs_per_hex_code.items():
            mono_probs[chr(int(code[2:], 16))] = prob
        assert CharProbs._almost_equal_to_one(sum(mono_probs.values()))
        return mono_probs

    @staticmethod
    def _almost_equal_to_one(number: float) -> bool:
        return round(number, 8) == 1.0

    @staticmethod
    def _merge_probs(probs_origin: ProbDict, probs_to_merge: ProbDict) -> ProbDict:
        for char, prob in probs_to_merge.items():
            probs_origin[char] += prob
        normed_and_stripped_probs = CharProbs.strip_and_normalize_probs(probs_origin)
        assert not normed_and_stripped_probs or CharProbs._almost_equal_to_one(
            sum(normed_and_stripped_probs.values())
        )
        return normed_and_stripped_probs

    @staticmethod
    def strip_and_normalize_probs(probs: ProbDict) -> ProbDict:
        """Strip from all zero elements and ensure values sum up to one

        Parameters
        ----------
        probs : ProbDict
            the dictionary of probabilities

        Returns
        -------
        ProbDict
            the stripped and normalized dict, in which the elements' values are
            guaranteed to sum up to one and no zeros are left
        """
        absolute_sum = sum(probs.values())
        stripped_and_normalized_probs = defaultdict(float)
        for char, count in probs.items():
            if count != 0:
                stripped_and_normalized_probs[char] = count / absolute_sum
        return stripped_and_normalized_probs

    def _extract_arnes_probs(self, filename: str) -> ProbDict:
        if CharProbs._currently_processing_bigrams(filename):
            chars_left_to_find = set(Chars(self.chars).bis)
        else:
            chars_left_to_find = set(Chars(self.chars).monos)
        with open(filename, encoding="utf-8-sig") as txt_file:
            total_sum: int = 0
            probs: ProbDict = defaultdict(int)
            for row in txt_file:
                count_and_glyphs: List[str, str] = (
                    row.lstrip().rstrip("\n").split(" ", 1)
                )
                if CharProbs._should_be_bigram_but_is_not(
                    count_and_glyphs[1], filename
                ) or CharProbs._is_replace_char(count_and_glyphs[1]):
                    continue
                assert (
                    Chars.is_bigram(count_and_glyphs[1])
                    if CharProbs._currently_processing_bigrams(filename)
                    else Chars.is_monogram(count_and_glyphs[1])
                )
                assert isinstance(count_and_glyphs, list)
                assert len(count_and_glyphs) == 2
                try:
                    count = int(count_and_glyphs[0])
                except ValueError:
                    continue
                if self._no_char_restr or (
                    count_and_glyphs[1][0] in self.chars
                    and count_and_glyphs[1][-1] in self.chars
                ):
                    probs[count_and_glyphs[1]] = count
                    total_sum += count
                    assert probs[count_and_glyphs[1]] == int(count_and_glyphs[0])
                    if chars_left_to_find is not None:
                        chars_left_to_find.discard(count_and_glyphs[1])
                assert total_sum == sum(probs.values())
                if chars_left_to_find is not None and not chars_left_to_find:
                    break
        normed_and_stripped_probs = CharProbs.strip_and_normalize_probs(probs)
        assert CharProbs._almost_equal_to_one(sum(normed_and_stripped_probs.values()))
        return normed_and_stripped_probs

    @staticmethod
    def _should_be_bigram_but_is_not(glyphs: Bigram, filename: str) -> bool:
        return "2" in basename(filename) and len(glyphs) == 1

    @staticmethod
    def _is_replace_char(glyphs: Char | Bigram) -> bool:
        return "65533" in " ".join(str(ord(char)) for char in glyphs)

    @staticmethod
    def _currently_processing_bigrams(filename: str) -> bool:
        return "2" in basename(filename)

    def _extract_bigram_data(self) -> ProbDict:
        bi_probs = defaultdict(float)
        for bi_filename in self.bi_filenames:
            bi_probs = CharProbs._merge_probs(
                bi_probs, self._extract_arnes_probs(bi_filename)
            )
        return bi_probs

    @property
    def mono_probs(self) -> ProbDict:
        """The probabilities for all single (special) characters"""
        return self._mono_probs

    @property
    def bi_probs(self) -> ProbDict:
        """The bigram probabilities for all (special) character pairs"""
        return self._bi_probs
