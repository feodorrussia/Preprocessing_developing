import gc
import os
import time
import numpy as np

from Files_operating import read_dataFile, save_results_toFiles
from source.Signal_preprocessing import fft_butter_skewness_filtering, data_converting_CNN

path_to_proj = input("Введите путь к запускаемому файлу (Plasma_processing/): ")
path_to_csv = input("Введите путь к файлам с данными относительно запускаемого файла (data_csv/): ")

if not os.path.exists(path_to_csv):
    os.mkdir(path_to_csv)

file_name = input("Введите имя файла. Доступные файлы:\n" + "\n".join(
    list(filter(lambda x: '.dat' in x or '.txt' in x, os.listdir(path_to_csv)))) + "\n----------\n")

file_path = path_to_csv + file_name
FILE_D_ID = file_name[:5]  # "00000"
# log
print(f"\n#log: Выбран файл {file_name} (FILE_ID: {FILE_D_ID})")

fragments_csv_name = file_path[:-4] + "_fragments.csv"

start = time.time()
data = read_dataFile(file_path, path_to_proj)
# log
print(f"#log: Файл {file_name} считан успешно. Tooks - {round(time.time() - start, 2) * 1} s.")
gc.collect()

SIGNAL_RATE = float(input("\nВведите частоту дискретизации для данного сигнала (4 / 10): "))  # 4
signal_maxLength = 512

# Предложение пользователю выбрать канал
available_channels = [col for col in data.columns if col != "t" and str(data[col][0]) != 'nan']
selected_channel = input("\nДоступные каналы: " + ', '.join(available_channels) + "\nВыберите канал: ")

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
fragments = fft_butter_skewness_filtering(x, y)
# log
print(f"#log: Предварительная обработка и фильтрация выполнена успешно. Tooks - {round(time.time() - start, 2) * 1} s.")
print("==========================================")
print(f"#log: Количество найденных фрагментов: {len(fragments[0])}")
print("==========================================")


