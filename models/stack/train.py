import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.optimizers import Adam
from sklearn.model_selection import train_test_split
from read_data import read_data
from keras.callbacks import ModelCheckpoint

data, target = read_data(50)


data = np.array(data, dtype=float)
target = np.array(target, dtype=float)
print(data)
print(data.shape)
print(target.shape)
x_train,x_test, y_train, y_test = train_test_split(data, target, test_size=0.2, random_state=21)

model = Sequential()
model.add(LSTM((30), input_shape=(50, 423),return_sequences=True))
model.add(LSTM((12), return_sequences=False))
model.add(Dense(1))
model.compile(loss='mean_absolute_error', optimizer=Adam(lr=0.005),metrics=['accuracy'])


filepath="weights\\improvement-{epoch:02d}.hdf5"
checkpoint = ModelCheckpoint(filepath, monitor='val_acc', verbose=1, mode='max',save_weights_only=True, period=50)

callbacks_list = [checkpoint]

model.fit(x_train, y_train, epochs=1000, batch_size=64, verbose=2,validation_data=(x_test, y_test), callbacks = callbacks_list)