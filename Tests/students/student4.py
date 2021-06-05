import pandas as pd

data = pd.read_csv('data.csv', delimiter=',')

data.describe()
data.tail(10)
data.head()

i = pd.notnull(data.MonthlyIncome) & data['MonthlyIncome']!=0
data.loc[i,'DebtRatio'] *= data.loc[i,'MonthlyIncome']
data


data.rename(columns={'DebtRatio':'Debt'}, inplace=True)


a = data.loc[:,'MonthlyIncome'].mean(axis = 0 ,skipna = True)


i = pd.isnull(data.MonthlyIncome)
data.loc[i,'MonthlyIncome'] = a
data


data['SeriousDlqin2yrs'].groupby(data['NumberOfDependents']).mean()


data['SeriousDlqin2yrs'].groupby(data['NumberRealEstateLoansOrLines']).mean()


import matplotlib.pyplot as plt

#  функция, позволяющая выводить графики прямо в ноутбук
get_ipython().run_line_magic('matplotlib', 'inline')


yAxes = data[data.SeriousDlqin2yrs == 0]['Debt']
xAxes = data[data.SeriousDlqin2yrs == 0]['age']
yAxes2 = data[data.SeriousDlqin2yrs == 1]['Debt']
xAxes2 = data[data.SeriousDlqin2yrs == 1]['age']
fig, ax = plt.subplots()
ax.scatter(xAxes,yAxes,c = 'b') 
ax.scatter(xAxes2,yAxes2,c = 'r') 
plt.xlabel('Age')
plt.ylabel('Debt')
plt.show()


i = data[data.Debt == 0]['MonthlyIncome']
j = data[data.Debt != 0]['MonthlyIncome']

fig, ax1 = plt.subplots()
i.plot(kind = 'kde', color = 'blue', xlim = (0,25000))
j.plot(kind = 'kde', color = 'red', xlim = (0,25000))
plt.show()

pd.plotting.scatter_matrix(data[data['MonthlyIncome'] <= 25000][['age','MonthlyIncome','NumberOfDependents']],figsize=(13,13));




