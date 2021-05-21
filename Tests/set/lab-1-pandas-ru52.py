import pandas as pd
fn = "data.csv"
data = pd.read_csv(fn, delimiter=',')

data.describe()


data.head(10)


data.tail(10)


i = pd.notnull(data['MonthlyIncome']) & data['MonthlyIncome'] != 0
data.loc[i, 'DebtRatio'] *= data.loc[i, 'MonthlyIncome']
data

data.rename(columns={'DebtRatio':'Debt'}, inplace=True)
data


del_data = pd.notnull(data['MonthlyIncome']) & data['MonthlyIncome'] != 0
p_ch = data.loc[del_data, 'MonthlyIncome'].mean()
i = pd.isnull(data['MonthlyIncome'])
data.loc[i, 'MonthlyIncome'] = p_ch
data


data['SeriousDlqin2yrs'].groupby(data['NumberOfDependents']).mean() 

import matplotlib.pyplot as plt

#  функция, позволяющая выводить графики прямо в ноутбук
get_ipython().run_line_magic('matplotlib', 'inline')


x = data['age']
y = data['Debt']
z = data['SeriousDlqin2yrs']
plt.scatter(x, y, c = z, cmap='RdYlGn_r')


i = data['SeriousDlqin2yrs'] != 0
x = data.loc[i, 'MonthlyIncome']
y = data.loc[~i, 'MonthlyIncome']

fig, ax = plt.subplots()
ax.hist(x, color = 'r', bins=50, density = True)
ax.hist(y, color = 'b', bins=200, density = True, alpha=0.5)
ax.set_xlim(0,20000)

mio25k = data['MonthlyIncome'] <= 25000
age = data.loc[mio25k, 'age']
mi = data.loc[mio25k, 'MonthlyIncome']
nod = data.loc[mio25k, 'NumberOfDependents']

slov = {'MonthlyIncome' : mi, 'age' : age, 'NumberOfDependents' : nod}
twoage = pd.DataFrame(slov)
pd.plotting.scatter_matrix(twoage)

