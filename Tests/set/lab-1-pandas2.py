import pandas as pd

data = pd.read_csv("data_full.csv", delimiter=',')

data.describe()

data.head(3)

data.tail(3)

data['DebtRatio'] = data['DebtRatio'] * data['MonthlyIncome']

data.rename(columns={'DebtRatio':'Debt'}, inplace=True)

data.loc[pd.isnull(data['MonthlyIncome']), 'MonthlyIncome'] = data.mean()['MonthlyIncome']

data['SeriousDlqin2yrs'].groupby(data['NumberOfDependents']).mean()


data['NumberRealEstateLoansOrLines'].groupby(data['NumberOfDependents']).mean()

import matplotlib.pyplot as plt

get_ipython().run_line_magic('matplotlib', 'inline')


fig, axes = plt.subplots()
data.loc[data['SeriousDlqin2yrs'] == 0].plot(x = 'age', y = 'Debt', kind='scatter', color = 'blue', ax = axes)
data.loc[data['SeriousDlqin2yrs'] == 1].plot(x = 'age', y = 'Debt', kind='scatter', color = 'red', ax = axes)
plt.show()


data[data['MonthlyIncome'] < 0].count()['Id']



fig, axes2 = plt.subplots()
data.loc[data['Debt'] == 0, 'MonthlyIncome'].plot(kind='kde', color = 'blue', ax = axes2, xlim=(0,25000))
data.loc[data['Debt'] != 0, 'MonthlyIncome'].plot(kind='kde', color = 'red', ax = axes2, xlim=(0,25000))
plt.show()

import seaborn as sns
sns.kdeplot(data=data, x='MonthlyIncome', hue='SeriousDlqin2yrs', common_norm=False, clip=(0, 25000))
plt.show()


pd.plotting.scatter_matrix(data[['age', 'MonthlyIncome', 'NumberOfDependents']], figsize = (13, 13), color = 'red')
plt.show()



