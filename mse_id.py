import argparse
import numpy as np
import utils_id
import core_py.mse_1d.mse_1d as mse_1d_f
import core_py.mse_2d.mse_2d as mse_2d_f
import core_py.mse_3d.mse_3d as mse_3d_f

'''
Usage:

Basic MSE_id parameters:
    - input: One, two or three dimensional input, depending on the algorithm.
        - For mse_2d and mse_3d the inputs height and width need to be squared, and for mse_2d the input values need to be int.
    - scales (int): Number of temporal scales in which the sample entropy of the input signal will be calculated.
    - m (int): Size of the window where patterns are compared.
    - r (float): Also known as the tolerance parameter, it should be any value between (0, 1], recommended values are [0.1, 0.3]
    - fuzzy (bool): Wether or not a fuzzy function is applied to determine how similar two patterns are.
    - method (str): Wether it is the MSE algorithm, the Composite (CMSE) or the Refined Composite (RCMSE) variants. (Not implemented in mse_2d)
    - n_threads (int): Number of parallel threads (OpenMP)
    
More advanced parameters are explained in the mse_1d.py, mse_2d.py, mse_3d.py scripts.
'''

'''
Examples:
'''

'''
MSE_1d:
'''
def mse_1d(input, scales, m, r, fuzzy, method, delta=0.7, distance_type=0, m_distance=2, std_type='UNIQUE_VALUES', dim=1, n_threads=32, status=False):
    mse_values_1d = mse_1d_f.mse_1d(input, scales, m, r, fuzzy, method, delta, distance_type, m_distance, std_type, dim, n_threads, status)
    return mse_values_1d

# white_noise_1d = np.random.random((10000, 1))
# mse_values_1d = mse_1d(input=white_noise_1d, scales=20, m=2, r=0.2, fuzzy=True, method='RCMSE', n_threads=8)
# utils_id.plot_arrays(mse_values_1d)

'''
MSE_2d:
'''
def mse_2d(input, scales, m, r, delta=0.7, fuzzy=False, distance_type=0, n_threads=32, status=False, size=(100, 100)):
    mse_values_2d = mse_2d_f.mse_2d(input, scales, m, r, delta, fuzzy, distance_type, n_threads, status, size)
    return mse_values_2d

# white_noise_2d = np.random.randint(0, 255 + 1, size=(100, 100))
# mse_values_2d = mse_2d(input=white_noise_2d, scales=20, m=1, r=0.5, n_threads=8)
# utils_id.plot_arrays(mse_values_2d)

'''
MSE_3d:
'''

def mse_3d(input, scales, m, r, fuzzy, method, delta=0.7, distance_type=0, m_distance=2, sampleo=1, std_type='UNIQUE_VALUES', mod=False, m_espacial=1, dim_cubo=1, shape=(10, 10, 100), n_threads=32, status=False):
    mse_values_3d = mse_3d_f.mse_3d(input, scales, m, r, fuzzy, method, delta, distance_type, m_distance, sampleo, std_type, mod, m_espacial, dim_cubo, shape, n_threads, status)
    return mse_values_3d

# white_noise_3d = np.random.random((10, 10, 100))
# mse_values_3d = mse_3d(input=white_noise_3d, scales=20, m=2, r=0.2, fuzzy=True, method='RCMSE', n_threads=8)
# utils_id.plot_arrays(mse_values_3d)

'''
Common parameters:
{'scales':20, 'm':2, 'r':0.2, 'fuzzy':True, 'method':'RCMSE', 'n_threads':8, 'delta':0.9, 'mod':True, 'n_threads':64}
'''

def parse_arguments():
    parser = argparse.ArgumentParser(description='Calculate MSE values.')

    parser.add_argument('input', help='Input data')
    parser.add_argument('--scales', type=int, help='Number of scales')
    parser.add_argument('--m', type=int, help='Window size for pattern comparison')
    parser.add_argument('--r', type=float, help='Tolerance parameter')
    parser.add_argument('--fuzzy', type=bool, help='Whether or not to use fuzzy function')
    parser.add_argument('--method', help='MSE algorithm method')
    parser.add_argument('--delta', type=float, default=0.7, help='Delta parameter')
    parser.add_argument('--distance_type', type=int, default=0, help='Distance type')
    parser.add_argument('--m_distance', type=int, default=2, help='M distance')
    parser.add_argument('--sampleo', type=int, default=1, help='Sampleo parameter')
    parser.add_argument('--std_type', default='UNIQUE_VALUES', help='Standard type')
    parser.add_argument('--mod', type=bool, default=False, help='Mod parameter')
    parser.add_argument('--m_espacial', type=int, default=1, help='M espacial parameter')
    parser.add_argument('--dim_cubo', type=int, default=1, help='Dimension cubo parameter')
    parser.add_argument('--shape', type=int, nargs='+', default=[10, 10, 100], help='Shape parameter')
    parser.add_argument('--n_threads', type=int, default=32, help='Number of threads')
    parser.add_argument('--status', type=bool, default=False, help='Status parameter')

    return parser.parse_args()

def main():
    args = parse_arguments()

    mse_values = mse_3d(args.input, args.scales, args.m, args.r, args.fuzzy, args.method, args.delta,
                                      args.distance_type, args.m_distance, args.sampleo, args.std_type, args.mod,
                                      args.m_espacial, args.dim_cubo, tuple(args.shape), args.n_threads, args.status)

    for value in mse_values[0][1]:
        print(value)

if __name__ == "__main__":
    main()