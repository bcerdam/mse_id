#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

int compare(const void* a, const void* b) {
    double x = *(const double*)a;
    double y = *(const double*)b;
    if (x < y) {
        return -1;
    } else if (x > y) {
        return 1;
    }
    return 0;
}

double* remove_duplicates(double* arr, int size, int* new_size) {
    qsort(arr, size, sizeof(double), compare);

    double* unique_arr = (double*)malloc(size * sizeof(double));

    int count = 0;
    for (int i = 0; i < size; i++) {
        if (i > 0 && arr[i] == arr[i - 1]) {
            continue;
        }

        unique_arr[count] = arr[i];
        count++;
    }

    unique_arr = (double*)realloc(unique_arr, count * sizeof(double));

    *new_size = count;
    return unique_arr;
}

double calculate_standard_deviation(double* values, int size) {
    double mean = 0.0;
    double sum = 0.0;

    for (int i = 0; i < size; i++) {
        mean += values[i];
    }
    mean /= size;

    for (int i = 0; i < size; i++) {
        double diff = fabs(values[i] - mean);
        sum += diff * diff;
    }

    double variance = sum / size;
    double standard_deviation = sqrt(variance);

    return standard_deviation;
}


double distance(int m, double ***list_of_matrices, int i, int j, int k, int a, int b, int c, int distance_type) {
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

double distance_exp_den(int m, double ***list_of_matrices, int i, int j, int k, int a, int b, int c, int distance_type, int m_espacial, int dim_cubo) {
    if(distance_type == 0){
        double max_dist = 0;
            for (int n = 0; n < m_espacial; n++){
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
            for (int n = 0; n < m_espacial; n++){
                for(int z = 0; z < m; z++) {
                    for(int l = 0; l < m; l++) {
                        double dist = pow(fabs(list_of_matrices[k+n][i+z][j+l] - list_of_matrices[c+n][a+z][b+l]), distance_type);
                        sum_dist += dist;
                    }
                }
            }
        sum_dist = powf(sum_dist, (1.0/distance_type));
        return sum_dist;
    }
}

double distance_exp_num(int m, double ***list_of_matrices, int i, int j, int k, int a, int b, int c, int distance_type, int m_espacial, int dim_cubo) {
    if(distance_type == 0){
        double max_dist = 0;
        for (int n = 0; n < m_espacial; n++){
            for(int z = 0; z < m; z++) {
                for(int l = 0; l < m; l++) {
                    double dist = fabs(list_of_matrices[k+n][i+z][j+l] - list_of_matrices[c+n][a+z][b+l]);
                    if(dist > max_dist) {
                        max_dist = dist;
                    }
                }
            }
        }
        int frame_middle = m / 2; // 1
        int sub_frame_middle = dim_cubo / 2; // 0
        int x_start = frame_middle-sub_frame_middle; // 1
        int y_start = frame_middle-sub_frame_middle; // 1
        for(int z = x_start; z < x_start+dim_cubo; z++) { // 1 a 1
                for(int l = y_start; l < y_start+dim_cubo; l++) { // 1 a 1
                    double dist = fabs(list_of_matrices[k+m_espacial][i+z][j+l] - list_of_matrices[c+m_espacial][a+z][b+l]);
                    if(dist > max_dist) {
                        max_dist = dist;
                    }
                }
            }
        return max_dist;
    }
    else{
        double sum_dist = 0;
        for (int n = 0; n < m_espacial; n++){
            for(int z = 0; z < m; z++) {
                for(int l = 0; l < m; l++) {
                    double dist = powf(fabs(list_of_matrices[k+n][i+z][j+l] - list_of_matrices[c+n][a+z][b+l]), distance_type);
                    sum_dist += dist;
                }
            }
        }
        int frame_middle = m / 2; // 1
        int sub_frame_middle = dim_cubo / 2; // 0
        int x_start = frame_middle-sub_frame_middle; // 1
        int y_start = frame_middle-sub_frame_middle; // 1
        for(int z = x_start; z < x_start+dim_cubo; z++) { // 1 a 1
                for(int l = y_start; l < y_start+dim_cubo; l++) { // 1 a 1
                    double dist = powf(fabs(list_of_matrices[k+m_espacial][i+z][j+l] - list_of_matrices[c+m_espacial][a+z][b+l]), distance_type);
                    sum_dist += dist;
                }
            }
        sum_dist = powf(sum_dist, (1.0/distance_type));
        return sum_dist;
    }
}

double* calculate_distance_m(double*** signal_array, int i, int j, int k, int m, int num_rows, int num_cols, int num_matrices, int distance_type, int* temp_new_size, int m_temp, int plus_one) {
    double* dists_array = (double*)malloc((((num_matrices-m_temp)*(num_rows-m)*(num_cols-m))-1) * sizeof(double));
    int co = 0;

    for (int c = 0; c < num_matrices - m_temp; c++){
        for (int a = 0; a < num_rows - m; a++) {
            for (int b = 0; b < num_cols - m; b++) {
                if (a == i && b == j && c == k) {
                    continue;
                }
                else{
                    // double dist = distance(m, signal_array, i, j, k, a, b, c, distance_type);
                    if(plus_one == 0){
                        double dist = distance_exp_den(m, signal_array, i, j, k, a, b, c, distance_type, m_temp, 1);
                        dists_array[co] = dist;
                    }
                    else if(plus_one == 1){
                        double dist = distance_exp_num(m, signal_array, i, j, k, a, b, c, distance_type, m_temp, 1);
                        dists_array[co] = dist;
                    }
                    co += 1;
                }
            }
        }
    }
    // double* temp_unique_arr = remove_duplicates(dists_array, ((num_matrices-m)*(num_rows-m)*(num_cols-m)-1), temp_new_size);
    // free(dists_array);
    // return temp_unique_arr;
    return dists_array;
}

double distance_m(double*** signal_array, int m, int num_rows, int num_cols, int num_matrices, int distance_type, double sampleo, int m_temp, int plus_one) {
    int size = (int)(round((num_matrices - m_temp) * 1 / sampleo) * round((num_rows - m) * 1 / sampleo) * round((num_cols - m) * 1 / sampleo));
    double** pos = (double**)malloc(size * sizeof(double*));
    int* ind_unique_values = (int*)malloc(size*sizeof(int));
    int flattened_size = 0;
    int c = 0;

    for (int k = 0; k < num_matrices - m_temp; k+=(int)sampleo){
        for (int i = 0; i < num_rows - m; i+=(int)sampleo) {
            for (int j = 0; j < num_cols - m; j+=(int)sampleo) {
                int temp_new_size = 0;
                pos[c] = calculate_distance_m(signal_array, i, j, k, m, num_rows, num_cols, num_matrices, distance_type, &temp_new_size, m_temp, plus_one);
                flattened_size += temp_new_size;
                ind_unique_values[c] = temp_new_size;
                c += 1;
            }
        }
    }
    // double* distances_flattened = (double*)malloc(flattened_size * sizeof(double));
    double* distances_flattened = (double*)malloc(size*(size-1) * sizeof(double));
    int co = 0;
    for(int i = 0; i < size; i++){
        // for(int j = 0; j < ind_unique_values[i]; j++){
        for(int j = 0; j < size-1; j++){
            distances_flattened[co] = pos[i][j];
            co += 1;
        }
    }
    
    for(int i = 0; i < size; i++){
        free(pos[i]);
    }
    free(pos);
    // int new_size;
    // double* unique_arr = remove_duplicates(distances_flattened, flattened_size, &new_size);
    // return calculate_standard_deviation(unique_arr, new_size);
    return calculate_standard_deviation(distances_flattened, size*(size-1));
}

double unique_values_std(double*** signal_array, int num_rows, int num_cols, int num_matrices){
    int size = num_rows*num_cols*num_matrices;
    double* values = (double*)malloc(size*sizeof(double));
    int c = 0;
    for(int k = 0; k < num_matrices; k++){
        for(int i = 0; i < num_rows; i++){
            for(int j = 0; j < num_cols; j++){
                values[c] = signal_array[k][i][j];
                c += 1;
            }
        }
    }
    return calculate_standard_deviation(values, size);
}
