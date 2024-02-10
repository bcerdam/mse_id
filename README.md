# Installation

## Step 1: Clone repo.

```console
git clone https://github.com/bcerdam/mse_id.git
cd mse_id
pip3 install -v -e . 
```

## Step 2: Install requirements.

```console
pip install requirements.txt
```

## Step 3: Compile C code.

Works for macOS ([Clang](https://clang.llvm.org/get_started.html) required) and Ubuntu:

### mse_1d:

#### clang:
```console
clang -Xclang -fopenmp -I/usr/local/opt/libomp/include -L/opt/homebrew/Cellar/libomp/16.0.6/lib -lomp -Icore_c/headers core_c/scripts/mse_1d.c core_c/scripts/read_csv.c core_c/scripts/signal_std.c core_c/scripts/utils.c -o core_c/executables/mse_1d_p
```

#### gcc:
```console
gcc -o core_c/executables/mse_1d core_c/scripts/mse_1d.c core_c/scripts/read_csv.c core_c/scripts/signal_std.c core_c/scripts/utils.c  -lm -Icore_c/headers
```

### mse_2d:

#### clang:
```console
clang -Xclang -fopenmp -I/usr/local/opt/libomp/include -L/opt/homebrew/Cellar/libomp/16.0.6/lib -lomp -Icore_c/headers core_c/scripts/mse_2d.c core_c/scripts/read_csv.c core_c/scripts/utils.c -o core_c/executables/mse_2d_p
```

#### gcc:
```console
gcc -o core_c/executables/mse_2d core_c/scripts/mse_2d.c core_c/scripts/read_csv.c core_c/scripts/utils.c  -lm -Icore_c/headers
```

### mse_3d:

#### clang:
```console
clang -Xclang -fopenmp -I/usr/local/opt/libomp/include -L/opt/homebrew/Cellar/libomp/16.0.6/lib -lomp -Icore_c/headers core_c/scripts/mse_3d.c core_c/scripts/read_csv.c core_c/scripts/signal_std.c core_c/scripts/utils.c -o core_c/executables/mse_3d_p
```

#### gcc:
```console
gcc -o core_c/executables/mse_3d core_c/scripts/mse_3d.c core_c/scripts/read_csv.c core_c/scripts/signal_std.c core_c/scripts/utils.c -lm -fopenmp -Icore_c/headers
```

# Usage

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

## Examples:

### MSE_1d:

# white_noise_1d = np.random.random((10000, 1))
# mse_values_1d = mse_1d.mse_1d(input=white_noise_1d, scales=20, m=2, r=0.2, fuzzy=True, method='RCMSE', n_threads=8)
# utils_id.plot_arrays(mse_values_1d)


### MSE_2d:

# white_noise_2d = np.random.randint(0, 255 + 1, size=(100, 100))
# mse_values_2d = mse_2d.mse_2d(input=white_noise_2d, scales=20, m=1, r=0.5, n_threads=8)
# utils_id.plot_arrays(mse_values_2d)


### MSE_3d:

# white_noise_3d = np.random.random((10, 10, 100))
# mse_values_3d = mse_3d.mse_3d(input=white_noise_3d, scales=20, m=2, r=0.2, fuzzy=True, method='RCMSE', n_threads=8)
# utils_id.plot_arrays(mse_values_3d)