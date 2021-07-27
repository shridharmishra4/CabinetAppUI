import numpy as np
import cv2
import tkinter as tk
from PIL import Image,ImageTk
# import ImageTk

#Set up GUI
window = tk.Tk()  #Makes main window
window.wm_title("Test")
window.config(background="#FFFFFF")

#Graphics window
imageFrame = tk.Frame(window, width=600, height=500)
imageFrame.grid(row=0, column=0, padx=10, pady=2)

#Capture video frames

cap = cv2.VideoCapture("117.mp4")

buffer = []
ret, frame = cap.read()


while(ret):
    ret, frame = cap.read()
    # frame = cv2.flip(frame, 1)
    
    buffer.append(frame)



def down(e):
    if m == 0:
        print ('Down\n', e.char, '\n', e)
        global m
        m = 1

def up(e):
    if m == 1:
        print ('Up\n', e.char, '\n', e)
        global m
        m = 0

window.bind('<KeyPress>', down)
window.bind('<KeyRelease>', up)


def show_frame():
    _, frame = cap.read()
    # frame = cv2.flip(frame, 1)
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    display1.imgtk = imgtk #Shows frame for display 1
    display1.configure(image=imgtk)
    # display2.imgtk = imgtk #Shows frame for display 2
    # display2.configure(image=imgtk)
    # window.after(100, show_frame) 
    # next['command'] = window.after(1, show_frame)


display1 = tk.Label(imageFrame)
display1.grid(row=1, column=0, padx=10, pady=2)  #Display 1
next = tk.Button(text='next',command = show_frame)
next.grid(row=1, column=0) #Display 2
# next['command'] = window.after(1, show_frame)

#Slider window (slider controls stage position)
# sliderFrame = tk.Frame(window, width=600, height=100)
# sliderFrame.grid(row = 600, column=0, padx=10, pady=2)
def printcoords(event):
    #outputting x and y coords to console
    print (event.x,event.y)
#mouseclick event
window.bind("<Button 1>",printcoords)
show_frame() #Display
window.mainloop()  #Starts GUI