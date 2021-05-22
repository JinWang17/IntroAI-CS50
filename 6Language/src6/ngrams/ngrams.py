from collections import Counter

import math
import nltk
import os
import sys


def main():
    """Calculate top term frequencies for a corpus of documents."""

    if len(sys.argv) != 3:
        sys.exit("Usage: python tfidf.py n corpus")
    print("Loading data...")

    nlist = sys.argv[1]
    
    corpus = load_data(sys.argv[2])

    for n in nlist.split(sep = ","):
        n = int(n)
        # Compute n-grams
        ngrams = Counter(nltk.ngrams(corpus, n))

        # Print most common n-grams
        for ngram, freq in ngrams.most_common(10):
            print(f"{freq}: {ngram}")


def load_data(directory):
    contents = []

    # Read all files and extract words
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            with open(os.path.join(directory, filename)) as f:
                contents.extend([
                    word.lower() for word in
                    nltk.word_tokenize(f.read())
                    if any(c.isalpha() for c in word) and word.lower() not in nltk.corpus.stopwords.words("english")
                ])
    return contents


if __name__ == "__main__":
    main()
