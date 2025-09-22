#!/usr/bin/env python3
import argparse
import csv
import sys
import time


class SpellCorrector:
    def __init__(self, path_to_dataset) -> None:
        self.word_frequencies = self.load_data(path_to_dataset)
        if not self.word_frequencies:
            raise FileNotFoundError(f"The file {path_to_dataset} not found")

    def load_data(self, file):
        wordFreq = {}
        try:
            with open(file, newline="") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    wordFreq[row["word"].lower()] = int(row["count"])

            return wordFreq
        except FileNotFoundError:
            return None

    def contains(self, word):
        return word in self.word_frequencies

    def generate_edits(self, word):
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

    def find_correct_spelling(self, word):
        if self.contains(word):
            return word

        likely = self.generate_edits(word)

        known_words1 = set()
        for candidate in likely:
            if self.contains(candidate):
                known_words1.add(candidate)

        if known_words1:
            return max(known_words1, key=self.word_frequencies.get)

        known_words2 = set(
            e2 for e1 in likely for e2 in self.generate_edits(e1) if self.contains(e2)
        )

        if known_words2:
            return max(known_words2, key=self.word_frequencies.get)
        return None


def main():
    parser = argparse.ArgumentParser(description="Suggest correct spelling")
    parser.add_argument("words", nargs="+", help="One or more words to spell check")
    parser.add_argument(
        "-b",
        "--benchmark",
        action="store_true",
        help="Run benchmark and print timing info",
    )

    args = parser.parse_args()
    words_to_check = args.words

    spell_correcter = SpellCorrector("unigram_freq.csv")

    if args.benchmark:
        start_time = time.perf_counter()

    for word in words_to_check:
        correct = spell_correcter.find_correct_spelling(word.lower())
        if correct is None:
            correct = word
        print(f"{word} {correct}")

    if args.benchmark:
        end_time = time.perf_counter()
        total_time_sec = end_time - start_time
        total_time_ms = total_time_sec * 1000
        num_words = len(args.words)
        words_per_sec = num_words / total_time_sec if total_time_sec > 0 else 0

        print(f"Time : {total_time_ms:.6f}ms {words_per_sec:.1f} words per second")


if __name__ == "__main__":
    main()
