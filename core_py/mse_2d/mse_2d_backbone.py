import csv
import os
import tempfile
import subprocess
from PIL import Image
import numpy as np

def calculate_std(csv_path):
    unique_values = set()

    with open(csv_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            for val in row:
                unique_values.add(float(val))

    std = np.std(list(unique_values))

    return std

def image_to_array(image_path, size):
    img = Image.open(image_path).resize(size).convert('L')
    arr = np.array(img)
    return arr

'''
detect_input_type(): Detects if input is a folder, file (.csv or .mp4), or a np.array -> Returns type
parameters:
    - input: Path of a folder containing .mp4 or .csv, or a 3D np.array
'''
def detect_input_type(input):
    if os.path.isdir(input):
        if detect_filetype(input, '.png') > 0:
            return 'dir_png'
        elif detect_filetype(input, '.jpeg') > 0 or detect_filetype(input, '.jpg') > 0:
            return 'dir_jpeg'
        else:
            return 'not valid'
    if os.path.isfile(input):
        if input.lower().endswith('.png'):
            return 'png'
        elif input.lower().endswith('.jpeg') or input.lower().endswith('.jpg'):
            return 'jpeg'
        else:
            return 'Unknown File Type'
    elif type(input) == np.ndarray:
        return 'np.array'
    else:
        return 'Not a valid file path'

'''
detect_filetype(): Detects if given path is one or multiple filetypes (Example: csv's or mp4's)" -> Returns number of filetypes inside a folder
parameters:
    - folder_path: path of file, or path of folder containing one or multiple files.
    - filetype: string of file extension, supported are .csv and .mp4
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
temp_dir(): Creates a temporary directory with a .csv of the input you want to process, then deletes it.
parameters:
    - array: input, two dimensional np.array
'''
def temp_dir(array):
    temp_dir = tempfile.mkdtemp()
    csv_path = os.path.join(temp_dir, 'temp_file.csv')
    np.savetxt(csv_path, array, fmt="%d", delimiter=',')
    return (temp_dir, csv_path)

'''
compile(): Function to compile C code, not sure if it generalizes well, should work Macos. Windows & Ubuntu not implemented.
'''
def compile():
    compile_command = ['clang', '-Xclang', '-fopenmp', '-I/usr/local/opt/libomp/include',
                       '-L/opt/homebrew/Cellar/libomp/16.0.6/lib', '-lomp', '-Icore_c/headers',
                       'core_c/scripts/mse_2d.c', 'core_c/scripts/read_csv.c', 'core_c/scripts/utils.c',
                       '-o', 'core_c/executables/mse_2d_p']

    subprocess.run(compile_command)
