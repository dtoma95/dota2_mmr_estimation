
import numpy as np
import json
import os
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from sklearn.model_selection import train_test_split
from read_data import read_data
import math


data, target = read_data(50)


data = np.array(data, dtype=float)
target = np.array(target, dtype=float)
print(data)
print(data.shape)
print(target.shape)
target.shape
x_train,x_test, y_train, y_test = train_test_split(data, target, test_size=0.2, random_state=21)

#data = data.reshape((1, 1, 100))

#target = target.reshape((1, 1, 100))
#x_test=[i for i in range(100,200)]
#x_test=np.array(x_test).reshape((1,1,100));
#y_test=[i for i in range(101,201)]
#y_test=np.array(y_test).reshape(1,1,100)


model = Sequential()  
model.add(LSTM((10), input_shape=(50, 3983),return_sequences=True))
model.add(LSTM((4), input_shape=(50, 100),return_sequences=False))
model.add(Dense(1))
model.compile(loss='mean_absolute_error', optimizer='adam',metrics=['accuracy'])
model.fit(x_train, y_train, epochs=100, batch_size=1, verbose=2,validation_data=(x_test, y_test))

try:
    model.save('my_model2.h5')
except:
    pass

def rmse(predicted_y, actual_y):
   # print(predicted_y)
   # print(actual_y)
    if len(predicted_y) != len(actual_y):
        print("Nesto ne valja")
        return
    N = float(len(predicted_y))
    result = 0
    for i in range(0, len(predicted_y)):
        result += (predicted_y[i] + actual_y[i])**2
    result = math.sqrt(result / N)
    return result

predicted_y = model.predict(x_test)
print(rmse(predicted_y, y_test))
model.save('my_model2.h5')