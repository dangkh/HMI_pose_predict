# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import cv2
import numpy as np
from utility import readLookupTable, readSkeleton
#------------------GolbalVariable----
resizedFrame = []
ske = []
table = []
img = None
pos = 0
cap = 0
dang_window_size = [600,600]
draged_list = []
edited = False
edit_to_track = False
auto_tracking = False
length = 0
track_pos = 0

# parameter for tracking Lucas
lk_params = dict( winSize  = (15,15),
                  maxLevel = 2,
                  criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

#Draw skeleton
def draw_skeleton(inputframe, one_ske, table):
	draw_frame = inputframe.copy()
	i = 0	
	# compute the middle of the hip
	centerHipY = (one_ske[4][0]+one_ske[5][0])/2
	centerHipX = (one_ske[4][1]+one_ske[5][1])/2
	centerHip = (centerHipY, centerHipX)
	cv2.line(draw_frame, one_ske[1], centerHip, blue, thickness)
	for xy in table:
		cv2.line(draw_frame, one_ske[xy[0]], one_ske[xy[1]], colors[i], thickness)        
		#draw joints
		cv2.circle(draw_frame, one_ske[xy[0]], joint_r, green, 2)
		cv2.circle(draw_frame, one_ske[xy[1]], joint_r, green, 2)
		i = i + 1
	cv2.resizeWindow('mywindow', dang_window_size[0], dang_window_size[1])
	cv2.imshow('mywindow',draw_frame)
	return draw_frame


# find nearest image doesnt have error
def get_valid_ske(value):
	result = value
	while len(ske[result]) == 0:
		result -= 1
		if result < 0: 
			break
	return result


def onChange(trackbarValue):
    global pos, cap, img
    pos = trackbarValue
    cap.set(cv2.CAP_PROP_POS_FRAMES,trackbarValue)
    err,img = cap.read()    
    try:
    	image_need = get_valid_ske(trackbarValue)
    	# auto tracking using OF
        if auto_tracking and edit_to_track:
        	print "auto_tracking"
        	tracking_OF()	
     #    cap.set(cv2.CAP_PROP_POS_FRAMES,trackbarValue)
    	# err,img = cap.read()
        draw_skeleton(img, ske[image_need], table)
    except Exception, e:
        print e
    pass


def onChange1(value):
	global auto_tracking
	auto_tracking = True if value == 1 else False

def checkNearby(m, one_ske):# m, r, p stands for mouse, radius, point (joint)
	#print "Checking ", m
	r = 10
	k = 0 #for index of joint
	for p in one_ske:
		#print p , m
		if (abs(p[1]-m[1])<r) and (abs(p[0]-m[0])<r):
			print "Ok " , k
			return k
		k = k + 1
	return -1

#Tracking function




def tracking_OF():
	global edit_to_track, ske, cap
	# print track_pos
	cap.set(cv2.CAP_PROP_POS_FRAMES,track_pos)
	old_err,old_img = cap.read()
	old_img = cv2.cvtColor(old_img, cv2.COLOR_BGR2GRAY)
	point = ske[track_pos]
	point = np.asarray(point, dtype=np.float32)
	for i in range(track_pos, length-1):
		cap.set(cv2.CAP_PROP_POS_FRAMES,i+1)
		new_err,new_img = cap.read()
		new_img = cv2.cvtColor(new_img, cv2.COLOR_BGR2GRAY)
		newpoint, st, err = cv2.calcOpticalFlowPyrLK(old_img, new_img, point, None, **lk_params)
		
		point = newpoint
		old_img = new_img
		
		newpoint = newpoint.astype(int)
		ske_new = []
		for j in range(len(newpoint)):
			ske_new.append(tuple([newpoint[j][0],newpoint[j][1]]))
		ske[i+1] = ske_new
	edit_to_track = False
	print("ok track done", track_pos)


#Drag function
moving = False
def click_and_drag(event, x, y, flags, param):
	global moving, pos, img, edited, edit_to_track, track_pos
	if event == cv2.EVENT_LBUTTONDOWN:
		#Check click nearby joint with radius of r pixcels
		if checkNearby((x,y), ske[pos]) >= 0:
			moving = True
		else:
			moving = False
	if event == cv2.EVENT_MOUSEMOVE:
		if moving:
			edited = True
			draged_list[pos] = True
			#update moving joint
			k = checkNearby((x,y), ske[pos])
			if k >= 0:
				ske[pos][k] = (x,y)
			else:
				moving = False			
			#draw
			track_pos = pos
			edit_to_track = True
			draw_skeleton(img, ske[pos], table)
	if event == cv2.EVENT_LBUTTONUP:
		moving = False
        
#Gen 14 different colors for 14 edges
def gen_colors():
	delta = 256/4;
	colors = []
	for i in range(0,4):
		for j in range(0,4):
			for k in range(0,4):
				colors.append((delta*i, delta*j, delta *k))
	return colors

#------------------Skeleton-style---------------
red = (0, 0, 255)
green = (0, 255, 0)
blue = (255, 0, 0)
thickness = 10
joint_r = 5
colors = gen_colors()
#------------------EndOfSkeletonStyle-----------


def run(filename):

    global table, ske, img, cap, draged_list, edited,length

    table = readLookupTable("lookup.skeleton")
    ske = readSkeleton(filename.split('.')[0] + ".skeleton")# Read the stored skeleton
    cap = cv2.VideoCapture(filename)
    length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    draged_list = [False] * length
    cv2.namedWindow('mywindow', cv2.WINDOW_NORMAL)
    
    cv2.setMouseCallback('mywindow',click_and_drag)
    cv2.createTrackbar( 'start', 'mywindow', 0, length, onChange )
    switch = 'auto tracking \n 0 : OFF \n1 : ON \n'
    cv2.createTrackbar( switch, 'mywindow', 0, 1, onChange1 )
    onChange(0)
    onChange1(0)
    while (True):
    	k = cv2.waitKey(1) & 0xFF
    	if k == ord('q'):
    		break
    	start = cv2.getTrackbarPos('start','mywindow')
    	cap.set(cv2.CAP_PROP_POS_FRAMES,start)

    #while cap.isOpened():
    #    err,img = cap.read()    
    #    cv2.imshow("mywindow", img)
    #    k = cv2.waitKey(10) & 0xff
    #    if k==27:
    #        break
    cap.release()
    cv2.destroyAllWindows()
    return ske, edited