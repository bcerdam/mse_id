#ifndef UTILS_FUNCS_H
#define UTILS_FUNCS_H

double*** coarse_graining(double*** list_of_matrices, int num_matrices, int scale, int rows, int cols);
double fuzzy_membership(double distance, double r, double delta);
double window_distance(int m, double ***list_of_matrices, int i, int j, int k, int a, int b, int c, int distance_type);
double fuzzy_sinusoidal(double distance, double r, double delta);

#endif