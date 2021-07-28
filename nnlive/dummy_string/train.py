#EpyNN/nnlive/dummy_boolean/train.py
################################## IMPORTS ################################
# Set default environment and settings
from nnlibs.initialize import *
# EpyNN meta-model for neural networks
from nnlibs.meta.models import EpyNN
# Embedding layer for input data
from nnlibs.embedding.models import Embedding
# Layers relevant to input data type
from nnlibs.flatten.models import Flatten
from nnlibs.dense.models import Dense
from nnlibs.lstm.models import LSTM
from nnlibs.rnn.models import RNN
from nnlibs.gru.models import GRU
# Commons utils and maths
import nnlibs.commons.library as cl
import nnlibs.commons.maths as cm
# Routines for dataset preparation
import prepare_dataset as ps
# Local EpyNN settings
import settings as se
# Compute with NumPy
import numpy as np

import random
random.seed(1)
################################## HEADERS ################################
np.set_printoptions(precision=3,threshold=sys.maxsize)

np.seterr(all='warn')

cl.init_dir(se.config)

# DOCS_HEADERS
################################## DATASETS ################################
dataset = ps.prepare_dataset(se.dataset)
#dataset = cl.read_dataset()


################################ BUILD MODEL ###############################
embedding = Embedding(dataset, se.dataset, encode=True)

name = 'Embedding_Flatten_Dense-2-Softmax' # (1)
layers = [embedding, Flatten(), Dense()]

name = 'RNN-11-bin-Softmax' # (2)
#layers = [embedding, RNN(hidden_size=12, binary=True)]

# name = 'GRU-12-bin-Softmax' # (3)
# layers = [embedding,GRU(12,binary=True)]

# name = 'LSTM-12-bin-Softmax' # (4)
# layers = [embedding,LSTM(12, binary=True)]

# name = 'Embedding_Flatten_RNN-11-Softmax_Dense-2-Softmax' # (5)
layers = [embedding, RNN(12), Flatten(), Dense(48,cm.relu), Dense()]

model = EpyNN(layers=layers, settings=[se.dataset, se.config, se.hPars], seed=1, name=name)


################################ TRAIN MODEL ################################
model.train()

model.plot()


################################# USE MODEL #################################
model = cl.read_model()

unlabeled_dataset = ps.prepare_unlabeled(N_SAMPLES=1)
# [[['A', 'G', ... , 'C'], None]]

X = model.embedding_unlabeled(unlabeled_dataset, encode=True)
# [[[0. 0. 1. 0.],[0. 1. 0. 0.], ... ,[0. 0. 0. 1.]]]

A = model.predict(X)
# [[0.61  0.39 ]]

P = np.argmax(A, axis=1)
# [0]
