import subprocess
import matplotlib.pyplot as plt
import numpy as np
import csv
import os
import pandas as pd
import time

def plot_arrays(data_list, title='', xlabel='', ylabel='', legends=None, save_path=None):
    fig, ax = plt.subplots()
    plt.grid('black')
    ax.set_facecolor('lightgrey')
    for i, data_tuple in enumerate(data_list):
        name, data = data_tuple
        if legends is not None and len(legends) == len(data_list):
            label = legends[i]
        else:
            label = name
        plt.plot(data, color=f'C{i}', marker='v', markersize=5, label=label, markeredgecolor='black')
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    if save_path is not None:
        plt.savefig(save_path)
    plt.show()

def calculate_csv_std(folder_path):
    unique_values = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):
            file_path = os.path.join(folder_path, filename)
            df = pd.read_csv(file_path, header=None)
            unique_values.extend(np.unique(df.values.astype(float)))
    unique_values = np.array(unique_values).astype(float)
    return np.std(unique_values)



def run_c_program(csv_path, scales, m, r):
    num_files = len([f for f in os.listdir(csv_path) if f.endswith('.csv')])
    csv_file = os.path.join(csv_path, os.listdir(csv_path)[0])
    with open(csv_file, 'r') as f:
        reader = csv.reader(f)
        csv_rows = len(list(reader))
        f.seek(0)
        csv_cols = len(next(reader))

    r_std = calculate_csv_std(csv_path) * r
    command = ['./mse_3D', csv_path, str(num_files), str(scales), str(csv_rows), str(csv_cols), str(m), str(r_std)]
    result = subprocess.run(command, stdout=subprocess.PIPE)
    output = result.stdout.decode('utf-8').strip()
    n_values = list(output.split())
    n_values = [float(x) for x in n_values]
    return n_values


def mse_3D(folder_path, scales, m, r):
    mse_values = []
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        print('Working on: ', filename)
        start_time = time.time()

        mse_values.append([filename, run_c_program(file_path, scales, m, r)])

        end_time = time.time()
        execution_time = end_time - start_time
        print(execution_time)

    return mse_values


# Ejemplo:

# 'Datos/10x10x100/datos_csv' => Hay que pasarle el path de la carpeta en donde estan los .csv de los datos originales (Hay que crear los .csv para cada imagen)
# (Es cosa de pedirle a chat gpt que haga una funcion que haga esto)

# 20 => escalas
# 1 => m
# 0.5 => r

# Tambien imprime el tiempo en segundos que se demora.

# En el ejemplo de abajo son 100 frames chicas de 10x10, por eso hay que ponerle m=1 y r=0.5.

# IMPORTANTE: Hay que cambiar el path de datos_csv al de tu computador y compilar de nuevo
# Compilar con este comando en la terminal del repo: gcc mse_3D.c -o mse_3D -lm

# v = mse_3D('Datos/10x10x100/datos_csv', 20, 1, 0.5)
# plot_arrays(v)