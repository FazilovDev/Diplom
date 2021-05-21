
import numpy
import pandas as pd

data_csv = pd.read_csv('data.csv', delimiter=',')

data_csv.describe()

data_csv.head(n=11)

tailed = data_csv.tail(n=19)
if isinstance(tailed, pd.DataFrame):
	print("tail возвращает DataFrame")

del tailed

data_csv.dtypes

filter1 = data_csv['MonthlyIncome'].notnull()
filter2 = data_csv['MonthlyIncome'] != 0
mixed_filter = filter1 & filter2
to_index = data_csv[mixed_filter]
data_csv.loc[mixed_filter, 'DebtRatio'] = to_index['MonthlyIncome'] * to_index['DebtRatio']


data_csv.rename(columns={'DebtRatio': 'Debt'}, inplace=True)

mean_income = data_csv['MonthlyIncome'].mean()
filter3 = data_csv['MonthlyIncome'].isnull()
data_csv.loc[filter3, 'MonthlyIncome'] = mean_income

data_csv['SeriousDlqin2yrs'].groupby(data_csv['NumberOfDependents']).mean()


data_csv['SeriousDlqin2yrs'].groupby(data_csv['NumberOfDependents']).count()


data_csv['SeriousDlqin2yrs'].groupby(data_csv['NumberRealEstateLoansOrLines']).mean()


data_csv['SeriousDlqin2yrs'].groupby(data_csv['NumberRealEstateLoansOrLines']).count()



import matplotlib.pyplot as plt

get_ipython().run_line_magic('matplotlib', 'inline')



colors_red = data_csv['SeriousDlqin2yrs'] == 1
colors_blue = data_csv['SeriousDlqin2yrs'] == 0
points_red = data_csv[colors_red]
points_blue = data_csv[colors_blue]
# Не пишем в глобальном plt
fig, axes = plt.subplots()
axes.scatter(points_red['age'], points_red['Debt'], s=2, marker='s', color='#FF0000')
axes.scatter(points_blue['age'], points_blue['Debt'], s=2, marker='s', color='#0000FF')
fig.show()
# место для кода


fig, axes = plt.subplots()

axes.set_xlim(right=25000)
axes.hist(data_csv['MonthlyIncome'][colors_red], color='#FF0000', density=True, bins=100)
axes.hist(data_csv['MonthlyIncome'][colors_blue], color='#0000FF', density=True, bins=100)
fig.show()


clients_no_debt = data_csv[data_csv['SeriousDlqin2yrs'] == 1].groupby('MonthlyIncome')['MonthlyIncome'].count()
clients_debt = data_csv[data_csv['SeriousDlqin2yrs'] == 0].groupby('MonthlyIncome')['MonthlyIncome'].count()
axes.scatter(clients_debt.index, clients_debt, s=3, marker='s', color='#FF0000')
axes.scatter(clients_no_debt.index, clients_no_debt, s=3, marker='s', color='#0000FF')

fig.show()

df = data_csv[['age', 'NumberOfDependents', 'MonthlyIncome']]
axes = pd.plotting.scatter_matrix(df)
for i in range(2):
	axes[i, 2].set_xlim((0, 25000))
	axes[2, i].set_ylim((0, 25000))
fig.show()

