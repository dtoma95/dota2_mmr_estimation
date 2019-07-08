from keras.layers import Input, Dense, Conv1D, MaxPooling1D, UpSampling1D
from keras.models import Model
from keras import backend as K
from read_data import read_data
from sklearn.model_selection import train_test_split


def get_items_model():
    input_shape = Input(shape=(308, 1))
    x = Conv1D(16,  kernel_size=4, activation='relu', padding='same')(input_shape)
    x = MaxPooling1D(pool_size=4, padding='same')(x)
    x = Conv1D(8,  kernel_size=4, activation='relu', padding='same')(x)
    x = MaxPooling1D(pool_size=4, padding='same')(x)
    x = Conv1D(1, kernel_size=2, activation='relu', padding='same')(x)
    encoded = MaxPooling1D(pool_size=4, padding='same')(x)
    encoder = Model(input_shape, encoded)
    encoder.load_weights("encoder.h5")
    return encoder