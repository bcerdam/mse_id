import numpy as np
import random
import cv2

def gen_weights():
    x_pos = [-2, -1, 0, 1, 2]
    y_pos = [-2, -1, 0, 1, 2]
    new_x = 0
    new_y = 0

    while np.abs(new_x) != 2 and np.abs(new_y) != 2:
        new_x = random.choice(x_pos)
        new_y = random.choice(y_pos)

    return [new_x, new_y]

def video(x, y, frames):
    positions = [[x, y]]
    current_pos = [x, y]
    c_frames = 0
    while c_frames != frames:
        next = gen_weights()
        current_pos[0] += next[0]
        current_pos[1] += next[1]
        if current_pos[0] >= 16 or current_pos[0] < 0 or current_pos[1] >= 16 or current_pos[1] < 0:
            current_pos[0] -= next[0]
            current_pos[1] -= next[1]
        else:
            positions.append([current_pos[0], current_pos[1]])
            c_frames += 1
    return positions

def create_video(positions):
    frames = []
    for x in positions:
        frame = np.zeros((16, 16), dtype=int)
        frame[x[0]][x[1]] = 255
        frames.append(frame)
    return frames

def create_grayscale_video(frames_list, output_file, fps=30):
    height, width = frames_list[0].shape
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_file, fourcc, fps, (width, height), isColor=False)

    for frame in frames_list:
        frame_uint8 = np.uint8(frame)  # Convert the frame to uint8 (8-bit grayscale)
        out.write(frame_uint8)

    out.release()
    return frames_list