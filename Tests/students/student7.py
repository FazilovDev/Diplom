import pandas as pd

dt=pd.read_csv('data.csv', delimiter=',')

dt.describe()


dt.head(12)
dt.tail(12)


i = pd.notnull(dt['MonthlyIncome']) & (dt['MonthlyIncome'] != 0) # выбираем строки, в которых не указан доход
dt.loc[i, 'DebtRatio']*=dt.loc[i, 'MonthlyIncome']
dt


dt.rename(columns={'DebtRatio':'Debt'}, inplace=True)
dt


meanincome=dt.mean()['MonthlyIncome']
i = pd.notnull(dt['MonthlyIncome']) & dt['MonthlyIncome'] == 0
dt.loc[i, 'MonthlyIncome'] = meanincome
dt


dt['SeriousDlqin2yrs'].groupby(dt['NumberOfDependents']).mean()
dt['SeriousDlqin2yrs'].groupby(dt['NumberRealEstateLoansOrLines']).mean()


import matplotlib.pyplot as plt

#  функция, позволяющая выводить графики прямо в ноутбук
get_ipython().run_line_magic('matplotlib', 'inline')


fig, ax = plt.subplots()
ser0 = dt['SeriousDlqin2yrs'] == 0
ser0X = dt.loc[ser0, 'age']
ser0Y = dt.loc[ser0, 'Debt']
ser1 = dt['SeriousDlqin2yrs'] == 1
ser1X = dt.loc[ser1, 'age']
ser1Y = dt.loc[ser1, 'Debt']
ax.scatter(ser0X, ser0Y, c='b')
ax.scatter(ser1X, ser1Y, c='r')
plt.show()


import scipy.stats as st
import numpy as np
fig, ax = plt.subplots()
i = dt['SeriousDlqin2yrs'] == 0
gr1 = dt.loc[i, 'MonthlyIncome']
j = dt['SeriousDlqin2yrs'] == 1
gr2 = dt.loc[j, 'MonthlyIncome']
ax.set_xlim([0,25000])
fit1 = st.norm.pdf(gr1.sort_values(), np.mean(gr1.sort_values()), np.std(gr1.sort_values())) #this is a fitting indeed
ax.plot(gr1.sort_values(),fit1,'-o', c='b')
fit2 = st.norm.pdf(gr2.sort_values(), np.mean(gr2.sort_values()), np.std(gr2.sort_values())) #this is a fitting indeed
ax.plot(gr2.sort_values(),fit2,'-o', c='r')
plt.show()

temp = pd.DataFrame(dt, columns = ['age', 'MonthlyIncome', 'NumberOfDependents'])
pd.plotting.scatter_matrix(temp)



