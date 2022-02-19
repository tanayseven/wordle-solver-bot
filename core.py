import json
from collections import namedtuple
from pathlib import Path
from random import randrange
from typing import Final, Literal

ColorRGB = namedtuple("ColorRGB", ["r", "g", "b"])
grey: Final[ColorRGB] = ColorRGB(124, 120, 126)
white: Final[ColorRGB] = ColorRGB(255, 255, 255)
green: Final[ColorRGB] = ColorRGB(170, 106, 100)
yellow: Final[ColorRGB] = ColorRGB(180, 201, 88)
ColorName = Literal["grey", "green", "yellow", "white"]
color_map: Final[dict[ColorRGB, ColorName]] = {
    grey: "grey",
    green: "green",
    yellow: "yellow",
    white: "white",
}


class WordsRepository:
    def __init__(
        self,
        words: tuple[str, ...] = None,
        letters_to_remember_at: tuple[str, str, str, str, str] = ("", "", "", "", ""),
    ):
        self._words: Final[tuple[str]] = (
            json.loads(Path("words_dictionary.json").read_text())
            if words is None
            else words
        )
        self._letters_to_remember_at: tuple[
            str, str, str, str, str
        ] = letters_to_remember_at

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

    def remember_not_at(
        self, current_word: str, at_positions: list[int]
    ) -> "WordsRepository":
        new_set_of_words = tuple(
            word
            for word in self._words
            if all(
                word[position] != current_word[position]
                and current_word[position] in word
                for position in at_positions
            )
        )
        return WordsRepository(new_set_of_words, self._letters_to_remember_at)

    def remember_at(
        self, current_word: str, at_positions: list[int]
    ) -> "WordsRepository":
        new_set_of_words = tuple(
            word
            for word in self._words
            if all(
                word[position] == current_word[position] for position in at_positions
            )
        )
        new_letters_to_remember_at = tuple(
            letters + current_word[letter_index]
            if letter_index in at_positions
            else letters
            for letter_index, letters in enumerate(self._letters_to_remember_at)
        )
        return WordsRepository(new_set_of_words, new_letters_to_remember_at)  # type: ignore

    def forget_word(self, word_to_forget: str):
        word_to_forget = word_to_forget.lower()
        new_set_of_words = tuple(word for word in self._words if word != word_to_forget)
        return WordsRepository(new_set_of_words, self._letters_to_remember_at)


class WordleSolver:
    def __init__(
        self, words_repo: WordsRepository, current_row: int = 0, current_word=""
    ):
        self._words_repo: Final[WordsRepository] = words_repo
        self._current_row: Final[int] = current_row
        self._current_word: Final[str] = current_word

    @property
    def current_row(self) -> int:
        return self._current_row

    @property
    def current_word(self) -> str:
        return self._current_word

    @property
    def remaining_words_in_memory(self) -> tuple[str]:
        return self._words_repo.remaining_words

    def get_random_word(self) -> "WordleSolver":
        new_current_word = self._words_repo.remaining_words[
            randrange(0, len(self._words_repo.remaining_words))
        ]
        return WordleSolver(
            self._words_repo.forget_word(new_current_word),
            self._current_row,
            new_current_word,
        )

    def reset_row(self) -> "WordleSolver":
        return WordleSolver(
            self._words_repo,
            0,
            self.current_word,
        )

    def highlighted_for_current_word(
        self, yellow_letters: list[int], green_letters: list[int], grey_letters: str
    ) -> "WordleSolver":
        words_repo = self._words_repo
        words_repo = words_repo.remember_at(self.current_word, green_letters)
        words_repo = words_repo.remember_not_at(self.current_word, yellow_letters)
        new_words_repo = words_repo.forget(grey_letters)
        new_words_repo = new_words_repo.forget_word(self._current_word)
        return WordleSolver(
            new_words_repo,
            self._current_row + 1,
            "",
        )
