from hls4ml.converters.keras_to_hls import keras_to_hls
import pytest
import hls4ml
import numpy as np
from sklearn.metrics import accuracy_score
import tensorflow as tf
from tensorflow.keras.models import model_from_json, Model
from tensorflow.keras.layers import Input, Permute
import yaml

@pytest.fixture(scope='module')
def data():
    X = np.random.rand(1, 2, 3)
    return X

@pytest.fixture(scope='module')
def keras_model():
    inp = Input(shape=(2, 3), name='input_1')
    out = Permute((2, 1))(inp)
    model = Model(inputs=inp, outputs=out)
    return model

@pytest.fixture      
@pytest.mark.parametrize('io_type', ['io_parallel',
                                     'io_stream'])
def hls_model(keras_model, io_type):
    hls_config = hls4ml.utils.config_from_keras_model(keras_model, 
                                                      default_precision='ap_fixed<16,3,AP_RND_CONV,AP_SAT>',
                                                      granularity='name')
    hls_model = hls4ml.converters.convert_from_keras_model(keras_model,
                                                           hls_config=hls_config,
                                                           io_type=io_type,
                                                           output_dir='hls4mlprj_transpose_{}'.format(io_type))

    hls_model.compile()
    return hls_model

@pytest.mark.parametrize('io_type', ['io_parallel', 
                                     'io_stream'])
def test_accuracy(data, keras_model, hls_model):
    X = data
    model = keras_model
    # model under test predictions and accuracy
    y_keras = model.predict(X)
    y_hls4ml   = hls_model.predict(X).reshape(y_keras.shape)
    # "accuracy" of hls4ml predictions vs keras
    np.testing.assert_allclose(y_keras, y_hls4ml, rtol=0, atol=1e-04, verbose=True)
