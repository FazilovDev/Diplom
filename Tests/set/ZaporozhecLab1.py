
import pandas as pd



d = pd.read_csv("C:\\Users\\Artem\\Desktop\\ФИИТ\\Машинное обучение(практика)\\Lab1\\data.csv", delimiter=',')

d.describe()

d.head(6)
d.tail(2)
print(' SeriousDlqin2yrs = категориальный \n RevolvingUtilizationOfUnsecuredLines = real \n age = integer \n NumberOfTime30-59DaysPastDueNotWorse = integer \n DebtRatio = real \n MonthlyIncome = real \n NumberOfOpenCreditLinesAndLoans = integer \n NumberOfTimes90DaysLate = integer \n', 
'NumberRealEstateLoansOrLines = integer \n NumberOfTime60-89DaysPastDueNotWorse = integer \n NumberOfDependents = integer \n')

i = d['MonthlyIncome'].notnull()
d.loc[i, 'DebtRatio'] = d.loc[i, 'DebtRatio']*d.loc[i,'MonthlyIncome']
d['DebtRatio']


d.rename(columns={'DebtRatio':'Debt'}, inplace=True)
d['Debt']
medium_MonthlyIncome = d.loc[i, 'MonthlyIncome'].mean()
print('Средний ежемесячный доход = ', medium_MonthlyIncome)
i1 = d['MonthlyIncome'].isnull()
d.loc[i1, 'MonthlyIncome'] = medium_MonthlyIncome
d['MonthlyIncome']

key = d['SeriousDlqin2yrs'] == 1
group_count = d.loc[key, 'SeriousDlqin2yrs'].groupby(d['NumberOfDependents']).count()
count_all = d['SeriousDlqin2yrs'].count()

for i in range(group_count.count()):
    probably = group_count[i] / count_all
    print('Вероятность невозврата кредита =', '%0.4f'%probably,', при значении иждивенца = ', i)
print('\n')
    
group_count = d.loc[key, 'SeriousDlqin2yrs'].groupby(d['NumberRealEstateLoansOrLines']).count()
count_all = d['SeriousDlqin2yrs'].count()

for x in group_count.keys():
    probably = group_count[x] / count_all
    print('Вероятность невозврата кредита =', '%0.4f'%probably,', при количестве ипотек = ', x)    


import matplotlib.pyplot as plt


get_ipython().run_line_magic('matplotlib', 'inline')



if1 = d['SeriousDlqin2yrs'] == 0
x1 = d.loc[if1, 'age']
y1 = d.loc[if1, 'Debt']
figure1 = plt.scatter(x1, y1, c = 'b')
if2 = d['SeriousDlqin2yrs'] == 1
x2 = d.loc[if2, 'age']
y2 = d.loc[if2, 'Debt']
figure2 = plt.scatter(x2, y2, c = 'r')

if1 = d['Debt'] > 0
x1 = d.loc[if1, 'MonthlyIncome']
figure1 = x1.plot.kde(c = 'r')
if2 = d['Debt'] == 0
x2 = d.loc[if2, 'MonthlyIncome']
figure2 = x2.plot.kde(c  ='b')
figure2.axis([d['MonthlyIncome'].min(),25000,0,0.0002])



if1 = d['MonthlyIncome'] <= 25000
pd.plotting.scatter_matrix(d.loc[if1,['age', 'MonthlyIncome', 'NumberOfDependents']], figsize = (20, 20))


