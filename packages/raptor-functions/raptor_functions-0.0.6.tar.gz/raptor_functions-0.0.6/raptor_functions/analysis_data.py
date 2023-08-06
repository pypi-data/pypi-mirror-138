import pandas as pd
import glob
import os
from datetime import datetime
import pickle
import random
import matplotlib.pyplot as plt
import numpy as np
import re
from datetime import timedelta


# 
def get_all_files(path_to_measurements):
  # 
  list_files = glob.glob(path_to_measurements)
  # 
  df_list = []
  for i in range(len(list_files)):
    df_temp = pd.read_csv(list_files[i],sep='\t',skiprows=(0,1,2),header=(30))
    df_list.append(df_temp)
  # 
  return df_list, list_files

def find_header_value(field, filename):
  # Get first 6 lines
  with open(filename) as file:
      lines = [next(file) for x in range(30)]
  value = None
  for line in lines:
      if line.startswith(field):
          # Get the part of the string after the field name
          end_of_string = line[len(field):]
          string = end_of_string[:-1]
  return string
  
def get_datetime(list_files):
  # 
  date_list = []
  time_list = []
  date_time_list = []
  for i in range(len(list_files)):
    filename = list_files[i]
    field = "Date = "
    date = find_header_value(field, filename)
    date_list.append(date)
    field = "Time = "
    time = find_header_value(field, filename)
    time_list.append(time)
    date_time =  date + ' ' + time
    try:
      datetime_object = datetime.strptime(date_time, '%d/%m/%Y %H:%M:%S')
      date_time_list.append(datetime_object)
    except:
      date_time = date_time.replace("24", "00")
      datetime_object = datetime.strptime(date_time, '%d/%m/%Y %H:%M:%S')
      datetime_object = datetime_object + timedelta(days=1)
      date_time_list.append(datetime_object)
  # 
  return date_list, time_list, date_time_list


def load_ml_model(path_to_model):
  model = pickle.load(open(path_to_model, "rb"))
  return model

def random_sample(df_list,x_columns):
  i = random.randint(0, len(df_list))
  df_temp = df_list[i]
  df_temp = df_temp[x_columns]
  # df_temp = df_temp.iloc[:,[1,2,3,4,5,6,7,8,9,10,11,12]]
  j = random.randint(0, len(df_temp.count()))
  input_data_sample = df_temp.iloc[[j]]
  print(input_data_sample)
  # 
  x = input_data_sample.columns.tolist()
  y = input_data_sample.iloc[0].values.tolist()
  # 
  plt.bar(x, y)
  fig = plt.gcf()
  fig.autofmt_xdate()
  # 
  return input_data_sample

def sample_prediction(input_data_sample, model):
  # 
  print('Prediction: ' + str(model.predict(input_data_sample)))
  print('Prediction Probability: ' + str(model.predict_proba(input_data_sample)))


def calculate_prediction_and_probability(list_files, df_list, x_columns, model):
  # 
  prediction = []
  probability = []
  for i in range(len(list_files)):
    df_temp = df_list[i]
    df_temp = df_temp[x_columns]
    prediction.append([])
    probability.append([])
    for j in range(df_temp.count()[0]):
      input_data_sample = df_temp.iloc[[j]]
      prediction_temp =  int(model.predict(input_data_sample))
      prediction[i].append(prediction_temp)
      probability_temp =  model.predict_proba(input_data_sample)
      probability_temp = float(probability_temp[0][1])
      probability[i].append(probability_temp)
  
  return prediction, probability

def calculate_mean_probability(list_files, probability):
  # 
  mean_probability = []
  std_probability = []
  for i in range(len(list_files)):
    probability_array = np.array(probability[i])
    # 
    mean_probability_temp = np.mean(probability_array)
    mean_probability.append(mean_probability_temp)
    # 
    std_probability_temp = np.std(probability_array)
    std_probability.append(std_probability_temp)
  # 
  return mean_probability, std_probability

def plot_histogram_probabilities(mean_probability):
  # 
  plt.hist(mean_probability, 30) 
  plt.title("histogram") 
  plt.show()

