# Author: Antonio Lang
# Date: 27 February 2023

import random

class Gram:
    def __init__(self, word, history=None) -> None:
        self.word = word
        self.history = None if history is None else self.get_history()
        self.probability = 0
    def get_history(self):
        for word in range(0, len(self.history)-1):
            self.history.append(word)
    def __eq__(self, __o: object) -> bool:
        return self.word == __o.word and self.history == __o.history

# load_data pulled from test_script.py
def load_data(fname):
  data = []
  fin = open(fname,'r')
  for line in fin:
    line = line.strip()
    data.append(line)
  fin.close()
  return data


def train_ngram(train_data, n):
    # returns a data structure with the ngrams and their probabilities
    
    ngrams = []
    split_data = []
    for index, line in enumerate(train_data):
        split_data.append(line.split(" "))
        for inner_index in range(n, len(split_data[index])+1):
            ngrams.append(split_data[index][inner_index-n:inner_index])
    # print(ngrams)
    n_tokens = len(ngrams)
    unique_tokens = [list(gram) for gram in set(tuple(gram) for gram in ngrams)]
    n_unique = len(unique_tokens)

    unique_probs = []
    for unique in unique_tokens:
        count = 0
        for gram in ngrams:
            if unique == gram: count += 1
        unique_probs.append(count/n_tokens)
    index_start_char = unique_tokens.index(['<s>'])
    del unique_tokens[index_start_char]
    del unique_probs[index_start_char]
    return unique_tokens, unique_probs

def generate_language(ngram_model, max_words) -> str:
    # returns an utterance generated from the ngram model

    tokens = ngram_model[0]
    weights = ngram_model[1]
    generate = True
    num_words = 1
    utterance = ['<s>']
    while generate and num_words < max_words:
        num_words += 1
        word = random.choices(tokens, weights)[len(tokens[0])-1][0]
        utterance.append(word)
        if word == "</s>": break
    if utterance[-1] != "</s>": utterance.append("</s>")
    return " ".join(utterance)

def calculate_probability(utterance, ngram_model) -> float:
    # returns the probability a given utterance could be 
    
    utterance_prob = 1
    split_utterance = utterance.split()
    tokens = [x[0] for x in ngram_model[0]]
    probabilities = dict(zip(tokens, ngram_model[1]))
    for index in range(1, len(split_utterance)):
        utterance_prob *= probabilities[str(split_utterance[index])]

    return utterance_prob

if __name__ == "__main__":
    train_data = load_data("data1.txt")
    model = train_ngram(train_data, 1)
    # print(generate_language(model, 10))
    print(calculate_probability("<s> Sam I am </s>", model))