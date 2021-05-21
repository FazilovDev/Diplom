import pandas as pd


df = pd.read_csv('data.csv', delimiter=',')
df.describe()

df.head(n=3)


df.tail(n=4)


df.describe()


idxs = pd.notnull(df['DebtRatio'])
df.loc[idxs, 'DebtRatio'] = df.loc[idxs,'DebtRatio'] * df.loc[idxs, 'MonthlyIncome']
df.describe()



df.rename(columns={'DebtRatio':'Debt'}, inplace=True)
df.describe()

mean = df['MonthlyIncome'].mean()
df['MonthlyIncome'] = df['MonthlyIncome'].fillna(value=mean)

df['SeriousDlqin2yrs'].groupby(df['NumberOfDependents']).mean()


df['SeriousDlqin2yrs'].groupby(df['NumberRealEstateLoansOrLines']).mean()


import matplotlib.pyplot as plt

#  функция, позволяющая выводить графики прямо в ноутбук
get_ipython().run_line_magic('matplotlib', 'inline')



_, ax = plt.subplots()

is_debt = df['SeriousDlqin2yrs'] == 0
is_not_debt = df['SeriousDlqin2yrs'] == 1

ax.scatter(df.loc[is_debt, 'age'], df.loc[is_debt,'Debt'])
ax.scatter(df.loc[is_not_debt, 'age'], df.loc[is_not_debt,'Debt'], color='red')
ax.set_xlabel("AGE")
ax.set_ylabel("DEBT")
plt.show()



lim_df = df[df['MonthlyIncome'] <= 25000]
y1 = lim_df[lim_df['SeriousDlqin2yrs'] == 0]['MonthlyIncome']
y2 = lim_df[lim_df['SeriousDlqin2yrs'] == 1]['MonthlyIncome']

_, ax = plt.subplots()
ax.hist(y1,density=True, label='Debtors')
ax.hist(y2,density=True, color='red', label='Not debtors')
ax.legend()
plt.show()


from pandas.plotting import scatter_matrix

lim_df = df[df['MonthlyIncome'] <= 25000]


scatter_matrix(lim_df.loc[:, ['age', 'MonthlyIncome', 'NumberOfDependents']], figsize=[15, 15])



