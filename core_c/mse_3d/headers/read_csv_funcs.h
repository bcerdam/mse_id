#ifndef READ_CSV_FUNCS_H
#define READ_CSV_FUNCS_H

double** read_csv(const char* file_path, int* rows, int* columns);
double*** data_structure(double** data_array, int num_matrices, int num_rows, int num_cols);

#endif