def plot_probability_over_time(date_time_list,mean_probability):
  # 
  plt.style.use('seaborn-colorblind')
  plt.scatter(date_time_list,mean_probability)
  degrees = 70
  plt.axhline(y=0.5, color='r', linestyle='--', linewidth = '1')
  plt.xticks(rotation=degrees)
  plt.xlabel('Time')
  plt.ylabel('Probability of Covid')
  plt.ylim([0,1])
  plt.title('Probability of COVID vs. Time')
  time_now = str(datetime.now())
  plt.savefig('Plot'+time_now +'.png', dpi = 200, bbox_inches='tight')




def get_exp_stage(time, dpps=4, baseline=2, absorb=7, pause=1, desorb=5, flush=23):
    
    # dpps: data point per second

    baseline_time = baseline*dpps
    if time <= baseline_time:
        return 'baseline'
    absorb_time = baseline_time + absorb*dpps
    if time <= absorb_time:
        return 'absorb'
    pause_time = absorb_time + pause*dpps
    if time <= pause_time:
        return 'pause'
    desorb_time = pause_time + desorb*dpps
    if time <= desorb_time:
        return 'desorb'
    flush_time = desorb_time + flush*dpps
    if time <= flush_time:
        return 'flush'
    wait_time = flush_time + flush*dpps
    if time <= wait_time:
        return 'wait'


def rename_columns(df, has_label=False):
    for col in df.columns:
        if 'Sen' in col:
        # print(col[4:])
            new_col = re.findall('\d+', col)[0]
            # print(new_col)
            df.rename(columns={col:new_col}, inplace=True)
    df.rename(columns={'Data Points': 'data_points'}, inplace=True)
    df.rename(columns={'Humidity (%r.h.)':'humidity'}, inplace=True)
    if has_label:
        df['exp_type'] = df['exp_type'].apply(lambda x: 'Covid' if x == 'COVID' else x)
    return df




def preprocess_single_file(f, parse_time=False, parse_filename=False, rename_column=True):

    df_temp = pd.read_csv(f,sep='\t',header=(37))
    baseline, absorb, pause, desorb, flush = get_exp_stage_duration(f)
    df_temp['exp_stage'] = df_temp['Data Points'].apply(get_exp_stage)
    
    if parse_time:
      date = find_header_value('Date = ', f)
      df_temp['date'] = find_header_value('Date = ', f)
      df_temp['time_start'] = find_header_value('Time = ', f)
      df_temp['time_elapsed'] = df_temp.index / 4
      df_temp['timestamp'] = pd.to_datetime(date + " " + df_temp['time_start'])
      df_temp['time'] = pd.to_datetime(date + " " + df_temp['time_start']) + pd.to_timedelta(df_temp['time_elapsed'], unit='s')

    if parse_filename:
      df_temp['filename'] = f
    

    df_temp['label'] = get_label(f)


    if rename_column:
      df_temp = rename_columns(df_temp)

    return df_temp


def get_label(f):
    exp_name = find_header_value('Name of the experiment =', f)
    if exp_name[-2].isupper():
      return 'Covid'
    else:
      return 'Control'

def get_exp_stage_duration(f):
    baseline = float(find_header_value('Baseline = ', f))
    absorb = float(find_header_value('Absorb = ', f))
    pause = float(find_header_value('Pause = ', f))
    desorb = float(find_header_value('Desorb = ', f))
    flush = float(find_header_value('Flush = ', f))

    return baseline, absorb, pause, desorb, flush





def preprocess_all_files(path_to_measurements, parse_time=False, parse_filename=False, concat_files=True, rename_column=True):
  # 
  list_files = glob.glob(path_to_measurements)
  # 
  df_list = []
  for i, f in enumerate(list_files):

    df_temp = preprocess_single_file(f, parse_time=False, parse_filename=False)
    # print(df_list)
    df_list.append(df_temp)

  
  if concat_files:
    return pd.concat(df_list)
  else: 
    return df_list







