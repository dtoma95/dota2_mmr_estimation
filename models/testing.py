import pandas
import numpy as np
from sklearn import metrics, linear_model, preprocessing, model_selection, ensemble
from misc_func import cross_validation, load, run_all

if __name__ == "__main__":

    #AdaBoost
    run_all(ensemble.AdaBoostRegressor(random_state=21), sta=4)
    
    #GradientBoost
    #run_all(ensemble.GradientBoostingRegressor(), sta=4)
    
    #test()
