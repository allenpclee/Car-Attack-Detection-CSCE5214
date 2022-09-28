import pandas as pd
import regex as re
import numpy as np

def extract_info(df):

  #function to strip PID and its message
  def pid_split(pid_str):
    pid_keywords = '[^#]+'
    try:
        splitted_str = re.findall(pid_keywords, pid_str)
    except KeyError:
        splitted_str = pid_str
    return splitted_str

  #split PID message into PID and message
  for index, row in df.iterrows():
    df.loc[df.index[index], 'PID'] = pid_split(df.loc[df.index[index], 'PID_info'])[0]
    df.loc[df.index[index], 'message'] = pid_split(df.loc[df.index[index], 'PID_info'])[1]

  #drop irrelevant information
  #select only data points with PID = 254 (Speed) and PID = 115 (RPM)
  #select only last four characters of the message
  df = df.drop(['Bus_id','PID_info','Time_Stamp'],axis=1)
  df = df.loc[(df['PID'] == '254') | (df['PID'] == '115')]
  df['message'] = df['message'].str[-4:]
  df = df.reset_index(drop=True)

  #create label based on RPM and SPEED values
  for index, row in df.iterrows():
    if df.loc[df.index[index], 'PID'] == '254':
      if int((df.loc[df.index[index], 'message']),16) >= 4095:
        df.loc[df.index[index], 'Attack'] = 1
      else:
        df.loc[df.index[index], 'Attack'] = 0
      df.loc[df.index[index], 'message'] = (int((df.loc[df.index[index], 'message']),16) * 0.62137119) /100
    else:
      if int((df.loc[df.index[index], 'message']),16) >= 65535:
        df.loc[df.index[index], 'Attack'] = 1
      else:
        df.loc[df.index[index], 'Attack'] = 0
      df.loc[df.index[index], 'message'] = (int((df.loc[df.index[index], 'message']),16)* 2)

  # Get one hot encoding of columns PID
  one_hot = pd.get_dummies(df['PID'])
  # Drop column B as it is now encoded
  df = df.drop('PID',axis = 1)
  # Join the encoded df
  df = df.join(one_hot)
  df = df[['115', '254', 'message', 'Attack']]
  df.rename(columns = {'115':'RPM', '254':'Speed'}, inplace = True)

  return df

#example on loading text file (You are given 3 differrent text file, You need to load those file separately and pass them through extract_df function to get 3 separate dataframe)
df = pd.read_csv("/content/CAN Bus log - injection of FFF as the speed reading.log", sep=" ", 
                 header=None, names=["Time_Stamp", "Bus_id","PID_info"])

#call function to create dataframe using relevant information from the text file
df = extract_info(df)

