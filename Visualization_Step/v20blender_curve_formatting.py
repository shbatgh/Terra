#This is formatting for curves rather than spheres
#formats data from the grouping segmentations stacks so that blender can understand

import time
import os
#import sys
#sys.path.append('C:/Users/areil/Desktop/Germarium_Visualization/Code/Intermediate_segmentation_analysis')       #PATH TO FOLDER

"""
{frame_num:[{(color):[[[x,y], [x,y], [x,y], [x,y], [x,y], [x,y], [x,y], [x,y]], 
                      [[x,y], [x,y], [x,y], [x,y], [x,y], [x,y], [x,y], [x,y]]]}
            {(color):[[[x,y], [x,y], [x,y], [x,y], [x,y], [x,y], [x,y], [x,y]], 
                      [[x,y], [x,y], [x,y], [x,y], [x,y], [x,y], [x,y], [x,y]]]}
            ]



}


"""



import v30group_segmentations_adjusted
import v10order_group               #group = v10order_group.main(group)

from v30group_segmentations_adjusted import brute_force_colors


pixel_dim = (0.198, 3) # In microns, dif between the x and y, and between z stacks
z_multiplier = pixel_dim[1]/pixel_dim[0]        #can by a constant to expand the stack     Not used anymore, disregard
#z_start = 3

#'t' + str(i) for i in range(1,47)
#'t1', 't2', 't3', 't4', 't5', 't6', 't7', 't8', 't9', 't10', 't11', 't12', 't13', 't14', 't15', 't16', 't17', 't18', 't19', 't20',
#'t21', 't22', 't23', 't24', 't25', 't26', 't27', 't28', 't29', 't30', 't31', 't32', 't33', 't34', 't35', 't36', 't37', 't38', 't39', 't40',
#'t41', 't42', 't43', 't44', 't45', 't46'

#Division at 't23', 't24', 't25'

output_file_name = 'blender_animation1.txt'
stack_paths = ['t' + str(i) for i in range(1,2)]   #47 for animation 1
frames = {}

total_start_time = time.time()

for frame_num in range(len(stack_paths)):
    cur_segmented_stack = v30group_segmentations_adjusted.main(stack_paths[frame_num])       #used to use v10group_segmentations, now use v20group_segmentations_adjusted
    for slice in cur_segmented_stack:
        for color in slice.keys():
            for group in slice[color]:
                if color in brute_force_colors:
                    cur_segmented_stack[cur_segmented_stack.index(slice)][color][slice[color].index(group)] = v10order_group.main(group)
                    #pass
    frames[frame_num] = cur_segmented_stack.copy()



with open(output_file_name, 'w') as f:
    f.write(str(frames))


print("\nAbsolute path to "+ output_file_name)
print(os.path.abspath(output_file_name))


print("\ntotal blender (curve & adjusted) formatting runtime: ", time.time()-total_start_time)