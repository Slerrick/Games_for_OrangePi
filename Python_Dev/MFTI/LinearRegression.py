import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression

plt.style.use("default")

random_generator = np.random.default_rng()
X = 2 * random_generator.random((100, 1))  # случайные значения от 0 до 2
y = 4 + 3 * X + random_generator.random((100, 1))  # зависимость y = 4 + 3x + шум


###########################

lin_reg = LinearRegression()
lin_reg.fit(X, y)  # метод "учит" модель на наших данных

# прямую линию можно и по двум точкам построить, так что достаточно взять x=0 и x=2
X_new = np.array([[0], [2]])
y_predict = lin_reg.predict(X_new)  # метод обученной моделью делает предсказание

plt.figure(figsize=(8, 5))
plt.scatter(X, y, color="blue", alpha=0.6, label="Данные")
plt.plot(X_new, y_predict, "r-", linewidth=2, label="Линейная регрессия")
plt.xlabel("X")
plt.ylabel("y")
plt.title("Линейная регрессия")
plt.legend()
plt.show()
print(lin_reg.coef_, lin_reg.intercept_)