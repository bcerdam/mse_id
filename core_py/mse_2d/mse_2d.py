import subprocess
import os
import shutil
import time
import numpy as np
import core_py.mse_2d.mse_2d_backbone as backbone

'''
run_c_program(): Executes C script.
parameters:
    - Same from mse_2d.
'''
def run_c_program(csv_path, scales, rows, cols, m, r, delta=0.7, fuzzy=False, distance_type=0, n_threads=32):
    command = [os.path.join(os.path.dirname(os.getcwd()), 'MSE_id/core_c/mse_2d', 'executables', 'mse_2d_p'), csv_path, str(scales), str(rows), str(cols), str(m), str(r), str(delta), str(fuzzy), str(distance_type), str(n_threads)]
    result = subprocess.run(command, stdout=subprocess.PIPE)
    output = result.stdout.decode('utf-8').strip()
    n_values = list(output.split())
    n_values = [np.inf if x == '1.#INF00' else float(x) for x in n_values]
    return n_values

'''
mse_2d(): Works as an interface to format the given parameters so that they can be fed into the C code.
parameters:
    - input: Any two-dimensional input should work, but they need to be in these formats: np.array, .png.
    - scales (int): Number of temporal scales in which the sample entropy of the three-dimensional signal will be calculated.
    - m (int): Size of the window where patterns are compared.
    - r (float): Also known as the tolerance parameter, it should be any value between (0, 1], recommended values are [0.1, 0.3]
    - fuzzy (bool): Wether or not a fuzzy function is applied to determine how similar two patterns are.
    - delta (float): fuzzy parameter, it should be any value between (0, 1).
    - distance_type (int): {0: max_norm, [1, inf]: p-norm}
    - n_threads: Number of parallel threads (OpenMP)
    - size: All images are by default resized to (100, 100), this because mse_2d is an expensive algorithm.
            I would recommend not going above (500, 500) unless you have access to a cluster or a CPU with
            a good amount of threads.
'''
def mse_2d(input, scales, m, r, delta=0.7, fuzzy=False, distance_type=0, n_threads=32, status=False, size=(100, 100)):
    if status:
        start_time = time.time()
        print('Working...')

    if fuzzy == False:
        fuzzy = 0
    elif fuzzy == True:
        fuzzy = 1

    input_type = backbone.detect_input_type(input)
    mse_values = []

    if input_type == 'np.array':
        filepath = backbone.temp_dir(input)
        rows, cols = input.shape
        mse_values.append(['array', run_c_program(filepath[1], scales, rows, cols, m, r * backbone.calculate_std(filepath[1]), delta, fuzzy, distance_type, n_threads)])
        shutil.rmtree(filepath[0])

    elif input_type == 'png':
        filename = os.path.basename(input)
        image_array = backbone.image_to_array(input, size)
        filepath = backbone.temp_dir(image_array)
        rows, cols = image_array.shape
        mse_values.append([filename,
                           run_c_program(filepath[1], scales, rows, cols, m, r * backbone.calculate_std(filepath[1]),
                                         delta, fuzzy, distance_type, n_threads)])
        shutil.rmtree(filepath[0])

    elif input_type == 'jpeg':
        filename = os.path.basename(input)
        image_array = backbone.image_to_array(input, size)
        filepath = backbone.temp_dir(image_array)
        rows, cols = image_array.shape
        mse_values.append([filename,
                           run_c_program(filepath[1], scales, rows, cols, m, r * backbone.calculate_std(filepath[1]),
                                         delta, fuzzy, distance_type, n_threads)])
        shutil.rmtree(filepath[0])

    elif input_type == 'dir_png':
        for filename in os.listdir(input):
            file_path = os.path.join(input, filename)
            image_array = backbone.image_to_array(file_path, size)
            filepath = backbone.temp_dir(image_array)
            rows, cols = image_array.shape
            mse_values.append([filename, run_c_program(filepath[1], scales, rows, cols, m, r * backbone.calculate_std(filepath[1]), delta, fuzzy, distance_type, n_threads)])
            shutil.rmtree(filepath[0])

    elif input_type == 'dir_jpeg':
        for filename in os.listdir(input):
            file_path = os.path.join(input, filename)
            image_array = backbone.image_to_array(file_path, size)
            filepath = backbone.temp_dir(image_array)
            rows, cols = image_array.shape
            mse_values.append([filename, run_c_program(filepath[1], scales, rows, cols, m, r * backbone.calculate_std(filepath[1]), delta, fuzzy, distance_type, n_threads)])
            shutil.rmtree(filepath[0])

    if status:
        end_time = time.time()
        execution_time = end_time - start_time
        print(execution_time)

    return mse_values