import os
import tempfile
import platform
import subprocess
import numpy as np

'''
info_matriz(): Returns useful info from matrix stored in a .csv
'''
def info_matriz(csv_path):
    data_array = np.genfromtxt(csv_path, delimiter=',')
    num_elements = data_array.shape[0]
    return (num_elements, data_array.min(), data_array.max())

'''
detect_filetype(): Detects if given path is one or multiple filetypes (Example: csv's)" -> Returns number of filetypes inside a folder
parameters:
    - folder_path: path of file, or path of folder containing one or multiple files.
    - filetype: string of file extension, supported are .csv
'''
def detect_filetype(folder_path, filetype):
    if os.path.isfile(folder_path) and folder_path.lower().endswith(filetype):
        return 1

    elif os.path.isdir(folder_path):
        files = os.listdir(folder_path)
        number_of_filetypes = sum(1 for file in files if file.lower().endswith(filetype))
        return number_of_filetypes

    else:
        return 0

'''
detect_input_type(): Detects if input is a folder, file (.csv), or a np.array -> Returns type
parameters:
    - input: Path of a folder containing .csv, or a 1D np.array
'''
def detect_input_type(input):
    if os.path.isdir(input):
        if detect_filetype(input, '.csv') > 0:
            return 'dir_csv'
        else:
            return 'not valid'
    if os.path.isfile(input):
        if input.lower().endswith('.csv'):
            return 'csv'
        else:
            return 'Unknown File Type'
    elif type(input) == np.ndarray:
        return 'np.array'
    else:
        return 'Not a valid file path'

'''
temp_dir(): Creates a temporary directory with a .csv of the input you want to process, then deletes it.
parameters:
    - array: input, one dimensional np.array
'''
def temp_dir(array):
    temp_dir = tempfile.mkdtemp()
    csv_path = os.path.join(temp_dir, 'temp_file.csv')
    np.savetxt(csv_path, array, fmt='%.18e', delimiter=',')
    return (temp_dir, csv_path)

'''
compile(): Function to compile C code, not sure if it generalizes well, should work on Ubuntu and Macos. Windows not implemented.
'''
def compile():
    current_platform = platform.system()

    if current_platform == 'Darwin':  # MacOS
        compile_command = ['clang', '-Xclang', '-fopenmp', '-I/usr/local/opt/libomp/include',
                           '-L/opt/homebrew/Cellar/libomp/16.0.6/lib', '-lomp', '-Icore_c/headers',
                           'core_c/scripts/mse_1d.c', 'core_c/scripts/read_csv.c', 'core_c/scripts/signal_std.c',
                           'core_c/scripts/utils.c', '-o', 'core_c/executables/mse_1d_p']
    elif current_platform == 'Linux':  # Ubuntu
        compile_command = ['gcc', '-o', 'core_c/executables/mse_1d', 'core_c/scripts/mse_1d.c',
                           'core_c/scripts/read_csv.c', 'core_c/scripts/signal_std.c', 'core_c/scripts/utils.c',
                           '-lm', '-Icore_c/headers']
    else:
        raise OSError(f"Unsupported operating system: {current_platform}")

    subprocess.run(compile_command)
