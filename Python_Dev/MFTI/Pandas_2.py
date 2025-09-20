import pandas as pd
import math as m
import numpy as np

data_number = pd.DataFrame({"A": [np.nan, -100, 10.0], "B": [-5.5, 35, 1]})

data_weather = pd.DataFrame({
    "Date": ["2024-01-01", "2024-01-01", "2024-01-01", "2024-01-02", "2024-01-02", "2024-01-02"],
    "City": ["Москва", "Владивосток", "Казань", "Москва", "Владивосток", "Казань"],
    "Temperature": [32, 15, 25, 33, 18, 26],
})

data_class = pd.DataFrame(
    {"Имя": ["Анна", "Иван", "Петр", "Елена", "Ольга"],
     "Фамилия": ["Иванова", "Петров", "Сидоров", "Михайлова", "Попова"],
     "Группа": ["А", "Б", "А", "А", "Б"],
     "Оценка": [75, 65, 90, 70, 85]})


#print(data_weather)
print("\n")
# используем метод pivot для изменения формы данных
pivot_df3 = data_weather.pivot(index="Date", columns="City", values="Temperature")


g = 9.81
def calculate_trajectory(initial_velocity: float, angle: float)-> tuple:
    #L = (v² * sin(2a)) / g
    float1 = int(((initial_velocity ** 2 * (m.sin(m.radians(angle)) * 2) / g) * 100)) / 100
    #H = (v² * sin²(a)) / (2g)
    float2 = int(((initial_velocity ** 2 * m.sin(m.radians(angle)) ** 2) / (g * 2) * 100)) / 100
    return [float1, float2]


def no_negative(pd_data: pd.DataFrame):

    df_copy = pd_data.copy()
    
    df_copy = df_copy.where(df_copy > 0, 0)

    return df_copy


def count_nan(dataframe: pd.DataFrame) -> pd.Series:

    nan_count = (dataframe.isnull()).sum()
    
    return nan_count

count_nan(data_number)


def best_of(data: pd.DataFrame, letter: str = "А")-> list:
    filtered_df = data[(data['Группа'] == letter) & (data['Оценка'] >= 75)]
    return list(pd.Series(filtered_df["Фамилия"]))

best_of(data_class)