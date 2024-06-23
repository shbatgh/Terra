#Just blender
import bpy
import ast

data_file_path = 'blender_animation1.txt'     #Remember to use backslashes instead of forward slashes
color_list = [(255,0,0), (0,255,0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255), (255, 100, 0)]

color_dict = {}
for color in color_list:
    converted_rgb = (color[0]/255, color[1]/255, color[2]/255, 1)
    cur_var = bpy.data.materials.new(str(color))
    cur_var.use_nodes = True
    principled = cur_var.node_tree.nodes['Principled BSDF']
    principled.inputs['Base Color'].default_value = converted_rgb
    color_dict[color] = cur_var


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
    
    curveOB = bpy.data.objects.new(name, curveData)         # create Object
    curveOB.data.materials.append(color_dict[color])        #add texture (color)
    cur_frame_col.objects.link(curveOB)                     #add to collection

    #Animation keyframes
    show_frame = frame*frames_per_time_point

    curveOB.hide_viewport = True
    curveOB.keyframe_insert(data_path = "hide_viewport",frame = 0)
    curveOB.hide_viewport = False
    curveOB.keyframe_insert(data_path = "hide_viewport",frame = show_frame)
    curveOB.hide_viewport = True
    curveOB.keyframe_insert(data_path = "hide_viewport",frame = show_frame + frames_per_time_point)


with open(data_file_path, 'r') as f:   #blender_format_adjusted or blender_format
    data = f.read()

frames = ast.literal_eval(data)

for frame_num in frames.keys():
    cur_frame_col = bpy.data.collections.new('frame'+str(frame_num))
    scene_col = bpy.context.scene.collection
    scene_col.children.link(cur_frame_col)
    for slice in frames[frame_num]:
        for color in slice.keys():
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