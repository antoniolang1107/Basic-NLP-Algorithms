import random
import automata
import edit_distance
import ngrams

def load_data(fname):
  data = []
  fin = open(fname,'r')
  for line in fin:
    line = line.strip()
    data.append(line)
  fin.close()
  return data


