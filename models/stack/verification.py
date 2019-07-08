import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.optimizers import Adam
from sklearn.model_selection import train_test_split
from read_data import read_data
from sklearn.metrics import r2_score
import math

data, target = read_data(50)


data = np.array(data, dtype=float)
target = np.array(target, dtype=float)
print(data)
print(data.shape)
print(target.shape)

model = Sequential()
model.add(LSTM((30), input_shape=(50, 423),return_sequences=True))
model.add(LSTM((12), return_sequences=False))
model.add(Dense(1))
#model.compile(loss='mean_absolute_error', optimizer=Adam(lr=0.005),metrics=['accuracy'])
model.load_weights("weights/improvement-1000.h5")


def rmse(predicted_y, actual_y):
   # print(predicted_y)
   # print(actual_y)
    if len(predicted_y) != len(actual_y):
        print("Nesto ne valja")
        return
    N = float(len(predicted_y))
    result = 0
    for i in range(0, len(predicted_y)):
        result += (predicted_y[i] - actual_y[i])**2
    result = math.sqrt(result / N)
    return result


def mae(predicted_y, actual_y):
   # print(predicted_y)
   # print(actual_y)
    if len(predicted_y) != len(actual_y):
        print("Nesto ne valja")
        return
    N = float(len(predicted_y))
    result = 0
    for i in range(0, len(predicted_y)):
        result += abs(predicted_y[i]- actual_y[i])
    print(result)
    result = result / N
    return result

predicted_y = model.predict(data)
print(rmse(predicted_y, target), "rmse")
print(r2_score(target,predicted_y), "r2")
print(mae(predicted_y, target), "mae")