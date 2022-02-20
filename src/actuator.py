import logging
from typing import Tuple

import cv2  # type: ignore
import pyautogui  # type: ignore
import numpy as np  # type: ignore

from screen_stuff import screen_shot_location
from sensor import take_a_screenshot


def enter_a_word(word: str):
    logging.info(f"Entering word: {word}")
    pyautogui.typewrite(word, interval=0.01)
    pyautogui.press("enter")


def close_modal():
    logging.info("Closing the modal")
    screen_object = cv2.imread("objects/close-modal.png", cv2.IMREAD_UNCHANGED)
    click_the_center_of(screen_object)


def click_share_button():
    logging.info("Clicking the share button")
    screen_object = cv2.imread("objects/share-button.png", cv2.IMREAD_UNCHANGED)
    click_the_center_of(screen_object)


def click_the_center_of(screen_object: np.ndarray):
    take_a_screenshot()
    screenshot = cv2.imread(screen_shot_location, cv2.IMREAD_UNCHANGED)
    result = cv2.matchTemplate(screenshot, screen_object, cv2.TM_CCOEFF_NORMED)
    _, __, ___, max_loc = cv2.minMaxLoc(result)
    click_location = (
        max_loc[0] + screen_object.shape[1] / 2,
        max_loc[1] + screen_object.shape[0] / 2,
    )
    pyautogui.click(x=click_location[0], y=click_location[1], interval=0.5)


def move_mouse(edges: Tuple[int, int, int, int], duration: float = 0.5):
    logging.info("Moving the mouse")
    pyautogui.moveTo(x=edges[0], y=edges[1])
    pyautogui.click(x=edges[0], y=edges[1])
    pyautogui.moveTo(x=edges[2], y=edges[3], duration=duration)
