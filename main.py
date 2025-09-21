import csv
import re

wordFreq = {}
try:
    with open("unigram_freq.csv", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            wordFreq[row["word"]] = int(row["count"])
except FileNotFoundError:
    print("Error: unigram_freq.csv not found")


def contains(word):
    if word.lower() in wordFreq:
        return True
    else:
        return False


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


def find_correct_spelling(word):
    if contains(word):
        return word

    word = word.lower()

    likely = generate_edits(word)

    known_words1 = set()
    for word in likely:
        if contains(word):
            known_words1.add(word)

    if known_words1:
        return max(known_words1, key=wordFreq.get)

    likely2 = set()
    for word in likely:
        likely2.update(generate_edits(word))

    known_words2 = set()
    for word in likely2:
        if contains(word):
            known_words2.add(word)

    if known_words2:
        return max(known_words2, key=wordFreq.get)
    return None


print(find_correct_spelling("Dreem"))
