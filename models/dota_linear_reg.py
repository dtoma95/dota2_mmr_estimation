import pandas
import numpy as np
from sklearn import metrics, linear_model, preprocessing, model_selection
from misc_func import cross_validation, load, run_all

def test():
    X, y = load("data1.csv")

    # normalizacija i centralizacija
    

    reg = linear_model.LinearRegression()
    reg.fit(X, y)
    print(reg.score(X, y))
    print(reg.coef_)

    X2, y2 = load("data.csv")
    X2 = scaler.transform(X2)
    y_pred = reg.predict(X2)
    # y_pred = y_pred * (y_max + y_min) + y_min
    y_pred = scaler2.inverse_transform(y_pred)
    print("RMSE: ", rmse(y_pred, y2))
    print("RMSE: ", metrics.mean_squared_error(y2, y_pred))
    print("R2: ", metrics.r2_score(y2, y_pred))


if __name__ == "__main__":
    run_all(linear_model.LinearRegression())
    #test()
