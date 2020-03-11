from sklearn.neural_network import MLPClassifier
import pickle

from ..utils import parsers
from ..config import config
from ..config import fields

class Model:

    def __init__(self, model = None, **kwargs):
        kwargs = parsers.kwarg_parser(fields.DNN_kwargs, kwargs)
        if model is None:
            self.model = MLPClassifier(**kwargs)
        else:
            self.model = model

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
        if config.DNN_model_extension not in path:
            path += config.DNN_model_extension
        pickle.dump(self.model, open(path, 'wb'))

def load(label):
    path = config.DNN_models_relpath + f'/{label}'
    if config.DNN_model_extension not in path:
        path += config.DNN_model_extension
    model = pickle.load(open(path, 'rb'))
    return Model(model = model)
