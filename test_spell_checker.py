import pytest

from spell_checker import find_correct_spelling, load_data


# A pytest "fixture" provides a consistent, reusable setup for your tests.
# This creates a sample dictionary that all tests can use, so we don't
# need to rely on an external CSV file.
@pytest.fixture
def word_freq_dict():
    """Provides a sample word frequency dictionary for testing."""
    return {
        "spelling": 100,
        "correct": 90,
        "word": 80,
        "checker": 70,
        "accept": 60,  # Higher frequency
        "except": 50,  # Lower frequency
    }


# --- Tests for find_correct_spelling ---


def test_correctly_spelled_word(word_freq_dict):
    """Tests that a word already in the dictionary is returned as is."""
    assert find_correct_spelling("correct", word_freq_dict) == "correct"


def test_correction_with_one_deletion(word_freq_dict):
    """Tests a word that needs one character deleted."""
    assert find_correct_spelling("speling", word_freq_dict) == "spelling"


def test_correction_with_one_swap(word_freq_dict):
    """Tests a word that needs two adjacent characters swapped."""
    assert find_correct_spelling("spellign", word_freq_dict) == "spelling"


def test_correction_with_one_replacement(word_freq_dict):
    """Tests a word that needs one character replaced."""
    assert find_correct_spelling("spelleng", word_freq_dict) == "spelling"


def test_correction_with_one_insertion(word_freq_dict):
    """Tests a word that has one extra character."""
    assert find_correct_spelling("wword", word_freq_dict) == "word"


def test_correction_with_edit_distance_two(word_freq_dict):
    """Tests a word that is two edits away from a correct word."""
    # "corect" -> "correct" (one insertion)
    # "chekcer" -> "checker" (one deletion)
    assert find_correct_spelling("corect", word_freq_dict) == "correct"
    assert find_correct_spelling("chekcer", word_freq_dict) == "checker"


def test_chooses_higher_frequency_word(word_freq_dict):
    """
    Tests that when a word can be corrected to multiple valid words,
    the one with the highest frequency is chosen.
    "acept" -> "accept" (60) or "except" (50)
    """
    assert find_correct_spelling("acept", word_freq_dict) == "accept"


def test_no_correction_found(word_freq_dict):
    """Tests that a word with no possible correction returns None."""
    assert find_correct_spelling("xyzabcfgu", word_freq_dict) is None


def test_case_insensitivity_handled_by_caller(word_freq_dict):
    """
    Tests that the function works as expected when the input is pre-lowercased,
    mimicking the behavior in your main() function.
    """
    assert find_correct_spelling("CORRECT".lower(), word_freq_dict) == "correct"


# --- Tests for load_data ---


def test_load_data_success(tmp_path):
    """
    Tests that load_data correctly reads a CSV and creates a dictionary.
    'tmp_path' is a pytest fixture that creates a temporary directory.
    """
    # Create a temporary CSV file for the test
    csv_file = tmp_path / "test_freq.csv"
    csv_file.write_text("word,count\nhello,10\nWORLD,20\n")

    # Call the function with the temporary file
    expected_dict = {"hello": 10, "world": 20}
    assert load_data(csv_file) == expected_dict


def test_load_data_file_not_found(capsys):
    """
    Tests the function's behavior when the file doesn't exist.
    'capsys' is a pytest fixture that captures output printed to the console.
    """
    # Attempt to load a non-existent file
    result = load_data("non_existent_file.csv")

    # Check that the function returns None or an empty dict on failure
    assert result is None or result == {}

    # Check that the correct error message was printed to the console
    captured = capsys.readouterr()
    assert "Error: non_existent_file.csv not found" in captured.out
