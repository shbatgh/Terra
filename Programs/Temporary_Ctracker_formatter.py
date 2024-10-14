"""
Temporary code to convert slice files into format for blender renderer
"""
import time
import os
import ast

def get_slice_data(data_file_path):
    with open(data_file_path, 'r') as f:   #blender_format_adjusted or blender_format
        data = f.read()
    
    slice_dict = ast.literal_eval(data)
    return(slice_dict)


def format_stack(stack_path):                #timepoint is the path to the stack
    print("Formatting stack " + os.path.basename(os.path.normpath(stack_path)))       #takes last parts
    slice_paths = [ f.path for f in os.scandir(stack_path) if f.is_file() ]

    n_slices = len(slice_paths)                                        #Might raise an error

    stack_list=[]
    for slice_num in range(n_slices):          #slices are numbered 1 through n
        print(slice_num)
        cur_slice = get_slice_data(data_file_path=slice_paths[slice_num])
        stack_list.append(cur_slice)
    return(stack_list)
        



def prepare_Ctracker_data(path_to_timepoints):
    start_Ctracker_time = time.time()
    print("Preparing Ctracker Data")

    global timepoint_folders
    timepoint_folders = [f.path for f in os.scandir(path_to_timepoints) if f.is_dir()]

    n_timepoints = len(timepoint_folders)
    

    frame_dict = {}
    for tp_num in range(n_timepoints):
        cur_stack = format_stack(stack_path=timepoint_folders[tp_num])        #add to dict which houses stacks (frames)
        frame_dict[tp_num] = cur_stack

    Ctracker_time_taken = time.time()-start_Ctracker_time
    return(frame_dict, Ctracker_time_taken)



#Testing stuff out


frame_dict, Ctracker_time_taken = prepare_Ctracker_data(path_to_timepoints='C:/Users/areil/Desktop/Terra/Processed_AI_Segs/A1T1_formatted')


print("Time Taken:", Ctracker_time_taken)
with open("C:/Users/areil/Desktop/Terra/Programs/Program Outputs/Test 13 new Ctracker data.txt", 'w') as f:
    f.write(str(frame_dict))