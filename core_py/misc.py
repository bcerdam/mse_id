import numpy as np
import random
import cv2

def gen_weights(r, method, res, x_prob, y_prob):
    new_x = 0
    new_y = 0
    if method == 'SEMI_RANDOM':
        weight_range = [x for x in range(-r, r + 1)]
        while np.abs(new_x) != r and np.abs(new_y) != r:
            new_x = random.choice(weight_range)
            new_y = random.choice(weight_range)
    elif method == 'RANDOM':
        weight_range = [x for x in range(-res, res + 1)]
        new_x = random.choice(weight_range)
        new_y = random.choice(weight_range)
    elif method == 'SEMI_RANDOM_CORR':
        weight_range = [x for x in range(-r, r + 1)]
        x_pos_prob_range = [x_prob/r for x in range(1, r+1)]
        x_neg_prog_range = [(1-x_prob)/r for x in range(-r, 0)]
        x_prob_range = x_neg_prog_range+[0]+x_pos_prob_range
        y_pos_prob_range = [y_prob/r for x in range(1, r + 1)]
        y_neg_prog_range = [(1-y_prob) / r for x in range(-r, 0)]
        y_prob_range = y_neg_prog_range + [0] + y_pos_prob_range
        while np.abs(new_x) != r and np.abs(new_y) != r:
            new_x = random.choices(weight_range, weights=x_prob_range)[0]
            new_y = random.choices(weight_range, weights=y_prob_range)[0]
    return [new_x, new_y]

def video(x, y, frames, r, res, size_bolita, method, x_prob, y_prob):
    diff = np.ceil((size_bolita[0]/2))
    positions = [[x, y]]
    current_pos = [x, y]
    c_frames = 0
    while c_frames != frames:
        next = gen_weights(r, method, res, x_prob, y_prob)
        current_pos[0] += next[0]
        current_pos[1] += next[1]
        if current_pos[0] >= ((res-1)-(diff-1)) or current_pos[0] <= (0+(diff-1)) or current_pos[1] >= ((res-1)-(diff-1)) or current_pos[1] <= (0+(diff-1)):
            current_pos[0] -= next[0]
            current_pos[1] -= next[1]
        else:
            positions.append([current_pos[0], current_pos[1]])
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

def create_grayscale_video(frames_list, output_file, fps=60):
    height, width = frames_list[0].shape
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_file, fourcc, fps, (width, height), isColor=False)

    for frame in frames_list:
        frame_uint8 = np.uint8(frame)  # Convert the frame to uint8 (8-bit grayscale)
        out.write(frame_uint8)

    out.release()
    return frames_list


def gen_video(r, size_bolita, method='SEMI_RANDOM', columna_prob=0.5, fila_prob=0.5, frames_res=(50, 50), starting_pos=(25, 25), frames_no=500, save_path='test.mp4'):
    pos = video(starting_pos[0], starting_pos[1], frames_no, r, frames_res[0], size_bolita, method, columna_prob, fila_prob)
    pos_fill = create_video(pos, frames_res[0], size_bolita)
    create_grayscale_video(pos_fill, save_path)

gen_video(2, (1, 1), method='SEMI_RANDOM_CORR', columna_prob=0.4, fila_prob=0.5)