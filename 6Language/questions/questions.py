import nltk
import sys
import os
import math
import string


FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    contents = dict()
    
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            with open(os.path.join(directory, filename), encoding="utf8") as f:
                #result = []
                #result.append([
                #    line
                #    for line in f.read().splitlines()
                #])
                #contents[filename] = result
                contents[filename] = f.read()
    
    return contents
        

def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    
    # Filter out punctuation and stopwords (common words that are unlikely to be useful for querying). 
    # Punctuation is defined as any character in string.punctuation (after you import string). 
    # Stopwords are defined as any word in nltk.corpus.stopwords.words("english").
    # If a word appears multiple times in the document, it should also appear multiple times in the returned list (unless it was filtered out).
    contents = []
    contents.extend([
        word.lower() for word in
        nltk.word_tokenize(document)
        if ((word.lower() not in nltk.corpus.stopwords.words("english")) and
            (word.lower() not in string.punctuation))
    ])
    return contents

def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    words = []
    for i in documents.values():
        words = words + list(i)
    
    # Calculate IDFs
    idfs = dict()
    for word in set(words):
        f = sum(word in documents[filename] for filename in documents)
        idf = math.log(len(documents) / f)
        idfs[word] = idf

    return idfs     

def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    # Calculate sum of TF-IDFs in each file
    sum_tfidfs = dict()
    for file in files:
        tfidfs = dict()
        # calculate the TF-IDF for each word in query 
        for word in query:
            # calculate frequency of word
            freq = files[file].count(word)
            tfidfs[word] = idfs[word] * freq
        
        sum_tfidfs[file] = sum(tfidfs.values())
    
    res = sorted(sum_tfidfs.items(), key = 
             lambda kv:kv[1], reverse = True)
    res_keys = [i[0] for i in res]
    return res_keys[:n]
    


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    # rule 1) rank by the matching word measure
    # matching word measure = sum of IDF for any word in the query that appears in the sentence
    # rule 2) if same matching word measure, sentences with a higher “query term density” are preferred
    # query term density = the proportion of words in the sentence that are also words in the query
    
    ranks = dict() # key: file=name; value=(matching word measure, term density)
    
    for s in sentences:
        density = 0
        matching = sum(idfs[word] for word in query if word in sentences[s])
        density = sum(sentences[s].count(word) for word in query) / len(s)
        
        ranks[s] = (matching, density)
    
    res = sorted(ranks.items(), key = 
             lambda kv:kv[1], reverse = True)
    res_keys = [i[0] for i in res]
    return res_keys[:n]

if __name__ == "__main__":
    main()
