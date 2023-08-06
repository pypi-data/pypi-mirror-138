# functions related to seeding the genetic algorithm 
# Jan 2022

import random
import config
import string as String 



# extract the literals from a given regex
# but for now just return some for testing 
# return: a list of single-character strings 
def get_tokens(regex):
    # tokens = [t.token for t in regex.tokens if t.type == 5 and t.token != ""]
    tokens = [] 
    for t in regex.tokens:
        if t.type == 5 and t.token != "":
            if t.token[0] == "\\":      # remove the escape \
                tokens.append(t.token[1:])
            else:
                tokens.append(t.token)
    return tokens



# input a list of characters 
# output all the substrings 
# abc -> a, b, c, ab, bc, abc
def regex_substrings(tokens):
    seeds = [] 
    for i in range(len(tokens)):
        for j in range(i, len(tokens)+1):
            substring = "".join(tokens[i:j])
            seeds.append(substring)
    return seeds 


# input tokens, a list of characters to be randomly (uniformly) sampled into strings 
# takes in list of tokens as single-character strings 
def generate_seeds(tokens):

    # get list of characters (alphabet, digits, punctuation)
    chars = String.printable
    if len(tokens)>0:
        substrings = regex_substrings(tokens) 
    else: 
        substrings = String.printable 

    seeds = []
    for i in range(config.num_seeds):
        length = random.randrange(2, config.max_len) # might want to bias this towards longer seeds
        seed = ""
        for j in range(length):
            # 50% pick character from substrings, 50% pick from chars 
            char = random.choice(random.choice([substrings, chars]))
            seed = seed + char     
        seeds.append(seed)
    return seeds 