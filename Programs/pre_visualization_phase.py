"""
This is what the user will run. 

Gets AI and Manually traced data and outputs in separate files. User can choose which one (or both) to use in blender.




NOTES

Try lower flow threshold for less cells
"""




#------------------------------------------------------------------------------AI SEGMENTATION------------------------------------------------------------------------------
"""
The AI segmentation code takes the following inputs:
folders
    - List of directories where the raw data is. Input in the form: 'folders=[*f1*, *f2*, *f3*, ...]'.

model_path
    -  Path to the CELLPOSE model. Input in the form: 'model_path="*path*"'. Remember to replace backslashes with forwardslashes.

channels
    - Channels that the model will use. Input in the form: 'channels=[*c1*, *c2*]. Choose between:
        - ["Grayscale", "Blue", "Green", "Red"] for channel 1.
        - ["None", "Blue", "Green", "Red"] for channel 2. 
      Channel 2 is recommended when possible, for instance the nuclei color.     <--- FACT CHECK THIS

segmentation_parameters
    - Segmentation parameters, in the form: 'segmentation_parameters=[*diameter*, *flow threshold*, *cellprob threshold*]'.
        - Diameter: diameter of cells (set to zero to use diameter from training set).
        - Flow threshold: threshold on flow error to accept a mask (set higher to get more cells, e.g. in range from (0.1, 3.0), OR set to 0.0 to turn off so no cells discarded).
        - Cellprob threshold: threshold on cellprob output to seed cell masks (set lower to include more pixels or higher to include fewer, e.g. in range from (-6, 6)).
"""


if input('Run AI segmentation model? (y/n)').lower() == 'y':
    import AI_segmentation
    print("Running AI Segmentation Model")


    #Change variables below
    folders = ['C:/Users/areil/Desktop/Terra/Unprocessed Animations/A1 raw data/t'+str(i) for i in range(1, 47)]
    model_path = "C:/Users/areil/Desktop/Terra/human_in_the_loop/train/models/CP_tissuenet"
    channels = ["Green", "Red"]
    segmentation_parameters = [30, 0.15, 0]          #A1 AI Segmentation Output uses [30, 0.4, 0]
    output_dir='C:/Users/areil/Desktop/Terra/Programs/Program Outputs/test3-A1 AI segmentations'
    #---------------------
    AI_segmentation.run_AI_segmentation_model(folders=folders,   #path to images
                                              model_path=model_path,     #path to model
                                              channels=channels,
                                              segmentation_parameters=segmentation_parameters,
                                              output_dir=output_dir)





#--------------------------------------------------------------------------FORMATTING PREPARATION---------------------------------------------------------------------------
"""
The formatting preparation code takes the following inputs:
img_path
    - Path to a sample image, in order to extract image dimensions. Input in the form: 'img_path="*path*"'. Remember to replace backslashes with forwardslashes.

number_of_timepoints
    -  Number of timepoints the data contains. Input in the form: 'number_of_timepoints = *Positive whole number*'.

number_of_slices
    -  Number of slices each timepoint in the data contains. Input in the form: 'number_of_slices = *Positive whole number*'.

path_end
    - File extensions of each image in the data. For example, '.png'. Input in the form: 'path_end = "*extension*"'.

reference_point_color
    - RGB value of the reference point that was manually drawn. Input in the form: 'reference_point_color = (*R*, *G*, *B*).
"""

if input('\n\nRun formatting preparation? This needs to be run to run the manual or AI segmentation formatter. (y/n)').lower() == 'y':
    import formatting_preparation
    print("Running formatting preparation")


    #Change variables below
    img_path="C:/Users/areil/Desktop/Terra/Unprocessed Animations/A1 manual data/t1/1.png"
    #---------------------
    
    #Change variables below if reference point should be found
    path_to_timepoints="C:/Users/areil/Desktop/Terra/Unprocessed Animations/A1 manual data"
    number_of_timepoints=46
    number_of_slices=15
    path_end=".png"
    reference_point_color=(255,255,0)
    #---------------------

    img_dims = formatting_preparation.find_image_dimensions(img_path=img_path)

    if input('Find reference points? This is needed to adjust the germarium if it moves during the animation. (y/n)').lower() == 'y':
        ref_list = formatting_preparation.find_reference_points(path_to_timepoints=path_to_timepoints,
                                                                number_of_timepoints=number_of_timepoints,
                                                                number_of_slices=number_of_slices,
                                                                path_end=path_end,
                                                                reference_point_color=reference_point_color,
                                                                image_dimensions=img_dims)





#-------------------------------------------------------------------------AI SEGMENTATION Formatter-------------------------------------------------------------------------
"""
output_file
    - This is the file name where the output data will be stored. Input in the form: 'output_file = "*file*"'.
      It may be helpful to have 'manual' in the name to distinguish from the output file from the AI segmentation formatter.

path_to_timepoints
    - Path to the directory where the manually drawn timepoint(s) are located. Input in the form: 'path_to_timepoints="*path*"'. Remember to replace backslashes with forwardslashes.

number_of_timepoints
    -  Number of timepoints the data contains. Input in the form: 'number_of_timepoints = *Positive whole number*'.

number_of_slices
    -  Number of slices each timepoint in the data contains. Input in the form: 'number_of_slices = *Positive whole number*'.

reference_point_list
    - List of the reference point on each timepoint. If the reference point list was found in the FORMATTING PREPARATION phase, use 'reference_point_list=ref_list'. 
      Otherwise, input in the form: 'reference_point_list=[(*x1*, *y1*), (*x2*, *y2*), ...]' or 'reference_point_list=None' for no reference point adjustments.
"""

