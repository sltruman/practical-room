import os
os.environ['PATH'] = 'C:/gtk-build/gtk/x64/release/bin;' + os.environ['PATH']

import sys
from practools import Scene,Editor,Viewer

import gi

gi.require_version("Gtk", "4.0")
from gi.repository import GLib, Gtk, GObject, Gio, Gdk, GdkPixbuf

import time
import cv2
import numpy as np

class App(Gtk.Application):
    builder = Gtk.Builder.new_from_file('./app.ui')
    window = builder.get_object('app_window')
    button_start = builder.get_object('start')
    button_stop = builder.get_object('stop')
    button_edit = builder.get_object('edit')
    button_anchor = builder.get_object('anchor')
    area = builder.get_object('simulation')
    scene = Scene()
    editor = Editor(scene)
    viewer = Viewer(scene)

    def __init__(self):
        super().__init__(application_id="xyz.practistyle.PracticalRoom")
        GLib.set_application_name('Practical Room')
        self.editor.add('store/plane/plane.urdf')

    def do_activate(self):
        self.add_window(self.window)
        self.area.set_draw_func(self.draw)
        self.button_start.connect('clicked',self.on_button_start_clicked)
        self.button_stop.connect('clicked',self.on_button_stop_clicked)

        controller = Gtk.EventControllerScroll.new(Gtk.EventControllerScrollFlags(Gtk.EventControllerScrollFlags.VERTICAL))
        controller.connect("scroll", self.on_area_zoom)
        self.area.add_controller(controller)

        controller = Gtk.GestureDrag.new()
        controller.set_button(1)
        controller.connect("drag_begin", self.on_area_rotate,'begin')
        controller.connect("drag_update", self.on_area_rotate,'update')
        controller.connect("drag_end", self.on_area_rotate,'end')
        self.area.add_controller(controller)

        controller = Gtk.GestureDrag.new()
        controller.set_button(3)
        controller.connect("drag_begin", self.on_area_pan,'begin')
        controller.connect("drag_update", self.on_area_pan,'update')
        controller.connect("drag_end", self.on_area_pan,'end')
        self.area.add_controller(controller)
    
    def update(self):
        elapsed = time.time() - self.tick
        self.scene.update(elapsed)
        self.viewer.update()
        GLib.idle_add(self.area.queue_draw)

    def draw(self, da, cr, area_w, area_h): 
        cr.set_source_rgb(40 / 255,40 / 255,40 / 255)
        cr.paint()

        aspect_ratio = 1. * self.scene.viewport_size[0] / self.scene.viewport_size[1]
        aspect_ratio2 = 1. * area_w / area_h
        factor = 1.0
        if aspect_ratio > aspect_ratio2: factor = 1. * area_w / self.scene.viewport_size[0]
        else: factor = 1. * area_h / self.scene.viewport_size[1]
        cr.scale(factor,factor)

        image_x = (area_w / factor - self.scene.viewport_size[0]) / 2
        image_y = (area_h / factor - self.scene.viewport_size[1]) / 2

        image = GdkPixbuf.Pixbuf.new_from_data(self.viewer.viewport_color_texture,GdkPixbuf.Colorspace.RGB,True,8,self.scene.viewport_size[0],self.scene.viewport_size[1],self.scene.viewport_size[0]*4)
        Gdk.cairo_set_source_pixbuf(cr,image,image_x,image_y)
        cr.paint()
        
        self.tick = time.time()
        GLib.idle_add(self.update)

    def on_area_rotate(self,obj,x,y,flag):
        if flag == 'begin':
            self.last_pos = 0,0
        elif flag == 'update':
            self.viewer.rotate(self.last_pos[0] - x,self.last_pos[1] - y)
            self.last_pos = x,y
        else:
            del self.last_pos   

    def on_area_pan(self,obj,x,y,flag):
        if flag == 'begin': self.last_pos = 0,0
        elif flag == 'update':
            self.viewer.pan(self.last_pos[0] - x,self.last_pos[1] - y)
            self.last_pos = x,y
        else: del self.last_pos
    
    def on_area_zoom(self,*args):
        self.viewer.zoom(args[2])

    def on_button_start_clicked(self,*args):
        self.button_start.set_visible(False)
        self.button_stop.set_visible(True)

    def on_button_stop_clicked(self,*args):
        self.button_start.set_visible(True)
        self.button_stop.set_visible(False)

    def on_button_import(self,*args):
        pass

    def on_button_export(self,*args):
        pass
    
exit_status = App().run(sys.argv)
sys.exit(exit_status)