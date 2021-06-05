
import pandas as pd

data = pd.read_csv('data.csv', delimiter=',')

data.describe()


data.head()
data.tail(7)


i = pd.notnull(data['MonthlyIncome']) & data['MonthlyIncome'] != 0
data.loc[i, 'DebtRatio'] *= data.loc[i, 'MonthlyIncome']
data

data.rename(columns={'DebtRatio':'Debt'}, inplace=True)
data


avg0 = data.mean(axis=0)
avg = avg0['MonthlyIncome']
#avg
j = pd.isnull(data['MonthlyIncome']) 
#j
data.loc[j, 'MonthlyIncome'] = avg
data.tail(10)


data['SeriousDlqin2yrs'].groupby(data['NumberOfDependents']).mean()


data['SeriousDlqin2yrs'].groupby(data['NumberRealEstateLoansOrLines']).mean()



import matplotlib.pyplot as plt
import scipy.stats as stats
import numpy as np

get_ipython().run_line_magic('matplotlib', 'inline')


b = data['SeriousDlqin2yrs'] == 0
p1 = plt.scatter(data.loc[b,'age'], data.loc[b,'Debt'], c='blue')
p1
r = data['SeriousDlqin2yrs'] == 1
p2 = plt.scatter(data.loc[r,'age'], data.loc[r,'Debt'], c='red')
p2


r1 = data.loc[r, 'MonthlyIncome']     # с задолженностями
b1 = data.loc[b, 'MonthlyIncome']     # без задолженностей

r2 = r1.sort_values()
b2 = b1.sort_values()

plt.plot(r2, stats.norm.pdf(r2, np.mean(r2), np.std(r2)), color='red')
plt.plot(b2, stats.norm.pdf(b2, np.mean(b2), np.std(b2)), color='blue')

plt.axis([0, 25000, 0, 1e-4])

plt.show()
