#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <omp.h>
#include "read_csv_funcs.h"
#include "utils_funcs.h"


float calculate_U_ij_m(double **image, int i, int j, int m, double r, int H, int W, double delta, int fuzzy, int distance_type) {
    double count = 0;
    int N_m = (H - m) * (W - m);
    for (int a = 0; a < H - m; a++) {
        for (int b = 0; b < W - m; b++) {
            double dist = max_distance(m, image, i, j, a, b, distance_type);
            if (a == i && b == j) {
                continue;
            }
            else{
                if (fuzzy == 0){
                    if (dist <= r){
                        count ++;
                    }
                }
                else if (fuzzy == 1){
                    count += fuzzy_membership(dist, r, delta);
                }
            }
        }
    }
    return (float) count / (N_m-1);
}

float calculate_U_ij_m_plus_one(double **image, int i, int j, int m, double r, int H, int W, double delta, int fuzzy, int distance_type) {
    double count = 0;
    int N_m = (H - m) * (W - m);
    for (int a = 0; a < H - m; a++) {
        for (int b = 0; b < W - m; b++) {
            double dist = max_distance(m+1, image, i, j, a, b, distance_type);
            if (a == i && b == j) {
                continue;
            }
            else{
                if (fuzzy == 0){
                    if (dist <= r){
                        count ++;
                    }
                }
                else if (fuzzy == 1){
                    count += fuzzy_membership(dist, r, delta);
                }
            }
        }
    }
    return (float) count / (N_m-1);
}


float calculate_U_m(double **image, int m, double r, int H, int W, double delta, int fuzzy, int distance_type, int n_threads) {
    float sum = 0.0;
    #pragma omp parallel for reduction(+:sum) num_threads(n_threads)
    for (int i = 0; i < H - m; i++) {
        for (int j = 0; j < W - m; j++) {
            sum += calculate_U_ij_m(image, i, j, m, r, H, W, delta, fuzzy, distance_type);
        }
    }
     #pragma omp barrier
     float average;
     #pragma omp critical
     {
         average = sum / ((H - m) * (W - m));
     }
     return average;
//    return sum / ((H - m) * (W - m));
}


float calculate_U_m_plus_one(double **image, int m, double r, int H, int W, double delta, int fuzzy, int distance_type, int n_threads) {
    float sum = 0.0;
    #pragma omp parallel for reduction(+:sum) num_threads(n_threads)
    for (int i = 0; i < H - m; i++) {
        for (int j = 0; j < W - m; j++) {
            sum += calculate_U_ij_m_plus_one(image, i, j, m, r, H, W, delta, fuzzy, distance_type);
        }
    }
     #pragma omp barrier
     float average;
     #pragma omp critical
     {
         average = sum / ((H - m) * (W - m));
     }
     return average;
//   return sum / ((H - m) * (W - m));
}

int main(int argc, char *argv[]) {
    
    char* csv_path = argv[1];
    double** data = read_csv(csv_path);
    int scales = atoi(argv[2]);
    int rows = atoi(argv[3]);
    int cols = atoi(argv[4]);
    int m = atoi(argv[5]);
    double r = atof(argv[6]);
    double delta = atof(argv[7]);
    int fuzzy = atoi(argv[8]);
    int distance_type = atoi(argv[9]);
    int n_threads = atoi(argv[10]);


    double* n_values = malloc(scales * sizeof(double));

    for (int i = 1; i <= scales; i++) {
        double** coarse_data = coarse_graining(data, rows, cols, i);
        float U_m = calculate_U_m(coarse_data, m, r, rows/i, cols/i, delta, fuzzy, distance_type, n_threads);
        float U_m_plus_one = calculate_U_m_plus_one(coarse_data, m, r, rows/i, cols/i, delta, fuzzy, distance_type, n_threads);
        float n = negative_logarithm(U_m, U_m_plus_one);
        n_values[i-1] = n;
    }

    for (int i = 0; i < scales; i++) {
        printf("%f ", n_values[i]);
    }
    printf("\n");


    return 0;
}