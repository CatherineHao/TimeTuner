import sklearn
# permutation feature importance with knn for regression
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
import matplotlib.pyplot as plt
import scipy.stats as stats
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_percentage_error
from sklearn.metrics import mean_absolute_percentage_error
# print(sklearn.__version__)

from tensorflow.keras.layers import Bidirectional,LSTM
from tensorflow.compat.v1 import ConfigProto
from tensorflow.compat.v1 import InteractiveSession


os.environ['CUDA_VISIBLE_DEVICES'] = '/gpu:0'

multi_data = pd.read_csv("./rawdata.csv")
multi_data.drop('date',axis=1,inplace=True)
multi_data.head()

values = multi_data.values
groups = [0,1,2,3,4,5]
i = 1
plt.figure()
for group in groups:
    plt.subplot(len(groups),1,i)
    plt.plot(values[:,group])
    plt.title(multi_data.columns[group],y=0.5,loc='right')
    i += 1
plt.show()

def series_to_supervised(input_data, predict_data, n_in, n_out, dropnan=True): 
    n_vars = 1 if type(input_data) is list else input_data.shape[1]
    df = pd.DataFrame(input_data)
    pre_df = pd.DataFrame(predict_data)
    cols, names = list(), list()
    # the input sequence (t-n, ... t-1)
    for i in range(n_in, 0, -1):
        cols.append(df.shift(i))
        names += [('var%d(t-%d)' % (j + 1, i)) for j in range(n_vars)]
    # the forecast sequence (t, t+1, ... t+n)
    for i in range(0, n_out):
        cols.append(pre_df.shift(-i))
        if i == 0:
            names += [('var%d(t)' % (j+1)) for j in range(n_vars)]
        else:
            names += [('var%d(t+%d)' % (j+1, i)) for j in range(n_vars)]
    # concat them together
    agg = pd.concat(cols, axis=1)
    agg.columns = names
    if dropnan:
        agg.dropna(inplace=True)
    return agg

# the task is to forecast the PM25 in 12 hours
predict_multi_data = pd.read_csv("./rawdata.csv")
predict_multi_data.drop('date',axis=1,inplace=True)

# according to the sampling parameter
skip = 24 

n_features = 6
train_len = 24
fore_len = 12

values = multi_data.values
pre_values = predict_multi_data.values

encoder  = preprocessing.LabelEncoder()
values[:,4] = encoder.fit_transform(values[:,4]) 
pre_values[:,4] = encoder.fit_transform(pre_values[:,4])
values = values.astype('float32')
pre_values = pre_values.astype('float32')

s1 = MinMaxScaler(feature_range=(0,1)) 
s2 = MinMaxScaler(feature_range=(0,1)) 

value1 = s1.fit_transform(values[:,0].reshape(-1,1))
value2 = s2.fit_transform(values[:,1:6]) 
new_values = np.append(value1, value2, axis=1)
pre_value1 = s1.fit_transform(pre_values[:,0].reshape(-1,1))
pre_value2 = s2.fit_transform(pre_values[:,1:6])
pre_new_values = np.append(pre_value1, pre_value2, axis=1)


# conversion of time-series data to supervised learning data
reframed = series_to_supervised(new_values, pre_new_values, train_len, fore_len) # (data, nin, nout)

print('column names:', reframed.columns)
del_col = []
for i in range(0,fore_len):
  for j in range(1,6):
    tmp = (train_len + i) * 6 + j
    del_col.append(tmp)

reframed.drop(reframed.columns[del_col], axis = 1, inplace = True)
print(reframed.head())
# print('the length of original reframed:', reframed)

sel_data_col = []
print(len(reframed))
for i in range(0,len(reframed),skip):
  sel_data_col.append(i)
reframed = reframed.iloc[sel_data_col]
print('the length of reframed after precessing:', reframed)

# split into train and test sets  
values = reframed.values
INDEX = int(len(values) * 0.8)

