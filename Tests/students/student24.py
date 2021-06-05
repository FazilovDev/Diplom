data = pd.read_csv('data.csv', delimiter=',')
data


data.describe()

data.head(20)

data.tail(4)

i = pd.notnull(data['MonthlyIncome']) & data['MonthlyIncome'] > 0
data.loc[i, 'DebtRatio'] *= data.loc[i, 'MonthlyIncome']
data.head(20)


data.rename(columns={'DebtRatio':'Debt'}, inplace=True)
data

income = data.mean()['MonthlyIncome']
i = pd.notnull(data['MonthlyIncome']) & data['MonthlyIncome'] == 0
data.loc[i, 'MonthlyIncome'] = income
data.head(20)

data['SeriousDlqin2yrs'].groupby(data['NumberOfDependents']).mean()

import matplotlib.pyplot as plt

get_ipython().run_line_magic('matplotlib', 'inline')

import scipy.stats as stats
import numpy as np

fig, ax = plt.subplots()

i = data['SeriousDlqin2yrs'] == 0
gr1 = data.loc[i, 'MonthlyIncome']
j = data['SeriousDlqin2yrs'] == 1
gr2 = data.loc[j, 'MonthlyIncome']

ax.set_xlim([0,25000])

fit1 = stats.norm.pdf(gr1.sort_values(), np.mean(gr1.sort_values()), np.std(gr1.sort_values())) #this is a fitting indeed
ax.plot(gr1.sort_values(),fit1,'-o', c='b')

fit2 = stats.norm.pdf(gr2.sort_values(), np.mean(gr2.sort_values()), np.std(gr2.sort_values())) #this is a fitting indeed
ax.plot(gr2.sort_values(),fit2,'-o', c='r')

plt.show()



i = data['MonthlyIncome'] < 25000
pd.plotting.scatter_matrix(pd.DataFrame(list(zip(data['age'], data.loc[i, 'MonthlyIncome'], data['NumberOfDependents'])), columns=['age','MonthlyIncome', 'NumberOfDependents']))

