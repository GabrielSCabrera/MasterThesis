from sklearn.neural_network import MLPClassifier

import sys
sys.path.insert(0, '..')
from preprocessing import config
from preprocessing import split_2D

clf = MLPClassifier(solver='lbfgs', alpha=1e-5,
                    hidden_layer_sizes=(5, 2), random_state=1)

clf.fit(X, y)
