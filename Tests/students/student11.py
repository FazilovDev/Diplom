import pandas as pd


dataf = pd.read_csv('data.csv', delimiter=',')


dataf.describe()




dataf.head(3)


dataf.tail(4)


dataf.loc[pd.notnull(dataf['MonthlyIncome']), 'DebtRatio'] *= dataf.loc[pd.notnull(dataf['MonthlyIncome']), 'MonthlyIncome']

dataf['DebtRatio']



dataf.rename(columns={'DebtRatio':'Debt'}, inplace=True)



dataf['Debt']

meanIncome = dataf['MonthlyIncome'].mean()
dataf.loc[pd.isnull(dataf['MonthlyIncome']), 'MonthlyIncome'] = meanIncome
dataf.loc[pd.isnull(dataf['MonthlyIncome']), 'MonthlyIncome']



dataf['SeriousDlqin2yrs'].groupby(dataf['NumberOfDependents']).mean()


dataf['SeriousDlqin2yrs'].groupby(dataf['NumberRealEstateLoansOrLines']).mean()



import matplotlib.pyplot as plt

#  функция, позволяющая выводить графики прямо в ноутбук
get_ipython().run_line_magic('matplotlib', 'inline')


x1 = dataf.loc[dataf['SeriousDlqin2yrs'] == 0, 'age']
x2 = dataf.loc[dataf['SeriousDlqin2yrs'] == 1, 'age']

y1 = dataf.loc[dataf['SeriousDlqin2yrs'] == 0, 'Debt']
y2 = dataf.loc[dataf['SeriousDlqin2yrs'] == 1, 'Debt']

pl0, pl1 = plt.subplots()
pl0 = plt.scatter(x1, y1, color='blue')
pl1 = plt.scatter(x2, y2, color='red')
plt.show()


x1 = dataf.loc[dataf['SeriousDlqin2yrs'] == 1, 'MonthlyIncome']
x2 = dataf.loc[dataf['SeriousDlqin2yrs'] == 0, 'MonthlyIncome']

plt.hist([x1, x2], range=(0,25000), density=True, color=['red', 'blue'])
plt.show()


df = pd.DataFrame()
df['age'] = dataf.loc[dataf['MonthlyIncome'] <= 25000, 'age']
df['MonthlyIncome'] = dataf.loc[dataf['MonthlyIncome'] <= 25000, 'MonthlyIncome']
df['NumberOfDependents'] = dataf.loc[dataf['MonthlyIncome'] <= 25000, 'NumberOfDependents']
pd.plotting.scatter_matrix(df, figsize=(10,10), alpha=0.2)
