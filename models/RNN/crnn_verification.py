
import numpy as np
import json
import os
from keras.models import Sequential
from keras.layers import Dense, Conv1D, MaxPool1D
from keras.layers import LSTM
from sklearn.model_selection import train_test_split
from keras.callbacks import ModelCheckpoint
from keras.optimizers import Adam
from read_data import read_data
import math


data, target = read_data(50)


data = np.array(data, dtype=float)
target = np.array(target, dtype=float)
print(data)
print(data.shape)
print(target.shape)

model = Sequential()
model.add(Conv1D(64, input_shape=(50, 3983), kernel_size=4)) #TimeDistributed(Conv1D(64, input_shape=(50, 3983), kernel_size=4))
model.add(MaxPool1D(pool_size=4)) #TimeDistributed(MaxPool1D(pool_size=4))
model.add(Conv1D(32, kernel_size=4)) #TimeDistributed(Conv1D(32, kernel_size=4))
model.add(MaxPool1D(pool_size=4)) #TimeDistributed(MaxPool1D(pool_size=4))
model.add(LSTM((21),return_sequences=False))#, input_shape=(50, 3983)
model.add(Dense(12))
model.add(Dense(1))
model.compile(loss='mean_absolute_error', optimizer=Adam(lr=0.001), metrics=['mae'])
#model.load_weights('digits_CNN/end_result_new.h5')

# saving the model weights after each epoch, just in case
filepath="weights\\improvement-{epoch:02d}.hdf5"
checkpoint = ModelCheckpoint(filepath, monitor='val_acc', verbose=1, mode='max')

callbacks_list = [checkpoint]

model.fit(x_train, y_train, epochs=500, batch_size=32, verbose=2,validation_data=(x_test, y_test), callbacks = callbacks_list)

try:
    model.save('simple.h5')
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
model.save('simple.h5')