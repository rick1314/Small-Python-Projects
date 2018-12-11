import cv2
import numpy as np
import pyautogui
import random
import time

def mse(imageA, imageB):
	# the 'Mean Squared Error' between the two images is the
	# sum of the squared difference between the two images;
	# NOTE: the two images must have the same dimension
	err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
	err /= float(imageA.shape[0] * imageA.shape[1])
	
	# return the MSE, the lower the error, the more "similar"
	# the two images are
	return err

	
'''

grabs a region (topx, topy, bottomx, bottomy)
to the tuple (topx, topy, width, height)

input : a tuple containing the 4 coordinates of the region to capture

output : a PIL image of the area selected.

'''
def region_grabber(region):
    x1 = region[0]
    y1 = region[1]
    width = region[2]
    height = region[3]

    return pyautogui.screenshot(region=(x1,y1,width,height))

'''
Searchs for an image on the screen

input :

image : path to the image file (see opencv imread for supported types)
precision : the higher, the lesser tolerant and fewer false positives are found default is 0.8
im : a PIL image, usefull if you intend to search the same unchanging region for several elements

returns :
the top left corner coordinates of the element if found as an array [x,y] or [-1,-1] if not

'''
def imagesearch(image,im, precision=0.7):
#    im = pyautogui.screenshot()
#    im.save('testarea.png') #usefull for debugging purposes, this will save the captured region as "testarea.png"
    img_rgb = np.array(im)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(image, 0)
    template.shape[::-1]

    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    if max_val < precision:
        return [-1,-1]
    return max_loc



def getPos(name,im):
	pos = imagesearch(name,im)
	if pos[0] != -1:
		print("position : ", pos[0], pos[1])
		#pyautogui.moveTo(pos[0], pos[1])
		position = (pos[0],pos[1])
		return position
	else:
		print("can't find")
		return -1
		
#all coordinates during game 

class Coordinates():
	im = pyautogui.screenshot()
	im.save('testarea.png')
	replayBtn = getPos("start.png",im)
	if replayBtn == -1:
		dino = getPos("head2.png",im)
		x1,y1 = dino
		x1 = x1+30
	else:
		dino = getPos("head.png",im)
		x1,y1 = dino
	region=(x1+30,y1,150,40)
	
def restartGame():
	if Coordinates.replayBtn != -1:
		pyautogui.click(Coordinates.replayBtn)
	else:
		pyautogui.click(Coordinates.dino)
		pressSpace()
		
def pressSpace():
	pyautogui.keyDown('space')
	time.sleep(0.05)
	pyautogui.keyUp('space')
	
def checkBuff():
	im = region_grabber(Coordinates.region) 
	im.save('testarea2.png')
	img = np.array(im)
	im_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	buffer = cv2.imread("bufferzone.png")
	im_buff = cv2.cvtColor(buffer, cv2.COLOR_BGR2GRAY)
	
	if mse(im_gray, im_buff) == 0:
		print("clear buffer")
		#time.sleep(0.25)
		
	else:
		print("jumping!")
		#time.sleep(0.25)
		pressSpace()
		#im.save('area.png')
		
	#im_gray.save('areaGray.png')
	#put getting the buffer region and checking code here.
	#need a buffer image during game running
	
restartGame()
time.sleep(2)
while(True):
	checkBuff()

#program keeps running till buffer is no longer, then we jump.

