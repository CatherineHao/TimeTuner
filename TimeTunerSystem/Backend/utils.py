import pandas as pd
import numpy as np
from statsmodels.tsa.stattools import adfuller
from scipy.fftpack import fft, fftfreq
from statsmodels.tsa.stattools import acf

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
    fft_periods = (1 / freqs[top_k_idxs]).astype(int)
    return fft_periods

## input fft_periods, out put the corresponding acf value
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

## smoothed_data, input:
def return_all_smoothed(raw_dataset_path, smooth_para_list):
    