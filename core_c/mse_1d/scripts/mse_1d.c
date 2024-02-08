#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <omp.h>
#include "read_csv_funcs.h"
#include "signal_std_funcs.h"
#include "utils_funcs.h"

double calculate_U_ij_m(double** data, int i, int m, double r, int num_entries, double delta, int fuzzy, int distance_type, int window_size, double min, double max, int dim) {
    double count = 0;
    double N_m = num_entries - m;
    for(int a = 0; a < num_entries - m; a++){
        if(a == i){
            continue;
        }
        else{
            if(window_size == 0){
                double dist = mod_distance(m, data, i, a, distance_type, dim);
                if (fuzzy == 0){
                    if (dist <= r){
                        count ++;
                    }
                }
                else if (fuzzy == 1){
                    count += fuzzy_membership(dist, r, delta, min, max);
                }
            }
            else if (window_size == 1){
                double dist = mod_distance(m+1, data, i, a, distance_type, dim);
                if (dist <= r){
                    count ++;
                }
                else if (fuzzy == 1){
                    count += fuzzy_membership(dist, r, delta, min, max);
                }
            }
        }
    }
    return count / (N_m-1);
}

double calculate_U_m(double** data, int m, double r, int num_entries, double delta, int fuzzy, int distance_type, int window_size, double min, double max, int dim, int n_threads) {
    double sum = 0.0;
    double size = (double)(num_entries - m);
    #pragma omp parallel for reduction(+:sum) num_threads(n_threads)
    for(int i = 0; i < (int)size; i++){
        sum += calculate_U_ij_m(data, i, m, r, num_entries, delta, fuzzy, distance_type, window_size, min, max, dim);
    }
    #pragma omp barrier
    double average;
    #pragma omp critical
    {
        average = sum / size;
    }
    return average;
    // return sum / size;
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

double* method_mse(double** data, int scales, int m, double r, int fuzzy, int method, double delta, int distance_type, int num_entries, double min, double max, int dim, int n_threads){
    double* n_values = malloc(scales * sizeof(double));

    for (int i = 1; i <= scales; i++) { // 20
    // for (int i = 6; i <= scales; i++) { // 20
        if (method == 1 || method == 2) {
            int coarse_grained_n = num_entries % i; // 0

            double* n_coarse_values = malloc((coarse_grained_n + 1) * sizeof(double)); // 1
            double* um_coarse_values = malloc((coarse_grained_n + 1) * sizeof(double)); // 1
            double* um1_coarse_values = malloc((coarse_grained_n + 1) * sizeof(double)); // 1

            double average = 0.0;
            double um_average = 0.0;
            double um1_average = 0.0;

            for (int j = 0; j <= coarse_grained_n; j++) { // 0
                double** remaining_array = malloc((num_entries - coarse_grained_n) * sizeof(double*)); // 2000 - 0
                int contador = 0;
                for (int k = j; k < num_entries - coarse_grained_n + j; k++) { // 0 ; 2000
                    remaining_array[contador] = data[k];
                    contador += 1;
                }

                double** coarse_data = mod_coarse_graining(remaining_array, (num_entries - coarse_grained_n)/dim, i, dim);
                double U_m = calculate_U_m(coarse_data, m, r, ((num_entries - coarse_grained_n)/dim)/i, delta, fuzzy, distance_type, 0, min, max, dim, n_threads);
                double U_m_plus_one = calculate_U_m(coarse_data, m, r, ((num_entries - coarse_grained_n)/dim)/i, delta, fuzzy, distance_type, 1, min, max, dim, n_threads);
                double n = negative_logarithm(U_m, U_m_plus_one);


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
                double n = negative_logarithm(um_average, um1_average);
                n_values[i - 1] = n;
            }
        }

        else{
            double** coarse_data = mod_coarse_graining(data, num_entries/dim, i, dim);
            double U_m = calculate_U_m(coarse_data, m, r, (num_entries/dim)/i, delta, fuzzy, distance_type, 0, min, max, dim, n_threads);
            double U_m_plus_one = calculate_U_m(coarse_data, m, r, (num_entries/dim)/i, delta, fuzzy, distance_type, 1, min, max, dim, n_threads);
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
    int std_type = atoi(argv[11]);
    int n_threads = atoi(argv[15]);

    // Info relevante de signal

    int num_entries = atoi(argv[10]);
    double min = atof(argv[12]);
    double max = atof(argv[13]);
    int dim = atoi(argv[14]);

    // Abrir .csv

    double* data = read_csv(file_path, num_entries);
    double** data_d = (double**)malloc(num_entries/dim * sizeof(double*));
    int c = 0;
    int c_o = 0;
    double* temp_data;

    for (int i = 0; i < num_entries; i++) {
        temp_data = (double*)malloc(dim * sizeof(double));
        for (int j = 0; j < dim; j++) {
            temp_data[j] = data[i * dim + j];
        }
        data_d[c_o] = temp_data;
        c_o += 1;
    }

    // Desviacion estandar de signal
    if(std_type == 1){
        double signal_std = distance_m(data, m_distance, num_entries, distance_type);
        r *= signal_std;
    }
    else{
        double signal_std = unique_values_std(data, num_entries);
        r *= signal_std;
    }

    // MSE 1D
    double* entropy_values = method_mse(data_d, scales, m, r, fuzzy, method, delta, distance_type, num_entries, min, max, dim, n_threads);

    // Return entropy values
    for (int i = 0; i < scales; i++) {
        printf("%f \n", entropy_values[i]);
    }
    printf("\n");

    return 0;
}