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

# Import functions from the provided code
from Tracker import (
    load_outlines,
    get_centers,
    centers_to_dict,
    calculate_shift,
    calculate_average_shift,
    find_closest_centers
)

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

        self.load_folder_button = ctk.CTkButton(self.button_frame, text="Load Folder", command=self.load_folder)
        self.load_folder_button.pack(side=tk.LEFT, padx=5)

        self.process_button = ctk.CTkButton(self.button_frame, text="Process Image", command=self.process_image)
        self.process_button.pack(side=tk.LEFT, padx=5)

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

    def extract_number(self, filename):
        match = re.search(r'\d+', filename)
        return int(match.group()) if match else float('inf')

    def load_folder(self):
        folder = filedialog.askdirectory()
        last_folder = os.path.basename(os.path.normpath(folder))
        file_path = filedialog.askopenfilename()
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

    def display_results(self, centers_dict: Dict[int, Tuple[float, float]], centers2: List[Tuple[float, float]], closest_centers_dict: Dict[int, int]):
        self.ax1.clear()
        self.ax2.clear()

        self.ax1.imshow(self.img, cmap='nipy_spectral')
        self.ax2.imshow(self.img, cmap='nipy_spectral')

        for center in centers_dict.values():
            self.ax1.plot(center[1], center[0], 'ro', markersize=1)

        for center in centers2:
            self.ax2.plot(center[1], center[0], 'bo', markersize=1)

        self.ax1.set_title('Original Centers')
        self.ax2.set_title('New Centers with Tracking')
        self.canvas.draw()

if __name__ == "__main__":
    app = CellTrackingApp()
    app.mainloop()