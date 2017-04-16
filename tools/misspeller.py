import random
import string

adjacency = { # this represents the likelihood of exchanging one letter for another
    'a': ['s'],
    'b': ['v', 'n'],
    'c': ['x', 'v'],
    'd': ['s', 'f'],
    'e': ['w', 'r'],
    'f': ['d', 'g'],
    'g': ['f', 'h'],
    'h': ['g', 'j'],
    'i': ['u', 'o'],
    'j': ['h', 'k'],
    'k': ['j', 'l'],
    'l': ['k'],
    'm': ['n'],
    'n': ['b', 'm'],
    'o': ['i', 'p'],
    'p': ['o'],
    'q': ['w'],
    'r': ['e', 't'],
    's': ['a', 'd'],
    't': ['r', 'y'],
    'u': ['y', 'i'],
    'v': ['c', 'b'],
    'w': ['q', 'e'],
    'x': ['z', 'c'],
    'y': ['t', 'u'],
    'z': ['x']
    }

def check(): #testing function
    f = set()

    def line(c):
        if not c in f:
            print(c, end='')
            f.add(c)
            for n in adjacency[c]:
                line(n)

    line('q')
    print()
    line('a')
    print()
    line('z')
    print()

def typo(word, model):
    valid_indexes = []
    for i in range(len(word)):
        if word[i] in string.ascii_letters:
            valid_indexes.append(i)
    
    if len(valid_indexes) > 0:
        upper = False
        index = random.choice(valid_indexes)
        if word[index] in string.ascii_uppercase:
            upper = True
        r = random.choice(model[word[index].lower()])
        if upper:
            r = r.upper()
        
        return word[:index] + r + word[index+1:]
    else:
        return word

w = "hello"
for i in range(100):
    print(typo(w, adjacency))
        







        
