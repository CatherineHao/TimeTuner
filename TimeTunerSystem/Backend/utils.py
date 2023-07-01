import pandas as pd
import numpy as np
from statsmodels.tsa.stattools import adfuller
from scipy.fftpack import fft, fftfreq
from statsmodels.tsa.stattools import acf
import keras
import shap
from sklearn.preprocessing import MinMaxScaler, StandardScaler, Normalizer
from keras.layers.core import Dense, Activation, Dropout
from keras.layers import Bidirectional,LSTM
from keras.models import Sequential
from keras import metrics
from tensorflow.keras.layers import Bidirectional,LSTM
import json
from keras.callbacks import Callback
from keras import optimizers
from keras.models import load_model
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_percentage_error
import math
os.environ['CUDA_VISIBLE_DEVICES'] = '/gpu:0'

## para:input_dataset_path  return:the variable num
def get_variable_num(input_dataset_path):
    data = pd.read_csv(input_dataset_path)
    return len(data.columns)

## return dict {bool, value}
def check_stationary(input_dataset_path):
    data = pd.read_csv(input_dataset_path)
    result  = adfuller(data['value'])
    if result[1] < 0.01:
        is_stationary = 1
    else:
        is_stationary = 0
    stationary_value = result[1]
    stationarity_results = {is_stationary,stationary_value}
    return stationarity_results

## return periodicity and its acf_score, return top_k periods
def periodicity_num(input_dataset_path, top_k = 4):
    data = pd.read_csv(input_dataset_path)
    fft_series = fft(data['value'].values)
    power = np.abs(fft_series)
    sample_freq = fftreq(fft_series.size)
    
    pos_mask = np.where(sample_freq > 0)
    freqs = sample_freq[pos_mask]
    powers = power[pos_mask]
    top_k_idxs = np.argpartition(powers, -top_k)[-top_k_:]
    top_k_power = powers[top_k_idxs]
    global fft_periods
    fft_periods = (1 / freqs[top_k_idxs]).astype(int)
    return fft_periods

## input fft_periods, output the corresponding acf value
def calculate_acf(input_dataset_path, fft_periods):
    data = pd.read_csv(input_dataset_path)
    for lag in fft_periods:
        acf_score = acf(data['value'].values, nlags = lag)[-1]
    return acf_score

## determine if there are missing values in the data and return how many, return {bool, number}
def checking_missing_values(input_dataset_path):
    data = pd.read_csv(input_dataset_path)
    is_missing = data.isnull()
    missing_num = data.isnull().sum().sum()
    # each variable missing value
    column_missing = data.isnull().sum().to_dict()
    return {is_missing, missing_num, column_missing}

## return the information about the input dataset
def dataset_information(input_dataset_path):
    variable_num = get_variable_num(input_dataset_path)
    stationarity = check_stationary(input_dataset_path)
    fft_periods = periodicity_num(input_dataset_path,top_k)
    missing_value = checking_missing_values(input_dataset_path)
    return {'variable_num': variable_num, 'stationarity':stationarity, 'periodicity':periodicity_num, 'smooth_parameter':fft_periods, 'skip':fft_periods, 'missing_value': missing_value, 'reshape': -1}

#################################################

## smoothed_data, input:raw_dataset, according to the smooth_para_list, output the all smoothed files (concat)
def return_all_smoothed(raw_dataset_path, smooth_para_list):
    data = pd.read_csv(raw_dataset_path)
    smoothed_data = data.copy()
    for window_size in smooth_para_list:
        # moving average
        MA = smoothed_data.rolling(window=window_size,min_periods=1).mean()
        MA.columns = [f'MA- ({window_size})']
        smoothed_data = pd.concat([smoothed_data, MA], axis = 1)
        
        # WMA
        weights = pd.Series(range(1, window_size + 1))
        WMA = smoothed_data.rolling(window=window_size).apply(lambda x : (x * weights).sum() / weights.sum(), raw=True)
        WMA.columns = [f'WMA- ({window_size})']
        smooth_data = pd.concat([smooth_data, WMA], axis = 1)
    smooth_data.to_csv('./all_smoothed_data.csv', index = False)
    return smooth_data
    
