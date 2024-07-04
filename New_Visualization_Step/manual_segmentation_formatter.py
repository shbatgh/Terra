"""
This code converts the self segmented images to the output dictionary given:
    - Reference point
    - Path to timepoints
    - Colors on draw image (recursive and brute-force)

Assuming:
    - Timepoints are labeled    t1, t2, ...,    tn
    - Images are labeled        1,  2,  ...,    n


Problem:
does not order large groups yet
    
Code is from v30group_segmentations_adjusted.py from Terra/Visualization folder
"""
import time
from PIL import Image
import sys

sys.setrecursionlimit(1500)



def get_surrounding_colored_points(pix, point_coords, color):                       #returns dictionary: {[*x,y*]: (*color*), [*x,y*]: (*color*), [*x,y*]: (*color*)}
    #check is color is in list or tuple form
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
        if coord_color == color:
            surrounding_points.append(coord)
            #print("Found surrounding point")
    return(surrounding_points)


def recursively_add_points(pix, point_list, point_coords, color, recursion_num, fin_p_list, reference_point, checked_points):
    if point_coords in point_list:
        return None
    #print("recursion:", recursion_num)
    point_list.append(point_coords)
    fin_p_list.append([point_coords[0]-reference_point[0], point_coords[1]-reference_point[1]])
    checked_points.append(point_coords)
    for surround_coords in get_surrounding_colored_points(pix, point_coords, color).copy():
        recursively_add_points(pix=pix,
                               point_list=point_list,
                               point_coords=surround_coords,
                               color=color,
                               recursion_num=recursion_num+1,
                               fin_p_list=fin_p_list,
                               reference_point=reference_point,
                               checked_points=checked_points)
    if recursion_num == 0:
        return(fin_p_list)


def group_cell_segmentations(pix, color, reference_point, checked_points):
    color_groups = []
    for x in range(width):
        for y in range(height):
            if (pix[x,y][:3] == color) and ([x,y] not in checked_points):
                cur_group = recursively_add_points(pix=pix,
                                                   point_list=[],
                                                   point_coords=[x,y],
                                                   color=color,
                                                   recursion_num=0,
                                                   fin_p_list=[],
                                                   reference_point=reference_point,
                                                   checked_points=checked_points)
                color_groups.append(cur_group)
    return(color_groups)


def group_large(pix, color, reference_point):         #Puts all pixels of a single color in a group, regards all pixels of that color as the same structure/cell
    group = []
    for x in range(width):
        for y in range(height):
            if pix[x,y][:3] == color:
                group.append([x-reference_point[0],y-reference_point[1]])
    return(group)


def format_slice(slice_path, reference_point):
    slice_dict = {}

    checked_points = []
    cur_img = Image.open(slice_path)
    pix = cur_img.load()


    for color in r_colors:
        slice_dict[color] = group_cell_segmentations(pix, color, reference_point, checked_points)
        print("color", color, "finished")
    for color in bf_colors:
        slice_dict[color] = [group_large(pix, color, reference_point)]
    return(slice_dict)

#Sample imgs: 'C:/Users/areil/Desktop/Germarium_Visualization/Images/Sample_Stacks/3-01.png'


def format_stack(timepoint, reference_point):                #timepoint is the path to the stack
    stack_list=[]
    for slice_num in range(n_slices):          #slices are numbered 1 through n
        cur_slice = format_slice(slice_path=tp_path+'/'+timepoint+'/'+str(slice_num)+p_end,
                                 reference_point=reference_point)
        stack_list.append(cur_slice)
        



def main(path_to_timepoints, recursive_colors, brute_force_colors, number_of_timepoints, number_of_slices, reference_point_list, path_end):
    start_manual_time = time.time()

    global tp_path, p_end
    tp_path, p_end = path_to_timepoints, path_end
    global r_colors, bf_colors
    r_colors, bf_colors = recursive_colors, brute_force_colors
    global n_slices
    n_timepoints, n_slices = number_of_timepoints, number_of_slices
    global width, height
    sample_img = Image.open(tp_path+'/t1/1.png')            #CHANGE IF MAKING THE IMAGE NAMES CHANGEABLE
    width, height = sample_img.size

    frame_dict = {}
    for tp_num in range(n_timepoints):
        cur_refp=reference_point_list[tp_num-1]
        cur_stack = format_stack(timepoint='t'+str(tp_num),              
                                 reference_point=cur_refp)        #add to dict which houses stacks (frames)
        frame_dict[tp_num] = cur_stack

    manual_time_taken = time.time()-start_manual_time
    return(frame_dict, manual_time_taken)

"""
def main(path):
    start_time = time.time()

    global stack_path
    global pix
    global grouped_segmentations
    global checked_points
    global reference_point
    global width
    global height

    segmented_stack = []
    
    stack_path = path
    sys.path.append(stack_path)
    img = Image.open(folder_name+'/'+stack_path+'/'+str(img_stack[0])+path_end)          #Make sure the same size???
    pix = img.load()

    width, height = img.size
    
    if reference_adjust:
        reference_point = find_reference_point()
        print("Reference point:", reference_point)

    for slice_num in img_stack:
        print("\n\nSlice:", slice_num)
        #print(path_start+'/'+stack_path+'/'+slice_num+path_end)
        
        grouped_segmentations = get_AI_groups(slice_num)
        checked_points = []
        img = Image.open(folder_name+'/'+stack_path+'/'+slice_num+path_end)
        pix = img.load()

        #format_data()
        segmented_stack.append(grouped_segmentations.copy())
        #print("slice", slice_num, "finished.")




    end_time = time.time()
    print("\nstack", stack_path, "runtime:", end_time-start_time)

    #with open('v20group_segmentations_adjusted output', 'w') as f:
        #f.write(str(segmented_stack))

    return(segmented_stack)

    """