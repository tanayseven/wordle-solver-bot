from typing import Any

import cv2  # type: ignore
import numpy as np
from termcolor import colored  # type: ignore

from core import ColorRGB, white, green, color_map, ColorName
from sensor import take_a_screenshot


CellBounds = list[tuple[tuple[Any, Any], tuple[Any, Any]]]
RowWithCellBounds = tuple[CellBounds, CellBounds, CellBounds, CellBounds, CellBounds]


def letter_colours(row: CellBounds, number=0) -> list[ColorRGB]:
    take_a_screenshot()
    screen_shot = cv2.imread("screen-shot.png", cv2.IMREAD_UNCHANGED)
    grid_colours: list[ColorRGB] = []
    for i, ((x1, y1), (x2, y2)) in enumerate(row):
        grid_cell = screen_shot[x1:y1, x2:y2]
        colors_, count = np.unique(grid_cell.reshape(-1, 4), axis=0, return_counts=True)
        rgb_tuple = colors_[count.argmax()][:3]
        grid_colours.append(ColorRGB(rgb_tuple[0], rgb_tuple[1], rgb_tuple[2]))
        cv2.imwrite(f"grid/{i}-{number}.png", grid_cell)
    return grid_colours


def all_white_cells(colors_: list[ColorRGB]) -> bool:
    for color in colors_:
        if not np.array_equal(color, np.array(white)):
            return False
    return True


def all_green_cells(colors_: list[ColorRGB]) -> bool:
    for color in colors_:
        if not np.array_equal(color, np.array(green)):
            return False
    return True


def color_squares(colors_: list[ColorRGB], word: str) -> str:
    result = ""
    for i, color in enumerate(colors_):
        result += colored(f' {word[i].upper()} ', "white", f"on_{color_map[color]}")
    return result


def color_names(colors_: list[ColorRGB]) -> list[ColorName]:
    result = []
    for color in colors_:
        result.append(color_map[color])
    return result


def fetch_grey_words(word_: str, colors_: list[ColorName]) -> str:
    letters = ""
    for i, _ in enumerate(word_):
        if colors_[i] == "grey":
            letters += word_[i]
    return letters


def fetch_green_words(word_: str, colors_: list[ColorName]) -> list[int]:
    letters = []
    for i, _ in enumerate(word_):
        if colors_[i] == "green":
            letters.append(i)
    return letters


def fetch_yellow_words(word_: str, colors_: list[ColorName]) -> list[int]:
    letters = []
    for i, _ in enumerate(word_):
        if colors_[i] == "yellow":
            letters.append(i)
    return letters


def eliminate_greys_having_green_and_yellow(
        grey_letters_: str,
        current_word: str,
        green_words_indexes: list[int],
        yellow_words_indexes: list[int],
):
    green_letters_ = str([current_word[index] for index in green_words_indexes])
    yellow_letters_ = str([current_word[index] for index in yellow_words_indexes])
    return str([
        letter for letter in grey_letters_
        if letter not in green_letters_ and letter not in yellow_letters_
    ])