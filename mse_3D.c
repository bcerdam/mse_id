#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <dirent.h>

#include <dirent.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int cmp_string(const void* a, const void* b) {
    const char** ia = (const char**)a;
    const char** ib = (const char**)b;
    return strcmp(*ia, *ib);
}

double*** read_csv(const char* folder_path, int num_files, int rows, int cols) {
    double*** data_array = (double***)malloc(num_files * sizeof(double**));

    // Iterate through all files in the folder
    DIR* dir;
    struct dirent* ent;
    if ((dir = opendir(folder_path)) != NULL) {
        int file_count = 0;
        char** file_names = (char**)malloc(num_files * sizeof(char*));
        while ((ent = readdir(dir)) != NULL) {
            // Only process CSV files
            if (strstr(ent->d_name, ".csv") != NULL) {
                file_names[file_count] = strdup(ent->d_name);
                file_count++;
            }
        }
        closedir(dir);

        qsort(file_names, file_count, sizeof(char*), cmp_string);

        for (int i = 0; i < file_count; i++) {
            char file_path[1024];
            snprintf(file_path, sizeof(file_path), "%s/%s", folder_path, file_names[i]);
            FILE* file = fopen(file_path, "r");
            if (file == NULL) {
                printf("Could not open file: %s\n", file_path);
                return NULL;
            }
            char line[1024];

            // Allocate memory for the data array
            double** data = (double**)malloc(rows * sizeof(double*));
            for (int i = 0; i < rows; i++) {
                data[i] = (double*)malloc(cols * sizeof(double));
            }

            // Read the data into the array
            int row = 0;
            while (fgets(line, 1024, file)) {
                int col = 0;
                char* token = strtok(line, ",");
                while (token != NULL) {
                    data[row][col] = atof(token);
                    col++;
                    token = strtok(NULL, ",");
                }
                row++;
            }
            fclose(file);
            data_array[i] = data;
        }

        for (int i = 0; i < file_count; i++) {
            free(file_names[i]);
        }
        free(file_names);

    } else {
        printf("Could not open folder: %s\n", folder_path);
        return NULL;
    }
    return data_array;
}


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

double fuzzy_membership(double distance, double r, int n, double delta) {
    if (r == 0){
        return 1;
    }
    else{
        return expf(powf(distance, 2.0) * log(delta) / powf(r, 2.0));
    }
}

double max_distance(int m, double ***list_of_matrices, int i, int j, int k, int a, int b, int c) {
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

float calculate_U_ij_m(double ***list_of_matrices, int i, int j, int k, int m, double r, int H, int W, int T, int n, double delta, int fuzzy) {
    double count = 0;
    int N_m = (H - m) * (W - m) * (T - m);
    for (int c = 0; c < T - m; c++){
        for (int a = 0; a < H - m; a++) {
            for (int b = 0; b < W - m; b++) {
                double dist = max_distance(m, list_of_matrices, i, j, k, a, b, c);
                if (a == i && b == j && c == k) {
                    continue;
                }
                else {
                    if (fuzzy == 0){
                        if (dist <= r){
                            count ++;
                        }
                    }
                    else if (fuzzy == 1){
                        count += fuzzy_membership(dist, r, n, delta);
                    }
                }
            }
        }
    }
    return (float) count / (N_m-1);
}

float calculate_U_ij_m_plus_one(double ***list_of_matrices, int i, int j, int k, int m, double r, int H, int W, int T, int n, double delta, int fuzzy) {
    double count = 0;
    int N_m = (H - m) * (W - m) * (T - m);
    for (int c = 0; c < T - m; c++){
        for (int a = 0; a < H - m; a++) {
            for (int b = 0; b < W - m; b++) {
                double dist = max_distance(m+1, list_of_matrices, i, j, k, a, b, c);
                if (a == i && b == j && c == k) {
                    continue;
                }
                else {
                    if (fuzzy == 0){
                        if (dist <= r){
                            count ++;
                        }
                    }
                    else if (fuzzy == 1){
                        count += fuzzy_membership(dist, r, n, delta);
                    }
                }
            }
        }
    }
    return (float) count / (N_m-1);
}

float calculate_U_m(double ***list_of_matrices, int m, double r, int H, int W, int T, int n, double delta, int fuzzy) {
    double sum = 0.0;
    for (int k = 0; k < T - m; k++){
        for (int i = 0; i < H - m; i++) {
            for (int j = 0; j < W - m; j++) {
                sum += calculate_U_ij_m(list_of_matrices, i, j, k, m, r, H, W, T, n, delta, fuzzy);
            }
        }
    }
    return sum / ((H - m) * (W - m) * (T - m));
}

float calculate_U_m_plus_one(double ***list_of_matrices, int m, double r, int H, int W, int T, int n, double delta, int fuzzy) {
    double sum = 0.0;
    for (int k = 0; k < T - m; k++){
        for (int i = 0; i < H - m; i++) {
            for (int j = 0; j < W - m; j++) {
                sum += calculate_U_ij_m_plus_one(list_of_matrices, i, j, k, m, r, H, W, T, n, delta, fuzzy);
            }
        }
    }
    return sum / ((H - m) * (W - m) * (T - m));
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

int main(int argc, char *argv[]) {

    char* file_path = argv[1];
    int num_files = atoi(argv[2]);
    int scales = atoi(argv[3]);
    int rows = atoi(argv[4]);
    int cols = atoi(argv[5]);
    int m = atoi(argv[6]);
    double r = atof(argv[7]);
    int n = atoi(argv[8]);
    double delta = atof(argv[9]);
    int fuzzy = atoi(argv[10]);

    double*** list_of_matrices = read_csv(file_path, num_files, rows, cols);
    double* n_values = malloc(scales * sizeof(double));

    for (int i = 1; i <= scales; i++) {
        double*** coarse_data = coarse_graining(list_of_matrices, num_files, i, rows, cols);
        float U_m = calculate_U_m(coarse_data, m ,r, cols, rows, num_files/i, n, delta, fuzzy);
        float U_m_plus_one = calculate_U_m_plus_one(coarse_data, m, r, cols, rows, num_files/i, n, delta, fuzzy);
        float n = negative_logarithm(U_m, U_m_plus_one);
        n_values[i-1] = n;
    }

    for (int i = 0; i < scales; i++) {
        printf("%f ", n_values[i]);
    }
    printf("\n");

    // double*** coarse_data = coarse_graining(list_of_matrices, num_files, scales, rows, cols);
    // for (int i = 0; i < num_files/scales; i++) {
    //     printf("Matrix %d:\n", i+1);
    //     for (int j = 0; j < rows; j++) {
    //         for (int k = 0; k < cols; k++) {
    //             printf("%lf ", coarse_data[i][j][k]);
    //         }
    //         printf("\n");
    //     }
    //     printf("\n");
    // }

    return 0;
}

/*
gcc mse_3D.c -o mse_3D -lm
./mse_3D
*/