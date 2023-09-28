import os
import math as m
import numpy as np

import bpy
import gpu
from gpu_extras.presets import draw_texture_2d

class Viewer:
    cam_target = np.array([0.0,0.0,0.0])

    def __init__(self,context):
        self.context = context
        self.nodes = dict()
        self.run(context)
        pass

    def __del__(self):
        pass
    
    def run(self):
        WIDTH = 1024
        HEIGHT = 768

        offscreen = gpu.types.GPUOffScreen(WIDTH, HEIGHT)

        def draw():
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
            draw_texture_2d(offscreen.texture_color, (0, 0), WIDTH, HEIGHT)

        bpy.types.SpaceView3D.draw_handler_add(draw, (), 'WINDOW', 'POST_PIXEL')

    # def rotate(self,x,y):
    #     cam = np.array(self.base.cam.getPos())
    #     rz,rx,ry = self.base.cam.getHpr()
    #     rz += x / 2
    #     rx += y / 4
    #     rz %= 360
    #     if rx < -89: rx = -89
    #     if rx > -2: rx = -2
    #     direction = [0,-np.linalg.norm(cam - self.cam_target),0]
    #     R = Rotation.from_euler('xyz',[rx,0,rz],True)
    #     pos = self.cam_target + R.apply(direction)
    #     self.base.cam.setPos(pos[0],pos[1],pos[2])
    #     self.base.cam.setHpr(rz,rx,ry)
    #     pass
    
    # def pan(self,x,y):
    #     rz,rx,ry = self.base.cam.getHpr()
    #     cam = np.array(self.base.cam.getPos())
    #     cam_target = self.cam_target
        
    #     len = self.base.camNode.getLens(0)
    #     width,height = self.context.viewport_size

    #     direction_in_image = LPoint2(x/width,y/height)
    #     direction_in_camera = LPoint3(0,0,0)
    #     direction2_in_camera = LPoint3(0,0,0)
    #     len.extrude(direction_in_image,direction_in_camera,direction2_in_camera)
        
    #     distance = np.linalg.norm(cam - cam_target) * 2
    #     direction_in_camera = Rotation.from_euler('xyz',[0,0,rz],True).apply([direction_in_camera[0],-direction_in_camera[2],0]) * distance
    #     cam += direction_in_camera
    #     self.cam_target += direction_in_camera
    #     self.base.cam.setPos(cam[0],cam[1],cam[2])

    # def zoom(self,factor):
    #     origin = np.array(self.base.cam.get_pos())
    #     target = self.cam_target
    #     direction = target - origin
    #     x,y,z = origin - factor * direction * 0.1
    #     self.base.cam.set_pos(x,y,z)
    
    # def pick(self,x,y):
    #     width,height = self.context.viewport_size
    #     x = (x - width / 2) / (width / 2)
    #     y = (y - height / 2) / (height / 2)

    #     self.pickerRay.setFromLens(self.base.camNode,x,-y)
    #     self.picker.traverse(self.base.render)
    
    #     if not self.pq.getNumEntries():
    #         return None
        
    #     self.pq.sortEntries()
    #     collision_entry = self.pq.getEntry(0)
    #     geomNode = collision_entry.getIntoNodePath()
    #     node = geomNode.getParent().getParent()
    #     pos = collision_entry.getInteriorPoint(geomNode)
    #     id = node.getPythonTag('owner_id')
    #     link_index = node.getPythonTag('owner_link_index')
    #     return pos,id,link_index