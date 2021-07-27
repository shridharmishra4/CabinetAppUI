import sys
import tkinter as tk
from tkinter import Canvas, filedialog
from PIL import Image, ImageTk
from collections import defaultdict
import argparse
import cv2

class Application:
    def __init__(self, output_path = "./"):
        """ Initialize application which uses OpenCV + Tkinter. It displays
            a video stream in a Tkinter window and stores current snapshot on disk """
        self.vs = cv2.VideoCapture("test.mp4") # capture video frames, 0 is your default video camera
        self.output_path = output_path  # store output path
        self.current_image = None  # current image from the camera
        self.prev_images = []  # Prev image from the camera
        self.prev_map = []
        self.window = tk.Tk()  # initialize window object

        self.img = ImageTk.PhotoImage(file = "door.jpg")
        # self.img = cv2.imread("door.jpg")
        self.left_cell_state = defaultdict(dict)
        self.right_cell_state = defaultdict(dict)
        self.temp_images = []
        self.left_rect_list = {}
        self.right_rect_list = {}
        self.current_frame = 0
        self.n = 5

        self.width, self.height = self.img.width(), self.img.height()
        # Padding stuff: xsize, ysize is the cell size in pixels (without pad).
        self.pad = 0

        self.xsize = (self.width) / self.n 
        self.ysize = (self.height) / self.n

        c_width, c_height = self.img.width(), self.img.height()

        self.window.title("Correction module")  # set window title
        # self.destructor function gets fired when the window is closed
        self.window.protocol('WM_DELETE_WINDOW', self.destructor)

        self.images_frame = tk.Frame(self.window,width=1080, height=720)
        self.images_frame.pack(side="top")

        self.left_imageFrame = tk.Canvas(self.images_frame, width=c_width, height=c_height)
        self.left_imageFrame.addtag_all("left")
        # self.left_imageFrame.pack(side="left", expand=True)
        self.left_imageFrame.create_image(0,0,image=self.img, anchor="nw")
        self.left_imageFrame.pack(side="left")


        # Create a label which displays the camera feed
        self.center_imageFrame = tk.Frame(self.images_frame,width=512, height=360)
        self.center_imageFrame.pack(side="left")

        self.right_imageFrame = tk.Canvas(self.images_frame, width=c_width, height=c_height)
        self.right_imageFrame.create_image(0,0,image=self.img, anchor="nw")
        self.right_imageFrame.pack(side="left")
        self.right_imageFrame.addtag_all("right")

        # self.left_panel = tk.Label(self.left_imageFrame)
        # self.left_panel.pack(side="bottom",expand=True)
        # self.left_panel.bind("<Button 1>",self.printcoords)
        self.left_imageFrame.bind('<ButtonPress-1>', self.left_click_callback)
        self.right_imageFrame.bind('<ButtonPress-1>', self.right_click_callback)

 
        self.center_panel = tk.Label(self.center_imageFrame) 
        self.center_panel.pack(side="left",expand=True)

        # self.right_panel = tk.Label(self.right_imageFrame)
        # self.right_panel.pack(side="left",expand=True)
        # self.right_panel.bind("<Button 2>",self.printcoords)

        self.prev_next = tk.Frame(self.window)
        self.prev_next.pack(side="bottom")
        
        # create a button, that when pressed, will take the current frame and save it to file
        prev = tk.Button(self.prev_next,text="Previous Frame", command=self.prev_frame)
        # prev.grid(row=1, column=0,sticky =tk.N)
        prev.pack(side=tk.LEFT)
        
        next = tk.Button(self.prev_next,text="Next Frame", command=self.next_frame)
        # next.grid(row=1, column=1,sticky = tk.N)
        next.pack( side=tk.LEFT)

        self.window.bind('<d>', self.next_frame)
        self.window.bind('<a>', self.prev_frame)

        self.next_frame()
        

        # start a self.video_loop that constantly pools the video sensor
        # for the most recently read frame
    

        #mouseclick event
    
    def draw_grid(self,canvas):
        self.cells = []
        
        for iy in range(self.n):
            for ix in range(self.n):
                i = iy*self.n+ix
                xpad, ypad = self.pad * (ix+1), self.pad * (iy+1) 
                x, y = xpad + ix*self.xsize, ypad + iy*self.ysize
                # rect = canvas.create_rectangle(int(x), int(y), int(x+self.xsize),
                #                            int(y+self.ysize), fill="")
                self.left_cell_state[i]["coordinates"] = [int(x), int(y), int(x+self.xsize),
                                           int(y+self.ysize)]
                self.left_cell_state[i]["clicked"] = False
                self.left_cell_state[i]["clicked"] = False

                self.right_cell_state[i]["coordinates"] = [int(x), int(y), int(x+self.xsize),
                                           int(y+self.ysize)]
                self.right_cell_state[i]["clicked"] = False

                rect = self.create_translucent_rectangle(canvas,int(x), int(y), int(x+self.xsize),
                            int(y+self.ysize), fill="")
                self.cells.append(rect)
    
    def create_translucent_rectangle(self,canvas, x1, y1, x2, y2, **kwargs):

        """Create a rectangle with coordinates (x1, y1) and (x2, y2)"""

        if 'alpha' in kwargs:
            alpha = int(kwargs.pop('alpha') * 255)
            fill = kwargs.pop('fill')
            fill = canvas.winfo_rgb(fill) + (alpha,)
            image = Image.new('RGBA', (x2-x1, y2-y1), fill)
            self.temp_images.append(ImageTk.PhotoImage(image))
            # canvas.imgtk = image
            return canvas.create_image(x1, y1, image=self.temp_images[-1], anchor=tk.NW)
        return canvas.create_rectangle(x1, y1, x2, y2, **kwargs)




    def left_click_callback(self,event):
            """Function called when someone clicks on the grid canvas."""
            x, y = event.x, event.y
            # Did the user click a cell in the grid?
            # Indexes into the grid of cells (including padding)
            ix = int(x // (self.xsize + self.pad))
            iy = int(y // (self.ysize + self.pad))
            xc = x - ix*(self.xsize + self.pad) - self.pad
            yc = y - iy*(self.ysize + self.pad) - self.pad
            if ix < self.n and iy < self.n and 0 < xc < self.xsize and 0 < yc < self.ysize:
                i = iy*self.n+ix
                # self.left_imageFrame.itemconfig(self.cells[i], fill="blue",stipple="gray50")
                coord = self.left_cell_state[i]["coordinates"]

                if not self.left_cell_state[i]["clicked"]:
                    self.left_cell_state[i]["clicked"] = True
                    im = self.create_translucent_rectangle(self.left_imageFrame,coord[0],
                                                    coord[1], coord[2], coord[3], 
                                                    fill="red",alpha=0.5)
                    self.left_rect_list[i] = im
                else:
                    # print(self.left_cell_state[i])
                    self.left_cell_state[i]["clicked"] = False
                    self.left_imageFrame.delete(self.left_rect_list[i])
                    # print(self.left_cell_state[i])
    
    def right_click_callback(self,event):
            """Function called when someone clicks on the grid canvas."""
            x, y = event.x, event.y

            # Did the user click a cell in the grid?
            # Indexes into the grid of cells (including padding)
            ix = int(x // (self.xsize + self.pad))
            iy = int(y // (self.ysize + self.pad))
            xc = x - ix*(self.xsize + self.pad) - self.pad
            yc = y - iy*(self.ysize + self.pad) - self.pad
            if ix < self.n and iy < self.n and 0 < xc < self.xsize and 0 < yc < self.ysize:
                i = iy*self.n+ix
                # self.right_imageFrame.itemconfig(self.cells[i], fill="blue",stipple="gray50")
                coord = self.right_cell_state[i]["coordinates"]
                if not self.right_cell_state[i]["clicked"]:
                    self.right_cell_state[i]["clicked"] = True
                    im = self.create_translucent_rectangle(self.right_imageFrame,coord[0],
                                                    coord[1], coord[2], coord[3], 
                                                    fill="red",alpha=0.5)
                    self.right_rect_list[i] = im
                else:
                    self.right_cell_state[i]["clicked"] = False
                    self.right_imageFrame.delete(self.right_rect_list[i])

    
    
    def update_next_sides(self,image):
        """ Update canvas when next is clicked """
        # cv2image = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGBA)  # convert colors from BGR to RGBA
        # current_image = Image.fromarray(cv2image)  # convert image for PIL
        # imgtk = ImageTk.PhotoImage(image=current_image)  # convert image for tkinter
        # self.left_panel.imgtk = imgtk  # anchor imgtk so it does not be deleted by garbage-collector
        # self.left_panel.config(image=imgtk)
        self.left_imageFrame.create_image(0,0,image=self.img, anchor="nw")
        self.draw_grid(self.left_imageFrame)
        self.right_imageFrame.create_image(0,0,image=self.img, anchor="nw")
        self.draw_grid(self.right_imageFrame)

    def update_prev_sides(self,image):
        """ Update canvas when prev is clicked """
        # cv2image = cv2.cvtColor(self.door_img, cv2.COLOR_BGR2RGBA)  # convert colors from BGR to RGBA
        # current_image = Image.fromarray(cv2image)  # convert image for PIL
        # imgtk = ImageTk.PhotoImage(image=current_image)  # convert image for tkinter
        # self.right_panel.imgtk = imgtk  # anchor imgtk so it does not be deleted by garbage-collector
        # self.right_panel.config(image=imgtk)
        self.left_imageFrame.create_image(0,0,image=self.img, anchor="nw")
        self.draw_grid(self.left_imageFrame)
        self.right_imageFrame.create_image(0,0,image=self.img, anchor="nw")
        self.draw_grid(self.right_imageFrame)


    def prev_frame(self,*_):
        """ Get previous frame from the video stream """
        if len(self.prev_images) > 0:
            self.current_frame -= 1
            self.current_image = self.prev_images.pop()
            self.update_prev_sides(self.current_image)
            # self.update_right(self.current_image)
            cv2image = cv2.cvtColor(self.current_image, cv2.COLOR_BGR2RGBA)
            self.current_image = Image.fromarray(cv2image)  
            imgtk = ImageTk.PhotoImage(image=self.current_image)
            self.center_panel.imgtk = imgtk
            self.center_panel.config(image=imgtk)

    def next_frame(self,*_):
        """ Get frame from the video stream and show it in Tkinter """
        ok, frame = self.vs.read()  # read frame from video stream
        if ok:  # frame captured without any errors
            self.current_frame += 1
            self.prev_images.append(frame)
            self.update_next_sides(frame)
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)  # convert colors from BGR to RGBA
            self.current_image = Image.fromarray(cv2image)  # convert image for PIL
            imgtk = ImageTk.PhotoImage(image=self.current_image)  # convert image for tkinter
            self.center_panel.imgtk = imgtk  # anchor imgtk so it does not be deleted by garbage-collector
            self.center_panel.config(image=imgtk)  # show the image
        # self.window.after(30, self.video_loop)  # call the same function after 30 milliseconds

    def _get_cell_coords(self, i):
        """Get the <letter><number> coordinates of the cell indexed at i."""

        # The horizontal axis is labelled A, B, C, ... left-to-right;
        # the vertical axis is labelled 1, 2, 3, ... bottom-to-top.
        iy, ix = divmod(i, self.n)
        return '{}{}'.format(chr(ix+65), self.n-iy)
    
    def destructor(self):
        """ Destroy the window object and release all resources """
        print("[INFO] closing...")
        self.window.destroy()
        self.vs.release()  # release web camera
        cv2.destroyAllWindows()  # it is not mandatory in this application

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-o", "--output", default="./",
    help="path to output directory to store snapshots (default: current folder")
args = vars(ap.parse_args())

# start the app
print("[INFO] starting...")
pba = Application(args["output"])
pba.window.mainloop()