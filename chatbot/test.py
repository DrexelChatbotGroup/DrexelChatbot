from postag import NLTKPOSTag

a = NLTKPOSTag()
#b = a.getpostag('What is professor Mongan\'s email address?')
#b = a.getpostag('Who is Yi Deng?')
b = a.getpostag('Email Building Room is not Mongan?')
print(b)

noun_list = []
count = 0
while count < len(b):
    tup = b[count]
    if tup[1][0].lower() == 'n':
        noun = tup[0]
        if tup[1][:3].lower() == 'nnp':
            while count + 1 < len(b):
                count = count + 1
                if b[count][1][:3].lower() == 'nnp':
                    noun = noun + ' ' + b[count][0]
                else:
                    break
        noun_list.append(noun)
    count = count + 1
print(noun_list)
