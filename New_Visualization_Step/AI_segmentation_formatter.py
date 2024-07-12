"""
UNFINISHED, Figure out AI segmentation first


parameters should be:
path_to_timepoints
number_of_timepoints
number_of_slices
reference_point_list

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

def prepare_AI_data(path_to_timepoints, number_of_timepoints, number_of_slices, reference_point_list):
    start_AI_time = time.time()
    print("Preparing AI Data")

    global tp_path, n_slices
    n_slices = number_of_slices
    tp_path = path_to_timepoints

    
    frame_dict = {}
    for tp_num in range(number_of_timepoints):

        cur_refp=reference_point_list[tp_num]
        cur_stack = format_stack(timepoint='t'+str(tp_num+1),              
                                 reference_point=cur_refp)        #add to dict which houses stacks (frames)
        
        frame_dict[tp_num] = cur_stack

    AI_time_taken = time.time()-start_AI_time
    return(frame_dict, AI_time_taken)


#######--------------------------------------------------------------------------------------------------------------------------------------------------------------------------


def find_image_dimensions(path_to_timepoints):
    sample_img = Image.open(path_to_timepoints+'/t1/1.png')            #CHANGE IF MAKING THE IMAGE NAMES CHANGEABLE
    width, height = sample_img.size
    return([width, height])

def find_reference_points(path_to_timepoints, number_of_timepoints, number_of_slices, path_end, reference_point_color, image_dimensions):
    print("Finding reference points on timepoints: ", end='')
    width, height = image_dimensions[0], image_dimensions[1]
    reference_point_list = []
    for tp_num in range(number_of_timepoints):
        print(str(tp_num+1) + ' ', end='')
        ref_point_found = False
        
        for slice_num in range(number_of_slices):
            if ref_point_found:
                continue
            cur_img = Image.open(path_to_timepoints+'/t'+str(tp_num+1)+'/'+str(slice_num+1)+path_end)
            pix = cur_img.load()
            reference_cell_x, reference_cell_y = [], []

            for x in range(width):
                for y in range(height):
                    if (pix[x,y][:3] == reference_point_color):
                        reference_cell_x.append(x)
                        reference_cell_y.append(y)
            if len(reference_cell_x) != 0:
                reference_point_list.append([int(sum(reference_cell_x) / len(reference_cell_x)), int(sum(reference_cell_y) / len(reference_cell_y))])
                ref_point_found = True

        if not ref_point_found: 
            print("No reference point found on timepoint t" + str(tp_num+1))
            reference_point_list.append([0,0])
    print("\n")
    return(reference_point_list)

img_dims = find_image_dimensions(path_to_timepoints='C:/Users/areil/Desktop/Germarium_Visualization/Images/Animation1')

ref_list = find_reference_points(path_to_timepoints='C:/Users/areil/Desktop/Germarium_Visualization/Images/Animation1',
                                 number_of_timepoints=4,
                                 number_of_slices=15,
                                 path_end='.png',
                                 reference_point_color=(255,255,0),
                                 image_dimensions=img_dims)


frame_dict, AI_time_taken = prepare_AI_data(path_to_timepoints='C:/Users/areil/Desktop/Terra/New_Visualization_Step/AI Segmentation Output',
                                            number_of_timepoints=4,
                                            number_of_slices=15,
                                            reference_point_list=ref_list)

print("AI data formatting time taken: " + str(AI_time_taken))
with open('AI_data.txt', 'w') as f:
        f.write(str(frame_dict))

#PATH to timepoints: C:/Users/areil/Desktop/Terra/New_Visualization_Step/AI Segmentation Output
#"C:/Users/areil/Desktop/Terra/New_Visualization_Step/AI_data.txt"