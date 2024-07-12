"""
This is what the user will run. 

Gets AI and Manually traced data and outputs in separate files. Then it combines them into one for a third file. User can choose which one to use in blender.
"""






#------------------------------------------------------------------------------AI SEGMENTATION------------------------------------------------------------------------------
"""
The AI segmentation code takes the following inputs:
folders
    - List of directories where the raw data is. Input in the form: 'folders=[*f1*, *f2*, *f3*, ...]

model_path
    -  The path to the CELLPOSE model. Input in the form: 'model_path="*path*"'. Remember to replace backslashes with forwardslashes

channels
    - The channels that the model will use. Input in the form: 'channels=[*c1*, *c2*]. Choose between:
        - ["Grayscale", "Blue", "Green", "Red"] for channel 1.
        - ["None", "Blue", "Green", "Red"] for channel 2. 
      Channel 2 is recommended when possible, for instance the nuclei color.     <--- FACT CHECK THIS

segmentation_parameters
    - The segmentation parameters, in the form: 'segmentation_parameters=[*diameter*, *flow_threshold*, *cellprob_threshold*]
        - Diameter of cells (set to zero to use diameter from training set)
        - Threshold on flow error to accept a mask (set higher to get more cells, e.g. in range from (0.1, 3.0), OR set to 0.0 to turn off so no cells discarded)
        - Threshold on cellprob output to seed cell masks (set lower to include more pixels or higher to include fewer, e.g. in range from (-6, 6))
"""

if input('Run AI segmentation model? (y/n)').lower() == 'y':
    import AI_segmentation
    print("Running AI Segmentation Model")


    #Change Variables Below
    folders = ['C:/Users/areil/Desktop/Terra/Raw data for Segmentation/t'+str(i) for i in range(1, 47)]
    model_path = "C:/Users/areil/Desktop/Terra/human_in_the_loop/train/models/CP_tissuenet"
    channels = ["Green", "Red"]
    segmentation_parameters = [30, 0.4, 0]
    output_dir='C:/Users/areil/Desktop/Terra/New_Visualization_Step/AI Segmentation Output'
    #---------------------

    AI_segmentation.run_AI_segmentation_model(folders=folders,   #path to images
                                            model_path=model_path,     #path to model
                                            channels=channels,
                                            segmentation_parameters=segmentation_parameters,
                                            output_dir=output_dir)






#-------------------------------------------------------------------------AI SEGMENTATION Formatter-------------------------------------------------------------------------
"""
The AI segmentation code takes the following inputs:
folders
    - List of directories where the raw data is. Input in the form: 'folders=[*f1*, *f2*, *f3*, ...]

model_path
    -  The path to the CELLPOSE model. Input in the form: 'model_path="*path*"'. Remember to replace backslashes with forwardslashes

channels
    - The channels that the model will use. Input in the form: 'channels=[*c1*, *c2*]. Choose between:
        - ["Grayscale", "Blue", "Green", "Red"] for channel 1.
        - ["None", "Blue", "Green", "Red"] for channel 2. 
      Channel 2 is recommended when possible, for instance the nuclei color.     <--- FACT CHECK THIS

segmentation_parameters
    - The segmentation parameters, in the form: 'segmentation_parameters=[*diameter*, *flow_threshold*, *cellprob_threshold*]
        - Diameter of cells (set to zero to use diameter from training set)
        - Threshold on flow error to accept a mask (set higher to get more cells, e.g. in range from (0.1, 3.0), OR set to 0.0 to turn off so no cells discarded)
        - Threshold on cellprob output to seed cell masks (set lower to include more pixels or higher to include fewer, e.g. in range from (-6, 6))
"""

if input('\n\nRun formatting preparation? This needs to be run to run the manual or AI segmentation formatter. (y/n)').lower() == 'y':
    import formatting_preparation
    print("Running formatting preparation")
    img_dims = formatting_preparation.find_image_dimensions(img_path='C:/Users/areil/Desktop/Germarium_Visualization/Images/Animation1/t1/1.png')

    ref_list = formatting_preparation.find_reference_points(path_to_timepoints='C:/Users/areil/Desktop/Germarium_Visualization/Images/Animation1',
                                                            number_of_timepoints=4,
                                                            number_of_slices=15,
                                                            path_end='.png',
                                                            reference_point_color=(255,255,0),
                                                            image_dimensions=img_dims)
    





#-------------------------------------------------------------------------AI SEGMENTATION Formatter-------------------------------------------------------------------------
"""
The AI segmentation code takes the following inputs:
folders
    - List of directories where the raw data is. Input in the form: 'folders=[*f1*, *f2*, *f3*, ...]

model_path
    -  The path to the CELLPOSE model. Input in the form: 'model_path="*path*"'. Remember to replace backslashes with forwardslashes

channels
    - The channels that the model will use. Input in the form: 'channels=[*c1*, *c2*]. Choose between:
        - ["Grayscale", "Blue", "Green", "Red"] for channel 1.
        - ["None", "Blue", "Green", "Red"] for channel 2. 
      Channel 2 is recommended when possible, for instance the nuclei color.     <--- FACT CHECK THIS

segmentation_parameters
    - The segmentation parameters, in the form: 'segmentation_parameters=[*diameter*, *flow_threshold*, *cellprob_threshold*]
        - Diameter of cells (set to zero to use diameter from training set)
        - Threshold on flow error to accept a mask (set higher to get more cells, e.g. in range from (0.1, 3.0), OR set to 0.0 to turn off so no cells discarded)
        - Threshold on cellprob output to seed cell masks (set lower to include more pixels or higher to include fewer, e.g. in range from (-6, 6))
"""

if input('\n\nRun formatting preparation? This needs to be run to run the manual or AI segmentation formatter. (y/n)').lower() == 'y':
    import AI_segmentation_formatter
    print("Running AI segmentation formatter")
    img_dims = formatting_preparation.find_image_dimensions(img_path='C:/Users/areil/Desktop/Germarium_Visualization/Images/Animation1/t1/1.png')


    ref_list = formatting_preparation.find_reference_points(path_to_timepoints='C:/Users/areil/Desktop/Germarium_Visualization/Images/Animation1',
                                                            number_of_timepoints=4,
                                                            number_of_slices=15,
                                                            path_end='.png',
                                                            reference_point_color=(255,255,0),
                                                            image_dimensions=img_dims)

#import AI_segmentation_formatter
#import manual_segmentation_formatter
#Make section two have variables for input, make 3rd section what its supposed  to be 