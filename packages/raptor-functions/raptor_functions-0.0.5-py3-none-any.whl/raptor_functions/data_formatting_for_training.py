import pandas as pd
# 
def column_selection():
  # 
  option = 2
  # 
  if option == 1:
    x_columns = ['Data Points', ' Sen-1', ' Sen-2', ' Sen-3', ' Sen-4', ' Sen-5',
        ' Sen-6', ' Sen-7', ' Sen-8', ' Sen-9', ' Sen-10', ' Sen-11', ' Sen-12',
        ' Sen-13', ' Sen-14', ' Sen-15', ' Sen-16', ' Sen-17', ' Sen-18',
        ' Sen-19', ' Sen-20', ' Sen-21', ' Sen-22', ' Sen-23', ' Sen-24',
        'Humidity (%r.h.)']
  elif option == 2:
    x_columns = [' Sen-1', ' Sen-2', ' Sen-3', ' Sen-4', ' Sen-5',
          ' Sen-6', ' Sen-7', ' Sen-8', ' Sen-9', ' Sen-10', ' Sen-11', ' Sen-12']
  elif option == 3:
    x_columns = [' Sen-1', ' Sen-2', ' Sen-3', ' Sen-4', ' Sen-5',
          ' Sen-6', ' Sen-7', ' Sen-8', ' Sen-9', ' Sen-10', ' Sen-11', ' Sen-12', 'Humidity (%r.h.)']
  elif option == 4:  
    x_columns = [' Sen-1', ' Sen-2', ' Sen-3', ' Sen-4', ' Sen-5',
          ' Sen-6', ' Sen-7', ' Sen-8', ' Sen-9', ' Sen-10', ' Sen-11', ' Sen-12',
          ' Sen-13', ' Sen-14', ' Sen-15', ' Sen-16', ' Sen-17', ' Sen-18',
          ' Sen-19', ' Sen-20', ' Sen-21', ' Sen-22', ' Sen-23', ' Sen-24']
  elif option == 5:
    x_columns = [' Sen-1', ' Sen-2', ' Sen-3', ' Sen-4', ' Sen-5',
          ' Sen-6', ' Sen-7', ' Sen-8', ' Sen-9', ' Sen-10', ' Sen-11', ' Sen-12',
          ' Sen-13', ' Sen-14', ' Sen-15', ' Sen-16', ' Sen-17', ' Sen-18',
          ' Sen-19', ' Sen-20', ' Sen-21', ' Sen-22', ' Sen-23', ' Sen-24','Humidity (%r.h.)']
  else:
    x_columns = ['Data Points', ' Sen-1', ' Sen-2', ' Sen-3', ' Sen-4', ' Sen-5',
        ' Sen-6', ' Sen-7', ' Sen-8', ' Sen-9', ' Sen-10', ' Sen-11', ' Sen-12',
        ' Sen-13', ' Sen-14', ' Sen-15', ' Sen-16', ' Sen-17', ' Sen-18',
        ' Sen-19', ' Sen-20', ' Sen-21', ' Sen-22', ' Sen-23', ' Sen-24',
        'Humidity (%r.h.)']

  # 
  y_columns = ['Target']
  # 
  return x_columns, y_columns

def data_formatting(list_all_exp_with_target):
  # 
  df_all = pd.concat(list_all_exp_with_target)
  x_columns, y_columns = column_selection()
  X = df_all[x_columns]
  y = df_all[y_columns]
  # 
  return X, y










