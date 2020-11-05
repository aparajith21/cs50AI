import nltk
import sys
import string
import os
from math import log
from collections import OrderedDict

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
    corpus ={}
    for file in os.listdir(directory):#for files in directory
        path = os.path.join(directory, file)
        if os.path.isfile(path) and file.endswith('.txt'):#pick text files
            f = open(path, 'r')#open file in read mode
            corpus[file] = f.read()#read file and add to dictionary
    return corpus


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    words = [word.lower() for word in nltk.word_tokenize(document)]#extract in lowercase
    final_words = []
    for word in words:
        if not all(character in string.punctuation for character in word) and word not in nltk.corpus.stopwords.words('english'):
            final_words.append(word)#extract words that are not fully punctuations or english stopwords.
    return final_words
    


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """


    wordcount = {}
    for file in documents:
        words = set()
        for word in documents[file]:
            if word not in words:
                words.add(word)
                if word in wordcount:#if word exists in dictionary
                    wordcount[word] += 1
                else:
                    wordcount[word] = 1
    word_idf = {}
    document_length = len(documents)
    for word in wordcount:
        word_idf[word] = log(document_length / wordcount[word]) #find idf

    return word_idf

def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    tfidf ={}
    for file in files:
        tfidf[file] = 0
        for word in query:
            tfidf[file] += idfs[word] * files[file].count(word)#idf* count
    nfiles = [file for file in OrderedDict(sorted(tfidf.items(), key = lambda kv: kv[1])[-n:])]#sort in order and pick highest n files
    return nfiles


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    ranks = []
    for sentence in sentences:
        sentence_parameter = [sentence, 0, 0]#store sentence, idfs, query term density
        for word in query:
            if word in sentences[sentence]:
                sentence_parameter[1] += idfs[word]#idfs
                sentence_length = len(sentences[sentence])
                sentence_parameter[2] += sentences[sentence].count(word)/sentence_length#term density
        ranks.append(sentence_parameter)
        
    final_ranks = [sentence for sentence, match, querydensity in sorted(ranks, key = lambda t : (t[1], t[2]))[-n:]]#pick the top 10
    return final_ranks


if __name__ == "__main__":
    main()
