import gc
import os
import time
import numpy as np
import pandas as pd

from Files_operating import read_dataFile, save_results_toFiles
from source.Signal_preprocessing import fft_butter_skewness_filtering, data_converting_CNN
from source.View_app import main

path_to_proj = ""
path_to_csv = "data/"
path_file = "data/41649_fragment.csv"

file_path = "data/41649_fragment.csv"
FILE_D_ID = "41649"
# log
print(f"\n#log: Выбран файл 41649_fragment (FILE_ID: {FILE_D_ID})")

fragments_csv_name = file_path[:-4] + "_fragments.csv"

start = time.time()
data = pd.read_csv(path_file)

# DataFrame for plotting
df = data.copy()  # .drop("ch12", axis=1)
# log
print(f"#log: Файл 41649_fragment считан успешно. Tooks - {round(time.time() - start, 2) * 1} s.")
gc.collect()

SIGNAL_RATE = 10.0  # float(input("\nВведите частоту дискретизации для данного сигнала (4 / 10): "))  # 4
signal_maxLength = 512

# Предложение пользователю выбрать канал
available_channels = [col for col in data.columns if col != "t" and str(data[col][0]) != 'nan']
selected_channel = "ch11"  # input("\nДоступные каналы: " + ', '.join(available_channels) + "\nВыберите канал: ")

# Проверка наличия выбранного канала в данных
if selected_channel in available_channels:
    selected_data = data[["t", selected_channel]].astype({"t": "float64"})
else:
    print("Выбранный канал не найден в данных.")
    selected_channel = input("Доступные каналы: " + '\n'.join(available_channels) + "\n----------\nВыберите канал: ")

signal_meta = {"id": FILE_D_ID, "ch": selected_channel, "rate": SIGNAL_RATE}

# Выбираем область графика
start = -np.inf
end = np.inf

x = np.array(data.t[(data.t > start) * (data.t < end)])
y = np.array(data[selected_channel][(data.t > start) * (data.t < end)])
# log
print("\n#log: Канал считан успешно")

# log
print("\n#log: Начата предварительная обработка данных.")
start = time.time()
fragments = fft_butter_skewness_filtering(x, y, log_df=df)
# log
print(f"#log: Предварительная обработка и фильтрация выполнена успешно. Tooks - {round(time.time() - start, 2) * 1} s.")
print("==========================================")
print(f"#log: Количество найденных фрагментов: {len(fragments[0])}")
print("==========================================")

# Run viewing app
main(df=df, left_p=55170, right_p=55330)  # 58460 58660
