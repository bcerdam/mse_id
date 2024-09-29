#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <omp.h>
#include "read_csv_funcs.h"
#include "signal_std_funcs.h"
#include "utils_funcs.h"


double calculate_U_ij_m(double ***list_of_matrices, int i, int j, int k, int m, double r, int H, int W, int T, double delta, int fuzzy, int distance_type, int window_size, int mod, int m_espacial, int dim_cubo) {
    double count = 0;
    int t_reduce;

    if(mod == 0){
        t_reduce = m;
    }
    else if(mod == 1){
        t_reduce = ((m_espacial-1)+1);
    }
    double size = (double)((H - m) * (W - m) * (T - t_reduce));

    int m_mod = m+1;
    for (int c = 0; c < T - t_reduce; c++){
        for (int a = 0; a < H - m; a++) {
            for (int b = 0; b < W - m; b++) {
                if (a == i && b == j && c == k) {
                    continue;
                }
                else {
                    if (mod == 1){
                        if (window_size == 0){
                            double dist = distance_exp_den(m_mod, list_of_matrices, i, j, k, a, b, c, distance_type, m_espacial, dim_cubo);
                            if (dist <= r){
                                count ++;
                            }
                            else if (fuzzy == 1){
                                count += fuzzy_membership(dist, r, delta);
                                // count += fuzzy_sinusoidal(dist, r, delta);
                            }
                        }
                        else if (window_size == 1){
                            double dist = distance_exp_num(m_mod, list_of_matrices, i, j, k, a, b, c, distance_type, m_espacial, dim_cubo);
                            if (dist <= r){
                                count ++;
                            }
                            else if (fuzzy == 1){
                                count += fuzzy_membership(dist, r, delta);
                                // count += fuzzy_sinusoidal(dist, r, delta);
                            }
                        }
                        
                    }
                    else if(window_size == 0){
                        double dist = distance(m, list_of_matrices, i, j, k, a, b, c, distance_type);
                        if (fuzzy == 0){
                            if (dist <= r){
                                count ++;
                            }
                        }
                        else if (fuzzy == 1){
                            count += fuzzy_membership(dist, r, delta);
                            // count += fuzzy_sinusoidal(dist, r, delta);
                        }
                    }
                    else if (window_size == 1){
                        double dist = distance(m+1, list_of_matrices, i, j, k, a, b, c, distance_type);
                        if (dist <= r){
                            count ++;
                        }
                        else if (fuzzy == 1){
                            count += fuzzy_membership(dist, r, delta);
                            // count += fuzzy_sinusoidal(dist, r, delta);
                        }
                    }
                }
            }
        }
    }
    return count / (size-1);
}

double calculate_U_m(double ***list_of_matrices, int m, double r, int H, int W, int T, double delta, int fuzzy, int distance_type, int window_size, int mod, int m_espacial, int dim_cubo, int n_threads) {
    double sum = 0.0;
    int t_reduce;

    if(mod == 0){
        t_reduce = m;
    }
    else if(mod == 1){
        t_reduce = ((m_espacial-1)+1);
    }
    double size = (double)((H - m) * (W - m) * (T - t_reduce));

    #pragma omp parallel for reduction(+:sum) num_threads(n_threads)
    for (int k = 0; k < T - t_reduce; k++){
        for (int i = 0; i < H - m; i++) {
            for (int j = 0; j < W - m; j++) {
                sum += calculate_U_ij_m(list_of_matrices, i, j, k, m, r, H, W, T, delta, fuzzy, distance_type, window_size, mod, m_espacial, dim_cubo);
            }
        }
    }
    #pragma omp barrier
    double average;
    #pragma omp critical
    {
        average = sum / size;
    }
    return average;
}

double negative_logarithm(double um, double umplus1) {
    if (um == 0) {
        return 0;
    }
    else {  
        double result = -log(umplus1 / um);
        return result;  
    }
}

