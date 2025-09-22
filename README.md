# Spell Checker

A command-line tool to find the correct spelling of a word.

## Description

This spell checker takes one or more words as input and suggests the most likely correct spelling based on a frequency dictionary. The tool generates edits of distance 1 and 2 to find the correct spelling.

## Features

- Suggests correct spelling for misspelled words.
- Handles multiple words as input.
- Calculates and displays the time taken and words per second.

## Requirements

- Python 3

## Usage

To use the spell checker, run the following command:

```bash
python3 spell_checker.py <word1> <word2> ...
```

To benchmark the spell checker, use the `-b` or `--benchmark` flag:

```bash
python3 spell_checker.py -b <word1> <word2> ...
```

### Example

Without benchmark:

```bash
python3 spell_checker.py speling corect
```

Output:

```
speling spelling
corect correct
```

With benchmark:

```bash
python3 spell_checker.py -b speling corect
```

Output:

```
speling spelling
corect correct
Time : 1.234567ms 1.6 words per second
```

## Data

The spell checker uses `unigram_freq.csv` as the frequency dictionary. This file is from [Kaggle](https://www.kaggle.com/datasets/rtatman/english-word-frequency?resource=download).

## Algorithm

The spell-checking algorithm is based on the following steps:

1.  **Load Data:** The frequency dictionary is loaded from `unigram_freq.csv`.
2.  **Check if the word is in the dictionary:** If the word is already in the dictionary, it is considered correct.
3.  **Generate Edits (Distance 1):** If the word is not in the dictionary, the tool generates a set of all possible words at an edit distance of 1. The edits include:
    - **Deletes:** Removing a single character.
    - **Swaps:** Swapping two adjacent characters.
    - **Replaces:** Replacing a single character with another.
    - **Inserts:** Inserting a single character.
4.  **Find Known Words (Distance 1):** The generated edits are checked against the frequency dictionary to find known words. The most frequent word is returned as the suggestion.
5.  **Generate Edits (Distance 2):** If no known words are found at a distance of 1, the tool generates a set of all possible words at an edit distance of 2.
6.  **Find Known Words (Distance 2):** The generated edits are checked against the frequency dictionary to find known words. The most frequent word is returned as the suggestion.
7.  **No Suggestion:** If no known words are found at a distance of 1 or 2, the original word is returned.

## Going Further

- Use a Bloom filter to speed up determining if a word is in the list of known words.

- Spelling correction without a word frequency table, i.e. using trigrams.

- Spelling correction using phonetic similarity.

- Spelling correction using context (i.e. the surrounding words).

## Inspiration

[Coding Challenges](https://codingchallenges.fyi/)
