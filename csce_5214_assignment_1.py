# ID: 11508393
# NAME: Ping-Chun Lee

import pandas as pd
import regex as re
import numpy as np
import matplotlib.pyplot as plt

def getData(filename):
  canData=[] #List to store teh can data
  f = open(filename)
  #read_file = reader(f)
  read_file =f.readlines()
  
  #file = list(read_file)
  speed_list = []
  rpm_list = []
  spd = 0
  rpm = 0
  i = 0
  for row in read_file:
    #Change the positions of the values if needed
    record = {'stamp':row[1:18], 'PID':row[25:28], 'const1':row[29:33], 
'change':row[33:41],'value':int(row[41:45], 16), 'value2':0 ,'attack':0}
    
    if record["PID"] == '254': #Processing of speed
      if record["value"] >= 4095:
        record["attack"] = 1
      record['value'] =  (record['value'] * 0.62137119) /100
      spd = record['value']
    speed_list.append(spd)
      #print("i == ",i, "speed= ", record['value'])
    
    if record["PID"] == '115': #Processing of RPM 
      if record["value"] >= 65535:
        record["attack"] = 1
      record['value'] =  (record['value'] * 2)
      rpm = record['value']
    rpm_list.append(rpm)
      #print("i == ",i, "RPM= ", record['value'])
    i = i+1   
    canData.append(record)
    record={}
    
  f.close()
  
  #Change the return value to speed or RPM if you want to return the other lists
  return speed_list, rpm_list, pd.DataFrame(data=canData)

# --- TASK 1 ---
speed_all_cases = []
rpm_all_cases = []
# get dataframe of injection of speed reading
s, r, df_inj_spd = getData("./CAN Bus log - injection of FFF as the speed reading.log")
speed_all_cases.append(s)
rpm_all_cases.append(r)

# get dataframe of injection of RPM
s, r, df_inj_rpm = getData("./CAN Bus log - injection of RPM readings.log")
speed_all_cases.append(s)
rpm_all_cases.append(r)

# get dataframe of pure dataset
s, r, df_inj_NA = getData("./CAN bus log - no injection of messages.log")
speed_all_cases.append(s)
rpm_all_cases.append(r)

# --- TASK 2 Step 1 ---
cases = [
    "speed injection: speed", 
    "speed injection: RPM", 
    "speed injection: speed vs RPM", 
    "RPM injection: speed", 
    "RPM injection: RPM", 
    "RPM injection: speed vs RPM", 
    "no injection: speed", 
    "no injection: RPM", 
    "no injection: speed vs RPM", 
]

inj_spd_x = np.arange(len(speed_all_cases[0]))
inj_rpm_x = np.arange(len(speed_all_cases[1]))
inj_NA_x  = np.arange(len(speed_all_cases[2]))

x_ary = [inj_spd_x, inj_spd_x, speed_all_cases[0],
         inj_rpm_x, inj_rpm_x, speed_all_cases[1],
         inj_NA_x,  inj_NA_x,  speed_all_cases[2]]
y_ary = [speed_all_cases[0], rpm_all_cases[0], rpm_all_cases[0],
         speed_all_cases[1], rpm_all_cases[1], rpm_all_cases[1],
         speed_all_cases[2], rpm_all_cases[2], rpm_all_cases[2]]

fig, axs = plt.subplots(3, 3, figsize=(10, 10), constrained_layout=True)
for ax, case, i in zip(axs.flat, cases, range(9)):
      #plt.subplot(3, 3, i+1)
      ax.scatter(x_ary[i], y_ary[i])
      ax.set_title(cases[i])

plt.show()

# --- TASK 2 Step 2 ---