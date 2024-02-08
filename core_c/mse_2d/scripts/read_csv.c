#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

double** read_csv(const char* filename) {
    double** data = NULL;
    FILE* file = fopen(filename, "r");
    char line[1024];
    int row_count = 0;
    int col_count = 0;
    
    if (file == NULL) {
        printf("Could not open file: %s\n", filename);
        return NULL;
    }
    
    // Count the number of rows and columns in the file
    while (fgets(line, 1024, file)) {
        col_count = 0;
        char* token = strtok(line, ",");
        while (token != NULL) {
            col_count++;
            token = strtok(NULL, ",");
        }
        row_count++;
    }
    
    // Allocate memory for the data array
    data = (double**)malloc(row_count * sizeof(double*));
    for (int i = 0; i < row_count; i++) {
        data[i] = (double*)malloc(col_count * sizeof(double));
    }
    
    // Reset the file pointer and read the data into the array
    fseek(file, 0, SEEK_SET);
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
    return data;
}