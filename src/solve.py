import datetime
import logging
import os
import signal
import subprocess
import time
from contextlib import contextmanager
from pathlib import Path

import cv2  # type: ignore
import pyautogui  # type: ignore
import pyperclip  # type: ignore
from PIL import ImageGrab, Image  # type: ignore
from termcolor import colored  # type: ignore

from actuator import enter_a_word, close_modal, move_mouse, click_share_button
from color_stuff import letter_colours, all_white_cells, all_green_cells, color_squares, color_names, fetch_grey_words, \
    fetch_green_words, fetch_yellow_words, eliminate_greys_having_green_and_yellow
from core import WordsRepository, WordleSolver
from screen_stuff import new_working_directory_location
from sensor import wait_till_animation_end, closable_modal_is_open, \
    check_if_game_has_started, partition_the_grid, winner_modal_is_open


@contextmanager
def opened_browser(on_date: datetime.date):
    browser_process = subprocess.Popen(
        [
            "faketime",
            f"{on_date.isoformat()}",
            "chromium",
            "http://localhost:8000",
            "--window-size=700,1000",
            "--window-position=0,0",
            "--new-window",
            "--incognito",
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.STDOUT,
        preexec_fn=os.setsid,
    )
    wordle_server_process = subprocess.Popen(
        [
            "python",
            "-m",
            "http.server",
            "--directory",
            str(Path("../worlde_server_files").absolute()),
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.STDOUT,
        preexec_fn=os.setsid,
    )
    yield
    os.killpg(os.getpgid(browser_process.pid), signal.SIGKILL)
    os.killpg(os.getpgid(wordle_server_process.pid), signal.SIGKILL)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format="[⌚ %(asctime)s] Wordle Bot: \"%(message)s\"")
    date = datetime.date.fromisoformat("2021-10-01")
    one_day = datetime.timedelta(days=1)
    date -= one_day
    while date.isoformat() != "2022-02-31":
        date += one_day
        logging.info(f"Opening browser for date {date.isoformat()}")
        wordle_solver = WordleSolver(WordsRepository())
        game_won = False
        while not game_won:
            with opened_browser(date), new_working_directory_location():
                check_if_game_has_started()
                wait_till_animation_end()
                move_mouse((200, 200, 300, 300), 0.5)
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
                        wordle_solver.reset_row()
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
                        logging.info(f"I see the colors 👀{color_squares(colors, wordle_solver.current_word)}")
                        logging.info("Looks like I won the game 🙋")
                        move_mouse((200, 200, 300, 300), 0.5)
                        game_won = True
                        break
                    else:
                        logging.info(f"I see the colors 👀{color_squares(colors, wordle_solver.current_word)}")
                        yellow_letters = fetch_yellow_words(wordle_solver.current_word, color_names(colors))
                        green_letters = fetch_green_words(wordle_solver.current_word, color_names(colors))
                        grey_letters = fetch_grey_words(wordle_solver.current_word, color_names(colors))
                        cleaned_grey_words = eliminate_greys_having_green_and_yellow(
                            grey_letters,
                            wordle_solver.current_word,
                            green_letters,
                            yellow_letters,
                        )
                        wordle_solver = wordle_solver.highlighted_for_current_word(
                            yellow_letters=yellow_letters,
                            green_letters=green_letters,
                            grey_letters=cleaned_grey_words,
                        )
                        logging.info(f"I'm forgetting the non-needed words from my memory 🧠")
                wait_till_animation_end()
                if winner_modal_is_open():
                    click_share_button()
                    time.sleep(0.3)
        logging.info("Ended the game")
        pyautogui.click(x=1000, y=700, interval=0.5)
        if game_won:
            output = pyperclip.paste()
            logging.info(f"My winning details details \n {output}")
