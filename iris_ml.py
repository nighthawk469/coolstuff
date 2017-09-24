import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegressionCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.externals import joblib


def train_model(model_type):
    df = pd.read_csv('TrainingData.csv')
    y = df['Team']
    X = df.drop('Team', axis=1)

    # train_X, test_X, train_y, test_y = train_test_split(X, y, train_size=1)
    lr = model_type()
    lr.fit(X, y)

    joblib.dump(lr, 'team_pred_model.pkl')

    # pred_y = lr.predict(test_X)
    # print(pred_y)
    #
    # print("Test fraction correct (Accuracy) = {:.2f}".format(lr.score(test_X, test_y)))
    # # Test fraction correct (Accuracy) = 0.83


def test_model():
    X = pd.read_csv('User2.csv')
    lr = joblib.load('team_pred_model.pkl')
    return lr.predict(X)[0], lr.predict_proba(X)[0]


if __name__ == '__main__':
    train_model(LogisticRegressionCV)
    result = test_model()
    print(result)
