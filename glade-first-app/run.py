#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
try:  
	import pygtk  
	pygtk.require("2.0")  
except:  
	pass  
try:  
	import gtk  
	import gtk.glade  
except:  
	print("GTK Not Availible")
	sys.exit(1)

class adder:

	result = 0
	
	def __init__( self, number1, number2 ):
		self.result = int( number1 ) + int( number2 )
		
	def giveResult( self ):
		return str(self.result)
		
class leeroyjenkins:

	wTree = None

	def __init__( self ):
		self.wTree = gtk.glade.XML( "gui.glade" )
		
		dic = { 
			"on_buttonQuit_clicked" : self.quit,
			"on_buttonAdd_clicked" : self.add,
			"on_windowMain_destroy" : self.quit,
		}
		
		self.wTree.signal_autoconnect( dic )
		
		gtk.main()

	def add(self, widget):
		try:
			thistime = adder( self.wTree.get_widget("entryNumber1").get_text(), self.wTree.get_widget("entryNumber2").get_text() )
		except ValueError:
			self.wTree.get_widget("hboxWarning").show()
			self.wTree.get_widget("entryResult").set_text("ERROR")
			return 0
		self.wTree.get_widget("hboxWarning").hide()
		self.wTree.get_widget("entryResult").set_text(thistime.giveResult())
	
	def quit(self, widget):
		sys.exit(0)
		
letsdothis = leeroyjenkins()
