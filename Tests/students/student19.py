import pandas as pd
data = pd.read_csv('data.csv', delimiter=',')


data.describe()
data.head(3)




data.tail(3)


idxs = pd.notnull(data['DebtRatio'])
data.loc[idxs, 'DebtRatio'] = data.loc[idxs,'DebtRatio'] * data.loc[idxs, 'MonthlyIncome']
data.rename(columns={'DebtRatio':'Debt'}, inplace=True)

mean_val = data['MonthlyIncome'].mean()
data['MonthlyIncome'] = data['MonthlyIncome'].fillna(mean_val)

data['SeriousDlqin2yrs'].groupby(data['NumberOfDependents']).mean() 


data['SeriousDlqin2yrs'].groupby(data['NumberRealEstateLoansOrLines']).mean()


import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')


_, ax = plt.subplots()
ax.scatter(data.loc[data['SeriousDlqin2yrs'] == 0, 'age'], data.loc[data['SeriousDlqin2yrs'] == 0,'Debt'])
ax.scatter(data.loc[data['SeriousDlqin2yrs'] == 1, 'age'], data.loc[data['SeriousDlqin2yrs'] == 1,'Debt'], color='red')
ax.set_xlabel("AGE")
ax.set_ylabel("DEBT")
plt.show()
get_ipython().run_line_magic('matplotlib', 'inline')

y1 = data[(data['MonthlyIncome'] <= 25000)]
y2 = data[(data['MonthlyIncome'] <= 25000)]


y1 = y1[y1['SeriousDlqin2yrs'] == 0]['MonthlyIncome']
y2 = y2[y2['SeriousDlqin2yrs'] == 1]['MonthlyIncome']


import seaborn as sns

_, ax = plt.subplots()
ax.hist(y1, density=True, label='Задолжники')
ax.hist(y2, density=True, color='r', label='Выплачивающие')
ax.legend()
plt.show()

n_data = data[(data['MonthlyIncome'] <= 25000)]



sns.pairplot(n_data.loc[:, ['age', 'MonthlyIncome', 'NumberOfDependents']], size=5)
