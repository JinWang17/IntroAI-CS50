#!/usr/bin/env python
# coding: utf-8
import os
import random
import re
import sys
from collections import Counter
import numpy

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    # The keys in that dictionary represent pages (e.g., "2.html"), and the values of the dictionary are a set of all of the pages linked to by the key (e.g. {"1.html", "3.html"}).
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
            # If there is a link to wiki in page 1, but wiki is not in the corpse folder
            # then wiki will not be part of page 1's links. 
            # "We only rank what we know for sure.", said Jin.
        )

    return pages




def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    #print(corpus)
    result = dict()
    N = len(corpus)
    N_page = len(corpus[page])
    # ignore the link to its own page
    if page in corpus[page]:
        N_page -= 1

    # With prob = 1 - damping_factor, randomly choose from all pages
    for p in corpus:
        result[p] = 1 / N * (1 - damping_factor)
        
    # With prob = damping_factor, randomly choose from links
    for p in corpus[page]:
        if p == page:
            continue
        else:
            result[p] += 1 / N_page * damping_factor
        
    # Normalize for floating errors:
    factor=1.0/sum(result.values())
    for p in result:
        result[p] = result[p]*factor

    # The return value of the function should be a Python dictionary with one 
    # key for each page in the corpus. Each key should be mapped to a value 
    # representing the probability that a random surfer would choose that page next. 
    # The values in this returned probability distribution should sum to 1
    return result


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    
    samples = list()
    
    # First sample: choosing from a page at random.
    current = random.choice(list(corpus.keys()))
    
    # Next sample: generated from the previous sample based on the 
    # previous sample’s transition model.
    for i in range(n):
        trans = transition_model(corpus, current, damping_factor)
        current = random.choices(
            population = list(trans.keys()),
            weights = trans.values(),
            k = 1
        )[0]
        samples.append(current)     
        
    # Summary of samples    
    frequency = Counter(samples)
    for page in frequency:
        frequency[page] = frequency[page] / n      
    return frequency 


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    
    # Preprocessing
    N = len(corpus)
    numLinks = numpy.array([len(corpus[p]) for p in corpus], dtype=float)
    numLinks[numLinks == 0] = N
    prob = numpy.reciprocal(numLinks)
    binaryLinks = numpy.zeros((N, N))
    for i, p1 in enumerate(corpus.keys()):
        if not corpus[p1]:
        # A page that has no links at all should be interpreted 
        # as having one link for every page in the corpus (including itself).
            for j in range(N):
                binaryLinks[j, i] = 1
        else:
            for j, p2 in enumerate(corpus.keys()):
                if p2 in corpus[p1]:
                    # ignore the link to its own
                    binaryLinks[j, i] = 1
    
    # Start: 1 / N for every page
    current = numpy.ones(N) / N
    #print(current)
    
    # Repeatedly update rank values until no change in values > 0.001.
    difference = 1
    while difference > 0.001: 
        new = (1 - damping_factor) * numpy.ones(N) / N + \
          (damping_factor) * numpy.sum(binaryLinks * prob * current, axis = 1)
        difference = max(abs(current - new))
        current = new
    
    result = dict()
    for i, page in enumerate(corpus):
        result[page] = new[i]
    return result



if __name__ == "__main__":
    main()

