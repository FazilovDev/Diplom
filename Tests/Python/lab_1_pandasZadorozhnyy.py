#!/usr/bin/env python
# coding: utf-8

# ## Полезные ссылки

# **Начало работы**
# 
# - Anaconda (дистрибутив для Python, содержащий в том числе Jupyter Notebook и сам Python): https://www.anaconda.com/download/ - рекомендуется версия Python 3.6 или больше; не забудьте выбрать нужную операционную систему!
# - документация по Jupyter: https://jupyter.readthedocs.io/en/latest/
# - документация по pip (для установки пакетов в Python с помощью pip install): https://pip.readthedocs.io/en/latest/
# - PyCharm: https://www.jetbrains.com/pycharm/
# 
# **Общее**
# 
# - для любых вопросов: https://www.google.com/
# - для (почти) любых ответов: https://stackoverflow.com/
# - профессиональный информационно-аналитический ресурс, посвященный машинному обучению, распознаванию образов и интеллектуальному анализу данных: http://www.machinelearning.ru/wiki/index.php?title=Заглавная_страница
# - A visual introduction to machine learning: http://www.r2d3.us/visual-intro-to-machine-learning-part-1/
# 
# **Python & Jupyter**
# 
# - A Crash Course in Python for Scientists: http://nbviewer.jupyter.org/gist/rpmuller/5920182
# - A Gallery of interesting Jupyter Notebooks: https://github.com/jupyter/jupyter/wiki/A-gallery-of-interesting-Jupyter-Notebooks
# - Markdown Cheatsheet: https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet
# 
# **pandas**
# 
# - документация: http://pandas.pydata.org/pandas-docs/stable/
# - 10 minutes to pandas: https://pandas.pydata.org/pandas-docs/stable/10min.html
# - Pandas Tutorial: DataFrames in Python: https://www.datacamp.com/community/tutorials/pandas-tutorial-dataframe-python
# - Cheet Sheet: https://www.analyticsvidhya.com/blog/2015/07/11-steps-perform-data-analysis-pandas-python/
# - Visualization: http://pandas.pydata.org/pandas-docs/stable/visualization.html
# 
# **sklearn**
# 
# - документация и многое другое: http://scikit-learn.org/stable/
# 
# **Другие библиотеки**
# 
# - matplotlib: https://matplotlib.org/users/pyplot_tutorial.html
# - seaborn: http://seaborn.pydata.org/

# ## Лабораторная работа 1: работа с Pandas.
# 
# Pandas - это библиотека Python, предоставляющая широкие возможности для анализа данных. С ее помощью очень удобно загружать, обрабатывать и анализировать табличные данные с помощью SQL-подобных запросов.

# In[1]:


import pandas as pd


# Основными структурами данных в Pandas являются классы Series и DataFrame. Первый из них представляет собой одномерный индексированный массив данных некоторого фиксированного типа. Второй - это двумерная структура данных, представляющая собой таблицу, каждый столбец которой содержит данные одного типа. Можно представлять её как словарь объектов типа Series.

# С помощью библиотеки Pandas займемся анализом данных. Будем работать с данными о клиентах банка, который интересуется, произойдет ли просрочка платежа на 90 и более дней при выдаче кредита. 

# ### 1
# Прочтите данные из файла data.csv
# 
# *Функции, которые могут пригодиться при решении: `pd.read_csv(..., delimiter=',')`*

# In[2]:


# место для кода
data = pd.read_csv('data.csv', delimiter=',')


# ### 2
# Выведите описание прочтенных данных. 
# 
# *Функции, которые могут пригодиться при решении: `.describe()`*

# In[3]:


data.describe()


# ### 3
# Отобразите несколько первых и несколько последних записей.
# 
# *Функции, которые могут пригодиться при решении: `.head(), .tail()`*
# 
# *Какие параметры можно передать этим функциям?*

# In[4]:


# место для кода, можно передать кол-во строк для отображения
data.head(3)


# In[5]:


data.tail(3)


# ### 4
# Прочтите в файле `DataDictionary-ru.txt`, что означают столбцы матрицы. Какому типу принадлежит каждый столбец (вещественный, целый, категориальный)?

# In[ ]:


# ### 5
# 
# Заметьте, что столбец `DebtRatio` содержит неправдоподобные данные. Только значения, соответствующие известному месячному доходу, являются отношениями. Остальные – абсолютные значения месячных выплат процентов. 
# 
# Исправьте данные, сделав все значения столбца `DebtRatio` абсолютными (умножьте их на `MonthlyIncome`).  Чтобы ваша программа быстро работала на полных данных, постарайтесь не использовать цикл.

# #### *Функции, которые могут пригодиться при решении:*
# 
# Обращение к элементам DataFrame:
#   * элемент: `data.loc[i, 'названиеСтолбца']`
#   * столбец: `data['названиеСтолбца']`
#   * подматрица: `data.loc[a:b, списокНазванийСтолбцов]`
# 
# Условная индексация:
# * `data.loc[data['столбец'] > 20, списокНазванийСтолбцов]`
# 
# лучше писать так:
# 
# * `i = data['столбец'] > 20`  # вектор `True` и `False`
# * `data.loc[i, 'названиеСтолбца']`
# 
# У подматриц номера строк наследуются от исходной.
# 
# * `pandas.isnull(скаляр или массив)` - проверка, является ли значение неопределенным (`NaN`)
# * `pandas.notnull(скаляр или массив)` - проверка, является ли значение определенным (не `NaN`)

