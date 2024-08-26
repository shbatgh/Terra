"""
NEW MANUAL SEGMENTATION FORMATTER

This code converts the self segmented images to the output dictionary given:
    - Reference points
    - Path to timepoints
    - Colors on draw image (recursive and brute-force)

Assuming:
    - Timepoints are labeled    t1, t2, ...,    tn
    - Images are labeled        1,  2,  ...,    n


Notes:
Maybe check num_slices business

Have a clause that makes sure that the points checked in get_surrounding_colored_points isn't outside the boundary of the image
-

fix gap in wireframe



DID NOT TEST NEW METHOD YET
"""
import time
from PIL import Image
import sys
import os
import math

import large_group_sorter

sys.setrecursionlimit(1500)


def get_surrounding_colored_points(pix, point_coords, color):                       #returns dictionary: {[*x,y*]: (*color*), [*x,y*]: (*color*), [*x,y*]: (*color*)}
    coords1 = [point_coords[0] - 1, point_coords[1] - 1]
    coords2 = [point_coords[0] - 1, point_coords[1]]
    coords3 = [point_coords[0] - 1, point_coords[1] + 1]

    coords4 = [point_coords[0], point_coords[1] - 1]
    coords5 = [point_coords[0], point_coords[1] + 1]

    coords6 = [point_coords[0] + 1, point_coords[1] - 1]
    coords7 = [point_coords[0] + 1, point_coords[1]]
    coords8 = [point_coords[0] + 1, point_coords[1] + 1]

    

    coords_list = [coords1, coords2, coords3, coords4, coords5, coords6, coords7, coords8]
    surrounding_points = []

    for coord in coords_list:
        cur_x, cur_y = coord[0], coord[1]
        coord_color = pix[cur_x, cur_y][:3]
        if (coord_color == color):
            surrounding_points.append(coord)
    return(surrounding_points)


def create_outline_lists(pix, starting_point, color): #maybe still need checked_points clause
    final_point_list =[starting_point]
    queued_points = get_surrounding_colored_points(pix = pix,
                                                   point_coords=starting_point,
                                                   color = color)
    while len(queued_points) >0:
        temporary_list = []
        for q_point in queued_points:
            for pos_new_point in get_surrounding_colored_points(pix=pix, point_coords=q_point, color=color):
                if (pos_new_point not in temporary_list) and (pos_new_point not in final_point_list):
                    temporary_list.append(pos_new_point)
        queued_points = temporary_list

        final_point_list += queued_points
    return (final_point_list)




def group_cell_segmentations(pix, color, checked_points):
    color_groups = []
    for x in range(width):
        for y in range(height):
            if (pix[x,y][:3] == color) and ([x,y] not in checked_points):
                cur_group = create_outline_lists(pix=pix,
                                                 starting_point= [x,y],
                                                 color=color)
                color_groups.append(cur_group)
    return(color_groups)

def sortFn(coords):
    P_x, P_y = coords[0], coords[1]
    return(math.atan((P_y-center[1])/(P_x-center[0])))      #Returns angle made by the center, the point, and the x-axis (Adjusted to the center)

def split_group(group_lst, C_x):
    right_group = []
    left_group = []
    for point in group_lst:
        if point[0] > C_x:      #Anything to the right of the center point
            right_group.append(point)
        else:
            left_group.append(point)
    return(right_group, left_group)


def adjusted_group(group, reference_point):
    return([[coord[0]-reference_point[0], coord[1]-reference_point[1]] for coord in group])

#Remember to adjust to reference point
def group_large(pix, color, reference_point):         #Puts all pixels of a single color in a group, regards all pixels of that color as the same structure/cell
    group = []
    for x in range(width):
        for y in range(height):
            if pix[x,y][:3] == color:
                group.append([x,y])
    if sort and len(group) > 1:
        #group = large_group_sorter.sort_group(group)
        global center
        x_avg = sum([coord[0] for coord in group])/len(group)
        y_avg = sum([coord[1] for coord in group])/len(group)
        center = (x_avg +0.5, y_avg +0.5)       #Adjusting a tiny bit so that the arctan doesn't equal 0
        print(center)

        right_group, left_group = split_group(group_lst=group,
                                              C_x=center[0])
        
        right_group.sort(key=sortFn)
        #print(right_group)
        left_group.sort(key=sortFn)
        group = right_group + left_group

    return(adjusted_group(group =group,
                          reference_point = reference_point))


def format_slice(slice_path, reference_point):
    slice_dict = {}

    checked_points = []
    cur_img = Image.open(slice_path)
    pix = cur_img.load()


    for color in r_colors:
        slice_dict[color] = group_cell_segmentations(pix, color, reference_point, checked_points)
    for color in bf_colors:
        slice_dict[color] = [group_large(pix, color, reference_point)]
    return(slice_dict)

#Sample imgs: 'C:/Users/areil/Desktop/Germarium_Visualization/Images/Sample_Stacks/3-01.png'


def format_stack(timepoint, reference_point):                #timepoint is the path to the stack
    cur_path = timepoint_folders[timepoint]
    print("Formatting stack " + os.path.basename(os.path.normpath(cur_path)))       #takes last parts
    slice_images = [ f.path for f in os.scandir(cur_path) if f.is_file() ]
    
    n_slices = len(slice_images)                                        #Might raise an error

    stack_list=[]
    for slice_num in range(n_slices):          #slices are numbered 1 through n
        cur_slice = format_slice(slice_path=slice_images[slice_num],
                                 reference_point=reference_point)
        stack_list.append(cur_slice)
    return(stack_list)
        



def prepare_manual_data(path_to_timepoints, recursive_colors, brute_force_colors, reference_point_list, image_dimensions, sort_large_groups):
    start_manual_time = time.time()
    print("Preparing Manual Data")

    global r_colors, bf_colors, sort
    r_colors, bf_colors, sort = recursive_colors, brute_force_colors, sort_large_groups
    global width, height
    width, height = image_dimensions[0], image_dimensions[1]


    global timepoint_folders
    timepoint_folders = [f.path for f in os.scandir(path_to_timepoints) if f.is_dir()]
    n_timepoints = len(timepoint_folders)
    

    frame_dict = {}
    for tp_num in range(n_timepoints):
        cur_refp=reference_point_list[tp_num]       #Is [0,0] if no ref list was inputted

        cur_stack = format_stack(timepoint=tp_num,              
                                 reference_point=cur_refp)        #add to dict which houses stacks (frames)
        frame_dict[tp_num] = cur_stack

    manual_time_taken = time.time()-start_manual_time
    return(frame_dict, manual_time_taken)



#Testing stuff out
frame_dict, manual_time_taken = prepare_manual_data(path_to_timepoints='C:/Users/areil/Desktop/Terra/Unprocessed Animations/G6 tp1-3 for tests',
                                                    recursive_colors = [], 
                                                    brute_force_colors =[(0, 255, 0)], 
                                                    reference_point_list = [[111, 80], [100, 121], [103, 123]],
                                                    image_dimensions = [512, 512], 
                                                    sort_large_groups = True)

with open("C:/Users/areil/Desktop/Terra/Programs/Program Outputs/Test 8 G6 non-recursive manual formatted data.txt", 'w') as f:
    f.write(str(frame_dict))