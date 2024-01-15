import numpy as np
import cv2 as cv

im = cv.imread('input/img/contours.jpg')
hsv = cv.cvtColor(im,cv.COLOR_BGR2HSV)

light_blue = np.array([110,50,50])
dark_blue  = np.array([130,255,255])

light_green = np.array([48,0,153])
dark_green  = np.array([73,255,255])

mask = cv.inRange(hsv,light_blue,dark_blue)
#mask = cv.inRange(hsv,light_green,dark_green)
print(np.shape(mask))

output = cv.bitwise_and(im,im,mask=mask)
print(np.shape(output))

contours, _= cv.findContours(image=mask, mode=cv.RETR_EXTERNAL, method=cv.CHAIN_APPROX_NONE)
#print(contours)

#for c in contours:
#    peri   = cv.arclength(c, true)
#    approx = cv.approxpolydp(c, 0.04 * peri, true)
#    if len(approx) == 4:
#        print("found square!")
#        print(peri)
#        print(approx)


for i in range(len(contours)):
    area = cv.contourArea(contours[i])
    peri = cv.arcLength(contours[i], True)
    approx = cv.approxPolyDP(contours[i], 0.04 * peri, True)


    if area > 3000 and len(approx) == 4:
        cv.drawContours(output, contours[i], -1, (0, 0, 255), 3)
        print(np.shape(contours[i]))
        len_of_cont = len(contours[i])
        print(len_of_cont)
        centroid = (sum(contours[i][:,0,0]) / len_of_cont, sum(contours[i][:,0,1]) / len_of_cont, 1)
        print(int(centroid[0]),int(centroid[1]))
        print("color:",centroid[2])
        output = cv.circle(output, (int(centroid[0]),int(centroid[1])), radius=0,color=(0,255,0),thickness=3)

cv.imshow("color detection",output)
cv.waitKey(0)
