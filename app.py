import os
os.chdir(os.path.dirname(os.path.realpath(__file__)))
import sys

import subprocess as sp

import gi
gi.require_version("Gtk", "4.0")
from gi.repository import GLib, Gtk, GObject, Gio, Gdk, GdkPixbuf

import time
import numpy as np

class App(Gtk.Application):
    builder = Gtk.Builder.new_from_file('./app.ui')
    window = builder.get_object('app_window')
    button_start = builder.get_object('start')
    button_stop = builder.get_object('stop')
    button_edit = builder.get_object('edit')
    button_anchor = builder.get_object('anchor')
    area = builder.get_object('simulation')


    def __init__(self):
        super().__init__(application_id="xyz.practistyle.PracticalRoom")
        GLib.set_application_name('Practical Room')

        # obj = ActiveObject(self.scene,base='store/plane/plane.urdf',pos=[0,0,0],rot=[0,0,0])
        # self.editor.add('s',obj)
        # self.printer3d = G50Printer3D(self.scene,base='store/printer3d/printer3d.urdf',pos=[0,0,0],rot=[0,0,0])
        # self.editor.add('a',self.printer3d)

    def do_activate(self):
        self.add_window(self.window)
        self.area.set_draw_func(self.draw)
        # self.button_start.connect('clicked',self.on_button_start_clicked)
        # self.button_stop.connect('clicked',self.on_button_stop_clicked)

        # controller = Gtk.EventControllerScroll.new(Gtk.EventControllerScrollFlags(Gtk.EventControllerScrollFlags.VERTICAL))
        # controller.connect("scroll", self.on_area_zoomed)
        # self.area.add_controller(controller)

        # controller = Gtk.GestureClick.new()
        # controller.connect("pressed", self.on_area_picked,'pressed')
        # controller.connect("released", self.on_area_picked,'released')
        # self.area.add_controller(controller)

        # controller = Gtk.GestureDrag.new()
        # controller.set_button(1)
        # controller.connect("drag_begin", self.on_area_rotated,'begin')
        # controller.connect("drag_update", self.on_area_rotated,'update')
        # controller.connect("drag_end", self.on_area_rotated,'end')
        # self.area.add_controller(controller)

        # controller = Gtk.GestureDrag.new()
        # controller.set_button(3)
        # controller.connect("drag_begin", self.on_area_panned,'begin')
        # controller.connect("drag_update", self.on_area_panned,'update')
        # controller.connect("drag_end", self.on_area_panned,'end')
        # self.area.add_controller(controller)
    
    def update(self):
        # self.scene.update()
        # self.viewer.update()
        GLib.idle_add(self.area.queue_draw)

    def draw(self, receiver, cr, area_w, area_h): 
        cr.set_source_rgb(40 / 255,40 / 255,40 / 255)
        cr.paint()

        # aspect_ratio = 1. * self.scene.viewport_size[0] / self.scene.viewport_size[1]
        # aspect_ratio2 = 1. * area_w / area_h
        # self.factor = 1.0
        # if aspect_ratio > aspect_ratio2: self.factor = 1. * area_w / self.scene.viewport_size[0]
        # else: self.factor = 1. * area_h / self.scene.viewport_size[1]
        # cr.scale(self.factor,self.factor)

        # self.image_offset_x = image_x = (area_w / self.factor - self.scene.viewport_size[0]) / 2
        # self.image_offset_y = image_y = (area_h / self.factor - self.scene.viewport_size[1]) / 2

        # image = GdkPixbuf.Pixbuf.new_from_data(self.viewer.viewport_color_texture,GdkPixbuf.Colorspace.RGB,True,8,self.scene.viewport_size[0],self.scene.viewport_size[1],self.scene.viewport_size[0]*4)
        # Gdk.cairo_set_source_pixbuf(cr,image,image_x,image_y)
        # cr.paint()
        
        # self.tick = time.time()
        GLib.idle_add(self.update)

    def on_area_picked(self,receiver,n_press,x,y,flag):
        if flag == 'pressed':
            self.begin_pos = x,y
        else:
            if self.begin_pos[0] == x and self.begin_pos[1] == y:
                x,y=x/self.factor - self.image_offset_x,y/self.factor - self.image_offset_y
                info_detected = self.viewer.pick(x,y)
                print(info_detected)
            del self.begin_pos

    def on_area_rotated(self,receiver,x,y,flag):
        if flag == 'begin':
            self.last_pos = 0,0
        elif flag == 'update':
            self.viewer.rotate(self.last_pos[0] - x,self.last_pos[1] - y)
            self.last_pos = x,y
        else:
            del self.last_pos   

    def on_area_panned(self,receiver,x,y,flag):
        if flag == 'begin': self.last_pos = 0,0
        elif flag == 'update':
            self.viewer.pan(self.last_pos[0] - x,self.last_pos[1] - y)
            self.last_pos = x,y
        else: del self.last_pos
    
    def on_area_zoomed(self,*args):
        self.viewer.zoom(args[2])

    def on_button_start_clicked(self,*args):
        self.button_start.set_visible(False)
        self.button_stop.set_visible(True)

        with open('C:/Users/SLTru/Desktop/圆锥体_G50_6_Ender-PLA_31m.gcode', 'r') as f:
            gcode = f.read()
            self.printer3d.print(gcode)

    def on_button_stop_clicked(self,*args):
        self.button_start.set_visible(True)
        self.button_stop.set_visible(False)

    def on_button_import(self,*args):
        pass

    def on_button_export(self,*args):
        pass

exit_status = App().run(sys.argv)
sys.exit(exit_status)