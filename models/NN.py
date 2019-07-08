
import numpy as np
import json
import os
from keras.models import Sequential
from keras.layers import Dense, Dropout, Conv1D,MaxPool1D, Flatten
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from misc_func import cross_validation, load, run_all, load_validation
import math
import matplotlib.pyplot as plt

data, target = load("../data/data_extraction/test/data_all_roles_items.csv")

print(len(data))
data = np.array(data, dtype=float)
target = np.array(target, dtype=float)
target = target/7000
print(data.shape)
data = data.reshape(data.shape[0],data.shape[1], 1)

print(data)
print(data.shape)
print(target.shape)
target.shape
x_train,x_test, y_train, y_test = train_test_split(data, target, test_size=0.2, random_state=12)
model = Sequential()
model.add(Conv1D(32, input_shape=(1830,1), kernel_size=8))
model.add(MaxPool1D(pool_size=2))
model.add(Flatten())
model.add(Dense(200,  kernel_initializer='normal', activation='relu'))#input_dim=1830,
model.add(Dropout(0.15))
model.add(Dense(21, kernel_initializer="uniform", activation="relu"))
model.add(Dropout(0.15))
model.add(Dense(12, kernel_initializer="uniform", activation="relu"))
model.add(Dropout(0.15))
model.add(Dense(1, kernel_initializer='normal'))
model.compile(loss='mean_absolute_error', optimizer='adam',metrics=['mae'])
model.load_weights("my_model3.h5")

data1, target1 = load_validation("../data/data_extraction/test/data_all_roles_items.csv","../data/data_extraction/ver/data_all_roles_items_verification.csv")
data1 = data1.reshape(data1.shape[0],data1.shape[1], 1)
target1 = np.array(target1, dtype=float)
target1 = target1/7000
history = model.fit(x_train, y_train, epochs=5, batch_size=32, verbose=2,validation_data=(x_test, y_test))
#try:
 #   model.save('simple.h5')
#except:
 #   pass
model.save('model33.h5')
# summarize history for accuracy
print(history.history)
plt.plot(history.history['mean_absolute_error'])
plt.plot(history.history['val_mean_absolute_error'])
plt.title('model mean absolute error')
plt.ylabel('mean absolute error')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()



def rmse(predicted_y, actual_y):
   # print(predicted_y)
   # print(actual_y)
    if len(predicted_y) != len(actual_y):
        print("Nesto ne valja")
        return
    N = float(len(predicted_y))
    result = 0
    for i in range(0, len(predicted_y)):
        result += (predicted_y[i]*7000 - actual_y[i]*7000)**2
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
        result += abs(predicted_y[i]*7000 - actual_y[i]*7000)
    print(result)
    result = result / N
    return result

data, target = load_validation("../data/data_extraction/test/data_all_roles_items.csv","../data/data_extraction/ver/data_all_roles_items_verification.csv")
data = data.reshape(data.shape[0],data.shape[1], 1)
target = np.array(target, dtype=float)
target = target/7000
predicted_y = model.predict(data)
print(rmse(predicted_y, target))
print(r2_score(target,predicted_y))
print(mae(predicted_y, target), "peder")
