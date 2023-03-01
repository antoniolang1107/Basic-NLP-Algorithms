# Author: Antonio Lang
# Date: 27 February 2023

import random

class Gram:
    def __init__(self, word, history=None) -> None:
        self.word = word
        self.history = None
        self.probability = 0
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
    ngram_model = {}
    for index, line in enumerate(train_data):
        split_data.append(line.split(" "))
        for inner_index in range(n, len(split_data[index])+1):
            gram_window = (split_data[index][inner_index-n:inner_index])
            word = gram_window[n-1]
            history = gram_window[:n-1]
            if ngram_model.get(str(history)) is None: ngram_model[str(history)] = [word]
            else: ngram_model[str(history)].append(word)
            ngrams.append(gram_window)
    return ngram_model, n

def generate_language(ngram_model, max_words) -> str:
    # returns an utterance generated from the ngram model
    ngram_model = ngram_model[0]
    generate = True
    num_words = 1
    utterance = []
    history_size = 0
    if ngram_model.get(str([])) is not None: utterance = ['<s>']
    else: 
        history_keys = list(ngram_model.keys())
        start_history = [history for history in history_keys if "['<s>'" in history]
        gram_history = random.choice(start_history)
        copy = gram_history # following clean 'copy' to add to utterance
        copy = copy.replace("[","").replace("]","").replace("'","")
        copy = copy.split(",")
        for index, word in enumerate(copy):
            copy[index] = copy[index].replace(" ","")
        utterance += copy
        utterance.append(random.choice(ngram_model[gram_history]))
        history_size = len(start_history)
        num_words = history_size + 1
    while generate and num_words < max_words:
        history = utterance[num_words-history_size:num_words]
        word = random.choice(ngram_model[str(history)])
        num_words += 1
        if word == '<s>': continue
        utterance.append(word)
        if word == "</s>": break
    if utterance[-1] != "</s>": utterance.append("</s>")
    return " ".join(utterance)

def calculate_probability(utterance, ngram_model) -> float:
    # returns the probability a given utterance could be 
    
    gram_size = ngram_model[1]
    ngram_model = ngram_model[0]
    utterance_prob = 1
    split_utterance = utterance.split()

    for key, value in ngram_model.items():
        unique_words = list(set(value))
        unique_probs = []
        for unique in unique_words:
            count = 0
            for word in value:
                if unique == word: count += 1
            unique_probs.append(count / len(value))
        ngram_model[key] = (unique_words, unique_probs)

    for index in range(gram_size-1, len(split_utterance)):
        history = split_utterance[index-gram_size+1:index]
        word = split_utterance[index]
        temp = ngram_model[str(history)]
        word_index = temp[0].index(word)
        word_prob = temp[1][word_index]
        utterance_prob *= word_prob

    return utterance_prob

if __name__ == "__main__":
    train_data = load_data("data1.txt")
    model = train_ngram(train_data, 2)
    print(generate_language(model, 10))
    print(calculate_probability("<s> Sam I am </s>", model))