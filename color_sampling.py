import cv2
import numpy as np
import csv

def nothing(x):
    pass

cv2.namedWindow("Tracking")
cv2.createTrackbar("LH", "Tracking", 0, 255, nothing)
cv2.createTrackbar("LS", "Tracking", 0, 255, nothing)
cv2.createTrackbar("LV", "Tracking", 0, 255, nothing)
cv2.createTrackbar("UH", "Tracking", 255, 255, nothing)
cv2.createTrackbar("US", "Tracking", 255, 255, nothing)
cv2.createTrackbar("UV", "Tracking", 255, 255, nothing)

#cam = cv2.VideoCapture(0)
frame = cv2.imread('input/contours02.jpg')

color_values = np.empty([6,6], dtype=int)
count = 0

while(True):

    #ret, frame = cam.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    l_h = cv2.getTrackbarPos("LH", "Tracking")
    l_s = cv2.getTrackbarPos("LS", "Tracking")
    l_v = cv2.getTrackbarPos("LV", "Tracking")

    u_h = cv2.getTrackbarPos("UH", "Tracking")
    u_s = cv2.getTrackbarPos("US", "Tracking")
    u_v = cv2.getTrackbarPos("UV", "Tracking")

    l_b = np.array([l_h, l_s, l_v])
    u_b = np.array([u_h, u_s, u_v])

    mask = cv2.inRange(hsv, l_b, u_b)
    res  = cv2.bitwise_and(frame, frame, mask=mask)

    cv2.imshow("Live Tranmission", frame)
    cv2.imshow("mask", mask)
    cv2.imshow("res", res)
    key = cv2.waitKey(5)
    if key==ord('s') and count<6:
        color_values[:][count] = [l_h, l_s, l_v, u_h, u_s, u_v]
        count = count + 1

    if key==ord('q'):
        break

cv2.destroyAllWindows()

file = open("samples.txt", "w+")
content = str(color_values)
file.write(content)
file.close()

with open('colors_1.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(color_values)

print(color_values)

