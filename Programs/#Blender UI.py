import bpy

cur_joe=0


cur_joe+=1
cur_frame_col = bpy.data.collections.new('timepoint'+str(cur_joe))
scene_col = bpy.context.scene.collection
scene_col.children.link(cur_frame_col)

cur_joe+=1
cur_frame_col = bpy.data.collections.new('timepoint'+str(cur_joe))
scene_col = bpy.context.scene.collection
scene_col.children.link(cur_frame_col)