##################################################

## check whether this dataset is univariate dataset (return 0) or multivariate dataset (return 1)
def check_multi_dataset(input_dataset_path):
    data = pd.read_csv(input_dataset_path)
    data = data.values
    shape = np.shape(data)
    if len(shape) == 1:
        return 0
    elif len(shape) == 2:
        return 1
    else:
        return "unable to determine dataset type."
class LossLogger(Callback):
    def __init__(self):
        super(LossLogger, self).__init__()
        self.train_loss = []
        self.val_loss = []

    def on_epoch_end(self, epoch, logs=None):
        self.train_loss.append(logs.get('loss'))
        self.val_loss.append(logs.get('val_loss'))

def univariate_model(input_univariate_data, reshaped_univariate_data, period_train, period_test, skip):
    x = []
    y = []
    for i in range(0,len(input_univariate_data)-period_train-period_test,skip):
        x.append(reshaped_univariate_data[i:i+period_train,:])
        y.append(reshaped_univariate_data[i+period_train:i+period_train+period_test,:])
    x = np.array(x)
    y = np.array(y)
    y = y.reshape(y.shape[0],y.shape[1])
    print(x.shape,y.shape)
    INDEX =int(len(x)*0.8)
    x_train = x[:INDEX]
    x_test  = x[INDEX:]
    y_train = y[:INDEX]
    y_test  = y[INDEX:]
    
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
    loss_logger = LossLogger()
    model.compile(loss='mean_squared_error', optimizer=optimizer, metrics=['mean_absolute_percentage_error'])
    model.fit(x_train, y_train, epochs = 100, batch_size = 32,validation_data=(x_test, y_test), callbacks=[loss_logger])
    print('the model information for univariate data:', model.summary())
    train_rmse = loss_logger.train_loss[-1]
    val_rmse = loss_logger.val_loss[-1]
    return train_rmse, val_rmse
    
## input the univariate dataset and output the json object
def overview_univariate_performance(input_dataset_path):
    smooth_data = return_all_smoothed(input_dataset_path, fft_periods)
    
    results = []
    skip = fft_periods
    period_train = 720
    period_test = 120
    
    ## different process methods
    for i in range(3):
        if i ==0:
            s = MinMaxScaler()
            for column_name, column_data in smooth_data.items():
                for skip_item in skip:
                    reshaped_univariate_data = s.fit_transform(column_data.reshape(-1,1))
                    train_metric, test_metric = univariate_model(column_data, reshaped_univariate_data, period_train, period_test, skip_item)
                    acf = np.correlate(column_data - np.mean(column_data), column_data - np.mean(column_data), mode = 'full')
                    acf_value = acf[len(column_data) - 1:]
                    result = {
                                "reshape":"min_max_scaler",
                                "smooth":column_name,
                                "skip":skip_item,
                                "train_rmse":train_metric,
                                "val_rmse":test_metric,
                                "ACF": acf_value
                                }
                    results.append(result)
            json_data = {
                "results": results
            }
        elif i == 1:
            s = StandardScaler()
            for column_name, column_data in smooth_data.items():
                for skip_item in skip:
                    reshaped_univariate_data = s.fit_transform(column_data)
                    train_metric, test_metric = univariate_model(column_data, reshaped_univariate_data, period_train, period_test, skip_item)
                    acf = np.correlate(column_data - np.mean(column_data), column_data - np.mean(column_data), mode = 'full')
                    acf_value = acf[len(column_data) - 1:]
                    result = {
                                "reshape":"standard_scaler",
                                "smooth":column_name,
                                "skip":skip_item,
                                "train_rmse":train_metric,
                                "val_rmse":test_metric,
                                "ACF": acf_value
                                }
                    results.append(result)
            json_data = {
                "results": results
            }
        else:
            s = Normalizer()
            for column_name, column_data in smooth_data.items():
                for skip_item in skip:
                    reshaped_univariate_data = s.fit_transform(column_data)
                    train_metric, test_metric = univariate_model(column_data, reshaped_univariate_data, period_train, period_test, skip_item)
                    acf = np.correlate(column_data - np.mean(column_data), column_data - np.mean(column_data), mode = 'full')
                    acf_value = acf[len(column_data) - 1:]
                    result = {
                                "reshape":"normalize",
                                "smooth":column_name,
                                "skip":skip_item,
                                "train_rmse":train_metric,
                                "val_rmse":test_metric,
                                "ACF": acf_value
                                }
                    results.append(result)
            json_data = {
                "results": results
            }
    return json.dumps(json_data)

