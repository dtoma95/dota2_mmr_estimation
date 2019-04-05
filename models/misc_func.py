import pandas
import numpy as np
from sklearn import metrics, linear_model, preprocessing, model_selection, decomposition

def normalize(X, y):
    scaler = preprocessing.StandardScaler()
    scaler.fit(X)
    X = scaler.transform(X)
    # y_min = min(y)
    # y_max = max(y)
    # y_norm = (y - y_min)/(y_max - y_min)
    #scaler2 = preprocessing.StandardScaler()
    #scaler2.fit(y)
    #y = scaler2.transform(y)
    return X, y

def dim_reduction(X_train, y_train, X_test):
    dec = decomposition.PCA(n_components=200)
    X_train = dec.fit_transform(X_train, y_train)
    X_test = dec.transform(X_test)
    
    print(len(X_train[0]))
    #print(X_train[0])
    
    return X_train, X_test
    
def cross_validation(X, y, model, dim_red=True):
    #X, y = load("data1.csv")

    print("CROSS VALIDATION")
    sss = model_selection.ShuffleSplit(n_splits=2, test_size=0.2, train_size=0.8, random_state=29)
    split = sss.split(X, y)

    #model = linear_model.ElasticNet(random_state=1)

    rmseovi = []
    for i, j in split:
        X_train, X_test = X[i], X[j]
        y_train, y_test = y[i], y[j]

        X_train, X_test = dim_reduction(X_train, y_train, X_test)
        
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        rmseovi.append(rmse(y_pred, y_test))

    print(rmseovi)
    return(sum(rmseovi)/len(rmseovi))
    
    
def rmse(predicted_y, actual_y):
   # print(predicted_y)
   # print(actual_y)
    if len(predicted_y) != len(actual_y):
        print("Nesto ne valja")
        return
    N = float(len(predicted_y))
    result = np.sqrt(sum(np.square((predicted_y - actual_y))) / N)
    return result
    
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
    return normalize(x, y)
       
def run_all(model, sta=0):
    
    if sta==0 or sta==1:
        print("Starting simple...")
        X, y = load("../data/data_extraction/data_simple_extraction.csv")
        print("Simple - ", cross_validation(X, y, model))
    if sta==0 or sta==2:
        print("Starting all heroes...")
        X, y = load("../data/data_extraction/data_all_heroes.csv")
        print("All Heroes - ", cross_validation(X, y, model))
    if sta==0 or sta==3:
        print("Starting roles...")
        X, y = load("../data/data_extraction/data_all_roles.csv")
        print("All Roles - ", cross_validation(X, y, model))
    if sta==0 or sta==4:
        print("Starting roles items...")
        X, y = load("../data/data_extraction/data_all_roles_items.csv")
        print("All Roles Items - ", cross_validation(X, y, model))