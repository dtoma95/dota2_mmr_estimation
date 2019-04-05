import pandas
import numpy as np
from sklearn import metrics, linear_model, preprocessing, model_selection
from misc_func import cross_validation, load, run_all

def test():
    X, y = load("data1.csv")

    # normalizacija i centralizacija
    scaler = preprocessing.StandardScaler()
    scaler.fit(X)
    X = scaler.transform(X)
    # y_min = min(y)
    # y_max = max(y)
    # y_norm = (y - y_min)/(y_max - y_min)
    scaler2 = preprocessing.StandardScaler()
    scaler2.fit(y)
    y = scaler2.transform(y)

    reg = linear_model.ElasticNet(random_state=0)
    reg.fit(X, y)
    print(reg.score(X, y))
    print(reg.coef_)

    X2, y2 = load("data.csv")
    X2 = scaler.transform(X2)
    y_pred = reg.predict(X2)
    # y_pred = y_pred * (y_max + y_min) + y_min
    y_pred = scaler2.inverse_transform(y_pred)
    print("RMSE: ", rmse(y_pred, y2))
    print("RMSE: ", metrics.r2_score(y2, y_pred))


def test_without_norm():
    X, y = load("data1.csv")

    reg = linear_model.ElasticNet(random_state=0)
    reg.fit(X, y)
    print(reg.score(X, y))
    print(reg.coef_)

    X2, y2 = load("data.csv")
    y_pred = reg.predict(X2)
    print("RMSE: ", rmse(y_pred, y2))
    print("RMSE: ", metrics.r2_score(y2, y_pred))

if __name__ == "__main__":
    run_all(linear_model.ElasticNet(random_state=0))
    # test()
    # test_without_norm()
