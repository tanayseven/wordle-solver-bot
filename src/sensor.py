import logging
import time
from typing import Tuple, Final, Any

import cv2  # type: ignore
import numpy as np
from PIL import Image, ImageGrab  # type: ignore

from image_objects import objects_root, blank_grid_png, share_button_png, close_modal_png, wordle_title_png
from screen_stuff import screen_shot_location

screen_area: Final = (0, 0, 1300, 2000)
CellBounds = list[tuple[tuple[Any, Any], tuple[Any, Any]]]
RowWithCellBounds = tuple[CellBounds, CellBounds, CellBounds, CellBounds, CellBounds]


def take_a_screenshot(area: Tuple[int, int, int, int] = screen_area) -> Image:
    screenshot = ImageGrab.grab(area)
    screenshot.save(screen_shot_location(), bitmap_format="png")
    return screenshot


def is_object_spotted(close_modal_: np.ndarray) -> bool:
    take_a_screenshot()
    screenshot = cv2.imread(screen_shot_location(), cv2.IMREAD_UNCHANGED)
    result = cv2.matchTemplate(screenshot, close_modal_, cv2.TM_CCOEFF_NORMED)
    threshold = .90
    yloc, xloc = np.where(result >= threshold)
    if len(xloc) == 0 or len(yloc) == 0:
        return False
    return True


def is_area_changed(area: Tuple[int, int, int, int], time_period: float, threshold_: float):
    take_a_screenshot(area)
    old_frame = cv2.imread(screen_shot_location(), cv2.IMREAD_UNCHANGED)
    time.sleep(time_period)
    take_a_screenshot(area)
    new_frame = cv2.imread(screen_shot_location(), cv2.IMREAD_UNCHANGED)
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


def closable_modal_is_open() -> bool:
    logging.info("Checking if closable modal is open")
    close_modal_ = cv2.imread(f"{objects_root / close_modal_png}", cv2.IMREAD_UNCHANGED)
    return is_object_spotted(close_modal_)


def winner_modal_is_open() -> bool:
    logging.info("Checking if winner modal is open")
    close_modal_ = cv2.imread(f"{objects_root / share_button_png}", cv2.IMREAD_UNCHANGED)
    return is_object_spotted(close_modal_)


def check_if_game_has_started() -> bool:
    logging.info("Checking if game has started")
    wordle_title = cv2.imread(f"{objects_root / wordle_title_png}", cv2.IMREAD_UNCHANGED)
    tries = 100
    for _ in range(tries):
        if is_object_spotted(wordle_title):
            return True
    return False


def partition_the_grid() -> tuple[
    CellBounds,
    CellBounds,
    CellBounds,
    CellBounds,
    CellBounds,
    CellBounds,
]:
    take_a_screenshot()
    screen_shot = cv2.imread(screen_shot_location(), cv2.IMREAD_UNCHANGED)
    grid_cell = cv2.imread(f"{objects_root / blank_grid_png}", cv2.IMREAD_UNCHANGED)
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
    return images[0:5], images[5:10], images[10:15], images[15:20], images[20:25], images[25:30]
