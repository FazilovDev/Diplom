import pandas as pd

data = pd.read_csv('data.csv')
data

data.describe()

data.head()
data.tail()

i = pd.notnull(data['MonthlyIncome']) & data['MonthlyIncome'] != 0
data.loc[i, 'DebtRatio'] *= data.loc[i, 'MonthlyIncome']
data


data.rename(columns={'DebtRatio':'Debt'}, inplace=True)
data


data['MonthlyIncome'].mean()
data


data['SeriousDlqin2yrs'].groupby(data['NumberRealEstateLoansOrLines']).mean()
import matplotlib.pyplot as plt

#  функция, позволяющая выводить графики прямо в ноутбук
get_ipython().run_line_magic('matplotlib', 'inline')


plt.scatter(data['age'], data['Debt'], c = data['SeriousDlqin2yrs'], cmap = 'RdYlBu_r')

fig, ax = plt.subplots()
i = pd.notnull(data['MonthlyIncome']) & (data['SeriousDlqin2yrs']==0)
ax.hist(data.loc[i, 'MonthlyIncome'], bins = 200, density=True)
i = pd.notnull(data['MonthlyIncome']) & (data['SeriousDlqin2yrs']==1)
ax.hist(data.loc[i, 'MonthlyIncome'], bins = 50, color='red', density=True, alpha=0.5)
ax.set_xlim(0,20000)
plt.show()



i = pd.notnull(data['MonthlyIncome']) & pd.notnull(data['NumberOfDependents'])
pd.plotting.scatter_matrix(data.loc[i, ['age', 'MonthlyIncome', 'NumberOfDependents']], figsize = [16, 16], 
                           marker=81, linewidths=49, s=64, c = data.loc[i, "SeriousDlqin2yrs"].to_numpy(), 
                           cmap="seismic")

i.sum()