# In[6]:


idxs = pd.notnull(data['DebtRatio'])
data.loc[idxs, 'DebtRatio'] = data.loc[idxs,'DebtRatio'] * data.loc[idxs, 'MonthlyIncome']


# ### 6
# 
# Поменяйте имя столбца на `Debt`.
# 
# *Функции, которые могут пригодиться при решении: `.rename(columns={'староеИмя':'новоеИмя'}, inplace=True)`*

# In[7]:


# место для кода
data.rename(columns={'DebtRatio':'Debt'}, inplace=True)


# ### 7
# 
# Вычислите средний ежемесячный доход и присвойте всем клиентам с неизвестным доходом полученное число.
# 
# *Функции, которые могут пригодиться при решении: `.mean()`*
# 
# *Другие описательные статистики:* https://pandas.pydata.org/pandas-docs/stable/reference/frame.html#computations-descriptive-stats

# In[8]:


# место для кода
mean_val = data['MonthlyIncome'].mean()
data['MonthlyIncome'] = data['MonthlyIncome'].fillna(mean_val)


# ### 8
# 
# Используя метод `groupby`, оцените вероятности невозврата кредита (`SeriousDlqin2yrs=1`) для различных значений количества иждивенцев (`NumberOfDependents`).  
# 
# Проделайте аналогичную процедуру для различных значений столбца `NumberRealEstateLoansOrLines`
# 
# *Подсказка:*
# `data['столбец1'].groupby(data['столбец2']).mean()`  *-- расчет средних значений столбца1 по группам из столбца2*

# In[9]:


# место для кода
data['SeriousDlqin2yrs'].groupby(data['NumberOfDependents']).mean() 


# In[10]:


data['SeriousDlqin2yrs'].groupby(data['NumberRealEstateLoansOrLines']).mean()


# ## Визуализация данных

# In[11]:


import matplotlib.pyplot as plt
#  функция, позволяющая выводить графики прямо в ноутбук
get_ipython().run_line_magic('matplotlib', 'inline')


# Matplotlib позволяет удобно визуализировать табличные данные.
# 
# *Функции, которые могут пригодиться при решении:*
# 
# * Рисование:
#    * `plt.plot(x, y)`  см. подробнее http://matplotlib.org/api/pyplot_api.html#matplotlib.pyplot.plot
#    * `plt.show()`
#    * `plt.scatter(x, y)` - график рассеяния, см. http://matplotlib.org/api/pyplot_api.html#matplotlib.pyplot.scatter
#    * `plt.hist()` - гистограмма, см. http://matplotlib.org/api/pyplot_api.html#matplotlib.pyplot.hist
# * Рисование нескольких графиков на одном:
# 
#   `fig, ax = plt.subplots()
#    ax.hist(...)
#    ax.hist(...)
#    plt.show()`
#    
# * Логарифмическая шкала:
#     * `ax.set_xscale('log')`  или `ax.set_yscale('log')`
# * Ограничение области графика:
#     * `ax.axis([x1, x2, y1, y2])`
# 
# 
# ### 9a
# 
# Постройте график рассеяния на осях `age` и `Debt`. Cиним отметьте клиентов без серьезных задолженностей (`SeriousDlqin2yrs = 0`) и красным — должников (`SeriousDlqin2yrs = 1`).

# In[12]:


_, ax = plt.subplots()
ax.scatter(data.loc[data['SeriousDlqin2yrs'] == 0, 'age'], data.loc[data['SeriousDlqin2yrs'] == 0,'Debt'])
ax.scatter(data.loc[data['SeriousDlqin2yrs'] == 1, 'age'], data.loc[data['SeriousDlqin2yrs'] == 1,'Debt'], color='red')
ax.set_xlabel("AGE")
ax.set_ylabel("DEBT")
plt.show()
get_ipython().run_line_magic('matplotlib', 'inline')


# ### 9b
# Постройте на одном графике две **нормированные** плотности распределения: красную – для месячного дохода клиентов с задолженностями, синюю – для месячного дохода клиентов без задолженностей. По оси абсцисс отобразите значения до 25000.

# In[13]:


y1 = data[(data['MonthlyIncome'] <= 25000)]
y2 = data[(data['MonthlyIncome'] <= 25000)]


# In[14]:


y1 = y1[y1['SeriousDlqin2yrs'] == 0]['MonthlyIncome']
y2 = y2[y2['SeriousDlqin2yrs'] == 1]['MonthlyIncome']


# In[18]:


# место для кода
import seaborn as sns
# snsplot = sns.kdeplot(data['sepal width (cm)'], shade=True)
# fig = snsplot.get_figure()
_, ax = plt.subplots()
ax.hist(y1, density=True, label='Задолжники')
ax.hist(y2, density=True, color='r', label='Выплачивающие')
ax.legend()
plt.show()


# ### 9c*
# Визуализируйте попарные зависимости между небинарными признаками `'age', 'MonthlyIncome', 'NumberOfDependents'`. Ограничьте при этом месячный доход значением 25000.
# 
# Какие закономерности вы можете наблюдать на получившихся графиках?
# 
# *Функции, которые могут пригодиться при решении: `pd.plotting.scatter_matrix()`*

# In[19]:


# место для кода
n_data = data[(data['MonthlyIncome'] <= 25000)]


# In[30]:


sns.pairplot(n_data.loc[:, ['age', 'MonthlyIncome', 'NumberOfDependents']], size=5)


# In[ ]:

