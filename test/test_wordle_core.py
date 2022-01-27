from core import WordsRepository


# TODO: Parameterize this test
def test_forget_letters():
    word_solver = WordsRepository(("cat", "dog", "bat", "mat"))
    new_word_solver = word_solver.forget("CB")
    assert len(new_word_solver.remaining_words) == 2
    assert "dog" in new_word_solver.remaining_words
    assert "mat" in new_word_solver.remaining_words


def test_forget_letters_given_no_letters():
    words = ("cat", "dog", "bat", "mat")
    word_solver = WordsRepository(words)
    new_word_solver = word_solver.forget("")
    assert len(new_word_solver.remaining_words) == 4
    assert set(words) == set(new_word_solver.remaining_words)


# TODO: Parameterize this test
def test_remember_letter():
    word_solver = WordsRepository(("cat", "dog", "bat", "tom"))
    new_word_solver = word_solver.remember_at(letter="A", at_position=1)
    assert len(new_word_solver.remaining_words) == 2
    assert "cat" in new_word_solver.remaining_words
    assert "bat" in new_word_solver.remaining_words


def test_remember_letter_better():
    word_solver = WordsRepository(("cat", "dog", "bat", "tom"))
    new_word_solver = word_solver.remember_not_at(current_word="O", at_position=0)
    new_word_solver = new_word_solver.remember_not_at(current_word="G", at_position=1)
    assert len(new_word_solver.remaining_words) == 1
    assert "dog" in new_word_solver.remaining_words


def test_remember_letter_given_no_letters():
    words = ("cat", "dog", "bat", "tom")
    word_solver = WordsRepository(words)
    new_word_solver = word_solver.remember_not_at(current_word="", at_position=0)
    assert len(new_word_solver.remaining_words) == 4
    assert set(words) == set(new_word_solver.remaining_words)


def test_already_remembered_letters_cant_be_forgotten():
    words = ("cat", "dog", "bat", "tom")
    word_solver = WordsRepository(words)
    new_word_solver = word_solver.remember_not_at(current_word="c", at_position=1)
    new_word_solver = new_word_solver.remember_at(letter="a", at_position=1)
    new_word_solver = new_word_solver.forget(grey_letters="ao")
    assert len(new_word_solver.remaining_words) == 4
    assert set(words) == set(new_word_solver.remaining_words)


# TODO: Parameterize this test
def test_remember_letter_at_location():
    word_solver = WordsRepository(("cat", "dog", "bat", "blah", "move"))
    new_word_solver = word_solver.remember_at(letter="A", at_position=1)
    assert len(new_word_solver.remaining_words) == 2
    assert "cat" in new_word_solver.remaining_words
    assert "bat" in new_word_solver.remaining_words


# TODO: Parameterize this test
def test_forget_word():
    given_words = ("cat", "dog", "bat", "blah", "move")
    expected_words = ("cat", "dog", "bat", "move")
    word_solver = WordsRepository(given_words)
    new_word_solver = word_solver.forget_word("blah")
    assert set(expected_words) == set(new_word_solver.remaining_words)
