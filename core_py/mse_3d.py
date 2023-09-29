import subprocess
import numpy as np
import os
import time
# import utils
# import misc

def info_matriz(csv_path):
    data_array = np.genfromtxt(csv_path, delimiter=',')
    num_matrices = data_array.shape[0]
    rows = np.sqrt(data_array.shape[1])
    cols = np.sqrt(data_array.shape[1])
    return (num_matrices, rows, cols)

def run_c_program(csv_path, scales, m, r, fuzzy, method, delta=0.7, distance_type=0, m_distance=2, sampleo=1, std_type=1, mod=False, m_espacial=1, dim_cubo=1):
    info = info_matriz(csv_path)
    command = [os.path.join(os.path.dirname(os.getcwd()), 'c_mse_3D/core_c', 'executables', 'mse_3d_p'), csv_path, str(scales), str(m), str(r), str(fuzzy), str(method),
               str(delta), str(distance_type), str(m_distance), str(sampleo), str(info[0]), str(info[1]), str(info[2]), str(std_type), str(mod), str(m_espacial), str(dim_cubo)]
    result = subprocess.run(command, stdout=subprocess.PIPE).stdout.decode('utf-8').strip()
    n_values = list(result.split())
    n_values = [float(x) for x in n_values]
    return n_values

def mse_3d(folder_path, scales, m, r, fuzzy, method, delta=0.9, distance_type=0, m_distance=2, sampleo=1, std_type='UNIQUE_VALUES', mod=False, m_espacial=1, dim_cubo=1):
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

        if dim_cubo not in [1, 3, 5] or dim_cubo > (m+1):
            return print('dim_cubo debe ser menor que parametro "m", y debe ser impar: (1, 3, 5, etc.)')

    mse_values = []
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        print('Working on: ', filename)
        start_time = time.time()

        mse_values.append([filename, run_c_program(file_path, scales, m, r, fuzzy, method, delta, distance_type, m_distance, sampleo, std_type, mod, m_espacial, dim_cubo)])


        end_time = time.time()
        execution_time = end_time - start_time
        print(execution_time)

    return mse_values

# Compilar con: gcc -o core_c/executables/mse_3d core_c/scripts/mse_3d.c core_c/scripts/read_csv.c core_c/scripts/signal_std.c core_c/scripts/utils.c -lm -fopenmp -Icore_c/headers

# clang -Xclang -fopenmp -I/usr/local/opt/libomp/include -L/opt/homebrew/Cellar/libomp/16.0.6/lib -lomp -Icore_c/headers core_c/scripts/mse_3d.c core_c/scripts/read_csv.c core_c/scripts/signal_std.c core_c/scripts/utils.c -o core_c/executables/mse_3d_p

# v = mse_3d('/Users/brunocerdamardini/Desktop/repo/c_mse_3D/Datos/test/staged', 20, 2, 0.2, True, 'MSE', mod=True, m_espacial=1, dim_cubo=1)

# 1: 12.12s
# 2: 6.32s
# 4: 3.48s
# 8: 2.75s
# 16: 2.77s
# 32: 2.71s
# 64: 2.67s
# 128: 2.70s