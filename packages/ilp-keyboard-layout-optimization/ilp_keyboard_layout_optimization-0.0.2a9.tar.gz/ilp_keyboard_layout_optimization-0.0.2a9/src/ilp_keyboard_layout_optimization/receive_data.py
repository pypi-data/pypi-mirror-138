"""This module contains a class representing (special) character counts"""

__all__ = ["CharProbs"]

import csv
from math import comb
from os.path import abspath, basename
from typing import Optional
from urllib.request import urlopen

from src.ilp_keyboard_layout_optimization.type_aliases import CharSet, CharTuple


class CharProbs:
    """Instances represent all relevant (special) character probabilities

    Parameters
    ----------
    mono_url : str
        download URL for the monogram probabilities including the file name
    bi_url : str
        download URL for the bigram probabilities including the file name
    """

    def __init__(
        self,
        chars: CharTuple = None,
        mono_url: str = "http://www.ids-mannheim.de/fileadmin/kl/derewo/"
        "DeReChar-v-uni-204-a-c-2018-02-28-1.0.csv",
        bi_url: str = "http://practicalcryptography.com/media/cryptanalysis/files/"
        "german_bigrams.txt",
    ):
        self.chars: Optional[CharSet] = None if chars is None else set(chars)
        self.mono_url: str = mono_url
        self.bi_url: str = bi_url
        self.mono_filename: str = self.download_raw_to_file(self.mono_url)
        self.bi_filename: str = self.download_raw_to_file(self.bi_url)
        self._mono_probs = self._extract_monogram_data()
        self._bi_probs = self._extract_bigram_data()

    @staticmethod
    def download_raw_to_file(url: str) -> str:
        """Download raw data from a URL

        Parameters
        ----------
        url : str
            download URL including file name

        Returns
        -------
        str
            file name of the raw data on disc extracted from the URL
        """
        filename = abspath(basename(url))
        with urlopen(url) as response, open(filename, "wb") as out_file:
            downloaded_raw_data = response.read()
            out_file.write(downloaded_raw_data)
        return filename

    def _extract_monogram_data(self) -> dict[str, float]:
        with open(self.mono_filename, encoding="UTF-8") as mono_csv_file:
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
            mono_probs: dict[str, float] = {}
            for row in reader:
                try:
                    probability = float(row["probability"])
                except ValueError:
                    continue
                total_sum += probability
                if self.chars is None or row["glyph"] in self.chars:
                    mono_probs[row["glyph"]] = probability
                    assert mono_probs[row["glyph"]] == float(row["probability"])
        assert round(total_sum, 8) == 1.0 if self.chars is None else total_sum <= 1.0
        assert (
            len(mono_probs) == reader.line_num - 4
            if self.chars is None
            else len(self.chars)
        )
        return mono_probs

    def _extract_bigram_data(self) -> dict[str, float]:
        bi_txt_dialect: str = "jamestxt"
        csv.register_dialect(bi_txt_dialect, delimiter=" ")
        with open(self.bi_filename, encoding="UTF-8") as bi_csv_file:
            reader = csv.DictReader(
                bi_csv_file,
                fieldnames=[
                    "bigram",
                    "absolute_count",
                ],
                dialect=bi_txt_dialect,
            )
            bi_probs: dict[str, float] = {}
            for row in reader:
                try:
                    absolute_count = int(row["absolute_count"])
                except ValueError:
                    continue
                assert len(row["bigram"]) == 2
                if self.chars is None or (
                    row["bigram"][0] in self.chars and row["bigram"][1] in self.chars
                ):
                    bi_probs[row["bigram"]] = absolute_count
        absolute_sum = sum(bi_probs.values())
        for character, count in bi_probs.items():
            bi_probs[character] = count / absolute_sum
        assert round(sum(bi_probs.values()), 8) == 1
        assert len(bi_probs) == reader.line_num or len(bi_probs) <= comb(
            reader.line_num, 2
        )
        return bi_probs

    @property
    def mono_probs(self):
        """The probabilities for all single (special) characters"""
        return self._mono_probs

    @property
    def bi_probs(self):
        """The bigram probabilities for all (special) character pairs"""
        return self._bi_probs


if __name__ == "__main__":
    CharProbs(
        None,
        "http://www.ids-mannheim.de/fileadmin/kl/derewo/"
        "DeReChar-v-uni-204-a-c-2018-02-28-1.0.csv",
        "http://practicalcryptography.com/media/cryptanalysis/files/"
        "german_bigrams.txt",
    )
