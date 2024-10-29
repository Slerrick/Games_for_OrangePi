import matplotlib.pyplot as plt

# Данные
years = [2000, 2005, 2010, 2015, 2020]
gdp_values = [15500, 26400, 37700, 66700, 103600]  # ВВП в миллиардах рублей

# Построение графика
plt.figure(figsize=(10, 5))
plt.plot(years, gdp_values, marker='o')

# Настройка осей
plt.title('Динамика роста ВВП России (2000-2020)', fontsize=16)
plt.xlabel('Год', fontsize=14)
plt.ylabel('ВВП (в миллиардах рублей)', fontsize=14)
plt.xticks(years)
plt.grid(True)

# Отображение графика
plt.show()
