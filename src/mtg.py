import pandas as pd  # only used to remove duplicate ngrams from the most likely ones
import numpy as np
import nltk


def finish_sentence(sentence, n, corpus, randomize):
    """
    Calls `next_word` in a loop until stopping conditon is met.
    """
    latest_word = sentence[-1]
    while not ((len(sentence) == 10) or (latest_word in (".", "?", "!"))):
        latest_word = next_word(sentence, n, corpus, randomize)
        sentence.append(latest_word)
        pass
    return sentence


def next_word(sentence, n, corpus, randomize):
    """
    1. Creates ngrams
    2. Subsets ngrams that match the sentence
    3. Computes probabilities for each ngram
    4. If more than one most likely words are found, chooses first occurance in corpus
    5. If no word is found, decrements n by 1 and runs again
    """
    word_found = False
    while not word_found:
        if n == 0:
            raise ValueError("Out of vocabulary.")
        else:
            pass

        ngram_list = create_ngrams(corpus, n)
        ngram_subset_list = matched_ngrams(ngram_list, sentence, n)

        if (len(ngram_subset_list) == 0) and (
            n != 1
        ):  # if no ngrams found, look for n-1 grams
            word_found = False
            n -= 1
            continue
        elif (len(ngram_subset_list) == 0) and (n == 1):
            most_likely_ngrams = compute_next_word_probs(ngram_list, randomize)
            first_occuring_ngram = most_likely_ngrams[0]
            word_found = True
            pass
        else:
            most_likely_ngrams = compute_next_word_probs(ngram_subset_list, randomize)

            # if multiple ngrams found, select first occurence in corpus
            first_occuring_ngram = choose_first_occurence(
                most_likely_ngrams, ngram_list
            )
            word_found = True
            pass
        pass

    return first_occuring_ngram[-1]


def create_ngrams(corpus, n):
    """
    Creates n-grams from corpus.
    """
    ngram_list = []
    for i in range(len(corpus) - n + 1):
        ngram_list.append(corpus[i : i + n])
        pass
    return ngram_list


def matched_ngrams(ngram_list, sentence, n):
    """
    Finds matching ngrams.
    """
    matched_ngram_list = []
    for ngram in ngram_list:
        if " ".join(ngram[: n - 1]) == " ".join(sentence[-n + 1 :]):
            matched_ngram_list.append(ngram)
            pass
        pass
    return matched_ngram_list


def compute_next_word_probs(ngram_list, randomize):
    """
    Picks most likely words if randomize=False, else picks randomly from distribution.
    """
    ALPHA = 1  # constant for stupid backoff

    word_count_dict = {}
    for ngram in ngram_list:
        if ngram[-1] in word_count_dict:
            word_count_dict[ngram[-1]] += 1
            pass
        else:
            word_count_dict[ngram[-1]] = 1
            pass
        pass

    # convert counts to probabilities
    word_probs_dict = {
        word: ALPHA * word_count_dict[word] / len(ngram_list)
        for word in word_count_dict.keys()
    }
    distribution = [word[-1] for word in ngram_list]

    if randomize:
        # pick word randomly from the distribution
        random_choice_word = np.random.choice(distribution)
        most_likely_ngrams = [
            word for word in ngram_list if word[-1] == random_choice_word
        ]
        pass
    else:
        # pick words that have max probability
        max_freq_words = [
            key
            for key, value in word_probs_dict.items()
            if value == max(word_probs_dict.values())
        ]
        most_likely_ngrams = [
            ngram for ngram in ngram_list if ngram[-1] in max_freq_words
        ]

    # ensure removal of duplicate ngrams (df.drop_duplicates is the fastest way)
    most_likely_ngrams_unique = (
        pd.DataFrame(most_likely_ngrams)
        .drop_duplicates()
        .reset_index(drop=True)
        .values.tolist()
    )
    return most_likely_ngrams_unique


def choose_first_occurence(ngrams, corpus_ngram_list):
    """
    Returns the orrucence positions for the given ngrams in the corpus ngrams.
    """
    ngram_occurence_pos_dict = {}
    for ngram_to_find in ngrams:
        for idx, ngram in enumerate(corpus_ngram_list):
            if " ".join(ngram_to_find) == " ".join(ngram):
                ngram_occurence_pos_dict[" ".join(ngram_to_find)] = idx
                break
            else:
                pass
        pass

    first_occurence_ngram_concat = min(
        ngram_occurence_pos_dict, key=ngram_occurence_pos_dict.get
    )
    first_occurence_ngram = [
        i for i in ngrams if " ".join(i) == first_occurence_ngram_concat
    ]
    return first_occurence_ngram[0]


if __name__ == "__main__":
    corp = nltk.word_tokenize(nltk.corpus.gutenberg.raw("austen-sense.txt").lower())
    st = ["she", "was", "not"]

    N = 3
    RANDOMIZE = False

    # st = ['robot']; N=3
    # ['robot', ',', 'and', 'the', 'two', 'miss', 'steeles', ',', 'as', 'she']

    # st = ['she', 'was', 'not']; N=1
    # ['she', 'was', 'not', ',', ',', ',', ',', ',', ',', ',']

    # st = ['robot']; N=2
    # ['robot', ',', 'and', 'the', 'same', 'time', ',', 'and', 'the', 'same']

    output = finish_sentence(sentence=st, corpus=corp, n=N, randomize=RANDOMIZE)
    print(output)
