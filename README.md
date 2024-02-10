# Installation

## Step 1: Clone repo.

From a desired directory, do this:

```console
git clone https://github.com/bcerdam/mse_id.git
cd mse_id
python3 -m venv env
source ./env/bin/activate
pip install -v -e . 
```

## Step 2: Install requirements.

```console
pip install -r requirements.txt
```

## Step 3: Compile C code.

Works for macOS ([Clang](https://clang.llvm.org/get_started.html) required) and Ubuntu:

### mse_1d:

#### clang:
```console
clang -Xclang -fopenmp -I/usr/local/opt/libomp/include -L/opt/homebrew/Cellar/libomp/16.0.6/lib -lomp -Icore_c/mse_1d/headers core_c/mse_1d/scripts/mse_1d.c core_c/mse_1d/scripts/read_csv.c core_c/mse_1d/scripts/signal_std.c core_c/mse_1d/scripts/utils.c -o core_c/mse_1d/executables/mse_1d_p
```

#### gcc:
```console
gcc -o core_c/mse_1d/executables/mse_1d core_c/mse_1d/scripts/mse_1d.c core_c/mse_1d/scripts/read_csv.c core_c/mse_1d/scripts/signal_std.c core_c/mse_1d/scripts/utils.c  -lm -Icore_c/mse_1d/headers
```

### mse_2d:

#### clang:
```console
clang -Xclang -fopenmp -I/usr/local/opt/libomp/include -L/opt/homebrew/Cellar/libomp/16.0.6/lib -lomp -Icore_c/mse_2d/headers core_c/mse_2d/scripts/mse_2d.c core_c/mse_2d/scripts/read_csv.c core_c/mse_2d/scripts/utils.c -o core_c/mse_2d/executables/mse_2d_p
```

#### gcc:
```console
gcc -o core_c/mse_2d/executables/mse_2d_p core_c/mse_2d/scripts/mse_2d.c core_c/mse_2d/scripts/read_csv.c core_c/mse_2d/scripts/utils.c  -lm -Icore_c/mse_2d/headers
```

### mse_3d:

#### clang:
```console
clang -Xclang -fopenmp -I/usr/local/opt/libomp/include -L/opt/homebrew/Cellar/libomp/16.0.6/lib -lomp -Icore_c/mse_3d/headers core_c/mse_3d/scripts/mse_3d.c core_c/mse_3d/scripts/read_csv.c core_c/mse_3d/scripts/signal_std.c core_c/mse_3d/scripts/utils.c -o core_c/mse_3d/executables/mse_3d_p
```

#### gcc:
```console
gcc -o core_c/mse_3d/executables/mse_3d_p core_c/mse_3d/scripts/mse_3d.c core_c/mse_3d/scripts/read_csv.c core_c/mse_3d/scripts/signal_std.c core_c/mse_3d/scripts/utils.c -lm -fopenmp -Icore_c/mse_3d/headers
```