# for multi_data, turn the time-series data to supervised data
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

def multivariate_model(values, pre_values, period_train, period_test, skip, n_features):
    reframed = series_to_supervised(values, pre_values, period_train, period_test) # (data, nin, nout)
    del_col = []
    for i in range(0, period_test):
        for j in range(1, n_features):
            tmp = (period_train + i) * n_features + j
            del_col.append(tmp)
    reframed.drop(reframed.columns[del_col], axis = 1, inplace = True)
    sel_data_col = []
    for i in range(0,len(reframed),skip):
        sel_data_col.append(i)
    reframed = reframed.iloc[sel_data_col]

    # split into train and test sets  
    values = reframed.values
    INDEX = int(len(values) * 0.8)
    
    train = values[:INDEX,:]
    test = values[INDEX:, :]  
    
    # split into input and outputs
    train_x, train_y = train[:, :-period_train],train[:, -period_test:] 
    test_x, test_y = test[:, :-period_train], test[:, -period_test:]
    # reshape input to be 3D [samples, timesteps, features]
    train_x = train_x.reshape((train_x.shape[0], 1, train_x.shape[1]))
    test_x = test_x.reshape((test_x.shape[0], 1, test_x.shape[1]))
    
    # model
    model = Sequential()
    model.add(LSTM(50, return_sequences=True, input_shape=(train_x.shape[1], train_x.shape[2]))) 
    model.add(Dense(12)) 
    sgd = optimizers.SGD(learning_rate = 0.001, decay = 1e-6, momentum = 0.9, nesterov = True)
    loss_logger = LossLogger()
    model.compile(loss='mean_squared_error', optimizer='sgd',metrics=['mean_absolute_percentage_error'],run_eagerly=True)
    model.fit(train_x, train_y, epochs=100, batch_size=128, validation_data=(test_x, test_y), verbose=2, shuffle=False, callbacks=[loss_logger]) 
    train_rmse = loss_logger.train_loss[-1]
    val_rmse = loss_logger.val_loss[-1]
    return train_rmse, val_rmse        

