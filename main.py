import csv

wordFreq = {}
try:
    with open("unigram_freq.csv", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            wordFreq[row["word"]] = int(row["count"])
except FileNotFoundError:
    print("Error: unigram_freq.csv not found")
