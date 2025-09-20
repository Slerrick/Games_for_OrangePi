import pandas as pd
data = {
    "Date": ["2024-01-01", "2024-01-01", "2024-01-01", "2024-01-02", "2024-01-02", "2024-01-02"],
    "City": ["Москва", "Владивосток", "Казань", "Москва", "Владивосток", "Казань"],
    "Temperature": [32, 15, 25, 33, 18, 26],
}
df3 = pd.DataFrame(data)
def to_fahrenheit(x: float) -> float:
    return x * 9 / 5 + 32


df3["Temperature"] = df3["Temperature"].apply(to_fahrenheit)
#print(df3)

def remove_missing_values(df: pd.DataFrame, subset=None, how='any'):
    return df.dropna(how=how, subset=subset)
#print(remove_missing_values(df3))

data2 = pd.DataFrame({
    "Название": [
        "Ручка гелевая",
        "Карандаш чернографитный",
        "Линейка пластиковая",
        "Блокнот на спирали",
        "Фломастеры цветные",
        "Тетрадь в клетку",
        "Клейкая лента",
        "Степлер офисный",
        "Конверты бумажные",
        "Маркер перманентный",
    ],
    "Цена": [116, 283, 249, 161, 299, 183, 105, 130, 275, 256],
    "Количество": [21, 34, 29, 23, 27, 34, 26, 33, 27, 34],
})

def top_sales(data: pd.DataFrame, target: int) -> list:
    maxi = data["Количество"].max()
    filtered_data = data[(data["Количество"] == maxi) & (data["Цена"] > target)]
    result = filtered_data["Название"].to_list()
    
    return result
#print(top_sales(data2, 250))
def count_rows_cols(name: pd.DataFrame):
    num_columns = len(name.columns)
    num_rows = len(name) + 1
    return (tuple([num_columns,num_rows]))
print(count_rows_cols(data2))

def baseline_median(data:pd.DataFrame):
    median = data["feature"].std()
    
    data["predict"] = median
    return data