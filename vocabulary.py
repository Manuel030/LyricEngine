import numpy as np

# Character-based vocabulary
vocab = sorted(set([' ', '!', '"', '#', '&', "'", '(', ')', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
         ':', '=', '?', '[', ']', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q',
         'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '–', '’', '%', '*', ';', '\n', '$', '“', '”', '‘', '+']))

# Creating a mapping from unique characters to indices
def char2idx(c):
    lookup = {u: i for i, u in enumerate(vocab)}
    return lookup[c]

def idx2char(idx):
    lookup = np.array(vocab)
    return lookup[idx]
