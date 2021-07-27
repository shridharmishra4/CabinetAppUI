import numpy as np
import cv2
from copy import deepcopy

# top left, top right, bottom left, bottom right

pointIndex = 0

cam = cv2.VideoCapture("117.mp4")

_,img = cam.read()
_,img = cam.read()

window_name = 'Image'
  
# font
font = cv2.FONT_HERSHEY_SIMPLEX
  
# org
org = (200, 50)
  
# fontScale
fontScale = 1
   
color = (0, 255, 0)
  
thickness = 2

text_img = deepcopy(img)
image = cv2.putText(text_img, 'Enter number of visible corners', org, font, 
                   fontScale, color, thickness, cv2.LINE_AA)
cv2.imshow('image',image)
key = cv2.waitKey(20)



# Size of cabinet
# Cabinet 
# height: 11
# width: 8.125 
# depth: 6
 
# Entire table top 
# length: 38.312
# width: 26.5
 
# Rectangle base that cabinet locks into on tabletop (including the frame)
# length: 9.25
# width: 7.8125

# For a different size, just change the value of this constant

# ASPECT_RATIO = (500,677)

# pts2 = np.float32([[0,0],[ASPECT_RATIO[1],0],[0,ASPECT_RATIO[0]],[ASPECT_RATIO[1],ASPECT_RATIO[0]]])
# mouse callback function
def draw_circle(event,x,y,flags,param):
	global img
	global pointIndex
	global pts

	if event == cv2.EVENT_LBUTTONDOWN:
		cv2.circle(img,(x,y),3,(0,0,255),-1)
		pts[pointIndex] = (x,y)
		pointIndex = pointIndex + 1

def selectnPoints():
	global img
	global pointIndex
	global pts


	# get number of points as input
	nPoints = input("Enter number of visible points: ")
	nPoints = int(nPoints)
	pts = [(0,0) for i in range(nPoints)]
	print ("Annotate visible points, by clicking on each of them")
	# pointIndex = 0	
	while(pointIndex != nPoints):
		cv2.imshow('image',img)
		key = cv2.waitKey(20) & 0xFF
		if key == 27:
			return False

	return True
# Create a black image, a window and bind the function to window
# img = np.zeros((512,512,3), np.uint8)

cv2.namedWindow('image')
cv2.setMouseCallback('image',draw_circle)

if (selectnPoints()):
	print(pts)
