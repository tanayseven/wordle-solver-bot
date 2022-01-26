import json
from pathlib import Path
from typing import Final


class WordsRepository:
    def __init__(self, words: tuple[str, ...] = None, letters_to_remember: tuple[str, str, str, str, str] = ()):
        self._words: Final[tuple[str]] = json.loads(Path("words_dictionary.json").read_text()) \
            if words is None else words
        self._letters_to_remember: tuple[str, str, str, str, str] = letters_to_remember

    def forget(self, letters: str) -> "WordsRepository":
        normalized_letters = frozenset(x for x in letters.lower())
        new_set_of_words = tuple(
            word
            for word in self._words
            if all(
                letter not in word
                for letter in normalized_letters
            ) and all(
                word[index] in word_letter
                for index, word_letter in enumerate(self._letters_to_remember)
            )
        )
        return WordsRepository(new_set_of_words, self._letters_to_remember)

    @property
    def remaining_words(self) -> tuple[str]:
        return self._words

    def remember_not_at(self, current_word: str, at_positions: list[int]) -> "WordsRepository":
        new_set_of_words = tuple(
            word
            for word in self._words
            if all(
                word[position] != current_word[position] and current_word[position] in word
                for position in at_positions
            )
        )
        return WordsRepository(new_set_of_words, self._letters_to_remember)

    def remember_at(self, current_word: str, at_positions: list[int]) -> "WordsRepository":
        new_set_of_words = tuple(
            word
            for word in self._words
            if all(
                word[position] == current_word[position]
                for position in at_positions
            )
        )
        new_words_to_remember = tuple(
            letters + current_word[letter_index]
            for letter_index, letters
            in enumerate(self._letters_to_remember)
        )
        return WordsRepository(new_set_of_words, new_words_to_remember) # type: ignore

    def forget_word(self, word_to_forget: str):
        word_to_forget = word_to_forget.lower()
        new_set_of_words = tuple(
            word
            for word in self._words
            if word != word_to_forget
        )
        return WordsRepository(new_set_of_words, self._letters_to_remember)
