#CS 121 Assignment 1: Text Processing Part B

from PartA import tokenize
from PartA import computeWordFrequencies
import sys

# runtime : average: O(N), Worst O(N^2); n represents length of text content. 
def findCommon(text1, text2):
    t1 = tokenize(text1)
    t2 = tokenize(text2)
    s1 = set(t1)
    s2 = set(t2)
    ans = s1.intersection(s2)
    print(ans)
    return len(ans)

def main():
    f1, f2 = sys.argv[1], sys.argv[2]
    print(findCommon(f1, f2))

if __name__ == '__main__':
    main()

