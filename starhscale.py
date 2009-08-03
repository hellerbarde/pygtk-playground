#!/usr/bin/env python

"""
StarHScale a Horizontal slider that uses stars
Copyright (C) 2006 Mark Mruss <selsine@gmail.com>

This library is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public
License as published by the Free Software Foundation; either
version 2.1 of the License, or (at your option) any later version.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public
License along with this library; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA

If you find any bugs or have any suggestions email: selsine@gmail.coim
"""

try:
	import math
	import gtk
  	import gobject
  	from gtk import gdk
except:
	raise SystemExit
	
import pango
import pygtk
if gtk.pygtk_version < (2, 0):
	print "PyGtk 2.0 or later required for this widget"
	raise SystemExit

BORDER_WIDTH = 5
PIXMAP_SIZE = 22
NR_VIS = 0

class StarHScale(gtk.Widget):
	"""A horizontal Scale Widget that attempts to mimic the star
	rating scheme used in iTunes"""
	
	def __init__(self, max_stars=5, stars=1):
		"""Initialization, numstars is the total number
		of stars that may be visible, and stars is the current
		number of stars to draw"""
		
		#Initialize the Widget
		gtk.Widget.__init__(self)
		
		self.max_stars = max_stars
		self.stars = stars
		self.faded_stars = 0
		self.number_is_visible = 0
		self.dots_are_visible = 0
		self.fadedstars_are_visible = 0
		# Init the list to blank
		self.sizes = []
		for count in range(0,self.max_stars):
			self.sizes.append((count * PIXMAP_SIZE) + BORDER_WIDTH)
		self.widget_width = self.max_stars*PIXMAP_SIZE+BORDER_WIDTH*2
		self.widget_height = PIXMAP_SIZE
		self.allocation = gtk.gdk.Rectangle(0,0, 
			self.widget_width, self.widget_height)

		
	def do_realize(self):
		"""Called when the widget should create all of its 
		windowing resources.  We will create our gtk.gdk.Window
		and load our star pixmap."""
		
		# First set an internal flag showing that we're realized
		self.set_flags(self.flags() | gtk.REALIZED)
		
		# Create a new gdk.Window which we can draw on.
		# Also say that we want to receive exposure events 
		# and button click and button press events
		

		self.window = gtk.gdk.Window(
			self.get_parent_window(),
			width=200,
			height=300,
# 			width=self.allocation.width,
# 			height=self.allocation.height,
			window_type=gdk.WINDOW_CHILD,
			wclass=gdk.INPUT_OUTPUT,
			event_mask=self.get_events() | gtk.gdk.EXPOSURE_MASK
				| gtk.gdk.BUTTON1_MOTION_MASK | gtk.gdk.BUTTON_PRESS_MASK
				| gtk.gdk.POINTER_MOTION_MASK
				| gtk.gdk.POINTER_MOTION_HINT_MASK
				| gtk.gdk.LEAVE_NOTIFY_MASK
				| gtk.gdk.ENTER_NOTIFY_MASK)
		
		# Create the pango context for font rendering
		self.pcontext = self.get_pango_context()
		
		# Associate the gdk.Window with ourselves, Gtk+ needs a reference
		# between the widget and the gdk window
		self.window.set_user_data(self)
		
		# Attach the style to the gdk.Window, a style contains colors and
		# GC contextes used for drawing
		self.style.attach(self.window)
		
		# The default color of the background should be what
		# the style (theme engine) tells us.
		self.style.set_background(self.window, gtk.STATE_NORMAL)
		self.window.move_resize(*self.allocation)
		
		# load the star xpm
		self.pixbuf_point=gtk.gdk.pixbuf_new_from_file_at_size("dot_light.svg",22,22)
		self.pixbuf_star=gtk.gdk.pixbuf_new_from_file_at_size("star_dark.svg",22,22)
		self.pixbuf_faded_star=gtk.gdk.pixbuf_new_from_file_at_size("star_light.svg",22,22)
		
