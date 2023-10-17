import numpy as np
import random
import cv2

def gen_weights(r, method, res, x_prob, y_prob, corr, weights_anteriores, sentido):
    new_x = 0
    new_y = 0
    if method == 'SEMI_RANDOM':
        weight_range = [x for x in range(-r, r + 1)]
        new_x = random.choice(weight_range)
        new_y = random.choice(weight_range)
    elif method == 'RANDOM':
        weight_range = [x for x in range(-res, res + 1)]
        new_x = random.choice(weight_range)
        new_y = random.choice(weight_range)
    elif method == 'SEMI_RANDOM_W':
        weight_range = [x for x in range(-r, r + 1)]
        x_pos_prob_range = [x_prob/r for x in range(1, r+1)]
        x_neg_prog_range = [(1-x_prob)/r for x in range(-r, 1)]
        x_prob_range = x_neg_prog_range+x_pos_prob_range
        # x_prob_range = x_neg_prog_range+[0]+x_pos_prob_range
        y_pos_prob_range = [y_prob/r for x in range(1, r + 1)]
        y_neg_prog_range = [(1-y_prob) / r for x in range(-r, 1)]
        # y_prob_range = y_neg_prog_range + [0] + y_pos_prob_range
        y_prob_range = y_neg_prog_range+y_pos_prob_range
        # while np.abs(new_x) != r and np.abs(new_y) != r:
        new_x = random.choices(weight_range, weights=x_prob_range)[0]
        new_y = random.choices(weight_range, weights=y_prob_range)[0]
    elif method == 'SEMI_RANDOM_CORR':
        weight_range = [x for x in range(-r, r + 1)]

        x_pos_prob_range = [corr / r for x in range(1, r + 1)]
        x_neg_prog_range = [(1 - corr) / (r+1) for x in range(-r, 1)]
        x_pos_range = x_neg_prog_range + x_pos_prob_range
        x_neg_range = x_pos_prob_range + x_neg_prog_range

        y_pos_prob_range = [corr / r for x in range(1, r + 1)]
        y_neg_prog_range = [(1 - corr) / (r + 1) for x in range(-r, 1)]
        y_pos_range = y_neg_prog_range + y_pos_prob_range
        y_neg_range = y_pos_prob_range + y_neg_prog_range

        if weights_anteriores[0] > 0:
            new_x = random.choices(weight_range, weights=x_pos_range)[0]
        elif weights_anteriores[0] <= 0:
            new_x = random.choices(weight_range, weights=x_neg_range)[0]

        if weights_anteriores[1] > 0:
            new_y = random.choices(weight_range, weights=y_pos_range)[0]
        elif weights_anteriores[1] <= 0:
            new_y = random.choices(weight_range, weights=y_neg_range)[0]

    elif method == 'LINE':
        new_x = (r*sentido)
        new_y = 0

    return [new_x, new_y]

def video(x, y, frames, r, res, size_bolita, method, x_prob, y_prob, corr):
    diff = np.ceil((size_bolita[0]/2))
    positions = [[x, y]]
    current_pos = [x, y]
    weights_anteriores = [0, 0]
    c_frames = 0
    sentido = 1
    while c_frames != frames:
        next = gen_weights(r, method, res, x_prob, y_prob, corr, weights_anteriores, sentido)
        current_pos[0] += next[0]
        current_pos[1] += next[1]
        if current_pos[0] >= ((res-1)-(diff-1)) or current_pos[0] <= (0+(diff-1)) or current_pos[1] >= ((res-1)-(diff-1)) or current_pos[1] <= (0+(diff-1)):
            current_pos[0] -= next[0]
            current_pos[1] -= next[1]
            sentido *= -1
        else:
            weights_anteriores = next
            positions.append([current_pos[1], current_pos[0]])
            c_frames += 1
    return positions

def create_video(positions, res, size_bolita):
    frames = []
    for x in positions:
        start_pos_x = x[0] - (np.ceil(size_bolita[0]/2)-1)
        start_pos_y = x[1] + (np.ceil(size_bolita[0]/2)-1)
        frame = np.zeros((res, res), dtype=int)
        for i in range(size_bolita[0]):
            for j in range(size_bolita[1]):
                frame[int(start_pos_x+i)][int(start_pos_y-j)] = 255
        frames.append(frame)
    return frames

def create_grayscale_video(frames_list, output_file, fps=24):
    height, width = frames_list[0].shape
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_file, fourcc, fps, (width, height), isColor=False)
    c = 0

    for frame in frames_list:
        frame_uint8 = np.uint8(frame)  # Convert the frame to uint8 (8-bit grayscale)
        out.write(frame_uint8)
        c+=1

    out.release()
    return frames_list


