file_name = "gac_data.csv"
out_name = "trained_model.m5"
num_of_gas = 9
max_question_length = 25 #used to be 100
top_words = 5000
filt = '.?"\/!,<>@#$%^&*_-+=|}{][:;~`'
embedding_vector_length = 64
percent_test = 0.10
#Note: It is very important that the above values be set in the same way for
#      both this script and the gac class file.


import csv
import math
import numpy
numpy.random.seed(0)

from keras.preprocessing import text
from keras.preprocessing import sequence
from keras.models import Sequential
from keras.layers.embeddings import Embedding
from keras.layers import LSTM
from keras.layers import Dense

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
            x.append(text.one_hot(record[2].replace("'", " "), top_words, filters=filt))
            temp = [0] * num_of_gas
            #print(record[3] + ":  " + str(int(record[3])))
            temp[int(record[3])] = 1
            #print(record[3] + ":  " + str(temp))
            #print(record[2])
            y.append(temp)
except ValueError:
    print("Error: malformed data")
    exit()

csvfile.close()

print(x)

x = x * 10 #These two lines are needed because we have very little input data
y = y * 10

x = sequence.pad_sequences(x, maxlen=max_question_length)

split_point = math.floor(len(x) * percent_test)
x_test = x[:split_point]
x_train = x[split_point:]
y_test = y[:split_point]
y_train = y[split_point:]

model = Sequential()
model.add(Embedding(top_words, embedding_vector_length, input_length=max_question_length))
model.add(LSTM(50)) #this was 100...
model.add(Dense(num_of_gas, activation='softmax'))

model.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics=['accuracy'])
print(model.summary())

model.fit(x_train, y_train, validation_data=(x_test, y_test), nb_epoch=40, batch_size=64)

scores = model.evaluate(x_test, y_test, verbose=0)
print("Accuracy: %.2f%%" % (scores[1]*100))

try:
    model.save(out_name) #apparently saving a model requires some package that is not installable on windows
except ImportError:
    print("Failed to save model, missing required libraries.")
input("Press enter to exit...")
