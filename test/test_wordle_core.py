from collections import namedtuple

import pytest

from core import WordsRepository


@pytest.mark.parametrize(
    "input_words,forget_letters,remaining_words",
    [
        ("URGER,RIBAT,ANORN,STRAM,SOFAR", "UGO", "RIBAT,STRAM")
    ]
)
def test_forget_letters(input_words, forget_letters, remaining_words):
    input_words = tuple(input_words.split(','))
    remaining_words = remaining_words.split(',')
    word_solver = WordsRepository(input_words)
    new_word_solver = word_solver.forget(forget_letters)
    assert set(new_word_solver.remaining_words) == set(remaining_words)


@pytest.mark.parametrize(
    "input_words",
    [
        "URGER,RIBAT,ANORN,STRAM,SOFAR"
    ]
)
def test_forget_letters_given_no_letters(input_words):
    input_words = tuple(input_words.split(','))
    word_solver = WordsRepository(input_words)
    new_word_solver = word_solver.forget("")
    assert set(new_word_solver.remaining_words) == set(input_words)


@pytest.mark.parametrize(
    "input_words,remember_positions,remaining_words",
    [
        ("UHURU,MORRO,FRORY,FJORD", ([3], [], [0], [2]), "FJORD,FRORY")
    ]
)
def test_remember_letter(input_words, remember_positions, remaining_words):
    input_words = tuple(input_words.split(','))
    word_solver = WordsRepository(input_words)
    remaining_words = remaining_words.split(",")
    for word, positions in zip(input_words, remember_positions):
        word_solver = word_solver.remember_at(current_word=word, at_positions=positions)
    assert set(word_solver.remaining_words) == set(remaining_words)


@pytest.mark.parametrize(
    "input_words,not_at_position,remaining_words",
    [
        ("SAURY,KEBAB,TUNIC,HEPAR,QUIFF", ([2], [], [3], [], []), "QUIFF")
    ]
)
def test_remember_letter_better(input_words, not_at_position, remaining_words):
    input_words = tuple(input_words.split(','))
    word_solver = WordsRepository(input_words)
    remaining_words = remaining_words.split(",")
    for current_word, position in zip(input_words, not_at_position):
        word_solver = word_solver.remember_not_at(current_word, position)
    assert set(word_solver.remaining_words) == set(remaining_words)


@pytest.mark.skip
def test_remember_letter_given_no_letters():
    words = ("cat", "dog", "bat", "tom")
    word_solver = WordsRepository(words)
    new_word_solver = word_solver.remember_not_at(current_word="", at_positions=[0])
    assert len(new_word_solver.remaining_words) == 4
    assert set(words) == set(new_word_solver.remaining_words)


@pytest.mark.skip
def test_already_remembered_letters_cant_be_forgotten():
    words = ("cat", "dog", "bat", "tom")
    word_solver = WordsRepository(words)
    new_word_solver = word_solver.remember_not_at(current_word="c", at_positions=[1])
    new_word_solver = new_word_solver.remember_at(current_word="a", at_positions=[1])
    new_word_solver = new_word_solver.forget(grey_letters="ao")
    assert len(new_word_solver.remaining_words) == 4
    assert set(words) == set(new_word_solver.remaining_words)


@pytest.mark.skip
def test_remember_letter_at_location():
    word_solver = WordsRepository(("cat", "dog", "bat", "blah", "move"))
    new_word_solver = word_solver.remember_at(current_word="A", at_positions=[1])
    assert len(new_word_solver.remaining_words) == 2
    assert "cat" in new_word_solver.remaining_words
    assert "bat" in new_word_solver.remaining_words


@pytest.mark.skip
def test_forget_word():
    given_words = ("cat", "dog", "bat", "blah", "move")
    expected_words = ("cat", "dog", "bat", "move")
    word_solver = WordsRepository(given_words)
    new_word_solver = word_solver.forget_word("blah")
    assert set(expected_words) == set(new_word_solver.remaining_words)
