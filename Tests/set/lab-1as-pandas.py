
import pandas as pd

data = pd.read_csv('data.csv', delimiter=',')


data.describe()

data.head()


data.tail()

i = pd.notnull(data['MonthlyIncome'])
data.loc[i, 'DebtRatio'] = data.loc[i, 'DebtRatio'] * data.loc[i, 'MonthlyIncome']

data.rename(columns={'DebtRatio': 'Debt'}, inplace=True)
null_income = pd.isnull(data['MonthlyIncome'])
mean_income = data['MonthlyIncome'].mean()
data.loc[null_income, ['MonthlyIncome']] = mean_income

data['SeriousDlqin2yrs'].groupby(data['NumberRealEstateLoansOrLines']).mean()

import matplotlib.pyplot as plt

#  функция, позволяющая выводить графики прямо в ноутбук
get_ipython().run_line_magic('matplotlib', 'inline')


plt.scatter(data['age'], data['Debt'], c = data['SeriousDlqin2yrs'], cmap='bwr')
plt.show()



clients_with_debt = data.loc[data['Debt'] > 0, 'MonthlyIncome']
clients_without_debt = data.loc[data['Debt'] == 0, 'MonthlyIncome']
plt1 = clients_with_debt.plot.kde(color='red')
plt2 = clients_without_debt.plot.kde(color='blue')
plt1.axis([-10000, 30000, 0, 0.00014])

data2 = data[['age', 'MonthlyIncome', 'NumberOfDependents']]
pd.plotting.scatter_matrix(data2)

