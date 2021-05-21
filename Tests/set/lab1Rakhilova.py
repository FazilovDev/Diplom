import pandas as pd

data1 = pd.read_csv("data.csv", delimiter=',')


data1.describe()


data1.head(8)

data1.tail(3)


i = data1['MonthlyIncome'].notnull()
data1.loc[i, 'DebtRatio'] = data1.loc[i, 'DebtRatio'] * data1.loc[i, 'MonthlyIncome']
data1['DebtRatio']



data1.rename(columns={'DebtRatio':'Debt'}, inplace=True)
data1['Debt']

i1 = data1['MonthlyIncome'].isnull()
i2 = data1['MonthlyIncome'].notnull().mean()
data1.loc[i1,'MonthlyIncome'] = i2
data1['MonthlyIncome']


i1 = data1['SeriousDlqin2yrs'] == 1
i1.groupby(data1['NumberOfDependents']).mean()


i1 = data1['SeriousDlqin2yrs'] == 1
i1.groupby(data1['NumberRealEstateLoansOrLines']).mean()


import matplotlib.pyplot as plt

#  функция, позволяющая выводить графики прямо в ноутбук
get_ipython().run_line_magic('matplotlib', 'inline')


i1 = data1['SeriousDlqin2yrs'] == 0
x = data1.loc[i1, 'age']
y = data1.loc[i1, 'Debt']
fig1 = plt.scatter(x, y, color = 'blue')
i2 = data1['SeriousDlqin2yrs'] == 1
x = data1.loc[i2, 'age']
y = data1.loc[i2, 'Debt']
fig2 = plt.scatter(x, y, color = 'red')


i1 = data1['Debt'] > 0 
x = data1.loc[i1, 'MonthlyIncome']
fgr1 = x.plot.kde(color = 'red')
i2 = data1['Debt'] == 0
y = data1.loc[i2,'MonthlyIncome']
fgr2 = y.plot.kde(color = 'blue')
fgr1.axis([-10000,25000,0,0.00014])


i = data1[['age','MonthlyIncome', 'NumberOfDependents']]
pd.plotting.scatter_matrix(i, figsize = (6,6))

