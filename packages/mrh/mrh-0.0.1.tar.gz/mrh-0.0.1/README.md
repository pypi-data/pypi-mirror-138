# Simulating building the MLCM package
This simulation is to parctice the procedure for building a package on PyPi.

# MLCM creates a 2D Multi-Label Confusion Matrix
Please read the following paper for more information:
M. Heydarian, T. Doyle, and R. Samavi, MLCM: Multi-Label Confusion Matrix, IEEE Access, 2022

# An example on how to use MLCM package:
import numpy as np\
import sklearn.metrics as skm\
from mlcm import mlcm

# Creating random input (multi-label data)
number_of_samples = 1000\
number_of_classes = 5\
label_true = np.random.randint(2, size=(number_of_samples, number_of_classes))\
label_pred = np.random.randint(2, size=(number_of_samples, number_of_classes))

conf_mat,normal_conf_mat = mlcm.cm(label_true,label_pred)\
print('\nRaw confusion Matrix:')\
print(conf_mat)\
print('\nNormalized confusion Matrix (%):')\
print(normal_conf_mat)

one_vs_rest = mlcm.stats(conf_mat)
