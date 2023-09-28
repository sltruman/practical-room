import sys
print(sys.path)
import bpy
import shutil
import os

blender_bin = shutil.which("C:/Users/SLTru/Desktop/BlenderFoundation.Blender_3.6.2.0_x64__ppwjx1n5r4v9t/Blender/blender.exe")
if blender_bin:
   print("Found:", blender_bin)
   bpy.app.binary_path = blender_bin
else:
   print("Unable to find blender!")

import gpu

WIDTH = 1024
HEIGHT = 768

offscreen = gpu.types.GPUOffScreen(WIDTH, HEIGHT)

import time

global tick
tick = time.time()

def draw():
    global tick
    context = bpy.context
    scene = context.scene
    view_matrix = scene.camera.matrix_world.inverted()
    projection_matrix = scene.camera.calc_matrix_camera(
        context.evaluated_depsgraph_get(), x=WIDTH, y=HEIGHT)

    offscreen.draw_view3d(
        scene,
        context.view_layer,
        context.space_data,
        context.region,
        view_matrix,
        projection_matrix,
        do_color_management=True)

    gpu.state.depth_mask_set(False)

    print(type(offscreen.texture_color.read()))
    
    print(time.time() - tick)
    tick = time.time()
bpy.types.SpaceView3D.draw_handler_add(draw, (), 'WINDOW', 'POST_PIXEL')