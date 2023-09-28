import sys
sys.path.append(".")


import bpy
import gpu
from gpu_extras.presets import draw_texture_2d

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