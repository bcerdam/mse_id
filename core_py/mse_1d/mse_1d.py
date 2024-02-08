import os
import time
import subprocess
import shutil
import core_py.mse_1d.mse_1d_backbone as backbone

'''
run_c_program(): Executes C script.
parameters:
    - Same from mse_1d.
'''
def run_c_program(csv_path, scales, m, r, fuzzy, method, delta=0.7, distance_type=0, m_distance=2, std_type=1, dim=1, n_threads=32):
    info = backbone.info_matriz(csv_path)
    command = [os.path.join(os.path.dirname(os.getcwd()), 'MSE_id/core_c/mse_1d', 'executables', 'mse_1d_p'), csv_path, str(scales), str(m), str(r), str(fuzzy), str(method),
               str(delta), str(distance_type), str(m_distance), str(info[0]), str(std_type), str(info[1]), str(info[2]), str(dim), str(n_threads)]
    result = subprocess.run(command, stdout=subprocess.PIPE).stdout.decode('utf-8').strip()
    n_values = list(result.split())
    n_values = [float(x) for x in n_values]
    return n_values


'''
mse_1d(): Works as an interface to format the given parameters so that they can be fed into the C code.
parameters:
    - input: Any one-dimensional input should work, but they need to be in these formats: np.array, .csv.
    - scales (int): Number of temporal scales in which the sample entropy of the three-dimensional signal will be calculated.
    - m (int): Size of the window where patterns are compared.
    - r (float): Also known as the tolerance parameter, it should be any value between (0, 1], recommended values are [0.1, 0.3]
    - fuzzy (bool): Wether or not a fuzzy function is applied to determine how similar two patterns are.
    - delta (float): fuzzy parameter, it should be any value between (0, 1).
    - distance_type (int): {0: max_norm, [1, inf]: p-norm}
    - std_type (str): 'UNIQUE_VALUES' => standard deviation is calculated from unique signal values
                      'UNIQUE_DISTANCES' => standard deviation is calculated from unique distance values
                      Better to leave it as 'UNIQUE_VALUES', since 'UNIQUE_DISTANCES' is slow to run and also the memory usage
                      is not properly handled.
    - m_distance (int): If 'UNIQUE_DISTANCES' is used, then this parameter is equivalent to the 'm' parameter.
    - dim: Used if each point in the time series has multiple attributes. For example, if you have a time series where
           each point has 2 attributes (temp, humidity), then dim needs to be set to 2. 
    - n_threads: Number of parallel threads. (OpenMP)
'''
def mse_1d(input, scales, m, r, fuzzy, method, delta=0.7, distance_type=0, m_distance=2, std_type='UNIQUE_VALUES', dim=1, n_threads=32, status=False):
    if status:
        start_time = time.time()
        print('Working...')

    if fuzzy == True:
        fuzzy = 1
    else:
        fuzzy = 0

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

    input_type = backbone.detect_input_type(input)
    mse_values = []
    if input_type == 'np.array':
        filepath = backbone.temp_dir(input)
        mse_values.append(['array',
                           run_c_program(filepath[1], scales, m, r, fuzzy,
                                         method, delta, distance_type, m_distance, std_type, dim, n_threads)])
        shutil.rmtree(filepath[0])
    elif input_type == 'csv':
        filename = os.path.basename(input)
        mse_values.append([filename,
                           run_c_program(input, scales, m, r, fuzzy,
                                         method, delta, distance_type, m_distance, std_type, dim, n_threads)])
    elif input_type == 'dir_csv':
        for filename in os.listdir(input):
            file_path = os.path.join(input, filename)
            mse_values.append([filename,
                               run_c_program(file_path, scales, m, r, fuzzy,
                                             method, delta, distance_type, m_distance, std_type, dim, n_threads)])

    if status:
        end_time = time.time()
        execution_time = end_time - start_time
        print(execution_time)

    return mse_values