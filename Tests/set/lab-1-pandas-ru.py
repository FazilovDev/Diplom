import pandas as pd


df = pd.read_csv("data.csv", delimiter=",", index_col="Id")

df.describe()



df.head()

df.tail()



i = pd.notnull(df['MonthlyIncome']) & df['MonthlyIncome']!=0
df.loc[i, 'DebtRatio'] *= df.loc[i, 'MonthlyIncome']


df.loc[i, 'DebtRatio']


df.rename(columns={'DebtRatio':'Debt'}, inplace=True)


meanMonthlyIncome = df.loc[i, 'MonthlyIncome'].mean()
withNoIncomeSelector = pd.isnull(df['MonthlyIncome'])
df.loc[withNoIncomeSelector, 'MonthlyIncome'] = meanMonthlyIncome




df['SeriousDlqin2yrs'].groupby(df['NumberOfDependents']).mean()


df['SeriousDlqin2yrs'].groupby(df['NumberRealEstateLoansOrLines']).mean()


import matplotlib.pyplot as plt

#  функция, позволяющая выводить графики прямо в ноутбук
get_ipython().run_line_magic('matplotlib', 'inline')


fig, ax = plt.subplots()

noSeriousDebtSelector = df['SeriousDlqin2yrs'] == 0
ax.scatter(df.loc[noSeriousDebtSelector, 'age'], df.loc[noSeriousDebtSelector, 'Debt'], color='blue')

debtSelector = df['SeriousDlqin2yrs'] == 1
ax.scatter(df.loc[debtSelector, 'age'], df.loc[debtSelector, 'Debt'], color='red')

plt.show()

indebted = df.loc[debtSelector, 'MonthlyIncome']
notindebted = df.loc[noSeriousDebtSelector, 'MonthlyIncome']

plt.hist([indebted, notindebted], density=True, color=['red', 'blue'], range=(0,25000), histtype='step')

plt.show()


incomeRestriction = df['MonthlyIncome'] < 25000
df_res = pd.DataFrame({'age':df['age'],
                   'MonthlyIncome':df.loc[incomeRestriction, 'MonthlyIncome'],
                   'NumberOfDependents':df['NumberOfDependents']})

pd.plotting.scatter_matrix(df_res)
