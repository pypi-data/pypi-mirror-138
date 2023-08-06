import pandas as pd
import matplotlib.pyplot as plt
from IPython.display import clear_output
from time import sleep

# 
def sensor_channel_response_bar(df,date_time,x_columns):
  df = df[x_columns]
  x = df.columns.tolist()
  # 
  fig = plt.figure()
  plt.title(str(date_time))
  for i in range(len(df)):
    y = df.iloc[i].values.tolist()
    plt.bar(x, y)
    plt.show()
    plt.ylim([0,500])
    plt.ylabel('mV')
    fig = plt.gcf()
    fig.autofmt_xdate()
    sleep(0.05)
    clear_output(wait=True)

def sensor_channel_response_line(df,date_time,x_columns):
  df = df[x_columns]
  x = df.columns.tolist()
  y = df.values.tolist()
  # 
  fig = plt.figure()
  plt.title(str(date_time))
  plt.plot(y)
  plt.ylim([0,500])
  plt.ylabel('mV')
  fig = plt.gcf()
  fig.autofmt_xdate()
  plt.legend(x)
  plt.show()

