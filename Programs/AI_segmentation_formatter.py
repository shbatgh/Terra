"""
Notes:
Color map on x and y coords. Center of a cell determines the cell color. Regard it as the same cell based on centers. How will user fix any mistake?

Try applying AI segmentation on maunal segs, to get complete, sorted wireframes

Speed should be found in blender. Should be able to fix by making a segmentation a certain color.

"""
import time
from PIL import Image
import os

def add_to_dict(dict, color, group):
    if color in dict.keys():
        dict[color].append(group)
    else:
        dict[color] = [group]

def find_color(timepoint, coords, slice_num):           #Does not distinguish between frames
    img = Image.open(tp_path+'/seg_'+timepoint+'/outlines/'+str(slice_num+1)+'_outlines.png')        #e.g. tp_path/seg_t1/outlines/1_outlines.txt
    pix = img.load()
    color = pix[int(coords[0]),int(coords[1])][:3]
    return(color)

#def make_color()

def line_to_group(line, reference_point):
    group = [[int(line[i]) - reference_point[0], int(line[i+1])- reference_point[1]] for i in range(0, len(line), 2)]       #Adjusted to reference
    group+= [group[0], group[1], group[2]]                                              #Loops around so wireframes are complete
    return(group)

def get_slice_groups(timepoint, slice_num, reference_point):
    slice_dict = {}

    slice_txt_path = tp_path+'/seg_'+timepoint+'/txt_outlines/'+str(slice_num+1)+'_cp_outlines.txt'         #e.g. tp_path/seg_t1/txt_outlines/1_cp_outlines.txt
    if not os.path.isfile(slice_txt_path):
        return(slice_dict)

    f = open(slice_txt_path, "r")          #Groups come from segmentation data    
    for line in f:
        line = line.split(',')
        cur_group = line_to_group(line=line,
                                  reference_point=reference_point)
        cur_color = find_color(timepoint=timepoint,
                               coords=[line[0], line[1]],
                               slice_num=slice_num)
        add_to_dict(slice_dict, cur_color, cur_group)
    return(slice_dict)

def format_stack(timepoint, reference_point):
    print("Stack " + timepoint)
    stack_list=[]
    for slice_num in range(n_slices):          #slices are numbered 1 through n
        cur_slice = get_slice_groups(timepoint=timepoint,
                                     slice_num=slice_num,
                                     reference_point=reference_point)
        stack_list.append(cur_slice)
    return(stack_list)


n_slices = 15
#######--------------------------------------------------------------------------------------------------------------------------------------------------------------------------