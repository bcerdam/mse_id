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
