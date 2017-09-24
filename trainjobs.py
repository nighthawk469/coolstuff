import pandas

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.cross_validation import train_test_split
from sklearn.linear_model import LogisticRegressionCV



df = pandas.read_csv("test.csv")
print(df.head())