# 		self.pixmap = gtk.Image()
# 		self.pixmap.set_from_file("star.png")
# 		self.pixmap, mask = gtk.gdk.pixmap_create_from_xpm_d(
# 			self.window
# 			, self.style.bg[gtk.STATE_NORMAL]
# 			, STAR_PIXMAP)
			
		# self.style is a gtk.Style object, self.style.fg_gc is
		# an array or graphic contexts used for drawing the forground
		# colours	
		self.gc = self.style.fg_gc[gtk.STATE_NORMAL]
# 		self.connect("expose_event", self.do_expose_event)
		self.connect("motion_notify_event", self.motion_notify_event)
		self.connect("leave_notify_event", self.do_leave_event)
		
	def do_unrealize(self):
		# The do_unrealized method is responsible for freeing the GDK resources
		# De-associate the window we created in do_realize with ourselves
		self.window.destroy()
		
	def do_size_request(self, requisition):
		"""From Widget.py: The do_size_request method Gtk+ is calling
		 on a widget to ask it the widget how large it wishes to be. 
		 It's not guaranteed that gtk+ will actually give this size 
		 to the widget.  So we will send gtk+ the size needed for
		 the maximum amount of stars"""
		
		requisition.height = PIXMAP_SIZE
		requisition.width = (PIXMAP_SIZE * self.max_stars) + (BORDER_WIDTH * 2)

	def do_size_allocate(self, allocation):
		"""The do_size_allocate is called by when the actual 
		size is known and the widget is told how much space 
		could actually be allocated Save the allocated space
		self.allocation = allocation. The following code is
		identical to the widget.py example"""
	
		if self.flags() & gtk.REALIZED:
			self.window.move_resize(*allocation)
		
	def do_expose_event(self, event):
		"""This is where the widget must draw itself."""
		#Draw the correct number of stars.  Each time you draw another star
		#move over by 22 pixels. which is the size of the star.
		if (self.dots_are_visible == 1):
			for count in range(0,self.max_stars):
				self.window.draw_pixbuf(	self.gc, self.pixbuf_point, 0, 0  # gc, pixbuf, src_x, src_y
											, self.sizes[count]         # dest_x, 
											, 0, -1, -1                 # dest_y, wid, hei, 
											, gtk.gdk.RGB_DITHER_NORMAL # dither,
											, 0, 0)
		if (self.fadedstars_are_visible == 1):
			for count in range(0,self.faded_stars):
				self.window.draw_pixbuf(	self.gc, self.pixbuf_faded_star, 0, 0  # gc, pixbuf, src_x, src_y
											, self.sizes[count]         # dest_x, 
											, 0, -1, -1                 # dest_y, wid, hei, 
											, gtk.gdk.RGB_DITHER_NORMAL # dither,
											, 0, 0)
		for count in range(0,self.stars):
			self.window.draw_pixbuf(	self.gc, self.pixbuf_star, 0, 0  # gc, pixbuf, src_x, src_y
										, self.sizes[count]         # dest_x, 
										, 0, -1, -1                 # dest_y, wid, hei, 
										, gtk.gdk.RGB_DITHER_NORMAL # dither,
										, 0, 0)

		# Draw the number
		if (self.number_is_visible == 1):
			self.playout = pango.Layout(self.pcontext)
			self.playout.set_font_description(pango.FontDescription("sans bold 8"))
			self.playout.set_text(str(self.stars))
			(w,h) = self.playout.get_pixel_size()
			lx = self.widget_width/2 -w/2
			ly = self.widget_height/2-h/2
			circle_r = h-2
			cx = self.widget_width/2
			cy = self.widget_height/2
			context = self.window.cairo_create()
			if (self.stars <= self.max_stars/2):
				context.arc(cx, cy, circle_r/2, 0, 2.0 * math.pi)
				context.set_source_rgb(0.2, 0.2, 0.2)
				context.fill_preserve()
			context.select_font_face("sans")
			context.set_font_size(6)
			context.set_source_rgb(0.7, 0.7, 0.7)			
			x_bearing, y_bearing, width, height = context.text_extents(str(self.stars))[:4]
#			print (str(lx - width / 2)+" "+str(ly))
			context.move_to(self.widget_width/2-width/2, self.widget_height/2+height/2)
			context.show_text(str(self.stars))
			
