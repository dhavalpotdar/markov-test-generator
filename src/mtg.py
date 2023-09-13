 
import numpy as np
import nltk


def finish_sentence(sentence, n, corpus):
    pass

def next_word(sentence, n, corpus):
    word_found = False
    while not word_found:
        n_gram_list = create_ngrams(corpus, n)
        pass
    pass

def create_ngrams(corpus, n):
    ngram_list = []
    for i in range(len(corpus)-n+1):
        ngram_list.append(corpus[i:i+n])
        pass
    return ngram_list

if __name__ == '__main__':
    sentence = ['she', 'was', 'not'] 
    # corpus = nltk.word_tokenize(
    #     nltk.corpus.gutenberg.raw('austen-sense.txt').lower()
    # )
    corpus = ['candy', 'paint', 'with', 'the', 'white', 'on', 'top']
    output = create_ngrams(corpus, 2)
    print(output)
