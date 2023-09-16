#ifndef SIGNAL_STD_FUNCS_H
#define SIGNAL_STD_FUNCS_H

int compare(const void* a, const void* b);
double* remove_duplicates(double* arr, int size, int* new_size);
double calculate_standard_deviation(double* values, int size);

double distance(int m, double ***list_of_matrices, int i, int j, int k, int a, int b, int c, int distance_type);

double* calculate_distance_m(double*** signal_array, int i, int j, int k, int m, int num_rows, int num_cols, int num_matrices, int distance_type, int* temp_new_size);

double distance_m(double*** signal_array, int m, int num_rows, int num_cols, int num_matrices, int distance_type, double sampleo);
double unique_values_std(double*** signal_array, int num_rows, int num_cols, int num_matrices);

double distance_exp_den(int m, double ***list_of_matrices, int i, int j, int k, int a, int b, int c, int distance_type, int m_espacial, int dim_cubo);
double distance_exp_num(int m, double ***list_of_matrices, int i, int j, int k, int a, int b, int c, int distance_type, int m_espacial, int dim_cubo);

#endif