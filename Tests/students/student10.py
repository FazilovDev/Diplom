import pandas as pd

data = pd.read_csv("data.csv", delimiter=',')
data.describe()


data.head()

data.tail()


data['DebtRatio']*=data['MonthlyIncome']
data.tail()


data.rename(columns={'DebtRatio':'Debt'}, inplace=True)


data.loc[pd.isnull(data['MonthlyIncome']), 'MonthlyIncome'] = data['MonthlyIncome'].mean()

data['SeriousDlqin2yrs'].groupby(data['NumberOfDependents']).mean()


# In[11]:


data['NumberRealEstateLoansOrLines'].groupby(data['NumberOfDependents']).mean()


import matplotlib.pyplot as plt

#  функция, позволяющая выводить графики прямо в ноутбук
get_ipython().run_line_magic('matplotlib', 'inline')



fig, ax1 = plt.subplots()
data.loc[data['SeriousDlqin2yrs']== 0].plot.scatter('age','Debt', color='blue',ax=ax1)
data.loc[data['SeriousDlqin2yrs']== 1].plot.scatter('age','Debt', color='red',ax=ax1)
plt.show()



fig, ax2 =plt.subplots()
data.loc[data['Debt']== 0,'MonthlyIncome'].plot.kde(color='blue',xlim=(0,25000),ax=ax2)
data.loc[data['Debt']!= 0,'MonthlyIncome'].plot.kde(color='red',xlim=(0,25000),ax=ax2)
plt.show()


pd.plotting.scatter_matrix(data[['age', 'MonthlyIncome', 'NumberOfDependents']],figsize = (10,10),color = 'green')
plt.show()
