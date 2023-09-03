import subprocess
import numpy as np
import os
import time
import utils
import misc

def info_matriz(csv_path):
    data_array = np.genfromtxt(csv_path, delimiter=',')
    num_matrices = data_array.shape[0]
    rows = np.sqrt(data_array.shape[1])
    cols = np.sqrt(data_array.shape[1])
    return (num_matrices, rows, cols)

def run_c_program(csv_path, scales, m, r, fuzzy, method, delta=0.7, distance_type=0, m_distance=2, sampleo=1, std_type=1, mod=False):
    info = info_matriz(csv_path)
    command = [os.path.join(os.path.dirname(os.getcwd()), 'c_mse_3D/core_c', 'executables', 'mse_3d_p'), csv_path, str(scales), str(m), str(r), str(fuzzy), str(method),
               str(delta), str(distance_type), str(m_distance), str(sampleo), str(info[0]), str(info[1]), str(info[2]), str(std_type), str(mod)]
    result = subprocess.run(command, stdout=subprocess.PIPE).stdout.decode('utf-8').strip()
    n_values = list(result.split())
    n_values = [float(x) for x in n_values]
    return n_values

def mse_3d(folder_path, scales, m, r, fuzzy, method, delta=0.7, distance_type=0, m_distance=2, sampleo=1, std_type='UNIQUE_VALUES', mod=False):
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

    if mod == False:
        mod = 0
    elif mod == True:
        mod = 1
        valores_permitidos = [x for x in range(2, 16, 2)]
        if m not in valores_permitidos:
            return print('Si parametro mod=True, entonces parametro "m" debe ser igual a 2, 4, 6 o 8.')

    mse_values = []
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        print('Working on: ', filename)
        start_time = time.time()

        mse_values.append([filename, run_c_program(file_path, scales, m, r, fuzzy, method, delta, distance_type, m_distance, sampleo, std_type, mod)])


        end_time = time.time()
        execution_time = end_time - start_time
        print(execution_time)

    return mse_values

# Compilar con: gcc -o core_c/executables/mse_3d core_c/scripts/mse_3d.c core_c/scripts/read_csv.c core_c/scripts/signal_std.c core_c/scripts/utils.c -lm -fopenmp -Icore_c/headers

# clang -Xclang -fopenmp -I/usr/local/opt/libomp/include -L/opt/homebrew/Cellar/libomp/16.0.6/lib -lomp -Icore_c/headers core_c/scripts/mse_3d.c core_c/scripts/read_csv.c core_c/scripts/signal_std.c core_c/scripts/utils.c -o core_c/executables/mse_3d_p

# Ultimos tres valores: [0.53259, 0.53985, 0.551946]
# Valores 10, 11, 12: [0.478086, 0.480089, 0.47814]