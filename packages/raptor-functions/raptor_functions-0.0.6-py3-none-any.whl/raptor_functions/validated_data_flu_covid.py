import pandas as pd

def read_validated_data_flu_covid(path_to_validated_data):
  # 
  # 12 hours, 24 hours and 48 hours
  # # -------------------------------------------
  # Read data
  # 12 hours
  # 
  # SET 1
  # COVID:
  # 12 hours COVID Control experiments
  df_12h_covid_control_set1_1 = pd.read_csv(path_to_validated_data + 'Flu and COVID RAW Data 03122021/CoV Control 1 12H_13_40_33.47.txt',sep='\t',skiprows=(0,1,2),header=(34))
  df_12h_covid_control_set1_2 = pd.read_csv(path_to_validated_data + 'Flu and COVID RAW Data 03122021/CoV Control 1 12H_13_41_18.47.txt',sep='\t',skiprows=(0,1,2),header=(34))
  df_12h_covid_control_set1_3 = pd.read_csv(path_to_validated_data + 'Flu and COVID RAW Data 03122021/CoV Control 1 12H_13_42_05.47.txt',sep='\t',skiprows=(0,1,2),header=(34))
  df_12h_covid_control_set1_4 = pd.read_csv(path_to_validated_data + 'Flu and COVID RAW Data 03122021/CoV Control 1 12H_13_42_50.47.txt',sep='\t',skiprows=(0,1,2),header=(34))
  # 12 hours COVID experiments
  df_12h_covid_set1_1 = pd.read_csv(path_to_validated_data + 'Flu and COVID RAW Data 03122021/CoV 1 12H_15_16_05.47.txt',sep='\t',skiprows=(0,1,2),header=(34))
  df_12h_covid_set1_2 = pd.read_csv(path_to_validated_data + 'Flu and COVID RAW Data 03122021/CoV 1 12H_15_16_52.47.txt',sep='\t',skiprows=(0,1,2),header=(34))
  df_12h_covid_set1_3 = pd.read_csv(path_to_validated_data + 'Flu and COVID RAW Data 03122021/CoV 1 12H_15_17_39.47.txt',sep='\t',skiprows=(0,1,2),header=(34))
  df_12h_covid_set1_4 = pd.read_csv(path_to_validated_data + 'Flu and COVID RAW Data 03122021/CoV 1 12H_15_18_26.47.txt',sep='\t',skiprows=(0,1,2),header=(34))
  #
  # FLU:
  # 12 hours FLU Control experiments
  df_12h_flu_control_set1_1 = pd.read_csv(path_to_validated_data + 'Flu and COVID RAW Data 03122021/Flu Control 1 12H_14_21_38.47.txt',sep='\t',skiprows=(0,1,2),header=(34))
  df_12h_flu_control_set1_2 = pd.read_csv(path_to_validated_data + 'Flu and COVID RAW Data 03122021/Flu Control 1 12H_14_22_25.47.txt',sep='\t',skiprows=(0,1,2),header=(34))
  # 12 hours FLU experiments
  df_12h_flu_set1_1 = pd.read_csv(path_to_validated_data + 'Flu and COVID RAW Data 03122021/Flu 1 12H_14_43_31.47.txt',sep='\t',skiprows=(0,1,2),header=(34))
  df_12h_flu_set1_2 = pd.read_csv(path_to_validated_data + 'Flu and COVID RAW Data 03122021/Flu 1 12H_14_44_20.47.txt',sep='\t',skiprows=(0,1,2),header=(34))
  df_12h_flu_set1_3 = pd.read_csv(path_to_validated_data + 'Flu and COVID RAW Data 03122021/Flu 1 12H_14_45_07.47.txt',sep='\t',skiprows=(0,1,2),header=(34))
  df_12h_flu_set1_4 = pd.read_csv(path_to_validated_data + 'Flu and COVID RAW Data 03122021/Flu 1 12H_14_45_54.47.txt',sep='\t',skiprows=(0,1,2),header=(34))
  #
  # SET 2
  # COVID:
  # 12 hours COVID Control experiments
  df_12h_covid_control_set2_1 = pd.read_csv(path_to_validated_data + 'Flu and COVID RAW Data 03122021/CoV Control 2 12H_13_44_29.47.txt',sep='\t',skiprows=(0,1,2),header=(34))
  df_12h_covid_control_set2_2 = pd.read_csv(path_to_validated_data + 'Flu and COVID RAW Data 03122021/CoV Control 2 12H_13_45_16.47.txt',sep='\t',skiprows=(0,1,2),header=(34))
  df_12h_covid_control_set2_3 = pd.read_csv(path_to_validated_data + 'Flu and COVID RAW Data 03122021/CoV Control 2 12H_13_46_03.47.txt',sep='\t',skiprows=(0,1,2),header=(34))
  df_12h_covid_control_set2_4 = pd.read_csv(path_to_validated_data + 'Flu and COVID RAW Data 03122021/CoV Control 2 12H_13_46_50.47.txt',sep='\t',skiprows=(0,1,2),header=(34))
  # 12 hours COVID experiments
  df_12h_covid_set2_1 = pd.read_csv(path_to_validated_data + 'Flu and COVID RAW Data 03122021/CoV 2 24H_15_21_02.47.txt',sep='\t',skiprows=(0,1,2),header=(34))
  df_12h_covid_set2_2 = pd.read_csv(path_to_validated_data + 'Flu and COVID RAW Data 03122021/CoV 2 24H_15_21_49.47.txt',sep='\t',skiprows=(0,1,2),header=(34))
  df_12h_covid_set2_3 = pd.read_csv(path_to_validated_data + 'Flu and COVID RAW Data 03122021/CoV 2 24H_15_22_36.47.txt',sep='\t',skiprows=(0,1,2),header=(34))
  #
  # FLU:
  # 12 hours FLU Control experiments
  # [no data] 
  # 12 hours FLU experiments
  df_12h_flu_set2_1 = pd.read_csv(path_to_validated_data + 'Flu and COVID RAW Data 03122021/Flu 2 12H_14_47_37.47.txt',sep='\t',skiprows=(0,1,2),header=(34))
  df_12h_flu_set2_2 = pd.read_csv(path_to_validated_data + 'Flu and COVID RAW Data 03122021/Flu 2 12H_14_48_24.47.txt',sep='\t',skiprows=(0,1,2),header=(34))
  df_12h_flu_set2_3 = pd.read_csv(path_to_validated_data + 'Flu and COVID RAW Data 03122021/Flu 2 12H_14_49_12.47.txt',sep='\t',skiprows=(0,1,2),header=(34))
  #
  # -------------------------------------------
  # Read data
  # 24 hours
  #
  # SET 1
  # COVID:
  # 24 hours COVID Control experiments
  df_24h_covid_control_set1_1 = pd.read_csv(path_to_validated_data + 'Flu and COVID RAW Data 03122021/CoV Control 1 24H_13_48_45.47.txt',sep='\t',skiprows=(0,1,2),header=(34))
  df_24h_covid_control_set1_2 = pd.read_csv(path_to_validated_data + 'Flu and COVID RAW Data 03122021/CoV Control 1 24H_13_50_19.47.txt',sep='\t',skiprows=(0,1,2),header=(34))
  df_24h_covid_control_set1_3 = pd.read_csv(path_to_validated_data + 'Flu and COVID RAW Data 03122021/CoV Control 1 24H_13_51_06.47.txt',sep='\t',skiprows=(0,1,2),header=(34))
  # 24 hours COVID experiments
  df_24h_covid_set1_1 = pd.read_csv(path_to_validated_data + 'Flu and COVID RAW Data 03122021/CoV 1 24H_15_25_04.47.txt',sep='\t',skiprows=(0,1,2),header=(34))
  df_24h_covid_set1_2 = pd.read_csv(path_to_validated_data + 'Flu and COVID RAW Data 03122021/CoV 1 24H_15_25_51.47.txt',sep='\t',skiprows=(0,1,2),header=(34))
  df_24h_covid_set1_3 = pd.read_csv(path_to_validated_data + 'Flu and COVID RAW Data 03122021/CoV 1 24H_15_26_38.47.txt',sep='\t',skiprows=(0,1,2),header=(34))
  #
  # FLU:
  # 24 hours FLU Control experiments
  df_24h_flu_control_set1_1 = pd.read_csv(path_to_validated_data + 'Flu and COVID RAW Data 03122021/Flu Control 1 24H_14_32_09.47.txt',sep='\t',skiprows=(0,1,2),header=(34))
  df_24h_flu_control_set1_2 = pd.read_csv(path_to_validated_data + 'Flu and COVID RAW Data 03122021/Flu Control 1 24H_14_32_56.47.txt',sep='\t',skiprows=(0,1,2),header=(34))
  df_24h_flu_control_set1_3 = pd.read_csv(path_to_validated_data + 'Flu and COVID RAW Data 03122021/Flu Control 1 24H_14_33_43.47.txt',sep='\t',skiprows=(0,1,2),header=(34))
  # 24 hours FLU experiments
  df_24h_flu_set1_1 = pd.read_csv(path_to_validated_data + 'Flu and COVID RAW Data 03122021/Flu 1 24H_14_52_46.47.txt',sep='\t',skiprows=(0,1,2),header=(34))
  df_24h_flu_set1_2 = pd.read_csv(path_to_validated_data + 'Flu and COVID RAW Data 03122021/Flu 1 24H_14_53_33.47.txt',sep='\t',skiprows=(0,1,2),header=(34))
  df_24h_flu_set1_3 = pd.read_csv(path_to_validated_data + 'Flu and COVID RAW Data 03122021/Flu 1 24H_14_54_20.47.txt',sep='\t',skiprows=(0,1,2),header=(34))
  df_24h_flu_set1_4 = pd.read_csv(path_to_validated_data + 'Flu and COVID RAW Data 03122021/Flu 1 24H_14_55_07.47.txt',sep='\t',skiprows=(0,1,2),header=(34))
  #
  # SET 2
  # COVID:
  # 24 hours COVID Control experiments
  df_24h_covid_control_set2_1 = pd.read_csv(path_to_validated_data + 'Flu and COVID RAW Data 03122021/CoV Control 2 24H_13_52_50.47.txt',sep='\t',skiprows=(0,1,2),header=(34))
  df_24h_covid_control_set2_2 = pd.read_csv(path_to_validated_data + 'Flu and COVID RAW Data 03122021/CoV Control 2 24H_13_53_37.47.txt',sep='\t',skiprows=(0,1,2),header=(34))
  df_24h_covid_control_set2_3 = pd.read_csv(path_to_validated_data + 'Flu and COVID RAW Data 03122021/CoV Control 2 24H_13_54_24.47.txt',sep='\t',skiprows=(0,1,2),header=(34))
  df_24h_covid_control_set2_4 = pd.read_csv(path_to_validated_data + 'Flu and COVID RAW Data 03122021/CoV Control 2 24H_13_55_11.47.txt',sep='\t',skiprows=(0,1,2),header=(34))
  # 24 hours COVID experiments
  df_24h_covid_set2_1 = pd.read_csv(path_to_validated_data + 'Flu and COVID RAW Data 03122021/CoV 2 24H_15_21_02.47.txt',sep='\t',skiprows=(0,1,2),header=(34))
  df_24h_covid_set2_2 = pd.read_csv(path_to_validated_data + 'Flu and COVID RAW Data 03122021/CoV 2 24H_15_21_49.47.txt',sep='\t',skiprows=(0,1,2),header=(34))
  df_24h_covid_set2_3 = pd.read_csv(path_to_validated_data + 'Flu and COVID RAW Data 03122021/CoV 2 24H_15_22_36.47.txt',sep='\t',skiprows=(0,1,2),header=(34))
  #
  # FLU:
  # 24 hours FLU Control experiments
  df_24h_flu_control_set2_1 = pd.read_csv(path_to_validated_data + 'Flu and COVID RAW Data 03122021/Flu Control 2 24H_14_28_08.47.txt',sep='\t',skiprows=(0,1,2),header=(34))
  df_24h_flu_control_set2_2 = pd.read_csv(path_to_validated_data + 'Flu and COVID RAW Data 03122021/Flu Control 2 24H_14_28_55.47.txt',sep='\t',skiprows=(0,1,2),header=(34))
  df_24h_flu_control_set2_3 = pd.read_csv(path_to_validated_data + 'Flu and COVID RAW Data 03122021/Flu Control 2 24H_14_29_42.47.txt',sep='\t',skiprows=(0,1,2),header=(34))
  df_24h_flu_control_set2_4 = pd.read_csv(path_to_validated_data + 'Flu and COVID RAW Data 03122021/Flu Control 2 24H_14_30_29.47.txt',sep='\t',skiprows=(0,1,2),header=(34))
  # 24 hours FLU experiments
  df_24h_flu_set2_1 = pd.read_csv(path_to_validated_data + 'Flu and COVID RAW Data 03122021/Flu 2 24H_14_56_50.47.txt',sep='\t',skiprows=(0,1,2),header=(34))
  df_24h_flu_set2_2 = pd.read_csv(path_to_validated_data + 'Flu and COVID RAW Data 03122021/Flu 2 24H_14_57_37.47.txt',sep='\t',skiprows=(0,1,2),header=(34))
  df_24h_flu_set2_3 = pd.read_csv(path_to_validated_data + 'Flu and COVID RAW Data 03122021/Flu 2 24H_14_58_24.47.txt',sep='\t',skiprows=(0,1,2),header=(34))
  df_24h_flu_set2_4 = pd.read_csv(path_to_validated_data + 'Flu and COVID RAW Data 03122021/Flu 2 24H_14_59_12.47.txt',sep='\t',skiprows=(0,1,2),header=(34))

  #
  # -------------------------------------------
  # Read data
  # 48 hours
  #
  # SET 1
  # COVID:
  # 48 hours COVID Control experiments
  df_48h_covid_control_set1_1 = pd.read_csv(path_to_validated_data + 'Flu and COVID RAW Data 03122021/CoV Control 1 48H_13_56_56.47.txt',sep='\t',skiprows=(0,1,2),header=(34))
  df_48h_covid_control_set1_2 = pd.read_csv(path_to_validated_data + 'Flu and COVID RAW Data 03122021/CoV Control 1 48H_13_59_50.47.txt',sep='\t',skiprows=(0,1,2),header=(34))
  df_48h_covid_control_set1_3 = pd.read_csv(path_to_validated_data + 'Flu and COVID RAW Data 03122021/CoV Control 1 48H_14_00_38.47.txt',sep='\t',skiprows=(0,1,2),header=(34))
  df_48h_covid_control_set1_4 = pd.read_csv(path_to_validated_data + 'Flu and COVID RAW Data 03122021/CoV Control 1 48H_14_01_27.47.txt',sep='\t',skiprows=(0,1,2),header=(34))
  # 48 hours COVID experiments
  df_48h_covid_set1_1 = pd.read_csv(path_to_validated_data + 'Flu and COVID RAW Data 03122021/CoV 1 48H_15_27_36.47.txt',sep='\t',skiprows=(0,1,2),header=(34))
  df_48h_covid_set1_2 = pd.read_csv(path_to_validated_data + 'Flu and COVID RAW Data 03122021/CoV 1 48H_15_28_21.47.txt',sep='\t',skiprows=(0,1,2),header=(34))
  df_48h_covid_set1_3 = pd.read_csv(path_to_validated_data + 'Flu and COVID RAW Data 03122021/CoV 1 48H_15_29_08.47.txt',sep='\t',skiprows=(0,1,2),header=(34))
  df_48h_covid_set1_4 = pd.read_csv(path_to_validated_data + 'Flu and COVID RAW Data 03122021/CoV 1 48H_15_29_55.47.txt',sep='\t',skiprows=(0,1,2),header=(34))
  #
  # FLU:
  # 48 hours FLU Control experiments
  df_48h_flu_control_set1_1 = pd.read_csv(path_to_validated_data + 'Flu and COVID RAW Data 03122021/Flu Control 1 48H_14_36_23.47.txt',sep='\t',skiprows=(0,1,2),header=(34))
  df_48h_flu_control_set1_2 = pd.read_csv(path_to_validated_data + 'Flu and COVID RAW Data 03122021/Flu Control 1 48H_14_37_10.47.txt',sep='\t',skiprows=(0,1,2),header=(34))
  df_48h_flu_control_set1_3 = pd.read_csv(path_to_validated_data + 'Flu and COVID RAW Data 03122021/Flu Control 1 48H_14_37_57.47.txt',sep='\t',skiprows=(0,1,2),header=(34))
  # 48 hours FLU experiments
  df_48h_flu_set1_1 = pd.read_csv(path_to_validated_data + 'Flu and COVID RAW Data 03122021/Flu 1 48H_15_00_59.47.txt',sep='\t',skiprows=(0,1,2),header=(34))
  df_48h_flu_set1_2 = pd.read_csv(path_to_validated_data + 'Flu and COVID RAW Data 03122021/Flu 1 48H_15_01_46.47.txt',sep='\t',skiprows=(0,1,2),header=(34))
  #
  # SET 2
  # COVID:
  # 48 hours COVID Control experiments
  df_48h_covid_control_set2_1 = pd.read_csv(path_to_validated_data + 'Flu and COVID RAW Data 03122021/CoV Control 2 48H_14_07_34.47.txt',sep='\t',skiprows=(0,1,2),header=(34))
  df_48h_covid_control_set2_2 = pd.read_csv(path_to_validated_data + 'Flu and COVID RAW Data 03122021/CoV Control 2 48H_14_08_19.47.txt',sep='\t',skiprows=(0,1,2),header=(34))
  # 48 hours COVID experiments
  df_48h_covid_set2_1 = pd.read_csv(path_to_validated_data + 'Flu and COVID RAW Data 03122021/CoV 2 48H_15_35_10.47.txt',sep='\t',skiprows=(0,1,2),header=(34))
  df_48h_covid_set2_2 = pd.read_csv(path_to_validated_data + 'Flu and COVID RAW Data 03122021/CoV 2 48H_15_35_57.47.txt',sep='\t',skiprows=(0,1,2),header=(34))
  df_48h_covid_set2_3 = pd.read_csv(path_to_validated_data + 'Flu and COVID RAW Data 03122021/CoV 2 48H_15_36_46.47.txt',sep='\t',skiprows=(0,1,2),header=(34))
  df_48h_covid_set2_4 = pd.read_csv(path_to_validated_data + 'Flu and COVID RAW Data 03122021/CoV 2 48H_15_37_33.47.txt',sep='\t',skiprows=(0,1,2),header=(34))
  #
  # FLU:
  # 48 hours FLU Control experiments
  df_48h_flu_control_set2_1 = pd.read_csv(path_to_validated_data + 'Flu and COVID RAW Data 03122021/Flu Control 2 48H_14_39_43.47.txt',sep='\t',skiprows=(0,1,2),header=(34))
  df_48h_flu_control_set2_2 = pd.read_csv(path_to_validated_data + 'Flu and COVID RAW Data 03122021/Flu Control 2 48H_14_40_31.47.txt',sep='\t',skiprows=(0,1,2),header=(34))
  df_48h_flu_control_set2_3 = pd.read_csv(path_to_validated_data + 'Flu and COVID RAW Data 03122021/Flu Control 2 48H_14_41_18.47.txt',sep='\t',skiprows=(0,1,2),header=(34))
  # 48 hours FLU experiments
  df_48h_flu_set2_1 = pd.read_csv(path_to_validated_data + 'Flu and COVID RAW Data 03122021/Flu 2 48H_15_07_30.47.txt',sep='\t',skiprows=(0,1,2),header=(34))
  df_48h_flu_set2_2 = pd.read_csv(path_to_validated_data + 'Flu and COVID RAW Data 03122021/Flu 2 48H_15_08_19.47.txt',sep='\t',skiprows=(0,1,2),header=(34))
  df_48h_flu_set2_3 = pd.read_csv(path_to_validated_data + 'Flu and COVID RAW Data 03122021/Flu 2 48H_15_09_06.47.txt',sep='\t',skiprows=(0,1,2),header=(34))
  df_48h_flu_set2_4 = pd.read_csv(path_to_validated_data + 'Flu and COVID RAW Data 03122021/Flu 2 48H_15_09_53.47.txt',sep='\t',skiprows=(0,1,2),header=(34))
  # -------------------------------------------
  # -------------------------------------------  
  # 
  # LISTS
  # Get all the experiments dataframes in a list
  list_all_exp = [
                  df_12h_covid_control_set1_1, df_12h_covid_control_set1_2, df_12h_covid_control_set1_3, df_12h_covid_control_set1_4,
                  df_12h_covid_set1_1, df_12h_covid_set1_2, df_12h_covid_set1_3,
                  df_12h_flu_control_set1_1, df_12h_flu_control_set1_2,
                  df_12h_flu_set1_1, df_12h_flu_set1_2, df_12h_flu_set1_3, df_12h_flu_set1_4,
                  #
                  df_12h_covid_control_set2_1, df_12h_covid_control_set2_2, df_12h_covid_control_set2_3, df_12h_covid_control_set2_4,
                  df_12h_covid_set2_1, df_12h_covid_set2_2, df_12h_covid_set2_3,
                  df_12h_flu_set2_1, df_12h_flu_set2_2, df_12h_flu_set2_3,
                  ##
                  df_24h_covid_control_set1_1, df_24h_covid_control_set1_2, df_24h_covid_control_set1_3,
                  df_24h_covid_set1_1, df_24h_covid_set1_2, df_24h_covid_set1_3,
                  df_24h_flu_control_set1_1, df_24h_flu_control_set1_2, df_24h_flu_control_set1_3,
                  df_24h_flu_set1_1, df_24h_flu_set1_2, df_24h_flu_set1_3, df_24h_flu_set1_4,
                  #
                  df_24h_covid_control_set2_1, df_24h_covid_control_set2_2, df_24h_covid_control_set2_3, df_24h_covid_control_set2_4,
                  df_24h_covid_set2_1, df_24h_covid_set2_2, df_24h_covid_set2_3,
                  df_24h_flu_control_set2_1, df_24h_flu_control_set2_2, df_24h_flu_control_set2_3, df_24h_flu_control_set2_4,
                  df_24h_flu_set2_1, df_24h_flu_set2_2, df_24h_flu_set2_3, df_24h_flu_set2_4,
                  ##
                  df_48h_covid_control_set1_1, df_48h_covid_control_set1_2, df_48h_covid_control_set1_3, df_48h_covid_control_set1_4,
                  df_48h_covid_set1_1, df_48h_covid_set1_2, df_48h_covid_set1_3, df_48h_covid_set1_4,
                  df_48h_flu_control_set1_1, df_48h_flu_control_set1_2, df_48h_flu_control_set1_3,
                  df_48h_flu_set1_1, df_48h_flu_set1_2,
                  #
                  df_48h_covid_control_set2_1, df_48h_covid_control_set2_2, 
                  df_48h_covid_set2_1, df_48h_covid_set2_2, df_48h_covid_set2_3, df_48h_covid_set2_4,
                  df_48h_flu_control_set2_1, df_48h_flu_control_set2_2, df_48h_flu_control_set2_3,
                  df_48h_flu_set2_1, df_48h_flu_set2_2, df_48h_flu_set2_3, df_48h_flu_set2_4
                  ]
  
  # 
  list_all_exp_names = [
                  'df_12h_covid_control_set1_1', 'df_12h_covid_control_set1_2', 'df_12h_covid_control_set1_3', 'df_12h_covid_control_set1_4',
                  'df_12h_covid_set1_1', 'df_12h_covid_set1_2', 'df_12h_covid_set1_3',
                  'df_12h_flu_control_set1_1', 'df_12h_flu_control_set1_2',
                  'df_12h_flu_set1_1', 'df_12h_flu_set1_2', 'df_12h_flu_set1_3', 'df_12h_flu_set1_4',
                  #
                  'df_12h_covid_control_set2_1', 'df_12h_covid_control_set2_2', 'df_12h_covid_control_set2_3', 'df_12h_covid_control_set2_4',
                  'df_12h_covid_set2_1', 'df_12h_covid_set2_2', 'df_12h_covid_set2_3',
                  'df_12h_flu_set2_1', 'df_12h_flu_set2_2', 'df_12h_flu_set2_3',
                  ##
                  'df_24h_covid_control_set1_1', 'df_24h_covid_control_set1_2', 'df_24h_covid_control_set1_3',
                  'df_24h_covid_set1_1', 'df_24h_covid_set1_2', 'df_24h_covid_set1_3',
                  'df_24h_flu_control_set1_1', 'df_24h_flu_control_set1_2', 'df_24h_flu_control_set1_3',
                  'df_24h_flu_set1_1', 'df_24h_flu_set1_2', 'df_24h_flu_set1_3', 'df_24h_flu_set1_4',
                  #
                  'df_24h_covid_control_set2_1', 'df_24h_covid_control_set2_2', 'df_24h_covid_control_set2_3', 'df_24h_covid_control_set2_4',
                  'df_24h_covid_set2_1', 'df_24h_covid_set2_2', 'df_24h_covid_set2_3',
                  'df_24h_flu_control_set2_1', 'df_24h_flu_control_set2_2', 'df_24h_flu_control_set2_3', 'df_24h_flu_control_set2_4',
                  'df_24h_flu_set2_1', 'df_24h_flu_set2_2', 'df_24h_flu_set2_3', 'df_24h_flu_set2_4',
                  ##
                  'df_48h_covid_control_set1_1', 'df_48h_covid_control_set1_2', 'df_48h_covid_control_set1_3', 'df_48h_covid_control_set1_4',
                  'df_48h_covid_set1_1', 'df_48h_covid_set1_2', 'df_48h_covid_set1_3', 'df_48h_covid_set1_4',
                  'df_48h_flu_control_set1_1', 'df_48h_flu_control_set1_2', 'df_48h_flu_control_set1_3',
                  'df_48h_flu_set1_1', 'df_48h_flu_set1_2',
                  #
                  'df_48h_covid_control_set2_1', 'df_48h_covid_control_set2_2', 
                  'df_48h_covid_set2_1', 'df_48h_covid_set2_2', 'df_48h_covid_set2_3', 'df_48h_covid_set2_4',
                  'df_48h_flu_control_set2_1', 'df_48h_flu_control_set2_2', 'df_48h_flu_control_set2_3',
                  'df_48h_flu_set2_1', 'df_48h_flu_set2_2', 'df_48h_flu_set2_3', 'df_48h_flu_set2_4'
                  ]
  # 
  list_12h_exp = [df_12h_covid_control_set1_1, df_12h_covid_control_set1_2, df_12h_covid_control_set1_3, df_12h_covid_control_set1_4,
                  df_12h_covid_set1_1, df_12h_covid_set1_2, df_12h_covid_set1_3,
                  df_12h_flu_control_set1_1, df_12h_flu_control_set1_2,
                  df_12h_flu_set1_1, df_12h_flu_set1_2, df_12h_flu_set1_3, df_12h_flu_set1_4,
                  #
                  df_12h_covid_control_set2_1, df_12h_covid_control_set2_2, df_12h_covid_control_set2_3, df_12h_covid_control_set2_4,
                  df_12h_covid_set2_1, df_12h_covid_set2_2, df_12h_covid_set2_3,
                  df_12h_flu_set2_1, df_12h_flu_set2_2, df_12h_flu_set2_3]
  # 
  list_12h_exp_names = ['df_12h_covid_control_set1_1', 'df_12h_covid_control_set1_2', 'df_12h_covid_control_set1_3', 'df_12h_covid_control_set1_4',
                  'df_12h_covid_set1_1', 'df_12h_covid_set1_2', 'df_12h_covid_set1_3',
                  'df_12h_flu_control_set1_1', 'df_12h_flu_control_set1_2',
                  'df_12h_flu_set1_1', 'df_12h_flu_set1_2', 'df_12h_flu_set1_3', 'df_12h_flu_set1_4',
                  #
                  'df_12h_covid_control_set2_1', 'df_12h_covid_control_set2_2', 'df_12h_covid_control_set2_3', 'df_12h_covid_control_set2_4',
                  'df_12h_covid_set2_1', 'df_12h_covid_set2_2', 'df_12h_covid_set2_3',
                  'df_12h_flu_set2_1', 'df_12h_flu_set2_2', 'df_12h_flu_set2_3']
  # 
  list_24h_exp = [df_24h_covid_control_set1_1, df_24h_covid_control_set1_2, df_24h_covid_control_set1_3,
                  df_24h_covid_set1_1, df_24h_covid_set1_2, df_24h_covid_set1_3,
                  df_24h_flu_control_set1_1, df_24h_flu_control_set1_2, df_24h_flu_control_set1_3,
                  df_24h_flu_set1_1, df_24h_flu_set1_2, df_24h_flu_set1_3, df_24h_flu_set1_4,
                  #
                  df_24h_covid_control_set2_1, df_24h_covid_control_set2_2, df_24h_covid_control_set2_3, df_24h_covid_control_set2_4,
                  df_24h_covid_set2_1, df_24h_covid_set2_2, df_24h_covid_set2_3,
                  df_24h_flu_control_set2_1, df_24h_flu_control_set2_2, df_24h_flu_control_set2_3, df_24h_flu_control_set2_4,
                  df_24h_flu_set2_1, df_24h_flu_set2_2, df_24h_flu_set2_3, df_24h_flu_set2_4]
  # 
  list_24h_exp_names = ['df_24h_covid_control_set1_1', 'df_24h_covid_control_set1_2', 'df_24h_covid_control_set1_3',
                  'df_24h_covid_set1_1', 'df_24h_covid_set1_2', 'df_24h_covid_set1_3',
                  'df_24h_flu_control_set1_1', 'df_24h_flu_control_set1_2', 'df_24h_flu_control_set1_3',
                  'df_24h_flu_set1_1', 'df_24h_flu_set1_2', 'df_24h_flu_set1_3', 'df_24h_flu_set1_4',
                  #
                  'df_24h_covid_control_set2_1', 'df_24h_covid_control_set2_2', 'df_24h_covid_control_set2_3', 'df_24h_covid_control_set2_4',
                  'df_24h_covid_set2_1', 'df_24h_covid_set2_2', 'df_24h_covid_set2_3',
                  'df_24h_flu_control_set2_1', 'df_24h_flu_control_set2_2', 'df_24h_flu_control_set2_3', 'df_24h_flu_control_set2_4',
                  'df_24h_flu_set2_1', 'df_24h_flu_set2_2', 'df_24h_flu_set2_3', 'df_24h_flu_set2_4']
  # 
  list_48h_exp = [ df_48h_covid_control_set1_1, df_48h_covid_control_set1_2, df_48h_covid_control_set1_3, df_48h_covid_control_set1_4,
                  df_48h_covid_set1_1, df_48h_covid_set1_2, df_48h_covid_set1_3, df_48h_covid_set1_4,
                  df_48h_flu_control_set1_1, df_48h_flu_control_set1_2, df_48h_flu_control_set1_3,
                  df_48h_flu_set1_1, df_48h_flu_set1_2,
                  #
                  df_48h_covid_control_set2_1, df_48h_covid_control_set2_2, 
                  df_48h_covid_set2_1, df_48h_covid_set2_2, df_48h_covid_set2_3, df_48h_covid_set2_4,
                  df_48h_flu_control_set2_1, df_48h_flu_control_set2_2, df_48h_flu_control_set2_3,
                  df_48h_flu_set2_1, df_48h_flu_set2_2, df_48h_flu_set2_3, df_48h_flu_set2_4]
  # 
  list_48h_exp_names = ['df_48h_covid_control_set1_1', 'df_48h_covid_control_set1_2', 'df_48h_covid_control_set1_3', 'df_48h_covid_control_set1_4',
                  'df_48h_covid_set1_1', 'df_48h_covid_set1_2', 'df_48h_covid_set1_3', 'df_48h_covid_set1_4',
                  'df_48h_flu_control_set1_1', 'df_48h_flu_control_set1_2', 'df_48h_flu_control_set1_3',
                  'df_48h_flu_set1_1', 'df_48h_flu_set1_2',
                  #
                  'df_48h_covid_control_set2_1', 'df_48h_covid_control_set2_2', 
                  'df_48h_covid_set2_1', 'df_48h_covid_set2_2', 'df_48h_covid_set2_3', 'df_48h_covid_set2_4',
                  'df_48h_flu_control_set2_1', 'df_48h_flu_control_set2_2', 'df_48h_flu_control_set2_3',
                  'df_48h_flu_set2_1', 'df_48h_flu_set2_2', 'df_48h_flu_set2_3', 'df_48h_flu_set2_4']
  # 
  # 
  return list_all_exp, list_12h_exp, list_24h_exp, list_48h_exp, list_all_exp_names, list_12h_exp_names, list_24h_exp_names, list_48h_exp_names


def create_target_validated_data_flu_covid(exp,exp_name):
  for i in range(len(exp)):
    name_str = exp_name[i]
    if ('covid' in name_str) and ('control' in name_str):
      exp[i]['Target'] = 'Control Covid'
    if ('flu' in name_str) and ('control' in name_str):
      exp[i]['Target'] = 'Control Flu'
    elif ('covid' in name_str):
      exp[i]['Target'] = 'Covid'
    elif ('flu' in name_str):
      exp[i]['Target'] = 'Flu'
    else:
      exp[i]['Target'] = 'Control'
  return exp

  



