
Writing a GUI app with Python & Glade

Edit: Please do check out the video screencast of this tutorial.

Here is what is to be created:



This tutorial will assume a basic knowledge of programming in general, and an understanding of Python. You don't even really need that, but if you don't know python well, you might need to look some stuff up, but google is your friend. This tutorial also assumes you are running Linux. I don't know about glade on Windows, so you'd have to check that out yourself.
You will also need to install python and glade.

Writing a GUI application to do a task may seem like a difficult job, but in fact, it can be very simple. Python is the language of choice for me, it's simple and fast to develop in, with a fair amount of power behind it.

First of all, we need an idea of what to do. Let's do something very basic to begin with, a program to add two numbers, and display an output. We'll start by creating a simple CLI app, which we'll convert.

tutCLI.py:

Code:
class adder:

result = 0

def __init__( self, number1, number2 ):
self.result = int( number1 ) + int( number2 )

def giveResult( self ):
return str(self.result)

endIt = False
while ( endIt == False ):
print "Please input two intergers you wish to add: "
number1 = raw_input( "Enter the first number: " )
number2 = raw_input( "Enter the second number: " )
try:
thistime = adder( number1, number2 )
except ValueError:
print "Sorry, one of your values was not a valid integer."
continue
print "Your result is: " + thistime.giveResult()
goagain = raw_input( "Do you want to eXit or go again? ('X' to eXit, anything else to continue): " )
if ( goagain == "x" or goagain == "X" ):
endIt = True

This is a simple python script to get the input. The class 'adder' does the actual addition. Taking two inputs in the constructor (__init__), and then adding the two, and storing the result in the 'result' member.
The rest is the stuff that makes our CLI work. It gives the user instructions, takes some input, then it adds the numbers (note this is in a try/except to see if an exception was thrown. This is so we don't throw ugly errors to the user if they input something which is not an integer. It then prints the result, and asks if the user wants to go again, all pretty self-explanetory.

Now we need to create a GUI for this. Open up glade.
Press the 'New Window' button on the left, under 'Toplevels'. This will give you an empty window.



Before we begin, I will make note that glade works in a way that web developers will be used to, by using relative positioning, and splitting the area to arrange things, not by absolute values.

You will need to create a vertical box with 3 items. This splits our window into three segments. The top will be instructions, the bottom buttons and information, the middle the entry areas.



Create a label, and put it up top, don't worry about the text at the moment. Next create a table 2 wide and 3 down in the middle, and finally a horizontal box with 2 items at the bottom.



In the middle, put a label in each as the three left-hand items, and a Text Entry as the right hand portion.



In the bottom, make another 2-item horizontal box in the bottom-left hand corner. Now add an image and a label to the this box. On the right of the main box add a two-item button box in the right hand slot. Add a button to each of these slots.



Add some appropriate text to the top label, and Number 1, Number 2, and Result to the labels on the left. This can all be done in the properties area on the right of your screen. Change your image in the bottom left hand corner to 'Stock' and then choose the stock image 'Warning'. Make the label next to it a warning (like "Sorry, one of your values was not a valid integer." in our CLI). For the two buttons, choose 'Stock' for both, and make one 'gtk-quit' and one 'gtk-add' - for obvious reasons.



OK, so we have everything set up, but it looks decidedly wonky and out of proportion. To counter this, you need to edit the way the items expand. Select the first Text Area, and go into 'packing'. Turn off the vertical 'Expand' option. Repeat this for all of the Text Areas and labels. You will need to go through your items forcing them to expand or not until it looks correct. (Only items in tables have individual horizontal and vertical expand options. For example, the button box should have 'expand' off.) Remember, you can use the tree view to the right to select items, so go through each one one-by-one and check it expanded and not, and see which works, you'll soon get the hang of what needs to be expanded to make the GUI function correctly.



You should end up with something like this:



Once you have, we still have a little to do in glade. Choose your Window (probably 'window1' in your treeview) and go to the 'General' tab in the properties window. Change the name to something more suitible - 'windowMain' is what I'll use. Set Window Title to something you want the user to see ("Latty's Amazing Adder!" in my case.). Next go to the signals tab, and open 'GtkObject' - and click on "destroy" - the dropdown menu under 'handler' - then choose 'on_windowMain_destroy' - This is the event that the GUI will give your application to say the user has tried to quite the application (by clicking on the close icon). Make sure to click somewhere else so it goes out of edit mode before doing anything else, otherwise it'll not save that signal.



Repeat this process for everything you will need to access, changing the names of the entries to something appropriate (these don't need any signals), changing the name of the bottom left hand hbox which contains your warning to something more apt, and changing the names of the two buttons then creating 'clicked' signals for both of them.

Almost there! Finally, we need to make a few small edits. Select the hbox which contains your warning (which should not be renamed something, hboxWarning in my case) - then set 'visible' to false. We don't want this warning shown to begin with. You need to do the opposite for the main window, which you do want visible, so make sure it is. You will also want to turn 'sensitive' on the result Text Entry (under 'Common') to be false - this is for the user to see the result, they don't need to edit it. This will 'grey-out' the box (allthough not in glade, for some reason. You also need to go to the button box containing your two buttons and set 'pack type' under 'packing' to end, so it doesn't move around when the warning appears and disappears.



There! Done with the GUI. Save it in the same folder as where you will develop your app. "main.glade" in my case.

OK, let's begin with our GUI script. First of all, we need to import the libraries we will need.
 
Code:
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

The sys library is there purely to allow us to call 'sys.exit' - used to exit the application. The rest is to import the GTK, our graphical library. It should all make sense.
Next we need to have our adder class again, this is unchanged from our original application (the wonders of object orientation, kids):
 
Code:
class adder:

result = 0

def __init__( self, number1, number2 ):
self.result = int( number1 ) + int( number2 )

def giveResult( self ):
return str(self.result)

Now, here comes the juicy bit, the GUI class.
 
Code:
class leeroyjenkins:

wTree = None

def __init__( self ):
self.wTree = gtk.glade.XML( "main.glade" )

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

Basically, it loads the widget tree from your glade file, and then creates a list of signals and what methods they point to. In our case, closing the window and clicking quit both make it quit (a member function which is pretty obvious), and clicking add calls our add member function.

The gtk.main() function just makes a loop which will display the GUI, and handle any signals as you have told it to.

Notice members called by signals need a 'widget' parameter. This is the widget that set off that signal. We don't need this, but you might in another case. Our add function should look very familiar, and should be pretty self explanetory.

Alright, that's it! Here is the end result in full:
 
Code:
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
self.wTree = gtk.glade.XML( "main.glade" )

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

Note the last line which creates an object of our GUI class, this makes the program actually begin.




There we have it, a simple GUI app with Python and Glade. It's not that hard to do. This example, of course, may seem like a lot of work for little result, as the resulting application is not that useful, but what you have learnt here can easily be applied to other things.

If you want to see a fully functional app written in python/glade, check out simpleconf. This was written for OCNix and is made in exactly the same way as is outlined here. You should be able to see how it functions. The source code is right there, so take a look.

Edit: Forgot to mention, there is a reason to use the stock buttons wherever possible. They are automatically translated to the language the user is currently using, and change icon with the theme the user is using, so it always fits in.

Attached is the full source to everything.
