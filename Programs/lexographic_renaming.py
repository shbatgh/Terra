#Renames all folders or files in a directory to be in lexographic order
#For example, 4.png will become 04.png
import os

def rename(path, file_or_folder, name_length):
    if file_or_folder == "file":
        items = [f.path for f in os.scandir(path) if f.is_file()]
    elif file_or_folder == "folder":
        items = [f.path for f in os.scandir(path) if f.is_dir()]
    else:
        print("file_or_folder not inputted correctly")
        return()
    
    if name_length == 'auto':
        name_length = max([len(os.path.basename(os.path.normpath(item))) for item in items])
    
    for cur_item in items:
        cur_name = str(os.path.basename(os.path.normpath(cur_item)))
        #print(cur_name)
        new_name = list(cur_name)
        if len(new_name) >= name_length:
            continue
        for i in range(len(new_name)):
            cur_char = new_name[i]
            if cur_char.isnumeric():
                for j in range (name_length-len(new_name)):
                    new_name.insert(i, '0')
                break
        new_name = ''.join(new_name)
        os.rename(os.path.normpath(path)+'/'+cur_name, os.path.normpath(path)+'/'+new_name)




def no_leading_zeros_rename(path, file_or_folder, name_length):
    if file_or_folder == "file":
        items = [f.path for f in os.scandir(path) if f.is_file()]
    elif file_or_folder == "folder":
        items = [f.path for f in os.scandir(path) if f.is_dir()]
    else:
        print("file_or_folder not inputted correctly")
        return()
    
    for cur_item in items:
        cur_name = str(os.path.basename(os.path.normpath(cur_item)))
        #print(cur_name)
        new_name = list(cur_name)

        if len(new_name) <= name_length:
            continue
        
        index_delete_list =[]
        for i in range(len(new_name)):
            cur_char = new_name[i]
            if cur_char.isnumeric() and cur_char != '0':
                break
            if cur_char == '0':
                index_delete_list.append(i)
                #len_dif-=1
        
        for i in range(len(index_delete_list)):
            del_index = index_delete_list[i]-i
            print(del_index)
            del new_name[del_index]
        new_name = ''.join(new_name)
        os.rename(os.path.normpath(path)+'/'+cur_name, os.path.normpath(path)+'/'+new_name)



"""no_leading_zeros_rename(path='C:/Users/areil/Desktop/Terra/Unprocessed Animations/Germarium6_96dpi',
       file_or_folder='folder',
       name_length=1)"""


"""
rename(path='C:/Users/areil/Desktop/Terra/Unprocessed Animations/Pngs Sept 2024',
        file_or_folder='folder',
        name_length='auto')

for cur_tp in [f.path for f in os.scandir('C:/Users/areil/Desktop/Terra/Unprocessed Animations/Pngs Sept 2024') if f.is_dir() ]:
    rename(path=cur_tp,
           file_or_folder='file',
           name_length='auto')

rename(path='C:/Users/areil/Desktop/Terra/Unprocessed Animations/Germarium6 raw data',
           file_or_folder='folder',
           name_length='auto')"""


"""no_leading_zeros_rename(path='C:/Users/areil/Desktop/Terra/Unprocessed Animations/Germarium6 raw data',
       file_or_folder='folder',
       name_length=1)"""


rename(path='C:/Users/areil/Desktop/Terra/Programs/Program Outputs/test2-A1 AI segmentations',
        file_or_folder='folder',
        name_length='auto')

timepoint_folders = [f.path for f in os.scandir('C:/Users/areil/Desktop/Terra/Programs/Program Outputs/test2-A1 AI segmentations') if f.is_dir()]
n_timepoints = len(timepoint_folders)

for cur_t in range(n_timepoints):
    cur_path = timepoint_folders[cur_t]
    txt_outline_path = os.path.normpath(cur_path) + "/txt_outlines"
    rename(path=txt_outline_path,
        file_or_folder='file',
        name_length='auto')