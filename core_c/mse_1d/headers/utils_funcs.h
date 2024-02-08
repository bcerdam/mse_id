#ifndef UTILS_FUNCS_H
#define UTILS_FUNCS_H

double* coarse_graining(double* data, int num_entries, int scale);
double** mod_coarse_graining(double** data, int num_entries, int scale, int dim);
double fuzzy_membership(double distance, double r, double delta, double min, double max);

#endif