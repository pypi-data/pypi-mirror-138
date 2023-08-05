#!/usr/bin/env python
# coding: utf-8
"""
for rolling updates:
    - python3 setup.py bdist_wheel sdist
    - twine upload dist/*

"""
from welcome_page import *
from variables import *
from import_funcs import *
import pandas as pd 
import numpy as np
import re
import pandas as pd
import numpy as np
from tqdm import tqdm
from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from xgboost import XGBClassifier
import statistics
import lightgbm as lgb
import sys
from joblib import Parallel, delayed


def get_similarities(df):
    untouched_df = df.copy()
    lis = df.columns
    cat,num,other = cato_numo_other(df)
    for i in cat+num:
        if(df[i].isnull().any()):
            if i in cat:
                df = missing_value_treatment(df,i,cat,num,other,"cat")
            elif i in num:
                df = missing_value_treatment(df,i,cat,num,other,"num")
    df.drop(columns=other,inplace=True)
    features_we_considered = df.columns
    bins = int(np.log(df.shape[0]))
    for _ in num:
        df[_] = pd.qcut(df[_],bins)
    # convert all the catagorical col whose no of cat is greater then 2% then tag it into others 
    # one hot encode the whole df
    df = pd.get_dummies(data=df, columns=df.columns)
    assert df.shape[0] == untouched_df.shape[0]
    df.reset_index(inplace=True,drop=True)
    untouched_df.reset_index(inplace=True,drop=True)
    r = Parallel(n_jobs=64, verbose=0)(delayed(get_most_similar_vectors)(df.iloc[_].to_numpy(),df.to_numpy(),_) for _ in tqdm(df.index.values))
    df_scores = pd.concat([pd.DataFrame.from_dict(x, orient='index') for x in tqdm(r)])
    df_scores.reset_index(inplace=True,drop=True)
    df_scores.columns = ["best_similarity_score","best_similar_with_index_number","first_array","similar_array"]
    fin_df = pd.concat([untouched_df,df_scores[["best_similarity_score","best_similar_with_index_number"]]],axis=1)
    return fin_df