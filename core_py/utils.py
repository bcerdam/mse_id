import matplotlib.pyplot as plt
import os
import numpy as np
import json

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

# # Parametros relacionados a Arreglo de Electrodos.
# folder_path = '/Users/brunocerdamardini/Desktop/repo/c_mse_3D/Datos/UV/UV_means/UV_means_json'
# indices_orden = indices_arreglos_electrodos()
# methods posibles: ('sin_fw', 'sqr_fw', 'sin_bw', 'sqr_bw') x ('lo', 'md', 'hi')
# mse_3d_matrix = create_2d_matrix_from_json(folder_path, indices_orden, ('sin_fw', 'hi'), 10)
#
# methods_1 = ['sin_fw', 'sqr_fw', 'sin_bw', 'sqr_bw']
# methods_2 = ['lo', 'md', 'hi']
# for method_1 in methods_1:
#     for method_2 in methods_2:
#         mse_3d_matrix = create_2d_matrix_from_json(folder_path, indices_orden, (method_1, method_2), 1)
#         # row_means = np.mean(mse_3d_matrix, axis=1)
#         # result_column = row_means.reshape(-1, 1)
#         np.savetxt(f'/Users/brunocerdamardini/Desktop/repo/c_mse_3D/Datos/UV/UV_means/UV_means_processed/electrode_array_1_csv/datos/{method_1+"_"+method_2}.csv',
#                    mse_3d_matrix, delimiter=',', fmt='%.18e')






# # Example usage:
# folder_path = "/path/to/your/csv/files/"
# order = ['K6', 'I8', 'L2', ...]  # Replace this with the actual 'order' list
# result_matrix = create_2d_matrix_from_csvs(folder_path, order)
#
# if result_matrix is not None:
#     print("Resulting 2D Matrix:")
#     print(result_matrix)