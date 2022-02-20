import pytest

from core import WordsRepository


@pytest.mark.parametrize(
    "input_words,forget_letters,remaining_words",
    [
        ("urger,ribat,anorn,stram,sofar", "ugo", "ribat,stram")
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
        "urger,ribat,anorn,stram,sofar"
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
        ("uhuru,morro,frory,fjord", ([3], [], [0], [2]), "fjord,frory")
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
        ("saury,kebab,tunic,hepar,quiff", ([2], [], [3], [], []), "quiff")
    ]
)
def test_remember_letter_better(input_words, not_at_position, remaining_words):
    input_words = tuple(input_words.split(','))
    word_solver = WordsRepository(input_words)
    remaining_words = remaining_words.split(",")
    for current_word, position in zip(input_words, not_at_position):
        word_solver = word_solver.remember_not_at(current_word, position)
    assert set(word_solver.remaining_words) == set(remaining_words)


# fmt: on
@pytest.mark.parametrize(
    "input_words,not_at_positions,at_positions,to_forget,remaining_words",
    [
        ("leese,tunic,benab", ([], []), ([1], []), ("e", "i"), "leese,benab")
    ]
)
# fmt: off
def test_already_remembered_letters_cant_be_forgotten(
        input_words,
        not_at_positions,
        at_positions,
        to_forget,
        remaining_words,
):
    input_words = tuple(input_words.split(","))
    word_solver = WordsRepository(input_words)
    remaining_words = tuple(remaining_words.split(","))
    new_word_solver = word_solver
    for word, not_at, at, forget in zip(input_words, not_at_positions, at_positions, to_forget):
        new_word_solver = word_solver.remember_not_at(word, not_at)
        new_word_solver = new_word_solver.remember_at(word, at)
        new_word_solver = new_word_solver.forget(grey_letters=forget)
    assert set(remaining_words) == set(new_word_solver.remaining_words)


@pytest.mark.parametrize(
    "input_words,forget_words,remaining_words",
    [
        ("saury,kebab,tunic,hepar,quiff", "kebab,hepar,quiff", "saury,tunic")
    ]
)
def test_forget_word(input_words, forget_words, remaining_words):
    input_words = tuple(input_words.split(","))
    forget_words = tuple(forget_words.split(","))
    remaining_words = tuple(remaining_words.split(","))
    word_solver = WordsRepository(input_words)
    new_word_solver = word_solver
    for word in forget_words:
        new_word_solver = new_word_solver.forget_word(word)
    assert set(remaining_words) == set(new_word_solver.remaining_words)
