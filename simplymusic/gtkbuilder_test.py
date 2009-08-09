#!/usr/bin/env python

import sys
import gobject
import pango
import math
try:
	import pygtk
	#tell pyGTK, if possible, that we want GTKv2
	pygtk.require("2.0")
except:
	#Some distributions come with GTK2, but not pyGTK
	pass

try:
	import gtk
	#import gtk.Builder
except:
	print "You need to install pyGTK or GTKv2 ",
	print "or set your PYTHONPATH correctly."
	print "try: export PYTHONPATH=",
	print "/usr/local/lib/python2.2/site-packages/"
	sys.exit(1)
from starhscale import StarHScale
# import cellrendererwidget


BORDER_WIDTH = 5
PIXMAP_SIZE = 22
NR_VIS = 0

class player_mainwindow:
	"""This is an Hello World GTK application"""

	def __init__(self):
		
		#Set the Glade file
		self.gladefile = "gui.glade"  
		self.builder = gtk.Builder() 
		self.builder.add_from_file(self.gladefile)
		
		
		#Get the Main Window, and connect the "destroy" event
		self.window = self.builder.get_object('mainwindow')
		self.addfolder = self.builder.get_object('addfolder')
		self.addfile = self.builder.get_object('addfile')
		self.clear = self.builder.get_object('clear')
		self.save = self.builder.get_object('save')
		self.playlistview = self.builder.get_object('playlist')
		self.status_label = self.builder.get_object('status_label')
		gobject.type_register(StarHScale)
		self.playliststore = gtk.ListStore(StarHScale, str)
# 		textrenderer = gtk.CellRendererText()
		column1 = gtk.TreeViewColumn("Name", gtk.CellRendererText(), text=0 )
		column1.set_sort_column_id(0)
		column2 = gtk.TreeViewColumn("Blubb", gtk.CellRendererText(), text=1)
		column2.set_sort_column_id(1)
		if (self.window):
			self.window.connect("destroy", gtk.main_quit)
# 			self.fontbutton.connect("font-set", self.put_font_to_text)
			self.addfolder.connect("clicked", self.add_folder_callback)
			self.addfile.connect("clicked", self.add_file_callback)
			self.clear.connect("clicked", self.clear_playlist_callback)
			self.save.connect("clicked", self.save_playlist_callback)
			self.scale = StarHScale(5,1)
			self.playliststore.append([self.scale,"bar"])
			
			self.playlistview.set_model(self.playliststore)
			self.playlistview.append_column(column1)
			self.playlistview.append_column(column2)
			self.playlistview.set_headers_visible(True)

# 			for row in self.data:

			self.window.show()
	data =  [
			 ["hallo", "welt"],
			 ["test", "me"]
			]

	def add_folder_callback(self, button):
		self.status_label.set_text("Muahahhahha")
	def add_file_callback(self, button):
		self.playliststore.append(["foo","bar"])
	def clear_playlist_callback(self, button):
		self.playliststore.append(["baz","snafu"])
	def save_playlist_callback(self, button):
		self.status_label.set_text("Muahahhahha")
# 	def put_font_to_text(self, fontbutton):
# 		font_string = fontbutton.get_font_name()
# 		arr = str.split(font_string, " ")
# 		xft_str = ""
# 		for i in arr[:-2]:
# 			xft_str = xft_str + i + " "
# 		xft_str = xft_str+arr[-2]+"-"+arr[-1]
# 		self.textentry.set_text(xft_str)

if __name__ == "__main__":
	hwg = player_mainwindow()
	gtk.main()