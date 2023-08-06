"""This module is meant to find the corresponding costs of certain assignments

Our approach here is to follow the ideas and conclusions as well as most of
the assumptions from

Feit, Anna Maria. ‘Assignment Problems for Optimizing Text Input’, n.d., 182.

This leads to some specific objective function, that require certain parameters to be
set. Details on that in our talk on the topic. The parameters needed are all
concerning the texts to type:

- the overall frequency of the single (special) characters
- the frequency of all bigrams, that is pairs of (special) characters
- the "times" to press certain (modified) keys at all
- the "times" to press certain (modified) keys one after another
- the (binary) information for each of the (modified) keys, if it is hard to reach
- (normalized) similarity measures for each two (special) character bigram
- distances between (modified) keys in terms of familiarity and intuitiveness
"""

FreqTuple = tuple[float, ...]


def setup_frequencies() -> FreqTuple:
    """Set up the frequencies used to weight the assignment of characters

    Returns
    -------
    FreqTuple
        the frequencies used to weight the assignment of characters
    """
    frequencies = (1, 2)
    return frequencies
