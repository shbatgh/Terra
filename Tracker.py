import os
import shutil
import numpy as np
from cellpose import core, utils, io, models, metrics
from glob import glob
from natsort import natsorted
from typing import List, Tuple, Dict
import math
import matplotlib.pyplot as plt
import imageio.v2 as iio

def load_outlines(file_path: str) -> List[np.ndarray]:
    """
    Load outlines from a file.

    Parameters:
    file_path (str): Path to the file containing outlines.

    Returns:
    List[np.ndarray]: List of outlines as numpy arrays.
    """
    with open(file_path, 'r') as f:
        lines = f.readlines()

    cells = []
    for line in lines:
        # Split the line at semicolons, convert each pair to a list of integers
        cell = [list(map(int, pair.split(','))) for pair in line.strip().split(';')]
        # Convert the list of pairs to a numpy array and reshape it into pairs of coordinates
        cell = np.reshape(cell, (-1, 2))
        cells.append(cell)

    return cells

def get_centers(cells: List[np.ndarray]) -> List[Tuple[float, float]]:
    """
    Calculate the center of each cell.

    Parameters:
    cells (List[np.ndarray]): List of cells represented as numpy arrays.

    Returns:
    List[Tuple[float, float]]: List of centers as (x, y) tuples.
    """
    centers = []
    for i, arr in enumerate(cells):
        total = (0,0)
        count = 0
        for point in arr:
            total = tuple(map(sum, zip(total, (point[1], point[0]))))
            count += 1
        
        center = tuple(x/count for x in total)
        centers.append(center)

    return centers

def find_z_center(stack: List[Dict[int, Tuple[int, int]]], cell_id: int) -> Dict[int, int]:
    first_appearance = 0
    last_appearance = 0

    for slice in stack:
        for cell, point in slice.items():
            if cell == cell_id:
                if first_appearance == 0:
                    first_appearance = cell
                if last_appearance == 0:
                    last_appearance == cell

    z_center = (first_appearance + last_appearance) / 2
    return z_center

def centers_to_dict(centers: List[Tuple[float, float]]) -> Dict[int, Tuple[float, float]]:
    """
    Convert a list of centers to a dictionary with indices as keys.

    Parameters:
    centers (List[Tuple[float, float]]): List of centers.

    Returns:
    Dict[int, Tuple[float, float]]: Dictionary of centers with indices as keys.
    """
    return {i: center for i, center in enumerate(centers, start=1)}

def calculate_shift(centers: List[Tuple[float, float]], centers2: List[Tuple[float, float]]) -> List[Tuple[float, float]]:
    """
    Calculate the shift between two sets of centers.

    Parameters:
    centers (List[Tuple[float, float]]): List of original centers.
    centers2 (List[Tuple[float, float]]): List of new centers.

    Returns:
    List[Tuple[float, float]]: List of shifts as (shift_x, shift_y) tuples.
    """
    shifts = []
    for (x1, y1), (x2, y2) in zip(centers, centers2):
        shift_x = x2 - x1
        shift_y = y2 - y1
        shifts.append((shift_x, shift_y))

    # Taj Edit just to output shifts in a text file
    with open("C:/Users/areil/Desktop/Terra/Programs/Program Outputs/test5-A1 Sam shift list.txt", 'w') as f:
        f.write(str(shifts))

    return shifts

def calculate_average_shift(shifts: List[Tuple[float, float]]) -> Tuple[float, float]:
    """
    Calculate the average shift from a list of shifts.

    Parameters:
    shifts (List[Tuple[float, float]]): List of shifts.

    Returns:
    Tuple[float, float]: Average shift as (average_shift_x, average_shift_y).
    """
    total_shift_x = sum(shift[0] for shift in shifts)
    total_shift_y = sum(shift[1] for shift in shifts)
    average_shift_x = total_shift_x / len(shifts)
    average_shift_y = total_shift_y / len(shifts)
    return average_shift_x, average_shift_y

def find_closest_centers(centers: List[Tuple[float, float]], centers2: List[Tuple[float, float]], average_shift: Tuple[float, float]) -> Dict[int, int]:
    """
    Find the closest centers between two sets of centers considering an average shift.

    Parameters:
    centers (List[Tuple[float, float]]): List of original centers.
    centers2 (List[Tuple[float, float]]): List of new centers.
    average_shift (Tuple[float, float]): Average shift to apply to the new centers.

    Returns:
    Dict[int, int]: Dictionary mapping indices of centers2 to the closest indices of centers.
    """
    centers_dict = {i: center for i, center in enumerate(centers, start=1)}
    closest_centers_dict = {i: None for i in range(1, len(centers2) + 1)}
    assigned_centers = set()
    DISTANCE_THRESHOLD = 20  # pixels

    for i2, (x2, y2) in enumerate(centers2, start=1):
        x2_shifted = x2 - average_shift[0]
        y2_shifted = y2 - average_shift[1]
        closest_distance = math.inf
        closest_center = None

        for i1, (x1, y1) in centers_dict.items():
            if i1 in assigned_centers:
                continue
            distance = math.sqrt((x2_shifted - x1)**2 + (y2_shifted - y1)**2)
            if distance < closest_distance:
                closest_distance = distance
                closest_center = i1

        if closest_distance <= DISTANCE_THRESHOLD:
            closest_centers_dict[i2] = closest_center
            assigned_centers.add(closest_center)

    return closest_centers_dict

def display_images_side_by_side(img: np.ndarray, new_centers_dict: Dict[int, Tuple[float, float]], centers2: List[Tuple[float, float]]) -> None:
    """
    Display the images side by side with centers marked.

    Parameters:
    img (np.ndarray): The image to display.
    new_centers_dict (Dict[int, Tuple[float, float]]): Dictionary of new centers to plot.
    centers2 (List[Tuple[float, float]]): List of centers to plot.
    """
    fig, (ax1, ax2) = plt.subplots(ncols=2, figsize=(20, 6))

    # Plot new_centers_dict
    ax1.imshow(img, cmap='nipy_spectral')
    for center in new_centers_dict.values():
        ax1.plot(center[1], center[0], 'ro', markersize=2)  # 'ro' means red dots
    ax1.set_title('Image with new_centers_dict')

    # Plot centers2
    ax2.imshow(img, cmap='nipy_spectral')
    for center in centers2:
        ax2.plot(center[1], center[0], 'bo', markersize=2)  # 'bo' means blue dots
    ax2.set_title('Image with centers2')

    plt.show()