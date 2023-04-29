import cv2
import numpy as np
import os
import time
import math

from module import utils as ut
from module import hand_tracking as htm

# The above code is importing the utils.py file and assigning the BRUSH_THICKNESS variable to the
# brushThickness variable.
brushThickness = ut.BRUSH_THICKNESS

# Assigning the value of the variable named "timer" to the variable named "TIMER" from the file named
# "utils.py".
timer = ut.TIMER

# Assigning the value of the variable named "header_imgs" to a list of images from the folder named
# "header".
header_imgs = [cv2.imread(ut.HEADER_FOLDER + '/' + img) for img in os.listdir(ut.HEADER_FOLDER)]

# Assigning the first image in the list named "header_imgs" to the variable named "menu_img" and the
# second image in the list named "header_imgs" to the variable named "header".
menu_img = header_imgs.pop(0)
header = header_imgs[0]

# Assigning the value of the variable named "draw_color" to the tuple (255, 0, 0) (blue).
draw_color = (255, 38, 0)

# Capturing the video from the webcam.
cap = cv2.VideoCapture(0)

# Setting the width and height of the video capture.
cap.set(3, 1280)
cap.set(4, 720)

# Creating an object of the class named "HandDetector" from the file named "hand_tracking.py" and
# assigning it to the variable named "detector".
detector = htm.HandDetector(detectionCon=0.85)

# Setting the initial value of the variables named "xp" and "yp" to 0.
xp, yp = 0, 0

# Creating a black image of size 720x1280.
imgCanvas = np.zeros((720, 1280, 3), np.uint8)

# Creating a white image of size 720x1280.
imgSaves = np.ones((720, 1280,3),np.uint8)*255

# Setting the value of the variable named "set_timer" to False used for the timer in the saving.
set_timer = False

# Setting the value of the variable named "menu" to False used in the menu switch.
menu = False

# Used to check if the user wants to exit the program.
destroy = False

# Setting the value of the variable named "start" to -1.
start = -1

init_distance = None

# Setting the variable named "img_to_save" to None.
img_to_save = None

def save_imgages(img_to_save, imgSaves):
    """
    It takes an image and saves it to a path that the user specifies
    
    :param img_to_save: The image that you want to save
    :param imgSaves: The image that will be saved
    """
    
    # Calling the function named "save" from the file named "utils.py" and assigning the value that it
    # returns to the variable named "save_path".
    save_path = ut.save()
    
    # Saving the image named "img_to_save" to the path that the user specifies with the name of the
    # file being the name of the file that the user specified with "_original" added to the end of it.
    cv2.imwrite(save_path.replace(".jpg", "_original.jpg"), img_to_save)
    
    # Saving the image named "imgSaves" to the path that the user specifies.
    cv2.imwrite(save_path, imgSaves)
    
    print("Saved!")


