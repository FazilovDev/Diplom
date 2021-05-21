
import pandas as pd
import matplotlib.pyplot as plt

get_ipython().run_line_magic('matplotlib', 'inline')

data = pd.read_csv('data.csv', delimiter=',')

data.describe()


data.head(15)


df = pd.read_csv('DataDictionary-ru.txt', header=None, error_bad_lines=False)

df.info()
import pandas as pd
from pandas.api.types import CategoricalDtype
drop_thresh = df.shape[0]*.9
df_raw =df.dropna(thresh=drop_thresh, how='all', axis='columns').copy()
df_raw.info()

data = data.rename(columns={'DebtRatio': 'Debt'})
data.head(20)


data.loc[data['MonthlyIncome'] == 0, 'MonthlyIncome'] = None
data.loc[data['MonthlyIncome'].notnull(), 'Debt'] *= data['MonthlyIncome'] 
data.loc[data['MonthlyIncome'].isnull(), 'MonthlyIncome'] = data['MonthlyIncome'].mean()
data.head(20)


data['SeriousDlqin2yrs'].groupby(data['NumberOfDependents']).mean()



data['SeriousDlqin2yrs'].groupby(data['NumberRealEstateLoansOrLines']).mean()

import matplotlib.pyplot as plt


get_ipython().run_line_magic('matplotlib', 'inline')


colors_map = {0: 'b', 1: 'r'}
colors = data['SeriousDlqin2yrs'].map(colors_map)
plt.scatter(data['age'], data['Debt'], c=colors, alpha=0.4)
plt.xlabel('Age')
plt.ylabel('Debt')
plt.show()


fig, ax = plt.subplots()
ax.hist(data['MonthlyIncome'].loc[data['SeriousDlqin2yrs'] == 0], bins=500)
ax.hist(data['MonthlyIncome'].loc[data['SeriousDlqin2yrs'] == 1], bins=500, color='red')
ax.axis([0, 25000, 0, 500])
plt.show()


dataSampling = data.loc[['age','NumberofDependents','MonthlyIncome']]
dataSamplingLimit = dataSampling.loc['MonthlyIncome'] <= 25000 
pd.plotting.scatter_matrix(dataSamplingLimit, figsize=(15,8,75))



