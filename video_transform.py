import numpy as np
import cv2


# top left, top right, bottom left, bottom right
pts = [(0, 0), (0, 0), (0, 0), (0, 0)]
pointIndex = 0

cam = cv2.VideoCapture("117.mp4")

_, img = cam.read()
_, img = cam.read()

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

ASPECT_RATIO = (500, 677)

# pts2 = np.float32([[0,0],[ASPECT_RATIO[1],0],[0,ASPECT_RATIO[0]],[ASPECT_RATIO[1],ASPECT_RATIO[0]]])
pts2 = np.float32([[0, 0], [ASPECT_RATIO[0],0], [0,ASPECT_RATIO[1]], [ASPECT_RATIO[0], ASPECT_RATIO[1]]])


# mouse callback function
def draw_circle(event, x, y, flags, param):
    global img
    global pointIndex
    global pts

    if event == cv2.EVENT_LBUTTONDOWN:
        cv2.circle(img, (x, y), 5, (0, 0, 255), -1)
        pts[pointIndex] = (x, y)
        pointIndex = pointIndex + 1


def selectFourPoints():
    global img
    global pointIndex

    print("Please select 4 points, by double clicking on each of them in the order: \n\
	top left, top right, bottom left, bottom right.")

    while (pointIndex != 4):
        cv2.imshow('image', img)
        key = cv2.waitKey(20) & 0xFF
        if key == 27:
            return False

    return True


# Create a black image, a window and bind the function to window
# img = np.zeros((512,512,3), np.uint8)

cv2.namedWindow('image')
cv2.setMouseCallback('image', draw_circle)

while (1):
    if (selectFourPoints()):
        # The four points of the A4 paper in the image
        pts1 = np.float32([ \
            [pts[0][0], pts[0][1]], \
            [pts[1][0], pts[1][1]], \
            [pts[2][0], pts[2][1]], \
            [pts[3][0], pts[3][1]]])

        M = cv2.getPerspectiveTransform(pts1, pts2)

        while (1):

            _, frame = cam.read()

            dst = cv2.warpPerspective(frame, M, (ASPECT_RATIO[0], ASPECT_RATIO[1]))
            cv2.imshow("output", dst)

            key = cv2.waitKey(10) & 0xFF
            if key == 27:
                break
    else:
        print("Exit")
    break
# cv2.imshow('image',img)
# if cv2.waitKey(20) & 0xFF == 27:
# 	break
cam.release()
cv2.destroyAllWindows()
