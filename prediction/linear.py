import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

dataset = pd.read_csv('D:\Dev\social-analytics-platform\prediction\dataset_mc.csv')
x = dataset.iloc[:,1:5]
y = dataset['Reactions']
x_train, x_test, y_train, y_test = train_test_split(x,y)

lin = LinearRegression()
lin.fit(x_train, y_train)
y_pred = lin.predict(x_test)

coef = lin.coef_
components = pd.DataFrame(zip(x.columns, coef), columns=['component', 'value'])
components = components.append({'component': 'intercept', 'value': lin.intercept_}, ignore_index=True)
print(components)

