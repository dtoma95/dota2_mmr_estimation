from keras.layers import Input, Dense, Conv1D, MaxPooling1D, UpSampling1D
from keras.models import Model


def get_items_model(path=""):
    input_shape = Input(shape=(308, 1))
    x = Conv1D(16,  kernel_size=4, activation='relu', padding='same')(input_shape)
    x = MaxPooling1D(pool_size=4, padding='same')(x)
    x = Conv1D(8,  kernel_size=4, activation='relu', padding='same')(x)
    x = MaxPooling1D(pool_size=4, padding='same')(x)
    x = Conv1D(1, kernel_size=2, activation='relu', padding='same')(x)
    encoded = MaxPooling1D(pool_size=4, padding='same')(x)
    encoder = Model(input_shape, encoded)
    encoder.load_weights(path+"encoder.h5")
    return encoder