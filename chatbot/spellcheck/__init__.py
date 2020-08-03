import re
from os import path
from collections import Counter
from warnings import warn


class SpellChecker:

    def __init__(self, local_path, language='en'):
        try:
            self.WORDS = Counter(self.words(open(path.join(
                local_path, language, "words.txt"), encoding='utf-8').read()))
        except FileNotFoundError:
            warn("words.txt for language `{}` not found in `{}`".format(language, local_path),
                 ResourceWarning)
            self.WORDS = Counter()
        self.total_word_count = sum(self.WORDS.values())
        if self.total_word_count == 0:
            self.total_word_count = 1

    @staticmethod
    def words(text):
        return re.findall(r'\w+', text.lower())

    def correction(self, text, min_word_length=4):
        """
        Spell correction based on Most probable spelling correction for word.
        :param text: str
        :param min_word_length: word length
        :return: str
        """
        return " ".join(i if len(i) < min_word_length or self.WORDS[i]
                        else max(self.candidates(i), key=self.probability)
                        for i in text.split())

    def probability(self, word):
        """
        Probability of `word`.
        :param word:
        :return: float
        """
        return self.WORDS[word] / self.total_word_count

    def candidates(self, word):
        """
        Generate possible spelling corrections for word.
        :param word: str
        :return: set of known words
        """
        return (self.known([word]) or self.known(self.edits1(word)) or
                self.known(self.edits2(word)) or [word])

    def known(self, words):
        """
        The subset of `words` that appear in the dictionary of WORDS.
        :param words: list of str
        :return: unique set of words
        """
        return set(w for w in words if w in self.WORDS)

    @staticmethod
    def edits1(word):
        """
        All edits that are one edit away from `word`.
        :param word: String
        :return: set of words
        """
        letters = 'abcdefghijklmnopqrstuvwxyz'
        splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
        deletes = [L + R[1:] for L, R in splits if R]
        transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
        replaces = [L + c + R[1:] for L, R in splits if R for c in letters]
        inserts = [L + c + R for L, R in splits for c in letters]
        return set(deletes + transposes + replaces + inserts)

    def edits2(self, word):
        """
        All edits that are two edits away from `word`.
        :param word: string
        :return: string generator
        """
        return (e2 for e1 in self.edits1(word) for e2 in self.edits1(e1))
