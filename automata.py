# Author: Antonio Lang
# Date: 27 February 2023

import random

ones_list = ['one','two','three','four','five','six','seven','eight','nine']
bases = ["twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]

class AutomatonNode:
    def __init__(self, state, next=[("", None)]) -> None:
        self.state = state
        self.next = next
    def __str__(self) -> str:
        return f"Automaton Node: {hex(id(self))}\nState {self.state}, next node list: {self.next}\n"

def create_automata(option) -> AutomatonNode: 
    # automata to recognize the following languages
    if option == 1: # baa+
        q3_1 = AutomatonNode("accept")
        q2_1 = AutomatonNode("valid", [("a", q3_1)])
        q3_1.next.append(("a", q2_1))
        q1_1 = AutomatonNode("valid", [("a", q2_1)])
        q0_1 = AutomatonNode("valid", [("b", q1_1)])
        return q0_1
    if option == 2: # (abba)+ or (baab)+
        q4_2 = AutomatonNode("accept")
        q3_2 = AutomatonNode("valid", [("a", q4_2)])
        q2_2 = AutomatonNode("valid", [("b", q3_2)])
        q1_2 = AutomatonNode("valid", [("b", q2_2)])
        q4_2.next = [("", None), ("a", q1_2)]
        q8_2 = AutomatonNode("accept")
        q7_2 = AutomatonNode("valid", [("b", q8_2)])
        q6_2 = AutomatonNode("valid", [("a", q7_2)])
        q5_2 = AutomatonNode("valid", [("a", q6_2)])
        q8_2.next.append(("b", q5_2))
        q0_2 = AutomatonNode("valid", [("a", q1_2),("b", q5_2)])
        return q0_2
    if option == 3: # zero through ninety nine
        q1_3 = AutomatonNode("accept", [("", None)]) # terminal accept state
        spaced_ones_list = [' one',' two',' three',' four',' five',' six',' seven',' eight',' nine']
        terminal_list = [q1_3] * len(spaced_ones_list)
        q2_3 = AutomatonNode("accept", list(zip(spaced_ones_list, terminal_list))) # accept state for twenty-ninety
        q2_3.next.append(("", None))
        special_nums = ones_list.copy()
        special_nums.insert(0, "zero")
        special_nums += ['ten', 'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen',
                         'sixteen','seventeen','eighteen','nineteen']
        q1_nodes = [q1_3] * len(special_nums)
        q1_paths = list(zip(special_nums, q1_nodes))
        q2_nodes = [q2_3] * len(bases)
        q2_paths = list(zip(bases, q2_nodes))
        q0_3 = AutomatonNode("valid", q1_paths+q2_paths)
        return q0_3
    
def generate_language(automata) -> str:
    # returns an utterance generated by the automaton
    utterance = []
    node = automata
    generate_utterance = True
    while generate_utterance:
        branch = random.randint(0, len(node.next)-1)
        if node.next[branch][1] == None:
            break
        utterance.append(node.next[branch][0])
        node = node.next[branch][1]
    return ''.join(utterance)

def recognize_language(automata, utterance) -> int:
    # wrapper function to call the recursive function and cast the output to int
    if " " in utterance: 
        space_index = utterance.index(' ')
        utterance = [utterance[:space_index], utterance[space_index:]]
    for words in ones_list+bases+['zero','ten']: # tokenizes specific utterances
        if utterance == words: utterance = [utterance] 
    return int(determine_valid_word(automata, utterance, 0))

def determine_valid_word(automaton_node, utterance, chars_read) -> bool:
    # recursive function to check if a word exists in a given automaton's language
    if automaton_node is None: return False # end of autoamaton path
    if automaton_node.state == "accept" and chars_read == len(utterance):
        return True
    elif len(utterance) == chars_read and automaton_node.state != "accept":
        return False
    else:
        valid_chars = [char[0] for char in automaton_node.next]
        if utterance[chars_read] in valid_chars:
            branch = valid_chars.index(utterance[chars_read]) # finds a valid path
            return determine_valid_word(automaton_node.next[branch][1],
                                        utterance, chars_read+1)
        else: # no valid paths
            return False