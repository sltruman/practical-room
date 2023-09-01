import os
os.environ['PATH'] = 'C:/gtk-build/gtk/x64/release/bin;' + os.environ['PATH']

import sys
import gi

gi.require_version("Gtk", "4.0")
from gi.repository import GLib, Gtk, GObject, Gio

class App(Gtk.Application):
    builder = Gtk.Builder.new_from_file('./app.ui')
    window = builder.get_object('app_window')
    button_start = builder.get_object('start')
    button_stop = builder.get_object('stop')
    button_edit = builder.get_object('edit')
    button_anchor = builder.get_object('anchor')
 
    def __init__(self):
        super().__init__(application_id="xyz.practistyle.PracticalRoom")
        GLib.set_application_name('Practical Room')

    def do_activate(self):
        self.add_window(self.window)
        self.button_start.connect('clicked',self.on_button_start_clicked)
        self.button_stop.connect('clicked',self.on_button_stop_clicked)

    def on_button_start_clicked(self,*args):
        self.button_start.set_visible(False)
        self.button_stop.set_visible(True)

    def on_button_stop_clicked(self,*args):
        self.button_start.set_visible(True)
        self.button_stop.set_visible(False)
    
exit_status = App().run(sys.argv)
sys.exit(exit_status)