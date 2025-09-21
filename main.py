import csv

wordFreq = {}
try:
    with open("unigram_freq.csv", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            wordFreq[row["word"]] = int(row["count"])
except FileNotFoundError:
    print("Error: unigram_freq.csv not found")


def contains(word):
    if word in wordFreq:
        print("correctly spelled")
    else:
        print("not")


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


print(generate_edits("cat"))
