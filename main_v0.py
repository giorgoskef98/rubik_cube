import numpy as np
import cv2 as cv
import pandas as pd
import lib.defines as defines

# ------------------------------------------------------------
def read_colors_csv():
    colors_dict = {}
    color_data = pd.read_csv(defines.COLORS_DIR+defines.COLORS_FILE,header = None)
    raw_data = color_data.values.tolist()
    for i in range(len(defines.colors)):
        colors_dict[defines.colors[i]] = {'Light': raw_data[i][0:3], 'Dark': raw_data[i][3:6]}
    return colors_dict

# ------------------------------------------------------------
def print_colors_dict(color_dict):
    for i in defines.colors:
        print(i,color_dict[i]) 

# ------------------------------------------------------------
def read_image():
    return cv.imread(defines.IMAGE_DIR+defines.IMAGE_FILE)

# ------------------------------------------------------------
def read_image_file(file_name):
    return cv.imread(file_name)

# ------------------------------------------------------------
def get_hsv(im):
    return cv.cvtColor(im,cv.COLOR_BGR2HSV)

# ------------------------------------------------------------
def get_mask(hsv, light_color, dark_color):
    return cv.inRange(hsv, np.array(light_color), np.array(dark_color))

# ------------------------------------------------------------
def get_bitwise_image(im,mask):
    return cv.bitwise_and(im, im, mask=mask)

# ------------------------------------------------------------
def find_index(VALS):
    bot_index = 0
    max       = VALS[bot_index][1]    

    if VALS[1][1] > max:
        max       = VALS[1][1]
        bot_index = 1

    if VALS[2][1] > max:
        max = VALS[2][1]
        bot_index = 2    

    if bot_index == 0:
        top_index = 2
        mid_index = 1
        if VALS[top_index][1] > VALS[mid_index][1]:
            top_index = 1
            mid_index = 2

    elif bot_index == 1:
        top_index = 2
        mid_index = 0
        if VALS[top_index][1] > VALS[mid_index][1]:
            top_index = 0
            mid_index = 2
    
    elif bot_index == 2:
        top_index = 1
        mid_index = 0
        if VALS[top_index][1] > VALS[mid_index][1]:
            top_index = 0
            mid_index = 1

    if defines.PRINT_INDEX_CALCULATION: 
        print("Top Index: "+str(top_index)+", Value: "+VALS[top_index][1]+", Color: "+VALS[top_index][2])
        print("Mid Index: "+str(mid_index)+", Value: "+VALS[mid_index][1]+", Color: "+VALS[mid_index][2])
        print("Bot Index: "+str(bot_index)+", Value: "+VALS[bot_index][1]+", Color: "+VALS[bot_index][2])

    return [VALS[bot_index][2], VALS[mid_index][2], VALS[top_index][2]]

# ------------------------------------------------------------
def get_all_side_colors(file_name):
    color_data   = read_colors_csv()
    if defines.PRINT_COLOR_DICT:
        print_colors_dict(color_data)
        print("----------------------------------------------")

    image  = read_image_file(file_name)
    hsv    = get_hsv(image)
    #Start colors
    centers = []
    for color in color_data:
        if defines.PRINT_CENTERS_DETAILS:
            print("======================================")
            print(color)

        mask   = get_mask(hsv, color_data[color]['Light'], color_data[color]['Dark'])
        output = get_bitwise_image(image, mask)

        contours, hierarchy= cv.findContours(image=mask, mode=cv.RETR_EXTERNAL, method=cv.CHAIN_APPROX_NONE)

        for contour in contours:
            area = cv.contourArea(contour)
            peri = cv.arcLength(contour, True)
            approx = cv.approxPolyDP(contour, 0.04 * peri, True)

            if area > defines.MIN_RECTANGLE_AREA and len(approx) == defines.NUM_OF_RECTANGLE_SIDES:
                cv.drawContours(output, contour, -1, defines.DRAW_COLOR, defines.THICKNESS)
                len_of_cont = len(contour)
                centroid = (sum(contour[:,0,0]) / len_of_cont, sum(contour[:,0,1]) / len_of_cont, color)
                centers.append([int(centroid[0]), int(centroid[1]), centroid[2]])
                output = cv.circle(output, (int(centroid[0]),int(centroid[1])), radius=0,color=defines.DRAW_COLOR,thickness=defines.THICKNESS)

                if defines.PRINT_CENTERS_DETAILS:
                    print("center:  ",int(centroid[0]),int(centroid[1]),", color:",centroid[2])
        
        if defines.IMSHOW_COLOR_MASK:
            cv.imshow("color detection",output)
            cv.waitKey(0)

    if (len(centers) > defines.MAX_RECTANGLES_FOUND):
        print("Error! Found more than 9 rectagles. Better Calibrationis needed!")

    if defines.PRINT_CENTERS_DETAILS:
        print("======================================")
    
    return centers

# ------------------------------------------------------------
def form_side(centers):
    X      = np.array(centers)[:,0]
    Y      = np.array(centers)[:,1]
    COLORS = np.array(centers)[:,2]

    RIGHT_VALS  = sorted(zip(X, Y, COLORS), reverse=True)[:3]
    RIGHT_COLORS  = find_index(RIGHT_VALS)
    if defines.PRINT_SIDE_CALCULATION:
        print(RIGHT_VALS)
        print("----------------------------------------------")

    MID_VALS   = sorted(zip(X, Y, COLORS), reverse=True)[3:6]
    MID_COLORS   = find_index(MID_VALS)
    if defines.PRINT_SIDE_CALCULATION:
        print(MID_VALS)
        print("----------------------------------------------")

    LEFT_VALS = sorted(zip(X, Y, COLORS), reverse=True)[6:9]
    LEFT_COLORS = find_index(LEFT_VALS)
    if defines.PRINT_SIDE_CALCULATION:
        print(LEFT_VALS)
        print("----------------------------------------------")

    side = np.array([[LEFT_COLORS[2], MID_COLORS[2], RIGHT_COLORS[2]],[LEFT_COLORS[1], MID_COLORS[1], RIGHT_COLORS[1]],[LEFT_COLORS[0], MID_COLORS[0], RIGHT_COLORS[0]]])
    
    return side

# ------------------------------------------------------------
#                           __main__
# ------------------------------------------------------------
centers = get_all_side_colors("input/img/contours01.jpg")
side = form_side(centers)

print('                           '+str(side[0]))
print('                           '+str(side[1]))
print('                           '+str(side[2]))
print()

print('                           '+str(side[0]))
print('                           '+str(side[1]))
print('                           '+str(side[2]))
print()

print(str(side[0])+'  '+str(side[0])+'  '+str(side[0]))
print(str(side[1])+'  '+str(side[1])+'  '+str(side[1]))
print(str(side[2])+'  '+str(side[2])+'  '+str(side[2]))
print()

print('                           '+str(side[0]))
print('                           '+str(side[1]))
print('                           '+str(side[2]))
print()



