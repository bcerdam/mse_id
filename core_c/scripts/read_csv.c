#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h> 

double** read_csv(const char* file_path, int* rows, int* columns) {
    FILE* file = fopen(file_path, "r");
    if (file == NULL) {
        printf("Failed to open the CSV file.\n");
        return NULL;
    }

    // Determine the number of rows and columns
    char* line = NULL;
    size_t line_buffer_size = 0;
    *rows = 0;
    *columns = 0;
    ssize_t line_length;
    while ((line_length = getline(&line, &line_buffer_size, file)) != -1) {
        (*rows)++;
        if (*columns == 0) {
            char* token = strtok(line, ",");
            while (token != NULL) {
                (*columns)++;
                token = strtok(NULL, ",");
            }
        }
    }

    // Rewind the file to read from the beginning
    rewind(file);

    // Allocate memory for the row pointers
    double** array = (double**)malloc((*rows) * sizeof(double*));
    if (array == NULL) {
        printf("Failed to allocate memory.\n");
        return NULL;
    }

    // Allocate memory for the individual rows
    for (int i = 0; i < (*rows); i++) {
        array[i] = (double*)malloc((*columns) * sizeof(double));
        if (array[i] == NULL) {
            printf("Failed to allocate memory.\n");
            // Clean up the previously allocated memory
            for (int j = 0; j < i; j++) {
                free(array[j]);
            }
            free(array);
            free(line);  // Free the dynamically allocated line buffer
            return NULL;
        }
    }

    // Read the matrix values from the file
    int row = 0;
    while ((line_length = getline(&line, &line_buffer_size, file)) != -1 && row < (*rows)) {
        char* token = strtok(line, ",");
        int column = 0;
        while (token != NULL && column < (*columns)) {
            array[row][column] = atof(token);
            token = strtok(NULL, ",");
            column++;
        }
        if (column < (*columns)) {
            for (int i = column; i < (*columns); i++) {
                array[row][i] = 0.0;
            }
        }
        else if (token == NULL && column > 0) {
            for (int i = column; i < (*columns); i++) {
                array[row][i] = 0.0;
            }
        }
        row++;
    }

    fclose(file);
    free(line);  // Free the dynamically allocated line buffer

    return array;
}

double*** data_structure(double** data_array, int num_matrices, int num_rows, int num_cols){
    double*** signal_array = (double***)malloc(num_matrices * sizeof(double**));
    for(int i = 0; i < num_matrices; i++){
        double** row = (double**)malloc(num_rows * sizeof(double*));
        for(int j = 0; j < num_rows; j++){
            double* col = (double*)malloc(num_cols * sizeof(double));
            row[j] = col;
        }
        signal_array[i] = row;
    }

    for(int i = 0; i < num_matrices; i++){
        int r = 0;
        int c = 0;
        for(int j = 0; j < num_rows*num_cols; j++){
            signal_array[i][r][c] = data_array[i][j];
            c += 1;
            if(c == num_cols){
                c = 0;
                r += 1;
            }
        }
    }

    return signal_array;
}
