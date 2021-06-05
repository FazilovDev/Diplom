import pandas as pd
data = pd.read_csv('data.csv', delimiter=',')

data.describe()

data.head(10)


data.tail()
is_monthly_income_not_NaN = pd.notnull(data['MonthlyIncome'])
data.loc[is_monthly_income_not_NaN, 'DebtRatio'] *= data.loc[is_monthly_income_not_NaN, 'MonthlyIncome']


data.head(10)


data.rename(columns={'DebtRatio': 'Debt'}, inplace=True)
data.head()


monthly_income_mean = data['MonthlyIncome'].mean()
data['MonthlyIncome'].fillna(monthly_income_mean, inplace=True)
data.head(10)


data['SeriousDlqin2yrs'].groupby(data['NumberOfDependents']).mean()

data['SeriousDlqin2yrs'].groupby(data['NumberRealEstateLoansOrLines']).mean()

import matplotlib.pyplot as plt

#  функция, позволяющая выводить графики прямо в ноутбук
get_ipython().run_line_magic('matplotlib', 'inline')


groups = data.groupby('SeriousDlqin2yrs')

fig, ax = plt.subplots()
for name, group in groups:
    clr = 'blue' if name == 0 else 'red'
    ax.plot(group['age'], group['Debt'], marker='o', linestyle='', c=clr, label="SeriousDlqin2yrs = "+str(name))
ax.legend()
plt.xlabel("age")
plt.ylabel("Debt")
plt.show()

fig, ax = plt.subplots()
for name, group in groups:
    clr = 'blue' if name == 0 else 'red'
    ax.hist(x=group['MonthlyIncome'], bins=50, range=(0,25000), density=True, color=clr, label="SeriousDlqin2yrs = "+str(name))
ax.legend()
plt.xlabel("MonthlyIncome")
plt.ylabel("Density")
plt.show()


dt = data.loc[data['MonthlyIncome'] <= 25000]
pd.plotting.scatter_matrix(dt[['age', 'MonthlyIncome', 'NumberOfDependents']], figsize=(10,8))