def gen_video(r, size_bolita, method='SEMI_RANDOM', corr=0.5, columna_prob=0.5, fila_prob=0.5, frames_res=(50, 50), starting_pos=(25, 25), frames_no=500, save_path='test.mp4'):
    pos = video(starting_pos[0], starting_pos[1], frames_no, r, frames_res[0], size_bolita, method, columna_prob, fila_prob, corr)
    pos_fill = create_video(pos, frames_res[0], size_bolita)
    return pos
    # return create_grayscale_video(pos_fill, save_path)

def video_csv(frame_list, save_path):
    flattened_list = []
    for frame in frame_list:
        flattened_list.append(frame.flatten())
    flattened_array = np.vstack(flattened_list)
    np.savetxt(save_path, flattened_array, delimiter=',')

# Videos de prueba

# line = gen_video(1, (3, 3), method='LINE', frames_res=(30, 30), starting_pos=(15, 15), frames_no=29999)
# random_v = gen_video(1, (3, 3), method='RANDOM', frames_res=(30, 30), starting_pos=(15, 15), frames_no=29999)
# semi_random = gen_video(3, (3, 3), method='SEMI_RANDOM', frames_res=(30, 30), starting_pos=(15, 15), frames_no=29999)
# semi_random_pos_corr = gen_video(3, (3, 3), method='SEMI_RANDOM_CORR', corr=0.6,
#                                  frames_res=(30, 30), starting_pos=(15, 15), frames_no=29999)
# semi_random_neg_corr = gen_video(3, (3, 3), method='SEMI_RANDOM_CORR', corr=0.3,
#                                  frames_res=(30, 30), starting_pos=(15, 15), frames_no=29999)

# Codigo para video FLASHES

# v = list(np.genfromtxt('tiempos.csv', delimiter=','))
# # time_points = [x[1] for x in v[1:]][:60]
# time_points = [x[1] for x in v[1:]]
#
# width, height = 100, 100  # Video frame dimensions
# # duration_ms = 15300  # Total duration in milliseconds (e.g., 10 seconds)
# duration_ms = np.round(time_points[-1]).astype(int)
# total_frames = duration_ms
#
# frames = np.zeros((total_frames, height, width, 3), dtype=np.uint8)
#
# for i in range(1, len(time_points), 2):
#     start_ms = time_points[i - 1]
#     end_ms = time_points[i]
#     diff_ms = end_ms - start_ms
#
#     if diff_ms < 10:
#         print('YES')
#     # if diff_ms == 10:
#     #     start_frame = int(start_ms / 1)
#     #     end_frame = int(end_ms / 1)
#     #     # for frame_idx in range(start_frame, end_frame):
#     #     #     frames[frame_idx] = (255, 255, 255)  # White frame
#     #     frames[start_frame:end_frame] = (255, 255, 255)  # Set all frames in the range to white
#     start_frame = int(start_ms / 1)
#     end_frame = int(end_ms / 1)
#     frames[start_frame:end_frame] = (255, 255, 255)
#
# frames = frames[::10]
# # #
# output_video = cv2.VideoWriter('output_video.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 100, (width, height))
# for frame in frames:
#     output_video.write(frame)
# output_video.release()

import csv

def combine_csvs(file1_path, file2_path):
    data1 = []
    data2 = []

    # Read data from the first CSV file
    with open(file1_path, 'r') as file1:
        csv_reader = csv.reader(file1)
        for row in csv_reader:
            data1.append(row)

    # Read data from the second CSV file
    with open(file2_path, 'r') as file2:
        csv_reader = csv.reader(file2)
        for row in csv_reader:
            data2.append(row)

    # Ensure both lists have the same length
    min_length = min(len(data1), len(data2))

    # Combine the data into a list of lists
    combined_data = []
    for i in range(min_length):
        combined_data.append( [ int(data1[i][0]*10), int(data2[i][0]*10) ] )
        # combined_data.append([data1[i][0], data2[i][0]])


    return combined_data

# Example usage:
file1_path = '/Users/brunocerdamardini/Desktop/repo/c_mse_3D/Datos/brownian/fbm_x_02.csv'  # Replace with the path to your first CSV
file2_path = '/Users/brunocerdamardini/Desktop/repo/c_mse_3D/Datos/brownian/fbm_y_02.csv'  # Replace with the path to your second CSV
result = combine_csvs(file1_path, file2_path)

x = np.genfromtxt('/Users/brunocerdamardini/Desktop/repo/c_mse_3D/Datos/brownian/fbm_x_02.csv', delimiter=',')
print(x.max(), x.min())

y = np.genfromtxt('/Users/brunocerdamardini/Desktop/repo/c_mse_3D/Datos/brownian/fbm_y_02.csv', delimiter=',')
print(y.max(), y.min())

