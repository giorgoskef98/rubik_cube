from cv2 import *

cam_port = 0
cam = VideoCapture(cam_port)

result, image = cam.read()

if result:
    #Show the image
    imshow("Image001", image)

    #Save the image
    imwrite('Image001.jpg',image)

    waitKey(0)
    #destroyWindow("Image001")

else:
    print("Error! Image isn't captured")