## input the univariate dataset and output the json object       
def overview_multivariate_performance(input_dataset_path):
    smooth_data = return_all_smoothed(input_dataset_path, fft_periods)
    smooth_data.drop('date',axis=1,inplace=True)
    variable_num = get_variable_num(smooth_data)
    
    n_features = variable_num
    skip = fft_periods
    period_train = 24
    period_test = 12
    values = smooth_data.values
    pre_values = smooth_data.values
    results = []
    
    # different process methods
    for i in range(3):
        if i == 0:
            s = MinMaxScaler(feature_range=(0,1))
            values = s.fit_transform(values)
            pre_values = s.fit_transform(pre_values)
            for index in range(0, len(values), n_features):
                end = index + n_features
                columns_to_extract = values.columns[index:end]
                pre_columns_to_extract = pre_values.columns[index:end]
                for skip_item in skip:
                    train_metric, test_metric = multivariate_model(columns_to_extract, pre_columns_to_extract, period_train, period_test, skip, n_features)
                    acf = np.correlate(columns_to_extract[0] - np.mean(columns_to_extract[0]), columns_to_extract[0] - np.mean(columns_to_extract[0]), mode = 'full')
                    acf_value = acf[len(columns_to_extract[0]) - 1:]
                    result = {
                                "reshape":"normalize",
                                "smooth":index,
                                "skip":skip_item,
                                "train_rmse":train_metric,
                                "val_rmse":test_metric,
                                "ACF": acf_value
                                }
            results.append(result)
            json_data = {
                "results": results
                }
        elif i == 1:
            s = StandardScaler()
            values = s.fit_transform(values)
            pre_values = s.fit_transform(pre_values)
            for index in range(0, len(values), n_features):
                end = index + n_features
                columns_to_extract = values.columns[index:end]
                pre_columns_to_extract = pre_values.columns[index:end]
                for skip_item in skip:
                    train_metric, test_metric = multivariate_model(columns_to_extract, pre_columns_to_extract, period_train, period_test, skip, n_features)
                    acf = np.correlate(columns_to_extract[0] - np.mean(columns_to_extract[0]), columns_to_extract[0] - np.mean(columns_to_extract[0]), mode = 'full')
                    acf_value = acf[len(columns_to_extract[0]) - 1:]
                    result = {
                                "reshape":"standard_scaler",
                                "smooth":index,
                                "skip":skip_item,
                                "train_rmse":train_metric,
                                "val_rmse":test_metric,
                                "ACF": acf_value
                                }
            results.append(result)
            json_data = {
                "results": results
                }
        else:
            s = Normalizer()
            values = s.fit_transform(values)
            pre_values = s.fit_transform(pre_values)
            for index in range(0, len(values), n_features):
                end = index + n_features
                columns_to_extract = values.columns[index:end]
                pre_columns_to_extract = pre_values.columns[index:end]
                for skip_item in skip:
                    train_metric, test_metric = multivariate_model(columns_to_extract, pre_columns_to_extract, period_train, period_test, skip, n_features)
                    acf = np.correlate(columns_to_extract[0] - np.mean(columns_to_extract[0]), columns_to_extract[0] - np.mean(columns_to_extract[0]), mode = 'full')
                    acf_value = acf[len(columns_to_extract[0]) - 1:]
                    result = {
                                "reshape":"normalize",
                                "smooth":index,
                                "skip":skip_item,
                                "train_rmse":train_metric,
                                "val_rmse":test_metric,
                                "ACF": acf_value
                                }
            results.append(result)
            json_data = {
                "results": results
                }
    return json.dumps(json_data)
                  
## return the the overview model performance for univariate dataset and multivariate model
def overview_performance(input_dataset_path):
    index = check_multi_dataset(input_dataset_path)
    if index == 0: # the input dataset is univariate dataset
        univariate_json = overview_univariate_performance(input_dataset_path)
        return univariate_json
    elif index == 1: # the input dataset is multivariate dataset
        multivariate_json = overview_multivariate_performance(input_dataset_path)
        return multivariate_json
    
##################################################

