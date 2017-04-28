from postag import NLTKPOSTag
import sys

#sentence = sys.argv[1]
#a = NLTKPOSTag()
#b = a.getpostag(sentence)
#
#noun_list = []
#count = 0
#while count < len(b):
#    word = b[count][0]
#    tag = b[count][1]
#    if tag[0].lower() == 'n':
#        noun = word
#        #consider adjacent proper nouns to be 1 noun
#        if tag[:3].lower() == 'nnp':
#            while count + 1 < len(b):
#                count = count + 1
#                word = b[count][0]
#                tag = b[count][1]
#                if tag[:3].lower() == 'nnp':
#                    noun = noun + ' ' + word
#                else:
#                    count = count - 1
#                    break
#        noun_list.append(noun)
#    count = count + 1
#print(noun_list)

filename = 'gac_data_yesyes.txt'
try:
    text = open(filename, 'rb')
except OSError:
    print('Error opening file')
    exit()
sentences = []
for line in text:
    sentences.append(line.strip())
bs = []
a = NLTKPOSTag()
for sentence in sentences:
    bs.append(a.getpostag(sentence))

for b in bs:
    noun_list = []
    count = 0
    while count < len(b):
        word = b[count][0]
        tag = b[count][1]
        if tag[0].lower() == 'n':
            noun = word
            #consider adjacent proper nouns to be 1 noun
            if tag[:3].lower() == 'nnp':
                while count + 1 < len(b):
                    count = count + 1
                    word = b[count][0]
                    tag = b[count][1]
                    if tag[:3].lower() == 'nnp':
                        noun = noun + ' ' + word
                    else:
                        count = count - 1
                        break
            noun_list.append(noun)
        count = count + 1
    print(noun_list)
