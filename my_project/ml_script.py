from sklearn.linear_model import LinearRegression
import joblib
import numpy as np

X = np.array([[600], [800], [1000], [1200], [1400]])  # Features (square footage)
y = np.array([150000, 180000, 210000, 240000, 270000])  # Targets (price)

model=LinearRegression()
model.fit(X,y)

joblib.dump(model,'model.pkl')
