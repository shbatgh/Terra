import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import imageio.v2 as iio
from typing import List, Tuple, Dict
import math
import os
import re
import os, shutil
import numpy as np
import matplotlib.pyplot as plt
from cellpose import core, utils, io, models, metrics
from glob import glob
from Programs.AI_segmentation_sam import *


use_GPU = core.use_gpu()


# Import functions from the provided code
from Tracker import (
    load_outlines,
    get_centers,
    centers_to_dict,
    calculate_shift,
    calculate_average_shift,
    find_closest_centers
)

from ColorGenerator import *

class CellTrackingApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Cell Tracking App")
        self.geometry("1200x800")

        # Create main frame
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Create buttons
        self.button_frame = ctk.CTkFrame(self.main_frame)
        self.button_frame.pack(pady=10)

        self.load_model_button = ctk.CTkButton(self.button_frame, text="Load Model", command=self.load_model)
        self.load_model_button.pack(side=tk.LEFT, padx=5)

        self.load_folder_button = ctk.CTkButton(self.button_frame, text="Load Folder", command=self.load_folder)
        self.load_folder_button.pack(side=tk.LEFT, padx=5)

        self.process_button = ctk.CTkButton(self.button_frame, text="Process Image", command=self.process_image)
        self.process_button.pack(side=tk.LEFT, padx=5)

        self.calculate_centers_button = ctk.CTkButton(self.button_frame, text="Calculate Centers", command=self.centers_bs)
        self.calculate_centers_button.pack(side=tk.LEFT, padx=5)

        self.next_image_button = ctk.CTkButton(self.button_frame, text="Next Image", command=self.next_image)
        self.next_image_button.pack(side=tk.LEFT, padx=5)

        # Create label for current image
        self.image_label = ctk.CTkLabel(self.main_frame, text="No image loaded")
        self.image_label.pack(pady=5)

        # Create canvas for matplotlib figures
        self.figure, (self.ax1, self.ax2) = plt.subplots(ncols=2, figsize=(12, 4))
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.main_frame)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill=tk.BOTH, expand=True)

        self.img = None
        self.centers = None
        self.centers2 = None
        self.centers2 = None
        self.image_files = []
        self.current_image_index = -1
        self.path = ""  # Add this line to keep track of the folder path
        self.cells = None
        self.index = 0
        self.outlines_path = "New_Visualization_Step/AI_Segmentation_Output/seg_"
        self.model_path = ""
        self.model = None
        self.folder = ""
        self.output_dir = ""
        self.cell_color_mapping = []

    def extract_number(self, filename):
        match = re.search(r'\d+', filename)
        return int(match.group()) if match else float('inf')

    def load_model(self):
        self.model_path = filedialog.askopenfilename()
        self.output_dir = filedialog.askdirectory()
        
    def load_folder(self):
        file_path = filedialog.askopenfilename()
        self.folder = os.path.dirname(file_path)
        folder = self.folder
        last_folder = os.path.basename(os.path.normpath(folder))
        file_name = os.path.splitext(file_path)[0]
        self.outlines_path += last_folder + "/txt_outlines/"
        self.path = os.path.dirname(file_path)
        if self.path:
            self.image_files = [f for f in os.listdir(folder) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.tif', '.tiff'))]
            self.image_files.sort(key=self.extract_number)  # Sort the files by the numeric part of the filenames
            self.image_files = [os.path.join(folder, f) for f in self.image_files]
            self.current_image_index = -1
            self.next_image()
        
    def next_image(self):
        if self.image_files:
            self.current_image_index = (self.current_image_index + 1) % len(self.image_files)
            self.load_image(self.image_files[self.current_image_index])

        self.index += 1
        self.index = self.index % len(self.image_files)

    def load_image(self, file_path):
        self.img = iio.imread(file_path)
        self.display_image(self.img)
        # Update the image label with the current file name
        self.image_label.configure(text=f"Current image: {os.path.basename(file_path)}")

    def display_image(self, img):
        self.ax1.clear()
        self.ax2.clear()
        self.ax1.imshow(img, cmap='nipy_spectral')
        self.ax2.imshow(img, cmap='nipy_spectral')
        self.ax1.set_title('Original Image')
        self.ax2.set_title('Processed Image')
        self.canvas.draw()

    def process_image(self):
        channels = ["Green", "Red"]
        segmentation_parameters = [30, 0.3, 0]   
        folders = [self.folder]
        run_AI_segmentation_model(folders=folders,   #path to images
                                              model_path=self.model_path,     #path to model
                                              channels=channels,
                                              segmentation_parameters=segmentation_parameters,
                                              output_dir=self.output_dir)
        
    def centers_bs(self):
        if self.img is None:
            print("Please load an image first.")
            return
        cells1 = load_outlines(self.output_dir + "/seg_" + os.path.basename(self.folder) + "/txt_outlines/" + str(self.index) + "_cp_outlines.txt")
        cells2 = None

        if self.index == 1:
            cells2 = load_outlines(self.output_dir + "/seg_" + os.path.basename(self.folder) + "/txt_outlines/" + str(self.index) + "_cp_outlines.txt")
        else:
            cells2 = load_outlines(self.output_dir + "/seg_" + os.path.basename(self.folder) + "/txt_outlines/" + str(self.index - 1) + "_cp_outlines.txt")

        self.centers = get_centers(cells2)
        self.centers2 = get_centers(cells1)

        centers_dict = centers_to_dict(self.centers2)
        shifts = calculate_shift(self.centers, self.centers2)
        average_shift = calculate_average_shift(shifts)
        closest_centers_dict = find_closest_centers(self.centers, self.centers2, average_shift)
        centers2_dict = {i - 1: self.centers2[closest_center - 1] for i, closest_center in closest_centers_dict.items() if closest_center is not None}
        slice = {i: center for i, center in enumerate(self.centers2)}  # Use enumerate to ensure valid indices
         # Find the maximum index in centers2_dict
        max_index = max(centers2_dict.keys(), default=-1) + 1
        # Create a mapping from centers to cell outlines for cells1
        centers_to_cells1 = {tuple(get_centers([cell])[0]): cell for cell in cells1}
        # Create a set of indices that appear as values in closest_centers_dict
        used_indices = set(closest_center for closest_center in closest_centers_dict.values() if closest_center is not None)
        cells2_dict = {}
        # For centers that were matched in closest_centers_dict
        for i, closest_center in closest_centers_dict.items():
            if closest_center is not None:
                center = self.centers2[closest_center - 1]
                cells2_dict[i - 1] = centers_to_cells1[tuple(center)]

        # For centers that were not matched and added at the end of centers2_dict
        max_index = max(centers2_dict.keys(), default=-1) + 1
        used_indices = set(closest_center for closest_center in closest_centers_dict.values() if closest_center is not None)

        for i, center in enumerate(self.centers2):
            if i + 1 not in used_indices:
                cells2_dict[max_index] = centers_to_cells1[tuple(center)]
                max_index += 1

        print(f"Debug: len(self.centers) = {len(self.centers)}, len(self.centers2) = {len(self.centers2)}")
        print(f"Debug: closest_centers_dict before display_results = {closest_centers_dict}")

        #self.update_color_mapping(cells2_dict, closest_centers_dict)
        self.display_results(cells2_dict, self.centers2, closest_centers_dict)

    def process_image_old(self):
        if self.img is None:
            print("Please load an image first.")
            return

        cells1 = load_outlines(self.outlines_path + str(self.index) + "_cp_outlines.txt")
        cells2 = None
        if self.index == len(self.image_files) - 1:
            cells2 = load_outlines(self.outlines_path + str(self.index) + "_cp_outlines.txt")
        else:
            cells2 = load_outlines(self.outlines_path + str(self.index + 1) + "_cp_outlines.txt")

        self.centers = get_centers(cells1)
        self.centers2 = get_centers(cells2)

        centers_dict = centers_to_dict(self.centers2)
        shifts = calculate_shift(self.centers, self.centers2)
        average_shift = calculate_average_shift(shifts)
        closest_centers_dict = find_closest_centers(self.centers, self.centers2, average_shift)
        slice = {i: center for i, center in centers_dict.items()}

        # Add any additional values from centers2 if centers2 is larger than centers
        if len(self.centers2) > len(self.centers2):
            for i in range(len(self.centers) + 1, len(self.centers2) + 1):
                slice[i] = self.centers2[i - 1]

        self.display_results(slice, self.centers2, closest_centers_dict)

    def update_color_mapping(self, cells2_dict, closest_centers_dict):
        new_cells = set(cells2_dict.values()) - set(self.cell_color_mapping.values())
        random_colors = generate_unique_colors(new_cells)
        random_colors = {(color[0] / 255, color[1] / 255, color[2] / 255): coord for color, coord in random_colors.items()}
        # Assign new colors to new cells
        for i, cell_id in enumerate(new_cells):
            self.cell_color_mapping[cell_id] = list(random_colors.values())[i]
        
        # Update mapping for cells that have moved
        for old_id, new_id in closest_centers_dict.items():
            if new_id is not None and old_id - 1 in self.cell_color_mapping:
                self.cell_color_mapping[new_id - 1] = self.cell_color_mapping[old_id - 1]
                if old_id - 1 != new_id - 1:
                    del self.cell_color_mapping[old_id - 1]
    
    def display_results(self, centers_dict, centers2: List[Tuple[float, float]], closest_centers_dict: Dict[int, int]):
        self.ax1.clear()
        self.ax2.clear()

        self.ax1.imshow(self.img, cmap='nipy_spectral')
        self.ax2.imshow(self.img, cmap='nipy_spectral')

        colors = generate_unique_colors(centers2)
        diff = len(centers2) - len(self.cell_color_mapping)
        if diff > 0:
            self.cell_color_mapping.extend(list(colors.keys())[-diff:])
        colors = self.cell_color_mapping
        #colors = [(71, 46, 13), (56, 70, 83), (31, 146, 69), (131, 95, 230), (23, 218, 169), (150, 19, 187), (157, 9, 252), (8, 19, 23), (87, 39, 129), (72, 61, 208), (93, 21, 56), (50, 169, 66), (51, 195, 207), (52, 40, 143), (143, 144, 217), (14, 216, 203), (228, 199, 248), (22, 186, 174), (199, 65, 90), (24, 234, 158), (176, 127, 250), (4, 108, 99), (93, 41, 180), (110, 29, 172), (240, 10, 68), (25, 208, 2), (100, 107, 65), (67, 69, 148), (130, 98, 149), (80, 62, 78), (2, 153, 19), (185, 238, 174), (124, 158, 137), (222, 214, 159), (72, 218, 246), (55, 105, 187), (57, 7, 170), (148, 15, 15), (36, 20, 17), (81, 55, 114), (235, 72, 203), (248, 149, 183), (108, 56, 42), (167, 40, 13), (133, 243, 242), (248, 157, 135), (201, 188, 139), (124, 219, 33), (130, 100, 244), (227, 30, 218), (134, 138, 241), (222, 169, 38), (186, 240, 255), (129, 8, 140), (148, 218, 184), (105, 9, 51), (27, 187, 57), (231, 205, 103), (29, 170, 51), (41, 202, 148), (4, 125, 3), (8, 195, 119), (68, 60, 134), (202, 14, 10), (2, 12, 182), (129, 179, 227), (110, 114, 123), (16, 217, 136), (194, 30, 162), (38, 236, 94), (46, 142, 210), (76, 23, 185), (52, 197, 78), (56, 186, 108), (25, 224, 94), (161, 53, 43), (222, 126, 220), (96, 157, 176), (7, 232, 146), (60, 21, 135), (191, 180, 216), (175, 142, 60), (184, 139, 92), (0, 31, 122), (15, 43, 236), (32, 245, 18), (81, 33, 229), (245, 92, 23), (175, 145, 46), (134, 212, 241), (170, 245, 36), (138, 139, 130), (162, 125, 187), (35, 247, 18), (215, 102, 243), (20, 197, 21), (4, 90, 24), (211, 55, 95), (84, 91, 197), (204, 129, 236)]
        # Normalize colors to range 0 to 1
        #normalized_colors = {(color[0] / 255, color[1] / 255, color[2] / 255): coord for color, coord in colors.items()}
        #normalized_colors = [(r / 255, g / 255, b / 255) for r, g, b in colors]
        if len(colors) != 0:
            normalized_colors = [(r / 255, g / 255, b / 255) for r, g, b in colors]

        # Plot points on ax1
        for i, center in centers_dict.items():
            #color = list(normalized_colors.keys())[list(normalized_colors.values()).index(center)]
            color = normalized_colors[i]
            for point in center:
                self.ax1.plot(point[0], point[1], 'o', color=color, markersize=1)

        # Plot points on ax2
        for i, center in enumerate(centers2):
            #color = list(normalized_colors.keys())[list(normalized_colors.values()).index(center)]
            color = normalized_colors[i]
            self.ax2.plot(center[1], center[0], 'o', color=color, markersize=5)

        # Draw lines between corresponding points
        """for i, j in closest_centers_dict.items():
            if i < len(centers_dict) and j < len(centers2):
                center1 = centers_dict[i+1]
                center2 = centers2[j]
                self.ax2.plot([center1[1], center2[1]], [center1[0], center2[0]], 'r-', linewidth=0.5)"""

        self.ax1.set_title('Original Centers')
        self.ax2.set_title('Matched Centers')
        
        self.canvas.draw()

if __name__ == "__main__":
    app = CellTrackingApp()
    app.mainloop()