double* method_mse(double*** list_of_matrices, int scales, int m, double r, int fuzzy, int method, double delta, int distance_type, int num_files, int rows, int cols, int mod, int m_espacial, int dim_cubo, int n_threads){
    double* n_values = malloc(scales * sizeof(double));

    for (int i = 1; i <= scales; i++) {
    // for (int i = 18; i <= 20; i++) {  
        if (method == 1 || method == 2) {
            int coarse_grained_n = num_files % i;

            double* n_coarse_values = malloc((coarse_grained_n + 1) * sizeof(double));
            double* um_coarse_values = malloc((coarse_grained_n + 1) * sizeof(double));
            double* um1_coarse_values = malloc((coarse_grained_n + 1) * sizeof(double));

            double average = 0.0;
            double um_average = 0.0;
            double um1_average = 0.0;

            for (int j = 0; j <= coarse_grained_n; j++) { 
                double*** remaining_array = malloc((num_files - coarse_grained_n) * sizeof(double**)); 
                int contador = 0;
                for (int k = j; k < num_files - coarse_grained_n + j; k++) { 
                    remaining_array[contador] = list_of_matrices[k]; 
                    contador += 1;
                }

                double*** coarse_data = coarse_graining(remaining_array, (num_files - coarse_grained_n), i, rows, cols);

                float U_m = calculate_U_m(coarse_data, m, r, cols, rows, (num_files - coarse_grained_n) / i, delta, fuzzy, distance_type, 0, mod, m_espacial, dim_cubo, n_threads);
                float U_m_plus_one = calculate_U_m(coarse_data, m, r, cols, rows, (num_files - coarse_grained_n) / i, delta, fuzzy, distance_type, 1, mod, m_espacial, dim_cubo, n_threads);
                float n = negative_logarithm(U_m, U_m_plus_one);

                n_coarse_values[j] = n;
                um_coarse_values[j] = U_m;
                um1_coarse_values[j] = U_m_plus_one;
            }

            if (method == 1){
                for (int z = 0; z <= coarse_grained_n; z++) { 
                    average += n_coarse_values[z]; 
                }
                average /= (coarse_grained_n + 1);
                n_values[i - 1] = average;
            }
            else if (method == 2){
                for (int z = 0; z <= coarse_grained_n; z++) { 
                    um_average += um_coarse_values[z];
                    um1_average += um1_coarse_values[z];
                }

                um_average /= (coarse_grained_n + 1);
                um1_average /= (coarse_grained_n + 1);
                float n = negative_logarithm(um_average, um1_average);
                n_values[i - 1] = n;
            }
        }

        else{
            double*** coarse_data = coarse_graining(list_of_matrices, num_files, i, rows, cols);
            double U_m = calculate_U_m(coarse_data, m ,r, rows, cols, num_files/i, delta, fuzzy, distance_type, 0, mod, m_espacial, dim_cubo, n_threads);
            double U_m_plus_one = calculate_U_m(coarse_data, m, r, rows, cols, num_files/i, delta, fuzzy, distance_type, 1, mod, m_espacial, dim_cubo, n_threads);
            double n = negative_logarithm(U_m, U_m_plus_one);
            n_values[i-1] = n;
        }
    }
    return n_values;
}

int main(int argc, char* argv[]) {

    // Parametros principales
    char* file_path = argv[1];
    int scales = atoi(argv[2]);
    int m = atoi(argv[3]);
    double r = atof(argv[4]);
    int fuzzy = atoi(argv[5]);
    int method = atoi(argv[6]);

    // Parametros secundarios

    double delta = atof(argv[7]);
    int distance_type = atoi(argv[8]);
    int m_distance = atoi(argv[9]);
    int sampleo = atoi(argv[10]);
    int std_type = atoi(argv[14]);
    int mod = atoi(argv[15]);
    int m_espacial = atoi(argv[16]);
    int dim_cubo = atoi(argv[17]);
    int n_threads = atoi(argv[18]);
    int m_temp = atoi(argv[19]);
    int plus_one = atoi(argv[20]);

    // Info relevante de signal

    int num_matrices = atoi(argv[11]);
    int num_rows = atoi(argv[12]);
    int num_cols = atoi(argv[13]);

    // Abrir .csv
    int rows, columns; // rows = numero de matrices, columns = rows * columns // Malos nombres de variables.
    double** data_array = read_csv(file_path, &rows, &columns);

    // Estructura matrices a lo largo del tiempo
    double*** signal_array = data_structure(data_array, num_matrices, num_rows, num_cols);

    // Desviacion estandar de signal
    if(std_type == 1){
        double signal_std = distance_m(signal_array, m_distance, num_rows, num_cols, num_matrices, distance_type, sampleo, m_temp, plus_one);
        r *= signal_std;
    }
    else{
        double signal_std = unique_values_std(signal_array, num_rows, num_cols, num_matrices);
        r *= signal_std;
    }

    // MSE 3D
    double* entropy_values = method_mse(signal_array, scales, m, r, fuzzy, method, delta, distance_type, num_matrices, num_rows, num_cols, mod, m_espacial, dim_cubo, n_threads);
    for (int i = 0; i < scales; i++) {
        printf("%f \n", entropy_values[i]);
    }
    printf("\n");

    return 0;
}