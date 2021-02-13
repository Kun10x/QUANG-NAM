import numpy as np 
from PIL import ImageGrab
import cv2
import time
import sys
import csv
maxInt = sys.maxsize
def make_coordinates(original_image, line_parameters):
	slope, intercept = line_parameters
	y1 = original_image.shape[0]
	y2 = int(y1*(3/5))
	x1 = int((y1 - intercept)/slope)
	x2 = int((y2 - intercept)/slope)

	return np.array([x1,y1,x2,y2])

def averaged_slope_intercept(original_image, lines):
	left_fit = []
	right_fit = []
	for line in lines:
		x1,y1,x2,y2 = line.reshape(4)
		parameters = np.polyfit((x1,x2), (y1,y2),1)
		slope = parameters[0]
		intercept = parameters[1]
		if slope < 0:
			left_fit.append((slope, intercept))
		else:
			right_fit.append((slope, intercept))

	left_fit_average = np.average(left_fit, axis=0)
	right_fit_average = np.average(right_fit, axis = 0)
	left_line = make_coordinates(original_image, left_fit_average)
	right_line = make_coordinates(original_image, right_fit_average)
	return np.array([left_line,right_line])

def process_img(original_image):
	processed_img = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
	blur = cv2.GaussianBlur(processed_img,(5,5),0)
	canny = cv2.Canny(blur, threshold1=50, threshold2=150)
	return canny
def display_lines(original_image,lines):
	line_image = np.zeros_like(original_image)
	if lines is not None:
		for x1,y1,x2,y2 in lines:
			cv2.line(line_image, (x1,y1), (x2,y2), (255,0,0), 10)
			
	return line_image







def region_of_interest(original_image):
	height = original_image.shape[0]
	polygons = np.array([
	[(100,height), (800,height), (350,250)]
	])
	mask = np.zeros_like(original_image)
	cv2.fillPoly(mask, polygons, 255)
	maksed_image = cv2.bitwise_and(original_image, mask)

	return maksed_image


last_time = time.time()
while(True):
	screen = np.array(ImageGrab.grab(bbox=(0,40,800,640)))
	new_screen = process_img(screen)
	cropped_image = region_of_interest(new_screen)
	lines = cv2.HoughLinesP(cropped_image, 2,np.pi/180, 100, np.array([]), minLineLength=40, maxLineGap=5)
	averaged_lines = averaged_slope_intercept(screen, lines)
	line_image = display_lines(screen, averaged_lines)
	print('Loop took {} seconds' .format(time.time()-last_time))
	last_time = time.time()
	combo_image = cv2.addWeighted(screen, 0.8,line_image, 1, 1)
	cv2.imshow('window', combo_image)
	#cv2.imshow('window', cv2.cvtColor(screen, cv2.COLOR_BGR2RGB))
	if cv2.waitKey(25) & 0xFF == ord('q'):
		cv2.destroyAllWindows()
		break