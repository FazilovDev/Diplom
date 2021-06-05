import pandas as pd


myData = pd.read_csv('data.csv', delimiter=',')


myData.describe()

myData.head(4)

myData.tail(6)




tec = myData['DebtRatio'].notnull()
myData.loc[tec, 'DebtRatio'] = myData.loc[tec, 'DebtRatio']*myData.loc[tec, 'MonthlyIncome']
myData['DebtRatio']


myData.rename(columns={'DebtRatio':'Debt'}, inplace = True)
myData['Debt']


everyMonths = myData['MonthlyIncome'].mean()
i = myData['MonthlyIncome'].isnull()
myData.loc[i, 'MonthlyIncome'] = everyMonths
myData['MonthlyIncome']


tec = myData['SeriousDlqin2yrs'] == 1
tec.groupby(myData['NumberOfDependents']).mean()


tec = myData['SeriousDlqin2yrs'] == 1
tec.groupby(myData['NumberRealEstateLoansOrLines']).mean()


import matplotlib.pyplot as plt

#  функция, позволяющая выводить графики прямо в ноутбук
get_ipython().run_line_magic('matplotlib', 'inline')



i = myData['SeriousDlqin2yrs'] == 0
x = myData.loc[i,'age']
y = myData.loc[i,'Debt']
figure = plt.scatter(x, y, color = 'blue')
i1 = myData['SeriousDlqin2yrs'] == 1
x1 = myData.loc[i1,'age']
y1 = myData.loc[i1,'Debt']
figure1 = plt.scatter(x1, y1, color = 'red')


i = myData['Debt'] == 0
x = myData.loc[i, 'MonthlyIncome']
figure = x.plot.kde(color = 'blue')
figure.axis([-20000,25000,0.0,0.0002])
i1 = myData['Debt'] > 0
x1 = myData.loc[i1, 'MonthlyIncome']
figure1 = x1.plot.kde(color = 'red')


i = myData[['age','MonthlyIncome', 'NumberOfDependents']]
pd.plotting.scatter_matrix(i, figsize = (6,6))