train = values[:INDEX,:]
test = values[INDEX:, :]    

# split into input and outputs
train_x, train_y = train[:, :-24],train[:, -12:] 
test_x, test_y = test[:, :-24], test[:, -12:]
# reshape input to be 3D [samples, timesteps, features]
train_x = train_x.reshape((train_x.shape[0], 1, train_x.shape[1]))
test_x = test_x.reshape((test_x.shape[0], 1, test_x.shape[1]))

print(train_x.shape, train_y.shape, test_x.shape, test_y.shape)

# model
model = Sequential()
model.add(LSTM(50, return_sequences=True, input_shape=(train_x.shape[1], train_x.shape[2]))) 
model.add(Dense(12)) 
sgd = optimizers.SGD(learning_rate = 0.001, decay = 1e-6, momentum = 0.9, nesterov = True)
model.compile(loss='mean_squared_error', optimizer='sgd',metrics=['mean_absolute_percentage_error'],run_eagerly=True)
print(model.summary())

# training model
history = model.fit(train_x, train_y, epochs=100, batch_size=128, validation_data=(test_x, test_y), verbose=2, shuffle=False) 
model.save("./model/rawdata_skip24.h5")  

# visualizing the loss
plt.plot(history.history['loss'], label='train')
plt.plot(history.history['val_loss'], label='test')
plt.legend()
plt.show()

predict_info = []
mse_info = []
rmse_info = []
smooth_info = []
skip_info = []

print('reframed length:', len(reframed))
all_test_data = reframed.values
all_x = all_test_data[:,:-24]
all_y = all_test_data[:,-12:]

# reshape input to be 3D [samples, timesteps, features]
all_x = all_x.reshape((all_x.shape[0], 1, all_x.shape[1]))

print(all_x.shape, all_y.shape)

# 预测值
all_yhat = model.predict(all_x)
all_yhat = all_yhat.reshape(-1 ,12)
print('shape',all_yhat.shape)
all_used_x = all_x.reshape((all_x.shape[0], all_x.shape[2]))

# invert scaling for forecast
inv_yhat = np.concatenate((all_used_x, all_yhat),axis=1)
inv_yhat = s1.inverse_transform(inv_yhat)
inv_yhat = inv_yhat[:, -12:]
print('forecast:',inv_yhat)
print('forecast len:',len(inv_yhat[0]))

# invert scaling for actual
inv_y = np.concatenate((all_used_x, all_y), axis=1)
inv_y = s1.inverse_transform(inv_y)
inv_y = inv_y[:, -12:]

# mse_info + rmse
for i in range(len(inv_yhat)):
  tmp_value = inv_yhat[i]
  predict_info.append(tmp_value)
  tmp_mse = mean_squared_error(inv_y[i], inv_yhat[i])
  tmp_rmse = math.sqrt(mean_squared_error(inv_y[i], inv_yhat[i]))
  mse_info.append(tmp_mse)
  rmse_info.append(tmp_rmse)
  smooth_info.append('raw')
  skip_info.append(skip)
  

raw_data = multi_data['pm25']
print('raw_length:',len(raw_data))
corr = []
num = 0
for i in range(0, len(raw_data)-24-12+1, skip):
    raw_tmp = raw_data[i + train_len : i + train_len + fore_len]
    # print('raw_data length:',len(raw_tmp))
    used_data = predict_info[num]
    used_list = [x for x in used_data.split(" ")] 
    while '' in used_list:
        used_list.remove('')
    used_list = [float(x) for x in used_list]
    r,p = stats.pearsonr(raw_tmp, used_list)
    #print('pearson:',r)
    corr.append(r)
    num = num + 1

print('data length',len(data))
print('corr length:', len(corr))

file_name = './raw_skip24.csv'  
info = pd.DataFrame()
info['predict_data'] = predict_info
info['mse'] = mse_info
info['rmse'] = rmse_info
info['smooth'] = smooth_info
info['skip'] = skip_info
info['corr'] = corr