
import pandas as pd

data=pd.read_csv('data.csv', delimiter=',')
data.describe()


get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plt



plt.scatter(data['VehOdo'], data['MMRCurrentRetailAveragePrice'], c=data['IsBadBuy'], cmap='RdYlGn')


from sklearn import * 
model1 = linear_model.LinearRegression()
i = pd.notnull(data['MMRCurrentRetailAveragePrice'])
x = data.loc[i, ['VehOdo','MMRCurrentRetailAveragePrice']]
y = data.loc[i, 'IsBadBuy']
model1.fit(x, y)
model1.coef_

prediction = model1.predict(x)
print(prediction)


predictionClass = [1 if prediction[i] > 0.5 else 0 for i in range(prediction.shape[0])]
predictionClass

print(metrics.classification_report(y, predictionClass))

print(metrics.confusion_matrix(y, predictionClass))


model2 = tree.DecisionTreeClassifier(max_depth=20)
i = pd.notnull(data['MMRCurrentRetailAveragePrice'])
x = data.loc[i, ['VehOdo','MMRCurrentRetailAveragePrice']]
y = data.loc[i, 'IsBadBuy']
model2.fit(x, y)


prediction2 = model2.predict_proba(x)
prediction2



prediction2Class = [1 if prediction2[i,1] > 0.3 else 0 for i in range(prediction2.shape[0]) ]
print(metrics.classification_report(y, prediction2Class))
print(metrics.confusion_matrix(y, prediction2Class))


dataTrain = data.loc[0:34999,]
dataTest = data.loc[35000:69999,]



for depth in range(1, 20, 2):
    print('Depth: ', depth, end = '\t')
    model3 = tree.DecisionTreeClassifier(max_depth=depth)
    i = pd.notnull(dataTrain['MMRCurrentRetailAveragePrice'])
    x = dataTrain.loc[i, ['VehOdo','MMRCurrentRetailAveragePrice']]
    y = dataTrain.loc[i, 'IsBadBuy']
    model3.fit(x, y)
    prediction3 = model3.predict_proba(x)
    prediction3Class = [1 if prediction3[i,1] > 0.5 else 0 for i in range(prediction3.shape[0]) ]

    print('dataTrain: ', metrics.accuracy_score(y, prediction3Class), end = '\t\t')

    i2 = pd.notnull(dataTest['MMRCurrentRetailAveragePrice'])
    x2 = dataTest.loc[i2, ['VehOdo','MMRCurrentRetailAveragePrice']]
    y2 = dataTest.loc[i2, 'IsBadBuy']
    prediction3_2 = model3.predict_proba(x2)
    prediction3_2Class = [1 if prediction3_2[i,1] > 0.5 else 0 for i in range(prediction3_2.shape[0]) ]

    print('dataTest: ', metrics.accuracy_score(y2, prediction3_2Class))



model4 = tree.DecisionTreeClassifier(max_depth=20)
i = pd.notnull(data['MMRCurrentRetailAveragePrice'])
x = data.loc[i, ['VehOdo', 'MMRCurrentRetailAveragePrice']]
y = data.loc[i, 'IsBadBuy']
model4.fit(x, y)
prediction4 = model4.predict_proba(x)

predictionClass4 = [1 if prediction4[i,1] > 0.5 else 0 for i in range(prediction4.shape[0])]
conf_mx = metrics.confusion_matrix(y, predictionClass4)
#conf_matrix
avg_coef = (conf_mx[0,1]*100 + conf_mx[1,0]*1000)/x.shape[0]
avg_coef

optimal = 0.0
k = 0.01
min_val = 10000.0

while (k <= 1):
    predictionClass4 = [1 if prediction4[i,1] > k else 0 for i in range(prediction4.shape[0])]
    conf_mx = metrics.confusion_matrix(y, predictionClass4)
    avg_coef = (conf_mx[0,1]*100 + conf_mx[1,0]*1000)/x.shape[0] 
    
    if (avg_coef < min_val):
        min_val = avg_coef
        optimal = k
    k += 0.01
    
print(min_val, ' ', optimal)



