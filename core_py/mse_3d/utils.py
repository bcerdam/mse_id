import mpld3
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.cm import get_cmap

# Compile with:
# gcc -o core_c/executables/mse_3d core_c/scripts/mse_3d.c core_c/scripts/read_csv.c core_c/scripts/signal_std.c core_c/scripts/utils.c -lm -fopenmp -Icore_c/headers
# clang -Xclang -fopenmp -I/usr/local/opt/libomp/include -L/opt/homebrew/Cellar/libomp/16.0.6/lib -lomp -Icore_c/headers core_c/scripts/mse_3d.c core_c/scripts/read_csv.c core_c/scripts/signal_std.c core_c/scripts/utils.c -o core_c/executables/mse_3d_p

'''
plot_arrays(): Plots the arrays that mse_3d returns.
parameters:
    - data_list: List containing the arrays that mse_3d returns.
    - title: self explanatory.
    - xlabel: label of x axis.
    - ylabel: label of y axis.
    - legends: List of strings containing the names of the arrays.
    - save_path: Path where it saves a .html that contains the plot, if no path is given, then nothing is saved.
    - markers: self explanatory.
    - fig_size: self explanatory.
'''
def plot_arrays(data_list, title='', xlabel='', ylabel='', legends=None, save_path=None, markers=True, figsize=(16, 12)):
    fig, ax = plt.subplots(figsize=figsize)
    plt.grid('black')
    ax.set_facecolor('lightgrey')

    # Get a colormap with enough colors for the lines
    cmap = get_cmap('Set2')
    colors = cmap(np.linspace(0, 1, len(data_list)))

    for i, data_tuple in enumerate(data_list):
        name, data = data_tuple
        if legends is not None and len(legends) == len(data_list):
            label = legends[i]
        else:
            label = name
        if markers == True:
            plt.plot(data, color=colors[i], marker='v', markersize=5, label=label, markeredgecolor='black')
        else:
            plt.plot(data, color=colors[i], label=label)


    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()

    if save_path == None:
        plt.show()
    else:
        html_fig = mpld3.fig_to_html(plt.gcf())  # Get HTML representation of the figure
        with open(save_path, 'w') as file:
            file.write(html_fig)