import cv2
import mediapipe as mp
import tkinter as tk
import time

# Creating a tkinter window.
root = tk.Tk()

def rescale_frame(frame):
    """
    It takes a frame, resizes it to the size of the screen, and returns the resized frame

    :param frame: The frame to be resized
    :return: The frame is being returned.
    """
    # Getting the width and height of the screen.
    width = int(root.winfo_screenwidth())
    height = int(root.winfo_screenheight())
    dim = (width, height)

    # Resizing the frame to the size of the screen.
    return cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)


# It creates an instance of the mediapipe hands solution, and then creates an instance of the Hands
# class.
class HandDetector():
    
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5, complexity=1):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.complexity = complexity

        # Importing the mediapipe hands solution.
        self.mpHands = mp.solutions.hands

        # Creating a new instance of the Hands class.
        self.hands = self.mpHands.Hands(
            self.mode, self.maxHands, self.complexity, self.detectionCon, self.trackCon)

        # Drawing the landmarks on the image.
        self.mpDraw = mp.solutions.drawing_utils

        self.tipIds = [4, 8, 12, 16, 20]
        
    def findHands(self, img, draw=True):
    
        # Converting the image from BGR to RGB.
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Processing the image and returning the results.
        self.results = self.hands.process(imgRGB)

        # Drawing the landmarks on the image.
        if self.results.multi_hand_landmarks:
            for handsLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(
                        img, handsLms, self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, handNumber=0, draw=True):
        """
        It takes an image, a hand number, and a boolean value as input, and returns a list of landmark
        positions
        
        :param img: the image to draw on
        :param handNumber: The index of the hand you want to find the landmarks for, defaults to 0
        (optional)
        :param draw: If True, the function will draw the landmarks on the image, defaults to True
        (optional)
        :return: a list of lists. Each list contains the landmark id, the x coordinate, and the y
        coordinate.
        """
        self.lmList = []
        
        # Finding the position of the hand.
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNumber]
            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                if draw:
                    cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
                self.lmList.append([id, cx, cy])
        return self.lmList

    def fingersUp(self):
        """
        If the tip of the finger is higher than the previous landmark, then it will append a 1 to the
        fingers list. If it isn't, then it will append a 0 to the fingers list
        :return: The fingers list is being returned.
        """
        fingers = []

        # Checking if the tip of the finger is higher than the previous landmark. If it is, then
        # it will append a 1 to the fingers list. If it isn't, then it will append a 0 to the fingers
        # list.
        if self.lmList[self.tipIds[0]][1] < self.lmList[self.tipIds[0]-1][1]:
            fingers.append(1)
        else:
            fingers.append(0)
        
        for id in range(1,5):
            if self.lmList[self.tipIds[id]][2] < self.lmList[self.tipIds[id]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        return fingers


def main():
    """
    The above code is reading the video from the webcam, finding the landmarks on the image, finding the
    position of the hand, resizing the image to the size of the screen, flipping the image horizontally,
    calculating the frames per second, drawing the frames per second on the image, showing the image,
    and checking if the user has pressed the 'q' key. If the user has pressed the 'q' key, then the
    program will stop.
    """

    # Capturing the video from the webcam.
    cap = cv2.VideoCapture(0)

    # cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1256)

    # Initializing the variables.
    pTime = 0

    cTime = 0

    # Creating a new instance of the handDetector class.
    detector = HandDetector()

    # The above code is reading the video from the webcam, finding the landmarks on the image, finding
    # the position of the hand, resizing the image to the size of the screen, flipping the image
    # horizontally, calculating the frames per second, drawing the frames per second on the image,
    # showing the image, and checking if the user has pressed the 'q' key. If the user has pressed the
    # 'q' key, then the program will stop.
    while True:

        # Reading the video from the webcam.
        success, img = cap.read()

        # Drawing the landmarks on the image.
        img = detector.findHands(img)

        # Finding the position of the hand.
        lmList = detector.findPosition(img, draw=False)

        # Resizing the image to the size of the screen.
        img = rescale_frame(img)

        # Flipping the image horizontally.
        img = cv2.flip(img, 1)

        # Calculating the frames per second.
        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime

        # Drawing the frames per second on the image.
        cv2.putText(img, str(int(fps)), (10, 70),
                    cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 3)

        # Showing the image.
        cv2.imshow("Image", img)

        # Checking if the user has pressed the 'q' key. If the user has pressed the 'q' key, then the
        # program will stop.
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


# A way to make sure that the code in the main() function is only executed when the file is run
# directly.
if __name__ == "__main__":
    main()
