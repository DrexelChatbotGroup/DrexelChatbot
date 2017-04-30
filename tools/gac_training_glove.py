file_name = "gac_data.csv"
out_name = "trained_model.m5"
num_of_gas = 9
max_question_length = 25 #used to be 100
top_words = 5000
filt = '.?"\/!,<>@#$%^&*_-+=|}{][:;~`()'
embedding_vector_length = 50
percent_test = 0.10
MAX_NB_WORDS = 20000
EMBEDDING_DIM = 100

#Note: It is very important that the above values be set in the same way for
#      both this script and the gac class file.


import csv
import math
import numpy
import os
numpy.random.seed(0)

from zlib import adler32
from keras.preprocessing import text
from keras.preprocessing import sequence
from keras.models import Sequential
from keras.layers.embeddings import Embedding
from keras.layers import LSTM
from keras.layers import Dense
import numpy as np


def my_hash(item):
    to_hash = item.replace("'s", "")
    to_hash = to_hash.replace("'", "")
    for c in filt:
        to_hash = to_hash.replace(c, "")

    # print(to_hash)
    final = []
    words = to_hash.lower().split(" ")
    for word in words:
        if(word in embeddings_index):
            final.append(embeddings_index[word])
        else:
            print("key error", word);
    return final

print('Indexing word vectors.')

# num_words = min(MAX_NB_WORDS, len(word_index))
# embedding_matrix = np.zeros((num_words, EMBEDDING_DIM))
# for word, i in word_index.items():
#     if i >= MAX_NB_WORDS:
#         continue
#     embedding_vector = embeddings_index.get(word)
#     if embedding_vector is not None:
#         # words not found in embedding index will be all-zeros.
#         embedding_matrix[i] = embedding_vector

embeddings_index = {}
f = open(os.path.join('', 'glove.6B.50d.txt'), encoding='utf8')
for line in f:
    values = line.split()
    word = values[0]
    coefs = np.asarray(values[1:], dtype='float32')
    embeddings_index[word] = coefs
f.close()

print('Found %s word vectors.' % len(embeddings_index))

try:
    csvfile = open(file_name, newline='')
except OSError:
    print("Error opening file")
    exit()

x = []
y = []
reader = csv.reader(csvfile)
next(reader) #Throw out the first line
try:
    for record in reader:
        if record[4] == "yes": #This is the line that makes it train on professor questions only
            x.append(my_hash(record[2]))
            temp = [0] * num_of_gas
            temp[int(record[3])] = 1
            y.append(temp)
except ValueError:
    print("Error: malformed data")
    exit()

csvfile.close()

x = x * 10 #These two lines are needed because we have very little input data
y = y * 10

x = sequence.pad_sequences(x, maxlen=max_question_length)

split_point = math.floor(len(x) * percent_test)
x_test = x[:split_point]
x_train = x[split_point:]
y_test = y[:split_point]
y_train = y[split_point:]



model = Sequential()
# note that we set trainable = False so as to keep the embeddings fixed
model.add(Embedding(top_words, embedding_vector_length, input_length=max_question_length, trainable=False))
model.add(LSTM(50)) #this was 100...
model.add(Dense(num_of_gas, activation='softmax'))

model.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics=['accuracy'])
print(model.summary())

model.fit(x_train, y_train, validation_data=(x_test, y_test), nb_epoch=20, batch_size=64)

scores = model.evaluate(x_test, y_test, verbose=0)
print("Accuracy: %.2f%%" % (scores[1]*100))

try:
    model.save(out_name) #apparently saving a model requires some package that is not installable on windows
except ImportError:
    print("Failed to save model, missing required libraries.")
input("Press enter to exit...")



