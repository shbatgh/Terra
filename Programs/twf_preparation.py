"""
This formats the data for the triple_wireframe program.
The triple_wireframe program takes data for a single cell/cyst object in the following format:
[
[[x, y], [x, y], [x, y], ...],      <--this is a slice
[[x, y], [x, y], [x, y], ...],
[[x, y], [x, y], [x, y], ...],
...
]


Each timepoint currently has the following format:
[
{(R,G,B): [group1, group2, ....]}       --> {(R,G,B): [[[x,y],[x,y],[x,y],..], [[x,y],[x,y],[x,y],..], ... ]},           <--- slice
{(R,G,B): [group1, group2, ....]}       --> {(R,G,B): [[[x,y],[x,y],[x,y],..], [[x,y],[x,y],[x,y],..], ... ]},
....
]
"""

import ast
import math
import triple_wireframe

import copy


cell_count = 0
cells = []


class Cell:         #Cell class
    def __init__(self, id, starting_slice, initial_outline, c_color):
        self.id = id
        self.color = c_color

        self.starting_slice = starting_slice
        self.top_slice = starting_slice

        self.centers = [find_center(initial_outline)]
        self.outlines = [initial_outline]
        

        global cell_count, cells
        cell_count +=1
        cells.append(self)
    
    def add_outline(self, new_outline):
        self.top_slice +=1
        self.outlines.append(new_outline)
        self.centers.append(find_center(new_outline))







def find_center(point_list):                 #Finds the center of a outline
    length = len(point_list)
    if length == 0:
        return(None)
    
    x_sum, y_sum = 0, 0
    for [x, y] in point_list:
        x_sum +=x
        y_sum +=y
    return((x_sum/length, y_sum/length))

def approx_width(point_list, x_or_y):
    comp = 0
    if x_or_y =="y":
        comp = 1
    res_min = point_list[0][comp]
    res_max = point_list[1][comp]
    for p in point_list:
        val = p[comp]
        if val < res_min:
            res_min = val
        elif val > res_max:
            res_max = val
    return(res_max - res_min)
    

def find_segs(slice_dict, color):            #Finds all segmentations of a certain color on a slice
    if color not in slice_dict.keys():
        return([])
    return(slice_dict[color].copy())

def matchedSortFn(e):
    return(e[1])

def match_cells(cur_cells, prev_cells):      #Matches up all combinations between cells in the slice above and below. Sorts by the distance between centers.
    
    matched_list = []                        #Each element is 2 paired cells. Each element has the format: [{center1: outline1, center2: outline2}, distance]
    for cur_c in cur_cells:
        cur_center = find_center(cur_c)
        for prev_c in prev_cells:
            prev_center = find_center(prev_c)
            matched_list.append([{cur_center: cur_c, prev_center: prev_c}, math.dist(cur_center, prev_center)])
    matched_list.sort(key = matchedSortFn)
    return(matched_list)


def remove_pairs(matched_list, center):                    #Removes all elements in a list that have an outline with the following center
    new_matched_list = []
    for pair in matched_list:
        if (center not in pair[0].keys()):                 #Creates new list, only adds elements that do not have the center.
            new_matched_list.append(pair)
    return(new_matched_list)

def find_max_error(point_list1, point_list2):              #Finds the maximum error a cell can change position in different slices to still be considered the same cell.
    approx_r1 = (approx_width(point_list1, "x") + approx_width(point_list1, "y"))/2         #Approximates the radius to do this.
    approx_r2 = (approx_width(point_list2, "x") + approx_width(point_list2, "y"))/2
    result = max(approx_r1, approx_r2) * 0.5      #Change this multiplier. Smaller for tighter ranges to classify two segs as the same cell.
    return(result)

def appears_before(matched_list, center, loc):
    found = False
    for e in matched_list[:loc]:
        if center in e[0].keys():
            found = True
            break
    return(found)

def tag_centers(matched_list, center, starting_idx):
    tagged = []
    for cur_idx in range(starting_idx, len(matched_list)):
        pair = matched_list[cur_idx]
        c_centers = list(pair[0].keys()).copy()
        if center in c_centers:
            c_centers.remove(center)
            center_pos_tag = c_centers[0]
            if not appears_before(matched_list=matched_list, center=center_pos_tag, loc=cur_idx):
                tagged.append(center_pos_tag)
    return(tagged)