while True:

    # Reading the video capture and assigning it to the variable named "img" and "img_copy".
    _, img = cap.read()    
    _, img_copy = cap.read()
    
    # Flipping the images horizontally.
    img = cv2.flip(img, 1)
    img_copy = cv2.flip(img_copy, 1)
    
    # Detecting the hand in the image.
    img = detector.findHands(img, draw=False)

    # Detecting the position of the hand.
    lmList = detector.findPosition(img, draw=False)
    

    # The above code is detecting the number of fingers that are up and changing the color of the
    # brush.
    if len(lmList) != 0:

        # Getting the coordinates of the tip of the thumb and the tip of the pinky finger.
        x1, y1 = lmList[8][1], lmList[8][2]
        x2, y2 = lmList[12][1:]
        x3, y3 = lmList[4][1], lmList[4][2]
        
        
        # Detecting the number of fingers that are up.
        fingers = detector.fingersUp()
   
        # Detecting the number of fingers that are up and changing the color of the brush.
        if fingers[1] and fingers[2] and not fingers[0]:
            
            # Setting the initial value of the variables named "xp" and "yp" to 0.
            xp, yp = 0, 0
            
            # Checking if the y coordinate of the tip of the thumb is less than 55 and if the variable
            # named "menu" is False. If both of those are true, then it sets the variable named "menu"
            # to True in order to show the menu
            if y1 < 55 and not menu:
                menu = True
                
            # Checking if the y coordinate of the tip of the thumb is less than 125 and if the
            # variable named "menu" is True. If both of those are true, then it checks if the x
            # coordinate of the tip of the thumb is between 40 and 160. If it is, then it sets the
            # variable named "header" to the first image in the list named "header_imgs". If it is
            # not, then it checks if the x coordinate of the tip of the thumb is between 220 and 340.
            # If it is, then it sets the variable named "header" to the first image in the list named
            # "header_imgs" and sets the variable named "draw_color" to (255, 38, 0) (blue). If it is
            # not, then it checks if the x coordinate of the tip of the thumb is between 400 and 520.
            # If it is, then it sets the variable named "header" to the second image in the list named
            # "header_imgs" and sets the variable named "draw_color" to (0, 0, 254) (red). If it is
            # not, then it checks if the x coordinate of the tip
            elif y1 < 125 and menu:
                
                # Checking if the value of x1 is between 40 and 160.
                if 40 < x1 < 160:
                    header = header_imgs[0]
                    
                # Checking if the x1 value is between 220 and 340. If it is, it will set the header to
                # the first image in the header_imgs list and the draw_color to (255, 38, 0) (blue).
                elif 220 < x1 < 340:
                    header = header_imgs[0]
                    draw_color = (255, 38, 0)
                    
                # Checking if the x1 value is between 400 and 520. If it is, it will set the header to
                # the second image in the header_imgs list and set the draw_color to red.
                elif 400 < x1 < 520:
                    header = header_imgs[1]
                    draw_color = (0, 0, 254)
                    
                # Checking if the x1 value is between 580 and 700. If it is, then it will set the
                # header to the third image in the header_imgs list and the draw_color to green.
                elif 580 < x1 < 700:
                    header = header_imgs[2]
                    draw_color = (14, 127, 0)
                    
                # Checking if the x1 value is between 760 and 880. If it is, then it will set the
                # header to the 4th image in the header_imgs list. It will also set the draw_color to
                # black in order to erase.
                elif 760 < x1 < 880:
                    header = header_imgs[3]
                    draw_color = (0,0,0)
                    
                # Checking if the x1 value is between 940 and 1060. If it is, then it will set the
                # header to the 5th image in the header_imgs list. It will also set the start time and set_timer to
                # True in order to start the countdown.
                elif 940 < x1 < 1060:
                    header = header_imgs[4]
                    if not set_timer:
                        start = time.time()
                        set_timer = True
                        
                # Checking if the x1 value is between 1129 and 1240. If it is, then it will set the
                # header to the 6th image in the header_imgs list. 
                elif 1120 < x1 < 1240:
                    header = header_imgs[5]
                    # Creating a black image of size 720x1280.
                    imgCanvas = np.zeros((720, 1280, 3), np.uint8)

                    # Creating a white image of size 720x1280.
                    imgSaves = np.ones((720, 1280,3),np.uint8)*255
                    
            # Setting the variable named "menu" to False if the y coordinate of the tip of the thumb
            # is not less than 125.
            else:
                menu = False
                
            # Drawing a rectangle on the image named "img" with the top left corner being at the
            # coordinates (x1, y1-25) and the bottom right corner being at the coordinates (x2, y2+25)
            # with a color of the variable named "draw_color" and a thickness of -1.
            cv2.rectangle(img, (x1, y1-25), (x2, y2+25), draw_color, cv2.FILLED)

        # The above code is drawing a line between the coordinates (xp, yp) and (x1, y1) with a color
        # of the variable named "draw_color" and a thickness of the variable named "brushThickness" or
        # "brushThickness" depending on the value of the variable named "draw_color".
        if fingers[1] and not fingers[2] and not fingers[0]:

            # Drawing a circle on the image named "img" with the center being at the coordinates (x1,
            # y1) with a radius of brushThickness, a color of the variable named "draw_color", and a thickness of
            # -1.
            cv2.circle(img, (x1, y1), int(brushThickness/2), draw_color, cv2.FILLED)

            # Setting the initial value of the variables named "xp" and "yp" to the coordinates of the
            # tip of the thumb.
            if xp == 0 and yp == 0:
                xp, yp = x1, y1

            # Drawing a line between the coordinates (xp, yp) and (x1, y1) with a color of the
            # variable named "draw_color" and a thickness of the variable named "brushThickness" or
            # "brushThickness" depending on the value of the variable named "draw_color".
        
            cv2.line(img, (xp, yp), (x1, y1), draw_color, brushThickness)
            cv2.line(imgCanvas, (xp, yp), (x1, y1), draw_color, brushThickness)
            if draw_color == (0, 0, 0):
                cv2.line(imgSaves, (xp, yp), (x1, y1), (255,255,255), brushThickness)
            else:
                cv2.line(imgSaves, (xp, yp), (x1, y1), draw_color, brushThickness)


            # Setting the value of the variables named "xp" and "yp" to the coordinates of the tip of
            # the thumb.
            xp, yp = x1, y1
            
        # Checking if the first two fingers are up. If this is true, increase or decrease the brush thickness.
        if fingers[0] and fingers[1] and not fingers[2]:
            xp, yp = 0, 0
            cv2.circle(img, (x1, y1), int(brushThickness/2), draw_color, cv2.FILLED)
            if init_distance == None:
                init_distance = math.sqrt(
                    (x3-x1)**2 + (y3-y1)**2
                )
            else:
                distance = math.sqrt(
                    (x3-x1)**2 + (y3-y1)**2
                )
                if init_distance < distance and brushThickness < 500:
                    brushThickness += 5
                elif init_distance > distance and brushThickness > 1:
                    brushThickness -= 5
                init_distance = distance
        
            
        # Checking if all the fingers in the list are equal to 1 in order to close the program.
        if all(ele == 1 for ele in fingers):
            destroy = True
            
        # Checking if the fingers are closed.
        if not fingers[0] and not fingers[1] and not fingers[2] and not fingers[3] and not fingers[4]:
            init_distance = None
            
        # Setting a timer to start when the user has all three fingers up in order to save.
        if fingers[0] and fingers[1] and fingers[2] and not fingers[3] and not fingers[4]:
            start = time.time()
            set_timer = True
        
    # Converting the image to grayscale, then inverting it, and then converting it back to BGR.
    imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)

    # Converting the image to grayscale, then inverting it, and then converting it back to BGR.
    # The above code is performing thresholding on a grayscale image `imgGray` using a threshold value
    # of 20. Pixels with intensity values below 20 are set to 255 (white) and pixels with intensity
    # values above or equal to 20 are set to 0 (black). The `cv2.THRESH_BINARY_INV` flag is used to
    # invert the binary image, so that the foreground (white) pixels become black and the background
    # (black) pixels become white. The resulting binary image is stored in the variable `imgInv`.
    _, imgInv = cv2.threshold(imgGray, 20, 255, cv2.THRESH_BINARY_INV)

    # Converting the image to grayscale, then inverting it, and then converting it back to BGR.
    imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)

    # Making the background transparent.
    # The above code is performing a bitwise AND operation between the image 'img' and its inverse
    # 'imgInv'. This operation will result in a new image where the pixels that are common in both
    # images will be retained, while the pixels that are different will be set to zero. This can be
    # useful for various image processing tasks such as masking, thresholding, and segmentation.
    img = cv2.bitwise_and(img, imgInv)
    img_copy = cv2.bitwise_and(img_copy, imgInv)

    img = cv2.bitwise_or(img, imgCanvas)
    img_copy = cv2.bitwise_or(img_copy, imgCanvas)
    
    # Checking if the variable named "menu" is False. If it is, then it sets the top 40 rows
    # of the image named "img" to the image named "menu_img". If it is not, then it sets the top 100
    # rows of the image named "img" to the image named "header".
    if not menu:
        img[0:40, 0:1280] = menu_img
    else:
        img[0:100, 0:1280] = header
    
    # A timer that counts down from 3 to 0.
    if set_timer:
        
        # Printing the timer on the screen.
        if timer >= 0:
            font = cv2.FONT_HERSHEY_SIMPLEX
            textsize = cv2.getTextSize(str(timer), font, 1, 2)[0]
            textX = int((img.shape[1] - textsize[0]) / 2)
            textY = int((img.shape[0] + textsize[1]) / 2)
            
            cv2.putText(img, str(timer),
                        (textX, textY), font,
                        7, (0, 255, 255),
                        4, cv2.LINE_AA)
            
        # Saving the image and resetting the timer.
        else:
            save_imgages(img_to_save, imgSaves)
            set_timer = False
            timer = ut.TIMER
        
        # A timer that counts down from 3 to 0.
        if time.time()-start>=1:
            start = time.time()
            timer-=1
    
    # Assigning the value of the variable named "img_copy" to the variable named "img_to_save".
    img_to_save = img_copy
    
    # Showing the image named "img" in a window named "Image".
    cv2.imshow("Image", img)
    
    
    # Waits 1 milliseconds to show the img
    keys = cv2.waitKey(1)

    # Saving the image.
    if keys == ord('s') and not set_timer:
        start = time.time()
        set_timer = True
        
    # Checking if the user presses the "q" key or if the variable named "destroy" is True or if the
    # window named "Image" is not visible. If any of those are true, then it breaks out of the loop.
    if keys == ord('q') or destroy or cv2.getWindowProperty("Image", cv2.WND_PROP_VISIBLE) < 1:
        break


# Releasing the video capture and destroying all the windows.
cap.release()
cv2.destroyAllWindows()