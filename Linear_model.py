import pandas as pd
import numpy as np
import io
import warnings
warnings.filterwarnings(action='ignore')
from matplotlib import pyplot as plt
from sklearn import linear_model
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import robust_scale
from IPython.display import display
import statsmodels.formula.api as sm
from statsmodels.sandbox.regression.predstd import wls_prediction_std

df = pd.read_csv("KCair.csv", encoding='utf-8')
df.head()
display(df.describe())

#Separate training and testing datasets
dfX = df[["O3", "NO2", "SO2", "china", "china1", "china2", "Wind velocity(m/s)", "Wind direction_NW", "Wind direction_S", "Wind direction_SE"]]
dfy = df["PM10"]

#split training and testing sets
dfX_train, dfX_test, dfy_train, dfy_test = train_test_split(dfX, dfy, test_size=0.3, random_state=0)
dfX_train.shape, dfX_test.shape, dfy_train.shape, dfy_test.shape

#scale
dfX_train = robust_scale(dfX_train)
dfX_test = robust_scale(dfX_test)
dfy_train = robust_scale(dfy_train)
dfy_test = robust_scale(dfy_test)
#print LinearRegression equation E
model = linear_model.LinearRegression().fit(dfX_train, dfy_train)
print("\n<Linear regression equation E - Training Data Set>")
j=0
for i in dfX.columns:
    print(i,": E = a(", "%0.5f"%float(model.coef_[j]), ")+","%0.5f"%float(model.intercept_))
    j = j+1

y_predict = model.predict(dfX_test)
#RSS calculation
print("\nRSS:", mean_squared_error(dfy_test, y_predict))
print("\nscore:", model.score(dfX_test, dfy_test))

#Visualization
line = np.linspace(min(dfy_test), max(dfy_test), 1000)
plt.plot(line, line, "r.-", label="Linear", color = "r")
plt.scatter(dfy_test, y_predict, color = "b")
plt.xlabel("predict value")
plt.ylabel("test value")
plt.show()

#Using OLS (non-scaled)
ols_model = sm.OLS(dfy, dfX)
result = ols_model.fit()

#summary
print(result.summary())
print('\nParameters : ', result.params)
#R squared
print('\nRsquaured : ', result.rsquared)
#P-value
print('\nP-value :', result.pvalues)