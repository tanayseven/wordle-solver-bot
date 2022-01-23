import json
from pathlib import Path
from typing import Final


class WordsRepository:
    def __init__(self, words: tuple[str, ...] = None, letters_in_words: frozenset = frozenset()):
        self._words: Final[tuple[str]] = json.loads(Path("words_dictionary.json").read_text()) \
            if words is None else words
        self._letters_in_words: Final[frozenset] = letters_in_words

    def forget(self, letters: str) -> "WordsRepository":
        normalized_letters = letters.lower()
        normalized_letters = "".join(set([x for x in normalized_letters]).difference([x for x in self._letters_in_words]))
        new_set_of_words = tuple(
            word
            for word in self._words
            if all(
                (letter not in word)
                for letter in normalized_letters
            )
        )
        return WordsRepository(new_set_of_words, self._letters_in_words)

    @property
    def remaining_words(self) -> tuple[str]:
        return self._words

    def remember_not_at(self, letter: str, at_position: int) -> "WordsRepository":
        letter = letter.lower()
        new_set_of_words = tuple(
            word
            for word in self._words if letter in word and word[at_position] != letter
        )
        new_letters_to_remember = self._letters_in_words.union(frozenset(letter))
        return WordsRepository(new_set_of_words, new_letters_to_remember)

    def remember_at(self, letter: str, at_position: int) -> "WordsRepository":
        letter = letter.lower()
        new_set_of_words = tuple(
            word
            for word in self._words
            if word[at_position] == letter
        )
        new_letters_to_remember = self._letters_in_words.union(frozenset(letter))
        return WordsRepository(new_set_of_words, new_letters_to_remember)

    def forget_word(self, word_to_forget: str):
        word_to_forget = word_to_forget.lower()
        new_set_of_words = tuple(
            word
            for word in self._words
            if word != word_to_forget
        )
        return WordsRepository(new_set_of_words, self._letters_in_words)
