from PIL import Image

def find_image_dimensions(img_path):
    sample_img = Image.open(img_path)            #CHANGE IF MAKING THE IMAGE NAMES CHANGEABLE
    width, height = sample_img.size
    print("Image dimensions: " + str(width) +", " + str(height))
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