def filter_pairs(matched_list):
    filtered = []
    idx = 0
    while idx < len(matched_list):
        filtered.append(matched_list[idx])

        paired_centers = list(matched_list[idx][0].keys())
        tagged = [paired_centers[0], paired_centers[1]]
        tagged += tag_centers(matched_list=matched_list, center=paired_centers[0], starting_idx=idx+1)
        tagged += tag_centers(matched_list=matched_list, center=paired_centers[1], starting_idx=idx+1)

        for center in tagged:
            matched_list = remove_pairs(matched_list = matched_list, center=center)
    new_filtered = []
    for pair in filtered:
        outlines = list(pair[0].values())
        max_error = find_max_error(outlines[0], outlines[1])
        if pair[1]<max_error:
            new_filtered.append(pair)
    return(new_filtered)

def identify_cell(center, color):
    for c_obj in cells:
        if (c_obj.color == color) and (center in c_obj.centers):
            return(c_obj)

    print("No Cell Found with center: ", center)
    return(None)


def compute_slice(stack_list, slice_num, color):
    cur_segs = find_segs(slice_dict=stack_list[slice_num], color=color)
    prev_segs = find_segs(slice_dict=stack_list[slice_num-1], color=color)

    if len(cur_segs) == 0:
        #print("No cells on current slice")
        return()
    if len(prev_segs) == 0:
        for seg in cur_segs:
            new_cell = Cell(id = "Cell"+str(color)+" "+str(cell_count),
                            starting_slice = slice_num,
                            initial_outline = seg,
                            c_color = color)
        return()
    
    matched_list = match_cells(cur_cells=cur_segs,
                               prev_cells=prev_segs)
    
    filtered_list = filter_pairs(matched_list=matched_list)

    for pair in filtered_list:
        cur_outline = list(pair[0].values())[0]
        prev_center = list(pair[0].keys())[1]

        cell_obj = identify_cell(prev_center, color)
        cell_obj.add_outline(new_outline=cur_outline)

        cur_segs.remove(cur_outline)
    
    for seg in cur_segs:
        new_cell = Cell(id = "Cell"+str(color)+" "+str(cell_count),
                        starting_slice = slice_num,
                        initial_outline = seg,
                        c_color = color)

def first_slice_cells(slice_dict, color):
    cur_segs = find_segs(slice_dict=slice_dict, color=color)
    for seg in cur_segs:
        new_cell = Cell(id = "Cell"+str(color)+" "+str(cell_count),
                        starting_slice = 0,
                        initial_outline = seg,
                        c_color = color)

def compute_stack(stack_list, color):
    global cells
    cells = []
    first_slice_cells(slice_dict=stack_list[0],
                      color=color)
    for slice_num in range(1, len(stack_list)):
        compute_slice(stack_list=stack_list,
                      slice_num=slice_num,
                      color=color)


def get_data(path):
    with open(path, 'r') as f:   #blender_format_adjusted or blender_format
        d = f.read()

    data = ast.literal_eval(d)
    return(data)

def create_wireframes(path, colors, output_dir):
    data = get_data(path=path)

    for color in colors:
        print("\n\nCurrent color: ", color)
        result = {} 

        for tp in range(0, len(data.keys())):
            result[tp] = []
            compute_stack(stack_list=data[tp],
                          color = color)
            for cell in cells:       
                wfsx = triple_wireframe.triple_wireframe_creation(outline_list = copy.deepcopy(cell.outlines), x_or_y = "x", starting_slice=cell.starting_slice, wf_dist_arg=(3/0.198)/1, wf_offset_arg=1.25)
                wfsy = triple_wireframe.triple_wireframe_creation(outline_list = copy.deepcopy(cell.outlines), x_or_y = "y", starting_slice=cell.starting_slice, wf_dist_arg=(3/0.198)/1, wf_offset_arg=1.25)
                result[tp].append({color : wfsx+wfsy})
        with open(output_dir + "R" + str(color[0]) + "G" + str(color[1]) + "B" + str(color[2]) +".txt", 'w') as f:
            f.write(str(result))



create_wireframes(path = "C:/Users/areil/Desktop/Terra/Programs/Program Outputs/For TWF First Animation Rotated.txt", #"C:/Users/areil/Desktop/Terra/Programs/Program Outputs/GC Iso 21tps.txt",
                  colors = [(255,0,0), (255,0,255), (0,0,255), (255,0,0), (0,255,255), (255,100,0)],      #(255,0,0), (255,0,255), (0,0,255), (255,0,0), (0,255,255), (255,100,0)
                  output_dir = "C:/Users/areil/Desktop/Terra/Programs/Program Outputs/PRES TWF Animation1 DENSE/")