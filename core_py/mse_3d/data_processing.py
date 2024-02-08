import os
import json
import numpy as np

'''
Ejemplo:
v = utils.process_outs('Datos/protocolos_led/processed_data/UV/MR-0612_per_h01_h02_h05_h08_h09_nd1/rs_1000_hz_bpf_0d1_100_hz/per_nd1_100', 
100, 
['per', 'h01', 'h02', 'h05', 'h08', 'h09'])

'''
def process_outs(directory_path, num_lines, string_list):
    all_out_values = []
    try:
        file_names = sorted(os.listdir(directory_path), key=lambda x: int(x.split('.')[0]))
        for c, file_name in enumerate(file_names):
            print(file_name)
            if file_name.endswith(".out"):
                file_path = os.path.join(directory_path, file_name)
                with open(file_path, 'r') as file:
                    lines = [float(next(file).strip()) for _ in range(num_lines)]
                    # for string_val in string_list:
                    all_out_values.append([string_list[c], lines])
        return all_out_values
    except FileNotFoundError:
        print(f"Directory '{directory_path}' not found.")
        return []
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return []

def indices_arreglos_electrodos():
    indice_letras = ['B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'O', 'P']
    indice_numeros = ['14', '13', '12', '11', '10', '9', '8', '7', '6', '5', '4', '3', '2', '1']
    indices_finales = []
    for indice_numero in indice_numeros:
        for indice_letra in indice_letras:
            indices_finales.append(indice_letra + indice_numero)
    return indices_finales
def create_2d_matrix_from_json(folder_path, order, method, sample=1):
    file_list = os.listdir(folder_path)
    data_dict = {}
    for name in order:
        matching_files = [filename for filename in file_list if filename.endswith('.json') and f'Signal_{name}_mean.json' == filename]
        file_path = os.path.join(folder_path, matching_files[0])
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)[method[0]][method[1]]
            sampled_data = np.array(data[::sample])
            if name in data_dict:
                data_dict[name] = np.column_stack((data_dict[name], sampled_data))
            else:
                data_dict[name] = sampled_data
    matrix = np.column_stack(list(data_dict.values()))
    return matrix

def mod_create_2d_matrix_from_json(folder_path, order, intervalo, sample=1, save_path=None, namy=None):
    file_list = os.listdir(folder_path)
    data_dict = {}
    for name in order:
        matching_files = [filename for filename in file_list if filename.endswith('.json') and f'Signal_{name}.json' == filename]
        file_path = os.path.join(folder_path, matching_files[0])
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)[intervalo[0]:intervalo[1]]
            sampled_data = np.array(data[::sample])
            if name in data_dict:
                data_dict[name] = np.column_stack((data_dict[name], sampled_data))
            else:
                data_dict[name] = sampled_data
    matrix = np.column_stack(list(data_dict.values()))

    if save_path:
        np.savetxt(save_path+namy+'.csv', matrix, delimiter=',')  # Change delimiter as needed

    return matrix