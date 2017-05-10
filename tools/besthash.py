def besthash(string):
    l = list(string)
    ints = list(map(lambda x: ord(x), l))
    return sum(ints)

print(besthash("test"))
