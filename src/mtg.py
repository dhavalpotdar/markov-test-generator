 
import numpy as np
import nltk


def finish_sentence(sentence, n, corpus):
    pass

def next_word(sentence, n, corpus):
    alpha_power = 0
    word_found = False
    while not word_found:
        ngram_list = create_ngrams(corpus=corpus, n=n)
        ngram_subset_list = matched_ngrams(ngram_list=ngram_list, sentence=sentence, n=n)

        most_likely_ngrams = compute_next_word_counts(ngram_list=ngram_subset_list)

        # if no ngrams found, look for n-1 grams
        if len(most_likely_ngrams) == 0:
            n -= 1
            word_found = False
            continue
        else:
            first_occuring_ngram = choose_first_occurence(ngrams=most_likely_ngrams, corpus_ngram_list=ngram_list)
            word_found = True
            pass
        pass

    return first_occuring_ngram[-1]

def create_ngrams(corpus, n):
    ngram_list = []
    for i in range(len(corpus)-n+1):
        ngram_list.append(corpus[i:i+n])
        pass
    return ngram_list

def matched_ngrams(ngram_list, sentence, n):
    matched_ngram_list = []
    for ngram in ngram_list:
        if ' '.join(ngram[:n-1]) == ' '.join(sentence[-n+1:]):
            matched_ngram_list.append(ngram)
            pass
        pass
    return matched_ngram_list

def compute_next_word_counts(ngram_list):
    word_count_dict = {}
    for ngram in ngram_list:
        if ngram[-1] in word_count_dict:
            word_count_dict[ngram[-1]] += 1
            pass
        else:
            word_count_dict[ngram[-1]] = 1
            pass
        pass
    
    # get keys corresponding to max value
    max_freq_words = [key for key, value in word_count_dict.items() if value == max(word_count_dict.values())]
    most_likely_ngrams = [ngram for ngram in ngram_list if ngram[-1] in max_freq_words]
    return most_likely_ngrams

def choose_first_occurence(ngrams, corpus_ngram_list):
    ngram_occurence_pos_dict = {}
    for ngram_to_find in ngrams:
        for idx, ngram in enumerate(corpus_ngram_list):
            if ' '.join(ngram_to_find) == ' '.join(ngram):
                ngram_occurence_pos_dict[' '.join(ngram_to_find)] = idx
                break
            else:
                pass
        pass

    first_occurence_ngram_concat = min(ngram_occurence_pos_dict, key=ngram_occurence_pos_dict.get) 
    first_occurence_ngram = [i for i in ngrams if ' '.join(i) == first_occurence_ngram_concat]
    return first_occurence_ngram[0]



if __name__ == '__main__':
    sentence = ['candy', 'this', 'with'] 
    # corpus = ['candy', 'paint', 'with', 'the', 'white', 'on', 'top']
    corpus = ['candy', 'paint', 'with', 'the', 'paint', 'with', 'red']
    N = 3

    output = next_word(sentence=sentence, corpus=corpus, n=N)
    print(output)