#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

double** coarse_graining(double** arr, int rows, int cols, int scale_factor) {
    if (scale_factor == 1) {
        return arr;
    }
    int new_rows = rows / scale_factor;
    int new_cols = cols / scale_factor;
    double** cg_arr = malloc(new_rows * sizeof(double*));
    for (int i = 0; i < new_rows; i++) {
        cg_arr[i] = malloc(new_cols * sizeof(double));
        for (int j = 0; j < new_cols; j++) {
            double sum = 0;
            for (int x = i * scale_factor; x < (i + 1) * scale_factor; x++) {
                for (int y = j * scale_factor; y < (j + 1) * scale_factor; y++) {
                    sum += arr[x][y];
                }
            }
            cg_arr[i][j] = sum / (scale_factor * scale_factor);
        }
    }
    return cg_arr;
}


double max_distance(int m, double **image, int i, int j, int a, int b, int distance_type) {
    if (distance_type == 0){
        double max_dist = 0;
        for(int k=0; k<m; k++) {
            for(int l=0; l<m; l++) {
                double dist = fabs(image[i+k][j+l] - image[a+k][b+l]);
                if(dist > max_dist) {
                    max_dist = dist;
                }
            }
        }
        return max_dist;
    }
    else{
        double sum_dist = 0;
        for(int k=0; k<m; k++) {
            for(int l=0; l<m; l++) {
                double dist = powf(fabs(image[i+k][j+l] - image[a+k][b+l]), distance_type);
                sum_dist += dist;
            }
        }
        sum_dist = powf(sum_dist, (1.0/distance_type));
        return sum_dist;
    }
}

double fuzzy_membership(double distance, double r, double delta) {
    if (r == 0){
        return 1;
    }
    else{
        return expf(powf(distance, 2) * log(delta) / powf(r, 2.0));
    }
}

float negative_logarithm(float um, float umplus1) {
    if (um == 0) {
        return 0;
    }
    else {  
        float result = -log(umplus1 / um);
        return result;  
    }
}