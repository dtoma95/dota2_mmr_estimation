from keras.layers import Input, Dense, Conv2D, MaxPooling2D, UpSampling2D
from keras.models import Model
from keras import backend as K
from read_data import read_data
from sklearn.model_selection import train_test_split

input_shape = Input(shape=(5, 400, 1))

x = Conv2D(16, (5, 5), activation='relu', padding='same')(input_shape)
x = MaxPooling2D((5, 5), padding='same')(x)
x = Conv2D(8, (4, 4), activation='relu', padding='same')(x)
x = MaxPooling2D((4, 4), padding='same')(x)
x = Conv2D(1, (2, 2), activation='relu', padding='same')(x)
encoded = MaxPooling2D((2, 2), padding='same')(x)
encoder = Model(input_shape, encoded)
print(encoder.input_shape)
# at this point the representation is (4, 4, 8) i.e. 128-dimensional

x = Conv2D(16, (2, 2), activation='relu', padding='same')(encoded)
x = UpSampling2D((1, 2))(x)
xer = Model(input_shape, x)
print(xer.output_shape)
x = Conv2D(8, (4, 4), activation='relu', padding='same')(x)
x = UpSampling2D((5, 5))(x)
xer = Model(input_shape, x)
print(xer.output_shape)
x = Conv2D(1, (1, 1), activation='relu')(x)
x = UpSampling2D((1, 4))(x)
xer = Model(input_shape, x)
print(xer.output_shape)
decoded = Conv2D(1, (4, 4), activation='sigmoid', padding='same')(x)

autoencoder = Model(input_shape, decoded)
autoencoder.compile(optimizer='adadelta', loss='binary_crossentropy')
print(autoencoder.output_shape)
from keras.datasets import mnist
import numpy as np

data = read_data(50)
data = np.array(data, dtype=float)
print(data.shape)
data = data.reshape(len(data), data[0].shape[0],data[0].shape[1], 1)
print(data.shape)
x_train,_, x_test,_ = train_test_split(data, data, test_size=0.2, random_state=21)

#for listo in x_train:
 #   listo.appned(0) #padding

autoencoder.fit(x_train, x_train,
                epochs=10,
                batch_size=128,
                shuffle=True,
                validation_data=(x_test, x_test))
autoencoder.save('autoencoder.h5')
encoder.save('encoder.h5')