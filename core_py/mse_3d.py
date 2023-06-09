import subprocess
import numpy as np
import os
import time
import utils

def info_matriz(csv_path):
    data_array = np.genfromtxt(csv_path, delimiter=',')
    num_matrices = data_array.shape[0]
    rows = np.sqrt(data_array.shape[1])
    cols = np.sqrt(data_array.shape[1])
    return (num_matrices, rows, cols)

def run_c_program(csv_path, scales, m, r, fuzzy, method, delta=0.7, distance_type=0, m_distance=2, sampleo=1, std_type=1):
    info = info_matriz(csv_path)
    command = [os.path.join(os.path.dirname(os.getcwd()), 'core_c', 'executables', 'mse_3d'), csv_path, str(scales), str(m), str(r), str(fuzzy), str(method),
               str(delta), str(distance_type), str(m_distance), str(sampleo), str(info[0]), str(info[1]), str(info[2]), str(std_type)]
    result = subprocess.run(command, stdout=subprocess.PIPE).stdout.decode('utf-8').strip()
    n_values = list(result.split())
    n_values = [float(x) for x in n_values]
    return n_values

def mse_3d(folder_path, scales, m, r, fuzzy, method, delta=0.7, distance_type=0, m_distance=2, sampleo=1, std_type='UNIQUE_DISTANCES'):
    # Fuzzy params
    if fuzzy == True:
        fuzzy = 1
    else:
        fuzzy = 0

    # Method params: MSE (MultiScale Entropy), CMSE (Composite MultiScale Entropy), RCMSE (Refined Composite MultiScale Entropy)
    if method in ['CMSE', 'RCMSE']:
        if method == 'CMSE':
            method = 1
        elif method == 'RCMSE':
            method = 2
    else:
        method = 0

    if std_type == 'UNIQUE_DISTANCES':
        std_type = 1
    elif std_type == 'UNIQUE_VALUES':
        std_type = 0

    mse_values = []
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        print('Working on: ', filename)
        start_time = time.time()

        mse_values.append([filename, run_c_program(file_path, scales, m, r, fuzzy, method, delta, distance_type, m_distance, sampleo, std_type)])


        end_time = time.time()
        execution_time = end_time - start_time
        print(execution_time)

    return mse_values

# Compilar con: gcc -o core_c/executables/mse_3d core_c/scripts/mse_3d.c core_c/scripts/read_csv.c core_c/scripts/signal_std.c core_c/scripts/utils.c -lm -fopenmp -Icore_c/headers

# White Noise
# v = mse_3d('/home/bcm/Desktop/Repo/c_mse_3D/Datos/10x10x100_2/white_noise', 20, 2, 0.25, True, 'RCMSE')
# utils.plot_arrays(v)

# Dots
# v = mse_3d('/home/bcm/Desktop/Repo/c_mse_3D/Datos/mse_3d_2/16x16x1000/dots', 20, 2, 0.25, True, 'RCMSE', delta=0.9)
# utils.plot_arrays(v)

# 1118469
