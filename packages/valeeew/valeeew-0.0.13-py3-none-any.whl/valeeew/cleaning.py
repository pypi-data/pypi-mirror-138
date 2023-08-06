#function return the variable name 
def var_name(var, dir=locals()):
    for key, val in dir.items():
        if id(val) == id(var):
            return key


#function to make a quick overview of your DATAframe
def watch(data):
  import matplotlib.pyplot as plt
  import seaborn as sns


  s = "\n"

  lin, col = data.shape
  total_cell = lin*col 
  total_null=data.isnull().sum().sum()
  prct=total_null *100/total_cell 

  dupli = data.duplicated().sum()
  nul = (data.isna().mean()).sum()
  reslt_dupli = "No duplicate value"
  if dupli + nul == 0:
    a = "No duplicate and no null DATA"
  elif dupli == 0 and nul != 0:
    a = "Null DATA and nothing duplicate"
  elif dupli != 0 and nul == 0:
    a = "Duplicate DATA and nothing null"
  else:
    a = "Duplicate and null DATA"
  
  if a == "Duplicate DATA and nothing null" or "Duplicate and null DATA":
    reslt_dupli = data[(data.duplicated())== True]
  
  
  print(a, s)
  print("Total missing value",s,s, data.isna().sum(),s)
  print("Percentage of missing value",s,s, round((data.isna().sum()*100/data.shape[0]),2).sort_values(ascending=True),s)
  print(reslt_dupli, s)
  plt.figure(figsize=(6,6))
  sns.heatmap(data.isna(), cbar=False)

# function to filter the values we want to keep
def keep(data, col, value):
    reslt = data[(data[col] == value) == True]
    return reslt

# function to filter the values we want to delete
def kick(data, col, value):
    reslt = data[(data[col] == value) == False]
    return reslt
