#Just blender
import bpy
import ast



red = bpy.data.materials.new("Red")
red.use_nodes = True
principled = red.node_tree.nodes['Principled BSDF']
principled.inputs['Base Color'].default_value = (1,0,0,1)

green = bpy.data.materials.new("Green")
green.use_nodes = True
principled = green.node_tree.nodes['Principled BSDF']
principled.inputs['Base Color'].default_value = (0,1,0,1)

blue = bpy.data.materials.new("Blue")
blue.use_nodes = True
principled = blue.node_tree.nodes['Principled BSDF']
principled.inputs['Base Color'].default_value = (0,0,1,1)

yellow = bpy.data.materials.new("Yellow")
yellow.use_nodes = True
principled = yellow.node_tree.nodes['Principled BSDF']
principled.inputs['Base Color'].default_value = (1,1,0,1)

purple = bpy.data.materials.new("Purple")
purple.use_nodes = True
principled = purple.node_tree.nodes['Principled BSDF']
principled.inputs['Base Color'].default_value = (1,0,1,1)

cyan = bpy.data.materials.new("Cyan")
cyan.use_nodes = True
principled = cyan.node_tree.nodes['Principled BSDF']
principled.inputs['Base Color'].default_value = (0,1,1,1)

orange = bpy.data.materials.new("Orange")
orange.use_nodes = True
principled = orange.node_tree.nodes['Principled BSDF']
principled.inputs['Base Color'].default_value = (1,0.25,0,1)

color_dict = {(255,0,0):red, (0,255,0):green, (0, 0, 255):blue, (255, 255, 0):yellow, (255, 0, 255):purple, (0, 255, 255):cyan, (255, 100, 0):orange}




frames_per_time_point = 10 

def add_curve(coords, name, slice, frame, color):
    global cur_frame_col
    curveData = bpy.data.curves.new('my_curve', type='CURVE')
    curveData.dimensions = '3D'
    curveData.resolution_u = 1     # Preview U
    curveData.fill_mode = 'FULL' # Fill Mode ==> Full
    curveData.bevel_depth      = 0.5   # Bevel Depth
    curveData.bevel_resolution = 1      # Bevel Resolution

    polyline = curveData.splines.new('NURBS')
    polyline.points.add(len(coords))
    for i, coord in enumerate(coords):
        x,y = coord
        z = frames[frame].index(slice)/0.198    #Multiply by 3/0.198????
        polyline.points[i].co = (x, y, z, 1)


    

    # create Object
    curveOB = bpy.data.objects.new(name, curveData)

    #add texture (color)
    curveOB.data.materials.append(color_dict[color])

    #add to collection
    cur_frame_col.objects.link(curveOB)

    #Animation keyframes
    show_frame = frame*frames_per_time_point

    curveOB.hide_viewport = True
    curveOB.keyframe_insert(data_path = "hide_viewport",frame = 0)
    curveOB.hide_viewport = False
    curveOB.keyframe_insert(data_path = "hide_viewport",frame = show_frame)
    curveOB.hide_viewport = True
    curveOB.keyframe_insert(data_path = "hide_viewport",frame = show_frame + frames_per_time_point)


with open('C:/Users/areil/Desktop/Germarium_Visualization/Code/Visualization/blender_format_adjusted_Animation1.txt', 'r') as f:   #blender_format_adjusted or blender_format
    data = f.read()

frames = ast.literal_eval(data)




for frame_num in frames.keys():
    cur_frame_col = bpy.data.collections.new('frame'+str(frame_num))
    scene_col = bpy.context.scene.collection
    scene_col.children.link(cur_frame_col)
    for slice in frames[frame_num]:
        for color in slice.keys():
            #if color == (0, 255, 0):
                #continue
            for group in slice[color]:
                name = 'f'+str(frame_num+1)+'_s'+str(frames[frame_num].index(slice))+'_c'+str(color)+'_g'+str(slice[color].index(group))        #frame, slice, color, group
                add_curve(coords=group, name=name, slice=slice, frame=frame_num, color=color)


"""
for a single frame

for slice in frames[0][:3]:
    for color in slice.keys():
        for group in slice[color]:
            name = 'f'+str(0)+'_s'+str(frames[0].index(slice))+'_c'+str(color)+'_g'+str(slice[color].index(group))        #frame, slice, color, group
            add_curve(coords = group, name = name, slice = slice, frame = 0)
"""