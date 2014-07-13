# gui_view_world.py     written by Duncan Murray 10/7/2014

import os
import sys
import math

try:
	import Tkinter as Tkinter
except:
	import tkinter as Tkinter

from PIL import ImageTk, Image, ImageDraw
from tkinter import Tk, Canvas, PhotoImage, mainloop
        	
root_folder = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + os.sep + ".." ) 
sys.path.append(root_folder)
print(root_folder)
#import AI.agents.agent as agt
			
def usage():
    print("gui_view_world.py - AIKIF script to view a saved map")
    print("Usage:")
    print("   gui_view_world.py filename")
"""
try:                                
    opts, args = getopt.getopt(sys.argv[1:], "f", ["help"])
    print (opts, args)
except getopt.GetoptError:          
	usage()                         
	sys.exit(2)                     
"""
	
fname = root_folder + os.sep + "examples" + os.sep + "test_world.txt"
fname = root_folder + os.sep + "examples" + os.sep + "test_world_traversed.txt"    
def main():
    """
    view a text file (map) in high resolution
    """
    print("viewing ", fname)
    wrld = read_map(fname)
    for row in wrld:
        #for col in row:
        print(row)
    app = gui_view_tk(None)
    app.title('Map View')
    app.mainloop()
    
    
    
def read_map(fname):
    """
    reads a saved text file to list
    """
    lst = []
    with open(fname, "r") as f:
        for line in f:
            lst.append(line)
    return lst



class gui_view_tk(Tkinter.Tk):
    def __init__(self,parent):
        Tkinter.Tk.__init__(self,parent)
        self.parent = parent
        self.appWidth = 1200
        self.appHeight = 800
        self.cell_width = 3
        self.cell_height = 3
        self.screenWidth = self.winfo_screenwidth()
        self.screenHeight = self.winfo_screenheight()
        self.configure(bg='black')
        self.geometry('%dx%d+%d+%d' % (self.appWidth, self.appHeight, self.screenWidth - self.appWidth - 0, self.screenHeight - self.appHeight - 0))

        WIDTH = self.appWidth
        HEIGHT = self.appHeight
        self.canvas = Canvas(self, width=WIDTH, height=HEIGHT, bg="#000000")
        self.canvas.pack()
        self.img = PhotoImage(width=WIDTH, height=HEIGHT)
        self.canvas.create_image((WIDTH/2, HEIGHT/2), image=self.img, state="normal")
        #self.TEST_sin()   # testing - draws a sin wave
        self.show_grid_from_file(fname)

        self.update()

        
    def TEST_sin(self):    
        for x in range(4 * self.appWidth):
            y = int(self.appHeight/2 + self.appHeight/4 * math.sin(x/80.0))
            self.img.put("#ffffff", (x//4,y))
        self.canvas.pack()
        
    def update(self):
        print("UPDATING GUI")
        #self.pix = self.im.load()
        #for i in range(n):
        #    pix[x, y] = value
        
        self.canvas.pack()


    def show_grid_from_file(self, fname):
        """
        reads a saved grid file and paints it on the canvas
        """
        with open(fname, "r") as f:
            for y, row in enumerate(f):
                for x, val in enumerate(row):
                    self.draw_cell(y, x, val)


    def draw_cell(self, row, col, val):
       # print("drawing cell: ", row, col, val)
        if val == '.':
            self.paint_land(row,col)
        elif val == '#':
            self.paint_block(row,col)
        elif val == 'X':
            self.paint_hill(row,col)
        elif val == 'T':
            self.paint_target(row,col)
        elif val in ['1','2','3','4','5','6','7','8','9']:
            self.paint_agent_trail(row,col, val)
        elif val in ['A']:
            self.paint_agent_location(row,col)
            
    def paint_land(self, y, x):
        for i in range(0,self.cell_width):
            for j in range(0,self.cell_height):
                self.img.put('white', (y*self.cell_height+j, x*self.cell_width+i))
        
    def paint_block(self, y, x):
        for i in range(0,self.cell_width):
            for j in range(0,self.cell_height):
                self.img.put('black', (y*self.cell_height+j, x*self.cell_width+i))

    def paint_hill(self, y, x):
        for i in range(0,self.cell_width):
            for j in range(0,self.cell_height):
                self.img.put('green', (y*self.cell_height+j, x*self.cell_width+i))

    def paint_target(self, y, x):
        print("TARGET PRINTING")
        self.img.put('black', (y*self.cell_height, x*self.cell_width))
        for i in range(0,self.cell_width):
            for j in range(0,self.cell_height):
                self.img.put('yellow', (y*self.cell_height+j, x*self.cell_width+i))

    def paint_agent_trail(self, y, x, val):
        """
        paint an agent trail as ONE pixle to allow for multiple agent
        trails to be seen in the same cell
        """
        self.img.put(self.agent_color(val), (y*self.cell_height+int(val), x*self.cell_width))
        self.img.put(self.agent_color(val), (y*self.cell_height+int(val), x*self.cell_width+1))
        self.img.put(self.agent_color(val), (y*self.cell_height+int(val), x*self.cell_width+2))

    def paint_agent_location(self, y, x):
        for i in range(0,self.cell_width):
            for j in range(0,self.cell_height):
                self.img.put('red', (y*self.cell_height+j, x*self.cell_width+i))

    def agent_color(self, val):
        """
        gets a colour for agent 0 - 9
        """
        if val == '0': 
            colour = 'blue'
        elif val == '1':
            colour = 'pink'
        else:
            colour = 'red'
    
        
        return colour
                
if __name__ == "__main__":
    main()