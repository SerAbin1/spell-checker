#!/usr/bin/env python3

import argparse
import csv
import sys
import time


def load_data(file):
    wordFreq = {}
    try:
        with open(file, newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                wordFreq[row["word"]] = int(row["count"])

        return wordFreq
    except FileNotFoundError:
        print("Error: unigram_freq.csv not found")


def contains(word, wordFreq):
    return word.lower() in wordFreq


def generate_edits(word):
    letters = "abcdefghijklmnopqrstuvwxyz"

    # create all possible combination of words (("", cat), (c, at), (ca, t), (cat, ""))
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]

    # delete a char (from right split)
    deletes = set()
    for left, right in splits:
        if right:
            deletes.add(left + right[1:])

    # swap two adjacent letters
    swaps = set()
    for left, right in splits:
        if len(right) > 1:
            swaps.add(left + right[1] + right[0] + right[2:])

    # replace a letter with each letter in alphabet
    replaces = set()
    for left, right in splits:
        if right:
            for char in letters:
                replaces.add(left + char + right[1:])

    # insert a letter at every position
    inserts = set()
    for left, right in splits:
        for char in letters:
            inserts.add(left + char + right)

    # Return a union of all sets
    return deletes.union(swaps, replaces, inserts)


def find_correct_spelling(word, wordFreq):
    if contains(word, wordFreq):
        return word

    word = word.lower()

    likely = generate_edits(word)

    known_words1 = set()
    for candidate in likely:
        if contains(candidate, wordFreq):
            known_words1.add(candidate)

    if known_words1:
        return max(known_words1, key=wordFreq.get)

    likely2 = set()
    for candidate in likely:
        likely2.update(generate_edits(candidate))

    known_words2 = set()
    for candidate in likely2:
        if contains(candidate, wordFreq):
            known_words2.add(candidate)

    if known_words2:
        return max(known_words2, key=wordFreq.get)
    return None


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Suggest correct spelling")
    parser.add_argument("words", nargs="+", help="One or more words to spell check")

    args = parser.parse_args()

    wordFrequencies = load_data("unigram_freq.csv")
    if not wordFrequencies:
        sys.exit(1)

    start_time = time.perf_counter()

    for word in args.words:
        correct = find_correct_spelling(word, wordFrequencies)
        if correct is None:
            correct = word
        print(f"{word} {correct}")

    end_time = time.perf_counter()
    total_time_sec = end_time - start_time
    total_time_ms = total_time_sec * 1000
    num_words = len(args.words)
    words_per_sec = num_words / total_time_sec if total_time_sec > 0 else 0

    print(f"Time : {total_time_ms:.6f}ms {words_per_sec:.1f} words per second")
