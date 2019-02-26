import pandas
import numpy as np
from sklearn import metrics, linear_model, preprocessing, model_selection


def load(filename):
    data = pandas.read_csv(filename)

    x_headers = list(data)
    remove_headers = ['account_id', 'mmr', 'recorded_games']
    x_headers = [h for h in x_headers if h not in remove_headers]

    # for h in x_headers:
        # print(h)
        # print(max(data[h]))
        # print(min(data[h]))
    #    h_min = min(data[h])
    #    h_max = max(data[h])
    #    data[h] = (data[h] - h_min)/(h_max - h_min)

    x = np.array(data.as_matrix(x_headers))
    y = data['mmr']
    y = np.array(y.tolist())
    return x, y


def rmse(predicted_y, actual_y):
    if len(predicted_y) != len(actual_y):
        print("Nesto ne valja")
        return
    N = float(len(predicted_y))
    result = np.sqrt(sum(np.square((predicted_y - actual_y))) / N)
    return result


def cross_validation():
    X, y = load("data1.csv")

    print("CROSS VALIDATION")
    sss = model_selection.ShuffleSplit(n_splits=10, test_size=0.2, train_size=0.8, random_state=29)
    split = sss.split(X, y)

    reg = linear_model.ElasticNet(random_state=1)

    rmseovi = []
    for i, j in split:
        X_train, X_test = X[i], X[j]
        y_train, y_test = y[i], y[j]

        reg.fit(X_train, y_train)
        y_pred = reg.predict(X_test)

        rmseovi.append(rmse(y_pred, y_test))

    print(rmseovi)
    print(sum(rmseovi)/len(rmseovi))


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
    cross_validation()
    # test()
    # test_without_norm()
