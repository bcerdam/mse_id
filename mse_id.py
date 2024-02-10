import numpy as np
import utils_id
import core_py.mse_1d.mse_1d as mse_1d
import core_py.mse_2d.mse_2d as mse_2d
import core_py.mse_3d.mse_3d as mse_3d

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
# white_noise_1d = np.random.random((10000, 1))
# mse_values_1d = mse_1d.mse_1d(input=white_noise_1d, scales=20, m=2, r=0.2, fuzzy=True, method='RCMSE', n_threads=8)
# utils_id.plot_arrays(mse_values_1d)

'''
MSE_2d:
'''
# white_noise_2d = np.random.randint(0, 255 + 1, size=(100, 100))
# mse_values_2d = mse_2d.mse_2d(input=white_noise_2d, scales=20, m=1, r=0.5, n_threads=8)
# utils_id.plot_arrays(mse_values_2d)

'''
MSE_3d:
'''
# white_noise_3d = np.random.random((10, 10, 100))
# mse_values_3d = mse_3d.mse_3d(input=white_noise_3d, scales=20, m=2, r=0.2, fuzzy=True, method='RCMSE', n_threads=8)
# utils_id.plot_arrays(mse_values_3d)