#			context.set_source_rgb(0.7, 0.7, 0.7)
#			context.text_path("foobar")
#			context.fill_preserve()
#			context.set_source_rgb(0, 0.5, 0)
#			context.stroke()
#			self.window.draw_arc(self.gc, True, cx, cy, circle_r, circle_r, 64*0, 64*360)
#			self.window.draw_layout(self.gc,lx,ly,self.playout)

	def motion_notify_event(self, widget, event):
		# if this is a hint, then let's get all the necessary 
		# information, if not it's all we need.
		if event.is_hint:
			x, y, state = event.window.get_pointer()
		else:
			x = event.x
			y = event.y
			state = event.state
		self.number_is_visible = NR_VIS
		self.dots_are_visible = 1
		self.fadedstars_are_visible = 1
		self.check_for_faded_stars(event.x)

		new_stars = 1
		if (state & gtk.gdk.BUTTON1_MASK):
			# loop through the sizes and see if the
			# number of stars should change
			self.check_for_new_stars(event.x)
		else:
			self.window.invalidate_rect(self.allocation,True)

	def do_leave_event(self, widget, event):
		# hide the number if the mouse leaves the widget
		self.dots_are_visible = 0
		self.number_is_visible = 0
		self.fadedstars_are_visible = 0
		self.window.invalidate_rect(self.allocation,True)
			
	def do_button_press_event(self, event):
		"""The button press event virtual method"""
		# make sure it was the first button
		if event.button == 1:
			#check for new stars
			self.number_is_visible = NR_VIS
			self.window.invalidate_rect(self.allocation,True)
			self.check_for_new_stars(event.x)
		return True
		
	def check_for_new_stars(self, xPos):
		"""This function will determine how many stars
		will be show based on an x coordinate. If the
		number of stars changes the widget will be invalidated
		and the new number drawn"""

		# loop through the sizes and see if the
		# number of stars should change
		new_stars = 0
		for size in self.sizes:
			if (xPos < size):
				# we've reached the star number
				break
			new_stars = new_stars + 1
		if (new_stars == 0):
			new_stars = 1
		#set the new value
		self.set_value(new_stars)
			
	def check_for_faded_stars(self, xPos):
		# loop through the sizes and see if the
		# number of stars should change
		faded_stars = 0
		for size in self.sizes:
			if (xPos < size):
				# we've reached the star number
				break
			faded_stars = faded_stars + 1
		if (faded_stars == 0):
			faded_stars = 1
		self.faded_stars = faded_stars


	def set_value(self, value):
		"""Sets the current number of stars that will be 
		drawn.  If the number is different then the current
		number the widget will be redrawn"""
		
		if (value >= 0):
			if (self.stars != value):
				self.stars = value
				#check for the maximum
				if (self.stars > self.max_stars):
					self.stars = self.max_stars
				# redraw the widget
				self.window.invalidate_rect(self.allocation,True)
			
	def get_value(self):
		"""Get the current number of stars displayed"""
		
		return self.stars
		
	def set_max_value(self, max_value):
		"""set the maximum number of stars"""
# 		self.allocation.x = 0
# 		self.allocation.y = 0
# 		self.allocation.width = max_value*22
# 		self.allocation.height = 22
		if (self.max_stars != max_value):
			"""Save the old max incase it is less then the 
			current number of stars, in which case we will
			have to redraw"""
			
			if (max_value > 0):
				self.max_stars = max_value
				#reinit the sizes list (should really be a sperate function
				self.sizes = []		
				for count in range(0,self.max_stars):
					self.sizes.append((count * PIXMAP_SIZE) + BORDER_WIDTH)
				"""do we have to change the current number of
				stars?"""			
				if (self.stars > self.max_stars):
					self.set_value(self.max_stars)
	
	def get_max_value(self):
		"""Get the maximum number of stars that can be shown"""
		
		return self.max_stars
			
if __name__ == "__main__":
	# register the class as a Gtk widget
	gobject.type_register(StarHScale)
	
	win = gtk.Window()
	#win.resize(200,20)
	win.connect('delete-event', gtk.main_quit)
	
	starScale = StarHScale(10,1)
	win.add(starScale)
	
	win.show_all()
	gtk.main()
	
