from sklearn.neural_network import MLPClassifier
import argparse
import pickle

from ..utils import parsers
from ..config import config
from ..config import fields

class Model:

    def __init__(self, **kwargs):
        kwargs = parsers.kwarg_parser(fields.DNN_kwargs, kwargs)
        if kwargs['model'] is None:
            model_kwargs = kwargs.copy()
            del model_kwargs['model']
            self.model = MLPClassifier(**model_kwargs)
        else:
            self.model = kwargs['model']

    def fit(self, X_train, y_train):
        params = {
                  'X'   :   X_train,
                  'y'   :   y_train,
                 }
        self.model.fit(**params)

    def score(self, X_test, y_test):
        params = {
                  'X'   :   X_test,
                  'y'   :   y_test,
                 }
        return self.model.score(**params)

    def save(self, label):
        path = config.DNN_models_relpath + f'/{label}'
        if config.model_extension not in path:
            path += config.model_extension
        pickle.dump(model, open(path, 'wb'))

def load(label):
    path = config.DNN_models_relpath + f'/{label}'
    if config.model_extension not in path:
        path += config.model_extension
    model = pickle.load(open(path, 'rb'))
    return DNN(model = model)
