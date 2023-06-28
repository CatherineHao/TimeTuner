import sklearn
from sklearn.datasets import make_regression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.inspection import permutation_importance
from matplotlib import pyplot
import pandas as pd
# import stumpy
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import UnivariateSpline
import random
import time
import os
import random
import math
from datetime import datetime
from scipy import spatial
from tqdm import tqdm
from scipy.spatial.distance import pdist
import keras
from scipy.interpolate import UnivariateSpline
import copy
from scipy.stats import zscore
import tensorflow as tf
from sklearn import preprocessing
from keras.layers.core import Dense, Activation, Dropout
from keras.layers import Bidirectional,LSTM
from keras.models import Sequential
from keras import metrics
from pandas import DataFrame
from sklearn.preprocessing import MinMaxScaler
from keras import optimizers
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_percentage_error
from keras.models import load_model
# print(sklearn.__version__)
import shap
import tqdm

from tensorflow.keras.layers import Bidirectional,LSTM
from tensorflow.compat.v1 import ConfigProto
from tensorflow.compat.v1 import InteractiveSession

## Training of univariate data and calculation of SHAP Value
## 1. input the transformed dataset
data = pd.read_csv("./json_data_v1.0/SN_weighted_moving_average13_tot.csv") 
print(data.head())

s1 = MinMaxScaler()
data1 = s1.fit_transform(data['value'].values.reshape(-1,1))

# 2 experimental setups, according to the skip length, change the skip
skip = 1 
period_train = 120 * 6
period_test = 120

x = []
y = []
for i in range(0,len(data)-period_train-period_test,skip):
    x.append(data1[i:i+period_train,:])
    y.append(data1[i+period_train:i+period_train+period_test,:])
x = np.array(x)
y = np.array(y)
y = y.reshape(y.shape[0],y.shape[1])
print(x.shape,y.shape)
INDEX =int(len(x)*0.8)
x_train = x[:INDEX]
x_test  = x[INDEX:]
y_train = y[:INDEX]
y_test  = y[INDEX:]
print('x_test_length:',len(x_test))
print('y_test_length:',len(y_test))

# 3 training model
model = Sequential()
model.add(LSTM(8, input_shape=(period_train, 1))) 
model.add(Dense(units = 120, activation='relu')) # units = period_test
initial_learning_rate = 0.05
lr_schedule = tf.optimizers.schedules.ExponentialDecay(
    initial_learning_rate,
    decay_steps=10,
    decay_rate=0.96,
    staircase=True)
optimizer = keras.optimizers.adam_v2.Adam(learning_rate=lr_schedule(0))
model.compile(loss='mean_squared_error', optimizer=optimizer, metrics=['mean_absolute_percentage_error'])
model.fit(x_train, y_train, epochs = 100, batch_size = 32,validation_data=(x_test, y_test))
print(model.summary())
model.save("./model/weighted13_skip1.h5") # model saving path

# 3 or load trained model
# model = load_model("./model/weighted13_skip1.h5")

# 4 set all data for testing
all_test_x = x
all_test_y = y
predict_all = model.predict(all_test_x)
print('how many results do we have?:',len(predict_all))
predict_info = []
mse_info = []
rmse_info = []
mape_info = []
smooth_info = []
skip_info = []

for i in range(len(predict_all)):
    predict_info.append(s1.inverse_transform(predict_all)[i,:])
    data_Mse = mean_squared_error(s1.inverse_transform(predict_all)[i,:],s1.inverse_transform(all_test_y)[i,:])
    data_mape = mean_absolute_percentage_error(s1.inverse_transform(predict_all)[i,:],s1.inverse_transform(all_test_y)[i,:])
    #print('MSE:',data_Mse)
    mse_info.append(data_Mse)
    data_rmse = math.sqrt(data_Mse)
    #print('rmse:',data_rmse)
    rmse_info.append(data_rmse)
    mape_info.append(data_mape)
    smooth_info.append('weighted13') # according to the smooth parameter
    skip_info.append(skip)
    
print("Type of model:", type(model))
print("Type of data:", type(all_test_x))
print("test_tmp_x shape",all_test_x.shape)

explainer = shap.GradientExplainer(model,all_test_x)
shap_values = explainer.shap_values(all_test_x)

sample_shap = []
for x in range(len(all_test_x)):
    sum_shap = 0
    for i in range (0,120):
        for j in range(0,720):
            sum_shap = sum_shap + shap_values[i][x][j][0]
    sample_shap.append(sum_shap)

file_name = "./uni_data/weighted13_skip1_0.8.csv"
info = pd.DataFrame({'predict_data':predict_info,'mse':mse_info,'rmse':rmse_info,'mape':mape_info,'shap':sample_shap,'smooth':smooth_info,'skip':skip_info})
info.to_csv(file_name,encoding="UTF-8")