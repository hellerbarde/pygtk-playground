#!/usr/bin/python

import pygst
pygst.require("0.10")
import gst
#import pygtk
#import gtk
import time
class Main:
	def __init__(self):
		self.pipeline = gst.Pipeline("mypipeline")

		self.audiotestsrc = gst.element_factory_make("audiotestsrc", "audio")
		self.filesrc = gst.element_factory_make("filesrc", "audiosrc")
		self.decoder = gst.element_factory_make("decodebin", "decoder")
		self.converter = gst.element_factory_make("audioconvert", "converter")

		self.pipeline.add(self.audiotestsrc)

		self.sink = gst.element_factory_make("alsasink", "sink")
		self.pipeline.add(self.sink)

		self.audiotestsrc.link(self.sink)

		self.pipeline.set_state(gst.STATE_PLAYING)

start=Main()
while True:
	time.sleep(0.5)
#gtk.main()

