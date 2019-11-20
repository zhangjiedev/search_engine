#CS 121 Assignment 1: Text Processing Part A

import sys
import re
# runtime : theta(n) linear; n represents length of text content
def tokenize(textFilePath : str):
    try:
        f = open(textFilePath, 'r')
    except FileNotFoundError as identifier:
        return None
    
    text = f.read()
    tokens = re.findall("[a-zA-Z0-9]+", text.lower())
    f.close()
    return tokens

# runtime : theta(n) linear n represents the number of tokens
def computeWordFrequencies(tokens: list):
    return {x:tokens.count(x) for x in tokens}


# runtime : theta(n log n) n represents the number of tokens
def frequencies(f: map):
    return sorted(f.items(), reverse = True, key = lambda x : x[1])

def main():
    path = sys.argv[1]
    tokens = tokenize(path)
    m = computeWordFrequencies(tokens)
    print(frequencies(m))

if __name__ == '__main__':
    main()