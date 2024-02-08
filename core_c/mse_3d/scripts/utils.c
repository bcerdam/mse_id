#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <dirent.h>

double*** coarse_graining(double*** list_of_matrices, int num_matrices, int scale, int rows, int cols) {
    if (scale == 1){
        return list_of_matrices;
    }
    int new_num_matrices = num_matrices / scale;
    double*** new_list_of_matrices = (double***)malloc(new_num_matrices * sizeof(double**));
    for (int i = 0; i < new_num_matrices; i++) {
        new_list_of_matrices[i] = (double**)malloc(sizeof(double*) * rows);
        for (int j = 0; j < rows; j++) {
            new_list_of_matrices[i][j] = (double*)malloc(sizeof(double) * cols);
            for (int k = 0; k < cols; k++) {
                double sum = 0.0;
                for (int s = i * scale; s < (i + 1) * scale && s < num_matrices; s++) {
                    sum += list_of_matrices[s][j][k];
                }
                new_list_of_matrices[i][j][k] = (sum / scale);
            }
        }
    }
    return new_list_of_matrices;
}

double fuzzy_membership(double distance, double r, double delta) {
    if (r == 0){
        return 1;
    }
    else{
        return expf(powf(distance, 2) * log(delta) / powf(r, 2.0));
    }
}

double fuzzy_sinusoidal(double distance, double r, double delta){
    if(r == 0){
        return 1;
    }
    else{
        return powf( (1 + expf( delta * (powf(distance, 2) - powf(r, 2) ) ) ) , -1);
    }
}

double window_distance(int m, double ***list_of_matrices, int i, int j, int k, int a, int b, int c, int distance_type) {
    if (distance_type == 0){
        double max_dist = 0;
        for (int n = 0; n < m; n++){
            for(int z = 0; z < m; z++) {
                for(int l = 0; l < m; l++) {
                    double dist = fabs(list_of_matrices[k+n][i+z][j+l] - list_of_matrices[c+n][a+z][b+l]);
                    if(dist > max_dist) {
                        max_dist = dist;
                    }
                }
            }
        }
        return max_dist;
    }
    else{
        double sum_dist = 0;
        for (int n = 0; n < m; n++){
            for(int z = 0; z < m; z++) {
                for(int l = 0; l < m; l++) {
                    double dist = powf(fabs(list_of_matrices[k+n][i+z][j+l] - list_of_matrices[c+n][a+z][b+l]), distance_type);
                    sum_dist += dist;
                }
            }
        }
        sum_dist = powf(sum_dist, (1.0/distance_type));
        return sum_dist;
    }
}