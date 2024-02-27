import subprocess
import os
import time
import shutil
import core_py.mse_3d.mse_3d_backbone as backbone

'''
run_c_program(): Executes C script.
parameters:
    - Same from mse_3d.
'''
def run_c_program(input, scales, m, r, fuzzy, method, delta=0.7, distance_type=0, m_distance=2, sampleo=1, std_type=1, mod=False, m_espacial=1, dim_cubo=1, n_threads=32):
    info = backbone.info_matriz(input)

    # Non cluster
    # command = [os.path.join(os.path.dirname(os.getcwd()), 'mse_id/core_c/mse_3d', 'executables', 'mse_3d_p'), input, str(scales), str(m), str(r), str(fuzzy), str(method),
    #            str(delta), str(distance_type), str(m_distance), str(sampleo), str(info[0]), str(info[1]), str(info[2]), str(std_type), str(mod), str(m_espacial), str(dim_cubo), str(n_threads)]

    # Cluster
    command = ['/home3/bcmardini/mse_id/core_c/mse_3d', 'executables', 'mse_3d_p', input, str(scales), str(m), str(r), str(fuzzy), str(method),
               str(delta), str(distance_type), str(m_distance), str(sampleo), str(info[0]), str(info[1]), str(info[2]), str(std_type), str(mod), str(m_espacial), str(dim_cubo), str(n_threads)]
    result = subprocess.run(command, stdout=subprocess.PIPE).stdout.decode('utf-8').strip()
    n_values = list(result.split())
    n_values = [float(x) for x in n_values]
    return n_values

'''
mse_3d(): Works as an interface to format the given parameters so that they can be fed into the C code.
parameters:
    - input: Any three-dimensional input should work, but they need to be in these formats: np.array, .mp4, .csv.
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
    - sampleo (int):  If 'UNIQUE_DISTANCES' is used, then this parameter samples possible unique distances, making it faster.
    - mod (bool): Activates modification of mse_3d algorithm, it basically gives more control on the shape of the patterns to be compared.
    - m_espacial (int): How far you want to consider values on the temporal scale as a pattern.
    - dim_cubo (int): Height and width of the pattern to predict.
    - shape: If a .mp4 is given, then that .mp4 is reshaped into that shape.
    - n_threads: Number of parallel threads (OpenMP)
'''
def mse_3d(input, scales, m, r, fuzzy, method, delta=0.7, distance_type=0, m_distance=2, sampleo=1, std_type='UNIQUE_VALUES', mod=False, m_espacial=1, dim_cubo=1, shape=(10, 10, 100), n_threads=32, status=False):
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

    if mod == False:
        mod = 0
    elif mod == True:
        mod = 1
        valores_permitidos = [x for x in range(2, 16, 2)]
        if m not in valores_permitidos:
            return print('Si parametro mod=True, entonces parametro "m" debe ser igual a 2, 4, 6 o 8.')

        if dim_cubo not in [1, 3, 5] or dim_cubo > (m+1):
            return print('dim_cubo debe ser menor que parametro "m", y debe ser impar: (1, 3, 5, etc.)')

    input_type = backbone.detect_input_type(input)
    mse_values = []
    if input_type == 'np.array':
        filepath = backbone.temp_dir(input)
        mse_values.append(['array',
                           run_c_program(filepath[1], scales, m, r, fuzzy, method, delta, distance_type, m_distance,
                                         sampleo, std_type, mod, m_espacial, dim_cubo, n_threads)])
        shutil.rmtree(filepath[0])
    elif input_type == 'mp4':
        video_array = backbone.mp4_to_3d_arr(input, shape)
        filepath = backbone.temp_dir(video_array)
        mse_values.append(['array',
                           run_c_program(filepath[1], scales, m, r, fuzzy, method, delta, distance_type, m_distance,
                                         sampleo, std_type, mod, m_espacial, dim_cubo, n_threads)])
        shutil.rmtree(filepath[0])
    elif input_type == 'csv':
        filename = os.path.basename(input)
        mse_values.append([filename,
                           run_c_program(input, scales, m, r, fuzzy, method, delta, distance_type, m_distance,
                                         sampleo, std_type, mod, m_espacial, dim_cubo, n_threads)])
    elif input_type == 'dir_csv':
        for filename in os.listdir(input):
            file_path = os.path.join(input, filename)
            mse_values.append([filename, run_c_program(file_path, scales, m, r, fuzzy, method, delta, distance_type, m_distance, sampleo, std_type, mod, m_espacial, dim_cubo, n_threads)])
    elif input_type == 'dir_mp4':
        for filename in os.listdir(input):
            if '.mp4' not in filename:
                pass
            else:
                file_path = os.path.join(input, filename)
                video_array = backbone.mp4_to_3d_arr(file_path, shape)
                csv_filepath = backbone.temp_dir(video_array)
                mse_values.append([filename, run_c_program(csv_filepath[1], scales, m, r, fuzzy, method, delta, distance_type, m_distance, sampleo, std_type, mod, m_espacial, dim_cubo, n_threads)])
                shutil.rmtree(csv_filepath[0])
    else:
        print("Valid inputs are: Directory containing .csv's, singular .csv, .mp4 or a np.array")

    if status:
        end_time = time.time()
        execution_time = end_time - start_time
        print(execution_time)

    return mse_values
