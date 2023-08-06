import pandas as pd

def read_validated_data(path_to_validated_data):
  # 
  # 24 hours, 48 hours and 72 hours
  # 
  # Read data
  # 24 HOURS
  # 
  # SET 1
  # 24 hours Control experiments - 3 repeats
  df_24h_control_set1_1 = pd.read_csv(path_to_validated_data + 'Tissue Culture Raw Data Files/24H 1 Control_14_15_26.28.txt',sep='\t',skiprows=(0,1,2),header=(34))
  df_24h_control_set1_2 = pd.read_csv(path_to_validated_data + 'Tissue Culture Raw Data Files/24H 1 Control_14_16_06.28.txt',sep='\t',skiprows=(0,1,2),header=(34))
  df_24h_control_set1_3 = pd.read_csv(path_to_validated_data + 'Tissue Culture Raw Data Files/24H 1 Control_14_16_45.28.txt',sep='\t',skiprows=(0,1,2),header=(34))
  # 24 hours COVID experiments - 3 repeats
  df_24h_covid_set1_1 = pd.read_csv(path_to_validated_data + 'Tissue Culture Raw Data Files/24H 1 COVID_14_42_45.28.txt',sep='\t',skiprows=(0,1,2),header=(34))
  df_24h_covid_set1_2 = pd.read_csv(path_to_validated_data + 'Tissue Culture Raw Data Files/24H 1 COVID_14_43_24.28.txt',sep='\t',skiprows=(0,1,2),header=(34))
  df_24h_covid_set1_3 = pd.read_csv(path_to_validated_data + 'Tissue Culture Raw Data Files/24H 1 COVID_14_44_03.28.txt',sep='\t',skiprows=(0,1,2),header=(34))
  # 
  # SET 2
  # 24 hours Control experiments - 3 repeats
  df_24h_control_set2_1 = pd.read_csv(path_to_validated_data + 'Tissue Culture Raw Data Files/24H 2 Control_14_18_15.28.txt',sep='\t',skiprows=(0,1,2),header=(34))
  df_24h_control_set2_2 = pd.read_csv(path_to_validated_data + 'Tissue Culture Raw Data Files/24H 2 Control_14_18_54.28.txt',sep='\t',skiprows=(0,1,2),header=(34))
  df_24h_control_set2_3 = pd.read_csv(path_to_validated_data + 'Tissue Culture Raw Data Files/24H 2 Control_14_19_33.28.txt',sep='\t',skiprows=(0,1,2),header=(34))
  # 24 hours COVID experiments - 3 repeats
  df_24h_covid_set2_1 = pd.read_csv(path_to_validated_data + 'Tissue Culture Raw Data Files/24H 2 COVID_14_48_37.28.txt',sep='\t',skiprows=(0,1,2),header=(34))
  df_24h_covid_set2_2 = pd.read_csv(path_to_validated_data + 'Tissue Culture Raw Data Files/24H 2 COVID_14_49_16.28.txt',sep='\t',skiprows=(0,1,2),header=(34))
  df_24h_covid_set2_3 = pd.read_csv(path_to_validated_data + 'Tissue Culture Raw Data Files/24H 2 COVID_14_49_55.28.txt',sep='\t',skiprows=(0,1,2),header=(34))
  # 
  # SET 3
  # 24 hours Control experiments - 3 repeats
  df_24h_control_set3_1 = pd.read_csv(path_to_validated_data + 'Tissue Culture Raw Data Files/24H 3 Control_14_12_45.28.txt',sep='\t',skiprows=(0,1,2),header=(34))
  df_24h_control_set3_2 = pd.read_csv(path_to_validated_data + 'Tissue Culture Raw Data Files/24H 3 Control_14_13_22.28.txt',sep='\t',skiprows=(0,1,2),header=(34))
  df_24h_control_set3_3 = pd.read_csv(path_to_validated_data + 'Tissue Culture Raw Data Files/24H 3 Control_14_14_01.28.txt',sep='\t',skiprows=(0,1,2),header=(34))
  # 24 hours COVID experiments - 3 repeats
  df_24h_covid_set3_1 = pd.read_csv(path_to_validated_data + 'Tissue Culture Raw Data Files/24H 3 COVID_14_45_31.28.txt',sep='\t',skiprows=(0,1,2),header=(34))
  df_24h_covid_set3_2 = pd.read_csv(path_to_validated_data + 'Tissue Culture Raw Data Files/24H 3 COVID_14_46_10.28.txt',sep='\t',skiprows=(0,1,2),header=(34))
  df_24h_covid_set3_3 = pd.read_csv(path_to_validated_data + 'Tissue Culture Raw Data Files/24H 3 COVID_14_46_49.28.txt',sep='\t',skiprows=(0,1,2),header=(34))
  # 
  # Read data
  # 48 HOURS
  # 
  # SET 1
  # 48 hours Control experiments - 3 repeats
  df_48h_control_set1_1 = pd.read_csv(path_to_validated_data + 'Tissue Culture Raw Data Files/48H 1 Control_14_27_13.28.txt',sep='\t',skiprows=(0,1,2),header=(34))
  df_48h_control_set1_2 = pd.read_csv(path_to_validated_data + 'Tissue Culture Raw Data Files/48H 1 Control_14_27_52.28.txt',sep='\t',skiprows=(0,1,2),header=(34))
  df_48h_control_set1_3 = pd.read_csv(path_to_validated_data + 'Tissue Culture Raw Data Files/48H 1 Control_14_28_31.28.txt',sep='\t',skiprows=(0,1,2),header=(34))
  # 48 hours COVID experiments - 3 repeats
  df_48h_covid_set1_1 = pd.read_csv(path_to_validated_data + 'Tissue Culture Raw Data Files/48H 1 COVID_14_56_24.28.txt',sep='\t',skiprows=(0,1,2),header=(34))
  df_48h_covid_set1_2 = pd.read_csv(path_to_validated_data + 'Tissue Culture Raw Data Files/48H 1 COVID_14_57_03.28.txt',sep='\t',skiprows=(0,1,2),header=(34))
  df_48h_covid_set1_3 = pd.read_csv(path_to_validated_data + 'Tissue Culture Raw Data Files/48H 1 COVID_14_57_42.28.txt',sep='\t',skiprows=(0,1,2),header=(34))
  # 
  # SET 2
  # 48 hours Control experiments - 3 repeats
  df_48h_control_set2_1 = pd.read_csv(path_to_validated_data + 'Tissue Culture Raw Data Files/48H 2 Control_14_24_25.28.txt',sep='\t',skiprows=(0,1,2),header=(34))
  df_48h_control_set2_2 = pd.read_csv(path_to_validated_data + 'Tissue Culture Raw Data Files/48H 2 Control_14_25_04.28.txt',sep='\t',skiprows=(0,1,2),header=(34))
  df_48h_control_set2_3 = pd.read_csv(path_to_validated_data + 'Tissue Culture Raw Data Files/48H 2 Control_14_25_43.28.txt',sep='\t',skiprows=(0,1,2),header=(34))
  # 48 hours COVID experiments - 3 repeats
  df_48h_covid_set2_1 = pd.read_csv(path_to_validated_data + 'Tissue Culture Raw Data Files/48H 2 COVID_14_53_41.28.txt',sep='\t',skiprows=(0,1,2),header=(34))
  df_48h_covid_set2_2 = pd.read_csv(path_to_validated_data + 'Tissue Culture Raw Data Files/48H 2 COVID_14_54_20.28.txt',sep='\t',skiprows=(0,1,2),header=(34))
  df_48h_covid_set2_3 = pd.read_csv(path_to_validated_data + 'Tissue Culture Raw Data Files/48H 2 COVID_14_54_59.28.txt',sep='\t',skiprows=(0,1,2),header=(34))
  # 
  # SET 3
  # 48 hours Control experiments - 3 repeats
  df_48h_control_set3_1 = pd.read_csv(path_to_validated_data + 'Tissue Culture Raw Data Files/48H 3 Control_14_21_40.28.txt',sep='\t',skiprows=(0,1,2),header=(34))
  df_48h_control_set3_2 = pd.read_csv(path_to_validated_data + 'Tissue Culture Raw Data Files/48H 3 Control_14_22_19.28.txt',sep='\t',skiprows=(0,1,2),header=(34))
  df_48h_control_set3_3 = pd.read_csv(path_to_validated_data + 'Tissue Culture Raw Data Files/48H 3 Control_14_22_58.28.txt',sep='\t',skiprows=(0,1,2),header=(34))
  # 48 hours COVID experiments - 3 repeats
  df_48h_covid_set3_1 = pd.read_csv(path_to_validated_data + 'Tissue Culture Raw Data Files/48H 3 COVID_14_59_12.28.txt',sep='\t',skiprows=(0,1,2),header=(34))
  df_48h_covid_set3_2 = pd.read_csv(path_to_validated_data + 'Tissue Culture Raw Data Files/48H 3 COVID_15_00_01.28.txt',sep='\t',skiprows=(0,1,2),header=(34))
  df_48h_covid_set3_3 = pd.read_csv(path_to_validated_data + 'Tissue Culture Raw Data Files/48H 3 COVID_15_00_40.28.txt',sep='\t',skiprows=(0,1,2),header=(34))
  # 
    # Read data
  # 72 HOURS
  # 
  # SET 1
  # 72 hours Control experiments - 3 repeats
  df_72h_control_set1_1 = pd.read_csv(path_to_validated_data + 'Tissue Culture Raw Data Files/72H 1 Control_14_32_48.28.txt',sep='\t',skiprows=(0,1,2),header=(34))
  df_72h_control_set1_2 = pd.read_csv(path_to_validated_data + 'Tissue Culture Raw Data Files/72H 1 Control_14_33_27.28.txt',sep='\t',skiprows=(0,1,2),header=(34))
  df_72h_control_set1_3 = pd.read_csv(path_to_validated_data + 'Tissue Culture Raw Data Files/72H 1 Control_14_34_07.28.txt',sep='\t',skiprows=(0,1,2),header=(34))
  # 72 hours COVID experiments - 3 repeats
  df_72h_covid_set1_1 = pd.read_csv(path_to_validated_data + 'Tissue Culture Raw Data Files/72H 1 COVID_15_05_34.28.txt',sep='\t',skiprows=(0,1,2),header=(34))
  df_72h_covid_set1_2 = pd.read_csv(path_to_validated_data + 'Tissue Culture Raw Data Files/72H 1 COVID_15_06_13.28.txt',sep='\t',skiprows=(0,1,2),header=(34))
  df_72h_covid_set1_3 = pd.read_csv(path_to_validated_data + 'Tissue Culture Raw Data Files/72H 1 COVID_15_06_52.28.txt',sep='\t',skiprows=(0,1,2),header=(34))
  # 
  # SET 2
  # 72 hours Control experiments - 3 repeats
  df_72h_control_set2_1 = pd.read_csv(path_to_validated_data + 'Tissue Culture Raw Data Files/72H 2 Control_14_35_34.28.txt',sep='\t',skiprows=(0,1,2),header=(34))
  df_72h_control_set2_2 = pd.read_csv(path_to_validated_data + 'Tissue Culture Raw Data Files/72H 2 Control_14_36_11.28.txt',sep='\t',skiprows=(0,1,2),header=(34))
  df_72h_control_set2_3 = pd.read_csv(path_to_validated_data + 'Tissue Culture Raw Data Files/72H 2 Control_14_36_50.28.txt',sep='\t',skiprows=(0,1,2),header=(34))
  # 72 hours COVID experiments - 3 repeats
  df_72h_covid_set2_1 = pd.read_csv(path_to_validated_data + 'Tissue Culture Raw Data Files/72H 2 COVID_15_08_20.28.txt',sep='\t',skiprows=(0,1,2),header=(34))
  df_72h_covid_set2_2 = pd.read_csv(path_to_validated_data + 'Tissue Culture Raw Data Files/72H 2 COVID_15_08_59.28.txt',sep='\t',skiprows=(0,1,2),header=(34))
  df_72h_covid_set2_3 = pd.read_csv(path_to_validated_data + 'Tissue Culture Raw Data Files/72H 2 COVID_15_09_38.28.txt',sep='\t',skiprows=(0,1,2),header=(34))
  # 
  # SET 3
  # 72 hours Control experiments - 3 repeats
  df_72h_control_set3_1 = pd.read_csv(path_to_validated_data + 'Tissue Culture Raw Data Files/72H 3 Control_14_30_02.28.txt',sep='\t',skiprows=(0,1,2),header=(34))
  df_72h_control_set3_2 = pd.read_csv(path_to_validated_data + 'Tissue Culture Raw Data Files/72H 3 Control_14_30_41.28.txt',sep='\t',skiprows=(0,1,2),header=(34))
  df_72h_control_set3_3 = pd.read_csv(path_to_validated_data + 'Tissue Culture Raw Data Files/72H 3 Control_14_31_21.28.txt',sep='\t',skiprows=(0,1,2),header=(34))
  # 72 hours COVID experiments - 3 repeats
  df_72h_covid_set3_1 = pd.read_csv(path_to_validated_data + 'Tissue Culture Raw Data Files/72H 3 COVID_15_02_29.28.txt',sep='\t',skiprows=(0,1,2),header=(34))
  df_72h_covid_set3_2 = pd.read_csv(path_to_validated_data + 'Tissue Culture Raw Data Files/72H 3 COVID_15_03_09.28.txt',sep='\t',skiprows=(0,1,2),header=(34))
  df_72h_covid_set3_3 = pd.read_csv(path_to_validated_data + 'Tissue Culture Raw Data Files/72H 3 COVID_15_03_48.28.txt',sep='\t',skiprows=(0,1,2),header=(34))
  # 
  # LISTS
  # Get all the experiments dataframes in a list
  list_all_exp = [df_24h_control_set1_1, df_24h_control_set1_2, df_24h_control_set1_3,
                df_24h_control_set2_1, df_24h_control_set2_2, df_24h_control_set2_3,
                df_24h_control_set3_1, df_24h_control_set2_2, df_24h_control_set3_3,
                df_48h_control_set1_1, df_48h_control_set1_2, df_48h_control_set1_3,
                df_48h_control_set2_1, df_48h_control_set2_2, df_48h_control_set2_3,
                df_48h_control_set3_1, df_48h_control_set3_2, df_48h_control_set3_3,
                df_72h_control_set1_1, df_72h_control_set1_2, df_72h_control_set1_3,
                df_72h_control_set2_1, df_48h_control_set2_2, df_72h_control_set2_3,
                df_72h_control_set3_1, df_72h_control_set3_2, df_72h_control_set3_3,
                df_24h_covid_set1_1, df_24h_covid_set1_2, df_24h_covid_set1_3,
                df_24h_covid_set2_1, df_24h_covid_set2_2, df_24h_covid_set2_3,
                df_24h_covid_set3_1, df_24h_covid_set2_2, df_24h_covid_set3_3,
                df_48h_covid_set1_1, df_48h_covid_set1_2, df_48h_covid_set1_3,
                df_48h_covid_set2_1, df_48h_covid_set2_2, df_48h_covid_set2_3,
                df_48h_covid_set3_1, df_48h_covid_set3_2, df_48h_covid_set3_3,
                df_72h_covid_set1_1, df_72h_covid_set1_2, df_72h_covid_set1_3,
                df_72h_covid_set2_1, df_48h_covid_set2_2, df_72h_covid_set2_3,
                df_72h_covid_set3_1, df_72h_covid_set3_2, df_72h_covid_set3_3]
  # 
  list_all_exp_names = ['df_24h_control_set1_1', 'df_24h_control_set1_2', 'df_24h_control_set1_3',
                      'df_24h_control_set2_1', 'df_24h_control_set2_2', 'df_24h_control_set2_3',
                      'df_24h_control_set3_1', 'df_24h_control_set2_2', 'df_24h_control_set3_3',
                      'df_48h_control_set1_1', 'df_48h_control_set1_2', 'df_48h_control_set1_3',
                      'df_48h_control_set2_1', 'df_48h_control_set2_2', 'df_48h_control_set2_3',
                      'df_48h_control_set3_1', 'df_48h_control_set3_2', 'df_48h_control_set3_3',
                      'df_72h_control_set1_1', 'df_72h_control_set1_2', 'df_72h_control_set1_3',
                      'df_72h_control_set2_1', 'df_48h_control_set2_2', 'df_72h_control_set2_3',
                      'df_72h_control_set3_1', 'df_72h_control_set3_2', 'df_72h_control_set3_3',
                      'df_24h_covid_set1_1', 'df_24h_covid_set1_2', 'df_24h_covid_set1_3',
                      'df_24h_covid_set2_1', 'df_24h_covid_set2_2', 'df_24h_covid_set2_3',
                      'df_24h_covid_set3_1', 'df_24h_covid_set2_2', 'df_24h_covid_set3_3',
                      'df_48h_covid_set1_1', 'df_48h_covid_set1_2', 'df_48h_covid_set1_3',
                      'df_48h_covid_set2_1', 'df_48h_covid_set2_2', 'df_48h_covid_set2_3',
                      'df_48h_covid_set3_1', 'df_48h_covid_set3_2', 'df_48h_covid_set3_3',
                      'df_72h_covid_set1_1', 'df_72h_covid_set1_2', 'df_72h_covid_set1_3',
                      'df_72h_covid_set2_1', 'df_48h_covid_set2_2', 'df_72h_covid_set2_3',
                      'df_72h_covid_set3_1', 'df_72h_covid_set3_2', 'df_72h_covid_set3_3']
  # 
  list_24h_exp = [df_24h_control_set1_1, df_24h_control_set1_2, df_24h_control_set1_3,
                  df_24h_control_set2_1, df_24h_control_set2_2, df_24h_control_set2_3,
                  df_24h_control_set3_1, df_24h_control_set2_2, df_24h_control_set3_3,
                  df_24h_covid_set1_1, df_24h_covid_set1_2, df_24h_covid_set1_3,
                  df_24h_covid_set2_1, df_24h_covid_set2_2, df_24h_covid_set2_3,
                  df_24h_covid_set3_1, df_24h_covid_set2_2, df_24h_covid_set3_3]
  # 
  list_24h_exp_names = ['df_24h_control_set1_1', 'df_24h_control_set1_2', 'df_24h_control_set1_3',
                  'df_24h_control_set2_1', 'df_24h_control_set2_2', 'df_24h_control_set2_3',
                  'df_24h_control_set3_1', 'df_24h_control_set2_2', 'df_24h_control_set3_3',
                  'df_24h_covid_set1_1', 'df_24h_covid_set1_2', 'df_24h_covid_set1_3',
                  'df_24h_covid_set2_1', 'df_24h_covid_set2_2', 'df_24h_covid_set2_3',
                  'df_24h_covid_set3_1', 'df_24h_covid_set2_2', 'df_24h_covid_set3_3']
  # 
  list_48h_exp = [df_48h_control_set1_1, df_48h_control_set1_2, df_48h_control_set1_3,
                  df_48h_control_set2_1, df_48h_control_set2_2, df_48h_control_set2_3,
                  df_48h_control_set3_1, df_48h_control_set3_2, df_48h_control_set3_3,
                  df_48h_covid_set1_1, df_48h_covid_set1_2, df_48h_covid_set1_3,
                  df_48h_covid_set2_1, df_48h_covid_set2_2, df_48h_covid_set2_3,
                  df_48h_covid_set3_1, df_48h_covid_set3_2, df_48h_covid_set3_3]
  # 
  list_48h_exp_names = ['df_48h_control_set1_1', 'df_48h_control_set1_2', 'df_48h_control_set1_3',
                  'df_48h_control_set2_1', 'df_48h_control_set2_2', 'df_48h_control_set2_3',
                  'df_48h_control_set3_1', 'df_48h_control_set3_2', 'df_48h_control_set3_3',
                  'df_48h_covid_set1_1', 'df_48h_covid_set1_2', 'df_48h_covid_set1_3',
                  'df_48h_covid_set2_1', 'df_48h_covid_set2_2', 'df_48h_covid_set2_3',
                  'df_48h_covid_set3_1', 'df_48h_covid_set3_2', 'df_48h_covid_set3_3']
  # 
  list_72h_exp = [df_72h_control_set1_1, df_72h_control_set1_2, df_72h_control_set1_3,
                  df_72h_control_set2_1, df_48h_control_set2_2, df_72h_control_set2_3,
                  df_72h_control_set3_1, df_72h_control_set3_2, df_72h_control_set3_3,
                  df_72h_covid_set1_1, df_72h_covid_set1_2, df_72h_covid_set1_3,
                  df_72h_covid_set2_1, df_48h_covid_set2_2, df_72h_covid_set2_3,
                  df_72h_covid_set3_1, df_72h_covid_set3_2, df_72h_covid_set3_3]
  # 
  list_72h_exp_names = ['df_72h_control_set1_1', 'df_72h_control_set1_2', 'df_72h_control_set1_3',
                  'df_72h_control_set2_1', 'df_48h_control_set2_2', 'df_72h_control_set2_3',
                  'df_72h_control_set3_1', 'df_72h_control_set3_2', 'df_72h_control_set3_3',
                  'df_72h_covid_set1_1', 'df_72h_covid_set1_2', 'df_72h_covid_set1_3',
                  'df_72h_covid_set2_1', 'df_48h_covid_set2_2', 'df_72h_covid_set2_3',
                  'df_72h_covid_set3_1', 'df_72h_covid_set3_2', 'df_72h_covid_set3_3']
  # 
  # 
  return list_all_exp, list_24h_exp, list_48h_exp, list_72h_exp, list_all_exp_names, list_24h_exp_names, list_48h_exp_names, list_72h_exp_names


def create_target_validated_data(exp,exp_name):
  for i in range(len(exp)):
    name_str = exp_name[i]
    if 'covid' in name_str:
      exp[i]['Target'] = 1
    else:
      exp[i]['Target'] = 0
  return exp

  



