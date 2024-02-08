#ifndef UTILS_FUNCS_H
#define UTILS_FUNCS_H

double** coarse_graining(double** arr, int rows, int cols, int scale_factor);
double max_distance(int m, double **image, int i, int j, int a, int b, int distance_type);
double fuzzy_membership(double distance, double r, double delta);
float negative_logarithm(float um, float umplus1);

#endif