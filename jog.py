from PIL import Image, ImageTk
import tkinter as tk
import argparse
import datetime
import cv2
import os

class Application:
    def __init__(self, output_path = "./"):
        """ Initialize application which uses OpenCV + Tkinter. It displays
            a video stream in a Tkinter window and stores current snapshot on disk """
        self.vs = cv2.VideoCapture("test.mp4") # capture video frames, 0 is your default video camera
        self.output_path = output_path  # store output path
        self.current_image = None  # current image from the camera
        self.prev_images = []  # Prev image from the camera

        self.door_img = cv2.imread("door.jpg")
        self.window = tk.Tk()  # initialize window object
        self.window.title("Correction module")  # set window title
        # self.destructor function gets fired when the window is closed
        self.window.protocol('WM_DELETE_WINDOW', self.destructor)

        self.images_frame = tk.Frame(self.window,width=1080, height=720)
        self.images_frame.pack(side="top")

        self.left_imageFrame = tk.Frame(self.images_frame, width=30, height=75)
        # self.left_imageFrame.pack(side="left", expand=True)
        self.left_imageFrame.pack(side="left")


        # Create a label which displays the camera feed
        self.center_imageFrame = tk.Frame(self.images_frame,width=512, height=360)
        self.center_imageFrame.pack(side="left")

        self.right_imageFrame = tk.Frame(self.images_frame, width=30, height=75)
        self.right_imageFrame.pack(side="left")

        self.left_panel = tk.Label(self.left_imageFrame)
        self.left_panel.pack(side="bottom",expand=True)
        self.left_panel.bind("<Button 1>",self.printcoords_left)


        self.center_panel = tk.Label(self.center_imageFrame) 
        self.center_panel.pack(side="left",expand=True)

        self.right_panel = tk.Label(self.right_imageFrame)
        self.right_panel.pack(side="left",expand=True)
        self.right_panel.bind("<Button 1>",self.printcoords_right)



        self.prev_next = tk.Frame(self.window)
        self.prev_next.pack(side="bottom")
        
        # create a button, that when pressed, will take the current frame and save it to file
        prev = tk.Button(self.prev_next,text="Previous Frame", command=self.prev_frame)
        # prev.grid(row=1, column=0,sticky =tk.N)
        prev.pack(side=tk.LEFT)
        
        next = tk.Button(self.prev_next,text="Next Frame", command=self.next_frame)
        # next.grid(row=1, column=1,sticky = tk.N)
        next.pack( side=tk.LEFT)
        self.next_frame()
        

        # start a self.video_loop that constantly pools the video sensor
        # for the most recently read frame
    
    def printcoords_left(self,event):
        print("left",event.x,event.y)
        # print(event.widget.find_closest(event.x, event.y))
    def printcoords_right(self,event):
        print("right",event.x,event.y)

        # print(event.widget.find_closest(event.x, event.y))

        #mouseclick event
        

    def update_left(self,image):
        """ Update left panel with current frame from video stream """
        cv2image = cv2.cvtColor(self.door_img, cv2.COLOR_BGR2RGBA)  # convert colors from BGR to RGBA
        current_image = Image.fromarray(cv2image)  # convert image for PIL
        imgtk = ImageTk.PhotoImage(image=current_image)  # convert image for tkinter
        self.left_panel.imgtk = imgtk  # anchor imgtk so it does not be deleted by garbage-collector
        self.left_panel.config(image=imgtk)

    def update_right(self,image):
        """ Update right panel with current frame from video stream """
        cv2image = cv2.cvtColor(self.door_img, cv2.COLOR_BGR2RGBA)  # convert colors from BGR to RGBA
        current_image = Image.fromarray(cv2image)  # convert image for PIL
        imgtk = ImageTk.PhotoImage(image=current_image)  # convert image for tkinter
        self.right_panel.imgtk = imgtk  # anchor imgtk so it does not be deleted by garbage-collector
        self.right_panel.config(image=imgtk)

    def prev_frame(self):
        """ Get previous frame from the video stream """
        if len(self.prev_images) > 0:
            self.current_image = self.prev_images.pop()
            self.update_left(self.current_image)
            self.update_right(self.current_image)
            cv2image = cv2.cvtColor(self.current_image, cv2.COLOR_BGR2RGBA)
            self.current_image = Image.fromarray(cv2image)  
            imgtk = ImageTk.PhotoImage(image=self.current_image)
            self.center_panel.imgtk = imgtk
            self.center_panel.config(image=imgtk)

    def next_frame(self):
        """ Get frame from the video stream and show it in Tkinter """
        ok, frame = self.vs.read()  # read frame from video stream
        if ok:  # frame captured without any errors
            self.prev_images.append(frame)
            self.update_left(frame)
            self.update_right(frame)
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)  # convert colors from BGR to RGBA
            self.current_image = Image.fromarray(cv2image)  # convert image for PIL
            imgtk = ImageTk.PhotoImage(image=self.current_image)  # convert image for tkinter
            self.center_panel.imgtk = imgtk  # anchor imgtk so it does not be deleted by garbage-collector
            self.center_panel.config(image=imgtk)  # show the image
        # self.window.after(30, self.video_loop)  # call the same function after 30 milliseconds

    # def take_snapshot(self):
    #     """ Take snapshot and save it to the file """
    #     ts = datetime.datetime.now() # grab the current timestamp
    #     filename = "{}.jpg".format(ts.strftime("%Y-%m-%d_%H-%M-%S"))  # construct filename
    #     p = os.path.join(self.output_path, filename)  # construct output path
    #     self.current_image.save(p, "JPEG")  # save image as jpeg file
    #     print("[INFO] saved {}".format(filename))

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