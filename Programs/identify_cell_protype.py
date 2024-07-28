"""
IGNORE FOR NOW

Groups segmentations together by distances to centers.
Just for one stack



Every segmentation in bottom layer, see in next layer.


Function that finds centers in each slice. Dict form, [list of coords]: (center)
"""
import time
from PIL import Image
import os


def find_centers(outlines):
    pass


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