if input('\n\nRun AI segmentation formatter? (y/n)').lower() == 'y':
    import AI_segmentation_formatter
    print("Running AI segmentation formatter")


    #Change variables below
    output_file = "C:/Users/areil/Desktop/Terra/Programs/Program Outputs/test3-A1 AI formatted data.txt"

    path_to_timepoints='C:/Users/areil/Desktop/Terra/Programs/Program Outputs/test3-A1 AI segmentations'
    number_of_timepoints=46
    number_of_slices=15
    reference_point_list=ref_list
    #---------------------


    frame_dict, AI_time_taken = AI_segmentation_formatter.prepare_AI_data(path_to_timepoints=path_to_timepoints,
                                                                          number_of_timepoints=number_of_timepoints,
                                                                          number_of_slices=number_of_slices,
                                                                          reference_point_list=reference_point_list)

    print("AI data formatting time taken: " + str(AI_time_taken))
    with open(output_file, 'w') as f:
            f.write(str(frame_dict))






#-----------------------------------------------------------------------MANUAL SEGMENTATION FORMATTER-----------------------------------------------------------------------
"""
The manual segmentation formatter code takes the following inputs:
output_file
    - This is the file name where the output data will be stored. Input in the form: 'output_file = "*file*"'.
      It may be helpful to have 'manual' in the name to distinguish from the output file from the AI segmentation formatter.

path_to_timepoints
    - Path to the directory where the manually drawn timepoint(s) are located. Input in the form: 'path_to_timepoints="*path*"'. Remember to replace backslashes with forwardslashes.

recursive_colors
    - List of RGB colors of cell outlines that are small to medium in size. Input in the form: 'recursive_colors=[(*R1*, *G1*, *B1*), (*R2*, *G2*, *B2*), ...]'.

brute_force_colors
    - List of RGB colors of cell outlines that are large in size. Input in the form: 'brute_force_colors=[(*R1*, *G1*, *B1*), (*R2*, *G2*, *B2*), ...]'.
      If Python's maximum recursion limit is exceeded for a color in recursive_colors, switching the color to brute_force_colors is recommended.

number_of_timepoints
    -  Number of timepoints the data contains. Input in the form: 'number_of_timepoints = *Positive whole number*'.

number_of_slices
    -  Number of slices each timepoint in the data contains. Input in the form: 'number_of_slices = *Positive whole number*'.

reference_point_list
    - List of the reference point on each timepoint. If the reference point list was found in the FORMATTING PREPARATION phase, use 'reference_point_list=ref_list'. 
      Otherwise, input in the form: 'reference_point_list=[(*x1*, *y1*), (*x2*, *y2*), ...]' or 'reference_point_list=None' for no reference point adjustments.

path_end
    - File extensions of each image in the data. For example, '.png'. Input in the form: 'path_end = "*extension*"'.

image_dimensions
    - Dimensions of each image. If the dimensions were found in the FORMATTING PREPARATION phase, use 'image_dimensions=img_dims'.
      Otherwise, input the dimensions manually in the form: 'image_dimensions=[*height*, *width*]'.

sort_large_groups
    - Boolean variable that determines if the outlines from brute_force_colors are sorted. This is needed because brute_force_colors are unsorted, leading to messy wireframes.
      This is highly suggested, but adds computing time. Input in the form: 'sort_large_groups=True' or 'sort_large_groups=False'.
"""

if input('\n\nRun manual segmentation formatter? (y/n)').lower() == 'y':
    import manual_segmentation_formatter
    print("Running manual segmentation formatter")


    #Change variables below
    output_file = "C:/Users/areil/Desktop/Terra/Programs/Program Outputs/test2-A1 manual formatted data.txt"

    path_to_timepoints="C:/Users/areil/Desktop/Terra/Unprocessed Animations/A1 manual data"
    recursive_colors=[(255,0,0), (0,0,255), (255,255,0), (255,0,255), (0,255,255), (255,100,0)]
    brute_force_colors=[(0, 255, 0)]
    number_of_timepoints=46
    number_of_slices=15
    reference_point_list=ref_list
    path_end='.png'
    image_dimensions=img_dims
    sort_large_groups=True
    #---------------------


    frame_dict, manual_time_taken = manual_segmentation_formatter.prepare_manual_data(path_to_timepoints=path_to_timepoints,
                                                                                      recursive_colors=recursive_colors,
                                                                                      brute_force_colors=brute_force_colors,
                                                                                      number_of_timepoints=number_of_timepoints,
                                                                                      number_of_slices=number_of_slices,
                                                                                      reference_point_list=reference_point_list,
                                                                                      path_end=path_end,
                                                                                      image_dimensions=image_dimensions,
                                                                                      sort_large_groups=sort_large_groups)
    
    print("Manual data formatting time taken: " + str(manual_time_taken))
    with open(output_file, 'w') as f:
        f.write(str(frame_dict))