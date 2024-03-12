import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn import metrics
from sklearn.model_selection import cross_val_score
import statsmodels.api as sm

def crearmodelo(df,features,resp):
    features=features
    x = df[features]
    x = x.reset_index(drop=True)
    y = df[resp]
    y = y.reset_index(drop=True)
    X_train, X_test, y_train, y_test = train_test_split(x, y, random_state=1, test_size=0.2)
    linreg = LinearRegression()
    linreg.fit(X_train, y_train)
    coef = linreg.intercept_
    y_pred = linreg.predict(X_test)
    plt.scatter(y_test, y_pred, color='blue')
    plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], linestyle='--', color='red')  # Línea de referencia y=x
    plt.xlabel('Valores reales')
    plt.ylabel('Prediccion del modelo')
    plt.title('Regresion')
    plt.savefig("regresion.png")
    plt.close()
    #Ahora metricas
    MAE = metrics.mean_absolute_error(y_test, y_pred)
    MSE = metrics.mean_squared_error(y_test, y_pred)
    RMSE = np.sqrt(MSE)
    loss = [MAE,MSE,RMSE]
    scores = cross_val_score(linreg, x, y, cv=5, scoring='neg_mean_squared_error')
    mse_scores = - scores
    rmse_scores = np.sqrt(mse_scores)
    #Ahora calculamos anova
    X_train = sm.add_constant(X_train)
    model = sm.OLS(y_train, X_train).fit()
    anova = model.summary()
    fig = sm.graphics.influence_plot(model, criterion="cooks")
    fig.savefig('influence.png')
    plt.close(fig)
    return coef,loss,anova,y_test,y_pred

    
