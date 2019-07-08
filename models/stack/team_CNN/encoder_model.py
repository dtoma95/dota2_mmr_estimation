from keras.layers import Input, Dense, Conv2D, MaxPooling2D, UpSampling1D
from keras.models import Model


def get_team_model(path=""):
    input_shape = Input(shape=(5, 400, 1))

    x = Conv2D(16, (5, 5), activation='relu', padding='same')(input_shape)
    x = MaxPooling2D((5, 5), padding='same')(x)
    x = Conv2D(8, (4, 4), activation='relu', padding='same')(x)
    x = MaxPooling2D((4, 4), padding='same')(x)
    x = Conv2D(1, (2, 2), activation='relu', padding='same')(x)
    encoded = MaxPooling2D((2, 2), padding='same')(x)
    encoder = Model(input_shape, encoded)
    encoder.load_weights(path+"/encoder.h5")
    return encoder