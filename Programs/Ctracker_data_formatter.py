"""
Used for the outputs of sam's shit. 
Takes Sam's cell tracker output (which is a dict for each slice) and formats it correctly.


Old Replacement Steps:
-   '[ ', '['
-   ' ' , ', '
-   ',,', ','
-   '  ', ' '
-   '\n', ''
-   ':,', ':'
-   '[[', '[[['
-   ']]', ']]]'
-   ' (', ', ('
"""



"""


array(		[
),			],
)}			]}

"""

import os


def format_folder(folder_path, save_copy_path):
    if os.path.isdir(save_copy_path):
        if input("Output directory already exists and may not be empty. Files will be deleted in the folder. Continue anyway? (Y/N)") == "Y":
            files = [f.path for f in os.scandir(save_copy_path) if f.is_file()]
            for del_path in files:
                os.remove(del_path)
    else:
        os.makedirs(save_copy_path)

    
    for cur_path in [f.path for f in os.scandir(folder_path) if f.is_file()]:
        cur_base_name = os.path.basename(os.path.normpath(cur_path))
        print (cur_base_name)

        formatted_file = format_file(cur_path=cur_path)

        file = open(os.path.normpath(save_copy_path) + '/formatted_' + cur_base_name, 'w+')
        file.write(formatted_file)



def format_file(cur_path):
    with open(cur_path, 'r') as file:
        filedata = file.read()

    # Replace the target string
    filedata = filedata.replace('array(', '[')
    filedata = filedata.replace('),', '],')
    filedata = filedata.replace(')}', ']}')
    

    # Return formatted file
    return(filedata)








format_folder(folder_path='C:/Users/areil/Desktop/Terra/Processed_AI_Segs/A1T1', save_copy_path='C:/Users/areil/Desktop/Terra/Processed_AI_Segs/A1T1_formatted/t1')