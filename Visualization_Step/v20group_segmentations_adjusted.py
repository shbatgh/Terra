import time
from PIL import Image
import sys

sys.setrecursionlimit(1500)

"""
Grouped segmentations:
{                                                                                                       <-- Z_slice
    (*color*): [                                                                                        <-- certain color
        [[*x, y*], [*x, y*], [*x, y*], [*x, y*], [*x, y*]],                                             <-- grouped segmentation points for that color
        [[*x, y*], [*x, y*]] 
        [[*x, y*], [*x, y*], [*x, y*], [*x, y*], [*x, y*], [*x, y*]]
    ] 

    
    (*color2*): [
        [[*x, y*], [*x, y*], [*x, y*], [*x, y*], [*x, y*], [*x, y*], [*x, y*], [*x, y*], [*x, y*], [*x, y*]], 
        [[*x, y*], [*x, y*], [*x, y*], [*x, y*], [*x, y*]]
        [[*x, y*], [*x, y*], [*x, y*], [*x, y*]]
    ] 
}

"""

path_start = 'C:/Users/areil/Desktop/Germarium_Visualization/Images/Animation1'                         #'C:/Users/areil/Desktop/Germarium_Visualization/Images/Animation1'
stack_path = 't1'
path_end = '.png'

sys.path.append(stack_path)

img_stack = [str(i) for i in range(1,16)]   #[str(i) for i in range(1,16)]




img = Image.open(path_start+'/'+stack_path+'/'+str(img_stack[0])+path_end)          #Make sure the same size???
pix = img.load()

width, height = img.size


#(255, 0, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255)
recursive_colors = [(255, 0, 0), (0, 0, 255), (255, 0, 255), (0, 255, 255), (255, 255, 0), (255, 100, 0)]   #(255, 255, 0) was taken out.

brute_force_colors = [(0, 255, 0)]
reference_cell_color = (255, 255, 0)
reference_adjust = True         #False: no adjusting




def find_reference_point():
    for slice_num in img_stack:
        img = Image.open(path_start+'/'+stack_path+'/'+slice_num+path_end)
        pix = img.load()
        reference_cell_x = []
        reference_cell_y = []
        for x in range(width):
            for y in range(height):
                if (pix[x,y][:3] == reference_cell_color):
                    reference_cell_x.append(x)
                    reference_cell_y.append(y)
        if len(reference_cell_x) != 0:
            return([int(sum(reference_cell_x) / len(reference_cell_x)), int(sum(reference_cell_y) / len(reference_cell_y))])
    print("No Reference Cell Found!")
    return([0,0])


def get_surrounding_colored_points(point_coords, color):                       #returns dictionary: {[*x,y*]: (*color*), [*x,y*]: (*color*), [*x,y*]: (*color*)}
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


def recursively_add_points(point_list, point_coords, color, recursion_num, fin_p_list):
        #point_list and checked points are black-boxed, using fin_p_list
    if point_coords in point_list:
        return None
    #print("recursion:", recursion_num)
    point_list.append(point_coords)
    fin_p_list.append([point_coords[0]-reference_point[0], point_coords[1]-reference_point[1]])
    checked_points.append(point_coords)
    for surround_coords in get_surrounding_colored_points(point_coords, color).copy():
        recursively_add_points(point_list, surround_coords, color, recursion_num+1, fin_p_list)
    if recursion_num == 0:
        #print(color, "group done")     #when a group is finished
        #if reference_adjust:
        #    for i in range (len(point_list)):
         #       point_list[i][0] -= reference_point[0]
         #       point_list[i][1] -= reference_point[1]
         #   return(point_list)
        return(fin_p_list)


def group_cell_segmentations(color):
    color_groups = []
    for x in range(width):
        for y in range(height):
            if (pix[x,y][:3] == color) and ([x,y] not in checked_points):
                cur_group = recursively_add_points([], [x,y], color, 0, [])
                color_groups.append(cur_group)
    return(color_groups)


def group_large(color):         #Puts all pixels of a single color in a group, regards all pixels of that color as the same structure/cell
    group = []
    for x in range(width):
        for y in range(height):
            if pix[x,y][:3] == color:
                group.append([x-reference_point[0],y-reference_point[1]])
    return(group)


def format_data():
    global grouped_segmentations
    for color in recursive_colors:
        grouped_segmentations[color] = group_cell_segmentations(color)
        print("color", color, "finished")
    for color in brute_force_colors:
        grouped_segmentations[color] = [group_large(color)]

#Sample imgs: 'C:/Users/areil/Desktop/Germarium_Visualization/Images/Sample_Stacks/3-01.png'



grouped_segmentations = {}
checked_points = []

segmented_stack = []
reference_point = [0,0]



def main(path):
    global stack_path
    global pix
    global grouped_segmentations
    global checked_points
    global reference_point
    segmented_stack = []
    start_time = time.time()
    stack_path = path
    
    if reference_adjust:
        reference_point = find_reference_point()
        print("Reference point:", reference_point)

    for slice_num in img_stack:
        print("\n\nSlice:", slice_num)
        #print(path_start+'/'+stack_path+'/'+slice_num+path_end)
        
        grouped_segmentations = {}
        checked_points = []
        img = Image.open(path_start+'/'+stack_path+'/'+slice_num+path_end)
        pix = img.load()

        format_data()
        segmented_stack.append(grouped_segmentations.copy())
        #print("slice", slice_num, "finished.")




    end_time = time.time()
    print("\nstack", stack_path, "runtime:", end_time-start_time)

    #with open('v20group_segmentations_adjusted output', 'w') as f:
        #f.write(str(segmented_stack))

    return(segmented_stack)