## return the predictions including the SHAP values
def predictions_info(input_dataset_path, model_path, skip, file_name):
    if file_name == "Sunspots.csv":
        period_train = 720
        period_test = 120
    elif file_name == "Pm25.csv":
        period_train = 24
        period_test = 12
    model = load_model(model_path)
    data = pd.read_csv(input_dataset_path)
    info = []
    for i in range(3):
        if i == 0:
            s = MinMaxScaler()
            process_data = s.fit_transform(data['value'].values)
            x = []
            y = []
            for i in range(0,len(data)-period_train-period_test,skip):
                x.append(process_data[i:i+period_train,:])
                y.append(process_data[i+period_train:i+period_train+period_test,:])
            x = np.array(x)
            y = np.array(y)
            y = y.reshape(y.shape[0],y.shape[1])
            predict_result = model.predict(x)
            predict_info = []
            rmse_info = []
            skip_info = []
            for i in range(len(predict_result)):
                predict_info.append(s.inverse_transform(predict_result)[i,:])
                data_Mse = mean_squared_error(s.inverse_transform(predict_result)[i,:],s.inverse_transform(y)[i,:])
                data_mape = mean_absolute_percentage_error(s.inverse_transform(predict_result)[i,:],s.inverse_transform(y)[i,:])
                data_rmse = math.sqrt(data_Mse)
                rmse_info.append(data_rmse)
                skip_info.append(skip)
            explainer = shap.GradientExplainer(model,x)
            shap_values = explainer.shap_values(x)
            sample_shap = []
            for index in range(len(x)):
                sum_shap = 0
                for i in range (0,period_test):
                    for j in range(0,period_train):
                        sum_shap = sum_shap + shap_values[i][index][j][0]
                sample_shap.append(sum_shap)
            tmp_info = {'predict_data':predict_info,
                    'reshape':"min_max_scaler",
                    'rmse':rmse_info,
                    'shap':sample_shap,
                    'skip':skip_info
                    }
            info.append(tmp_info)
            json_data = {
                "results": info
            }
        elif i == 1:
            s = StandardScaler()
            process_data = s.fit_transform(data['value'].values)
            x = []
            y = []
            for i in range(0,len(data)-period_train-period_test,skip):
                x.append(process_data[i:i+period_train,:])
                y.append(process_data[i+period_train:i+period_train+period_test,:])
            x = np.array(x)
            y = np.array(y)
            y = y.reshape(y.shape[0],y.shape[1])
            predict_result = model.predict(x)
            predict_info = []
            rmse_info = []
            skip_info = []
            for i in range(len(predict_result )):
                predict_info.append(s.inverse_transform(predict_result )[i,:])
                data_Mse = mean_squared_error(s.inverse_transform(predict_result )[i,:],s.inverse_transform(y)[i,:])
                data_mape = mean_absolute_percentage_error(s.inverse_transform(predict_result)[i,:],s.inverse_transform(y)[i,:])
                data_rmse = math.sqrt(data_Mse)
                rmse_info.append(data_rmse)
                skip_info.append(skip)
            explainer = shap.GradientExplainer(model,x)
            shap_values = explainer.shap_values(x)
            sample_shap = []
            for index in range(len(x)):
                sum_shap = 0
                for i in range (0,period_test):
                    for j in range(0,period_train):
                        sum_shap = sum_shap + shap_values[i][index][j][0]
                sample_shap.append(sum_shap)
            tmp_info = {'predict_data':predict_info,
                    'reshape':"standard_scaler",
                    'rmse':rmse_info,
                    'shap':sample_shap,
                    'skip':skip_info
                    }
            info.append(tmp_info)
            json_data = {
                "results": info
            }
        else:
            s = Normalizer()
            process_data = s.fit_transform(data['value'].values)
            x = []
            y = []
            for i in range(0,len(data)-period_train-period_test,skip):
                x.append(process_data[i:i+period_train,:])
                y.append(process_data[i+period_train:i+period_train+period_test,:])
            x = np.array(x)
            y = np.array(y)
            y = y.reshape(y.shape[0],y.shape[1])
            predict_result = model.predict(x)
            predict_info = []
            rmse_info = []
            skip_info = []
            for i in range(len(predict_result)):
                predict_info.append(s.inverse_transform(predict_result )[i,:])
                data_Mse = mean_squared_error(s.inverse_transform(predict_result )[i,:],s.inverse_transform(y)[i,:])
                data_mape = mean_absolute_percentage_error(s.inverse_transform(predict_result)[i,:],s.inverse_transform(y)[i,:])
                data_rmse = math.sqrt(data_Mse)
                rmse_info.append(data_rmse)
                skip_info.append(skip)
            explainer = shap.GradientExplainer(model,x)
            shap_values = explainer.shap_values(x)
            sample_shap = []
            for index in range(len(x)):
                sum_shap = 0
                for i in range (0,period_test):
                    for j in range(0,period_train):
                        sum_shap = sum_shap + shap_values[i][index][j][0]
                sample_shap.append(sum_shap)
            tmp_info = {'predict_data':predict_info,
                    'reshape':"normalize",
                    'rmse':rmse_info,
                    'shap':sample_shap,
                    'skip':skip_info
                    }
            info.append(tmp_info)
        json_data = {
            "results": info
        }
    return json.dumps(json_data)