import pandas as pd


data = pd.read_csv("data.csv",delimiter=",")
data.describe()

data.head(15) #Первые 15 записей
data.tail(3) #Последние 3 записи


nonnulls = pd.notnull(data["MonthlyIncome"]) & data["MonthlyIncome"]!=0
data[nonnulls]


nonnulls = pd.notnull(data["MonthlyIncome"]) & data["MonthlyIncome"]!=0
data.loc[nonnulls,"DebtRatio"] = data.loc[nonnulls,"MonthlyIncome"] * data.loc[nonnulls,"DebtRatio"]#


data.head()


data.rename(columns = {'DebtRatio':"Debt"},inplace = True)


nulls = pd.isnull(data["MonthlyIncome"]) 
data.loc[nulls,"MonthlyIncome"] = data.mean(skipna=True)["MonthlyIncome"]


data['SeriousDlqin2yrs'].groupby(data['NumberOfDependents']).mean()


data['SeriousDlqin2yrs'].groupby(data['NumberRealEstateLoansOrLines']).mean()


import matplotlib.pyplot as plt


get_ipython().run_line_magic('matplotlib', 'inline')


plt.figure(figsize=(12, 6))
groups = data.groupby('SeriousDlqin2yrs')
colors = ['blue','red']
for tmp,color in zip(groups, colors):
    name, group = tmp
    plt.plot(group["age"], group["Debt"], marker="o", linestyle="", label='SeriousDlqin2yrs = ' + str(name),color = color)
plt.legend()


data[data['SeriousDlqin2yrs']==0]['MonthlyIncome'].plot.kde(color = 'blue')
data[data['SeriousDlqin2yrs']==1]['MonthlyIncome'].plot.kde(color = 'red')
plt.xlim(-20000,25000)


data_new = data[data['MonthlyIncome']<=25000]
import seaborn as sns
g = sns.PairGrid(data_new, vars=['age', 'MonthlyIncome', 'NumberOfDependents'])
g.map(plt.scatter)

