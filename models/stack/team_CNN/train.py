from keras.layers import Input, Dense, Conv1D, MaxPooling1D, UpSampling1D
from keras.models import Model
from keras import backend as K
from read_data import read_data
from sklearn.model_selection import train_test_split

input_shape = Input(shape=(274, 1))

x = Conv1D(32,  kernel_size=4, activation='relu', padding='same')(input_shape)
x = MaxPooling1D(pool_size=2, padding='same')(x)
x = Conv1D(8, kernel_size=2, activation='relu', padding='same')(x)
encoded = MaxPooling1D(pool_size=2, padding='same')(x)

# at this point the representation is (4, 4, 8) i.e. 128-dimensional

x = Conv1D(8, kernel_size=2, activation='relu', padding='same')(encoded)
x = UpSampling1D(2)(x)
x = Conv1D(32, kernel_size=2, activation='relu')(x)
x = UpSampling1D(2)(x)
decoded = Conv1D(1, kernel_size=2, activation='sigmoid', padding='same')(x)

autoencoder = Model(input_shape, decoded)
autoencoder.compile(optimizer='adadelta', loss='binary_crossentropy')

from keras.datasets import mnist
import numpy as np

data = read_data(50)
data = np.array(data, dtype=float)
print(data.shape)
data = data.reshape(data.shape[0],data.shape[1], 1)

x_train,_, x_test,_ = train_test_split(data, data, test_size=0.2, random_state=21)

#for listo in x_train:
 #   listo.appned(0) #padding

autoencoder.fit(x_train, x_train,
                epochs=50,
                batch_size=128,
                shuffle=True,
                validation_data=(x_test, x_test))
autoencoder.save('autoencoder.h5')
encoded.save('encoder.h5')