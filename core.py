import json
from pathlib import Path
from typing import Final


class WordsRepository:
    def __init__(self, words: tuple[str, ...] = None,
                 letters_to_remember_at: tuple[str, str, str, str, str] = ("", "", "", "", "")):
        self._words: Final[tuple[str]] = json.loads(Path("words_dictionary.json").read_text()) \
            if words is None else words
        self._letters_to_remember_at: tuple[str, str, str, str, str] = letters_to_remember_at

    def forget(self, grey_letters: str) -> "WordsRepository":
        words_to_remember = tuple(
            word
            for word in self._words
            if all(
                word[index] in green_letters or word[index] not in grey_letters
                for index, green_letters in enumerate(self._letters_to_remember_at)
            )
        )
        return WordsRepository(words_to_remember, self._letters_to_remember_at)

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
        return WordsRepository(new_set_of_words, self._letters_to_remember_at)

    def remember_at(self, current_word: str, at_positions: list[int]) -> "WordsRepository":
        new_set_of_words = tuple(
            word
            for word in self._words
            if all(
                word[position] == current_word[position]
                for position in at_positions
            )
        )
        new_letters_to_remember_at = tuple(
            letters + current_word[letter_index] if letter_index in at_positions else letters
            for letter_index, letters
            in enumerate(self._letters_to_remember_at)
        )
        return WordsRepository(new_set_of_words, new_letters_to_remember_at)  # type: ignore

    def forget_word(self, word_to_forget: str):
        word_to_forget = word_to_forget.lower()
        new_set_of_words = tuple(
            word
            for word in self._words
            if word != word_to_forget
        )
        return WordsRepository(new_set_of_words, self._letters_to_remember_at)
