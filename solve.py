import datetime
import logging
import os
import signal
import subprocess
import time
from contextlib import contextmanager
from pathlib import Path
from typing import Tuple, Final, Any, List

import cv2  # type: ignore
import numpy as np
import pyautogui  # type: ignore
from PIL import ImageGrab, Image  # type: ignore
from pyperclip import paste  # type: ignore
from termcolor import colored  # type: ignore

from core import WordsRepository, WordleSolver, white, green, color_map, ColorRGB, ColorName


CellBounds = list[tuple[tuple[Any, Any], tuple[Any, Any]]]
RowWithCellBounds = tuple[CellBounds, CellBounds, CellBounds, CellBounds, CellBounds]


def enter_a_word(word: str):
    logging.info(f"Entering word: {word}")
    pyautogui.typewrite(word, interval=0.01)
    pyautogui.press("enter")


screen_area: Final = (0, 0, 1300, 2000)
screen_shot_location: Final = "screen-shot.png"


def take_a_screenshot(area: Tuple[int, int, int, int] = screen_area) -> Image:
    screenshot = ImageGrab.grab(area)
    screenshot.save(Path(screen_shot_location), bitmap_format="png")
    return screenshot


@contextmanager
def opened_browser(on_date: datetime.date):
    browser_process = subprocess.Popen(
        ["faketime", f"{on_date.isoformat()}", "chromium", "https://www.powerlanguage.co.uk/wordle/",
         "--window-size=700,1000",
         "--window-position=0,0", "--new-window", "--incognito",
         ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.STDOUT,
        preexec_fn=os.setsid,
    )
    yield
    os.killpg(os.getpgid(browser_process.pid), signal.SIGKILL)


def closable_modal_is_open() -> bool:
    logging.info("Checking if closable modal is open")
    close_modal_ = cv2.imread("objects/close-modal.png", cv2.IMREAD_UNCHANGED)
    return is_object_spotted(close_modal_)


def check_if_game_has_started() -> bool:
    logging.info("Checking if game has started")
    wordle_title = cv2.imread("objects/wordle_title.png", cv2.IMREAD_UNCHANGED)
    tries = 100
    for _ in range(tries):
        if is_object_spotted(wordle_title):
            return True
    return False


def is_object_spotted(close_modal_: np.ndarray) -> bool:
    take_a_screenshot()
    screenshot = cv2.imread(screen_shot_location, cv2.IMREAD_UNCHANGED)
    result = cv2.matchTemplate(screenshot, close_modal_, cv2.TM_CCOEFF_NORMED)
    threshold = .90
    yloc, xloc = np.where(result >= threshold)
    if len(xloc) == 0 or len(yloc) == 0:
        return False
    return True


def close_modal():
    logging.info("Closing the modal")
    close_modal_ = cv2.imread("objects/close-modal.png", cv2.IMREAD_UNCHANGED)
    take_a_screenshot()
    screenshot = cv2.imread(screen_shot_location, cv2.IMREAD_UNCHANGED)
    result = cv2.matchTemplate(screenshot, close_modal_, cv2.TM_CCOEFF_NORMED)
    _, __, ___, max_loc = cv2.minMaxLoc(result)
    click_location = (
        max_loc[0] + close_modal_.shape[0] / 2,
        max_loc[1] + close_modal_.shape[1] / 2,
    )
    pyautogui.click(x=click_location[0], y=click_location[1], interval=0.5)


def is_area_changed(area: Tuple[int, int, int, int], time_period: float, threshold_: float):
    take_a_screenshot(area)
    old_frame = cv2.imread(screen_shot_location, cv2.IMREAD_UNCHANGED)
    time.sleep(time_period)
    take_a_screenshot(area)
    new_frame = cv2.imread(screen_shot_location, cv2.IMREAD_UNCHANGED)
    difference = cv2.subtract(old_frame, new_frame)
    return threshold_ < np.average(difference)


def wait_till_animation_end(checks=1):
    no_changes = 0
    while True:
        if not is_area_changed(screen_area, 0.1, 0.4):
            no_changes += 1
        if no_changes > checks:
            break
        time.sleep(0.1)


def move_mouse(edges: Tuple[int, int, int, int], duration: float = 0.5):
    logging.info("Moving the mouse")
    pyautogui.moveTo(x=edges[0], y=edges[1])
    pyautogui.moveTo(x=edges[2], y=edges[3], duration=duration)


def partition_the_grid() -> tuple[
    CellBounds,
    CellBounds,
    CellBounds,
    CellBounds,
    CellBounds,
    CellBounds,
]:
    take_a_screenshot()
    screen_shot = cv2.imread("screen-shot.png", cv2.IMREAD_UNCHANGED)
    grid_cell = cv2.imread("objects/blank_grid.png", cv2.IMREAD_UNCHANGED)
    res = cv2.matchTemplate(screen_shot, grid_cell, cv2.TM_CCOEFF_NORMED)
    threshold: Final = 0.8
    loc = np.where(res >= threshold)
    w, h = grid_cell.shape[:2]
    mask = np.zeros(screen_shot.shape[:2], np.uint8)
    images = []
    for pt in zip(*loc[::-1]):
        if mask[pt[1] + int(round(h / 2)), pt[0] + int(round(w / 2))] != 255:
            mask[pt[1]:pt[1] + h, pt[0]:pt[0] + w] = 255
            images.append(((pt[1], pt[1] + h), (pt[0], pt[0] + w)))
            cv2.rectangle(screen_shot, pt, (pt[0] + w, pt[1] + h), (0, 255, 0), 1)
    cv2.imwrite("marked_screenshot.png", screen_shot)
    return images[0:5], images[5:10], images[10:15], images[15:20], images[20:25], images[25:30]


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


def all_white_cells(colors_):
    for color in colors_:
        if not np.array_equal(color, np.array(white)):
            return False
    return True


def all_green_cells(colors_):
    for color in colors_:
        if not np.array_equal(color, np.array(green)):
            return False
    return True


def color_squares(colors_):
    result = ""
    for color in colors_:
        color_tuple = tuple(elem for elem in color)
        result += colored(' ■', color_map[color_tuple])  # type: ignore
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


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format="[⌚ %(asctime)s] Wordle Bot: \"%(message)s\"")
    logging.info(f"Opening browser: {datetime.date.today().isoformat()}")
    with opened_browser(datetime.date.today()):
        wordle_solver = WordleSolver(WordsRepository())
        check_if_game_has_started()
        wait_till_animation_end()
        if closable_modal_is_open():
            close_modal()
        wait_till_animation_end()
        partitions = partition_the_grid()
        while True:
            logging.info(f"I have {len(wordle_solver.remaining_words_in_memory)} words in my memory 🧠")
            if len(wordle_solver.remaining_words_in_memory) == 0:
                logging.info(f"I don't know the word the game wants me to guess 😞")
                break
            if wordle_solver.current_row == 6:
                logging.info("Looks like I used up all the attempts 😞")
                break
            wordle_solver = wordle_solver.get_random_word()
            wait_till_animation_end()
            enter_a_word(wordle_solver.current_word.upper())
            wait_till_animation_end(checks=2)
            colors = letter_colours(partitions[wordle_solver.current_row], wordle_solver.current_row)
            if all_white_cells(colors):
                logging.info("Looks like the game does not know this word 🤷‍")
                for _ in range(5):
                    pyautogui.press("backspace")
            elif all_green_cells(colors):
                logging.info("Looks like I won the game 🙋")
                break
            else:
                logging.info(f"I see the colors 👀{color_squares(colors)}")
                yellow_letters = fetch_yellow_words(wordle_solver.current_word, color_names(colors))
                green_letters = fetch_green_words(wordle_solver.current_word, color_names(colors))
                grey_letters = fetch_grey_words(wordle_solver.current_word, color_names(colors))
                cleaned_grey_words = eliminate_greys_having_green_and_yellow(
                    grey_letters,
                    wordle_solver.current_word,
                    green_letters,
                    yellow_letters
                )
                wordle_solver = wordle_solver.highlighted_for_current_word(
                    yellow_letters=yellow_letters,
                    green_letters=green_letters,
                    grey_letters=cleaned_grey_words,
                )
                logging.info(f"I'm forgetting the non-needed words from my memory 🧠")
        clipped = paste()
        Path("solved.txt").write_text(clipped)
        logging.info(f"I'm closing the browser now")
