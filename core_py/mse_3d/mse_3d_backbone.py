import os
import tempfile
import cv2
import numpy as np
import subprocess
import platform

'''
detect_input_type(): Detects if input is a folder, file (.csv or .mp4), or a np.array -> Returns type
parameters:
    - input: Path of a folder containing .mp4 or .csv, or a 3D np.array
'''
def detect_input_type(input):
    if os.path.isdir(input):
        if detect_filetype(input, '.csv') > 0:
            return 'dir_csv'
        elif detect_filetype(input, '.mp4') > 0:
            return 'dir_mp4'
        else:
            return 'not valid'
    if os.path.isfile(input):
        if input.lower().endswith('.csv'):
            return 'csv'
        elif input.lower().endswith('.mp4'):
            return 'mp4'
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
    - array: input, three dimensional np.array
'''
def temp_dir(array):
    temp_dir = tempfile.mkdtemp()
    csv_path = os.path.join(temp_dir, 'temp_file.csv')
    array = arr_3d_to_2d(array)
    np.savetxt(csv_path, array, fmt='%.18e', delimiter=',')
    return (temp_dir, csv_path)

'''
arr_3d_to_2d(): Transforms 3-dimensional array into a 2-dimensional array, where each row is a flattened
                2-dimensional array from the original 3-dimensional array. This format is necessary for the 
                C code to work.
parameters:
    - array: input, three dimensional np.array
'''
def arr_3d_to_2d(array):
    if array.ndim != 3:
        raise ValueError("Input must be a 3D array.")

    values = []
    for i in range(array.shape[2]):
        slice_2d = array[:, :, i].flatten()
        values.append(slice_2d)
    values = np.vstack(values)
    return values

'''
mp4_to_3d_arr(): Recieves .mp4 path and shape of np.array. Function will transform the .mp4 into a 3-dimensional
array of the given shape.
parameters:
    - mp4_path: self explanatory.
    - shape: shape of the array containing the video.
'''
def mp4_to_3d_arr(mp4_path, shape):
    height, width, frames = shape
    video_array = np.empty((height, width, frames), dtype=np.uint8)
    cap = cv2.VideoCapture(mp4_path)

    for i in range(frames):
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.resize(frame, (width, height))
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        video_array[:, :, i] = frame_gray
    cap.release()
    return video_array


'''
compile(): Function to compile C code, not sure if it generalizes well, should work on Ubuntu and Macos. Windows not implemented.
'''
def compile():
    current_platform = platform.system()

    if current_platform == 'Darwin':  # MacOS
        compile_command = ['clang', '-Xclang', '-fopenmp', '-I/usr/local/opt/libomp/include',
                           '-L/opt/homebrew/Cellar/libomp/16.0.6/lib', '-lomp', '-Icore_c/headers',
                           'core_c/scripts/mse_3d.c', 'core_c/scripts/read_csv.c', 'core_c/scripts/signal_std.c',
                           'core_c/scripts/utils.c', '-o', 'core_c/executables/mse_3d_p']
    elif current_platform == 'Linux':  # Ubuntu
        compile_command = ['gcc', '-o', 'core_c/executables/mse_3d', 'core_c/scripts/mse_3d.c',
                           'core_c/scripts/read_csv.c', 'core_c/scripts/signal_std.c', 'core_c/scripts/utils.c',
                           '-lm', '-fopenmp', '-Icore_c/headers']
    else:
        raise OSError(f"Unsupported operating system: {current_platform}")

    subprocess.run(compile_command)


'''
info_matriz(): Returns useful info from matrix stored in a .csv
'''
def info_matriz(csv_path):
    data_array = np.genfromtxt(csv_path, delimiter=',')
    num_matrices = data_array.shape[0]
    rows = np.sqrt(data_array.shape[1])
    cols = np.sqrt(data_array.shape[1])
    return (num_matrices, rows, cols)