import pandas as pd

import pandas as pd
data = pd.read_csv('data.csv', delimiter=',')
data



data.describe()


data.head()

data.tail()


i = data['MonthlyIncome'].notnull()

data.loc[i, 'DebtRatio']= data.loc[i, 'DebtRatio'] *data.loc[i, 'MonthlyIncome']
data

data.rename(columns={'DebtRatio':'Debt'}, inplace=True)
data


k = data['MonthlyIncome'].mean()
k1 = data[ 'MonthlyIncome'].isnull()
data.loc[k1,'MonthlyIncome'] = k
data



data['SeriousDlqin2yrs'].groupby(data['NumberOfDependents']).mean()


import matplotlib.pyplot as plt

get_ipython().run_line_magic('matplotlib', 'inline')



import matplotlib.pyplot as plt

fig, axes = plt.subplots()
data.loc[data['SeriousDlqin2yrs'] == 0].plot(x='age',y='Debt',kind='scatter',ax=axes)
data.loc[data['SeriousDlqin2yrs'] == 1].plot(x='age',y='Debt',kind='scatter',color='red',ax=axes)

plt.show()




fig1, axes1 = plt.subplots()
data.loc[(data['NumberOfTime30-59DaysPastDueNotWorse'] == 0) & (data['NumberOfTimes90DaysLate'] == 0)& (data['NumberOfTime60-89DaysPastDueNotWorse'] == 0), 'MonthlyIncome'].plot(kind='kde',ax=axes1,xlim=(0,25000))
data.loc[(data['NumberOfTime30-59DaysPastDueNotWorse'] > 0) & (data['NumberOfTimes90DaysLate'] > 0)& (data['NumberOfTime60-89DaysPastDueNotWorse'] > 0), 'MonthlyIncome'].plot(kind='kde',color='red',ax=axes1,xlim=(0,25000))

plt.show()

d = {'AGE': data['age'], 'MI': data.loc[data['MonthlyIncome'] < 25000,'MonthlyIncome'], 'ND': data['NumberOfDependents']}
df = pd.DataFrame(data=d)

pd.plotting.scatter_matrix(df)



